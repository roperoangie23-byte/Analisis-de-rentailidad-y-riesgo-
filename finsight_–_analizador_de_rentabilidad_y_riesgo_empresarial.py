# 💼 FinSight – Analizador de Rentabilidad y Riesgo Empresarial (Versión mejorada)
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="FinSight", page_icon="💼", layout="wide")

# 💠 Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #F9FAFB;
    }
    h1, h2, h3 {
        color: #002B5B;
    }
    .stButton>button {
        background-color: #0078D7;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 🧭 Encabezado principal
st.markdown("<h1 style='text-align: center;'>💼 FinSight</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Analizador de Rentabilidad y Riesgo Empresarial</h4>", unsafe_allow_html=True)
st.markdown("---")

# 🎯 Entradas del usuario
st.sidebar.header("⚙ Configuración de análisis")
ticker = st.sidebar.text_input("📊 Ticker de la empresa:", "AAPL")
start_date = st.sidebar.date_input("📅 Fecha inicial:", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("📅 Fecha final:", pd.to_datetime("2024-12-31"))

# 🚀 Botón de análisis
if st.sidebar.button("Analizar empresa"):
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if data.empty:
        st.error("❌ No se encontraron datos para el ticker especificado.")
    else:
        st.success(f"✅ Datos descargados correctamente para **{ticker}**")

        # Cálculos
        price_col = "Adj Close" if "Adj Close" in data.columns else "Close"
        data["Daily Return"] = data[price_col].pct_change()
        avg_return = data["Daily Return"].mean()
        std_dev = data["Daily Return"].std()
        sharpe_ratio = avg_return / std_dev if std_dev != 0 else 0

        # 🎯 Mostrar resultados
        col1, col2, col3 = st.columns(3)
        col1.metric("Rentabilidad promedio", f"{avg_return*100:.2f}%")
        col2.metric("Riesgo (volatilidad)", f"{std_dev*100:.2f}%")
        col3.metric("Índice de Sharpe", f"{sharpe_ratio:.2f}")

        st.markdown("---")

        # 📈 Gráfico de precios
        st.subheader("📉 Evolución del precio ajustado")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data[price_col], color='#0078D7', linewidth=2)
        ax.set_title(f"Precio histórico de {ticker}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio ($)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        # 📊 Distribución de retornos
        st.subheader("📊 Distribución de los rendimientos diarios")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.histplot(data["Daily Return"].dropna(), bins=30, kde=True, ax=ax2, color='#009688')
        st.pyplot(fig2)

        # 🧾 Datos recientes
        st.subheader("📘 Últimos datos descargados")
        st.dataframe(data.tail(10), use_container_width=True)

# 🪪 Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 FinSight | Desarrollado por Angie</p>", unsafe_allow_html=True)






