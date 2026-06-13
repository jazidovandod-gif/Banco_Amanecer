from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.db import get_db
from utils import login_required, admin_required, registrar_auditoria
from datetime import datetime

prestamos_bp = Blueprint('prestamos', __name__)

@prestamos_bp.route('/prestamos')
@login_required
def prestamos_index():
    estado = request.args.get('estado', 'todos')
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if estado == 'todos':
        cursor.execute("""
            SELECT p.*, cl.nombre, cl.apellido, cl.ci
            FROM prestamos p JOIN clientes cl ON p.cliente_id=cl.id
            ORDER BY p.fecha_solicitud DESC
        """)
    else:
        cursor.execute("""
            SELECT p.*, cl.nombre, cl.apellido, cl.ci
            FROM prestamos p JOIN clientes cl ON p.cliente_id=cl.id
            WHERE p.estado=%s
            ORDER BY p.fecha_solicitud DESC
        """, (estado,))

    lista = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('prestamos.html', prestamos=lista, estado_filtro=estado)

@prestamos_bp.route('/prestamos/solicitar', methods=['GET', 'POST'])
@login_required
def solicitar_prestamo():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT cl.id as cliente_id, cl.nombre, cl.apellido, cl.ci,
               c.id as cuenta_id, c.numero_cuenta, c.tipo, c.saldo
        FROM clientes cl
        JOIN cuentas c ON c.cliente_id = cl.id
        WHERE cl.activo=1 AND c.estado='activa'
        ORDER BY cl.apellido, cl.nombre
    """)
    clientes_cuentas = cursor.fetchall()

    if request.method == 'POST':
        try:
            cliente_id = int(request.form['cliente_id'])
            monto = float(request.form['monto'])
            tasa = float(request.form['tasa_interes'])
            plazo = int(request.form['plazo_meses'])

            tasa_mensual = tasa / 100 / 12
            if tasa_mensual > 0:
                cuota = monto * (tasa_mensual * (1 + tasa_mensual)**plazo) / ((1 + tasa_mensual)**plazo - 1)
            else:
                cuota = monto / plazo

            cursor2 = db.cursor()
            cursor2.execute("""
                INSERT INTO prestamos (cliente_id, monto, tasa_interes, plazo_meses, cuota_mensual, saldo_pendiente, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
            """, (cliente_id, monto, tasa, plazo, round(cuota, 2), monto))
            db.commit()
            cursor2.close()
            cursor.close()
            db.close()
            registrar_auditoria('Solicitud de préstamo', 'Préstamos', f"Monto: Bs {monto:.2f}, Plazo: {plazo} meses, Cliente ID: {cliente_id}")
            flash('Solicitud de préstamo registrada exitosamente. Pendiente de aprobación.', 'success')
            return redirect(url_for('prestamos.prestamos_index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    cursor.close()
    db.close()
    return render_template('solicitar_prestamo.html', clientes_cuentas=clientes_cuentas)

@prestamos_bp.route('/prestamos/<int:prestamo_id>')
@login_required
def detalle_prestamo(prestamo_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, cl.nombre, cl.apellido, cl.ci, cl.telefono, cl.email
        FROM prestamos p JOIN clientes cl ON p.cliente_id=cl.id
        WHERE p.id=%s
    """, (prestamo_id,))
    prestamo = cursor.fetchone()

    if not prestamo:
        flash('Préstamo no encontrado', 'error')
        cursor.close()
        db.close()
        return redirect(url_for('prestamos.prestamos_index'))

    cursor.execute("""
        SELECT cp.*, e.nombre as emp_nombre, e.apellido as emp_apellido
        FROM cuotas_prestamo cp
        LEFT JOIN empleados e ON cp.empleado_id = e.id
        WHERE cp.prestamo_id=%s
        ORDER BY cp.numero_cuota
    """, (prestamo_id,))
    cuotas = cursor.fetchall()

    cuotas_pagadas = sum(1 for c in cuotas if c['estado'] == 'pagada')
    total_pagado = sum(float(c['monto_cuota']) for c in cuotas if c['estado'] == 'pagada')

    empleado_aprobador = None
    if prestamo.get('empleado_id'):
        cursor.execute("SELECT nombre, apellido FROM empleados WHERE id=%s", (prestamo['empleado_id'],))
        empleado_aprobador = cursor.fetchone()

    cursor.close()
    db.close()
    return render_template('detalle_prestamo.html',
        prestamo=prestamo, cuotas=cuotas,
        cuotas_pagadas=cuotas_pagadas, total_pagado=total_pagado,
        empleado_aprobador=empleado_aprobador)

@prestamos_bp.route('/prestamos/<int:prestamo_id>/aprobar', methods=['POST'])
@login_required
@admin_required
def aprobar_prestamo(prestamo_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM prestamos WHERE id=%s AND estado='pendiente'", (prestamo_id,))
        prestamo = cursor.fetchone()
        if not prestamo:
            flash('Préstamo no encontrado o ya fue procesado', 'error')
            cursor.close(); db.close()
            return redirect(url_for('prestamos.prestamos_index'))

        cuenta_id = request.form.get('cuenta_id')
        if not cuenta_id:
            cursor.execute("SELECT id FROM cuentas WHERE cliente_id=%s AND estado='activa' LIMIT 1",
                          (prestamo['cliente_id'],))
            cuenta = cursor.fetchone()
            if not cuenta:
                flash('El cliente no tiene una cuenta activa para el desembolso', 'error')
                cursor.close(); db.close()
                return redirect(url_for('prestamos.detalle_prestamo', prestamo_id=prestamo_id))
            cuenta_id = cuenta['id']

        cursor2 = db.cursor(dictionary=True)

        cursor2.execute("""
            UPDATE prestamos SET estado='aprobado', fecha_aprobacion=NOW(), empleado_id=%s
            WHERE id=%s
        """, (session['empleado_id'], prestamo_id))

        cursor2.execute("SELECT saldo FROM cuentas WHERE id=%s", (cuenta_id,))
        cuenta_data = cursor2.fetchone()
        saldo_anterior = float(cuenta_data['saldo'])
        saldo_posterior = saldo_anterior + float(prestamo['monto'])

        cursor2.execute("UPDATE cuentas SET saldo=%s WHERE id=%s", (saldo_posterior, cuenta_id))
        cursor2.execute("""
            INSERT INTO transacciones (cuenta_id, tipo, monto, saldo_anterior, saldo_posterior, descripcion, empleado_id)
            VALUES (%s, 'deposito', %s, %s, %s, %s, %s)
        """, (cuenta_id, prestamo['monto'], saldo_anterior, saldo_posterior,
              f'Desembolso préstamo #{prestamo_id}', session['empleado_id']))

        try:
            from dateutil.relativedelta import relativedelta
            fecha_base = datetime.now()
            plazo = prestamo['plazo_meses']
            cuota_mensual = float(prestamo['cuota_mensual'])

            for i in range(1, plazo + 1):
                fecha_vencimiento = fecha_base + relativedelta(months=i)
                cursor2.execute("""
                    INSERT INTO cuotas_prestamo (prestamo_id, numero_cuota, monto_cuota, fecha_vencimiento, estado)
                    VALUES (%s, %s, %s, %s, 'pendiente')
                """, (prestamo_id, i, cuota_mensual, fecha_vencimiento.date()))
        except ImportError:
            from datetime import timedelta
            fecha_base = datetime.now()
            plazo = prestamo['plazo_meses']
            cuota_mensual = float(prestamo['cuota_mensual'])

            for i in range(1, plazo + 1):
                fv = fecha_base + timedelta(days=30 * i)
                cursor2.execute("""
                    INSERT INTO cuotas_prestamo (prestamo_id, numero_cuota, monto_cuota, fecha_vencimiento, estado)
                    VALUES (%s, %s, %s, %s, 'pendiente')
                """, (prestamo_id, i, cuota_mensual, fv.date()))

        db.commit()
        cursor2.close()
        cursor.close()
        db.close()
        registrar_auditoria('Aprobación de préstamo', 'Préstamos', f"Préstamo ID: {prestamo_id}, Monto Desembolsado: Bs {prestamo['monto']:.2f}, Cuenta ID: {cuenta_id}")
        flash(f'Préstamo #{prestamo_id} aprobado. Bs {prestamo["monto"]:,.2f} desembolsados.', 'success')
    except Exception as e:
        flash(f'Error al aprobar: {str(e)}', 'error')

    return redirect(url_for('prestamos.detalle_prestamo', prestamo_id=prestamo_id))

@prestamos_bp.route('/prestamos/<int:prestamo_id>/rechazar', methods=['POST'])
@login_required
@admin_required
def rechazar_prestamo(prestamo_id):
    try:
        motivo = request.form.get('motivo_rechazo', 'Sin motivo especificado')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE prestamos SET estado='rechazado', motivo_rechazo=%s, empleado_id=%s
            WHERE id=%s AND estado='pendiente'
        """, (motivo, session['empleado_id'], prestamo_id))
        db.commit()
        cursor.close()
        db.close()
        registrar_auditoria('Rechazo de préstamo', 'Préstamos', f"Préstamo ID: {prestamo_id}, Motivo: {motivo}")
        flash(f'Préstamo #{prestamo_id} rechazado.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('prestamos.detalle_prestamo', prestamo_id=prestamo_id))

@prestamos_bp.route('/prestamos/<int:prestamo_id>/pagar', methods=['POST'])
@login_required
def pagar_cuota(prestamo_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM cuotas_prestamo
            WHERE prestamo_id=%s AND estado='pendiente'
            ORDER BY numero_cuota LIMIT 1
        """, (prestamo_id,))
        cuota = cursor.fetchone()

        if not cuota:
            flash('No hay cuotas pendientes para este préstamo', 'error')
            cursor.close(); db.close()
            return redirect(url_for('prestamos.detalle_prestamo', prestamo_id=prestamo_id))

        cursor2 = db.cursor()
        cursor2.execute("""
            UPDATE cuotas_prestamo SET estado='pagada', fecha_pago=NOW(), empleado_id=%s
            WHERE id=%s
        """, (session['empleado_id'], cuota['id']))

        cursor2.execute("""
            UPDATE prestamos SET saldo_pendiente = saldo_pendiente - %s
            WHERE id=%s
        """, (cuota['monto_cuota'], prestamo_id))

        cursor.execute("""
            SELECT COUNT(*) as pendientes FROM cuotas_prestamo
            WHERE prestamo_id=%s AND estado='pendiente'
        """, (prestamo_id,))
        pendientes = cursor.fetchone()['pendientes']

        if pendientes <= 1:
            cursor2.execute("UPDATE prestamos SET estado='pagado', saldo_pendiente=0 WHERE id=%s", (prestamo_id,))
            flash(f'¡Última cuota pagada! Préstamo #{prestamo_id} completado. 🎉', 'success')
        else:
            flash(f'Cuota #{cuota["numero_cuota"]} pagada exitosamente. Quedan {pendientes - 1} cuotas.', 'success')

        db.commit()
        cursor2.close()
        cursor.close()
        db.close()
        registrar_auditoria('Pago de cuota', 'Préstamos', f"Préstamo ID: {prestamo_id}, Cuota: #{cuota['numero_cuota']}, Monto: Bs {cuota['monto_cuota']:.2f}")
    except Exception as e:
        flash(f'Error al pagar cuota: {str(e)}', 'error')

    return redirect(url_for('prestamos.detalle_prestamo', prestamo_id=prestamo_id))
