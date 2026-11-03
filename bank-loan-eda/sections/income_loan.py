"""Page 3: Income and Loan Amount analysis."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

from utils.style import page_header, takeaway, note, status_box, BLUE, NAVY, nice


def render(df):
    page_header("Income and loan amount",
                "Do approved applicants earn more, or ask for smaller loans? In this data, barely.")

    st.markdown("### How incomes are spread")
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
    for a, col, data, title in [
        (ax[0], "ApplicantIncome", df["ApplicantIncome"], "Applicant income"),
        (ax[1], "CoapplicantIncome", df["CoapplicantIncome"], "Co-applicant income"),
        (ax[2], "TotalIncome", np.log1p(df["TotalIncome"]), "Total income (log scale)"),
    ]:
        sns.histplot(data, kde=True, color=BLUE, edgecolor="#fcfcfb", linewidth=1,
                     line_kws={"color": NAVY, "linewidth": 1.6}, ax=a)
        a.set_title(title, loc="left", fontsize=11)
        a.set_xlabel("")
        a.set_ylabel("Applications" if a is ax[0] else "")
    plt.tight_layout()
    st.pyplot(fig)
    note("Most applicants earn a modest income and a few earn far more, so the long tail is stretched. "
         "Many co-applicants have an income of zero, meaning there was no co-applicant.")

    st.markdown("### Income by outcome")
    cap = st.slider("Highest applicant income to show", 5000, 80000, 20000, step=1000)
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(4.6, 3.6))
        status_box(df, "ApplicantIncome", ax, ylim=(0, cap))
        ax.set_title("Applicant income", loc="left", fontsize=11)
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(4.6, 3.6))
        status_box(df, "LoanAmount", ax)
        ax.set_title("Loan amount", loc="left", fontsize=11)
        st.pyplot(fig)

    med = df.groupby("Status")[["ApplicantIncome", "CoapplicantIncome", "TotalIncome", "LoanAmount"]].median()
    if {"Approved", "Rejected"} <= set(med.index):
        takeaway("Typical applicant income is almost the same for both outcomes "
                 f"(median {med.loc['Approved', 'ApplicantIncome']:,.0f} approved, "
                 f"{med.loc['Rejected', 'ApplicantIncome']:,.0f} rejected), and so is loan amount "
                 f"({med.loc['Approved', 'LoanAmount']:,.0f} against {med.loc['Rejected', 'LoanAmount']:,.0f}). "
                 f"Co-applicant income differs more ({med.loc['Approved', 'CoapplicantIncome']:,.0f} against "
                 f"{med.loc['Rejected', 'CoapplicantIncome']:,.0f}).")

    with st.expander("Show medians as table"):
        st.dataframe(med.round(0).rename(columns=nice))
