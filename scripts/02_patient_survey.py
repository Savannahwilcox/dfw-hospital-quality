import pandas as pd
pd.set_option("display.width", 200)

survey = pd.read_csv("data/raw/HCAHPS-Hospital.csv", dtype=str)

print("Rows:", len(survey))
print("Unique hospitals:", survey["Facility ID"].nunique())

rating = survey[survey["HCAHPS Measure ID"] == "H_HSP_RATING_9_10"]
rating = rating[["Facility ID", "HCAHPS Answer Percent", "Number of Completed Surveys"]]

print(rating.head())
print("Hospitals:", len(rating))
print(rating["HCAHPS Answer Percent"].value_counts().head(10))

rating["pct_9_10"] = pd.to_numeric(rating["HCAHPS Answer Percent"], errors="coerce")
rating["surveys"] = pd.to_numeric(rating["Number of Completed Surveys"], errors="coerce")

rating = rating[rating["surveys"] >= 100]
rating = rating[["Facility ID", "pct_9_10", "surveys"]]

print("Hospitals with 100+ surveys:", len(rating))
print(rating["pct_9_10"].describe())

rating.to_csv("data/clean/patient_ratings.csv", index=False)

