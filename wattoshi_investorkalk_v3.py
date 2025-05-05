
import streamlit as st
import matplotlib.pyplot as plt

# Tittel
st.title("Wattoshi Panelinvestor Kalkulator – Kunde / Tak-eier / Wattoshi")

# Inputparametere
col1, col2 = st.columns(2)
with col1:
    antall_paneler = st.slider("Antall paneler", 1, 100, 1)
    panelkapasitet = st.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
    pris_per_panel = st.number_input("Pris per panel (NOK)", value=2000)
    eksportpris = st.number_input("Eksportpris (NOK/kWh)", value=0.6)
    produksjonstimer = st.slider("Produksjonstimer per år", 500, 1300, 1000)
    btc_vekst = st.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)

with col2:
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

# Resultatkolonne
with col2:
    st.markdown("## Resultater")
    total_investering = antall_paneler * pris_per_panel
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")

# Nedbetalingstid
btc_kumulativ = 0
år = 0
vekstfaktor = 1 + btc_vekst / 100
utbetaling = utbetaling_kunde
utbetaling_kunde_vekst = []
while btc_kumulativ < total_investering and år < 50:
    if år == 0:
        btc_kumulativ += utbetaling  # Første årsverdi legges direkte
    else:
        utbetaling *= vekstfaktor
        btc_kumulativ += utbetaling
    utbetaling_kunde_vekst.append(btc_kumulativ)
    år += 1

nedbetalingstid = år
col2.success(f"Nedbetalingstid for kunde: {nedbetalingstid:.2f} år.")

# Årlig BTC-utbetaling (før BTC-vekst)
col2.markdown("### Årlig BTC-utbetaling fra panel (før vekst i BTC-verdi)")
col2.markdown(f"- **Kunde**: {verdi_årlig * andel_kunde / 100:,.2f} kr")
col2.markdown(f"- **Tak-eier**: {verdi_årlig * andel_takeier / 100:,.2f} kr")
col2.markdown(f"- **Wattoshi**: {verdi_årlig * andel_wattoshi / 100:,.2f} kr")

# Akkumulert verdi etter 10, 20 og 30 år
def akkumulerte_verdier(startverdi, vekstfaktor, år):
    sum = 0
    for i in range(år):
        sum += startverdi * (vekstfaktor ** i)
    return sum

btc_kunde_10 = akkumulerte_verdier(utbetaling_kunde, vekstfaktor, 10)
btc_kunde_20 = akkumulerte_verdier(utbetaling_kunde, vekstfaktor, 20)
btc_kunde_30 = akkumulerte_verdier(utbetaling_kunde, vekstfaktor, 30)
btc_takeier_10 = akkumulerte_verdier(utbetaling_takeier, vekstfaktor, 10)
btc_takeier_20 = akkumulerte_verdier(utbetaling_takeier, vekstfaktor, 20)
btc_takeier_30 = akkumulerte_verdier(utbetaling_takeier, vekstfaktor, 30)
btc_wattoshi_10 = akkumulerte_verdier(utbetaling_wattoshi, vekstfaktor, 10)
btc_wattoshi_20 = akkumulerte_verdier(utbetaling_wattoshi, vekstfaktor, 20)
btc_wattoshi_30 = akkumulerte_verdier(utbetaling_wattoshi, vekstfaktor, 30)

col2.markdown("### Akkumulert BTC-verdi etter 10 år")
col2.markdown(f"- **Kunde**: {btc_kunde_10:,.0f} kr")
col2.markdown(f"- **Tak-eier**: {btc_takeier_10:,.0f} kr")
col2.markdown(f"- **Wattoshi**: {btc_wattoshi_10:,.0f} kr")

col2.markdown("### Akkumulert BTC-verdi etter 20 år")
col2.markdown(f"- **Kunde**: {btc_kunde_20:,.0f} kr")
col2.markdown(f"- **Tak-eier**: {btc_takeier_20:,.0f} kr")
col2.markdown(f"- **Wattoshi**: {btc_wattoshi_20:,.0f} kr")

col2.markdown("### Akkumulert BTC-verdi etter 30 år")
col2.markdown(f"- **Kunde**: {btc_kunde_30:,.0f} kr")
col2.markdown(f"- **Tak-eier**: {btc_takeier_30:,.0f} kr")
col2.markdown(f"- **Wattoshi**: {btc_wattoshi_30:,.0f} kr")
