from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.db import get_db
from utils import login_required, registrar_auditoria

transacciones_bp = Blueprint('transacciones', __name__)

@transacciones_bp.route('/transacciones')
@login_required
def transacciones_index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, c.numero_cuenta, cl.nombre, cl.apellido
        FROM transacciones t
        JOIN cuentas c ON t.cuenta_id = c.id
        JOIN clientes cl ON c.cliente_id = cl.id
        ORDER BY t.fecha DESC LIMIT 100
    """)
    lista = cursor.fetchall()
    cursor.close(); db.close()
    return render_template('transacciones.html', transacciones=lista)

@transacciones_bp.route('/transacciones/nueva', methods=['GET', 'POST'])
@login_required
def nueva_transaccion():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT c.id, c.numero_cuenta, c.tipo, c.saldo, cl.nombre, cl.apellido FROM cuentas c JOIN clientes cl ON c.cliente_id=cl.id WHERE c.estado='activa'")
    cuentas_lista = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            cuenta_id = request.form['cuenta_id']
            tipo = request.form['tipo']
            monto = float(request.form['monto'])
            descripcion = request.form.get('descripcion', '')
            
            cursor2 = db.cursor(dictionary=True)
            cursor2.execute("SELECT saldo FROM cuentas WHERE id=%s", (cuenta_id,))
            cuenta = cursor2.fetchone()
            saldo_anterior = float(cuenta['saldo'])
            
            if tipo in ('retiro', 'transferencia') and monto > saldo_anterior:
                flash('Saldo insuficiente para la operación', 'error')
            elif tipo == 'transferencia':
                cuenta_destino_id = request.form.get('cuenta_destino_id')
                if not cuenta_destino_id or cuenta_id == cuenta_destino_id:
                    flash('Debe seleccionar una cuenta destino válida y diferente a la de origen', 'error')
                else:
                    cursor2.execute("SELECT saldo FROM cuentas WHERE id=%s AND estado='activa'", (cuenta_destino_id,))
                    cuenta_dest = cursor2.fetchone()
                    if not cuenta_dest:
                        flash('La cuenta destino no existe o no está activa', 'error')
                    else:
                        saldo_dest_anterior = float(cuenta_dest['saldo'])
                        
                        # 1. Descontar origen
                        saldo_posterior = saldo_anterior - monto
                        cursor2.execute("UPDATE cuentas SET saldo=%s WHERE id=%s", (saldo_posterior, cuenta_id))
                        cursor2.execute("""
                            INSERT INTO transacciones (cuenta_id, tipo, monto, saldo_anterior, saldo_posterior, descripcion, empleado_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (cuenta_id, 'transferencia_salida', monto, saldo_anterior, saldo_posterior, descripcion, session['empleado_id']))
                        
                        # 2. Sumar destino
                        saldo_dest_posterior = saldo_dest_anterior + monto
                        cursor2.execute("UPDATE cuentas SET saldo=%s WHERE id=%s", (saldo_dest_posterior, cuenta_destino_id))
                        cursor2.execute("""
                            INSERT INTO transacciones (cuenta_id, tipo, monto, saldo_anterior, saldo_posterior, descripcion, empleado_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (cuenta_destino_id, 'transferencia_entrada', monto, saldo_dest_anterior, saldo_dest_posterior, f"Transferencia recibida (Glosa: {descripcion})", session['empleado_id']))
                        
                        db.commit()
                        registrar_auditoria('Transferencia', 'Transacciones', f"Monto: Bs {monto:.2f}, Origen: {cuenta_id}, Destino: {cuenta_destino_id}")
                        flash('Transferencia realizada exitosamente', 'success')
                        return redirect(url_for('transacciones.transacciones_index'))
            else:
                saldo_posterior = saldo_anterior + monto if tipo == 'deposito' else saldo_anterior - monto
                cursor2.execute("UPDATE cuentas SET saldo=%s WHERE id=%s", (saldo_posterior, cuenta_id))
                cursor2.execute("""
                    INSERT INTO transacciones (cuenta_id, tipo, monto, saldo_anterior, saldo_posterior, descripcion, empleado_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cuenta_id, tipo, monto, saldo_anterior, saldo_posterior, descripcion, session['empleado_id']))
                db.commit()
                registrar_auditoria('Nueva transacción', 'Transacciones', f"Tipo: {tipo}, Monto: Bs {monto:.2f}, Cuenta ID: {cuenta_id}, Saldo Anterior: Bs {saldo_anterior:.2f}, Saldo Posterior: Bs {saldo_posterior:.2f}")
                flash('Transacción realizada exitosamente', 'success')
                return redirect(url_for('transacciones.transacciones_index'))
            cursor2.close()
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    cursor.close(); db.close()
    return render_template('nueva_transaccion.html', cuentas=cuentas_lista)
