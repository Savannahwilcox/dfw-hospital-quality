import pandas as pd

deaths = pd.read_csv("data/raw/Complications_and_Deaths-Hospital.csv", dtype=str)
readmits = pd.read_csv("data/raw/Unplanned_Hospital_Visits-Hospital.csv", dtype=str)

def get_measure(df, measure_id, new_name):
    rows = df[df["Measure ID"] == measure_id]
    rows = rows[rows["Footnote"].fillna("") != "1"]
    rows = rows[["Facility ID", "Score"]].copy()
    rows[new_name] = pd.to_numeric(rows["Score"], errors="coerce")
    return rows[["Facility ID", new_name]]


death_rate = get_measure(deaths, "Hybrid_HWM", "death_rate")
readmit_rate = get_measure(readmits, "READM_30_HF", "hf_readmit_rate")

print(death_rate["death_rate"].describe())
print(readmit_rate["hf_readmit_rate"].describe())

death_rate.to_csv("data/clean/death_rate.csv", index=False)
readmit_rate.to_csv("data/clean/hf_readmit_rate.csv", index=False)