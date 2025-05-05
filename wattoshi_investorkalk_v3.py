
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("BTC-utbetaling med vekst – Nedbetalingstid og akkumulert verdi")

# Inputparametere
initial_payout = st.number_input("Årlig startutbetaling (NOK)", value=96)
growth_rate_percent = st.slider("Årlig vekst i verdi (%)", min_value=0, max_value=100, value=20)
investment = st.number_input("Investeringsbeløp (NOK)", value=770)
years = 30

# Beregning
growth_rate = growth_rate_percent / 100
year_list = []
annual_list = []
accumulated_list = []
flagged = False
accumulated = 0

for year in range(years + 1):
    annual = initial_payout * ((1 + growth_rate) ** year)
    accumulated += annual
    year_list.append(year)
    annual_list.append(round(annual, 2))
    accumulated_list.append(round(accumulated, 2))

# Finn første år med nedbetaling
nedbetalt_flag = []
for val in accumulated_list:
    if not flagged and val >= investment:
        nedbetalt_flag.append("✅")
        flagged = True
    else:
        nedbetalt_flag.append("")

# DataFrame for visning
df = pd.DataFrame({
    "År": year_list,
    "Årlig utbetaling (NOK)": annual_list,
    "Akkumulert verdi (NOK)": accumulated_list,
    "Nedbetalt": nedbetalt_flag
})

# Tabellvisning
st.subheader("Årlig oversikt")
st.dataframe(df, use_container_width=True)

# Plot
st.subheader("Graf – Akkumulert verdi over tid")
fig, ax = plt.subplots()
ax.plot(year_list, accumulated_list, marker='o')
ax.axhline(y=investment, color='r', linestyle='--', label='Investeringsbeløp')
ax.set_xlabel("År")
ax.set_ylabel("Akkumulert verdi (NOK)")
ax.set_title("Akkumulert verdi over 30 år")
ax.legend()
st.pyplot(fig)
