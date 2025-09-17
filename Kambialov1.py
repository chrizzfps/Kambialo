import requests
import streamlit as st

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
tasa_bcv = st.number_input("Tasa BCV (VES/$)", min_value=0.0, value=8.0, step=0.01)

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
