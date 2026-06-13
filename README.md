<div align="center">
  <img src="capturas/admin/admin_dashboard.png" width="800" alt="Dashboard Banco Amanecer" style="border-radius: 10px;">

  <h1>🌅 Banco Amanecer</h1>
  <p><strong>Un Sistema Bancario Moderno, Escalable y Seguro</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  </p>
</div>

---

## 📖 Acerca del Proyecto

**Banco Amanecer** es una plataforma de gestión bancaria desarrollada con el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** en Python/Flask. Está diseñada para ofrecer una interfaz fluida, interactiva y de aspecto premium para el personal interno del banco (Cajeros y Administradores).

## ✨ Características Principales

- 📊 **Panel de Control Interactivo**: Visualización gráfica (Chart.js) en tiempo real de los saldos y volúmenes de transacciones.
- 👥 **Gestión de Clientes**: Creación y administración de perfiles detallados de clientes.
- 💳 **Cuentas y Tarjetas**: Administración de cuentas de ahorro/corriente y emisión de tarjetas.
- 💸 **Transacciones Financieras**: Sistema robusto para depósitos, retiros y transferencias entre cuentas.
- 🏦 **Módulo de Préstamos**: Flujo completo de solicitud, aprobación, y cálculo de plan de pagos en cuotas.
- 🔒 **Roles y Permisos**: Accesos diferenciados. Los Administradores tienen acceso total (incluyendo el registro de **Auditoría**), mientras que los Cajeros tienen un acceso operativo.

---

## 📸 Capturas de Pantalla

### 🛡️ Vista de Administrador
<div align="center">
  <img src="capturas/admin/admin_dashboard.png" width="48%">
  <img src="capturas/admin/admin_clientes.png" width="48%">
  <br>
  <img src="capturas/admin/admin_prestamos.png" width="48%">
  <img src="capturas/admin/admin_auditoria.png" width="48%">
</div>

### 🧑‍💼 Vista de Cajero
<div align="center">
  <img src="capturas/cajero/cajero_nueva_transaccion.png" width="48%">
  <img src="capturas/cajero/cajero_cuentas.png" width="48%">
</div>

---

## 🚀 Instalación y Uso Local

Sigue estos pasos para ejecutar el sistema en tu propio computador:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/jazidovandod-gif/Banco_Amanecer.git
   cd Banco_Amanecer
   ```

2. **Instalar las dependencias:**
   Asegúrate de tener Python instalado y ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la Base de Datos:**
   - Instala y ejecuta **MySQL** (por ejemplo, a través de XAMPP).
   - Crea la base de datos importando el archivo `database.sql`:
     ```bash
     mysql -u tu_usuario -p < database.sql
     ```
   - *Nota:* Asegúrate de actualizar tus credenciales de MySQL en `config/config.py`.

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

5. **Acceder:**
   Abre tu navegador y ve a `http://127.0.0.1:5000`. Puedes iniciar sesión con los usuarios por defecto:
   - Administrador: `admin` / `admin123`
   - Cajero: `jperez` / `cajero123`

---

## 📂 Arquitectura del Proyecto (MVC)

El proyecto mantiene una estricta separación de responsabilidades:
- `config/`: Credenciales y configuración del entorno.
- `database/`: Capa física de conexión a MySQL.
- `crud/` (Modelo): Consultas SQL e interacciones con los datos.
- `routes/` (Controladores): Blueprints de Flask que manejan el flujo HTTP.
- `templates/` & `static/` (Vistas): Interfaz HTML estilizada con CSS puro.

---
<div align="center">
  <i>Desarrollado con pasión para transformar las finanzas.</i>
</div>
