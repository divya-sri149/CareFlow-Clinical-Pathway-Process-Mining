import pandas as pd

def generate_executive_insights(df, avg_waits, conf_df):
    insights = []
    
    # Bottleneck alert
    if not avg_waits.empty:
        worst_delay = avg_waits.sort_values(by="Avg Waiting Time (Mins)", ascending=False).iloc[0]
        insights.append(
            f"⚠️ **Major Bottleneck Detected**: Highest average wait time is **{worst_delay['Avg Waiting Time (Mins)']} mins** "
            f"between *{worst_delay['From Activity']}* and *{worst_delay['To Activity']}*."
        )
    
    # Conformance rate
    if not conf_df.empty:
        total_patients = len(conf_df)
        std_count = len(conf_df[conf_df["Conformance Status"] == "Standard Ideal Pathway"])
        std_pct = round((std_count / total_patients) * 100, 1)
        insights.append(
            f"📊 **Pathway Adherence**: **{std_pct}%** of patients adhered strictly to the Standard Ideal Pathway."
        )
        
        revisits = len(conf_df[conf_df["Conformance Status"] == "Deviation: Repeated Consultation"])
        if revisits > 0:
            insights.append(
                f"🔄 **Process Deviations**: **{revisits} patient(s)** required multiple consultations, indicating review cycles or diagnosis confirmation delays."
            )
            
    return insights