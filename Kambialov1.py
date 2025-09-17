import requests
import streamlit as st
from datetime import datetime

# =======================
# Configuración de la página
# =======================
st.set_page_config(page_title="Kambialo", page_icon="💱", layout="wide")

# =======================
# CSS general de la app - ¡Rediseño completo y corrección de colores!
# =======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e0f7fa 0%, #e8eaf6 100%);
        font-family: 'Poppins', sans-serif;
        color: #333333;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
        margin: auto;
    }
    h1 {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        color: #1a1a1a;
        background: -webkit-linear-gradient(45deg, #00796b, #00BCD4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h2 {
        font-size: 2rem;
        font-weight: 600;
        color: #263238;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #cfd8dc;
        padding-bottom: 0.5rem;
    }
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #37474f;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .stCard, .card {
        background-color: #f0f2f6;
        border-radius: 25px;
        padding: 25px;
        box-shadow: 8px 8px 16px rgba(174, 174, 192, 0.2), -8px -8px 16px rgba(255, 255, 255, 0.7);
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: none;
    }
    .stCard:hover, .card:hover {
        box-shadow: 6px 6px 12px rgba(174, 174, 192, 0.15), -6px -6px 12px rgba(255, 255, 255, 0.6);
        transform: translateY(-2px);
    }
    .card-title {
        color: #546e7a;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .card-value {
        color: #263238;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .bcv-card {
        background: linear-gradient(135deg, #e0f2f7, #c1e4f4);
        color: #006064;
    }
    .bcv-card .card-title {
        color: #006064;
    }
    .bcv-card .card-value {
        color: #004d40;
    }
    .bcv-card .card-footer {
        font-size: 0.85rem;
        color: #00796b;
        margin-top: 10px;
    }

    .stNumberInput > div > div > input {
        border-radius: 15px;
        border: 1px solid #cfd8dc;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05), inset -2px -2px 5px rgba(255,255,255,0.8);
        padding: 10px 15px;
        font-size: 1.1rem;
        background-color: #fcfdff;
    }
    .stNumberInput label {
        font-weight: 600;
        color: #455a64;
        margin-bottom: 8px;
    }

    .stButton > button {
        background: linear-gradient(45deg, #00796b, #00BCD4);
        color: white;
        border-radius: 15px;
        padding: 10px 20px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 4px 4px 10px rgba(0, 121, 107, 0.3);
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #00695c, #00ACC1);
        box-shadow: 6px 6px 15px rgba(0, 121, 107, 0.4);
        transform: translateY(-1px);
    }

    /* ¡CORRECCIÓN! Estilo para los mensajes de Streamlit */
    .stAlert {
        border-radius: 15px;
    }
    .stAlert p {
        color: #263238 !important; /* Fuerza el color del texto a un gris oscuro */
        font-weight: 500;
    }
    .stAlert.success {
        background-color: #e8f5e9;
        border-color: #a5d6a7;
    }
    .stAlert.warning {
        background-color: #fffde7;
        border-color: #ffe082;
    }
    .stAlert.error {
        background-color: #fbe9e7;
        border-color: #ffab91;
    }
    .stAlert.info {
        background-color: #e3f2fd;
        border-color: #90caf9;
    }

    .history-item {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.95rem;
        color: #455a64;
    }
    .history-item-value {
        font-weight: 600;
        color: #263238;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# Funciones para obtener datos (con caché)
# ... (las funciones get_binance_usdt_sell_rate y get_bcv_official_rate son las mismas)
# =======================
@st.cache_data(ttl=600)
def get_binance_usdt_sell_rate():
    # ... (código sin cambios)
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL",
        "page": 1,
        "rows": 1,
        "payTypes": ["PagoMovil"],
        "publisherType": None
    }
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        offers = data["data"]
        if not offers: return None
        best_offer = offers[0]["adv"]
        best_price = float(best_offer["price"])
        seller = offers[0]["advertiser"]["nickName"]
        min_limit = best_offer["minSingleTransAmount"]
        max_limit = best_offer["dynamicMaxSingleTransAmount"]
        return { "price": best_price, "seller": seller, "min": min_limit, "max": max_limit }
    except Exception as e:
        st.error(f"⚠️ Error obteniendo tasa Binance: {e}")
        return None

@st.cache_data(ttl=3600)
def get_bcv_official_rate():
    # ... (código sin cambios)
    url = "https://api.yadio.io/compare/1/VES"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data and "official" in data[0]:
            rate = float(data[0]["official"])
            timestamp_ms = int(data[0].get("timestamp", 0))
            fecha = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%d/%m/%Y %H:%M:%S") if timestamp_ms else "Fecha no disponible"
            return {"rate": rate, "fecha": fecha}
        else:
            return None
    except Exception as e:
        st.error(f"⚠️ No se pudo obtener la tasa OFFICIAL de Yadio: {e}")
        return None

# =======================
# Lógica principal de la app
# =======================
st.markdown("<h1>Kambialo 💱</h1>", unsafe_allow_html=True)
st.subheader("Calculadora USDT → VES")
precio_usd = st.number_input("💲 Precio del producto en USD", min_value=0.0, value=10.0, step=0.01, format="%.2f")

col_bcv, col_binance = st.columns(2)

with col_bcv:
    tasa_info = get_bcv_official_rate()
    if tasa_info is None:
        tasa_bcv = st.number_input("⚠️ No se pudo obtener la tasa oficial, ingresa BCV manualmente (VES/$):", min_value=0.0, value=8.0, step=0.01, format="%.2f")
    else:
        tasa_bcv = tasa_info["rate"]
        fecha_cotizacion = tasa_info["fecha"]
        st.markdown(f"""
            <div class="card bcv-card">
                <div class="card-title">Tasa oficial del BCV</div>
                <div class="card-value">{tasa_bcv:.2f} VES/USD</div>
                <div class="card-footer">Cotización: {fecha_cotizacion}</div>
            </div>
        """, unsafe_allow_html=True)

with col_binance:
    oferta = get_binance_usdt_sell_rate()
    if oferta:
        tasa_binance = oferta["price"]
        st.markdown(f"""
            <div class="card">
                <div class="card-title">💱 Tasa Binance (Venta USDT)</div>
                <div class="card-value">{tasa_binance:.2f} VES/USDT</div>
                <div style="font-size:0.85rem; color:#607d8b;">Vendedor: {oferta['seller']}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        tasa_binance = st.number_input("Ingresa la tasa Binance manualmente (VES/USDT)", min_value=0.0, value=9.0, step=0.01, format="%.2f")

monto_bs = precio_usd * tasa_bcv
usdt_necesarios = monto_bs / tasa_binance

st.subheader("📊 Resultados")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="card">
            <div class="card-title">💵 Total en VES</div>
            <div class="card-value">{monto_bs:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card">
            <div class="card-title">💰 USDT necesarios</div>
            <div class="card-value">{usdt_necesarios:.2f} USDT</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if oferta:
        diferencia = tasa_binance - tasa_bcv
        st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #fce4ec, #f8bbd0); color: #ad1457;">
                <div class="card-title" style="color: #ad1457;">Diferencia Tasa</div>
                <div class="card-value" style="color: #880e4f;">{diferencia:.2f} VES</div>
                <div style="font-size:0.85rem; color:#880e4f;">Binance vs BCV</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); color: #1976d2;">
                <div class="card-title" style="color: #1976d2;">Información</div>
                <div class="card-value" style="color: #0d47a1;">Datos incompletos</div>
                <div style="font-size:0.85rem; color:#0d47a1;">No se calculó diferencia</div>
            </div>
        """, unsafe_allow_html=True)


# =======================
# Historial de Cálculos
# =======================
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("---")

col_save, col_clear_history = st.columns([0.7, 0.3])

with col_save:
    if st.button("💾 Guardar Cálculo Actual"):
        if precio_usd > 0 and tasa_bcv > 0 and tasa_binance > 0:
            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "precio_usd": precio_usd,
                "tasa_bcv": tasa_bcv,
                "tasa_binance": tasa_binance,
                "monto_bs": monto_bs,
                "usdt_necesarios": usdt_necesarios
            })
            st.success("¡Cálculo guardado en el historial!")
        else:
            st.warning("No se puede guardar un cálculo con valores en cero.")

with col_clear_history:
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.history = []
        st.success("Historial limpiado.")

st.subheader("📜 Historial de Cálculos")

if st.session_state.history:
    for entry in reversed(st.session_state.history):
        st.markdown(f"""
            <div class="history-item">
                <div>
                    <span style="font-weight: 500;">{entry['timestamp']}</span><br>
                    USD: <span class="history-item-value">{entry['precio_usd']:.2f}</span> |
                    BCV: <span class="history-item-value">{entry['tasa_bcv']:.2f}</span> |
                    Binance: <span class="history-item-value">{entry['tasa_binance']:.2f}</span>
                </div>
                <div>
                    VES: <span class="history-item-value">{entry['monto_bs']:,.2f}</span><br>
                    USDT: <span class="history-item-value">{entry['usdt_necesarios']:.2f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("El historial de cálculos está vacío. ¡Haz tu primer cálculo y guárdalo!")

# =======================
# Detalles del vendedor
# =======================
if oferta:
    st.markdown("---")
    st.subheader("Detalles del Vendedor en Binance P2P")
    # ¡CORRECCIÓN! Usando markdown para mejor control del estilo
    st.markdown(f"""
    <div style="font-weight:600; color: #263238;">👤 Vendedor: <span style="font-weight:400;">{oferta['seller']}</span></div>
    <div style="font-weight:600; color: #263238;">💲 Límite de transacción: <span style="font-weight:400;">{float(oferta['min']):,.2f} - {float(oferta['max']):,.2f} VES</span></div>
    """, unsafe_allow_html=True)