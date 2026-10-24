import pandas as pd

# Hospital Standard Ideal Pathway
STANDARD_PATHWAY = [
    "Registration",
    "Consultation",
    "Treatment",
    "Discharge"
]

def check_conformance(df):
    results = []
    
    # Sort and group by patient
    df_sorted = df.sort_values(by=["case_id", "timestamp"])
    
    for case_id, group in df_sorted.groupby("case_id"):
        actual_path = group["activity"].tolist()
        
        # Check standard path match
        is_standard = actual_path == STANDARD_PATHWAY
        
        # Check repeated consultations
        consult_count = actual_path.count("Consultation")
        has_revisit = consult_count > 1
        
        # Check diagnostic tests done
        has_tests = ("Laboratory Test" in actual_path) or ("Imaging" in actual_path)
        
        # Status determination
        if is_standard:
            status = "Standard Ideal Pathway"
        elif has_revisit:
            status = "Deviation: Repeated Consultation"
        elif has_tests:
            status = "Diagnostic Pathway (Lab/Imaging)"
        else:
            status = "Non-standard Pathway"
            
        results.append({
            "Patient ID": case_id,
            "Total Steps": len(actual_path),
            "Sequence Followed": " ➔ ".join(actual_path),
            "Conformance Status": status
        })
        
    return pd.DataFrame(results)