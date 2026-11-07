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

def create_sankey_diagram(df_transitions):
    # Get unique activity labels
    all_nodes = list(pd.unique(df_transitions[['Source', 'Target']].values.ravel('K')))
    node_map = {node: idx for idx, node in enumerate(all_nodes)}
    
    # Map sources, targets, and values
    sources = df_transitions['Source'].map(node_map).tolist()
    targets = df_transitions['Target'].map(node_map).tolist()
    values = df_transitions['Count'].tolist()
    
    # Palette for clear node visibility
    palette = [
        "#0284c7", "#0ea5e9", "#2563eb", "#7c3aed", 
        "#059669", "#d97706", "#dc2626", "#475569"
    ]
    node_colors = [palette[i % len(palette)] for i in range(len(all_nodes))]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="#1e293b", width=1),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            # Semi-transparent blue for high contrast and visible flow paths
            color="rgba(2, 132, 199, 0.45)"
        )
    )])
    
    fig.update_layout(
        title_text="Patient Pathway Flow Topology",
        font=dict(size=13, color="#1e293b", family="sans-serif"),
        height=520,
        margin=dict(l=20, r=20, t=50, b=25)
    )
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