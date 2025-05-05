
import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("Wattoshi Panelinvestor Kalkulator – Kunde / Tak-eier / Wattoshi")

# Inputs
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

# Calculations
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris
total_investering = antall_paneler * pris_per_panel
btc_vekst_faktor = 1 + btc_vekst / 100

# Fordeling per rolle
utbetaling_kunde = verdi_årlig * andel_kunde / 100
utbetaling_takeier = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

# Nedbetalingstid
btc_kumulativ = 0
år = 0
utbetaling_k = utbetaling_kunde
utbetaling_kunde_vekst = []
while btc_kumulativ < total_investering and år < 50:
    btc_kumulativ += utbetaling_k
    utbetaling_kunde_vekst.append(btc_kumulativ)
    utbetaling_k *= btc_vekst_faktor
    år += 1

if btc_kumulativ >= total_investering:
    st.success(f"Nedbetalingstid for kunde: {år:.2f} år.")
else:
    st.warning("Investeringen nedbetales ikke innen 50 år.")

with col2:
    st.markdown("### Årlig BTC-utbetaling fra panel (før vekst i BTC-verdi)")
    st.markdown(f"- **Kunde**: {utbetaling_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier**: {utbetaling_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {utbetaling_wattoshi:.2f} kr")

# Akkumulert verdi
btc_kunde, btc_takeier, btc_wattoshi = 0, 0, 0
btc_k, btc_t, btc_w = utbetaling_kunde, utbetaling_takeier, utbetaling_wattoshi

for i in range(30):
    btc_kunde += btc_k
    btc_takeier += btc_t
    btc_wattoshi += btc_w
    btc_k *= btc_vekst_faktor
    btc_t *= btc_vekst_faktor
    btc_w *= btc_vekst_faktor

    if i+1 in [10, 20, 30]:
        st.markdown(f"### Akkumulert BTC-verdi etter {i+1} år")
        st.markdown(f"- **Kunde**: {btc_kunde:,.0f} kr")
        st.markdown(f"- **Tak-eier**: {btc_takeier:,.0f} kr")
        st.markdown(f"- **Wattoshi**: {btc_wattoshi:,.0f} kr")

# Årlig utbetaling og kumulativ
st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
btc_k = utbetaling_kunde
cumulative = 0
for i in range(11):
    cumulative += btc_k
    st.markdown(f"- År {i}: {btc_k:.2f} kr (kumulativ: {cumulative:.2f} kr)")
    btc_k *= btc_vekst_faktor
