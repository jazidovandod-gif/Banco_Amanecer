from flask import Flask
from config.config import Config

# Importar Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.clientes import clientes_bp
from routes.cuentas import cuentas_bp
from routes.transacciones import transacciones_bp
from routes.prestamos import prestamos_bp
from routes.auditoria import auditoria_bp
from routes.tarjetas import tarjetas_bp

app = Flask(__name__)
app.config.from_object(Config)

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(cuentas_bp)
app.register_blueprint(transacciones_bp)
app.register_blueprint(prestamos_bp)
app.register_blueprint(auditoria_bp)
app.register_blueprint(tarjetas_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
