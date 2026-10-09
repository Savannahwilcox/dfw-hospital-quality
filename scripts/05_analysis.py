# tests whether hospitals that patients rate highly also have better
# outcomes (lower death and readmission rates). Uses every US acute
# care hospital that has both numbers

import pandas as pd

df = pd.read_csv("data/clean/hospitals_combined.csv", dtype={"Facility ID": str})


def compare_by_rating(df, outcome):
    # only keep hospitals that have both a patient rating and this outcome
    both = df.dropna(subset=["pct_9_10", outcome]).copy()

    # split hospitals into 5 equal sized groups by patient rating
    both["rating_group"] = pd.qcut(both["pct_9_10"], 5,
                                   labels=["1 lowest", "2", "3", "4", "5 highest"])

    # average outcome for each rating group
    summary = both.groupby("rating_group", observed=True).agg(
        hospitals=("pct_9_10", "size"),
        rating_low=("pct_9_10", "min"),
        rating_high=("pct_9_10", "max"),
        avg_outcome=(outcome, "mean"),
    )
    print("\n------", outcome, "------")
    print(summary.round(2))

    # compare how often the top and bottom
    # groups land on the worse side of the national median
    median = both[outcome].median()
    top = both[both["rating_group"] == "5 highest"]
    bottom = both[both["rating_group"] == "1 lowest"]

    print("National median:", median)
    print("Top-rated above median:", round((top[outcome] > median).mean() * 100), "%")
    print("Lowest-rated above median:", round((bottom[outcome] > median).mean() * 100), "%")


compare_by_rating(df, "death_rate")
compare_by_rating(df, "hf_readmit_rate")
