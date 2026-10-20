import pandas as pd

def load_and_clean_data(file_source="data/hospital_events.csv"):
    # String path leda uploaded file buffer rendu handle chesthundhi
    if isinstance(file_source, str):
        df = pd.read_csv(file_source)
    else:
        df = pd.read_csv(file_source)
    
    # Missing values remove cheyadam
    df = df.dropna(subset=["case_id", "activity", "timestamp"])
    
    # Duplicates remove cheyadam
    df = df.drop_duplicates()
    
    # Datetime convert chesi sort cheyadam
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=["case_id", "timestamp"]).reset_index(drop=True)
    
    return df

def get_data_summary(df):
    if df.empty:
        return {
            "total_cases": 0,
            "total_events": 0,
            "activities_count": 0,
            "departments_count": 0
        }
    return {
        "total_cases": int(df["case_id"].nunique()),
        "total_events": int(len(df)),
        "activities_count": int(df["activity"].nunique()),
        "departments_count": int(df["department"].nunique()) if "department" in df.columns else 0
    }