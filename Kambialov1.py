import requests
import streamlit as st
from datetime import datetime

# =======================
# Función para obtener la mejor tasa Binance P2P
# =======================
def get_binance_usdt_sell_rate():
    """Obtiene el mejor precio de VENTA de USDT en VES desde Binance P2P filtrado por Pago Móvil"""
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

        if not offers:
            return None

        best_offer = offers[0]["adv"]
        best_price = float(best_offer["price"])
        seller = offers[0]["advertiser"]["nickName"]
        min_limit = best_offer["minSingleTransAmount"]
        max_limit = best_offer["dynamicMaxSingleTransAmount"]

        return {
            "price": best_price,
            "seller": seller,
            "min": min_limit,
            "max": max_limit
        }
    except Exception as e:
        print("⚠️ Error obteniendo tasa Binance:", e)
        return None

# =======================
# Función para obtener la tasa oficial del BCV desde Yadio
# =======================
def get_bcv_official_rate():
    """Obtiene la tasa oficial del BCV desde Yadio (último dato)"""
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
        print("⚠️ No se pudo obtener la tasa OFFICIAL de Yadio:", e)
        return None

# =======================
# Configuración de la página
# =======================
st.set_page_config(page_title="Kambialo", page_icon="💱", layout="centered")

# =======================
# CSS general de la app
# =======================
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', sans-serif; background-color: #f9f9f9; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { font-size: 2.8rem; font-weight: 600; text-align: center; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# =======================
# Título
# =======================
st.markdown("<h1>Kambialo 💱</h1>", unsafe_allow_html=True)

# =======================
# Inputs del usuario
# =======================
st.subheader("Calculadora USDT → VES")
precio_usd = st.number_input("💲 Precio del producto en USD", min_value=0.0, value=10.0, step=0.01)

# =======================
# Obtener tasa oficial BCV automáticamente
# =======================
tasa_info = get_bcv_official_rate()
if tasa_info is None:
    tasa_bcv = st.number_input("⚠️ No se pudo obtener la tasa OFFICIAL, ingresa la tasa BCV manualmente (VES/$):", min_value=0.0, value=8.0, step=0.01)
    fecha_cotizacion = None
else:
    tasa_bcv = tasa_info["rate"]
    fecha_cotizacion = tasa_info["fecha"]
    st.markdown(f"""
    <div style="
        background: #e0f7fa;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        font-size: 1.2rem;
        font-weight: 600;
        color: #00796b;
    ">
        Tasa oficial del BCV: {tasa_bcv:.2f} VES/USD<br>
        <span style="font-size:0.9rem; color:#004d40;">Cotización: {fecha_cotizacion}</span>
    </div>
    """, unsafe_allow_html=True)

# =======================
# Obtener tasa Binance
# =======================
oferta = get_binance_usdt_sell_rate()
if oferta:
    tasa_binance = oferta["price"]
else:
    tasa_binance = st.number_input("Ingresa la tasa Binance manualmente (VES/USDT)", min_value=0.0, value=9.0, step=0.01)

# =======================
# Cálculos
# =======================
monto_bs = precio_usd * tasa_bcv
usdt_necesarios = monto_bs / tasa_binance

# =======================
# Mostrar resultados con tarjetas personalizadas
# =======================
st.subheader("📊 Resultados")

# Tarjeta Total en VES
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #ffffff, #f0f2f6);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
">
    <div style="color: #333333; font-size: 1rem; font-weight: 500;">💵 Total en VES</div>
    <div style="color: #1a1a1a; font-size: 1.5rem; font-weight: 600;">{monto_bs:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# Tarjeta Tasa Binance
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #ffffff, #f0f2f6);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
">
    <div style="color: #333333; font-size: 1rem; font-weight: 500;">💱 Tasa Binance</div>
    <div style="color: #1a1a1a; font-size: 1.5rem; font-weight: 600;">{tasa_binance:.2f} VES/USDT</div>
</div>
""", unsafe_allow_html=True)

# Tarjeta USDT necesarios
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #ffffff, #f0f2f6);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
">
    <div style="color: #333333; font-size: 1rem; font-weight: 500;">🪙 USDT necesarios</div>
    <div style="color: #1a1a1a; font-size: 1.5rem; font-weight: 600;">{usdt_necesarios:.2f} USDT</div>
</div>
""", unsafe_allow_html=True)

# =======================
# Mostrar detalles del vendedor si hay oferta
# =======================
if oferta:
    st.markdown("### Detalles del vendedor")
    st.write(f"**Vendedor:** {oferta['seller']}")
    st.write(f"**Límite de transacción:** {oferta['min']} - {oferta['max']} VES")
