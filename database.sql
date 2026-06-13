-- SISTEMA BANCARIO - Base de Datos

CREATE DATABASE IF NOT EXISTS banco_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE banco_db;

-- Tabla de empleados (usuarios del sistema)
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo VARCHAR(80) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    ci VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(120),
    direccion TEXT,
    fecha_nacimiento DATE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1
);

-- Tabla de cuentas bancarias
CREATE TABLE IF NOT EXISTS cuentas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    tipo ENUM('ahorro', 'corriente') NOT NULL DEFAULT 'ahorro',
    saldo DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    cliente_id INT NOT NULL,
    fecha_apertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('activa', 'suspendida', 'cerrada') DEFAULT 'activa',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Tabla de transacciones
CREATE TABLE IF NOT EXISTS transacciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cuenta_id INT NOT NULL,
    tipo ENUM('deposito', 'retiro', 'transferencia_entrada', 'transferencia_salida') NOT NULL,
    monto DECIMAL(15, 2) NOT NULL,
    saldo_anterior DECIMAL(15, 2),
    saldo_posterior DECIMAL(15, 2),
    descripcion VARCHAR(255),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    empleado_id INT,
    FOREIGN KEY (cuenta_id) REFERENCES cuentas(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

-- Tabla de préstamos
CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    monto DECIMAL(15, 2) NOT NULL,
    tasa_interes DECIMAL(5, 2) NOT NULL,
    plazo_meses INT NOT NULL,
    cuota_mensual DECIMAL(15, 2),
    saldo_pendiente DECIMAL(15, 2),
    estado ENUM('pendiente', 'aprobado', 'rechazado', 'pagado') DEFAULT 'pendiente',
    fecha_solicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_aprobacion DATETIME,
    empleado_id INT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

-- Tabla de cuotas de préstamos
CREATE TABLE IF NOT EXISTS cuotas_prestamo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prestamo_id INT NOT NULL,
    numero_cuota INT NOT NULL,
    monto_cuota DECIMAL(15, 2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATETIME,
    estado ENUM('pendiente', 'pagada', 'vencida') DEFAULT 'pendiente',
    empleado_id INT,
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);

-- Tabla de auditoría (Registro de eventos)
CREATE TABLE IF NOT EXISTS auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    accion VARCHAR(100) NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    detalles TEXT,
    ip_address VARCHAR(45),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);

-- Tabla de tarjetas de débito/crédito
CREATE TABLE IF NOT EXISTS tarjetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cuenta_id INT NOT NULL,
    numero_tarjeta VARCHAR(16) NOT NULL UNIQUE,
    tipo ENUM('debito', 'credito') NOT NULL,
    marca ENUM('Visa', 'MasterCard') NOT NULL,
    fecha_expiracion VARCHAR(5) NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    limite_credito DECIMAL(15, 2) DEFAULT 0,
    estado ENUM('activa', 'bloqueada', 'cancelada') DEFAULT 'activa',
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cuenta_id) REFERENCES cuentas(id) ON DELETE CASCADE
);

-- DATOS INICIALES

-- Empleado administrador (password: admin123)
INSERT INTO empleados (nombre, apellido, cargo, usuario, password, email) VALUES
('Admin', 'Sistema', 'Administrador', 'admin', 'admin123', 'admin@banco.com'),
('Juan', 'Perez', 'Cajero', 'jperez', 'cajero123', 'jperez@banco.com');

-- Clientes de ejemplo
INSERT INTO clientes (nombre, apellido, ci, telefono, email, direccion, fecha_nacimiento) VALUES
('Carlos', 'Mamani', '1234567', '70123456', 'carlos@gmail.com', 'Av. Principal 123', '1990-03-15'),
('Maria', 'Flores', '7654321', '71234567', 'maria@gmail.com', 'Calle 2 Norte', '1985-07-22'),
('Luis', 'Quispe', '9876543', '69876543', 'luis@gmail.com', 'Zona Central 456', '1992-11-10');

-- Cuentas de ejemplo
INSERT INTO cuentas (numero_cuenta, tipo, saldo, cliente_id) VALUES
('1000000001', 'ahorro', 5000.00, 1),
('1000000002', 'corriente', 12000.00, 2),
('1000000003', 'ahorro', 850.50, 3);
