"""Page 1: Overview - the headline finding, dataset summary and loan status."""
import matplotlib.pyplot as plt
import streamlit as st

from utils.data import load_raw, approval_rate
from utils.style import (hero, stats, page_header, note, count_by_status,
                         BLUE, INK2)


def render(df):
    raw = load_raw()
    overall = (df["Loan_Status"] == "Y").mean() * 100
    rates = approval_rate(df, "Credit_History")

    page_header("Bank loan approval",
                "What separates approved loan applications from rejected ones? "
                "An exploration of 614 applications.")

    if 1.0 in rates.index and 0.0 in rates.index:
        hero(f"With a good credit history, {rates[1.0]:.1f}% of applicants were approved. "
             f"Without one, {rates[0.0]:.1f}%.",
             [("Credit history good (1)", rates[1.0]), ("Credit history poor (0)", rates[0.0])],
             "No other factor in this data separates the two outcomes as clearly.")
    else:
        hero(f"{overall:.1f}% of the selected applications were approved.",
             [("Approved", overall)])

    stats([
        ("Applications", f"{len(df):,}", "in the current selection"),
        ("Approval rate", f"{overall:.1f}%", "of all applications"),
        ("Columns", f"{len(raw.columns) + 1}", "13 original plus total income"),
        ("Missing values", f"{int(raw.isnull().sum().sum())}", "in the original file, all filled"),
    ])

    left, right = st.columns(2)

    with left:
        st.markdown("### Approved and rejected")
        fig, ax = plt.subplots(figsize=(5.2, 3.6))
        count_by_status(df, "Status", ax)
        ax.set_xlabel("")
        st.pyplot(fig)

    with right:
        st.markdown("### Missing values in the original file")
        missing = raw.isnull().sum()
        missing = missing[missing > 0].sort_values()
        fig, ax = plt.subplots(figsize=(5.2, 3.6))
        bars = ax.barh([c.replace("_", " ") for c in missing.index], missing.values,
                       color=BLUE, height=0.6)
        ax.bar_label(bars, fontsize=9, color=INK2, padding=3)
        ax.grid(axis="y", visible=False)
        ax.grid(axis="x", visible=True)
        ax.set_xlabel("Rows with no value")
        ax.margins(x=0.12)
        st.pyplot(fig)

    note("Missing categories were filled with the most common value, and loan amount with the median, "
         "because loan amounts are skewed by a few very large loans.")

    with st.expander("Show the first 20 rows"):
        st.dataframe(df.drop(columns=["Status", "Credit_Label"]).head(20), use_container_width=True)
