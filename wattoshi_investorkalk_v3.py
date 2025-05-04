
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

col1, col2 = st.columns(2)

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
utbetaling_kunde_vekst = []

btc_serie = []
while btc_kumulativ < total_investering and år < 50:
    utbetaling_kunde *= vekstfaktor
    btc_kumulativ += utbetaling_kunde
    btc_serie.append(utbetaling_kunde)
    utbetaling_kunde_vekst.append(btc_kumulativ)
    år += 1

with col2:
    st.subheader("Resultater")
    st.markdown(f"**Total investering for kunde**: {total_investering:,.0f} kr")
    if btc_kumulativ >= total_investering:
        st.success(f"Nedbetalingstid for kunde: {år} år.")
    else:
        st.warning("Investeringen nedbetales ikke innen 50 år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    btc_etter = utbetaling_kunde
    btc_takeier = utbetaling_takeier
    btc_wattoshi = utbetaling_wattoshi
    st.markdown(f"- **Kunde**: {btc_etter:.2f} kr")
    st.markdown(f"- **Tak-eier**: {btc_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi**: {btc_wattoshi:.2f} kr")

    btc_kunde = 0
    btc_takeier_sum = 0
    btc_wattoshi_sum = 0
    btc_ann = btc_etter
    take_ann = btc_takeier
    watt_ann = btc_wattoshi

    for i in range(30):
        btc_ann *= vekstfaktor
        take_ann *= vekstfaktor
        watt_ann *= vekstfaktor
        btc_kunde += btc_ann
        btc_takeier_sum += take_ann
        btc_wattoshi_sum += watt_ann

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde**: {btc_kunde:,.0f} kr")
    st.markdown(f"- **Tak-eier**: {btc_takeier_sum:,.0f} kr")
    st.markdown(f"- **Wattoshi**: {btc_wattoshi_sum:,.0f} kr")

    # ROI-beregning
    annual_cashflows = [-total_investering] + btc_serie + [btc_etter * (vekstfaktor ** i) for i in range(50 - år)]
    irr = np.irr(annual_cashflows)
    roi = ((btc_kunde) / total_investering) * 100
    avg_return = (btc_kunde / total_investering) ** (1/30) - 1

    st.markdown("### Avkastningsanalyse")
    st.markdown(f"- **Internrente (IRR)**: {irr*100:.2f} %")
    st.markdown(f"- **Total ROI etter 30 år**: {roi:.2f} %")
    st.markdown(f"- **Årlig gjennomsnittlig avkastning**: {avg_return*100:.2f} %")

# Plott
årstall = list(range(1, 31))
kunde_y = []
takeier_y = []
wattoshi_y = []
investeringslinje = [total_investering] * 30

btc_e = utbetaling_kunde
btc_t = utbetaling_takeier
btc_w = utbetaling_wattoshi
sum_k = 0
sum_t = 0
sum_w = 0
for i in range(30):
    btc_e *= vekstfaktor
    btc_t *= vekstfaktor
    btc_w *= vekstfaktor
    sum_k += btc_e
    sum_t += btc_t
    sum_w += btc_w
    kunde_y.append(sum_k)
    takeier_y.append(sum_t)
    wattoshi_y.append(sum_w)

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
