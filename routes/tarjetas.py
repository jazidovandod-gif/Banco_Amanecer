from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from database.db import get_db
from utils import login_required, registrar_auditoria
import random
import datetime

tarjetas_bp = Blueprint('tarjetas', __name__)

def generar_numero_tarjeta(marca):
    prefix = "4" if marca == "Visa" else "5"
    rest = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    # Formatear el número con espacios (xxxx xxxx xxxx xxxx) para uso visual si se requiere, 
    # pero guardamos como string continuo de 16 dígitos.
    return prefix + rest

def generar_cvv():
    return str(random.randint(100, 999))

def generar_fecha_expiracion():
    now = datetime.datetime.now()
    mes = str(now.month).zfill(2)
    anio = str(now.year + 5)[-2:] # Validez de 5 años
    return f"{mes}/{anio}"

@tarjetas_bp.route('/tarjetas')
@login_required
def tarjetas_index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.numero_cuenta, cl.nombre, cl.apellido 
        FROM tarjetas t
        JOIN cuentas c ON t.cuenta_id = c.id
        JOIN clientes cl ON c.cliente_id = cl.id
        ORDER BY t.fecha_emision DESC
    """)
    tarjetas = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tarjetas.html', tarjetas=tarjetas)

@tarjetas_bp.route('/tarjetas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_tarjeta():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        cuenta_id = request.form['cuenta_id']
        tipo = request.form['tipo']
        marca = request.form['marca']
        limite = float(request.form.get('limite_credito', 0))
        
        numero = generar_numero_tarjeta(marca)
        cvv = generar_cvv()
        expiracion = generar_fecha_expiracion()
        
        try:
            cursor.execute("""
                INSERT INTO tarjetas (cuenta_id, numero_tarjeta, tipo, marca, fecha_expiracion, cvv, limite_credito)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (cuenta_id, numero, tipo, marca, expiracion, cvv, limite))
            db.commit()
            
            cursor.execute("SELECT numero_cuenta FROM cuentas WHERE id = %s", (cuenta_id,))
            num_cta = cursor.fetchone()['numero_cuenta']
            
            registrar_auditoria('Emisión de tarjeta', 'Tarjetas', f"Marca: {marca}, Tipo: {tipo}, Cuenta: {num_cta}, Límite: {limite}")
            flash(f'Tarjeta {marca} ({tipo}) terminada en {numero[-4:]} emitida exitosamente.', 'success')
            return redirect(url_for('tarjetas.tarjetas_index'))
        except Exception as e:
            flash(f'Error al emitir tarjeta: {str(e)}', 'error')
            
    cursor.execute("""
        SELECT c.id, c.numero_cuenta, cl.nombre, cl.apellido, c.saldo, c.tipo
        FROM cuentas c
        JOIN clientes cl ON c.cliente_id = cl.id
        WHERE c.estado = 'activa'
    """)
    cuentas = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('nueva_tarjeta.html', cuentas=cuentas)

@tarjetas_bp.route('/tarjetas/<int:tarjeta_id>/estado', methods=['POST'])
@login_required
def cambiar_estado(tarjeta_id):
    nuevo_estado = request.form['estado']
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE tarjetas SET estado = %s WHERE id = %s", (nuevo_estado, tarjeta_id))
        db.commit()
        registrar_auditoria('Cambio estado tarjeta', 'Tarjetas', f"Tarjeta ID {tarjeta_id} cambiada a {nuevo_estado}")
        flash(f'El estado de la tarjeta se actualizó a: {nuevo_estado}.', 'success')
    except Exception as e:
        flash(f'Error al cambiar estado: {str(e)}', 'error')
    finally:
        cursor.close()
        db.close()
        
    return redirect(url_for('tarjetas.tarjetas_index'))
