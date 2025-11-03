# -- coding: utf-8 --
"""
FinSight - Analizador de Rentabilidad y Riesgo Empresarial
Aplicación Streamlit para análisis financiero y portafolios
Desarrollado por Angie 💼
"""

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# -----------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------
st.set_page_config(
    page_title="FinSight - Analizador de Rentabilidad y Riesgo",
    page_icon="📈",
    layout="wide"
)

# -----------------------------------------------------------
# TÍTULO PRINCIPAL
# -----------------------------------------------------------
st.title("📊 FinSight - Analizador de Rentabilidad y Riesgo Empresarial")
st.markdown("---")

# -----------------------------------------------------------
# SIDEBAR - PARÁMETROS DE CONFIGURACIÓN
# -----------------------------------------------------------
st.sidebar.header("⚙ Configuración del análisis")

# Ingreso de empresas
default_tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]
tickers_input = st.sidebar.text_input(
    "Empresas (símbolos bursátiles separados por comas):",
    value=",".join(default_tickers)
)
tickers = [t.strip().upper() for t in tickers_input.split(",")]

# Selección de fechas
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Fecha de inicio", pd.to_datetime("2020-01-01"))
with col2:
    end_date = st.date_input("Fecha final", pd.to_datetime("2023-12-31"))

# Número de simulaciones
num_portfolios = st.sidebar.slider(
    "Número de simulaciones Monte Carlo",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=1000
)

# -----------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------------------------------------
if st.sidebar.button("🚀 Ejecutar Análisis", type="primary"):
    with st.spinner("Descargando datos..."):
        try:
            # Descarga de precios históricos
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)["Close"]

            if data.empty:
                st.error("⚠ No se encontraron datos. Revisa los tickers o el rango de fechas.")
                st.stop()

            st.success("✅ Datos descargados correctamente")

            # -----------------------------------------------------------
            # SECCIÓN 1 - Datos históricos
            # -----------------------------------------------------------
            st.header("1️⃣ Datos Históricos de Precios")
            st.dataframe(data.head(10), use_container_width=True)

            st.subheader("Evolución de Precios")
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            data.plot(ax=ax1)
            ax1.set_title("Evolución de precios ajustados")
            ax1.set_xlabel("Fecha")
            ax1.set_ylabel("Precio ($)")
            ax1.grid(alpha=0.3)
            st.pyplot(fig1)

            # -----------------------------------------------------------
            # SECCIÓN 2 - Retornos
            # -----------------------------------------------------------
            st.header("2️⃣ Análisis de Retornos Diarios")
            returns = data.pct_change().dropna()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Estadísticas Descriptivas")
                st.dataframe(returns.describe(), use_container_width=True)
            with col2:
                st.subheader("Gráfico de Retornos")
                fig2, ax2 = plt.subplots(figsize=(10, 6))
                returns.plot(ax=ax2, alpha=0.7)
                ax2.set_title("Retornos diarios")
                ax2.grid(alpha=0.3)
                st.pyplot(fig2)

            # -----------------------------------------------------------
            # SECCIÓN 3 - Correlación
            # -----------------------------------------------------------
            st.header("3️⃣ Matriz de Correlación")
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            sns.heatmap(returns.corr(), annot=True, cmap="coolwarm", ax=ax3, center=0)
            ax3.set_title("Matriz de correlación del portafolio")
            st.pyplot(fig3)

            # -----------------------------------------------------------
            # SECCIÓN 4 - Métricas de Riesgo y Rentabilidad
            # -----------------------------------------------------------
            st.header("4️⃣ Métricas de Rentabilidad y Riesgo Anualizadas")
            mean_returns = returns.mean() * 252
            risk = returns.std() * np.sqrt(252)
            metrics_df = pd.DataFrame({
                "Rendimiento Anual": mean_returns,
                "Riesgo (Volatilidad)": risk
