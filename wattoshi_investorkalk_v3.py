
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

# Grunnverdier
år = list(range(0, 31))
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris
btc_growth = btc_vekst / 100
investering = antall_paneler * pris_per_panel

# Årlig utbetaling per rolle (konstant)
årlig_kunde = verdi_årlig * andel_kunde / 100
årlig_takeier = verdi_årlig * andel_takeier / 100
årlig_wattoshi = verdi_årlig * andel_wattoshi / 100

# Akkumulert vekst
def fremtidsverdi_per_år(beløp, vekst, år):
    return [round(beløp * ((1 + vekst) ** (år - i)), 2) for i in range(år + 1)]

kunde_per_år = []
takeier_per_år = []
wattoshi_per_år = []

akk_kunde = 0
nedbetaling_tid = None

for n in år:
    k_list = fremtidsverdi_per_år(årlig_kunde, btc_growth, n)
    t_list = fremtidsverdi_per_år(årlig_takeier, btc_growth, n)
    w_list = fremtidsverdi_per_år(årlig_wattoshi, btc_growth, n)
    k = round(sum(k_list), 2)
    t = round(sum(t_list), 2)
    w = round(sum(w_list), 2)
    kunde_per_år.append(k)
    takeier_per_år.append(t)
    wattoshi_per_år.append(w)
    if not nedbetaling_tid and k >= investering:
        nedbetaling_tid = n

# Akkumulert inntekt 10/20/30 år
akkum_kunde = [round(kunde_per_år[i], 2) for i in [10, 20, 30]]
akkum_takeier = [round(takeier_per_år[i], 2) for i in [10, 20, 30]]
akkum_wattoshi = [round(wattoshi_per_år[i], 2) for i in [10, 20, 30]]

with col2:
    st.subheader("🔍 Resultater")
    st.markdown(f"### 💸 Kundens investering: **{investering:,.0f} kr**")
    if nedbetaling_tid is not None:
        st.success(f"✅ **Nedbetalt etter {nedbetaling_tid:.2f} år**")
    else:
        st.warning("⏳ Ikke nedbetalt innen 30 år")

    # Fast årlig verdi uten vekst
    st.markdown("#### 💼 Årlig utbetaling uten BTC-vekst")
    st.table(pd.DataFrame({
        "Rolle": ["Kunde", "Tak-eier", "Wattoshi"],
        "Årlig utbetaling (NOK)": [round(årlig_kunde, 2), round(årlig_takeier, 2), round(årlig_wattoshi, 2)]
    }))

    # Akkumulert tabell
    st.markdown("#### 📊 Akkumulert inntekt (etter 10, 20, 30 år)")
    st.table(pd.DataFrame({
        "År": [10, 20, 30],
        "Kunde (NOK)": akkum_kunde,
        "Tak-eier (NOK)": akkum_takeier,
        "Wattoshi (NOK)": akkum_wattoshi
    }))

    # Graf
    st.subheader("📈 Graf – Akkumulert verdi per aktør")
    fig, ax = plt.subplots()
    ax.plot(år, kunde_per_år, label="Kunde", color="green")
    ax.plot(år, takeier_per_år, label="Tak-eier", color="orange")
    ax.plot(år, wattoshi_per_år, label="Wattoshi", color="blue")
    ax.axhline(investering, color="red", linestyle="--", label="Investering")
    ax.set_xlabel("År")
    ax.set_ylabel("Akkumulert verdi (NOK)")
    ax.set_title("Akkumulert verdi ved årlig utbetaling og BTC-vekst")
    ax.legend()
    st.pyplot(fig)

    # Tabell for kunde
    st.subheader("📊 Tabell – Kundeinntekt år 0–30")
    df = pd.DataFrame({
        "År": år,
        "Akkumulert inntekt (NOK)": kunde_per_år
    })
    st.dataframe(df, use_container_width=True)
