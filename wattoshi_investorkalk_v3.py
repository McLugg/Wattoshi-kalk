
import streamlit as st
import matplotlib.pyplot as plt

# Tittel
st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

col1, col2 = st.columns(2)

with col1:
    # Inputparametere
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

with col2:
    # Beregning
    produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
    verdi_årlig = produksjon_kwh * eksportpris

    utbetaling_kunde_start = verdi_årlig * andel_kunde / 100
    utbetaling_takeier = verdi_årlig * andel_takeier / 100
    utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

    # Nedbetalingstid
    total_investering = antall_paneler * pris_per_panel
    btc_kumulativ = 0
    år = 0
    vekstfaktor = 1 + btc_vekst / 100
    årlig_liste = []
    while btc_kumulativ < total_investering and år < 50:
        utbetaling_kunde_start *= vekstfaktor
        btc_kumulativ += utbetaling_kunde_start
        årlig_liste.append(round(utbetaling_kunde_start, 2))
        år += 1

    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    if btc_kumulativ >= total_investering:
        st.success(f"Nedbetalingstid for kunde: {år} år.")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    btc_etter = round(verdi_årlig * andel_kunde / 100, 2)
    st.markdown(f"- **Kunde**: {btc_etter:.2f} kr")
    st.markdown(f"- **Tak-eier**: {utbetaling_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {utbetaling_wattoshi:.2f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    def akkumulert_verdi(startverdi, vekst, år):
        total = 0
        for _ in range(år):
            startverdi *= (1 + vekst / 100)
            total += startverdi
        return round(total, 0)

    st.markdown(f"- **Kunde**: {akkumulert_verdi(btc_etter, btc_vekst, 10):,} kr")
    st.markdown(f"- **Tak-eier**: {akkumulert_verdi(utbetaling_takeier, btc_vekst, 10):,} kr")
    st.markdown(f"- **Wattoshi**: {akkumulert_verdi(utbetaling_wattoshi, btc_vekst, 10):,} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde**: {akkumulert_verdi(btc_etter, btc_vekst, 20):,} kr")
    st.markdown(f"- **Tak-eier**: {akkumulert_verdi(utbetaling_takeier, btc_vekst, 20):,} kr")
    st.markdown(f"- **Wattoshi**: {akkumulert_verdi(utbetaling_wattoshi, btc_vekst, 20):,} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {akkumulert_verdi(btc_etter, btc_vekst, 30):,} kr")
    st.markdown(f"- **Tak-eier**: {akkumulert_verdi(utbetaling_takeier, btc_vekst, 30):,} kr")
    st.markdown(f"- **Wattoshi**: {akkumulert_verdi(utbetaling_wattoshi, btc_vekst, 30):,} kr")

    st.markdown("### Utbetaling pr år (år 1–10)")
    for i, beløp in enumerate(årlig_liste[:10], 1):
        st.markdown(f"- År {i}: {beløp:.2f} kr")
