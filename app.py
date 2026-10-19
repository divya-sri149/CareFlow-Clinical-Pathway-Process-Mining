import streamlit as st
import plotly.express as px
from modules.data_preprocessing import load_and_clean_data, get_data_summary
from modules.process_mining import (
    discover_process_graph,
    create_sankey_diagram,
    calculate_waiting_times
)

st.set_page_config(page_title="CareFlow", page_icon="🏥", layout="wide")
st.title("🏥 CareFlow")
st.subheader("Clinical Pathway Process Mining")

df = load_and_clean_data()
summary = get_data_summary(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", summary["total_cases"])
col2.metric("Total Activities", summary["total_events"])
col3.metric("Unique Activities", summary["activities_count"])
col4.metric("Departments", summary["departments_count"])

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📋 Clinical Event Log", "🔄 Process Flow", "⏱️ Bottleneck & Waiting Times"])

with tab1:
    st.dataframe(df, width="stretch")

with tab2:
    transitions_df, start_acts, end_acts = discover_process_graph(df)
    
    # Visual Sankey Diagram
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

with tab3:
    avg_waits = calculate_waiting_times(df)
    
    st.subheader("Average Transition Delays")
    st.dataframe(avg_waits, width="stretch")
    
    fig = px.bar(
        avg_waits,
        x="From Activity",
        y="Avg Waiting Time (Mins)",
        color="To Activity",
        barmode="group",
        title="Waiting Times Between Clinical Activities"
    )
    st.plotly_chart(fig, width="stretch")