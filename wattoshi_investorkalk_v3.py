
import streamlit as st
import matplotlib.pyplot as plt

def beregn_kundeinntekter(antall_paneler, panelkapasitet_watt, pris_per_panel,
                           eksportpris_nok_per_kwh, btc_vekst_prosent,
                           andel_kunde, andel_takeier):
    produksjon_kwh_per_år = (antall_paneler * panelkapasitet_watt) / 1000
    årlig_verdi = produksjon_kwh_per_år * eksportpris_nok_per_kwh

    kunde_andel = årlig_verdi * andel_kunde / 100
    takeier_andel = årlig_verdi * andel_takeier / 100
    wattoshi_andel = årlig_verdi * (100 - andel_kunde - andel_takeier) / 100

    levetid = 30
    btc_vekst = 1 + btc_vekst_prosent / 100

    def akkumulert_verdi(start, rente, år):
        return start * (rente**år)

    kunde_akk = sum(akkumulert_verdi(kunde_andel, btc_vekst, 30 - i) for i in range(levetid))
    takeier_akk = sum(akkumulert_verdi(takeier_andel, btc_vekst, 30 - i) for i in range(levetid))
    wattoshi_akk = sum(akkumulert_verdi(wattoshi_andel, btc_vekst, 30 - i) for i in range(levetid))

    # Finne nedbetalingstid
    nedbetalingstid = 30
    cumul = 0
    for i in range(1, 31):
        cumul += akkumulert_verdi(kunde_andel, btc_vekst, 30 - i)
        if cumul >= pris_per_panel:
            nedbetalingstid = i
            break

    return {
        "nedbetalingstid": nedbetalingstid,
        "årlig_kunde": kunde_andel,
        "årlig_takeier": takeier_andel,
        "årlig_wattoshi": wattoshi_andel,
        "akk_kunde": kunde_akk,
        "akk_takeier": takeier_akk,
        "akk_wattoshi": wattoshi_akk,
        "år": list(range(1, 31)),
        "kunde_inntekt": [sum(akkumulert_verdi(kunde_andel, btc_vekst, 30 - i) for i in range(år)) for år in range(1, 31)],
        "takeier_inntekt": [sum(akkumulert_verdi(takeier_andel, btc_vekst, 30 - i) for i in range(år)) for år in range(1, 31)],
        "wattoshi_inntekt": [sum(akkumulert_verdi(wattoshi_andel, btc_vekst, 30 - i) for i in range(år)) for år in range(1, 31)],
    }

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

st.sidebar.header("Inputparametere")
antall_paneler = st.sidebar.slider("Antall paneler", 1, 100, 1)
panelkapasitet = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
pris_per_panel = st.sidebar.number_input("Pris per panel (NOK)", value=2000)
eksportpris = st.sidebar.number_input("Eksportpris (NOK/kWh)", value=2.0)
btc_vekst = st.sidebar.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)

st.sidebar.markdown("### Fordeling av produksjonsverdi (%)")
andel_kunde = st.sidebar.slider("Kunde", 0, 100, 50)
andel_takeier = st.sidebar.slider("Tak-eier", 0, 50, 30)

result = beregn_kundeinntekter(
    antall_paneler, panelkapasitet, pris_per_panel,
    eksportpris, btc_vekst,
    andel_kunde, andel_takeier
)

st.success(f"Nedbetalingstid for kunde: {result['nedbetalingstid']} år.")

st.subheader("Årlig BTC-utbetaling etter nedbetalingstid")
st.markdown(f"- Kunde: {result['årlig_kunde']:.2f} kr")
st.markdown(f"- Tak-eier: {result['årlig_takeier']:.2f} kr")
st.markdown(f"- Wattoshi: {result['årlig_wattoshi']:.2f} kr")

st.subheader("Akkumulert BTC-verdi etter 30 år")
st.markdown(f"- Kunde: {result['akk_kunde']:.0f} kr")
st.markdown(f"- Tak-eier: {result['akk_takeier']:.0f} kr")
st.markdown(f"- Wattoshi: {result['akk_wattoshi']:.0f} kr")

st.subheader("Kumulativ Inntekt per rolle")
fig, ax = plt.subplots()
ax.plot(result['år'], result['kunde_inntekt'], label="Kumulativ (Kunde)")
ax.plot(result['år'], result['takeier_inntekt'], label="Kumulativ (Tak-eier)")
ax.plot(result['år'], result['wattoshi_inntekt'], label="Kumulativ (Wattoshi)")
ax.axhline(y=pris_per_panel, color="red", linestyle="dashed", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.legend()
st.pyplot(fig)
