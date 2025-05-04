
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import streamlit as st

# INPUTS
st.set_page_config(layout="wide")
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

# BEREGNING
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris

utbetaling_kunde = verdi_årlig * andel_kunde / 100
utbetaling_takeier = verdi_årlig * andel_takeier / 100
utbetaling_wattoshi = verdi_årlig * andel_wattoshi / 100

# Nedbetalingstid
total_investering = antall_paneler * pris_per_panel
btc_kumulativ = 0
år = 0
vekstfaktor = 1 + btc_vekst / 100
utbetaling_k = utbetaling_kunde
utbetaling_kunde_vekst = []

while btc_kumulativ < total_investering and år < 50:
    utbetaling_k *= vekstfaktor
    btc_kumulativ += utbetaling_k
    utbetaling_kunde_vekst.append(btc_kumulativ)
    år += 1

nedbetalingstid = år if btc_kumulativ >= total_investering else None

# Årlig BTC etter nedbetaling
btc_k = utbetaling_k
btc_t = utbetaling_takeier
btc_w = utbetaling_wattoshi

btc_k_sum = 0
btc_t_sum = 0
btc_w_sum = 0
cashflows = [-total_investering]

kunde_y = []
takeier_y = []
wattoshi_y = []
årstall = list(range(1, 31))
investeringslinje = [total_investering] * 30

for i in range(30):
    btc_k *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor
    btc_k_sum += btc_k
    btc_t_sum += btc_t
    btc_w_sum += btc_w
    cashflows.append(btc_k)
    kunde_y.append(btc_k_sum)
    takeier_y.append(btc_t_sum)
    wattoshi_y.append(btc_w_sum)

# RESULTATER
with col2:
    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    if nedbetalingstid:
        st.success(f"Nedbetalingstid for kunde: {nedbetalingstid} år.")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde**: {utbetaling_k:,.2f} kr")
    st.markdown(f"- **Tak-eier**: {utbetaling_takeier:,.2f} kr")
    st.markdown(f"- **Wattoshi**: {utbetaling_wattoshi:,.2f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {btc_k_sum:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {btc_t_sum:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {btc_w_sum:,.0f} kr")

    roi = ((btc_k_sum - total_investering) / total_investering) * 100
    irr = npf.irr(cashflows)
    annualized_return = (btc_k_sum / total_investering)**(1/30) - 1

    st.markdown("### Nøkkeltall for kunde")
    st.markdown(f"- **Internrente (IRR)**: {irr * 100:.2f} %")
    st.markdown(f"- **Total ROI etter 30 år**: {roi:.2f} %")
    st.markdown(f"- **Årlig gjennomsnittlig avkastning**: {annualized_return * 100:.2f} %")

# GRAF
fig, ax = plt.subplots()
ax.plot(årstall, kunde_y, label="Kumulativ (Kunde)")
ax.plot(årstall, takeier_y, label="Kumulativ (Tak-eier)")
ax.plot(årstall, wattoshi_y, label="Kumulativ (Wattoshi)")
ax.plot(årstall, investeringslinje, "r--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt per rolle")
ax.legend()
st.pyplot(fig)
