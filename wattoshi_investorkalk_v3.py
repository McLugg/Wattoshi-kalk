
import streamlit as st
import matplotlib.pyplot as plt

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
vekstfaktor = 1 + btc_vekst / 100

btc_kumulativ = utbetaling_kunde
btc_etter = utbetaling_kunde
år = 1
while btc_kumulativ < total_investering and år < 50:
    btc_etter *= vekstfaktor
    btc_kumulativ += btc_etter
    år += 1

with col2:
    st.markdown("### Resultater")
    st.markdown(f"**Total investering for kunde:** {total_investering:,.0f} kr")
    st.success(f"Nedbetalingstid for kunde: {år:.2f} år.")

    st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
    st.markdown(f"- **Kunde:** {utbetaling_kunde:.2f} kr")
    st.markdown(f"- **Tak-eier:** {utbetaling_takeier:.2f} kr")
    st.markdown(f"- **Wattoshi:** {utbetaling_wattoshi:.2f} kr")

btc_kunde = 0
btc_takeier_sum = 0
btc_wattoshi_sum = 0

btc_ek = utbetaling_kunde
btc_et = utbetaling_takeier
btc_ew = utbetaling_wattoshi

årstall = list(range(1, 31))
kunde_y, takeier_y, wattoshi_y = [], [], []
investeringslinje = [total_investering] * 30

btc_tabell = []
btc_r = utbetaling_kunde
btc_sum = btc_r

btc_tabell.append((0, btc_r, btc_sum))
for i in range(1, 31):
    btc_r *= vekstfaktor
    btc_sum += btc_r
    btc_tabell.append((i, btc_r, btc_sum))

    btc_ek *= vekstfaktor
    btc_et *= vekstfaktor
    btc_ew *= vekstfaktor

    btc_kunde += btc_ek
    btc_takeier_sum += btc_et
    btc_wattoshi_sum += btc_ew

    kunde_y.append(btc_kunde)
    takeier_y.append(btc_takeier_sum)
    wattoshi_y.append(btc_wattoshi_sum)

with col2:
    st.markdown("### Akkumulert BTC-verdi etter 10 år")
    st.markdown(f"- **Kunde:** {kunde_y[9]:,.0f} kr")
    st.markdown(f"- **Tak-eier:** {takeier_y[9]:,.0f} kr")
    st.markdown(f"- **Wattoshi:** {wattoshi_y[9]:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 20 år")
    st.markdown(f"- **Kunde:** {kunde_y[19]:,.0f} kr")
    st.markdown(f"- **Tak-eier:** {takeier_y[19]:,.0f} kr")
    st.markdown(f"- **Wattoshi:** {wattoshi_y[19]:,.0f} kr")

    st.markdown("### Akkumulert BTC-verdi etter 30 år")
    st.markdown(f"- **Kunde:** {kunde_y[29]:,.0f} kr")
    st.markdown(f"- **Tak-eier:** {takeier_y[29]:,.0f} kr")
    st.markdown(f"- **Wattoshi:** {wattoshi_y[29]:,.0f} kr")

    st.markdown("### Årlig utbetaling og akkumulert sum (år 0–10)")
    for i in range(11):
        st.markdown(f"- År {btc_tabell[i][0]}: {btc_tabell[i][1]:.2f} kr (kumulativ: {btc_tabell[i][2]:.2f} kr)")

fig, ax = plt.subplots()
ax.plot(årstall, kunde_y, label="Kumulativ (Kunde)")
ax.plot(årstall, takeier_y, label="Kumulativ (Tak-eier)")
ax.plot(årstall, wattoshi_y, label="Kumulativ (Wattoshi)")
ax.plot(årstall, investeringslinje, "r--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ inntekt per rolle")
ax.legend()
st.pyplot(fig)
