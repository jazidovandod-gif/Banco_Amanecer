import os

base_top = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Banco Amanecer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-brand">
        <div class="logo-icon">🏦</div>
        <div>
            <div class="sidebar-brand-name">Banco Amanecer</div>
            <div class="sidebar-brand-sub">Sistema Bancario</div>
        </div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section-title">Principal</div>
      <a href="{{ url_for('dashboard.dashboard_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>Dashboard</a>
      <div class="nav-section-title">Gestión</div>
      <a href="{{ url_for('clientes.clientes_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Clientes</a>
      <a href="{{ url_for('cuentas.cuentas_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>Cuentas</a>
      <a href="{{ url_for('transacciones.transacciones_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>Transacciones</a>
      <a href="{{ url_for('prestamos.prestamos_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Préstamos</a>
      <a href="{{ url_for('tarjetas.tarjetas_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>Tarjetas</a>
      
      {% if session.empleado_cargo == 'Administrador' %}
      <a href="{{ url_for('auditoria.auditoria_index') }}" class="nav-item"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>Auditoría</a>
      {% endif %}
    </nav>
    <div class="sidebar-footer">
        <div class="user-info">
            <div class="user-avatar">{{ session.empleado_nombre[0] if session.empleado_nombre else 'A' }}</div>
            <div>
                <div class="user-name">{{ session.empleado_nombre }}</div>
                <div class="user-role">{{ session.empleado_cargo }}</div>
            </div>
        </div>
        <a href="{{ url_for('auth.logout') }}" class="logout-btn">Cerrar sesión</a>
    </div>
  </aside>
  <main class="main-content">
"""

flash_messages = """
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}{% for cat, msg in messages %}
        <div class="alert alert-{{ cat }}" style="margin-bottom:16px">{{ msg }}</div>
      {% endfor %}{% endif %}
    {% endwith %}
"""

base_bottom = """
  </main>
</div>
</body>
</html>
"""

login_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso — Banco Amanecer</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; height: 100vh; display: flex; background: #fff; overflow: hidden; }
        .login-hero { flex: 1.2; position: relative; background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); display: flex; flex-direction: column; justify-content: center; padding: 10%; color: white; overflow: hidden; }
        .login-hero::before, .login-hero::after { content: ''; position: absolute; border-radius: 50%; background: rgba(255, 255, 255, 0.1); animation: float 10s infinite ease-in-out alternate; }
        .login-hero::before { width: 450px; height: 450px; top: -100px; left: -100px; filter: blur(50px); }
        .login-hero::after { width: 600px; height: 600px; bottom: -200px; right: -100px; animation-delay: -5s; filter: blur(70px); background: rgba(147, 197, 253, 0.15); }
        @keyframes float { 0% { transform: translateY(0) scale(1); } 100% { transform: translateY(40px) scale(1.05); } }
        .brand-content { position: relative; z-index: 10; }
        .brand-logo-icon { font-size: 64px; margin-bottom: 24px; display: inline-block; background: rgba(255, 255, 255, 0.2); padding: 24px; border-radius: 24px; backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 12px 32px rgba(0,0,0,0.1); }
        .brand-title { font-family: 'Outfit', sans-serif; font-size: 3.8rem; font-weight: 700; line-height: 1.1; margin-bottom: 24px; letter-spacing: -1px; text-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .brand-subtitle { font-size: 1.25rem; font-weight: 300; opacity: 0.95; max-width: 420px; line-height: 1.6; }
        .login-wrapper { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; background: #ffffff; position: relative; }
        .login-form-container { width: 100%; max-width: 420px; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(30px); }
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }
        .form-header { margin-bottom: 40px; }
        .form-title { font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 700; color: #0f172a; margin-bottom: 10px; }
        .form-subtitle { color: #64748b; font-size: 1rem; }
        .input-group { margin-bottom: 24px; position: relative; }
        .input-group label { display: block; font-weight: 500; font-size: 0.95rem; color: #334155; margin-bottom: 10px; }
        .input-field { width: 100%; padding: 16px; border: 1px solid #cbd5e1; border-radius: 12px; font-size: 1.05rem; font-family: 'Inter', sans-serif; color: #0f172a; background: #f8fafc; transition: all 0.3s ease; }
        .input-field:focus { outline: none; border-color: #3B82F6; background: #ffffff; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); }
        .input-field::placeholder { color: #94a3b8; }
        .btn-login { width: 100%; padding: 18px; background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; border: none; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; box-shadow: 0 6px 16px rgba(59, 130, 246, 0.3); margin-top: 8px; font-family: 'Inter', sans-serif; }
        .btn-login:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(59, 130, 246, 0.45); }
        .alert { padding: 16px; border-radius: 12px; margin-bottom: 24px; font-size: 0.95rem; display: flex; align-items: center; gap: 12px; animation: shake 0.4s ease-in-out; }
        @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-5px); } 50% { transform: translateX(5px); } 75% { transform: translateX(-5px); } }
        .alert-error { background: #fef2f2; color: #991b1b; border: 1px solid #f87171; }
        @media (max-width: 900px) { body { flex-direction: column; overflow-y: auto; } .login-hero { flex: none; padding: 60px 30px; text-align: center; } .login-hero::before, .login-hero::after { display: none; } .brand-logo-icon { margin: 0 auto 20px auto; display: block; width: max-content; } }
    </style>
</head>
<body>
    <div class="login-hero">
        <div class="brand-content">
            <div class="brand-logo-icon">🌅</div>
            <h1 class="brand-title">Banco<br>Amanecer</h1>
            <p class="brand-subtitle">Innovación financiera para un futuro brillante. Ingresa a tu plataforma administrativa.</p>
        </div>
    </div>
    <div class="login-wrapper">
        <div class="login-form-container">
            <div class="form-header">
                <h2 class="form-title">Bienvenido de vuelta</h2>
                <p class="form-subtitle">Por favor, ingresa tus credenciales corporativas.</p>
            </div>
            """ + flash_messages + """
            <form method="POST" action="{{ url_for('auth.login') }}">
                <div class="input-group">
                    <label>Nombre de Usuario</label>
                    <input type="text" name="usuario" class="input-field" required>
                </div>
                <div class="input-group">
                    <label>Contraseña</label>
                    <input type="password" name="password" class="input-field" required>
                </div>
                <button type="submit" class="btn-login">Acceder al Sistema</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

dashboard_html = base_top + """
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    <div class="topbar">
      <div><div class="page-title">Dashboard</div><div class="page-breadcrumb">Banco Amanecer / Inicio</div></div>
    </div>
    <div class="content">
""" + flash_messages + """
        <div class="stats-grid">
            <div class="stat-card blue"><div class="stat-icon blue">👥</div><div><div class="stat-value">{{ total_clientes or 0 }}</div><div class="stat-label">Clientes Activos</div></div></div>
            <div class="stat-card green"><div class="stat-icon green">💳</div><div><div class="stat-value">{{ total_cuentas or 0 }}</div><div class="stat-label">Cuentas Abiertas</div></div></div>
            <div class="stat-card purple"><div class="stat-icon purple">💰</div><div><div class="stat-value">Bs {{ "{:,.2f}".format(total_saldos or 0) }}</div><div class="stat-label">Total en Depósitos</div></div></div>
            <div class="stat-card orange"><div class="stat-icon orange">📊</div><div><div class="stat-value">{{ transacciones_hoy or 0 }}</div><div class="stat-label">Transacciones Hoy</div></div></div>
        </div>
        
        <div class="two-col" style="margin-bottom: 24px;">
            <div class="card">
                <div class="card-header"><div><div class="card-title">Distribución de Saldos</div></div></div>
                <div style="padding: 24px; display: flex; justify-content: center; align-items: center; height: 300px;">
                    <canvas id="chartSaldos"></canvas>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><div><div class="card-title">Volumen de Transacciones</div></div></div>
                <div style="padding: 24px; height: 300px;">
                    <canvas id="chartTransacciones"></canvas>
                </div>
            </div>
        </div>

        <div class="two-col">
            <div class="card">
                <div class="card-header"><div><div class="card-title">Últimas Transacciones</div></div></div>
                <table>
                    <thead><tr><th>Cliente</th><th>Tipo</th><th>Monto</th><th>Fecha</th></tr></thead>
                    <tbody>
                        {% for t in ultimas_transacciones %}
                        <tr>
                            <td>{{ t.nombre }} {{ t.apellido }}</td>
                            <td>
                                {% if t.tipo == 'deposito' %}<span class="badge badge-success">Depósito</span>
                                {% elif t.tipo == 'retiro' %}<span class="badge badge-danger">Retiro</span>
                                {% elif t.tipo == 'transferencia_salida' %}<span class="badge badge-warning">Transf. Enviada</span>
                                {% elif t.tipo == 'transferencia_entrada' %}<span class="badge badge-success" style="background:#dcfce7;color:#166534;">Transf. Recibida</span>
                                {% else %}<span class="badge badge-info">Transferencia</span>{% endif %}
                            </td>
                            <td>Bs {{ "{:,.2f}".format(t.monto) }}</td>
                            <td>{{ t.fecha.strftime('%d/%m %H:%M') if t.fecha else '-' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="card">
                <div class="card-header"><div><div class="card-title">Préstamos Pendientes</div></div></div>
                <table>
                    <thead><tr><th>Cliente</th><th>Monto</th><th>Estado</th></tr></thead>
                    <tbody>
                        {% for p in prestamos_pendientes %}
                        <tr>
                            <td>{{ p.nombre }} {{ p.apellido }}</td>
                            <td>Bs {{ "{:,.2f}".format(p.monto) }}</td>
                            <td><span class="badge badge-warning">Pendiente</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            // Gráfico de Saldos (Anillo con Porcentajes)
            const ctxSaldos = document.getElementById('chartSaldos').getContext('2d');
            new Chart(ctxSaldos, {
                type: 'doughnut',
                data: {
                    labels: ['Ahorro', 'Corriente'],
                    datasets: [{
                        data: [{{ saldo_ahorro|default(0) }}, {{ saldo_corriente|default(0) }}],
                        backgroundColor: ['#3B82F6', '#F97316'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                plugins: [ChartDataLabels],
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { 
                        legend: { position: 'bottom' },
                        datalabels: {
                            color: '#ffffff',
                            font: { weight: 'bold', size: 16 },
                            formatter: (value, ctx) => {
                                let sum = 0;
                                let dataArr = ctx.chart.data.datasets[0].data;
                                dataArr.forEach(data => { sum += Number(data); });
                                if (sum === 0 || value === 0) return '';
                                let percentage = (value * 100 / sum).toFixed(1) + "%";
                                return percentage;
                            }
                        }
                    } 
                }
            });

            // Gráfico de Transacciones (Barras)
            const ctxTrans = document.getElementById('chartTransacciones').getContext('2d');
            new Chart(ctxTrans, {
                type: 'bar',
                data: {
                    labels: ['Depósitos', 'Retiros', 'Transferencias'],
                    datasets: [{
                        label: 'Monto Total (Bs)',
                        data: [{{ vol_depositos|default(0) }}, {{ vol_retiros|default(0) }}, {{ vol_transferencias|default(0) }}],
                        backgroundColor: ['#22C55E', '#EF4444', '#0EA5E9'],
                        borderRadius: 6
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false },
                        datalabels: { display: false } // Desactivar porcentajes en barras
                    },
                    scales: { y: { beginAtZero: true, grid: { display: false } }, x: { grid: { display: false } } }
                }
            });
        </script>
    </div>
""" + base_bottom

clientes_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Clientes</div><div class="page-breadcrumb">Banco Amanecer / Clientes</div></div>
      <a href="{{ url_for('clientes.nuevo_cliente') }}" class="btn btn-primary">+ Nuevo Cliente</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card">
        <div class="card-header">
          <div><div class="card-title">Lista de Clientes</div></div>
        </div>
        <table>
          <thead><tr><th>#</th><th>Nombre</th><th>C.I.</th><th>Teléfono</th><th>Email</th><th>Registro</th><th>Estado</th></tr></thead>
          <tbody>
            {% for c in clientes %}
            <tr>
              <td>{{ loop.index }}</td>
              <td><strong>{{ c.nombre }} {{ c.apellido }}</strong></td>
              <td>{{ c.ci }}</td>
              <td>{{ c.telefono or '-' }}</td>
              <td>{{ c.email or '-' }}</td>
              <td>{{ c.fecha_registro.strftime('%d/%m/%Y') if c.fecha_registro else '-' }}</td>
              <td>{% if c.activo %}<span class="badge badge-success">Activo</span>{% else %}<span class="badge badge-danger">Inactivo</span>{% endif %}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
""" + base_bottom

nuevo_cliente_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Nuevo Cliente</div><div class="page-breadcrumb">Banco Amanecer / Clientes / Nuevo</div></div>
      <a href="{{ url_for('clientes.clientes_index') }}" class="btn btn-outline">Cancelar</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card" style="max-width:600px;margin:0 auto;">
        <div class="card-header"><div class="card-title">Datos del Cliente</div></div>
        <form method="POST" style="padding:24px;">
            <div class="form-group"><label>Nombre</label><input type="text" name="nombre" class="form-control" required></div>
            <div class="form-group"><label>Apellido</label><input type="text" name="apellido" class="form-control" required></div>
            <div class="form-group"><label>C.I.</label><input type="text" name="ci" class="form-control" required></div>
            <div class="form-group"><label>Teléfono</label><input type="text" name="telefono" class="form-control"></div>
            <div class="form-group"><label>Email</label><input type="email" name="email" class="form-control"></div>
            <div class="form-group"><label>Dirección</label><input type="text" name="direccion" class="form-control"></div>
            <div class="form-group"><label>Fecha de Nacimiento</label><input type="date" name="fecha_nacimiento" class="form-control"></div>
            <button type="submit" class="btn btn-primary">Registrar Cliente</button>
        </form>
      </div>
    </div>
""" + base_bottom

cuentas_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Cuentas Bancarias</div><div class="page-breadcrumb">Banco Amanecer / Cuentas</div></div>
      <a href="{{ url_for('cuentas.nueva_cuenta') }}" class="btn btn-primary">+ Nueva Cuenta</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card">
        <div class="card-header"><div><div class="card-title">Lista de Cuentas</div></div></div>
        <table>
          <thead><tr><th>Número</th><th>Cliente</th><th>C.I.</th><th>Tipo</th><th>Saldo</th><th>Estado</th></tr></thead>
          <tbody>
            {% for c in cuentas %}
            <tr>
              <td><strong>{{ c.numero_cuenta }}</strong></td>
              <td>{{ c.nombre }} {{ c.apellido }}</td>
              <td>{{ c.ci }}</td>
              <td>{{ c.tipo|capitalize }}</td>
              <td>Bs {{ "{:,.2f}".format(c.saldo) }}</td>
              <td><span class="badge badge-success">{{ c.estado }}</span></td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
""" + base_bottom

nueva_cuenta_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Apertura de Cuenta</div><div class="page-breadcrumb">Banco Amanecer / Cuentas / Nueva</div></div>
      <a href="{{ url_for('cuentas.cuentas_index') }}" class="btn btn-outline">Cancelar</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card" style="max-width:600px;margin:0 auto;">
        <div class="card-header"><div class="card-title">Detalles de la Cuenta</div></div>
        <form method="POST" style="padding:24px;">
            <div class="form-group">
                <label>Cliente</label>
                <select name="cliente_id" class="form-control" required>
                    {% for c in clientes %}
                    <option value="{{ c.id }}">{{ c.nombre }} {{ c.apellido }} ({{ c.ci }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label>Tipo de Cuenta</label>
                <select name="tipo" class="form-control" required>
                    <option value="ahorro">Ahorro</option>
                    <option value="corriente">Corriente</option>
                </select>
            </div>
            <div class="form-group">
                <label>Saldo Inicial (Bs)</label>
                <input type="number" step="0.01" name="saldo_inicial" class="form-control" value="0.00" required>
            </div>
            <button type="submit" class="btn btn-primary">Abrir Cuenta</button>
        </form>
      </div>
    </div>
""" + base_bottom

transacciones_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Transacciones</div><div class="page-breadcrumb">Banco Amanecer / Transacciones</div></div>
      <a href="{{ url_for('transacciones.nueva_transaccion') }}" class="btn btn-primary">+ Nueva Transacción</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card">
        <div class="card-header"><div><div class="card-title">Historial de Transacciones</div></div></div>
        <table>
          <thead><tr><th>ID</th><th>Fecha</th><th>Cuenta</th><th>Cliente</th><th>Tipo</th><th>Monto</th><th>Saldo Posterior</th></tr></thead>
          <tbody>
            {% for t in transacciones %}
            <tr>
              <td>#{{ t.id }}</td>
              <td>{{ t.fecha.strftime('%d/%m/%Y %H:%M') if t.fecha else '-' }}</td>
              <td>{{ t.numero_cuenta }}</td>
              <td>{{ t.nombre }} {{ t.apellido }}</td>
              <td>
                {% if t.tipo == 'deposito' %}<span class="badge badge-success">Depósito</span>
                {% elif t.tipo == 'retiro' %}<span class="badge badge-danger">Retiro</span>
                {% elif t.tipo == 'transferencia_salida' %}<span class="badge badge-warning">Transf. Enviada</span>
                {% elif t.tipo == 'transferencia_entrada' %}<span class="badge badge-success" style="background:#dcfce7;color:#166534;">Transf. Recibida</span>
                {% else %}<span class="badge badge-info">Transferencia</span>{% endif %}
              </td>
              <td style="{% if t.tipo in ['retiro', 'transferencia_salida'] %}color:#dc2626;{% else %}color:#16a34a;{% endif %}">
                {% if t.tipo in ['retiro', 'transferencia_salida'] %}-{% else %}+{% endif %}Bs {{ "{:,.2f}".format(t.monto) }}
              </td>
              <td>Bs {{ "{:,.2f}".format(t.saldo_posterior) }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
""" + base_bottom

nueva_transaccion_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Nueva Transacción</div><div class="page-breadcrumb">Banco Amanecer / Transacciones / Nueva</div></div>
      <a href="{{ url_for('transacciones.transacciones_index') }}" class="btn btn-outline">Cancelar</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card" style="max-width:600px;margin:0 auto;">
        <div class="card-header"><div class="card-title">Detalles de la Transacción</div></div>
        <form method="POST" style="padding:24px;">
            <div class="form-group">
                <label>Cuenta Destino/Origen</label>
                <select name="cuenta_id" class="form-control" required>
                    {% for c in cuentas %}
                    <option value="{{ c.id }}">{{ c.numero_cuenta }} - {{ c.nombre }} {{ c.apellido }} (Saldo: Bs {{ "{:,.2f}".format(c.saldo) }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label>Tipo de Transacción</label>
                <select name="tipo" id="tipo_select" class="form-control" required onchange="toggleDestino()">
                    <option value="deposito">Depósito</option>
                    <option value="retiro">Retiro</option>
                    <option value="transferencia">Transferencia entre Cuentas</option>
                </select>
            </div>
            <div class="form-group" id="grupo_destino" style="display: none;">
                <label>Cuenta Destino</label>
                <select name="cuenta_destino_id" id="cuenta_destino_id" class="form-control">
                    <option value="">Seleccione cuenta receptora...</option>
                    {% for c in cuentas %}
                    <option value="{{ c.id }}">{{ c.numero_cuenta }} - {{ c.nombre }} {{ c.apellido }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label>Monto (Bs)</label>
                <input type="number" step="0.01" name="monto" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Descripción / Glosa</label>
                <input type="text" name="descripcion" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Ejecutar Transacción</button>
        </form>
      </div>
      <script>
        function toggleDestino() {
            var tipo = document.getElementById('tipo_select').value;
            var grupoDestino = document.getElementById('grupo_destino');
            var selectDestino = document.getElementById('cuenta_destino_id');
            if (tipo === 'transferencia') {
                grupoDestino.style.display = 'block';
                selectDestino.required = true;
            } else {
                grupoDestino.style.display = 'none';
                selectDestino.required = false;
                selectDestino.value = '';
            }
        }
      </script>
    </div>
""" + base_bottom

prestamos_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Préstamos</div><div class="page-breadcrumb">Banco Amanecer / Préstamos</div></div>
      <a href="{{ url_for('prestamos.solicitar_prestamo') }}" class="btn btn-primary">+ Solicitar Préstamo</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card">
        <div class="card-header"><div><div class="card-title">Listado de Préstamos</div></div></div>
        <table>
          <thead><tr><th>ID</th><th>Cliente</th><th>Monto</th><th>Plazo</th><th>Cuota</th><th>Saldo Pendiente</th><th>Estado</th><th>Acciones</th></tr></thead>
          <tbody>
            {% for p in prestamos %}
            <tr>
              <td>#{{ p.id }}</td>
              <td>{{ p.nombre }} {{ p.apellido }}</td>
              <td>Bs {{ "{:,.2f}".format(p.monto) }}</td>
              <td>{{ p.plazo_meses }} meses</td>
              <td>Bs {{ "{:,.2f}".format(p.cuota_mensual) }}</td>
              <td>Bs {{ "{:,.2f}".format(p.saldo_pendiente) }}</td>
              <td>
                {% if p.estado == 'pendiente' %}<span class="badge badge-warning">Pendiente</span>
                {% elif p.estado == 'aprobado' %}<span class="badge badge-success">Aprobado</span>
                {% elif p.estado == 'rechazado' %}<span class="badge badge-danger">Rechazado</span>
                {% else %}<span class="badge badge-info">Pagado</span>{% endif %}
              </td>
              <td><a href="{{ url_for('prestamos.detalle_prestamo', prestamo_id=p.id) }}" class="btn btn-sm btn-outline">Ver</a></td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
""" + base_bottom

solicitar_prestamo_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Solicitar Préstamo</div><div class="page-breadcrumb">Banco Amanecer / Préstamos / Solicitar</div></div>
      <a href="{{ url_for('prestamos.prestamos_index') }}" class="btn btn-outline">Cancelar</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="card" style="max-width:600px;margin:0 auto;">
        <div class="card-header"><div class="card-title">Datos de la Solicitud</div></div>
        <form method="POST" style="padding:24px;">
            <div class="form-group">
                <label>Cliente (debe tener cuenta activa)</label>
                <select name="cliente_id" class="form-control" required>
                    {% for c in clientes_cuentas %}
                    <option value="{{ c.cliente_id }}">{{ c.nombre }} {{ c.apellido }} ({{ c.ci }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group"><label>Monto Solicitado (Bs)</label><input type="number" step="0.01" name="monto" class="form-control" required></div>
            <div class="form-group"><label>Plazo (Meses)</label><input type="number" name="plazo_meses" class="form-control" required></div>
            <div class="form-group"><label>Tasa de Interés Anual (%)</label><input type="number" step="0.01" name="tasa_interes" class="form-control" value="12" required></div>
            <button type="submit" class="btn btn-primary">Registrar Solicitud</button>
        </form>
      </div>
    </div>
""" + base_bottom

detalle_prestamo_html = base_top + """
    <div class="topbar">
      <div><div class="page-title">Detalle de Préstamo #{{ prestamo.id }}</div><div class="page-breadcrumb">Banco Amanecer / Préstamos / Detalle</div></div>
      <a href="{{ url_for('prestamos.prestamos_index') }}" class="btn btn-outline">Volver</a>
    </div>
    <div class="content">
""" + flash_messages + """
      <div class="two-col">
        <div class="card">
            <div class="card-header"><div class="card-title">Información del Préstamo</div></div>
            <div style="padding:24px;">
                <p><strong>Cliente:</strong> {{ prestamo.nombre }} {{ prestamo.apellido }}</p>
                <p><strong>Monto:</strong> Bs {{ "{:,.2f}".format(prestamo.monto) }}</p>
                <p><strong>Plazo:</strong> {{ prestamo.plazo_meses }} meses</p>
                <p><strong>Tasa de Interés:</strong> {{ prestamo.tasa_interes }}% anual</p>
                <p><strong>Estado:</strong> 
                    {% if prestamo.estado == 'pendiente' %}<span class="badge badge-warning">Pendiente</span>
                    {% elif prestamo.estado == 'aprobado' %}<span class="badge badge-success">Aprobado</span>
                    {% elif prestamo.estado == 'rechazado' %}<span class="badge badge-danger">Rechazado</span>
                    {% else %}<span class="badge badge-info">Pagado</span>{% endif %}
                </p>
                {% if prestamo.estado == 'pendiente' and session.empleado_cargo == 'Administrador' %}
                <div style="display:flex;gap:8px;margin-top:16px;">
                    <form method="POST" action="{{ url_for('prestamos.aprobar_prestamo', prestamo_id=prestamo.id) }}">
                        <button type="submit" class="btn btn-success">Aprobar y Desembolsar</button>
                    </form>
                    <form method="POST" action="{{ url_for('prestamos.rechazar_prestamo', prestamo_id=prestamo.id) }}">
                        <button type="submit" class="btn btn-danger">Rechazar</button>
                    </form>
                </div>
                {% endif %}
            </div>
        </div>
        <div class="card">
            <div class="card-header"><div class="card-title">Plan de Pagos (Cuotas)</div></div>
            <table>
                <thead><tr><th>#</th><th>Vencimiento</th><th>Monto</th><th>Estado</th><th>Acción</th></tr></thead>
                <tbody>
                    {% for c in cuotas %}
                    <tr>
                        <td>{{ c.numero_cuota }}</td>
                        <td>{{ c.fecha_vencimiento.strftime('%d/%m/%Y') }}</td>
                        <td>Bs {{ "{:,.2f}".format(c.monto_cuota) }}</td>
                        <td>
                            {% if c.estado == 'pagada' %}<span class="badge badge-success">Pagada</span>
                            {% else %}<span class="badge badge-warning">Pendiente</span>{% endif %}
                        </td>
                        <td>
                            {% if c.estado == 'pendiente' and prestamo.estado == 'aprobado' %}
                            <form method="POST" action="{{ url_for('prestamos.pagar_cuota', prestamo_id=prestamo.id) }}">
                                <button type="submit" class="btn btn-sm btn-primary">Pagar</button>
                            </form>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
      </div>
    </div>
""" + base_bottom

templates = {
    'login.html': login_html,
    'dashboard.html': dashboard_html,
    'clientes.html': clientes_html,
    'nuevo_cliente.html': nuevo_cliente_html,
    'cuentas.html': cuentas_html,
    'nueva_cuenta.html': nueva_cuenta_html,
    'transacciones.html': transacciones_html,
    'nueva_transaccion.html': nueva_transaccion_html,
    'prestamos.html': prestamos_html,
    'solicitar_prestamo.html': solicitar_prestamo_html,
    'detalle_prestamo.html': detalle_prestamo_html
}

for name, content in templates.items():
    with open(os.path.join(r"G:\banco\templates", name), "w", encoding="utf-8") as f:
        f.write(content)
