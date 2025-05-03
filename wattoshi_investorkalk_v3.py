
import streamlit as st
import matplotlib.pyplot as plt

# App title
st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Input parameters
st.sidebar.header("Inputparametere")

num_panels = st.sidebar.slider("Antall paneler", 1, 100, 10)
panel_capacity = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
panel_price = st.sidebar.number_input("Pris per panel (NOK)", min_value=1000, max_value=10000, value=3500, step=100)
export_price = st.sidebar.number_input("Eksportpris (NOK/kWh)", min_value=0.10, max_value=5.0, value=0.60, step=0.01)
btc_growth = st.sidebar.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)
år = 30

st.sidebar.markdown("### Fordeling av produksjonsverdi (%)")
kunde_andel = st.sidebar.slider("Kunde", 0, 100, 50)
tak_eier_andel = st.sidebar.slider("Tak-eier", 0, 100 - kunde_andel, 25)
wattoshi_andel = 100 - kunde_andel - tak_eier_andel
st.sidebar.markdown(f"Wattoshi: {wattoshi_andel} %")

# Produksjonsberegning
panel_kw = panel_capacity / 1000
annual_production_kwh = panel_kw * 1000 * num_panels  # 1000 kWh/kWp
total_investering = num_panels * panel_price

kunde_andel_verdi = (kunde_andel / 100) * annual_production_kwh * export_price
tak_eier_andel_verdi = (tak_eier_andel / 100) * annual_production_kwh * export_price
wattoshi_andel_verdi = (wattoshi_andel / 100) * annual_production_kwh * export_price

btc_multiplier = 1
kunde_btc = []
tak_eier_btc = []
wattoshi_btc = []
kumulative_kunde = []

for i in range(1, år + 1):
    btc_multiplier *= 1 + (btc_growth / 100)
    kunde_verdi = kunde_andel_verdi * btc_multiplier
    tak_verdi = tak_eier_andel_verdi * btc_multiplier
    wattoshi_verdi = wattoshi_andel_verdi * btc_multiplier

    kunde_btc.append(kunde_verdi)
    tak_eier_btc.append(tak_verdi)
    wattoshi_btc.append(wattoshi_verdi)
    kumulative_kunde.append(sum(kunde_btc))

# Beregn nedbetalingstid
nedbetalingstid = next((i + 1 for i, v in enumerate(kumulative_kunde) if v >= total_investering), None)

# Resultater
if nedbetalingstid:
    st.success(f"Nedbetalingstid for kunde: {nedbetalingstid} år.")
else:
    st.error("Investeringen nedbetales ikke innen 30 år.")

st.markdown("### Årlig BTC-utbetaling etter nedbetalingstid")
if nedbetalingstid and nedbetalingstid < år:
    st.write(f"Kunde: {round(kunde_btc[nedbetalingstid], 2)} kr")
    st.write(f"Tak-eier: {round(tak_eier_btc[nedbetalingstid], 2)} kr")
    st.write(f"Wattoshi: {round(wattoshi_btc[nedbetalingstid], 2)} kr")

st.markdown("### Akkumulert BTC-verdi etter 30 år")
st.write(f"Kunde: {int(sum(kunde_btc))} kr")
st.write(f"Tak-eier: {int(sum(tak_eier_btc))} kr")
st.write(f"Wattoshi: {int(sum(wattoshi_btc))} kr")

# Plot
fig, ax = plt.subplots()
ax.plot(range(1, år + 1), [sum(kunde_btc[:i]) for i in range(1, år + 1)], label="Kumulativ (Kunde)")
ax.plot(range(1, år + 1), [sum(tak_eier_btc[:i]) for i in range(1, år + 1)], label="Kumulativ (Tak-eier)")
ax.plot(range(1, år + 1), [sum(wattoshi_btc[:i]) for i in range(1, år + 1)], label="Kumulativ (Wattoshi)")
ax.axhline(y=total_investering, color="r", linestyle="--", label="Investering")
ax.set_xlabel("År")
ax.set_ylabel("Verdi (NOK)")
ax.set_title("Kumulativ Inntekt per rolle")
ax.legend()
st.pyplot(fig)
