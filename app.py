import streamlit as st
import pandas as pd
from modules.data_preprocessing import load_and_clean_data, get_data_summary

st.set_page_config(
    page_title="CareFlow",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 CareFlow")
st.subheader("Clinical Pathway Process Mining")

# Data Load
df = load_and_clean_data()
summary = get_data_summary(df)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", summary["total_cases"])
col2.metric("Total Activities", summary["total_events"])
col3.metric("Unique Activities", summary["activities_count"])
col4.metric("Departments", summary["departments_count"])

st.markdown("---")
st.subheader("📋 Preprocessed Clinical Event Log")
st.dataframe(df, width="stretch")