
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Kunde / Tak-eier / Wattoshi")

col1, col2 = st.columns(2)

with col1:
    antall_paneler = st.slider("Antall paneler", 1, 100, 1)
    panelkapasitet = st.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
    pris_per_panel = st.number_input("Pris per panel (NOK)", value=2000)
    eksportpris = st.number_input("Eksportpris (NOK/kWh)", value=0.6)
    produksjonstimer = st.slider("Produksjonstimer per år", 500, 1300, 1000)
    btc_vekst = st.slider("Årlig BTC verdiøkning (%)", 0, 50, 20) / 100

    st.markdown("### Fordeling av produksjonsverdi (%)")
    andel_kunde = st.slider("Kunde", 0, 100, 40)
    andel_takeier = st.slider("Tak-eier", 0, 50, 25)
    andel_wattoshi = 100 - andel_kunde - andel_takeier
    if andel_wattoshi < 0:
        st.error("Summen av fordelingene overstiger 100 %!")
        st.stop()

with col2:
    produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
    verdi_årlig = produksjon_kwh * eksportpris
    total_investering = antall_paneler * pris_per_panel
    vekstfaktor = 1 + btc_vekst

    årlig_kunde_start = verdi_årlig * andel_kunde / 100
    årlig_takeier_start = verdi_årlig * andel_takeier / 100
    årlig_wattoshi_start = verdi_årlig * andel_wattoshi / 100

    btc_kumulativ = 0
    år = 0
    utbetaling_kunde_vekst = []

    årlig_beløp = årlig_kunde_start
    while btc_kumulativ < total_investering and år < 50:
        btc_kumulativ += årlig_beløp
        utbetaling_kunde_vekst.append(btc_kumulativ)
        årlig_beløp *= vekstfaktor
        år += 1

    nedbetalingstid = år if btc_kumulativ >= total_investering else None

    if nedbetalingstid:
        st.success(f"Nedbetalingstid for kunde: {nedbetalingstid:.2f} år")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    st.markdown("### Årlig BTC-utbetaling fra panel (før vekst i BTC-verdi)")
    st.markdown(f"- **Kunde**: {årlig_kunde_start:.2f} kr")
    st.markdown(f"- **Tak-eier**: {årlig_takeier_start:.2f} kr")
    st.markdown(f"- **Wattoshi**: {årlig_wattoshi_start:.2f} kr")

    def geometrisk_sum(a, r, n):
        return a * ((1 + r)**n - 1) / r

    for årstall in [10, 20, 30]:
        kunde_sum = geometrisk_sum(årlig_kunde_start, btc_vekst, årstall)
        takeier_sum = geometrisk_sum(årlig_takeier_start, btc_vekst, årstall)
        wattoshi_sum = geometrisk_sum(årlig_wattoshi_start, btc_vekst, årstall)
        st.markdown(f"### Akkumulert BTC-verdi etter {årstall} år")
        st.markdown(f"- **Kunde**: {kunde_sum:,.0f} kr")
        st.markdown(f"- **Tak-eier**: {takeier_sum:,.0f} kr")
        st.markdown(f"- **Wattoshi**: {wattoshi_sum:,.0f} kr")

# Tabell med utvikling år 0–10
st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
btc = årlig_kunde_start
total = 0
for i in range(11):
    total += btc
    st.markdown(f"År {i}: {btc:.2f} kr (kumulativ: {total:.2f} kr)")
    btc *= vekstfaktor

# Plot
årstall = list(range(1, 31))
kunde_y, takeier_y, wattoshi_y = [], [], []
investeringslinje = [total_investering] * 30

btc_e, btc_t, btc_w = årlig_kunde_start, årlig_takeier_start, årlig_wattoshi_start
sum_k, sum_t, sum_w = 0, 0, 0
for _ in range(30):
    btc_e *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor
    sum_k += btc_e
    sum_t += btc_t
    sum_w += btc_w
    kunde_y.append(sum_k)
    takeier_y.append(sum_t)
    wattoshi_y.append(sum_w)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(årstall, kunde_y, label="Kunde")
ax.plot(årstall, takeier_y, label="Tak-eier")
ax.plot(årstall, wattoshi_y, label="Wattoshi")
ax.plot(årstall, investeringslinje, "r--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt")
ax.legend()
st.pyplot(fig)
