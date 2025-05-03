
import streamlit as st
import matplotlib.pyplot as plt

st.title("Wattoshi Investorkalkulator")

# Inndata
st.sidebar.header("Inputparametere")
panel_type = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
antall_paneler = st.sidebar.number_input("Antall paneler", min_value=1, value=1)
timer_per_år = st.sidebar.number_input("Antall produksjonstimer per år", min_value=500, max_value=1500, value=1300)
eksportpris = st.sidebar.number_input("Eksportpris (kr/kWh)", min_value=0.0, value=0.60)
panelpris = st.sidebar.number_input("Pris per panel (kr)", min_value=0, value=2000)
btc_vekst = st.sidebar.slider("BTC verdiøkning (%/år etter nedbetaling)", 0, 30, 20) / 100
levetid = st.sidebar.number_input("Levetid (år)", min_value=1, max_value=50, value=30)

# Fordeling
st.sidebar.subheader("Fordeling av produksjonsverdi (%)")
andel_kunde = st.sidebar.slider("Kunde", 0, 100, 50)
andel_ola = st.sidebar.slider("Tak-eier (Ola)", 0, 100, 25)
andel_wattoshi = 100 - andel_kunde - andel_ola
if andel_wattoshi < 0:
    st.sidebar.error("Fordelingen overstiger 100 %!")
    st.stop()

# Kalkulasjoner
produksjon_kwh_per_panel = panel_type * timer_per_år / 1000
total_kwh = produksjon_kwh_per_panel * antall_paneler
total_verdi = total_kwh * eksportpris

årlig_kunde = total_verdi * andel_kunde / 100
årlig_ola = total_verdi * andel_ola / 100
årlig_wattoshi = total_verdi * andel_wattoshi / 100

# Beregning av nedbetalingstid
investeringskost = panelpris * antall_paneler
kumulativ = 0
år_nedbetalt = None
resultater = []

for år in range(1, levetid + 1):
    if år_nedbetalt is None:
        kumulativ += årlig_kunde
        if kumulativ >= investeringskost:
            år_nedbetalt = år
    else:
        kumulativ = (kumulativ + årlig_kunde) * (1 + btc_vekst)
    resultater.append(kumulativ)

# Utdata
if år_nedbetalt:
    st.success(f"Nedbetalingstid: {år_nedbetalt} år")
else:
    st.warning("Investeringen nedbetales ikke i løpet av levetiden.")

st.write(f"**Årlig produksjon:** {total_kwh:.1f} kWh")
st.write(f"**Årlig kundeutbetaling:** {årlig_kunde:.2f} kr")
st.write(f"**Årlig Ola (tak-eier) utbetaling:** {årlig_ola:.2f} kr")
st.write(f"**Årlig Wattoshi utbetaling:** {årlig_wattoshi:.2f} kr")

if år_nedbetalt:
    st.write(f"**Årlig BTC-utbytte etter nedbetalingstid:** {årlig_kunde:.2f} kr med {int(btc_vekst*100)} % årlig vekst")

st.write(f"**Total kundeopptjent verdi etter {levetid} år:** {resultater[-1]:,.2f} kr")

# Visualisering
fig, ax = plt.subplots()
ax.plot(range(1, levetid + 1), resultater, label="Kumulativ kundeinntekt")
ax.axhline(y=investeringskost, color="red", linestyle="--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Kr")
ax.set_title("Utvikling i kundens inntekt")
ax.legend()
st.pyplot(fig)
