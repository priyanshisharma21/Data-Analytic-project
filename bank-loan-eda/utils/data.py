"""Data loading and cleaning. Used by every page of the dashboard."""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # folder that holds app.py


def find_data_path() -> str:
    """Find the training CSV whatever its case or folder (Linux servers are case sensitive)."""
    def is_train_csv(f: Path) -> bool:
        return f.is_file() and f.suffix.lower() == ".csv" and "train" in f.name.lower()

    # 1) the usual places
    for folder in (ROOT, Path.cwd(), ROOT.parent):
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                if is_train_csv(f):
                    return str(f)
    # 2) any subfolder (e.g. repo/bank-loan-eda/train.csv when app.py sits at the repo root)
    for f in sorted(ROOT.rglob("*.csv")):
        if is_train_csv(f) and not any(part.startswith(".") for part in f.relative_to(ROOT).parts):
            return str(f)
    raise FileNotFoundError("train.csv not found")


@st.cache_data
def load_raw(path: str = "") -> pd.DataFrame:
    """Read the original CSV without any changes."""
    return pd.read_csv(path or find_data_path())


@st.cache_data
def load_clean(path: str = "") -> pd.DataFrame:
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
