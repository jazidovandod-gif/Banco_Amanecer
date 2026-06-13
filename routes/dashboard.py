from flask import Blueprint, render_template, flash
from database.db import get_db
from utils import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_index():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE activo=1")
        total_clientes = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM cuentas WHERE estado='activa'")
        total_cuentas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COALESCE(SUM(saldo),0) as total FROM cuentas WHERE estado='activa'")
        total_saldos = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM transacciones WHERE DATE(fecha)=CURDATE()")
        transacciones_hoy = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT t.*, c.numero_cuenta, cl.nombre, cl.apellido
            FROM transacciones t
            JOIN cuentas c ON t.cuenta_id = c.id
            JOIN clientes cl ON c.cliente_id = cl.id
            ORDER BY t.fecha DESC LIMIT 8
        """)
        ultimas_transacciones = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.*, cl.nombre, cl.apellido
            FROM prestamos p
            JOIN clientes cl ON p.cliente_id = cl.id
            WHERE p.estado='pendiente' ORDER BY p.fecha_solicitud DESC LIMIT 5
        """)
        prestamos_pendientes = cursor.fetchall()
        
        # Datos para Gráficos
        cursor.execute("SELECT tipo, COALESCE(SUM(saldo),0) as total FROM cuentas WHERE estado='activa' GROUP BY tipo")
        saldos_por_tipo = {row['tipo']: float(row['total']) for row in cursor.fetchall()}
        saldo_ahorro = saldos_por_tipo.get('ahorro', 0)
        saldo_corriente = saldos_por_tipo.get('corriente', 0)
        
        cursor.execute("SELECT tipo, COALESCE(SUM(monto),0) as total FROM transacciones GROUP BY tipo")
        trans_por_tipo = {row['tipo']: float(row['total']) for row in cursor.fetchall()}
        vol_depositos = trans_por_tipo.get('deposito', 0)
        vol_retiros = trans_por_tipo.get('retiro', 0)
        vol_transferencias = trans_por_tipo.get('transferencia_salida', 0)
        
        cursor.close()
        db.close()
        
        return render_template('dashboard.html',
            total_clientes=total_clientes,
            total_cuentas=total_cuentas,
            total_saldos=total_saldos,
            transacciones_hoy=transacciones_hoy,
            ultimas_transacciones=ultimas_transacciones,
            prestamos_pendientes=prestamos_pendientes,
            saldo_ahorro=saldo_ahorro,
            saldo_corriente=saldo_corriente,
            vol_depositos=vol_depositos,
            vol_retiros=vol_retiros,
            vol_transferencias=vol_transferencias
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('dashboard.html')
