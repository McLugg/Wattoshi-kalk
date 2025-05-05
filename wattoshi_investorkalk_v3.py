
import streamlit as st

# Tittel
st.title("Wattoshi Panelinvestor Kalkulator – Kunde / Tak-eier / Wattoshi")

# Inputparametere
antall_paneler = st.slider("Antall paneler", 1, 100, 1)
panelkapasitet = st.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
pris_per_panel = st.number_input("Pris per panel (NOK)", value=2000)
eksportpris = st.number_input("Eksportpris (NOK/kWh)", value=0.6)
btc_vekst = st.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)
produksjonstimer = st.slider("Produksjonstimer per år", 500, 1300, 1000)

# Fordeling
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
utbetaling_kunde_vekst = []
betaling = utbetaling_kunde

while btc_kumulativ < total_investering and år < 50:
    btc_kumulativ += betaling
    utbetaling_kunde_vekst.append(btc_kumulativ)
    betaling *= vekstfaktor
    år += 1

if btc_kumulativ >= total_investering:
    st.success(f"Nedbetalingstid for kunde: {år:.2f} år.")
else:
    st.warning("Investeringen nedbetales ikke innen 50 år.")

# Årlig BTC-utbetaling fra panel
st.markdown("### Årlig BTC-utbetaling fra panel (før vekst i BTC-verdi)")
st.markdown(f"- **Kunde**: {utbetaling_kunde:.2f} kr")
st.markdown(f"- **Tak-eier**: {utbetaling_takeier:.2f} kr")
st.markdown(f"- **Wattoshi**: {utbetaling_wattoshi:.2f} kr")

# Akkumulert BTC-verdi etter 10, 20 og 30 år
btc_kunde = 0
btc_takeier_sum = 0
btc_wattoshi_sum = 0
btc_kunde_10 = btc_kunde_20 = btc_kunde_30 = 0
btc_takeier_10 = btc_takeier_20 = btc_takeier_30 = 0
btc_wattoshi_10 = btc_wattoshi_20 = btc_wattoshi_30 = 0

btc_k = utbetaling_kunde
btc_t = utbetaling_takeier
btc_w = utbetaling_wattoshi

for i in range(30):
    btc_kunde += btc_k
    btc_takeier_sum += btc_t
    btc_wattoshi_sum += btc_w
    if i == 9:
        btc_kunde_10 = btc_kunde
        btc_takeier_10 = btc_takeier_sum
        btc_wattoshi_10 = btc_wattoshi_sum
    if i == 19:
        btc_kunde_20 = btc_kunde
        btc_takeier_20 = btc_takeier_sum
        btc_wattoshi_20 = btc_wattoshi_sum
    if i == 29:
        btc_kunde_30 = btc_kunde
        btc_takeier_30 = btc_takeier_sum
        btc_wattoshi_30 = btc_wattoshi_sum
    btc_k *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor

st.markdown("### Akkumulert BTC-verdi etter 10 år")
st.markdown(f"- **Kunde**: {btc_kunde_10:,.0f} kr")
st.markdown(f"- **Tak-eier**: {btc_takeier_10:,.0f} kr")
st.markdown(f"- **Wattoshi**: {btc_wattoshi_10:,.0f} kr")

st.markdown("### Akkumulert BTC-verdi etter 20 år")
st.markdown(f"- **Kunde**: {btc_kunde_20:,.0f} kr")
st.markdown(f"- **Tak-eier**: {btc_takeier_20:,.0f} kr")
st.markdown(f"- **Wattoshi**: {btc_wattoshi_20:,.0f} kr")

st.markdown("### Akkumulert BTC-verdi etter 30 år")
st.markdown(f"- **Kunde**: {btc_kunde_30:,.0f} kr")
st.markdown(f"- **Tak-eier**: {btc_takeier_30:,.0f} kr")
st.markdown(f"- **Wattoshi**: {btc_wattoshi_30:,.0f} kr")
