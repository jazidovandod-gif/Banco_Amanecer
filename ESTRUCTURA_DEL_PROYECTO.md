# Estructura Sostenible: Proyecto Banco Amanecer

Este documento explica paso a paso cómo está organizado nuestro proyecto bancario, aplicando las mejores prácticas del patrón de diseño **MVC (Modelo-Vista-Controlador)** adaptado para Flask. Esta arquitectura garantiza que el proyecto sea escalable, fácil de leer y seguro.

---

## 📁 Árbol de Directorios

```text
G:\banco\
│
├── config/                  (1. Capa de Configuración)
│   └── config.py
│
├── database/                (2. Capa de Base de Datos)
│   ├── db.py
│   └── database.sql
│
├── crud/                    (3. Capa de Lógica / Modelo)
│   ├── clientes_crud.py
│   ├── cuentas_crud.py
│   └── ...
│
├── routes/                  (4. Capa de Controladores HTTP)
│   ├── auth.py
│   ├── clientes.py
│   ├── cuentas.py
│   └── ...
│
├── templates/               (5. Capa de Vistas - HTML)
│   ├── login.html
│   └── ...
│
├── static/                  (6. Capa de Estilos Visuales - CSS/JS)
│   ├── css/
│   └── js/
│
├── app.py                   (7. El Núcleo / Inicializador)
└── utils.py                 (8. Utilidades Compartidas)
```

---

## 🔍 Explicación Paso a Paso de Cada Capa

### 1. `config/` (Configuración)
Aquí guardamos **únicamente** variables del entorno y credenciales (como contraseñas, IPs, y llaves secretas).
- **Ejemplo (`config.py`)**: Tiene la configuración `DB_CONFIG` que contiene el usuario `banco_user`. Si mañana el banco cambia de servidor de base de datos, solo tocamos este archivo y no alteramos nada más del código.

### 2. `database/` (Conexión)
Maneja estrictamente la **comunicación física** con MySQL.
- **Ejemplo (`db.py`)**: Importa las credenciales de la carpeta `config/` y devuelve un objeto de conexión abierto (`mysql.connector.connect()`) listo para usarse en el resto de la aplicación.
- **Ejemplo (`database.sql`)**: Guarda el diseño de las tablas por si necesitamos recrear la base de datos desde cero.

### 3. `crud/` (Acceso a Datos / Modelo)
*CRUD significa Create, Read, Update, Delete.* 
Esta carpeta es el **cerebro de operaciones SQL**. Aquí es el ÚNICO lugar donde verás comandos como `SELECT`, `INSERT` o `UPDATE`.
- **Por qué existe:** Evita que las rutas web se llenen de sentencias SQL mezcladas con HTML. Si en el futuro cambiamos MySQL por PostgreSQL, solo modificaremos esta carpeta.
- **Ejemplo (`clientes_crud.py`)**: Tendrá funciones como `def crear_cliente(nombre, apellido, ci):` que solo hacen la inserción y retornan el resultado.

### 4. `routes/` (Controladores)
Actúan como el **"Tráfico de la web"**. Reciben lo que el usuario envía desde su navegador, llaman a las funciones de `crud/`, y le devuelven la pantalla HTML correspondiente.
- **Ejemplo (`routes/clientes.py`)**: 
  1. Recibe una petición `POST` del formulario.
  2. Llama a `crear_cliente(datos)` de la carpeta `crud/`.
  3. Ejecuta un `render_template('clientes.html')` para mostrar la pantalla de éxito.
  4. **No** escribe directamente a MySQL.

### 5. `templates/` (Vistas)
Es la **"Cara"** del sistema. Aquí viven todos los archivos HTML (con variables de Jinja2).
- Estas pantallas solo muestran información, no hacen cálculos complejos ni se conectan a bases de datos directamente.

### 6. `static/` (Recursos Estáticos)
Guarda lo que hace que la página se vea "premium" y dinámica: CSS (Diseño y colores), JS (Animaciones) e Imágenes.

### 7. `app.py` (Núcleo)
Es la **puerta de entrada**. Lo único que hace es:
1. Crear la app de Flask.
2. Cargar las credenciales de la carpeta `config/`.
3. Ensamblar todos los módulos de `routes/` (usando Blueprints).
4. Levantar el servidor web en el puerto `5000`.

### 8. `utils.py` (Ayudantes)
Guarda pedazos de código que se repiten en muchos lados, como por ejemplo la función de "Verificar si el usuario inició sesión" (`@login_required`) o registrar auditorías de seguridad.

---
**Conclusión:**
Esta división permite que, si algo falla en el diseño, vas a `templates/` o `static/`. Si falla una consulta, vas a `crud/`. Y si hay un error en una URL, vas a `routes/`. Es una estructura limpia, predecible y lista para crecer al nivel corporativo.
