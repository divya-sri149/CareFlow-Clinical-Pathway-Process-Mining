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

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="CareFlow | Clinical Process Mining",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Professional Healthcare Theme (Custom CSS)
# ---------------------------------------------------------
# ---------------------------------------------------------
# Professional Healthcare Theme (Custom CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 1. App-wide Base Background (Soft Slate Mesh) */
    .stApp {
        background-color: #f0f4f9 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(2, 132, 199, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(30, 58, 138, 0.06) 0px, transparent 50%) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 2. Main Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #091e42 0%, #0c4a6e 50%, #0284c7 100%);
        padding: 2.2rem 2.6rem;
        border-radius: 18px;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 12px 28px -6px rgba(2, 132, 199, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-container h1 {
        color: #ffffff !important;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-container p {
        color: #bae6fd !important;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }

    /* 3. Floating Metric KPI Cards */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 1.25rem 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 20px -3px rgba(15, 23, 42, 0.07), 0 4px 6px -2px rgba(15, 23, 42, 0.04) !important;
        border-top: 4px solid #0284c7 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 25px -5px rgba(2, 132, 199, 0.15) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    div[data-testid="stMetricValue"] div {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #0c4a6e !important;
    }

    /* 4. Tab Navigation Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #e2e8f0;
        padding: 6px;
        border-radius: 14px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.4rem;
        font-weight: 600;
        color: #475569;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.6);
        color: #0f172a;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0284c7 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
    }

    /* 5. Executive Insight Cards */
    .insight-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #0284c7;
        padding: 1.25rem 1.6rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        font-size: 0.98rem;
        color: #1e293b;
        line-height: 1.6;
    }
    .insight-card b {
        color: #0f172a;
        font-weight: 700;
    }
    .insight-card i {
        color: #0284c7;
        font-style: normal;
        font-weight: 600;
    }

    /* 6. Professional Sidebar Panel */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%) !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
        margin-top: 1rem !important;
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 1px dashed #cbd5e1 !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background-color: #f8fafc !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #e2e8f0 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* 7. Clinical Soft-Blue Filter Badges */
    [data-testid="stSidebar"] [data-baseweb="tag"],
    span[data-baseweb="tag"] {
        background-color: #e0f2fe !important;
        background: #e0f2fe !important;
        border: 1px solid #7dd3fc !important;
        border-radius: 8px !important;
        padding: 4px 10px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    span[data-baseweb="tag"] span {
        color: #0369a1 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] svg,
    span[data-baseweb="tag"] svg {
        fill: #0284c7 !important;
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# Sidebar: Data Source & Patient Cohort Filters
# ---------------------------------------------------------
st.sidebar.markdown("### 📁 Data Source & Intake")
uploaded_file = st.sidebar.file_uploader(
    "Upload Clinical Event Log (.csv)", 
    type=["csv"],
    help="Upload a standard CSV file with case_id, activity, timestamp, and department columns."
)

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file)
    st.sidebar.success("Custom hospital event log active.")
else:
    raw_df = load_and_clean_data("data/hospital_events.csv")


st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Patient Cohort Filters")

# Department Filter
all_departments = sorted(raw_df["department"].dropna().unique().tolist()) if "department" in raw_df.columns else []
selected_departments = st.sidebar.multiselect(
    "Clinical Departments",
    options=all_departments,
    default=all_departments
)

# Patient ID Filter
all_cases = sorted(raw_df["case_id"].unique().tolist())
selected_cases = st.sidebar.multiselect(
    "Patient Cohort (Case IDs)",
    options=all_cases,
    default=all_cases[:15] if len(all_cases) >= 15 else all_cases
)

# Apply cohort filtering
filtered_df = raw_df[raw_df["case_id"].isin(selected_cases)]
if "department" in raw_df.columns and selected_departments:
    filtered_df = filtered_df[filtered_df["department"].isin(selected_departments)]

# ---------------------------------------------------------
# Main Application Content
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <h1>🏥 CareFlow: Clinical Intelligence Platform</h1>
    <p>Operational Process Mining, Bottleneck Identification & Protocol Adherence</p>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No records match the selected criteria. Please expand the department or patient ID filter.")
else:
    # Key Performance Indicator (KPI) Cards
    summary = get_data_summary(filtered_df)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Active Patient Traces", f"{summary['total_cases']:,}")
    kpi2.metric("Total Clinical Events", f"{summary['total_events']:,}")
    kpi3.metric("Care Pathway Stages", summary["activities_count"])
    kpi4.metric("Reporting Units", summary["departments_count"])

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Dashboard Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Event Log",
        "🔄 Pathway Flow",
        "⏱️ Bottlenecks & Delays",
        "🎯 Conformance Analysis",
        "💡 Clinical Insights"
    ])

    # Tab 1: Clinical Event Log
    with tab1:
        st.subheader("Sanitized Clinical Event Log")
        st.caption(f"Showing {len(filtered_df):,} event instances across selected filters.")
        
        st.dataframe(filtered_df, width="stretch")
        
        csv_export = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Cleaned Dataset (CSV)",
            data=csv_export,
            file_name="careflow_cleaned_cohort.csv",
            mime="text/csv"
        )

    # Tab 2: Discovered Pathway Map
    with tab2:
        transitions_df, start_acts, end_acts = discover_process_graph(filtered_df)
        if not transitions_df.empty:
            st.subheader("Patient Flow Topology (Sankey Diagram)")
            st.caption("Flow volume width represents patient transitions between consecutive clinical stages.")
            
            sankey_fig = create_sankey_diagram(transitions_df)
            sankey_fig.update_layout(
                font_family="-apple-system, BlinkMacSystemFont, Segoe UI",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(sankey_fig, width="stretch")
            
            col_left, col_right = st.columns([2, 1])
            with col_left:
                st.markdown("**Discovered Pathway Transitions**")
                st.dataframe(transitions_df, width="stretch")
            with col_right:
                st.markdown("#### 🚪 Gateway Endpoints")
                st.markdown("**Intake / Start Stages:**")
                for act, count in dict(start_acts).items():
                    st.success(f"🟢 **{act}**: {count} patients")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Discharge / End Stages:**")
                for act, count in dict(end_acts).items():
                    st.info(f"🏁 **{act}**: {count} patients")
        else:
            st.info("Insufficient pathway transitions found for this cohort selection.")

    # Tab 3: Delays and Bottlenecks
    with tab3:
        avg_waits = calculate_waiting_times(filtered_df)
        if not avg_waits.empty:
            st.subheader("Inter-Stage Transition Delays")
            st.caption("Average waiting durations between subsequent activity checkpoints.")
            
            st.dataframe(avg_waits, width="stretch")
            
            waits_export = avg_waits.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Delay Report (CSV)",
                data=waits_export,
                file_name="careflow_bottleneck_delays.csv",
                mime="text/csv"
            )
            
            fig_bar = px.bar(
                avg_waits,
                x="From Activity",
                y="Avg Waiting Time (Mins)",
                color="To Activity",
                barmode="group",
                title="Mean Activity Waiting Times (Minutes)",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_bar.update_layout(
                font_family="-apple-system, BlinkMacSystemFont, Segoe UI",
                xaxis_title="Origin Stage",
                yaxis_title="Duration (Minutes)",
                legend_title="Destination Stage"
            )
            st.plotly_chart(fig_bar, width="stretch")
        else:
            st.info("Insufficient sequential events available to compute waiting durations.")

    # Tab 4: Protocol Conformance
    with tab4:
        st.subheader("Clinical Pathway Conformance Checking")
        st.caption("Benchmarking against Standard Care Protocol: Registration ➔ Consultation ➔ Treatment ➔ Discharge")
        
        conf_df = check_conformance(filtered_df)
        st.dataframe(conf_df, width="stretch")
        
        fig_pie = px.pie(
            conf_df,
            names="Conformance Status",
            title="Adherence vs. Pathway Deviations",
            hole=0.45,
            template="plotly_white",
            color_discrete_sequence=["#0284c7", "#f59e0b", "#10b981", "#ef4444"]
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            font_family="-apple-system, BlinkMacSystemFont, Segoe UI",
            showlegend=True
        )
        st.plotly_chart(fig_pie, width="stretch")

    # Tab 5: Automated Executive Insights
    with tab5:
        st.subheader("Executive Clinical Intelligence")
        st.caption("Rule-based operational highlights derived from process flow and waiting time data.")
        
        avg_waits = calculate_waiting_times(filtered_df)
        conf_df = check_conformance(filtered_df)
        insights = generate_executive_insights(filtered_df, avg_waits, conf_df)
        
        if insights:
            for item in insights:
                card_html = f'<div class="insight-card">{item}</div>'
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("No actionable clinical alerts identified for the selected cohort.")