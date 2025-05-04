
import streamlit as st
import matplotlib.pyplot as plt

# Tittel og layout
st.set_page_config(layout="wide")
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")
col1, col2 = st.columns([1, 1])

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

produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris

utbetaling_kunde = verdi_årlig * andel_kunde / 100
utbetaling_takeier = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

total_investering = antall_paneler * pris_per_panel
btc_kumulativ = 0
år = 0
vekstfaktor = 1 + btc_vekst / 100
btc_vekst_liste = []
kunde_utbetaling = utbetaling_kunde

while btc_kumulativ < total_investering and år < 50:
    kunde_utbetaling *= vekstfaktor
    btc_kumulativ += kunde_utbetaling
    btc_vekst_liste.append(btc_kumulativ)
    år += 1

with col2:
    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde**: {total_investering:,.0f} kr")
    if btc_kumulativ >= total_investering:
        st.success(f"Nedbetalingstid for kunde: {år} år.")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde**: {utbetaling_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier**: {utbetaling_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {utbetaling_wattoshi:.2f} kr")

    btc_kunde = btc_takeier = btc_wattoshi = 0
    kunde_10 = kunde_20 = kunde_30 = 0
    takeier_10 = takeier_20 = takeier_30 = 0
    wattoshi_10 = wattoshi_20 = wattoshi_30 = 0

    y_kunde = []
    y_takeier = []
    y_wattoshi = []
    investeringslinje = [total_investering] * 30

    u_kunde = utbetaling_kunde
    u_takeier = utbetaling_takeier
    u_wattoshi = utbetaling_wattoshi

    for i in range(30):
        u_kunde *= vekstfaktor
        u_takeier *= vekstfaktor
        u_wattoshi *= vekstfaktor

        btc_kunde += u_kunde
        btc_takeier += u_takeier
        btc_wattoshi += u_wattoshi

        y_kunde.append(btc_kunde)
        y_takeier.append(btc_takeier)
        y_wattoshi.append(btc_wattoshi)

        if i == 9:
            kunde_10, takeier_10, wattoshi_10 = btc_kunde, btc_takeier, btc_wattoshi
        elif i == 19:
            kunde_20, takeier_20, wattoshi_20 = btc_kunde, btc_takeier, btc_wattoshi
        elif i == 29:
            kunde_30, takeier_30, wattoshi_30 = btc_kunde, btc_takeier, btc_wattoshi

    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde**: {kunde_10:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {takeier_10:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {wattoshi_10:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde**: {kunde_20:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {takeier_20:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {wattoshi_20:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {kunde_30:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {takeier_30:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {wattoshi_30:,.0f} kr")

    roi = ((btc_kunde - total_investering) / total_investering) * 100
    cagr = ((btc_kunde / total_investering) ** (1 / 30) - 1) * 100

    st.markdown("### Investeringsnøkkeltall")
    st.markdown(f"- **ROI**: {roi:.0f} %")
    st.markdown(f"- **CAGR**: {cagr:.2f} %")

    fig, ax = plt.subplots(figsize=(6, 4))
    årstall = list(range(1, 31))
    ax.plot(årstall, y_kunde, label="Kumulativ (Kunde)")
    ax.plot(årstall, y_takeier, label="Kumulativ (Tak-eier)")
    ax.plot(årstall, y_wattoshi, label="Kumulativ (Wattoshi)")
    ax.plot(årstall, investeringslinje, "r--", label="Investering")
    ax.set_xlabel("År")
    ax.set_ylabel("Verdi (NOK)")
    ax.set_title("Kumulativ inntekt per rolle")
    ax.legend()
    st.pyplot(fig)
