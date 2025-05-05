
import streamlit as st
import matplotlib.pyplot as plt

# Tittel
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Layout
col1, col2 = st.columns([1, 1.2])

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

utb_kunde = verdi_årlig * andel_kunde / 100
utb_takeier = verdi_årlig * andel_takeier / 100
utb_wattoshi = verdi_årlig * andel_wattoshi / 100

total_investering = antall_paneler * pris_per_panel
vekstfaktor = 1 + btc_vekst / 100

# Kalkuler nedbetalingstid
btc_kumulativ = 0
år = 0
utb = utb_kunde
nedbetaling_fullført = False
utb_kunde_tabell = []
kumulativ_tabell = []

btc_kumulativ += utb  # år 0
utb_kunde_tabell.append((0, utb, btc_kumulativ))

while not nedbetaling_fullført and år < 50:
    år += 1
    utb *= vekstfaktor
    btc_kumulativ += utb
    utb_kunde_tabell.append((år, utb, btc_kumulativ))
    if btc_kumulativ >= total_investering:
        nedbetaling_fullført = True

with col2:
    st.markdown("## Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    st.success(f"Nedbetalingstid for kunde: {år:.2f} år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde**: {utb_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier**: {utb_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {utb_wattoshi:.2f} kr")

    # Akkumulert verdi etter 10, 20 og 30 år
    btc_kunde = 0
    btc_takeier = 0
    btc_wattoshi = 0
    utb_k = utb_kunde
    utb_t = utb_takeier
    utb_w = utb_wattoshi

    for i in range(30):
        utb_k *= vekstfaktor
        utb_t *= vekstfaktor
        utb_w *= vekstfaktor
        btc_kunde += utb_k
        btc_takeier += utb_t
        btc_wattoshi += utb_w
        if i + 1 == 10:
            v10 = (btc_kunde, btc_takeier, btc_wattoshi)
        if i + 1 == 20:
            v20 = (btc_kunde, btc_takeier, btc_wattoshi)

    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde**: {v10[0]:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {v10[1]:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {v10[2]:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde**: {v20[0]:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {v20[1]:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {v20[2]:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {btc_kunde:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {btc_takeier:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {btc_wattoshi:,.0f} kr")

    # Vis tabell for årlige utbetalinger
    st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
    for år, utb, akk in utb_kunde_tabell[:11]:
        st.markdown(f"- År {år}: {utb:,.2f} kr (kumulativt: {akk:,.2f} kr)")
