# -- coding: utf-8 --
"""
FinSight - Analizador de Rentabilidad y Riesgo Empresarial
Aplicación Streamlit para análisis financiero de empresas
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="FinSight", layout="wide")

# 🎯 Encabezado principal
st.title("💼 FinSight – Analizador de Rentabilidad y Riesgo Empresarial")
st.write("Explora el desempeño financiero de distintas empresas a través de indicadores de rentabilidad y riesgo.")

# 🧭 Selección de tickers
default_tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]
tickers_input = st.sidebar.text_input(
    "Tickers (separados por comas)",
    value=",".join(default_tickers)
)
tickers = [t.strip().upper() for t in tickers_input.split(",")]

# 📅 Fechas
start_date = st.date_input("Fecha inicial:", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Fecha final:", pd.to_datetime("2024-12-31"))

# 📈 Descargar datos
if st.button("Analizar"):
    data = yf.download(tickers, start=start_date, end=end_date)

    if data.empty:
        st.error("No se encontraron datos para los tickers especificados.")
    else:
        st.success(f"Datos descargados exitosamente para: {', '.join(tickers)}")

        # 🧠 --- 🔧 Corrección del error KeyError: 'Adj Close'
        if isinstance(data.columns, pd.MultiIndex):
            data = data["Adj Close"]

        # 🧮 Cálculos
        data["Daily Return"] = data.pct_change()
        avg_return = data["Daily Return"].mean()
        std_dev = data["Daily Return"].std()
        sharpe_ratio = avg_return / std_dev

        # 📊 Mostrar métricas
        metrics_df = pd.DataFrame({
            'Indicador': ['Rentabilidad promedio (%)', 'Riesgo (Desviación estándar %)', 'Sharpe Ratio promedio'],
            'Valor': [avg_return.mean() * 100, std_dev.mean() * 100, sharpe_ratio.mean()]
        })
        st.table(metrics_df)

        # 📈 Gráfico de precios ajustados
        st.subheader("Evolución del precio ajustado")
        fig, ax = plt.subplots()
        data.plot(ax=ax, linewidth=2)
        ax.set_title("Precio ajustado de las empresas seleccionadas")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio ($)")
        st.pyplot(fig)

        # 📉 Histograma de rendimientos diarios
        st.subheader("Distribución de los rendimientos diarios")
        fig2, ax2 = plt.subplots()
        sns.histplot(data["Daily Return"].dropna().melt(value_name="Return")["Return"], bins=30, kde=True, ax=ax2)
        ax2.set_title("Distribución de rendimientos diarios combinados")
        st.pyplot(fig2)




