from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import get_db
from utils import registrar_auditoria
import datetime

auth_bp = Blueprint('auth', __name__)

# Diccionario en memoria para rastrear intentos por usuario
intentos_login = {}

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'empleado_id' in session:
        return redirect(url_for('dashboard.dashboard_index'))
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        ahora = datetime.datetime.now()
        
        # Verificar si el usuario está actualmente bloqueado
        if usuario in intentos_login:
            datos = intentos_login[usuario]
            if datos['bloqueado_hasta']:
                if ahora < datos['bloqueado_hasta']:
                    faltan = (datos['bloqueado_hasta'] - ahora).seconds
                    flash(f'Cuenta bloqueada por seguridad. Intente de nuevo en {faltan} segundos.', 'error')
                    return render_template('login.html')
                else:
                    # El tiempo de bloqueo ya expiró
                    intentos_login[usuario] = {'intentos': 0, 'bloqueado_hasta': None}
        else:
            intentos_login[usuario] = {'intentos': 0, 'bloqueado_hasta': None}
            
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM empleados WHERE usuario=%s AND password=%s AND activo=1", (usuario, password))
            empleado = cursor.fetchone()
            cursor.close()
            db.close()
            
            if empleado:
                # Login exitoso: reiniciar el contador
                if usuario in intentos_login:
                    del intentos_login[usuario]
                    
                session['empleado_id'] = empleado['id']
                session['empleado_nombre'] = f"{empleado['nombre']} {empleado['apellido']}"
                session['empleado_cargo'] = empleado['cargo']
                registrar_auditoria('Login exitoso', 'Autenticación', f"Usuario: {usuario}")
                return redirect(url_for('dashboard.dashboard_index'))
            else:
                # Login fallido: incrementar contador
                intentos_login[usuario]['intentos'] += 1
                intentos_actuales = intentos_login[usuario]['intentos']
                
                if intentos_actuales >= 3:
                    # Bloquear por 1 minuto
                    intentos_login[usuario]['bloqueado_hasta'] = ahora + datetime.timedelta(minutes=1)
                    registrar_auditoria('Bloqueo de cuenta temporal', 'Autenticación', f"Usuario bloqueado por 1 min. ({intentos_actuales} intentos fallidos)")
                    flash('Demasiados intentos fallidos. Por seguridad, debe esperar 1 minuto.', 'error')
                else:
                    intentos_restantes = 3 - intentos_actuales
                    registrar_auditoria('Intento de login fallido', 'Autenticación', f"Usuario intentado: {usuario}. Restantes: {intentos_restantes}")
                    flash(f'Usuario o contraseña incorrectos. Le quedan {intentos_restantes} intento(s).', 'error')

        except Exception as e:
            flash(f'Error de conexión: {str(e)}', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    if 'empleado_id' in session:
        registrar_auditoria('Cierre de sesión', 'Autenticación')
    session.clear()
    return redirect(url_for('auth.login'))
