
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Input parameters
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

# Beregninger
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris

ut_kunde = verdi_årlig * andel_kunde / 100
ut_takeier = verdi_årlig * andel_takeier / 100
ut_wattoshi = verdi_årlig * andel_wattoshi / 100

vekstfaktor = 1 + btc_vekst / 100
investering = antall_paneler * pris_per_panel

# Beregn nedbetalingstid med interpolasjon
sum_kunde = 0
betalingsår = 0
interpolert = False
utbetalinger = []

for år in range(100):
    if år == 0:
        sum_kunde += ut_kunde
        utbetalinger.append((år, ut_kunde, sum_kunde))
    else:
        ut_kunde *= vekstfaktor
        sum_kunde += ut_kunde
        utbetalinger.append((år, ut_kunde, sum_kunde))
    if not interpolert and sum_kunde >= investering:
        prev_sum = utbetalinger[-2][2]
        delta = sum_kunde - prev_sum
        interpolasjon = (investering - prev_sum) / delta
        betalingsår = år - 1 + interpolasjon
        interpolert = True
        break

with col2:
    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde:** {investering:,.0f} kr")
    st.success(f"Nedbetalingstid for kunde: {betalingsår:.2f} år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde**: {ut_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier**: {ut_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {ut_wattoshi:.2f} kr")

    btc_kunde, btc_takeier, btc_wattoshi = 0, 0, 0
    uk, ut, uw = ut_kunde, ut_takeier, ut_wattoshi

    for i in range(30):
        uk *= vekstfaktor
        ut *= vekstfaktor
        uw *= vekstfaktor
        btc_kunde += uk
        btc_takeier += ut
        btc_wattoshi += uw

    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde**: {sum([x[1]*vekstfaktor**(9-x[0]) for x in utbetalinger[:10]]):,.1f} kr")
    st.markdown(f"- **Tak-eier**: {(ut_takeier * vekstfaktor**10 - ut_takeier)/(vekstfaktor - 1):,.0f} kr")
    st.markdown(f"- **Wattoshi**: {(ut_wattoshi * vekstfaktor**10 - ut_wattoshi)/(vekstfaktor - 1):,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde**: {(btc_kunde / 2):,.0f} kr")
    st.markdown(f"- **Tak-eier**: {(btc_takeier / 2):,.0f} kr")
    st.markdown(f"- **Wattoshi**: {(btc_wattoshi / 2):,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {btc_kunde:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {btc_takeier:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {btc_wattoshi:,.0f} kr")

    st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
    for i in range(min(11, len(utbetalinger))):
        år, beløp, akk = utbetalinger[i]
        st.markdown(f"- År {år}: {beløp:.2f} kr (kumulativ: {akk:.2f} kr)")
