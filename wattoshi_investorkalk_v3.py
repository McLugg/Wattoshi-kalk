
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

st.sidebar.header("Inputparametere")
paneler = st.sidebar.slider("Antall paneler", 1, 100, 1)
panelkapasitet = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
panelpris = st.sidebar.number_input("Pris per panel (NOK)", min_value=500, max_value=10000, value=2000)
pris_per_kwh = st.sidebar.number_input("Eksportpris (NOK/kWh)", min_value=0.1, max_value=5.0, value=0.60, step=0.1)
btc_vekst = st.sidebar.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)
produksjonstimer = st.sidebar.slider("Produksjonstimer per år", 500, 1300, 1000)

# Fordeling
st.sidebar.subheader("Fordeling av produksjonsverdi (%)")
andel_kunde = st.sidebar.slider("Kunde", 0, 100, 40)
andel_takeier = st.sidebar.slider("Tak-eier", 0, 50, 25)
andel_wattoshi = 100 - andel_kunde - andel_takeier

if andel_wattoshi < 0:
    st.error("Summen av prosentandelene overstiger 100 %. Juster verdiene.")
    st.stop()

# Beregninger
effekt_kw = panelkapasitet / 1000
produksjon_kwh_år = paneler * effekt_kw * produksjonstimer
verdi_total_år = produksjon_kwh_år * pris_per_kwh

btc_faktor = 1 + btc_vekst / 100
nedbetalingstid = 0
akk_kunde = 0
kunde_andel_kr = verdi_total_år * andel_kunde / 100
investering = paneler * panelpris

for år in range(1, 31):
    akk_kunde += kunde_andel_kr * (btc_faktor ** år)
    if akk_kunde < investering:
        nedbetalingstid = år

# Årlig utbetaling etter nedbetaling
årlig_utbetaling_kunde = kunde_andel_kr
årlig_utbetaling_takeier = verdi_total_år * andel_takeier / 100
årlig_utbetaling_wattoshi = verdi_total_år * andel_wattoshi / 100

# Akkumulert etter 30 år
akk_kunde = sum([årlig_utbetaling_kunde * (btc_faktor ** i) for i in range(1, 31)])
akk_takeier = sum([årlig_utbetaling_takeier * (btc_faktor ** i) for i in range(1, 31)])
akk_wattoshi = sum([årlig_utbetaling_wattoshi * (btc_faktor ** i) for i in range(1, 31)])

# Resultater
st.success(f"Nedbetalingstid for kunde: {nedbetalingstid} år.")

st.subheader("Årlig BTC-utbetaling etter nedbetalingstid")
st.markdown(f"- **Kunde:** {årlig_utbetaling_kunde:,.2f} kr")
st.markdown(f"- **Tak-eier:** {årlig_utbetaling_takeier:,.2f} kr")
st.markdown(f"- **Wattoshi:** {årlig_utbetaling_wattoshi:,.2f} kr")

st.subheader("Akkumulert BTC-verdi etter 30 år")
st.markdown(f"- **Kunde:** {akk_kunde:,.0f} kr")
st.markdown(f"- **Tak-eier:** {akk_takeier:,.0f} kr")
st.markdown(f"- **Wattoshi:** {akk_wattoshi:,.0f} kr")

# Plot
fig, ax = plt.subplots()
år = list(range(1, 31))
kunde = [årlig_utbetaling_kunde * (btc_faktor ** i) for i in år]
takeier = [årlig_utbetaling_takeier * (btc_faktor ** i) for i in år]
wattoshi = [årlig_utbetaling_wattoshi * (btc_faktor ** i) for i in år]

ax.plot(år, [sum(kunde[:i]) for i in range(1, 31)], label="Kumulativ (Kunde)")
ax.plot(år, [sum(takeier[:i]) for i in range(1, 31)], label="Kumulativ (Tak-eier)")
ax.plot(år, [sum(wattoshi[:i]) for i in range(1, 31)], label="Kumulativ (Wattoshi)")
ax.axhline(investering, color="red", linestyle="--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt per rolle")
ax.legend()

st.pyplot(fig)
