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

# ⚙️ Configuración de página
st.set_page_config(page_title="FinSight", page_icon="💼", layout="wide")

# 🎯 Encabezado principal
st.title("💼 FinSight – Analizador de Rentabilidad y Riesgo Empresarial")
st.markdown("Explora el desempeño financiero de distintas empresas a través de indicadores de **rentabilidad** y **riesgo**.")
st.divider()

# 🔍 Entrada del usuario
ticker = st.text_input("📊 Ingresa el ticker de la empresa (por ejemplo: AAPL, MSFT, NVDA):", "AAPL")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("📅 Fecha inicial:", pd.to_datetime("2020-01-01"))
with col2:
    end_date = st.date_input("📅 Fecha final:", pd.to_datetime("2024-12-31"))

# 🚀 Botón de análisis
if st.button("Analizar"):
    with st.spinner("Descargando datos financieros..."):
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # Verificación de datos
    if data.empty:
        st.error("❌ No se encontraron datos para el ticker especificado. Verifica que sea válido.")
        st.stop()

    st.success(f"✅ Datos descargados exitosamente para **{ticker}**")

    # 🧮 Asegurar que las columnas sean planas (a veces vienen en MultiIndex)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
