
import streamlit as st
import pandas as pd
import plotly.express as px
import pm4py

st.set_page_config(
    page_title="CareFlow",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 CareFlow")
st.subheader("Clinical Pathway Process Mining")

st.write(
    "Analyze clinical workflows and discover "
    "bottlenecks using hospital event data."
)

# Load hospital event data
@st.cache_data
def load_data():
    df = pd.read_csv("data/hospital_events.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

try:
    df = load_data()

    st.success("Hospital event data loaded successfully!")

    # Key performance indicators
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", df["case_id"].nunique())
    col2.metric("Total Activities", len(df))
    col3.metric("Departments", df["department"].nunique())

    st.subheader("📋 Hospital Event Log")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Activities Distribution")

    activity_counts = (
        df["activity"]
        .value_counts()
        .reset_index()
    )
    activity_counts.columns = ["Activity", "Count"]

    fig = px.bar(
        activity_counts,
        x="Activity",
        y="Count",
        title="Number of Events by Clinical Activity",
        text="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error(
        "Dataset not found. Please check "
        "data/hospital_events.csv"
    )
