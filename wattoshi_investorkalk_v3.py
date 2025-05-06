
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

# Beregning
år = list(range(0, 31))
produksjon_kwh = antall_paneler * panelkapasitet / 1000 * produksjonstimer
verdi_årlig = produksjon_kwh * eksportpris
btc_growth = btc_vekst / 100
investering = antall_paneler * pris_per_panel

# Årlig inntekt uten BTC
årlig_kunde = verdi_årlig * andel_kunde / 100
årlig_takeier = verdi_årlig * andel_takeier / 100
årlig_wattoshi = verdi_årlig * andel_wattoshi / 100

# Akkumulert verdi per år med korrekt reinvestering
def akk_serie(inntekt, vekst, år):
    resultater = []
    for n in range(år + 1):
        total = sum([inntekt * ((1 + vekst) ** (n - i)) for i in range(n + 1)])
        resultater.append(round(total, 4))
    return resultater

kunde_akk = akk_serie(årlig_kunde, btc_growth, 30)
takeier_akk = akk_serie(årlig_takeier, btc_growth, 30)
wattoshi_akk = akk_serie(årlig_wattoshi, btc_growth, 30)

# Nedbetalingstid
nedbetaling_tid = None
for i in range(1, len(kunde_akk)):
    if kunde_akk[i] >= investering:
        før = kunde_akk[i-1]
        etter = kunde_akk[i]
        interpolert = i - 1 + (investering - før) / (etter - før)
        nedbetaling_tid = round(interpolert, 2)
        break

# Akkumulert verdi etter 10/20/30
akkum_kunde = [kunde_akk[i] for i in [10, 20, 30]]
akkum_takeier = [takeier_akk[i] for i in [10, 20, 30]]
akkum_wattoshi = [wattoshi_akk[i] for i in [10, 20, 30]]

with col2:
    st.subheader("🔍 Resultater")
    st.markdown(f"### 💸 Kundens investering: **{investering:,.0f} kr**")
    if nedbetaling_tid:
        st.success(f"✅ **Nedbetalt etter {nedbetaling_tid:.2f} år**")
    else:
        st.warning("⏳ Ikke nedbetalt innen 30 år")

    st.markdown("#### 💼 Årlig utbetaling uten BTC-vekst")
    st.table(pd.DataFrame({
        "Rolle": ["Kunde", "Tak-eier", "Wattoshi"],
        "Årlig utbetaling (NOK)": [round(årlig_kunde, 4), round(årlig_takeier, 4), round(årlig_wattoshi, 4)]
    }))

    st.markdown("#### 📊 Akkumulert inntekt (etter 10, 20, 30 år)")
    st.table(pd.DataFrame({
        "År": [10, 20, 30],
        "Kunde (NOK)": akkum_kunde,
        "Tak-eier (NOK)": akkum_takeier,
        "Wattoshi (NOK)": akkum_wattoshi
    }))

    st.subheader("📈 Graf – Akkumulert verdi per aktør")
    fig, ax = plt.subplots()
    ax.plot(år, kunde_akk, label="Kunde", color="green")
    ax.plot(år, takeier_akk, label="Tak-eier", color="orange")
    ax.plot(år, wattoshi_akk, label="Wattoshi", color="blue")
    ax.axhline(investering, color="red", linestyle="--", label="Investering")
    ax.set_xlabel("År")
    ax.set_ylabel("Akkumulert verdi (NOK)")
    ax.set_title("Akkumulert verdi ved årlig utbetaling og BTC-vekst")
    ax.legend()
    st.pyplot(fig)

    st.subheader("📊 Tabell – Kundeinntekt år 0–30")
    df = pd.DataFrame({
        "År": år,
        "Akkumulert inntekt (NOK)": kunde_akk
    })
    st.dataframe(df, use_container_width=True)
