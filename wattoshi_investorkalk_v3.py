
import streamlit as st
import matplotlib.pyplot as plt

# Tittel
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

col1, col2 = st.columns(2)

with col1:
    antall_paneler = st.slider("Antall paneler", 1, 100, 1)
    panelkapasitet = st.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
    pris_per_panel = st.number_input("Pris per panel (NOK)", value=2000)
    eksportpris = st.number_input("Eksportpris (NOK/kWh)", value=0.6)
    btc_vekst = st.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)
    produksjonstimer = st.slider("Produksjonstimer per år", 500, 1300, 1000)

    st.markdown("### Fordeling av produksjonsverdi (%)")
    andel_kunde = st.slider("Kunde", 0, 100, 40)
    andel_takeier = st.slider("Tak-eier", 0, 50, 25)
    andel_wattoshi = 100 - andel_kunde - andel_takeier
    if andel_wattoshi < 0:
        st.error("Summen av fordelingene overstiger 100 %!")
        st.stop()

# Beregning
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris

utbetaling_kunde = verdi_årlig * andel_kunde / 100
utbetaling_takeier = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

# Nedbetalingstid
total_investering = antall_paneler * pris_per_panel
btc_kumulativ = 0
år = 0
vekstfaktor = 1 + btc_vekst / 100
btc_per_år = utbetaling_kunde
utbetaling_kunde_vekst = []

while btc_kumulativ < total_investering and år < 50:
    btc_kumulativ += btc_per_år
    utbetaling_kunde_vekst.append(btc_kumulativ)
    btc_per_år *= vekstfaktor
    år += 1

with col2:
    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    if btc_kumulativ >= total_investering:
        st.success(f"Nedbetalingstid for kunde: {år} år.")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    # Årlig BTC etter nedbetaling
    btc_etter = btc_per_år / vekstfaktor  # reset to actual annual payout after nedbetaling
    btc_takeier = utbetaling_takeier
    btc_wattoshi = utbetaling_wattoshi

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde**: {btc_etter:,.2f} kr")
    st.markdown(f"- **Tak-eier**: {btc_takeier:,.2f} kr")
    st.markdown(f"- **Wattoshi**: {btc_wattoshi:,.2f} kr")

    # Akkumulert verdi etter 10, 20 og 30 år
    btc_kunde = btc_takeier_sum = btc_wattoshi_sum = 0
    btc_k = btc_etter
    btc_t = btc_takeier
    btc_w = btc_wattoshi
    result_years = [10, 20, 30]
    acc_kunde = {}
    acc_tak = {}
    acc_watt = {}

    for i in range(1, 31):
        btc_kunde += btc_k
        btc_takeier_sum += btc_t
        btc_wattoshi_sum += btc_w

        if i in result_years:
            acc_kunde[i] = btc_kunde
            acc_tak[i] = btc_takeier_sum
            acc_watt[i] = btc_wattoshi_sum

        btc_k *= vekstfaktor
        btc_t *= vekstfaktor
        btc_w *= vekstfaktor

    for y in result_years:
        st.markdown(f"### Akkumulert BTC-verdi etter {y} år")
        st.markdown(f"- **Kunde**: {acc_kunde[y]:,.0f} kr")
        st.markdown(f"- **Tak-eier**: {acc_tak[y]:,.0f} kr")
        st.markdown(f"- **Wattoshi**: {acc_watt[y]:,.0f} kr")

    
    # Årlige utbetalinger for år 1 til 10
    st.markdown("### Utbetaling per år (år 1–10) etter nedbetalingstid")
    btc_k = btc_etter
    btc_t = btc_takeier
    btc_w = btc_wattoshi
    for i in range(1, 11):
        st.markdown(f"**År {i}:**")
        st.markdown(f"- Kunde: {btc_k:,.2f} kr")
        st.markdown(f"- Tak-eier: {btc_t:,.2f} kr")
        st.markdown(f"- Wattoshi: {btc_w:,.2f} kr")
        btc_k *= vekstfaktor
        btc_t *= vekstfaktor
        btc_w *= vekstfaktor

    # ROI og CAGR
    
    roi = ((btc_kunde - total_investering) / total_investering) * 100
    cagr = ((btc_kunde / total_investering) ** (1/30) - 1) * 100
    st.markdown("### Investeringsnøkkeltall")
    st.markdown(f"- **ROI:** {roi:,.0f} %")
    st.markdown(f"- **CAGR:** {cagr:,.2f} %")

    # Plot
    årstall = list(range(1, 31))
    kunde_y = []
    takeier_y = []
    wattoshi_y = []
    investeringslinje = [total_investering] * 30

    btc_k = btc_etter
    btc_t = btc_takeier
    btc_w = btc_wattoshi
    sum_k = sum_t = sum_w = 0
    for i in range(30):
        sum_k += btc_k
        sum_t += btc_t
        sum_w += btc_w
        kunde_y.append(sum_k)
        takeier_y.append(sum_t)
        wattoshi_y.append(sum_w)
        btc_k *= vekstfaktor
        btc_t *= vekstfaktor
        btc_w *= vekstfaktor

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(årstall, kunde_y, label="Kumulativ (Kunde)")
    ax.plot(årstall, takeier_y, label="Kumulativ (Tak-eier)")
    ax.plot(årstall, wattoshi_y, label="Kumulativ (Wattoshi)")
    ax.plot(årstall, investeringslinje, "r--", label="Investering")
    ax.set_xlabel("År")
    ax.set_ylabel("Verdi (NOK)")
    ax.set_title("Kumulativ inntekt per rolle")
    ax.legend()
    st.pyplot(fig)
