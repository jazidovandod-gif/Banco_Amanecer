import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'banco_secreto_2026')
    
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'banco_user',
        'password': 'banco123',
        'database': 'banco_db',
        'charset': 'utf8mb4'
    }
