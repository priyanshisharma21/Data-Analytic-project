"""Page 4: Customer categories (Property Area, Education, Married, ...)."""
import matplotlib.pyplot as plt
import streamlit as st

from utils.data import approval_rate
from utils.style import page_header, rate_bars, takeaway, count_by_status, nice

CATEGORIES = ["Property_Area", "Education", "Married", "Self_Employed",
              "Gender", "Dependents"]


def render(df):
    page_header("Customer groups",
                "Pick a way to group applicants and compare how often each group was approved.")

    col = st.selectbox("Group applicants by", CATEGORIES, format_func=nice)

    rates = approval_rate(df, col).sort_values(ascending=False)
    st.markdown(f"### Share approved, by {nice(col).lower()}")
    rate_bars([(str(k), v) for k, v in rates.items()])

    if len(rates) > 1:
        gap = rates.iloc[0] - rates.iloc[-1]
        takeaway(f"<b>{rates.index[0]}</b> has the highest approval rate and <b>{rates.index[-1]}</b> the lowest, "
                 f"a gap of {gap:.1f} percentage points. For comparison, good against poor credit history "
                 "is a gap of more than 70 points.")

    if col == "Gender":
        takeaway("A difference between genders in this data is not a reason to use gender in lending "
                 "decisions. It raises fairness and legal concerns.")

    st.markdown(f"### Applications, by {nice(col).lower()}")
    fig, ax = plt.subplots(figsize=(6.4, 4))
    count_by_status(df, col, ax, order=sorted(df[col].unique().tolist(), key=str))
    st.pyplot(fig)

    with st.expander("Show as table"):
        st.dataframe(rates.round(1).rename("Approval rate (%)"))
