
import streamlit as st
import matplotlib.pyplot as plt

# Input parameters
st.sidebar.header("Inputparametere")

antall_paneler = st.sidebar.slider("Antall paneler", 1, 100, 1)
panelkapasitet = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
pris_per_panel = st.sidebar.number_input("Pris per panel (NOK)", value=2000)
eksportpris = st.sidebar.number_input("Eksportpris (NOK/kWh)", value=2.0)
btc_vekst = st.sidebar.slider("Årlig BTC verdiøkning (%)", 0, 50, 20) / 100

st.sidebar.markdown("### Fordeling av produksjonsverdi (%)")
andel_kunde = st.sidebar.slider("Kunde", 0, 100, 50)
andel_takeier = st.sidebar.slider("Tak-eier", 0, 50, 30)
andel_wattoshi = 100 - andel_kunde - andel_takeier

if andel_wattoshi < 0:
    st.error("Summen av kunde og tak-eier kan ikke overstige 100 %.")
    st.stop()

# Beregninger
produksjon_kwh_per_år = antall_paneler * panelkapasitet / 1000
total_verdi_per_år = produksjon_kwh_per_år * eksportpris

inntekt_kunde = total_verdi_per_år * andel_kunde / 100
inntekt_takeier = total_verdi_per_år * andel_takeier / 100
inntekt_wattoshi = total_verdi_per_år * andel_wattoshi / 100

investeringskostnad = antall_paneler * pris_per_panel

# Nedbetalingstid (kun basert på fast årlig beløp uten BTC vekst)
if inntekt_kunde > 0:
    nedbetalingstid = investeringskostnad / inntekt_kunde
    nedbetalingstid_tekst = f"Nedbetalingstid for kunde: {nedbetalingstid:.0f} år."
else:
    nedbetalingstid_tekst = "Ingen inntekt til kunde – nedbetaling ikke mulig."

# Akkumulert verdi med BTC-vekst
år = list(range(1, 31))
btc_kunde = []
btc_takeier = []
btc_wattoshi = []

v_kunde = 0
v_takeier = 0
v_wattoshi = 0

for _ in år:
    v_kunde = (v_kunde + inntekt_kunde) * (1 + btc_vekst)
    v_takeier = (v_takeier + inntekt_takeier) * (1 + btc_vekst)
    v_wattoshi = (v_wattoshi + inntekt_wattoshi) * (1 + btc_vekst)
    btc_kunde.append(v_kunde)
    btc_takeier.append(v_takeier)
    btc_wattoshi.append(v_wattoshi)

# Resultater
st.title("Wattoshi Panelinvestor Kalkulator –
Fordeling Kunde / Tak-eier / Wattoshi")
st.success(nedbetalingstid_tekst)

st.subheader("Årlig BTC-utbetaling etter nedbetalingstid")
st.markdown(f"- Kunde: {inntekt_kunde:.2f} kr")
st.markdown(f"- Tak-eier: {inntekt_takeier:.2f} kr")
st.markdown(f"- Wattoshi: {inntekt_wattoshi:.2f} kr")

st.subheader("Akkumulert BTC-verdi etter 30 år")
st.markdown(f"- Kunde: {v_kunde:.0f} kr")
st.markdown(f"- Tak-eier: {v_takeier:.0f} kr")
st.markdown(f"- Wattoshi: {v_wattoshi:.0f} kr")

# Visualisering
fig, ax = plt.subplots()
ax.plot(år, btc_kunde, label="Kumulativ (Kunde)")
ax.plot(år, btc_takeier, label="Kumulativ (Tak-eier)")
ax.plot(år, btc_wattoshi, label="Kumulativ (Wattoshi)")
ax.axhline(y=investeringskostnad, color='red', linestyle='--', label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt per rolle")
ax.legend()
st.pyplot(fig)
