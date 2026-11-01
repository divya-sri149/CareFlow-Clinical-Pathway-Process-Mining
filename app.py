import streamlit as st
import plotly.express as px
from modules.data_preprocessing import load_and_clean_data, get_data_summary
from modules.process_mining import (
    discover_process_graph,
    create_sankey_diagram,
    calculate_waiting_times
)
from modules.conformance_checking import check_conformance
from modules.performance_analysis import generate_executive_insights

# Page Config
st.set_page_config(
    page_title="CareFlow - Clinical Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Healthcare Styling (CSS)
st.markdown("""
<style>
    /* Main Background & Font */
    .main {
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1e3a8a, #0284c7);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-box h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
    }
    .header-box p {
        margin: 5px 0 0 0;
        font-size: 1.05rem;
        opacity: 0.9;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        border-left: 5px solid #0284c7;
    }
    
    /* Tabs Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        color: #334155;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: white !important;
        border-color: #0284c7 !important;
    }

    /* Sidebar Clean Look */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### ⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("📂 Upload Event Log (CSV)", type=["csv"])

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file)
    st.sidebar.success("Custom event log loaded!")
else:
    raw_df = load_and_clean_data("data/hospital_events.csv")
    st.sidebar.info("Using default hospital dataset.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

all_departments = sorted(raw_df["department"].dropna().unique().tolist()) if "department" in raw_df.columns else []
selected_departments = st.sidebar.multiselect(
    "Select Departments",
    options=all_departments,
    default=all_departments
)

all_cases = sorted(raw_df["case_id"].unique().tolist())
selected_cases = st.sidebar.multiselect(
    "Filter Patient IDs",
    options=all_cases,
    default=all_cases[:10] if len(all_cases) >= 10 else all_cases
)

# Apply Filters
filtered_df = raw_df[raw_df["case_id"].isin(selected_cases)]
if "department" in raw_df.columns and selected_departments:
    filtered_df = filtered_df[filtered_df["department"].isin(selected_departments)]

# Header
st.markdown("""
<div class="header-box">
    <h1>🏥 CareFlow Clinical Intelligence</h1>
    <p>Process Mining, Pathway Optimization & Operational Bottleneck Discovery</p>
</div>
""", unsafe_allow_html=True)

