# Compares CMS's new hybrid hospital-wide death rate to the older
# condition-specific death rates, which CMS rates as better, no different
# or worse than national. Checks whether the two agree, and which DFW
# hospitals look different depending on which one you use.

import pandas as pd

pd.set_option("display.width", 200)

df = pd.read_csv("data/clean/hospitals_combined.csv", dtype={"Facility ID": str})
hosp = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype=str)

old = hosp[["Facility ID", "Count of Facility MORT Measures",
            "Count of MORT Measures Better", "Count of MORT Measures Worse"]].copy()
old.columns = ["Facility ID", "mort_measures", "mort_better", "mort_worse"]
for col in ["mort_measures", "mort_better", "mort_worse"]:
    old[col] = pd.to_numeric(old[col], errors="coerce")

df = df.merge(old, on="Facility ID", how="left")
df = df.dropna(subset=["death_rate", "mort_measures"])

# only hospitals with at least 3 older measures, so the rating means something
df = df[df["mort_measures"] >= 3]


def old_rating(row):
    if row["mort_better"] > 0 and row["mort_worse"] == 0:
        return "Better on 1+"
    if row["mort_worse"] > 0 and row["mort_better"] == 0:
        return "Worse on 1+"
    if row["mort_better"] > 0 and row["mort_worse"] > 0:
        return "Mixed"
    return "No different on all"


df["old_rating"] = df.apply(old_rating, axis=1)

print("US hospitals:", len(df))
print(df.groupby("old_rating")["death_rate"].agg(["size", "mean"]).round(2))

cols = ["Facility Name", "death_rate", "mort_better", "mort_worse", "old_rating", "pct_9_10"]
dfw = df[df["dfw"]].sort_values("death_rate")
print()
print(dfw[cols].to_string(index=False))

df.to_csv("data/clean/mortality_compare.csv", index=False)

# tag each DFW hospital with its health system, based on the name
def system(name):
    name = name.upper()
    if "BAYLOR" in name:
        return "Baylor Scott & White"
    if "TEXAS HEALTH" in name:
        return "Texas Health Resources"
    if "MEDICAL CITY" in name:
        return "Medical City (HCA)"
    if "METHODIST" in name:
        return "Methodist Health System"
    return "Other"


dfw = dfw.copy()
dfw["system"] = dfw["Facility Name"].apply(system)
dfw["rated_better"] = dfw["old_rating"].isin(["Better on 1+", "Mixed"])

print(dfw.groupby("system").agg(
    hospitals=("system", "size"),
    rated_better=("rated_better", "sum"),
    avg_death_rate=("death_rate", "mean"),
    avg_pct_9_10=("pct_9_10", "mean"),
).round(2).to_string())

# check whether Baylors lead is just a size effect
deaths = pd.read_csv("data/raw/Complications_and_Deaths-Hospital.csv", dtype=str)
hwm = deaths[deaths["Measure ID"] == "Hybrid_HWM"][["Facility ID", "Denominator"]].copy()
hwm["patients"] = pd.to_numeric(hwm["Denominator"], errors="coerce")

dfw = dfw.merge(hwm[["Facility ID", "patients"]], on="Facility ID", how="left")

print()
print("Median patients, rated better vs not:")
print(dfw.groupby("rated_better")["patients"].median())

print()
print("Median patients by system:")
print(dfw.groupby("system")["patients"].median())

# compare systems using only the bigger half of DFW hospitals
big = dfw[dfw["patients"] >= dfw["patients"].median()]
print()
print("Bigger half of DFW hospitals only:")
print(big.groupby("system").agg(
    hospitals=("system", "size"),
    rated_better=("rated_better", "sum"),
).to_string())