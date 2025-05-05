
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Layout
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("Inputparametere")
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
utbetaling_kunde_start = verdi_årlig * andel_kunde / 100
utbetaling_takeier = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

total_investering = antall_paneler * pris_per_panel
vekstfaktor = 1 + btc_vekst / 100

btc_kumulativ = 0
utbetaling_kunde = utbetaling_kunde_start
år = 0
tabell = []
while btc_kumulativ < total_investering and år < 50:
    btc_kumulativ += utbetaling_kunde
    tabell.append((år, utbetaling_kunde, btc_kumulativ))
    utbetaling_kunde *= vekstfaktor
    år += 1

nedbetalingstid = tabell[-1][0] + 1 if btc_kumulativ >= total_investering else ">50"

# Etter nedbetaling
btc_etter = utbetaling_kunde_start * (vekstfaktor ** nedbetalingstid)
btc_takeier = utbetaling_takeier * (vekstfaktor ** nedbetalingstid)
btc_wattoshi = utbetaling_wattoshi * (vekstfaktor ** nedbetalingstid)

btc_kunde = btc_etter
btc_takeier_sum = btc_takeier
btc_wattoshi_sum = btc_wattoshi

årstall = [nedbetalingstid + i for i in range(1, 30 - nedbetalingstid + 1)]
kunde_y = [btc_etter]
takeier_y = [btc_takeier]
wattoshi_y = [btc_wattoshi]

for _ in årstall[1:]:
    btc_etter *= vekstfaktor
    btc_takeier *= vekstfaktor
    btc_wattoshi *= vekstfaktor

    btc_kunde += btc_etter
    btc_takeier_sum += btc_takeier
    btc_wattoshi_sum += btc_wattoshi

    kunde_y.append(btc_kunde)
    takeier_y.append(btc_takeier_sum)
    wattoshi_y.append(btc_wattoshi_sum)

with col2:
    st.header("Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    st.success(f"Nedbetalingstid for kunde: {nedbetalingstid:.2f} år.")

    st.subheader("Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde:** {utbetaling_kunde_start * (vekstfaktor ** nedbetalingstid):,.2f} kr")
    st.markdown(f"- **Tak-eier:** {utbetaling_takeier * (vekstfaktor ** nedbetalingstid):,.2f} kr")
    st.markdown(f"- **Wattoshi:** {utbetaling_wattoshi * (vekstfaktor ** nedbetalingstid):,.2f} kr")

    def akkumulert_verdi(startbeløp, vekstfaktor, år):
        sum = 0
        beløp = startbeløp
        for _ in range(år):
            sum += beløp
            beløp *= vekstfaktor
        return sum

    st.subheader("Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde:** {akkumulert_verdi(utbetaling_kunde_start, vekstfaktor, 10):,.0f} kr")
    st.markdown(f"- **Tak-eier:** {akkumulert_verdi(utbetaling_takeier, vekstfaktor, 10):,.0f} kr")
    st.markdown(f"- **Wattoshi:** {akkumulert_verdi(utbetaling_wattoshi, vekstfaktor, 10):,.0f} kr")

    st.subheader("Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde:** {akkumulert_verdi(utbetaling_kunde_start, vekstfaktor, 20):,.0f} kr")
    st.markdown(f"- **Tak-eier:** {akkumulert_verdi(utbetaling_takeier, vekstfaktor, 20):,.0f} kr")
    st.markdown(f"- **Wattoshi:** {akkumulert_verdi(utbetaling_wattoshi, vekstfaktor, 20):,.0f} kr")

    st.subheader("Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde:** {akkumulert_verdi(utbetaling_kunde_start, vekstfaktor, 30):,.0f} kr")
    st.markdown(f"- **Tak-eier:** {akkumulert_verdi(utbetaling_takeier, vekstfaktor, 30):,.0f} kr")
    st.markdown(f"- **Wattoshi:** {akkumulert_verdi(utbetaling_wattoshi, vekstfaktor, 30):,.0f} kr")

    st.subheader("Årlig utbetaling og akkumulert sum (år 0–10)")
    beløp = utbetaling_kunde_start
    kum_sum = 0
    for i in range(11):
        kum_sum += beløp
        st.markdown(f"- År {i}: {beløp:,.2f} kr (kumulativ: {kum_sum:,.2f} kr)")
        beløp *= vekstfaktor
