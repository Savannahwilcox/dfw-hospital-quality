import pandas as pd 

hosp = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype=str)

dfw_counties = ["COLLIN", "DALLAS", "DENTON", "ELLIS", "HUNT", "JOHNSON",
 "KAUFMAN", "PARKER", "ROCKWALL", "TARRANT", "WISE"]

dfw = hosp[
    (hosp["State"] == "TX")
    & (hosp["County/Parish"].str.upper().isin(dfw_counties))
    & (hosp["Hospital Type"] == "Acute Care Hospitals")
]

print("DFW acute care hospitals:", len(dfw))
print(dfw["Hospital overall rating"].value_counts())

no_rating = dfw[dfw["Hospital overall rating"] == "Not Available"]
print(no_rating["Facility Name"].tolist())