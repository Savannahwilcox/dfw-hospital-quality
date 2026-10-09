# tests whether hospitals that patients rate highly also have lower
# death rates. Uses every US acute care hospital with both numbers

import pandas as pd

df = pd.read_csv("data/clean/hospitals_combined.csv", dtype={"Facility ID": str})

# only keep hospitals that have both a patient rating and a death rate
both = df.dropna(subset=["pct_9_10", "death_rate"]).copy()

# split hospitals into 5 equal sized groups by patient rating
both["rating_group"] = pd.qcut(both["pct_9_10"], 5,
                               labels=["1 lowest", "2", "3", "4", "5 highest"])

# average death rate for each rating group
summary = both.groupby("rating_group", observed=True).agg(
    hospitals=("pct_9_10", "size"),
    rating_low=("pct_9_10", "min"),
    rating_high=("pct_9_10", "max"),
    avg_death_rate=("death_rate", "mean"),
)
print(summary.round(2))

# check how many top-rated hospitals still have 
# a worse than typical death rate
median_death = both["death_rate"].median()
top_group = both[both["rating_group"] == "5 highest"]

share_worse = (top_group["death_rate"] > median_death).mean()
print("National median death rate:", median_death)
print("Share of top-rated hospitals with above-median death rate:", round(share_worse * 100), "%")

bottom_group = both[both["rating_group"] == "1 lowest"]
share_worse_bottom = (bottom_group["death_rate"] > median_death).mean()
print("Share of lowest-rated hospitals with above-median death rate:", round(share_worse_bottom * 100), "%")