import os
import re

replacements = {
    r"url_for\('login'\)": "url_for('auth.login')",
    r"url_for\('logout'\)": "url_for('auth.logout')",
    r"url_for\('dashboard'\)": "url_for('dashboard.dashboard_index')",
    r"url_for\('clientes'\)": "url_for('clientes.clientes_index')",
    r"url_for\('nuevo_cliente'\)": "url_for('clientes.nuevo_cliente')",
    r"url_for\('cuentas'\)": "url_for('cuentas.cuentas_index')",
    r"url_for\('nueva_cuenta'\)": "url_for('cuentas.nueva_cuenta')",
    r"url_for\('transacciones'\)": "url_for('transacciones.transacciones_index')",
    r"url_for\('nueva_transaccion'\)": "url_for('transacciones.nueva_transaccion')",
    r"url_for\('prestamos'\)": "url_for('prestamos.prestamos_index')",
    r"url_for\('prestamos'": "url_for('prestamos.prestamos_index'",
    r"url_for\('solicitar_prestamo'\)": "url_for('prestamos.solicitar_prestamo')",
    r"url_for\('detalle_prestamo'": "url_for('prestamos.detalle_prestamo'",
    r"url_for\('aprobar_prestamo'": "url_for('prestamos.aprobar_prestamo'",
    r"url_for\('rechazar_prestamo'": "url_for('prestamos.rechazar_prestamo'",
    r"url_for\('pagar_cuota'": "url_for('prestamos.pagar_cuota'"
}

templates_dir = r"G:\banco\templates"

for filename in os.listdir(templates_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")

print("All templates updated.")
