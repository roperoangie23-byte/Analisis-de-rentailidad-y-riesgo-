    if st.sidebar.button("Comparar empresas"):
        data1 = yf.download(ticker1, start=start_date, end=end_date, progress=False)
        data2 = yf.download(ticker2, start=start_date, end=end_date, progress=False)

        if data1.empty or data2.empty:
            st.error("❌ Verifica los tickers, no se encontraron datos.")
        else:
            st.success(f"✅ Comparando **{ticker1}** y **{ticker2}**")

            # 🔍 Manejo de MultiIndex si es necesario
            if isinstance(data1.columns, pd.MultiIndex):
                data1 = data1['Adj Close'] if 'Adj Close' in data1.columns.levels[0] else data1['Close']
            else:
                data1 = data1[['Adj Close']] if 'Adj Close' in data1.columns else data1[['Close']]

            if isinstance(data2.columns, pd.MultiIndex):
                data2 = data2['Adj Close'] if 'Adj Close' in data2.columns.levels[0] else data2['Close']
            else:
                data2 = data2[['Adj Close']] if 'Adj Close' in data2.columns else data2[['Close']]

            # Renombrar columnas para que no se mezclen
            data1.columns = [ticker1]
            data2.columns = [ticker2]

            # Unir datos por fecha
            data = pd.concat([data1, data2], axis=1).dropna()

            # Calcular retornos
            returns = data.pct_change().dropna()

            # 📊 Estadísticas
            avg1, avg2 = returns[ticker1].mean(), returns[ticker2].mean()
            std1, std2 = returns[ticker1].std(), returns[ticker2].std()
            corr = returns[ticker1].corr(returns[ticker2])

            col1, col2, col3 = st.columns(3)
            col1.metric(f"Rentabilidad {ticker1}", f"{avg1*100:.2f}%")
            col2.metric(f"Rentabilidad {ticker2}", f"{avg2*100:.2f}%")
            col3.metric("Correlación", f"{corr:.2f}")

            # 📈 Gráfico comparativo
            st.subheader("📉 Comparación de precios históricos")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data[ticker1], label=ticker1, linewidth=2)
            ax.plot(data[ticker2], label=ticker2, linewidth=2)
            ax.set_title("Evolución de precios ajustados")
            ax.legend()
            st.pyplot(fig)

            # 📊 Dispersión de rendimientos
            st.subheader("📊 Relación entre los rendimientos")
            fig2, ax2 = plt.subplots(figsize=(7, 5))
            sns.scatterplot(x=returns[ticker1], y=returns[ticker2], ax=ax2)
            ax2.set_xlabel(f"Rendimientos {ticker1}")
            ax2.set_ylabel(f"Rendimientos {ticker2}")
            ax2.set_title("Correlación de rendimientos")
            st.pyplot(fig2)

            # 🧠 Conclusión automática
            st.markdown("### 📈 Conclusión del análisis")
            if corr > 0.7:
                st.info(f"Los rendimientos de **{ticker1}** y **{ticker2}** están fuertemente correlacionados — se mueven en la misma dirección.")
            elif corr > 0.3:
                st.warning(f"Existe una correlación moderada entre **{ticker1}** y **{ticker2}**.")
            else:
                st.success(f"Los rendimientos de **{ticker1}** y **{ticker2}** son poco o nada correlacionados — buena opción para diversificar.")




