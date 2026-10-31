import pandas as pd
import random
from datetime import datetime, timedelta

def generate_hospital_data(num_patients=1000):
    departments_map = {
        "Registration": "Administration",
        "Consultation": "General Medicine",
        "Laboratory Test": "Diagnostics",
        "Imaging": "Radiology",
        "Treatment": "Inpatient Care",
        "Discharge": "Administration"
    }

    records = []
    base_time = datetime(2026, 1, 1, 8, 0, 0)

    for i in range(1, num_patients + 1):
        case_id = f"P{i:04d}"
        
        # Path type decide cheyadam (Real hospital scenarios)
        rand_val = random.random()
        if rand_val < 0.60:
            # 60% standard flow
            activities = ["Registration", "Consultation", "Treatment", "Discharge"]
        elif rand_val < 0.80:
            # 20% lab & diagnosis flow
            activities = ["Registration", "Consultation", "Laboratory Test", "Consultation", "Treatment", "Discharge"]
        elif rand_val < 0.95:
            # 15% radiology imaging flow
            activities = ["Registration", "Consultation", "Imaging", "Treatment", "Discharge"]
        else:
            # 5% complex flow with multiple delays
            activities = ["Registration", "Consultation", "Laboratory Test", "Imaging", "Consultation", "Treatment", "Discharge"]

        curr_time = base_time + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 8),
            minutes=random.randint(0, 59)
        )

        for act in activities:
            records.append({
                "case_id": case_id,
                "activity": act,
                "timestamp": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
                "department": departments_map[act]
            })
            # Activity madhyalo waiting time (15 to 90 mins)
            curr_time += timedelta(minutes=random.randint(15, 90))

    df = pd.DataFrame(records)
    df.to_csv("data/hospital_events.csv", index=False)
    print(f"✅ Successfully generated {len(df)} events for {num_patients} patients in data/hospital_events.csv!")

if __name__ == "__main__":
    generate_hospital_data(1000)