"""Bank Loan Approval - EDA Dashboard (Streamlit).

Run locally:  python -m streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="Bank Loan Approval", page_icon="🏦", layout="wide")

from utils.data import load_clean
from utils.style import inject_css, apply_chart_theme
from sections import overview, credit_history, income_loan, demographics, correlation

inject_css()
apply_chart_theme()

try:
    df_all = load_clean()
except FileNotFoundError:
    st.error("train.csv not found. Put it in the same folder as app.py.")
    st.stop()

PAGES = {
    "Overview": overview,
    "Credit history": credit_history,
    "Income and loan amount": income_loan,
    "Customer groups": demographics,
    "Correlation": correlation,
}

# ---- Sidebar: brand, navigation, filters ----
st.sidebar.markdown(
    '<div class="brand"><div class="name">Loan approval</div>'
    '<div class="sub">Exploratory data analysis</div></div>', unsafe_allow_html=True)

page = st.sidebar.radio("Pages", list(PAGES.keys()), label_visibility="collapsed")

st.sidebar.markdown("**Filter applications**")
areas_all = sorted(df_all["Property_Area"].unique())
edu_all = sorted(df_all["Education"].unique())
areas = st.sidebar.multiselect("Property area", areas_all, default=areas_all)
edu = st.sidebar.multiselect("Education", edu_all, default=edu_all)

df = df_all[df_all["Property_Area"].isin(areas) & df_all["Education"].isin(edu)]

if df.empty:
    st.warning("No applications match these filters. Choose at least one property area and one education level.")
    st.stop()

st.sidebar.caption(f"Showing {len(df):,} of {len(df_all):,} applications")

PAGES[page].render(df)
