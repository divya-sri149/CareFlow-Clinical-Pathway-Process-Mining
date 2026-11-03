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

if filtered_df.empty:
    st.warning("Filters match ayye records levu bro. Please select at least one department and patient.")
else:
    # Summary Metrics
    summary = get_data_summary(filtered_df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected Patients", summary["total_cases"])
    c2.metric("Total Activities", summary["total_events"])
    c3.metric("Unique Stages", summary["activities_count"])
    c4.metric("Active Departments", summary["departments_count"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Event Log",
        "🔄 Process Pathways",
        "⏱️ Delay & Bottlenecks",
        "🎯 Conformance Analysis",
        "💡 Clinical Insights"
    ])

    with tab1:
        st.subheader("Clinical Event Records")
        st.write(f"Displaying **{len(filtered_df)}** records matching current filters:")
        st.dataframe(filtered_df, use_container_width=True)
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Log (CSV)",
            data=csv_data,
            file_name="careflow_filtered_events.csv",
            mime="text/csv"
        )

    with tab2:
        transitions_df, start_acts, end_acts = discover_process_graph(filtered_df)
        if not transitions_df.empty:
            st.subheader("Patient Pathway Flow Map")
            sankey_fig = create_sankey_diagram(transitions_df)
            st.plotly_chart(sankey_fig, use_container_width=True)
            
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.write("**Discovered Activity Transitions**")
                st.dataframe(transitions_df, use_container_width=True)
            with col_b:
                st.write("**Entry Stages**", dict(start_acts))
                st.write("**Exit Stages**", dict(end_acts))
        else:
            st.info("Transitions discover cheyadaniki saripada data points levu.")

    with tab3:
        avg_waits = calculate_waiting_times(filtered_df)
        if not avg_waits.empty:
            st.subheader("Average Operational Delays")
            st.dataframe(avg_waits, use_container_width=True)
            
            waits_csv = avg_waits.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Delay Report (CSV)",
                data=waits_csv,
                file_name="careflow_delay_report.csv",
                mime="text/csv"
            )
            
            fig = px.bar(
                avg_waits,
                x="From Activity",
                y="Avg Waiting Time (Mins)",
                color="To Activity",
                barmode="group",
                title="Stage Transition Waiting Times (Minutes)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Waiting times calculate cheyadaniki consecutive data saripoledu.")

   