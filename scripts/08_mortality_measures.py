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