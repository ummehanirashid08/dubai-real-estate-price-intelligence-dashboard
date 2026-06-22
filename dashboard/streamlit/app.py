import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Dubai Real Estate Price Intelligence Dashboard",
    page_icon="🏙️",
    layout="wide"
)

# --------------------------------------------------
# Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

TRANSACTIONS_FILE = PROCESSED_DATA_DIR / "powerbi_dashboard_transactions.csv"
ML_SUMMARY_FILE = PROCESSED_DATA_DIR / "ml_final_model_summary.csv"

# Optional latest/live files
LIVE_TRANSACTIONS_FILE = RAW_DATA_DIR / "Transactions_live.csv"
LIVE_TRANSACTIONS_URL = os.getenv("DLD_TRANSACTIONS_CSV_URL", "").strip()

# --------------------------------------------------
# Premium CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #07111F 0%, #0B1728 45%, #111827 100%);
        color: #F8FAFC;
    }

    header[data-testid="stHeader"] {
        background: #07111F !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stDeployButton {
        visibility: hidden;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        width: 330px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB !important;
    }

    section[data-testid="stSidebar"] h2 {
        font-size: 24px !important;
        line-height: 1.2 !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #94A3B8 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stDateInput"] input {
        background: linear-gradient(135deg, #111827, #1E293B) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        border-radius: 14px !important;
        min-height: 46px !important;
        font-weight: 700 !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25) !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: linear-gradient(135deg, #111827, #1E293B) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        border-radius: 16px !important;
        min-height: 86px !important;
        max-height: 165px !important;
        overflow-y: auto !important;
        padding: 8px !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25) !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #F8FAFC !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="tag"] {
        background: linear-gradient(135deg, #F59E0B, #D97706) !important;
        color: #111827 !important;
        border: 1px solid rgba(252, 211, 77, 0.45) !important;
        border-radius: 999px !important;
        font-weight: 800 !important;
        padding: 6px 10px !important;
        margin: 4px !important;
        box-shadow: 0 8px 18px rgba(245, 158, 11, 0.22) !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="tag"] span,
    section[data-testid="stSidebar"] div[data-baseweb="tag"] svg {
        color: #111827 !important;
        fill: #111827 !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        color: #FCD34D !important;
        fill: #FCD34D !important;
    }

    div[data-baseweb="popover"] {
        background: #0F172A !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: #0F172A !important;
        color: #F8FAFC !important;
    }

    div[data-baseweb="popover"] li:hover {
        background: rgba(245, 158, 11, 0.18) !important;
        color: #FCD34D !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 26px 0 !important;
    }

    section[data-testid="stSidebar"] .stAlert {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(15, 23, 42, 0.72)) !important;
        border: 1px solid rgba(245, 158, 11, 0.32) !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }

    section[data-testid="stSidebar"] .stAlert p {
        font-size: 14px !important;
        line-height: 1.55 !important;
        color: #E5E7EB !important;
    }

    h1, h2, h3 {
        color: #F8FAFC;
        letter-spacing: -0.03em;
    }

    .hero-card {
        background: radial-gradient(circle at top left, rgba(245, 158, 11, 0.24), transparent 30%),
                    linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.92));
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 28px;
        padding: 34px 36px;
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        line-height: 1.08;
        margin-bottom: 12px;
        color: #FFFFFF;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #CBD5E1;
        max-width: 1120px;
        line-height: 1.7;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 22px;
    }

    .pill {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.32);
        color: #FCD34D;
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(17, 24, 39, 0.96));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        padding: 22px 24px;
        box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22);
        min-height: 150px;
        margin-bottom: 18px;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.35;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 8px;
        word-break: break-word;
    }

    .metric-help {
        color: #A7F3D0;
        font-size: 12px;
        font-weight: 600;
    }

    .insight-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.16), rgba(59, 130, 246, 0.10));
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 20px;
        padding: 18px 20px;
        color: #E5E7EB;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    .insight-title {
        font-size: 15px;
        font-weight: 800;
        color: #FCD34D;
        margin-bottom: 7px;
    }

    .insight-text {
        font-size: 14px;
        line-height: 1.7;
        color: #CBD5E1;
    }

    .summary-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.11), rgba(245, 158, 11, 0.10));
        border: 1px solid rgba(255,255,255,0.10);
        border-left: 4px solid #F59E0B;
        border-radius: 22px;
        padding: 22px 24px;
        margin-top: 24px;
        margin-bottom: 18px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.20);
    }

    .summary-title {
        color: #FCD34D;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .summary-text {
        color: #CBD5E1;
        font-size: 15px;
        line-height: 1.75;
    }

    .live-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.14), rgba(245, 158, 11, 0.10));
        border: 1px solid rgba(16, 185, 129, 0.28);
        border-radius: 20px;
        padding: 18px 20px;
        margin: 12px 0 20px;
    }

    .live-title {
        color: #A7F3D0;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .live-text {
        color: #CBD5E1;
        font-size: 14px;
        line-height: 1.65;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 8px;
        border-radius: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 18px;
        background: transparent;
        border-radius: 12px;
        color: #CBD5E1;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: #111827 !important;
    }

    .js-plotly-plot {
        border-radius: 22px !important;
        overflow: hidden !important;
    }

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.70);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        overflow: hidden;
    }

    .dark-table-wrapper {
        width: 100%;
        overflow-x: auto;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 0;
        margin-top: 14px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
    }

    .dark-table {
        width: 100%;
        border-collapse: collapse;
        color: #E5E7EB;
        font-size: 14px;
    }

    .dark-table thead tr {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(30, 41, 59, 0.95));
    }

    .dark-table th {
        padding: 14px 16px;
        text-align: left;
        color: #FCD34D;
        font-weight: 800;
        border-bottom: 1px solid rgba(255, 255, 255, 0.10);
        white-space: nowrap;
    }

    .dark-table td {
        padding: 13px 16px;
        color: #CBD5E1;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        white-space: nowrap;
    }

    .dark-table tbody tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.025);
    }

    .dark-table tbody tr:hover {
        background: rgba(245, 158, 11, 0.09);
    }

    .footer {
        color: #94A3B8;
        font-size: 13px;
        text-align: center;
        padding: 30px 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def clean_column_name(col):
    return (
        str(col)
        .strip()
        .lower()
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
    )


def format_aed(value):
    if pd.isna(value):
        return "AED 0"
    if value >= 1_000_000_000_000:
        return f"AED {value / 1_000_000_000_000:,.2f}T"
    if value >= 1_000_000_000:
        return f"AED {value / 1_000_000_000:,.2f}B"
    if value >= 1_000_000:
        return f"AED {value / 1_000_000:,.2f}M"
    return f"AED {value:,.0f}"


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"


def metric_card(label, value, help_text):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight_box(title, text):
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_summary(title, text):
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-title">{title}</div>
            <div class="summary-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def live_status_card(title, text):
    st.markdown(
        f"""
        <div class="live-card">
            <div class="live-title">{title}</div>
            <div class="live-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_plotly(fig, height=430):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.35)",
        font=dict(color="#E5E7EB", family="Inter"),
        title=dict(font=dict(size=18, color="#FFFFFF"), x=0.02),
        margin=dict(l=20, r=20, t=58, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1"))
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.12)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.12)")
    return fig


def format_summary_table(df):
    formatted = df.copy()

    money_cols = [
        "total_sales_value",
        "average_price",
        "median_price",
        "average_price_per_sqm",
        "forecast_average_price",
        "actual_worth",
        "price_per_sqm",
        "MAE",
        "RMSE"
    ]

    for col in money_cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].apply(lambda x: format_aed(x) if pd.notna(x) else "AED 0")

    if "total_transactions" in formatted.columns:
        formatted["total_transactions"] = formatted["total_transactions"].apply(format_number)

    if "R2" in formatted.columns:
        formatted["R2"] = formatted["R2"].apply(lambda x: round(x, 3))

    return formatted


def render_dark_table(df, max_rows=12):
    display_df = df.head(max_rows).copy()

    table_html = """
    <div class="dark-table-wrapper">
        <table class="dark-table">
            <thead>
                <tr>
    """

    for col in display_df.columns:
        table_html += f"<th>{col}</th>"

    table_html += """
                </tr>
            </thead>
            <tbody>
    """

    for _, row in display_df.iterrows():
        table_html += "<tr>"
        for value in row:
            table_html += f"<td>{value}</td>"
        table_html += "</tr>"

    table_html += """
            </tbody>
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)


def standardize_live_transactions(live_df):
    if live_df.empty:
        return live_df

    live_df = live_df.copy()
    live_df.columns = [clean_column_name(col) for col in live_df.columns]

    rename_map = {
        "transaction_number": "transaction_id",
        "transaction_id": "transaction_id",
        "transaction_date": "transaction_date",
        "instance_date": "transaction_date",
        "registration_type": "reg_type_en",
        "registration_type_en": "reg_type_en",
        "reg_type_en": "reg_type_en",
        "area": "area_name_en",
        "area_name_en": "area_name_en",
        "property_type": "property_type_en",
        "property_type_en": "property_type_en",
        "property_sub_type": "property_sub_type_en",
        "property_sub_type_en": "property_sub_type_en",
        "usage": "property_usage_en",
        "property_usage_en": "property_usage_en",
        "amount": "actual_worth",
        "actual_worth": "actual_worth",
        "transaction_size_sqm": "procedure_area",
        "procedure_area": "procedure_area",
        "property_size_sqm": "property_size_sqm",
        "rooms": "rooms_en",
        "rooms_en": "rooms_en",
        "parking": "has_parking",
        "has_parking": "has_parking",
        "nearest_metro": "nearest_metro_en",
        "nearest_metro_en": "nearest_metro_en",
        "nearest_mall": "nearest_mall_en",
        "nearest_mall_en": "nearest_mall_en",
        "nearest_landmark": "nearest_landmark_en",
        "nearest_landmark_en": "nearest_landmark_en",
    }

    live_df = live_df.rename(columns={k: v for k, v in rename_map.items() if k in live_df.columns})

    required_cols = [
        "transaction_id",
        "transaction_date",
        "area_name_en",
        "property_type_en",
        "property_sub_type_en",
        "property_usage_en",
        "reg_type_en",
        "rooms_en",
        "has_parking",
        "procedure_area",
        "actual_worth",
        "nearest_metro_en",
        "nearest_mall_en",
        "nearest_landmark_en",
    ]

    for col in required_cols:
        if col not in live_df.columns:
            live_df[col] = np.nan

    live_df["transaction_date"] = pd.to_datetime(live_df["transaction_date"], errors="coerce", dayfirst=True)
    live_df["actual_worth"] = pd.to_numeric(live_df["actual_worth"], errors="coerce")
    live_df["procedure_area"] = pd.to_numeric(live_df["procedure_area"], errors="coerce")

    live_df["price_per_sqm"] = np.where(
        live_df["procedure_area"] > 0,
        live_df["actual_worth"] / live_df["procedure_area"],
        np.nan
    )

    live_df["area_size_sqm"] = live_df["procedure_area"]
    live_df["transaction_year"] = live_df["transaction_date"].dt.year
    live_df["transaction_month"] = live_df["transaction_date"].dt.month
    live_df["transaction_quarter"] = "Q" + live_df["transaction_date"].dt.quarter.astype("Int64").astype(str)
    live_df["transaction_year_month"] = live_df["transaction_date"].dt.to_period("M").astype(str)
    live_df["year_month_sort"] = live_df["transaction_date"].dt.strftime("%Y-%m")
    live_df["month_name"] = live_df["transaction_date"].dt.month_name()

    final_cols = [
        "transaction_id",
        "instance_date",
        "transaction_date",
        "transaction_year",
        "transaction_month",
        "transaction_quarter",
        "transaction_year_month",
        "year_month_sort",
        "month_name",
        "area_name_en",
        "property_type_en",
        "property_sub_type_en",
        "property_usage_en",
        "reg_type_en",
        "rooms_en",
        "has_parking",
        "procedure_area",
        "area_size_sqm",
        "actual_worth",
        "price_per_sqm",
        "nearest_metro_en",
        "nearest_mall_en",
        "nearest_landmark_en",
    ]

    live_df["instance_date"] = live_df["transaction_date"]

    return live_df[[col for col in final_cols if col in live_df.columns]].dropna(
        subset=["transaction_date", "actual_worth", "area_name_en", "property_type_en"]
    )


@st.cache_data(ttl=3600)
def load_live_transactions():
    try:
        if LIVE_TRANSACTIONS_URL:
            live = pd.read_csv(LIVE_TRANSACTIONS_URL, low_memory=False)
            live = standardize_live_transactions(live)
            return live, f"Live URL loaded: {LIVE_TRANSACTIONS_URL}"

        if LIVE_TRANSACTIONS_FILE.exists():
            live = pd.read_csv(LIVE_TRANSACTIONS_FILE, low_memory=False)
            live = standardize_live_transactions(live)
            return live, f"Live CSV loaded: {LIVE_TRANSACTIONS_FILE}"

        return pd.DataFrame(), "No live CSV found. Add latest DLD file as data/raw/Transactions_live.csv."
    except Exception as error:
        return pd.DataFrame(), f"Live data could not be loaded: {error}"


@st.cache_data(ttl=3600)
def load_data():
    transactions = pd.read_csv(TRANSACTIONS_FILE, low_memory=False)

    if "transaction_date" in transactions.columns:
        transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"], errors="coerce")
    else:
        transactions["transaction_date"] = pd.to_datetime(transactions["instance_date"], errors="coerce")

    if "price_per_sqm" not in transactions.columns:
        transactions["price_per_sqm"] = transactions["meter_sale_price"]

    live_transactions, live_message = load_live_transactions()

    if not live_transactions.empty:
        transactions["data_source"] = "Historical"
        live_transactions["data_source"] = "Latest DLD CSV"

        combined = pd.concat([transactions, live_transactions], ignore_index=True, sort=False)

        if "transaction_id" in combined.columns:
            combined = combined.drop_duplicates(subset=["transaction_id"], keep="last")
        else:
            combined = combined.drop_duplicates()

        transactions = combined
    else:
        transactions["data_source"] = "Historical"

    transactions = transactions.dropna(subset=["transaction_date", "actual_worth", "area_name_en", "property_type_en"])

    ml_summary = pd.read_csv(ML_SUMMARY_FILE) if ML_SUMMARY_FILE.exists() else pd.DataFrame()

    return transactions, ml_summary, live_message


def build_live_forecast(base_df, months=12):
    forecast_input = (
        base_df
        .dropna(subset=["transaction_date", "actual_worth"])
        .groupby("year_month_sort")
        .agg(average_price=("actual_worth", "mean"))
        .reset_index()
        .sort_values("year_month_sort")
    )

    forecast_input["date"] = pd.to_datetime(forecast_input["year_month_sort"] + "-01", errors="coerce")
    forecast_input = forecast_input.dropna(subset=["date", "average_price"])

    if len(forecast_input) < 12:
        return pd.DataFrame(), forecast_input

    forecast_input["time_index"] = np.arange(len(forecast_input))

    x = forecast_input["time_index"].values
    y = forecast_input["average_price"].values

    slope, intercept = np.polyfit(x, y, 1)

    last_date = forecast_input["date"].max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=months, freq="MS")
    future_index = np.arange(len(forecast_input), len(forecast_input) + months)

    forecast_df = pd.DataFrame({
        "date": future_dates,
        "time_index": future_index,
        "forecast_average_price": intercept + slope * future_index
    })

    return forecast_df, forecast_input


# --------------------------------------------------
# Load data
# --------------------------------------------------
try:
    df, ml_summary, live_message = load_data()
except FileNotFoundError as e:
    st.error("Required data files are missing. Please complete the data preparation step first.")
    st.code(str(e))
    st.stop()

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.caption("Use these filters to explore specific market segments.")

latest_data_date = df["transaction_date"].max()
oldest_data_date = df["transaction_date"].min()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🟢 Data Status")
st.sidebar.caption(f"Latest transaction date: **{latest_data_date.date()}**")
st.sidebar.caption(live_message)

min_date = oldest_data_date
max_date = latest_data_date

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

property_options = sorted(df["property_type_en"].dropna().astype(str).unique())
selected_property_types = st.sidebar.multiselect(
    "Select Property Type",
    options=property_options,
    default=property_options
)

top_areas_default = (
    df["area_name_en"]
    .dropna()
    .astype(str)
    .value_counts()
    .head(20)
    .index
    .tolist()
)

selected_areas = st.sidebar.multiselect(
    "Select Area",
    options=sorted(df["area_name_en"].dropna().astype(str).unique()),
    default=top_areas_default
)

st.sidebar.markdown("---")
st.sidebar.info(
    "To update the dashboard with newer DLD records, download the latest transactions CSV and save it as data/raw/Transactions_live.csv."
)

# --------------------------------------------------
# Apply filters
# --------------------------------------------------
filtered_df = df.copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["transaction_date"] >= start_date) &
        (filtered_df["transaction_date"] <= end_date)
    ]

if selected_property_types:
    filtered_df = filtered_df[filtered_df["property_type_en"].astype(str).isin(selected_property_types)]

if selected_areas:
    filtered_df = filtered_df[filtered_df["area_name_en"].astype(str).isin(selected_areas)]

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust filters.")
    st.stop()

# --------------------------------------------------
# KPI calculations
# --------------------------------------------------
total_transactions = filtered_df["transaction_id"].nunique() if "transaction_id" in filtered_df.columns else len(filtered_df)
total_sales_value = filtered_df["actual_worth"].sum()
avg_transaction_price = filtered_df["actual_worth"].mean()
median_transaction_price = filtered_df["actual_worth"].median()
avg_price_per_sqm = filtered_df["price_per_sqm"].mean()
total_areas = filtered_df["area_name_en"].nunique()

top_area_by_sales = (
    filtered_df.groupby("area_name_en")["actual_worth"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

top_property_type = filtered_df["property_type_en"].value_counts().index[0]

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-title">🏙️ Dubai Real Estate Price Intelligence Dashboard</div>
        <div class="hero-subtitle">
            A professional market intelligence dashboard for Dubai property transactions.
            It combines historical market analysis with optional latest DLD transaction CSV updates.
            Latest available transaction date in this dashboard: <b>{latest_data_date.date()}</b>.
        </div>
        <div class="pill-row">
            <div class="pill">Historical + Latest CSV Ready</div>
            <div class="pill">Dubai Market Analytics</div>
            <div class="pill">ML Price Prediction</div>
            <div class="pill">Live-Aware Forecasting</div>
            <div class="pill">Portfolio Project</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

live_status_card(
    "Live Data Compatibility",
    f"{live_message} The dashboard currently covers data from {oldest_data_date.date()} to {latest_data_date.date()}."
)

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Executive Overview",
    "📍 Area Intelligence",
    "🏢 Property Type Analysis",
    "🤖 ML Price Prediction",
    "📈 Forecasting"
])

# --------------------------------------------------
# Tab 1: Executive Overview
# --------------------------------------------------
with tab1:
    st.markdown("## Executive Overview")
    st.caption("A simple summary of Dubai property market performance for the selected filters.")

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        metric_card("Total Transactions", format_number(total_transactions), "Number of property deals")
    with kpi2:
        metric_card("Total Sales Value", format_aed(total_sales_value), "Total transaction value")
    with kpi3:
        metric_card("Avg Price", format_aed(avg_transaction_price), "Average transaction price")

    kpi4, kpi5, kpi6 = st.columns(3)
    with kpi4:
        metric_card("Median Price", format_aed(median_transaction_price), "Typical market price")
    with kpi5:
        metric_card("Avg AED / Sqm", format_aed(avg_price_per_sqm), "Average price density")
    with kpi6:
        metric_card("Active Areas", format_number(total_areas), "Areas in selected view")

    insight_box(
        "Plain-English Summary",
        f"In this filtered market view, {top_area_by_sales} leads by total sales value, "
        f"while {top_property_type} is the most active property type. "
        f"The average transaction price is {format_aed(avg_transaction_price)}, "
        f"and the average price per square meter is {format_aed(avg_price_per_sqm)}."
    )

    monthly_filtered = (
        filtered_df
        .groupby("year_month_sort")
        .agg(
            total_transactions=("transaction_id", "count"),
            total_sales_value=("actual_worth", "sum"),
            average_price=("actual_worth", "mean"),
            average_price_per_sqm=("price_per_sqm", "mean")
        )
        .reset_index()
        .sort_values("year_month_sort")
    )

    col1, col2 = st.columns([1.25, 1])

    with col1:
        fig = px.area(
            monthly_filtered,
            x="year_month_sort",
            y="total_sales_value",
            title="Monthly Sales Value Trend",
            labels={"year_month_sort": "Month", "total_sales_value": "Sales Value AED"},
            color_discrete_sequence=["#F59E0B"]
        )
        fig = style_plotly(fig, height=440)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_areas_sales = (
            filtered_df
            .groupby("area_name_en")
            .agg(total_sales_value=("actual_worth", "sum"))
            .reset_index()
            .sort_values("total_sales_value", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_areas_sales,
            x="total_sales_value",
            y="area_name_en",
            orientation="h",
            title="Top 10 Areas by Sales Value",
            labels={"total_sales_value": "Sales Value AED", "area_name_en": "Area"},
            color="total_sales_value",
            color_continuous_scale="Agsunset"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        fig = style_plotly(fig, height=440)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        property_share = (
            filtered_df
            .groupby("property_type_en")
            .agg(total_transactions=("transaction_id", "count"))
            .reset_index()
            .sort_values("total_transactions", ascending=False)
        )

        fig = px.pie(
            property_share,
            names="property_type_en",
            values="total_transactions",
            hole=0.55,
            title="Transaction Share by Property Type",
            color_discrete_sequence=px.colors.sequential.Agsunset
        )
        fig = style_plotly(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        reg_type_summary = (
            filtered_df
            .groupby("reg_type_en")
            .agg(total_transactions=("transaction_id", "count"))
            .reset_index()
            .sort_values("total_transactions", ascending=False)
        )

        fig = px.bar(
            reg_type_summary,
            x="reg_type_en",
            y="total_transactions",
            title="Ready vs Off-Plan Market Activity",
            labels={"reg_type_en": "Registration Type", "total_transactions": "Transactions"},
            color="total_transactions",
            color_continuous_scale="Tealgrn"
        )
        fig.update_layout(coloraxis_showscale=False)
        fig = style_plotly(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    section_summary(
        "Executive Overview Summary",
        "This page gives a quick snapshot of the selected Dubai real estate market. "
        "The KPIs show the size of the market, total transaction value, average deal price, and average price per square meter. "
        "The trend chart shows how sales value changes over time, while the area and property charts show where market activity is concentrated."
    )

# --------------------------------------------------
# Tab 2: Area Intelligence
# --------------------------------------------------
with tab2:
    st.markdown("## Area Intelligence")
    st.caption("Compare Dubai areas by transaction activity, total sales value, average price, and price per sqm.")

    area_summary = (
        filtered_df
        .groupby("area_name_en")
        .agg(
            total_transactions=("transaction_id", "count"),
            total_sales_value=("actual_worth", "sum"),
            average_price=("actual_worth", "mean"),
            median_price=("actual_worth", "median"),
            average_price_per_sqm=("price_per_sqm", "mean")
        )
        .reset_index()
        .sort_values("total_sales_value", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            area_summary.sort_values("total_transactions", ascending=False).head(15),
            x="total_transactions",
            y="area_name_en",
            orientation="h",
            title="Most Active Areas by Number of Deals",
            labels={"total_transactions": "Transactions", "area_name_en": "Area"},
            color="total_transactions",
            color_continuous_scale="Blues"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        fig = style_plotly(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_price_per_sqm = (
            area_summary[area_summary["total_transactions"] >= 100]
            .sort_values("average_price_per_sqm", ascending=False)
            .head(15)
        )

        fig = px.bar(
            top_price_per_sqm,
            x="average_price_per_sqm",
            y="area_name_en",
            orientation="h",
            title="Premium Areas by Average Price per Sqm",
            labels={"average_price_per_sqm": "Avg Price / Sqm AED", "area_name_en": "Area"},
            color="average_price_per_sqm",
            color_continuous_scale="Agsunset"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        fig = style_plotly(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    bubble_df = area_summary[area_summary["total_transactions"] >= 100].copy()

    fig = px.scatter(
        bubble_df,
        x="total_transactions",
        y="average_price_per_sqm",
        size="total_sales_value",
        color="average_price",
        hover_name="area_name_en",
        title="Area Investment Map: Activity vs Price Level",
        labels={
            "total_transactions": "Market Activity: Number of Transactions",
            "average_price_per_sqm": "Average Price / Sqm AED",
            "average_price": "Average Price AED",
            "total_sales_value": "Sales Value AED"
        },
        color_continuous_scale="Agsunset",
        size_max=48
    )
    fig = style_plotly(fig, height=560)
    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        "How to read this chart",
        "Areas on the right side have higher transaction activity. Areas higher on the chart are more expensive per square meter. Large bubbles represent areas with higher total sales value."
    )

    with st.expander("View detailed area summary data"):
        render_dark_table(format_summary_table(area_summary), max_rows=12)

    top_area = area_summary.iloc[0]["area_name_en"]
    top_area_sales = area_summary.iloc[0]["total_sales_value"]

    section_summary(
        "Area Intelligence Summary",
        f"This section compares Dubai areas from both activity and pricing perspectives. "
        f"In the current filtered view, {top_area} has the highest total sales value at {format_aed(top_area_sales)}. "
        f"The bubble chart combines activity, price level, and total sales value so users can identify high-volume and high-value areas."
    )

# --------------------------------------------------
# Tab 3: Property Type Analysis
# --------------------------------------------------
with tab3:
    st.markdown("## Property Type Analysis")
    st.caption("Understand which property types dominate the market and how prices differ by category.")

    property_summary = (
        filtered_df
        .groupby("property_type_en")
        .agg(
            total_transactions=("transaction_id", "count"),
            total_sales_value=("actual_worth", "sum"),
            average_price=("actual_worth", "mean"),
            median_price=("actual_worth", "median"),
            average_price_per_sqm=("price_per_sqm", "mean")
        )
        .reset_index()
        .sort_values("total_transactions", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            property_summary,
            x="property_type_en",
            y="total_transactions",
            title="Demand by Property Type",
            labels={"property_type_en": "Property Type", "total_transactions": "Transactions"},
            color="total_transactions",
            color_continuous_scale="Tealgrn"
        )
        fig.update_layout(coloraxis_showscale=False)
        fig = style_plotly(fig, height=430)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            property_summary,
            x="property_type_en",
            y="average_price",
            title="Average Price by Property Type",
            labels={"property_type_en": "Property Type", "average_price": "Average Price AED"},
            color="average_price",
            color_continuous_scale="Agsunset"
        )
        fig.update_layout(coloraxis_showscale=False)
        fig = style_plotly(fig, height=430)
        st.plotly_chart(fig, use_container_width=True)

    subtype_summary = (
        filtered_df
        .groupby("property_sub_type_en")
        .agg(
            total_transactions=("transaction_id", "count"),
            average_price=("actual_worth", "mean"),
            average_price_per_sqm=("price_per_sqm", "mean")
        )
        .reset_index()
        .sort_values("total_transactions", ascending=False)
        .head(20)
    )

    fig = px.bar(
        subtype_summary,
        x="total_transactions",
        y="property_sub_type_en",
        orientation="h",
        title="Top 20 Property Subtypes by Transactions",
        labels={"total_transactions": "Transactions", "property_sub_type_en": "Property Subtype"},
        color="total_transactions",
        color_continuous_scale="Blues"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    fig = style_plotly(fig, height=560)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View property type summary data"):
        render_dark_table(format_summary_table(property_summary), max_rows=10)

    top_property = property_summary.iloc[0]["property_type_en"]
    top_property_transactions = property_summary.iloc[0]["total_transactions"]

    section_summary(
        "Property Type Analysis Summary",
        f"This section explains which property categories are most popular and how prices differ between them. "
        f"In the current view, {top_property} is the most active property type with {format_number(top_property_transactions)} transactions."
    )

# --------------------------------------------------
# Tab 4: ML Price Prediction
# --------------------------------------------------
with tab4:
    st.markdown("## Machine Learning Price Prediction")
    st.caption("Model comparison for predicting Dubai real estate transaction prices.")

    if ml_summary.empty:
        st.warning("ML summary file is missing. Please run the ML notebook first.")
    else:
        ml_chart_df = ml_summary.copy()
        ml_chart_df["short_model_name"] = ml_chart_df["model_name"].replace({
            "Random Forest Regressor": "Random Forest",
            "Gradient Boosting Regressor": "Gradient Boosting",
            "Realistic Random Forest Without Price Leakage": "Realistic RF",
            "Linear Regression": "Linear"
        })

        col1, col2 = st.columns([1, 1])

        with col1:
            with st.expander("View ML model metrics"):
                render_dark_table(format_summary_table(ml_summary), max_rows=10)

            realistic = ml_summary[
                ml_summary["model_name"].str.contains("Realistic", case=False, na=False)
            ]

            if not realistic.empty:
                r2_value = realistic.iloc[0]["R2"]
                mae_value = realistic.iloc[0]["MAE"]

                metric_card("Realistic Model R²", f"{r2_value:.2f}", "Real-world model quality")
                metric_card("Realistic Model MAE", format_aed(mae_value), "Average prediction error")

        with col2:
            fig = px.bar(
                ml_chart_df,
                x="short_model_name",
                y="R2",
                title="Model Comparison by R² Score",
                labels={"short_model_name": "Model", "R2": "R² Score"},
                color="R2",
                color_continuous_scale="Agsunset",
                text=ml_chart_df["R2"].round(2)
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(coloraxis_showscale=False)
            fig = style_plotly(fig, height=420)
            st.plotly_chart(fig, use_container_width=True)

        insight_box(
            "Important ML Note",
            "The benchmark Random Forest model performs extremely well because it includes price-per-square-meter, which is strongly related to the target price. For a more honest real-world result, the project also includes a realistic model without price leakage."
        )

        section_summary(
            "Machine Learning Summary",
            "This section compares different machine learning models used to estimate real estate transaction prices. "
            "It shows model performance while also explaining the difference between a benchmark model and a more realistic model without price leakage."
        )

# --------------------------------------------------
# Tab 5: Forecasting
# --------------------------------------------------
with tab5:
    st.markdown("## Forecasting")
    st.caption("Live-aware 12-month market forecast using the latest available monthly average transaction prices.")

    forecast_df, historical_monthly = build_live_forecast(filtered_df, months=12)

    if forecast_df.empty:
        st.warning("Not enough monthly data available for forecasting.")
    else:
        historical_tail = historical_monthly.tail(36).copy()
        historical_tail["series"] = "Historical Average Price"
        historical_tail = historical_tail.rename(columns={"average_price": "price"})

        forecast_plot = forecast_df.copy()
        forecast_plot["series"] = "Next 12 Months Forecast"
        forecast_plot = forecast_plot.rename(columns={"forecast_average_price": "price"})

        combined_forecast_plot = pd.concat(
            [
                historical_tail[["date", "price", "series"]],
                forecast_plot[["date", "price", "series"]]
            ],
            ignore_index=True
        )

        fig = px.line(
            combined_forecast_plot,
            x="date",
            y="price",
            color="series",
            markers=True,
            title="Historical Average Price and Next 12 Months Forecast",
            labels={"date": "Date", "price": "Average Price AED", "series": "Series"},
            color_discrete_sequence=["#38BDF8", "#F59E0B"]
        )
        fig = style_plotly(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

        first_forecast = forecast_df.iloc[0]["forecast_average_price"]
        latest_forecast = forecast_df.iloc[-1]["forecast_average_price"]
        forecast_change = latest_forecast - first_forecast
        forecast_change_pct = (forecast_change / first_forecast) * 100

        f1, f2, f3 = st.columns(3)
        with f1:
            metric_card("First Forecast Month", format_aed(first_forecast), "Forecast starting point")
        with f2:
            metric_card("12-Month Forecast Price", format_aed(latest_forecast), "Forecast ending point")
        with f3:
            metric_card("Forecast Change", f"{forecast_change_pct:.2f}%", "Projected change")

        insight_box(
            "Forecasting Interpretation",
            "This forecast now uses the latest available transaction data in the dashboard. It is still a simple baseline trend forecast, not a guaranteed market prediction."
        )

        section_summary(
            "Forecasting Summary",
            f"This page shows a 12-month market forecast based on the latest monthly average transaction prices available in the dashboard. "
            f"The forecast starts at {format_aed(first_forecast)} and reaches {format_aed(latest_forecast)} after 12 months, "
            f"which represents an estimated change of {forecast_change_pct:.2f}%. "
            f"If you add a newer DLD transactions CSV, this forecast will automatically update."
        )

        with st.expander("View forecast data"):
            render_dark_table(format_summary_table(forecast_df), max_rows=12)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built as an end-to-end data science and analytics portfolio project for Dubai/UAE real estate market intelligence.
    </div>
    """,
    unsafe_allow_html=True
)