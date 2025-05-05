
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Layout
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("Inputparametere")
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
andel_kunde_decimal = andel_kunde / 100
btc_growth = btc_vekst / 100
investering = antall_paneler * pris_per_panel

# Kalkulere årlig og akkumulert inntekt for kunde
år = list(range(0, 31))
årlig_inntekt = []
akkumulert = []
sum_inntekt = 0
nedbetalt_markert = []
flag = False

for n in år:
    inntekt = verdi_årlig * (1 + btc_growth) ** n * andel_kunde_decimal
    sum_inntekt += inntekt
    årlig_inntekt.append(round(inntekt, 2))
    akkumulert.append(round(sum_inntekt, 2))
    if not flag and sum_inntekt >= investering:
        nedbetalt_markert.append("✅")
        flag = True
    else:
        nedbetalt_markert.append("")

# Presentere som tabell
df = pd.DataFrame({
    "År": år,
    "Årlig inntekt kunde (NOK)": årlig_inntekt,
    "Akkumulert inntekt (NOK)": akkumulert,
    "Nedbetalt": nedbetalt_markert
})

with col2:
    st.subheader("Inntektstabell år 0–30")
    st.dataframe(df, use_container_width=True)

    st.subheader("Graf – Akkumulert inntekt")
    fig, ax = plt.subplots()
    ax.plot(år, akkumulert, marker='o', label="Akkumulert verdi")
    ax.axhline(investering, color='r', linestyle='--', label="Investering")
    ax.set_xlabel("År")
    ax.set_ylabel("Verdi (NOK)")
    ax.set_title("Akkumulert verdi over tid for kunde")
    ax.legend()
    st.pyplot(fig)
