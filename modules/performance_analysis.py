import pandas as pd

def generate_executive_insights(df, avg_waits, conf_df):
    insights = []
    
    # Bottleneck alert
    if not avg_waits.empty:
        worst_delay = avg_waits.sort_values(by="Avg Waiting Time (Mins)", ascending=False).iloc[0]
        insights.append(
            f"⚠️ <b>Major Bottleneck Detected</b>: Highest average wait time is <b>{worst_delay['Avg Waiting Time (Mins)']} mins</b> "
            f"between <i>{worst_delay['From Activity']}</i> and <i>{worst_delay['To Activity']}</i>."
        )
    
    # Conformance rate
    if not conf_df.empty:
        total_patients = len(conf_df)
        std_count = len(conf_df[conf_df["Conformance Status"] == "Standard Ideal Pathway"])
        std_pct = round((std_count / total_patients) * 100, 1)
        insights.append(
            f"📊 <b>Pathway Adherence</b>: <b>{std_pct}%</b> of patients adhered strictly to the Standard Ideal Pathway."
        )
        
        revisits = len(conf_df[conf_df["Conformance Status"] == "Deviation: Repeated Consultation"])
        if revisits > 0:
            insights.append(
                f"🔄 <b>Process Deviations</b>: <b>{revisits} patient(s)</b> required multiple consultations, indicating review cycles or diagnosis confirmation delays."
            )
            
    return insights