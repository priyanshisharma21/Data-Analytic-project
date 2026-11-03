"""Data loading and cleaning. Used by every page of the dashboard."""
import pandas as pd
import streamlit as st

DATA_PATH = "train.csv"


@st.cache_data
def load_raw(path: str = DATA_PATH) -> pd.DataFrame:
    """Read the original CSV without any changes."""
    return pd.read_csv(path)


@st.cache_data
def load_clean(path: str = DATA_PATH) -> pd.DataFrame:
    """Same cleaning steps as the notebook, plus two readable label columns."""
    df = load_raw(path).copy()

    # Categorical columns -> fill with mode
    for col in ["Gender", "Married", "Dependents", "Self_Employed",
                "Credit_History", "Loan_Amount_Term"]:
        df[col] = df[col].fillna(df[col].mode()[0])

    # LoanAmount -> fill with median (outliers present)
    df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())

    df = df.drop_duplicates()
    df["TotalIncome"] = df["ApplicantIncome"] + df["CoapplicantIncome"]

    # Readable labels used by charts
    df["Status"] = df["Loan_Status"].map({"Y": "Approved", "N": "Rejected"})
    df["Credit_Label"] = df["Credit_History"].map({1.0: "Good (1)", 0.0: "Poor (0)"})
    return df


def approval_rate(df: pd.DataFrame, by: str) -> pd.Series:
    """Approval rate (%) for each category of column `by`."""
    return df.groupby(by)["Loan_Status"].apply(lambda s: (s == "Y").mean() * 100)
