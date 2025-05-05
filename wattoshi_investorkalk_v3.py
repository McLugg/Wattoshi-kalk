
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Inputparametere
col1, col2 = st.columns([1, 1.5])
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

# Beregninger
år = list(range(0, 31))
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris
btc_growth = btc_vekst / 100
investering = antall_paneler * pris_per_panel

# Beregn årlige verdier
kunde_inntekt, takeier_inntekt, wattoshi_inntekt = [], [], []
akk_kunde = 0
nedbetaling_tid = None
akkum_kunde, akkum_takeier, akkum_wattoshi = [], [], []

for n in år:
    total = verdi_årlig * ((1 + btc_growth) ** n)
    k = total * (andel_kunde / 100)
    t = total * (andel_takeier / 100)
    w = total * (andel_wattoshi / 100)
    akk_kunde += k
    kunde_inntekt.append(round(k, 2))
    takeier_inntekt.append(round(t, 2))
    wattoshi_inntekt.append(round(w, 2))
    if not nedbetaling_tid and akk_kunde >= investering:
        år_før = n - 1
        if år_før < 0:
            nedbetaling_tid = 0.0
        else:
            diff = investering - sum(kunde_inntekt[:-1])
            steg = k
            nedbetaling_tid = år_før + (diff / steg)

    # For ny tabell
    if n in [10, 20, 30]:
        akkum_kunde.append(round(sum(kunde_inntekt[:n+1]), 2))
        akkum_takeier.append(round(sum(takeier_inntekt[:n+1]), 2))
        akkum_wattoshi.append(round(sum(wattoshi_inntekt[:n+1]), 2))

# Resultatvisning
with col2:
    st.subheader("🔍 Resultater")
    st.markdown(f"### 💸 Kundens investering: **{investering:,.0f} kr**")
    if nedbetaling_tid:
        st.success(f"✅ **Nedbetalt etter {nedbetaling_tid:.2f} år**")
    else:
        st.warning("⏳ Ikke nedbetalt innen 30 år")

    st.markdown("#### 📊 Akkumulert inntekt (etter 10, 20, 30 år)")
    df_summary = pd.DataFrame({
        "År": [10, 20, 30],
        "Kunde (NOK)": akkum_kunde,
        "Tak-eier (NOK)": akkum_takeier,
        "Wattoshi (NOK)": akkum_wattoshi
    })
    st.table(df_summary)

    st.subheader("📈 Graf – Årlig utbetaling per aktør")
    fig, ax = plt.subplots()
    ax.plot(år, kunde_inntekt, label="Kunde", color="green")
    ax.plot(år, takeier_inntekt, label="Tak-eier", color="orange")
    ax.plot(år, wattoshi_inntekt, label="Wattoshi", color="blue")
    ax.axhline(investering, color="red", linestyle="--", label="Investering (kunde)")
    ax.set_xlabel("År")
    ax.set_ylabel("Årlig utbetaling (NOK)")
    ax.set_title("Årlig verdi av produksjon fordelt på aktører")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📊 Tabell – Kundeinntekt år 0–30")
    total = 0
    akkum_kunde_alle = []
    for beløp in kunde_inntekt:
        total += beløp
        akkum_kunde_alle.append(round(total, 2))
    df = pd.DataFrame({
        "År": år,
        "Årlig inntekt (NOK)": kunde_inntekt,
        "Akkumulert inntekt (NOK)": akkum_kunde_alle
    })
    st.dataframe(df, use_container_width=True)
