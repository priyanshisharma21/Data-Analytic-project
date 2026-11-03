# Bank Loan Approval - Data Exploration (EDA)

Exploratory Data Analysis of bank loan applications to understand which factors are
associated with loan approval. Built with Python, Pandas, NumPy, Matplotlib, Seaborn
and an interactive **Streamlit** dashboard.

> EDA shows associations, not causes. Lending decisions must also consider fairness,
> privacy and banking regulations.

## Key findings (614 applications)
- 68.7% of applications were approved.
- Credit history is the strongest factor: 79.0% approval with credit history = 1 vs 7.9% with 0.
- Semiurban (76.8%) > Urban (65.8%) > Rural (61.5%) approval rate.
- Applicant income and loan amount alone show almost no relationship with approval.

## Project structure
```
bank-loan-eda/
├── app.py                      # Dashboard entry point (navigation + filters)
├── utils/data.py               # Data loading and cleaning
├── utils/style.py              # Colors, CSS and chart styling
├── .streamlit/config.toml      # Streamlit theme
├── sections/
│   ├── overview.py             # Dataset summary, loan status chart
│   ├── credit_history.py       # Credit history analysis
│   ├── income_loan.py          # Income and loan amount analysis
│   ├── demographics.py         # Property area, education, married, ...
│   └── correlation.py          # Correlation heatmap
├── Bank_Loan_Approval_EDA.ipynb  # Full analysis notebook
├── train.csv                   # Dataset
└── requirements.txt
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Team contributions
| File | Owner |
|---|---|
| `utils/data.py`, `utils/style.py`, `app.py`, `README.md`, notebook | _name_ |
| `sections/overview.py` | _name_ |
| `sections/credit_history.py` | _name_ |
| `sections/income_loan.py` | _name_ |
| `sections/demographics.py` | _name_ |
| `sections/correlation.py` | _name_ |

## Dataset
Loan Prediction Problem dataset (Kaggle / Analytics Vidhya), `train.csv`.
