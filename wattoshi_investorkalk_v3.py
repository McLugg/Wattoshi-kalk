
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Kolonner
col1, col2 = st.columns([1, 1])

with col1:
    st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")
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

total_investering = antall_paneler * pris_per_panel
vekstfaktor = 1 + btc_vekst / 100

# Nøyaktig nedbetalingstid
btc_sum = 0
betalinger = [utbetaling_kunde]
år = 0
while btc_sum < total_investering:
    btc_sum += betalinger[-1]
    betalinger.append(betalinger[-1] * vekstfaktor)
    år += 1

# Interpolasjon mellom siste to år
if btc_sum > total_investering:
    over = btc_sum - total_investering
    diff = betalinger[-1] - betalinger[-2]
    ratio = (betalinger[-1] - over) / diff
    nøyaktig_tid = år - 1 + ratio
else:
    nøyaktig_tid = år

# Resultater
with col2:
    st.markdown("## Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    st.success(f"Nedbetalingstid for kunde: {nøyaktig_tid:.2f} år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde:** {utbetaling_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier:** {utbetaling_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi:** {utbetaling_wattoshi:.2f} kr")

    btc_kunde = btc_takeier = btc_wattoshi = 0
    btc_k = utbetaling_kunde
    btc_t = utbetaling_takeier
    btc_w = utbetaling_wattoshi

    for i in range(30):
        btc_k *= vekstfaktor
        btc_t *= vekstfaktor
        btc_w *= vekstfaktor
        btc_kunde += btc_k
        btc_takeier += btc_t
        btc_wattoshi += btc_w

    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde:** {sum([utbetaling_kunde * (vekstfaktor ** i) for i in range(10)]):,.0f} kr")
    st.markdown(f"- **Tak-eier:** {sum([utbetaling_takeier * (vekstfaktor ** i) for i in range(10)]):,.0f} kr")
    st.markdown(f"- **Wattoshi:** {sum([utbetaling_wattoshi * (vekstfaktor ** i) for i in range(10)]):,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde:** {sum([utbetaling_kunde * (vekstfaktor ** i) for i in range(20)]):,.0f} kr")
    st.markdown(f"- **Tak-eier:** {sum([utbetaling_takeier * (vekstfaktor ** i) for i in range(20)]):,.0f} kr")
    st.markdown(f"- **Wattoshi:** {sum([utbetaling_wattoshi * (vekstfaktor ** i) for i in range(20)]):,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde:** {btc_kunde:,.0f} kr")
    st.markdown(f"- **Tak-eier:** {btc_takeier:,.0f} kr")
    st.markdown(f"- **Wattoshi:** {btc_wattoshi:,.0f} kr")

    st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
    sum_ = 0
    for i in range(11):
        beløp = utbetaling_kunde * (vekstfaktor ** i)
        sum_ += beløp
        st.markdown(f"- År {i}: {beløp:.2f} kr (kumulativ: {sum_:,.2f} kr)")
