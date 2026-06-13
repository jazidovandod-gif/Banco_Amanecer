# 📋 DOCUMENTACIÓN — Módulo de Préstamos BancoSys

## 1. Descripción General

El módulo de préstamos permite gestionar el ciclo completo de un préstamo bancario:
desde la solicitud hasta el pago total de todas las cuotas.

---

## 2. Roles del Sistema

### 🏧 Cajero
- **Puede**: Registrar solicitudes de préstamo, ver préstamos, registrar pagos de cuotas.
- **NO puede**: Aprobar o rechazar solicitudes de préstamo.

### 👔 Administrador
- **Puede**: Todo lo que hace el cajero + aprobar y rechazar solicitudes de préstamo.
- Es el único que tiene autoridad para decidir si un préstamo se aprueba o se rechaza.

### 🤖 Sistema (automático)
- Al aprobar un préstamo, el sistema automáticamente:
  1. Deposita el monto del préstamo en la cuenta del cliente.
  2. Genera todas las cuotas mensuales con sus fechas de vencimiento.

---

## 3. Flujo Completo Paso a Paso

### Paso 1: Solicitud (Cajero)
1. El **cliente** se acerca al banco y solicita un préstamo.
2. El **cajero** accede a `Préstamos > Solicitar Préstamo`.
3. Selecciona al cliente (debe tener una cuenta activa).
4. Ingresa: monto, tasa de interés anual (por defecto 12%), y plazo en meses.
5. El sistema calcula la cuota mensual en tiempo real (amortización francesa).
6. El cajero confirma y registra la solicitud.
7. El préstamo queda en estado **PENDIENTE**.

### Paso 2: Evaluación y Decisión (Administrador)
1. El **administrador** ve las solicitudes pendientes en la lista de préstamos.
2. Hace clic en "Ver" para abrir el detalle del préstamo.
3. Revisa la información del cliente y el monto solicitado.
4. Tiene dos opciones:
   - **Aprobar**: Confirma y el sistema desembolsa automáticamente.
   - **Rechazar**: Debe ingresar un motivo de rechazo.

### Paso 3: Desembolso (Sistema Automático)
Al aprobar el préstamo, el sistema ejecuta automáticamente:
1. Cambia el estado del préstamo a **APROBADO**.
2. Registra qué administrador lo aprobó y la fecha.
3. **Deposita el monto** en la cuenta activa del cliente (se crea una transacción).
4. **Genera las cuotas mensuales** con fechas de vencimiento (una por mes).

### Paso 4: Pagos de Cuotas (Cajero)
1. El **cliente** se acerca al banco para pagar su cuota mensual.
2. El **cajero** busca el préstamo y accede al detalle.
3. Hace clic en "Registrar Pago de Cuota".
4. El sistema marca la cuota como **PAGADA** y actualiza el saldo pendiente.
5. Cuando se paga la última cuota, el préstamo cambia a estado **PAGADO**.

---

## 4. Estados del Préstamo

| Estado | Significado | Color |
|---|---|---|
| **Pendiente** | Solicitud registrada, esperando aprobación del administrador | 🟡 Amarillo |
| **Aprobado** | Aprobado y desembolsado. El cliente está pagando cuotas | 🟢 Verde |
| **Rechazado** | El administrador rechazó la solicitud (con motivo) | 🔴 Rojo |
| **Pagado** | Todas las cuotas fueron pagadas. Préstamo finalizado | 🔵 Azul |

## 5. Estados de las Cuotas

| Estado | Significado |
|---|---|
| **Pendiente** | Aún no se ha pagado |
| **Pagada** | El cajero registró el pago |
| **Vencida** | Pasó la fecha de vencimiento sin pago (uso futuro) |

---

## 6. Fórmula de Cálculo

Se utiliza el **sistema de amortización francés** (cuota fija):

```
Cuota Mensual = M × [ r × (1 + r)^n ] / [ (1 + r)^n − 1 ]
```

Donde:
- **M** = Monto del préstamo
- **r** = Tasa de interés mensual (tasa anual / 12 / 100)
- **n** = Número de cuotas (plazo en meses)

### Ejemplo
- Monto: Bs 10,000.00
- Tasa anual: 12% → Tasa mensual: 1%
- Plazo: 12 meses
- **Cuota mensual: Bs 888.49**
- Total a pagar: Bs 10,661.85
- Total intereses: Bs 661.85

---

## 7. Estructura de la Base de Datos

### Tabla `prestamos`
| Campo | Tipo | Descripción |
|---|---|---|
| id | INT | Identificador único |
| cliente_id | INT (FK) | Cliente que solicita el préstamo |
| monto | DECIMAL(15,2) | Monto solicitado |
| tasa_interes | DECIMAL(5,2) | Tasa de interés anual (%) |
| plazo_meses | INT | Plazo en meses |
| cuota_mensual | DECIMAL(15,2) | Cuota mensual calculada |
| saldo_pendiente | DECIMAL(15,2) | Saldo que falta por pagar |
| estado | ENUM | pendiente, aprobado, rechazado, pagado |
| fecha_solicitud | DATETIME | Cuándo se registró la solicitud |
| fecha_aprobacion | DATETIME | Cuándo se aprobó (si aplica) |
| empleado_id | INT (FK) | Empleado que aprobó/rechazó |
| motivo_rechazo | VARCHAR(255) | Motivo del rechazo (NULL si fue aprobado) |

### Tabla `cuotas_prestamo`
| Campo | Tipo | Descripción |
|---|---|---|
| id | INT | Identificador único |
| prestamo_id | INT (FK) | Préstamo al que pertenece |
| numero_cuota | INT | Número de cuota (1, 2, 3...) |
| monto_cuota | DECIMAL(15,2) | Monto a pagar |
| fecha_vencimiento | DATE | Fecha límite de pago |
| fecha_pago | DATETIME | Cuándo se pagó (NULL si no se ha pagado) |
| estado | ENUM | pendiente, pagada, vencida |
| empleado_id | INT (FK) | Cajero que registró el pago |

---

## 8. Restricciones de Seguridad

- Solo empleados autenticados pueden acceder al sistema.
- Solo empleados con cargo **Administrador** pueden aprobar o rechazar préstamos.
- Si un cajero intenta aprobar/rechazar, recibe un mensaje de "Acceso denegado".
- El cliente debe tener al menos una cuenta activa para poder solicitar un préstamo.
