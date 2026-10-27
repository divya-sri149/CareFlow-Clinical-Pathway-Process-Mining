import streamlit as st
import plotly.express as px
from modules.data_preprocessing import load_and_clean_data, get_data_summary
from modules.process_mining import (
    discover_process_graph,
    create_sankey_diagram,
    calculate_waiting_times
)
from modules.conformance_checking import check_conformance

st.set_page_config(page_title="CareFlow", page_icon="🏥", layout="wide")

# Sidebar - Controls & Upload
st.sidebar.title("⚙️ Dashboard Controls")

uploaded_file = st.sidebar.file_uploader("Upload Hospital CSV Log", type=["csv"])

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file)
    st.sidebar.success("Custom event log loaded!")
else:
    raw_df = load_and_clean_data("data/hospital_events.csv")
    st.sidebar.info("Using default hospital dataset.")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

all_departments = sorted(raw_df["department"].dropna().unique().tolist()) if "department" in raw_df.columns else []
selected_departments = st.sidebar.multiselect(
    "Select Departments",
    options=all_departments,
    default=all_departments
)

all_cases = sorted(raw_df["case_id"].unique().tolist())
selected_cases = st.sidebar.multiselect(
    "Filter by Patient ID",
    options=all_cases,
    default=all_cases[:10] if len(all_cases) >= 10 else all_cases
)

# Apply filters
filtered_df = raw_df[raw_df["case_id"].isin(selected_cases)]
if "department" in raw_df.columns and selected_departments:
    filtered_df = filtered_df[filtered_df["department"].isin(selected_departments)]

# Main Dashboard
st.title("🏥 CareFlow")
st.subheader("Clinical Pathway Process Mining")

if filtered_df.empty:
    st.warning("Filters match ayye records emi levu. Please select at least one department and patient.")
else:
    summary = get_data_summary(filtered_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Selected Patients", summary["total_cases"])
    col2.metric("Total Activities", summary["total_events"])
    col3.metric("Unique Activities", summary["activities_count"])
    col4.metric("Departments", summary["departments_count"])

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Clinical Event Log",
        "🔄 Process Flow",
        "⏱️ Bottleneck & Waiting Times",
        "🎯 Conformance & Deviations"
    ])

    with tab1:
        st.write(f"Showing **{len(filtered_df)}** event records based on selected filters:")
        st.dataframe(filtered_df, width="stretch")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Data (CSV)",
            data=csv_data,
            file_name="careflow_cleaned_events.csv",
            mime="text/csv"
        )

    with tab2:
        transitions_df, start_acts, end_acts = discover_process_graph(filtered_df)
        if not transitions_df.empty:
            sankey_fig = create_sankey_diagram(transitions_df)
            st.plotly_chart(sankey_fig, width="stretch")
            
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.subheader("Discovered Pathways")
                st.dataframe(transitions_df, width="stretch")
            with col_b:
                st.subheader("Entry & Exit Points")
                st.write("**Start Activities:**", dict(start_acts))
                st.write("**End Activities:**", dict(end_acts))
        else:
            st.info("Transitions discover cheyadaniki saripada data points levu.")

    with tab3:
        avg_waits = calculate_waiting_times(filtered_df)
        if not avg_waits.empty:
            st.subheader("Average Transition Delays")
            st.dataframe(avg_waits, width="stretch")
            waits_csv = avg_waits.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Bottleneck Report (CSV)",
                data=waits_csv,
                file_name="careflow_bottleneck_report.csv",
                mime="text/csv"
            )
            fig = px.bar(
                avg_waits,
                x="From Activity",
                y="Avg Waiting Time (Mins)",
                color="To Activity",
                barmode="group",
                title="Waiting Times Between Clinical Activities"
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Waiting times calculate cheyadaniki consecutive events saripoledu.")

    with tab4:
        st.subheader("Expected vs. Actual Pathway Conformance")
        st.markdown("**Standard Expected Flow:** `Registration ➔ Consultation ➔ Treatment ➔ Discharge`")
        
        conf_df = check_conformance(filtered_df)
        st.dataframe(conf_df, width="stretch")
        
        # Conformance breakdown chart
        fig_conf = px.pie(
            conf_df,
            names="Conformance Status",
            title="Patient Pathway Conformance Breakdown"
        )
        st.plotly_chart(fig_conf, width="stretch")