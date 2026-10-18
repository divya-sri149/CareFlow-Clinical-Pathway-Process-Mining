import pm4py
import pandas as pd
import plotly.graph_objects as go

def discover_process_graph(df):
    event_log = pm4py.format_dataframe(
        df.copy(),
        case_id="case_id",
        activity_key="activity",
        timestamp_key="timestamp"
    )
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    transitions = [
        {"Source": src, "Target": target, "Count": count}
        for (src, target), count in dfg.items()
    ]
    return pd.DataFrame(transitions), start_activities, end_activities

def create_sankey_diagram(transitions_df):
    all_nodes = list(pd.concat([transitions_df["Source"], transitions_df["Target"]]).unique())
    node_map = {node: idx for idx, node in enumerate(all_nodes)}
    
    source_indices = transitions_df["Source"].map(node_map).tolist()
    target_indices = transitions_df["Target"].map(node_map).tolist()
    values = transitions_df["Count"].tolist()
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="royalblue"
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        )
    )])
    fig.update_layout(title_text="Clinical Pathway Process Flow (Sankey)", font_size=12)
    return fig

def calculate_waiting_times(df):
    df_sorted = df.sort_values(by=["case_id", "timestamp"]).copy()
    df_sorted["next_activity"] = df_sorted.groupby("case_id")["activity"].shift(-1)
    df_sorted["next_timestamp"] = df_sorted.groupby("case_id")["timestamp"].shift(-1)
    df_sorted["duration_mins"] = (df_sorted["next_timestamp"] - df_sorted["timestamp"]).dt.total_seconds() / 60
    
    waits = df_sorted.dropna(subset=["next_activity", "duration_mins"])
    avg_waits = waits.groupby(["activity", "next_activity"])["duration_mins"].mean().reset_index()
    avg_waits["duration_mins"] = avg_waits["duration_mins"].round(1)
    avg_waits.columns = ["From Activity", "To Activity", "Avg Waiting Time (Mins)"]
    return avg_waits