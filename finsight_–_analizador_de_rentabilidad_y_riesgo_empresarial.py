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

# 🔍 Entrada del usuario
ticker = st.text_input("Ingresa el ticker de la empresa (por ejemplo: AAPL, MSFT, NVDA):", "AAPL")
start_date = st.date_input("Fecha inicial:", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Fecha final:", pd.to_datetime("2024-12-31"))

# 📈 Descargar datos
if st.button("Analizar"):
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error("No se encontraron datos para el ticker especificado.")
    else:
        st.success(f"Datos descargados exitosamente para **{ticker}**")

        # 🧮 Cálculos
        data["Daily Return"] = data["Adj Close"].pct_change()
        avg_return = data["Daily Return"].mean()
        std_dev = data["Daily Return"].std()
        sharpe_ratio = avg_return / std_dev if std_dev != 0 else 0

        # 📊 Mostrar métricas
        metrics_df = pd.DataFrame({
            'Indicador': ['Rentabilidad promedio (%)', 'Riesgo (Desviación estándar %)', 'Sharpe Ratio'],
            'Valor': [avg_return * 100, std_dev * 100, sharpe_ratio]
        })
        st.table(metrics_df)

        # 📈 Gráfico de precios ajustados
        st.subheader("Evolución del precio ajustado")
        fig, ax = plt.subplots()
        ax.plot(data["Adj Close"], color='blue')
        ax.set_title(f"Precio ajustado de {ticker}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio ($)")
        st.pyplot(fig)

        # 📉 Histograma de rendimientos diarios
        st.subheader("Distribución de los rendimientos diarios")
        fig2, ax2 = plt.subplots()
        sns.histplot(data["Daily Return"].dropna(), bins=30, kde=True, ax=ax2)
        st.pyplot(fig2)
