import sys
sys.path.append('.')
import recover

tarjetas_content = recover.base_top + """
<div class="topbar">
  <div><div class="page-title">Tarjetas</div><div class="page-breadcrumb">Banco Amanecer / Tarjetas</div></div>
  <a href="{{ url_for('tarjetas.nueva_tarjeta') }}" class="btn btn-primary">+ Emitir Tarjeta</a>
</div>
<div class="content">
""" + recover.flash_messages + """
<style>
    .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 32px; }
    .credit-card {
        border-radius: 16px; padding: 24px; color: white; position: relative; overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15); transition: transform 0.3s;
        height: 200px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .credit-card:hover { transform: translateY(-5px); }
    .card-visa { background: linear-gradient(135deg, #1a1f71 0%, #00529b 100%); }
    .card-mastercard { background: linear-gradient(135deg, #eb001b 0%, #ff5f00 100%); }
    .card-chip { 
        width: 45px; height: 35px; background: #e0c283; border-radius: 6px; 
        background-image: linear-gradient(-45deg, rgba(255,255,255,0.2) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.2) 75%, transparent 75%, transparent); 
    }
    .card-number { font-family: monospace; font-size: 1.4rem; letter-spacing: 2px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .card-footer { display: flex; justify-content: space-between; align-items: flex-end; }
    .card-name { text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1px; }
    .card-exp { font-size: 0.8rem; }
    .card-logo { font-size: 1.5rem; font-weight: 800; font-style: italic; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .card-status { position: absolute; top: 20px; right: 20px; font-size: 0.8rem; background: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 12px; }
    .card-status.bloqueada { background: #dc2626; }
    .card-actions { margin-top: 12px; display: flex; gap: 8px; align-items: center; }
</style>
<div class="cards-grid">
    {% for t in tarjetas %}
    <div>
        <div class="credit-card {{ 'card-visa' if t.marca == 'Visa' else 'card-mastercard' }}" style="{% if t.estado != 'activa' %}filter: grayscale(100%); opacity: 0.8;{% endif %}">
            <div class="card-status {{ t.estado }}">{{ t.estado|upper }}</div>
            <div class="card-chip"></div>
            <div class="card-number">
                {{ t.numero_tarjeta[:4] }} {{ t.numero_tarjeta[4:8] }} {{ t.numero_tarjeta[8:12] }} {{ t.numero_tarjeta[12:] }}
            </div>
            <div class="card-footer">
                <div>
                    <div class="card-exp">{{ t.fecha_expiracion }}</div>
                    <div class="card-name">{{ t.nombre }} {{ t.apellido }}</div>
                </div>
                <div class="card-logo">{{ t.marca }}</div>
            </div>
        </div>
        <div class="card-actions">
            <form method="POST" action="{{ url_for('tarjetas.cambiar_estado', tarjeta_id=t.id) }}" style="margin:0;">
                {% if t.estado == 'activa' %}
                <input type="hidden" name="estado" value="bloqueada">
                <button type="submit" class="btn btn-sm btn-danger">Bloquear</button>
                {% elif t.estado == 'bloqueada' %}
                <input type="hidden" name="estado" value="activa">
                <button type="submit" class="btn btn-sm btn-success">Desbloquear</button>
                {% endif %}
            </form>
            <div style="font-size:0.8rem; color:var(--text-secondary); margin-left:auto; text-align:right">
                <div>Cta: {{ t.numero_cuenta }}</div>
                <div><strong>{{ t.tipo|capitalize }}</strong> {% if t.tipo == 'credito' %}(Lím: Bs {{ "{:,.2f}".format(t.limite_credito) }}){% endif %}</div>
            </div>
        </div>
    </div>
    {% else %}
    <div style="color:var(--text-secondary)">No hay tarjetas emitidas.</div>
    {% endfor %}
</div>
</div>
""" + recover.base_bottom

nueva_tarjeta_content = recover.base_top + """
<div class="topbar">
  <div><div class="page-title">Emitir Tarjeta</div><div class="page-breadcrumb">Banco Amanecer / Tarjetas / Emitir</div></div>
  <a href="{{ url_for('tarjetas.tarjetas_index') }}" class="btn btn-outline">Cancelar</a>
</div>
<div class="content">
""" + recover.flash_messages + """
  <div class="card" style="max-width:600px;margin:0 auto;">
    <div class="card-header"><div class="card-title">Detalles de la Emisión</div></div>
    <form method="POST" style="padding:24px;">
        <div class="form-group">
            <label>Cuenta Asociada</label>
            <select name="cuenta_id" class="form-control" required>
                {% for c in cuentas %}
                <option value="{{ c.id }}">{{ c.numero_cuenta }} - {{ c.nombre }} {{ c.apellido }} ({{ c.tipo|capitalize }})</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>Tipo de Tarjeta</label>
            <select name="tipo" id="tipo" class="form-control" required onchange="toggleLimite()">
                <option value="debito">Débito</option>
                <option value="credito">Crédito</option>
            </select>
        </div>
        <div class="form-group">
            <label>Marca Emisora</label>
            <select name="marca" class="form-control" required>
                <option value="Visa">Visa</option>
                <option value="MasterCard">MasterCard</option>
            </select>
        </div>
        <div class="form-group" id="div_limite" style="display:none;">
            <label>Límite de Crédito Aprobado (Bs)</label>
            <input type="number" step="0.01" name="limite_credito" class="form-control" value="0">
        </div>
        <button type="submit" class="btn btn-primary" style="margin-top:16px;">Emitir Tarjeta</button>
    </form>
  </div>
</div>
<script>
function toggleLimite() {
    var tipo = document.getElementById('tipo').value;
    document.getElementById('div_limite').style.display = (tipo === 'credito') ? 'block' : 'none';
}
</script>
""" + recover.base_bottom

with open('templates/tarjetas.html', 'w', encoding='utf-8') as f:
    f.write(tarjetas_content)
    
with open('templates/nueva_tarjeta.html', 'w', encoding='utf-8') as f:
    f.write(nueva_tarjeta_content)
