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

# 🎨 Configuración de la página
st.set_page_config(page_title="FinSight", layout="wide", page_icon="📈")

# 🎯 Encabezado principal
st.title("💼 FinSight – Analizador de Rentabilidad y Riesgo Empresarial")
st.write("Explora el desempeño financiero de distintas empresas a través de indicadores de rentabilidad y riesgo.")

# ----------------------------------------------------------
# 🧠 Función para validar y sugerir tickers
# ----------------------------------------------------------
def validar_ticker(ticker):
    ticker = ticker.strip().upper()
    try:
        data = yf.Ticker(ticker)
        info = data.info
        # Si no tiene nombre, no es válido
        if not info or "shortName" not in info:
            return None
        return ticker
    except Exception:
        return None


# ----------------------------------------------------------
# 🔍 Entrada del usuario
# ----------------------------------------------------------
ticker_input = st.text_input(
    "Ingresa el ticker de la empresa (por ejemplo: AAPL, MSFT, NVDA):",
    "AAPL"
).upper()
start_date = st.date_input("Fecha inicial:", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Fecha final:", pd.to_datetime("2024-12-31"))

# ----------------------------------------------------------
# 🚀 Botón principal
# ----------------------------------------------------------
if st.button("Analizar Empresa"):
    with st.spinner("Verificando ticker y descargando datos..."):
        ticker_valido = validar_ticker(ticker_input)

        if not ticker_valido:
            st.error(f"❌ El ticker '{ticker_input}' no existe o no tiene datos válidos en Yahoo Finance.")
            st.info("Verifica que esté bien escrito. Ejemplos válidos: **AAPL**, **MSFT**, **NVDA**, **GOOGL**, **TSLA**")
        else:
            data = yf.download(ticker_valido, start=start_date, end=end_date)

            if data.empty:
                st.error("⚠️ No se encontraron datos en el rango de fechas seleccionado.")
            else:
                st.success(f"✅ Datos descargados exitosamente para **{ticker_valido}**")

                # ----------------------------------------------------------
                # 🧮 Cálculos
                # ----------------------------------------------------------
                data["Daily Return"] = data["Adj Close"].pct_change()
                avg_return = data["Daily Return"].mean()
                std_dev = data["Daily Return"].std()
                sharpe_ratio = avg_return / std_dev if std_dev != 0 else 0

                # 📊 Mostrar métricas
                st.subheader("📈 Indicadores Financieros")
                metrics_df = pd.DataFrame({
                    'Indicador': ['Rentabilidad promedio (%)', 'Riesgo (Desviación estándar %)', 'Índice de Sharpe'],
                    'Valor': [avg_return * 100, std_dev * 100, sharpe_ratio]
                })
                st.table(metrics_df.style.format({'Valor': "{:.2f}"}))

                # ----------------------------------------------------------
                # 📈 Gráfico de precios ajustados
                # ----------------------------------------------------------
                st.subheader("💹 Evolución del Precio Ajustado")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(data["Adj Close"], color='dodgerblue', linewidth=2)
                ax.set_title(f"Precio ajustado de {ticker_valido}", fontsize=13)
                ax.set_xlabel("Fecha")
                ax.set_ylabel("Precio ($)")
                ax.grid(alpha=0.3)
                st.pyplot(fig)

                # ----------------------------------------------------------
                # 📉 Histograma de rendimientos diarios
                # ----------------------------------------------------------
                st.subheader("📊 Distribución de los Rendimientos Diarios")
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                sns.histplot(data["Daily Return"].dropna(), bins=30, kde=True, ax=ax2, color='salmon')
                ax2.set_title("Distribución de los retornos diarios")
                ax2.set_xlabel("Retorno diario (%)")
                ax2.set_ylabel("Frecuencia")
                st.pyplot(fig2)

# ----------------------------------------------------------
# 🧾 Pie de página
# ----------------------------------------------------------
st.markdown("---")
st.caption("Desarrollado por Angie Ropero, Jhony Soto, Dayana Gaviria• Datos obtenidos de Yahoo Finance • Proyecto Universitario 2025")

