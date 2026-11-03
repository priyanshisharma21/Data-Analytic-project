"""Page 2: Credit History analysis."""
import matplotlib.pyplot as plt
import streamlit as st

from utils.data import approval_rate
from utils.style import page_header, rate_bars, takeaway, note, count_by_status


def render(df):
    page_header("Credit history",
                "Applicants are marked 1 if their credit history meets the bank's guidelines, "
                "and 0 if it does not.")

    rates = approval_rate(df, "Credit_History")
    rows = []
    if 1.0 in rates.index:
        rows.append(("Good (1)", rates[1.0]))
    if 0.0 in rates.index:
        rows.append(("Poor (0)", rates[0.0]))
    st.markdown("### Share of applications approved")
    rate_bars(rows)

    if len(rows) == 2:
        ratio = rates[1.0] / max(rates[0.0], 0.1)
        takeaway(f"Applicants with a good credit history were approved about <b>{ratio:.0f} times</b> "
                 "as often. This is an association in this dataset, not proof of cause.")

    st.markdown("### Applications by credit history")
    fig, ax = plt.subplots(figsize=(6.4, 4))
    count_by_status(df, "Credit_Label", ax, order=["Good (1)", "Poor (0)"])
    ax.set_xlabel("Credit history")
    st.pyplot(fig)

    note("About 50 applications had no credit history recorded. They were filled with the most common "
         "value (1), so the approval rate for good credit may be slightly overstated.")

    with st.expander("Show as table"):
        st.dataframe(rates.round(1).rename("Approval rate (%)"))
