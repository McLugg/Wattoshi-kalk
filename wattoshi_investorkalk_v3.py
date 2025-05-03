
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wattoshi Panelinvestor Kalkulator", layout="wide")

st.title("Wattoshi Panelinvestor Kalkulator – Fordeling Kunde / Tak-eier / Wattoshi")

# Input parameters
st.sidebar.header("Inputparametere")
num_panels = st.sidebar.slider("Antall paneler", 1, 100, 1)
panel_capacity = st.sidebar.selectbox("Panelkapasitet (Watt)", [400, 415, 430])
panel_price = st.sidebar.number_input("Pris per panel (NOK)", value=2000)
export_price = st.sidebar.number_input("Eksportpris (NOK/kWh)", value=2.0)
btc_growth = st.sidebar.slider("Årlig BTC verdiøkning (%)", 0, 50, 20)

st.sidebar.subheader("Fordeling av produksjonsverdi (%)")
share_customer = st.sidebar.slider("Kunde", 0, 100, 50)
share_roofowner = st.sidebar.slider("Tak-eier", 0, 50, 30)
share_wattoshi = 100 - (share_customer + share_roofowner)

if share_customer + share_roofowner > 100:
    st.error("Summen av fordeling for Kunde og Tak-eier kan ikke overstige 100 %.")
    st.stop()

# Beregninger
capacity_kw = panel_capacity / 1000
annual_production_kwh = num_panels * capacity_kw * 1000  # 1000 kWh per kW per år

def future_value_annuity(payment, rate, years):
    return payment * (((1 + rate)**years - 1) / rate)

# Årlige utbetalinger
btc_value_customer = annual_production_kwh * export_price * (share_customer / 100)
btc_value_roofowner = annual_production_kwh * export_price * (share_roofowner / 100)
btc_value_wattoshi = annual_production_kwh * export_price * (share_wattoshi / 100)

# Nedbetalingstid for kunde
investment = panel_price * num_panels
if btc_value_customer == 0:
    payback_years = 30
else:
    total = 0
    year = 0
    while total < investment and year < 30:
        total += btc_value_customer * ((1 + btc_growth / 100) ** year)
        year += 1
    payback_years = year

st.success(f"Nedbetalingstid for kunde: {payback_years} år.")

# Årlig BTC etter nedbetalingstid
st.subheader("Årlig BTC-utbetaling etter nedbetalingstid")
st.write(f"- Kunde: {btc_value_customer:.2f} kr")
st.write(f"- Tak-eier: {btc_value_roofowner:.2f} kr")
st.write(f"- Wattoshi: {btc_value_wattoshi:.2f} kr")

# Akkumulert BTC-verdi etter 30 år
btc_future_customer = future_value_annuity(btc_value_customer, btc_growth / 100, 30)
btc_future_roofowner = future_value_annuity(btc_value_roofowner, btc_growth / 100, 30)
btc_future_wattoshi = future_value_annuity(btc_value_wattoshi, btc_growth / 100, 30)

st.subheader("Akkumulert BTC-verdi etter 30 år")
st.write(f"- Kunde: {btc_future_customer:.0f} kr")
st.write(f"- Tak-eier: {btc_future_roofowner:.0f} kr")
st.write(f"- Wattoshi: {btc_future_wattoshi:.0f} kr")

# Visualisering
years = list(range(1, 31))
btc_c = [btc_value_customer * ((1 + btc_growth / 100) ** i) for i in range(30)]
btc_r = [btc_value_roofowner * ((1 + btc_growth / 100) ** i) for i in range(30)]
btc_w = [btc_value_wattoshi * ((1 + btc_growth / 100) ** i) for i in range(30)]

cumulative_c = [sum(btc_c[:i+1]) for i in range(30)]
cumulative_r = [sum(btc_r[:i+1]) for i in range(30)]
cumulative_w = [sum(btc_w[:i+1]) for i in range(30)]

plt.figure(figsize=(10, 5))
plt.plot(years, cumulative_c, label="Kumulativ (Kunde)")
plt.plot(years, cumulative_r, label="Kumulativ (Tak-eier)")
plt.plot(years, cumulative_w, label="Kumulativ (Wattoshi)")
plt.axhline(y=investment, color='red', linestyle='--', label="Investering")
plt.xlabel("År")
plt.ylabel("Verdi (NOK)")
plt.title("Kumulativ Inntekt per rolle")
plt.legend()
plt.tight_layout()

st.pyplot(plt)
