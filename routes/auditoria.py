from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from database.db import get_db
from utils import login_required, admin_required

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/auditoria')
@login_required
@admin_required
def auditoria_index():
    modulo = request.args.get('modulo', '')
    usuario = request.args.get('usuario', '')
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT a.*, e.nombre, e.apellido, e.cargo, e.usuario as empleado_usuario
        FROM auditoria a
        LEFT JOIN empleados e ON a.empleado_id = e.id
        WHERE 1=1
    """
    params = []
    
    if modulo:
        query += " AND a.modulo = %s"
        params.append(modulo)
    
    if usuario:
        query += " AND (e.usuario LIKE %s OR e.nombre LIKE %s OR e.apellido LIKE %s)"
        params.extend([f"%{usuario}%", f"%{usuario}%", f"%{usuario}%"])
        
    query += " ORDER BY a.fecha DESC LIMIT 200"
    
    cursor.execute(query, tuple(params))
    lista = cursor.fetchall()
    
    # Obtener la lista de módulos únicos para el selector del filtro
    cursor.execute("SELECT DISTINCT modulo FROM auditoria ORDER BY modulo")
    modulos = [row['modulo'] for row in cursor.fetchall()]
    
    cursor.close()
    db.close()
    
    return render_template('auditoria.html', 
                           auditorias=lista, 
                           modulos=modulos,
                           modulo_filtro=modulo,
                           usuario_filtro=usuario)
