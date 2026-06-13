import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"
CAPTURAS_DIR = "capturas"

if not os.path.exists(CAPTURAS_DIR):
    os.makedirs(CAPTURAS_DIR)

rutas_comunes = {
    "dashboard": "/dashboard",
    "clientes": "/clientes",
    "nuevo_cliente": "/clientes/nuevo",
    "cuentas": "/cuentas",
    "nueva_cuenta": "/cuentas/nueva",
    "transacciones": "/transacciones",
    "nueva_transaccion": "/transacciones/nueva",
    "prestamos": "/prestamos",
    "solicitar_prestamo": "/prestamos/solicitar",
    "tarjetas": "/tarjetas"
}

ruta_admin = {
    "auditoria": "/auditoria"
}

def tomar_capturas(page, rol, usuario, password):
    print(f"[{rol}] Iniciando sesión...")
    # Go to root, which should redirect to login, or go to login explicitly
    page.goto(f"{BASE_URL}/login")
    
    # Fill login form
    page.fill('input[name="usuario"]', usuario)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    
    # Wait for dashboard to load
    page.wait_for_selector(".main-content", timeout=5000)
    time.sleep(1) # Extra wait for animations
    
    print(f"[{rol}] Sesión iniciada. Tomando capturas...")
    
    todas_rutas = {**rutas_comunes}
    if rol == "Admin":
        todas_rutas.update(ruta_admin)
        
    for nombre, ruta in todas_rutas.items():
        print(f"[{rol}] Capturando {nombre}...")
        url = f"{BASE_URL}{ruta}"
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(0.5) # Wait for rendering
            # Save screenshot
            path = os.path.join(CAPTURAS_DIR, f"{rol.lower()}_{nombre}.png")
            page.screenshot(path=path, full_page=True)
        except Exception as e:
            print(f"[{rol}] Error capturando {nombre} en {url}: {e}")

    # Logout
    try:
        page.goto(f"{BASE_URL}/logout")
        page.wait_for_load_state("networkidle", timeout=5000)
    except:
        pass

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        # Admin
        tomar_capturas(page, "Admin", "admin", "admin123")
        
        # Cajero
        tomar_capturas(page, "Cajero", "jperez", "cajero123")
        
        browser.close()
        print("¡Todas las capturas se han guardado exitosamente!")

if __name__ == "__main__":
    run()
