import mysql.connector
from config.config import Config

def get_db():
    """Retorna una conexión a la base de datos."""
    return mysql.connector.connect(**Config.DB_CONFIG)
