from flask import Blueprint, render_template, request, redirect, url_for, flash
from crud.clientes_crud import obtener_clientes, crear_cliente
from utils import login_required, registrar_auditoria

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes')
@login_required
def clientes_index():
    estado = request.args.get('estado', '1')
    lista = obtener_clientes(estado)
    return render_template('clientes.html', clientes=lista, estado_filtro=estado)

@clientes_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    if request.method == 'POST':
        try:
            crear_cliente(request.form)
            registrar_auditoria('Registro de cliente', 'Clientes', f"Cliente: {request.form['nombre']} {request.form['apellido']} (CI: {request.form['ci']})")
            flash('Cliente registrado exitosamente', 'success')
            return redirect(url_for('clientes.clientes_index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    return render_template('nuevo_cliente.html')

