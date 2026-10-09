# look at DFW hospitals specifically- which ones fit the national
# pattern and which dont

import pandas as pd

df = pd.read_csv("data/clean/hospitals_combined.csv", dtype={"Facility ID": str})

median_rating = df["pct_9_10"].median()
median_death = df["death_rate"].median()

dfw = df[df["dfw"]].dropna(subset=["pct_9_10", "death_rate"]).copy()
print("DFW hospitals with both numbers:", len(dfw))

# label each hospital by whether patients rate it above or below the
# national median, and whether its death rate is above or below
dfw["patients_say"] = (dfw["pct_9_10"] > median_rating).map({True: "rated high", False: "rated low"})
dfw["death_rate_is"] = (dfw["death_rate"] > median_death).map({True: "higher", False: "lower or typical"})

print(pd.crosstab(dfw["patients_say"], dfw["death_rate_is"]))

cols = ["Facility Name", "City/Town", "pct_9_10", "death_rate", "hf_readmit_rate"]
print(dfw.sort_values("pct_9_10", ascending=False)[cols].to_string())