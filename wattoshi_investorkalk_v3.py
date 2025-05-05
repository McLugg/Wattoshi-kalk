import streamlit as st

st.title("BTC Sparing med 20% Vekst – Eksempelberegning")

# Konstantverdier
start = 96.0
vekst = 0.20

# Beregn utbetalinger og kumulativ sum
beløp = start
akkumulert = beløp
resultater = [(0, round(beløp, 2), round(akkumulert, 2))]

for år in range(1, 10):
    beløp *= (1 + vekst)
    akkumulert += beløp
    resultater.append((år, round(beløp, 2), round(akkumulert, 2)))

# Vis resultatene
st.subheader("Utbetaling og Kumulativ BTC-verdi per År (20% vekst)")
st.write("| År | Utbetaling (kr) | Kumulativ sum (kr) |")
st.write("|----|------------------|---------------------|")
for år, b, k in resultater:
    st.write(f"| {år} | {b:.2f} | {k:.2f} |")
