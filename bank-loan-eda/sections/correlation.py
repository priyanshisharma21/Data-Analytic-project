"""Page 5: Correlation."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

from utils.style import (page_header, takeaway, note, DIVERGING, SURFACE, INK2,
                         BLUE, RED, nice)


def render(df):
    page_header("Correlation",
                "How strongly do the numeric columns move together? "
                "Values run from -1 to 1, and 0 means no straight-line relationship.")

    d = df.copy()
    d["Loan_Status_Num"] = (d["Loan_Status"] == "Y").astype(int)
    cols = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term",
            "Credit_History", "TotalIncome", "Loan_Status_Num"]
    corr = d[cols].corr()

    st.markdown("### Correlation with approval")
    s = corr["Loan_Status_Num"].drop("Loan_Status_Num").sort_values()
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    bars = ax.barh([nice(i) for i in s.index], s.values,
                   color=[BLUE if v >= 0 else RED for v in s.values], height=0.6)
    ax.bar_label(bars, labels=[f"{v:.2f}" for v in s.values], fontsize=9, color=INK2, padding=3)
    ax.axvline(0, color="#cfcec6", linewidth=1)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.set_xlim(-0.2, 0.7)
    ax.set_xlabel("Correlation with being approved")
    st.pyplot(fig)

    if "Credit_History" in s.index:
        takeaway(f"Credit history is the only column with a clear link to approval ({s['Credit_History']:.2f}). "
                 "Income, loan amount and loan term are all close to zero.")

    st.markdown("### All columns against each other")
    labels = [nice(c) for c in corr.columns]
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap=DIVERGING, vmin=-1, vmax=1,
                linewidths=2, linecolor=SURFACE, xticklabels=labels, yticklabels=labels,
                cbar_kws={"shrink": 0.8}, ax=ax)
    ax.grid(False)
    plt.xticks(rotation=40, ha="right")
    st.pyplot(fig)

    note("Applicant income and loan amount move together, since larger incomes tend to ask for larger loans. "
         "Correlation shows association, not cause.")
