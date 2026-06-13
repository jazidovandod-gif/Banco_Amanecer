from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db
from utils import login_required, registrar_auditoria
import random
import string

cuentas_bp = Blueprint('cuentas', __name__)

@cuentas_bp.route('/cuentas')
@login_required
def cuentas_index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, cl.nombre, cl.apellido, cl.ci
        FROM cuentas c JOIN clientes cl ON c.cliente_id = cl.id
        ORDER BY c.fecha_apertura DESC
    """)
    lista = cursor.fetchall()
    cursor.close(); db.close()
    return render_template('cuentas.html', cuentas=lista)

@cuentas_bp.route('/cuentas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cuenta():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, apellido, ci FROM clientes WHERE activo=1")
    clientes_lista = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            num = ''.join(random.choices(string.digits, k=10))
            cursor2 = db.cursor()
            cursor2.execute("""
                INSERT INTO cuentas (numero_cuenta, tipo, saldo, cliente_id)
                VALUES (%s, %s, %s, %s)
            """, (num, request.form['tipo'], request.form.get('saldo_inicial', 0), request.form['cliente_id']))
            db.commit()
            cursor2.close(); cursor.close(); db.close()
            registrar_auditoria('Apertura de cuenta', 'Cuentas', f"Cuenta Nº: {num}, Tipo: {request.form['tipo']}, Saldo Inicial: Bs {request.form.get('saldo_inicial', 0)}, Cliente ID: {request.form['cliente_id']}")
            flash(f'Cuenta {num} creada exitosamente', 'success')
            return redirect(url_for('cuentas.cuentas_index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    cursor.close(); db.close()
    return render_template('nueva_cuenta.html', clientes=clientes_lista)
