import pandas as pd

def load_and_clean_data(filepath="data/hospital_events.csv"):
    df = pd.read_csv(filepath)
    
    # Missing values remove cheyadam
    df = df.dropna(subset=["case_id", "activity", "timestamp"])
    
    # Duplicates remove cheyadam
    df = df.drop_duplicates()
    
    # Datetime format lo convert cheyadam
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Timestamps prakaaram sort cheyadam
    df = df.sort_values(by=["case_id", "timestamp"]).reset_index(drop=True)
    
    return df

def get_data_summary(df):
    summary = {
        "total_cases": df["case_id"].nunique(),
        "total_events": len(df),
        "activities_count": df["activity"].nunique(),
        "departments_count": df["department"].nunique()
    }
    return summary