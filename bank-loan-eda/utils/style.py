"""Look and feel of the dashboard: CSS, chart theme and small HTML helpers.

Colors (validated for colour-blind readers):
    Approved = blue, Rejected = orange.
"""
import matplotlib as mpl
import seaborn as sns
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap

# ---------- colors ----------
SURFACE = "#fcfcfb"
PAGE = "#f9f9f7"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#7a7973"
GRID = "#ecebe6"
NAVY = "#0d366b"
BLUE = "#2a78d6"      # Approved / brand
ORANGE = "#eb6834"    # Rejected
RED = "#e34948"

STATUS_COLORS = {"Approved": BLUE, "Rejected": ORANGE}
STATUS_ORDER = ["Approved", "Rejected"]
DIVERGING = LinearSegmentedColormap.from_list("div", [RED, "#f0efec", BLUE])

NICE = {
    "ApplicantIncome": "Applicant income",
    "CoapplicantIncome": "Co-applicant income",
    "TotalIncome": "Total income",
    "LoanAmount": "Loan amount",
    "Loan_Amount_Term": "Loan term",
    "Credit_History": "Credit history",
    "Loan_Status_Num": "Approved (1) / Rejected (0)",
    "Property_Area": "Property area",
    "Self_Employed": "Self employed",
}


def nice(name: str) -> str:
    return NICE.get(name, name.replace("_", " "))


# ---------- CSS ----------
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:wght@400;500;600&display=swap');

.stApp { background: #f9f9f7; font-family: 'Public Sans', system-ui, sans-serif; color: #0b0b0b; }
.block-container { max-width: 1080px; padding: 2.4rem 1.5rem 4rem; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

h1, h2, h3, h4 { font-family: 'Bricolage Grotesque', 'Public Sans', sans-serif; letter-spacing: -0.01em; color: #0b0b0b; }
h3 { font-size: 1.15rem; font-weight: 600; margin-top: 2.2rem; }

[data-testid="stSidebar"] { background: #f1f1ed; border-right: 1px solid #e2e1db; }

.brand { padding: .2rem 0 1rem; margin-bottom: .6rem; border-bottom: 1px solid #d9d8d1; }
.brand .name { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.25rem; color: #0d366b; line-height: 1.2; }
.brand .sub { color: #52514e; font-size: .85rem; margin-top: .15rem; }

.pageheader { margin-bottom: 1.6rem; }
.pageheader h1 { font-size: clamp(1.8rem, 3.4vw, 2.5rem); font-weight: 700; margin: 0 0 .5rem; padding: 0; line-height: 1.1; }
.pageheader .lede { color: #52514e; font-size: 1.05rem; line-height: 1.55; max-width: 62ch; margin: 0; }

.hero { border-top: 3px solid #0d366b; padding: 1.4rem 0 1.2rem; margin-bottom: 1.6rem; }
.hero .claim { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: clamp(1.6rem, 3.4vw, 2.6rem);
  line-height: 1.12; letter-spacing: -0.02em; max-width: 26ch; margin: 0 0 1.4rem; color: #0b0b0b; }
.hero .src { color: #7a7973; font-size: .85rem; margin: .9rem 0 0; }

.rb { max-width: 760px; }
.rb-row { display: grid; grid-template-columns: minmax(130px, 210px) 1fr 64px; align-items: center; gap: 1rem; margin: .6rem 0; }
.rb-label { color: #0b0b0b; font-size: .95rem; }
.rb-track { height: 12px; background: #ecebe6; border-radius: 2px; }
.rb-fill { height: 100%; background: #2a78d6; border-radius: 2px; }
.rb-val { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.15rem; text-align: right; font-variant-numeric: tabular-nums; }

.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1.6rem; margin: 0 0 1rem; }
.stat { border-top: 1px solid #cfcec6; padding-top: .7rem; }
.stat .v { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 2rem; line-height: 1.1; font-variant-numeric: tabular-nums; }
.stat .l { color: #0b0b0b; font-size: .92rem; margin-top: .2rem; }
.stat .n { color: #7a7973; font-size: .8rem; margin-top: .1rem; }

.takeaway { border-left: 3px solid #2a78d6; background: #f1f4f9; padding: .75rem 1rem; margin: 1rem 0 .5rem; color: #1d1f23; line-height: 1.5; max-width: 70ch; }
.note { color: #7a7973; font-size: .85rem; line-height: 1.45; max-width: 70ch; }

@media (max-width: 640px) {
  .rb-row { grid-template-columns: 1fr 56px; }
  .rb-label { grid-column: 1 / -1; }
}
"""


def inject_css():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def apply_chart_theme():
    """Quiet charts: no box, light horizontal grid, left-aligned titles."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": "#d9d8d1", "axes.labelcolor": INK2,
        "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 1,
        "axes.axisbelow": True, "font.size": 10, "axes.labelsize": 10,
        "legend.frameon": False, "figure.dpi": 110,
    })


# ---------- HTML helpers ----------
def page_header(title: str, lede: str = ""):
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    st.markdown(f'<div class="pageheader"><h1>{title}</h1>{lede_html}</div>', unsafe_allow_html=True)


def _rate_bars_html(rows):
    html = '<div class="rb">'
    for label, pct in rows:
        pct = max(0.0, min(100.0, float(pct)))
        html += (f'<div class="rb-row"><div class="rb-label">{label}</div>'
                 f'<div class="rb-track"><div class="rb-fill" style="width:{pct:.1f}%"></div></div>'
                 f'<div class="rb-val">{pct:.1f}%</div></div>')
    return html + "</div>"


def rate_bars(rows):
    """rows = [(label, approval_rate_percent), ...]"""
    st.markdown(_rate_bars_html(rows), unsafe_allow_html=True)


def hero(claim: str, rows, source: str = ""):
    src = f'<p class="src">{source}</p>' if source else ""
    st.markdown(f'<section class="hero"><p class="claim">{claim}</p>{_rate_bars_html(rows)}{src}</section>',
                unsafe_allow_html=True)


def stats(items):
    """items = [(label, value, note), ...]"""
    html = '<div class="stats">'
    for label, value, note in items:
        html += (f'<div class="stat"><div class="v">{value}</div><div class="l">{label}</div>'
                 f'<div class="n">{note}</div></div>')
    st.markdown(html + "</div>", unsafe_allow_html=True)


def takeaway(text: str):
    st.markdown(f'<div class="takeaway">{text}</div>', unsafe_allow_html=True)


def note(text: str):
    st.markdown(f'<p class="note">{text}</p>', unsafe_allow_html=True)


# ---------- chart helpers ----------
def count_by_status(df, x, ax, order=None):
    """Bars of applications per category, split Approved / Rejected, with counts on the bars."""
    sns.countplot(x=x, hue="Status", hue_order=STATUS_ORDER, palette=STATUS_COLORS,
                  data=df, order=order, ax=ax, edgecolor=SURFACE, linewidth=2, saturation=1)
    for c in ax.containers:
        ax.bar_label(c, fontsize=9, color=INK2, padding=2)
    ax.set_ylabel("Applications")
    ax.set_xlabel(nice(x))
    if x != "Status":
        ax.legend(title=None, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2)
    ax.margins(y=0.12)


def status_box(df, y, ax, ylim=None):
    sns.boxplot(x="Status", y=y, data=df, order=STATUS_ORDER, hue="Status", hue_order=STATUS_ORDER,
                palette=STATUS_COLORS, legend=False, width=0.5, linewidth=1.2, fliersize=3, saturation=1, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel(nice(y))
    if ylim:
        ax.set_ylim(*ylim)
