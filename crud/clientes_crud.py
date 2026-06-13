from database.db import get_db

def obtener_clientes(estado='1'):
    """Obtiene la lista de clientes filtrada por estado activo/inactivo/todos."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        if estado == 'todos':
            cursor.execute("SELECT * FROM clientes ORDER BY fecha_registro DESC")
        else:
            activo = int(estado) if estado in ('0', '1') else 1
            cursor.execute("SELECT * FROM clientes WHERE activo=%s ORDER BY fecha_registro DESC", (activo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

def crear_cliente(datos):
    """Inserta un nuevo cliente en la base de datos."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nombre, apellido, ci, telefono, email, direccion, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datos['nombre'], 
            datos['apellido'], 
            datos['ci'],
            datos['telefono'], 
            datos['email'], 
            datos['direccion'],
            datos['fecha_nacimiento'] or None
        ))
        db.commit()
    finally:
        cursor.close()
        db.close()
