
import streamlit as st
import matplotlib.pyplot as plt

# Tittel
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Inputparametere
antall_paneler = st.slider("Antall paneler", 1, 100, 1)
panelkapasitet = st.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
pris_per_panel = st.number_input("Pris per panel (NOK)", value=2000)
eksportpris = st.number_input("Eksportpris (NOK/kWh)", value=0.6)
btc_vekst = st.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)
produksjonstimer = st.slider("Produksjonstimer per år", 500, 1300, 1000)

# Fordeling
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

utbetaling_kunde_base = verdi_årlig * andel_kunde / 100
utbetaling_takeier_base = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi_base = verdi_årlig * andel_wattoshi / 100

# Nedbetalingstid
total_investering = antall_paneler * pris_per_panel
btc_kumulativ = 0
år = 0
vekstfaktor = 1 + btc_vekst / 100
btc_vekst_liste = []
btc_kunde = utbetaling_kunde_base

while btc_kumulativ < total_investering and år < 50:
    btc_kumulativ += btc_kunde
    btc_kunde *= vekstfaktor
    btc_vekst_liste.append(btc_kumulativ)
    år += 1

if btc_kumulativ >= total_investering:
    st.success(f"Nedbetalingstid for kunde: {år} år.")
else:
    st.warning("Investeringen nedbetales ikke innen 50 år.")

# Årlig BTC etter nedbetaling (år + 1)
btc_etter_kunde = utbetaling_kunde_base
btc_etter_takeier = utbetaling_takeier_base
btc_etter_wattoshi = utbetaling_wattoshi_base

st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
st.markdown(f"- **Kunde**: {btc_etter_kunde:.2f} kr")
st.markdown(f"- **Tak-eier**: {btc_etter_takeier:.2f} kr")
st.markdown(f"- **Wattoshi**: {btc_etter_wattoshi:.2f} kr")

# Akkumulert BTC-verdi etter 30 år
btc_kunde = 0
btc_takeier_sum = 0
btc_wattoshi_sum = 0
btc_e = btc_etter_kunde
btc_t = btc_etter_takeier
btc_w = btc_etter_wattoshi

for i in range(30):
    btc_kunde += btc_e
    btc_takeier_sum += btc_t
    btc_wattoshi_sum += btc_w
    btc_e *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor

st.markdown("### Akkumulert BTC-verdi etter 30 år")
st.markdown(f"- **Kunde**: {btc_kunde:,.0f} kr")
st.markdown(f"- **Tak-eier**: {btc_takeier_sum:,.0f} kr")
st.markdown(f"- **Wattoshi**: {btc_wattoshi_sum:,.0f} kr")

# Plot
årstall = list(range(1, 31))
kunde_y, takeier_y, wattoshi_y = [], [], []
btc_e = btc_etter_kunde
btc_t = btc_etter_takeier
btc_w = btc_etter_wattoshi
sum_k = sum_t = sum_w = 0

for i in range(30):
    sum_k += btc_e
    sum_t += btc_t
    sum_w += btc_w
    kunde_y.append(sum_k)
    takeier_y.append(sum_t)
    wattoshi_y.append(sum_w)
    btc_e *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor

fig, ax = plt.subplots()
ax.plot(årstall, kunde_y, label="Kumulativ (Kunde)")
ax.plot(årstall, takeier_y, label="Kumulativ (Tak-eier)")
ax.plot(årstall, wattoshi_y, label="Kumulativ (Wattoshi)")
ax.plot(årstall, [total_investering] * 30, "r--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt per rolle")
ax.legend()
st.pyplot(fig)
