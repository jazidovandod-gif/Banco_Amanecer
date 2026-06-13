from functools import wraps
from flask import session, redirect, url_for, flash, request

def registrar_auditoria(accion, modulo, detalles=None):
    """Registra una acción en la tabla de auditoría.
    Obtiene automáticamente el empleado_id de la sesión actual y la dirección IP.
    """
    try:
        from database.db import get_db
        db = get_db()
        cursor = db.cursor()
        
        empleado_id = session.get('empleado_id')
        ip_address = request.remote_addr if request else '127.0.0.1'
        
        cursor.execute("""
            INSERT INTO auditoria (empleado_id, accion, modulo, detalles, ip_address)
            VALUES (%s, %s, %s, %s, %s)
        """, (empleado_id, accion, modulo, detalles, ip_address))
        
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error al registrar auditoría: {str(e)}")

def login_required(f):
    """Decorador para requerir que el usuario haya iniciado sesión."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'empleado_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorador para requerir permisos de Administrador."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('empleado_cargo') != 'Administrador':
            flash('Acceso denegado: solo Administradores pueden realizar esta acción', 'error')
            return redirect(url_for('prestamos.prestamos_index'))
        return f(*args, **kwargs)
    return decorated
