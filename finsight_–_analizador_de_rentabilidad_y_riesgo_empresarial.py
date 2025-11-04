# ==========================
# 💼 NUEVA SECCIÓN: PORTAFOLIO
# ==========================

st.markdown("---")
st.header("💹 Simulador de Portafolio de Inversión")

colp1, colp2 = st.columns(2)

with colp1:
    p_ticker1 = st.text_input("📊 Empresa 1 (Ticker):", "AAPL")
    w1 = st.slider("Peso (%) Empresa 1", 0, 100, 50)

with colp2:
    p_ticker2 = st.text_input("📈 Empresa 2 (Ticker):", "MSFT")
    w2 = 100 - w1
    st.write(f"Peso Empresa 2: **{w2}%**")

if st.button("Calcular Portafolio"):
    # Descargar datos de ambas empresas
    p_data = yf.download([p_ticker1, p_ticker2], start=start_date, end=end_date, progress=False)['Adj Close']

    if isinstance(p_data.columns, pd.MultiIndex):
        p_data.columns = p_data.columns.get_level_values(1)

    p_data = p_data.dropna()

    if p_data.empty:
        st.error("❌ No se encontraron datos para los tickers seleccionados.")
    else:
        st.success(f"Datos obtenidos para **{p_ticker1}** y **{p_ticker2}**")

        # Calcular retornos diarios
        returns = p_data.pct_change().dropna()

        # Pesos del portafolio
        weights = np.array([w1/100, w2/100])

        # Rentabilidad esperada del portafolio
        exp_return = np.sum(returns.mean() * weights) * 252  # anualizada

        # Riesgo del portafolio
        cov_matrix = returns.cov() * 252
        port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        port_std_dev = np.sqrt(port_variance)

        # Ratio de Sharpe (supone tasa libre de riesgo 0%)
        sharpe_ratio = exp_return / port_std_dev

        # Mostrar resultados
        st.subheader("📈 Resultados del Portafolio")
        st.write(f"**Rentabilidad esperada (anualizada):** {exp_return*100:.2f}%")
        st.write(f"**Riesgo (Desviación estándar anual):** {port_std_dev*100:.2f}%")
        st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")

        # 📊 Visualización de pesos
        st.subheader("📊 Composición del portafolio")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(weights, labels=[p_ticker1, p_ticker2], autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e'])
        ax.axis('equal')
        st.pyplot(fig)

        # 🔵 Frontera eficiente simple (variando pesos)
        st.subheader("📈 Frontera eficiente simulada")
        port_returns = []
        port_risks = []

        for w in np.linspace(0, 1, 100):
            wts = np.array([w, 1-w])
            r = np.sum(returns.mean() * wts) * 252
            s = np.sqrt(np.dot(wts.T, np.dot(cov_matrix, wts)))
            port_returns.append(r)
            port_risks.append(s)

        fig2, ax2 = plt.subplots(figsize=(7, 5))
        ax2.plot(port_risks, port_returns, 'b-', linewidth=2)
        ax2.scatter(port_std_dev, exp_return, color='red', s=80, label='Tu portafolio')
        ax2.set_xlabel('Riesgo (Desviación estándar)')
        ax2.set_ylabel('Rentabilidad esperada')
        ax2.set_title('Frontera eficiente (2 activos)')
        ax2.legend()
        st.pyplot(fig2)




