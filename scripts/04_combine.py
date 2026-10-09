import pandas as pd

hosp = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype=str)
ratings = pd.read_csv("data/clean/patient_ratings.csv", dtype={"Facility ID": str})
deaths = pd.read_csv("data/clean/death_rate.csv", dtype={"Facility ID": str})
readmits = pd.read_csv("data/clean/hf_readmit_rate.csv", dtype={"Facility ID": str})

# keep regulular acute care hospitals only
hosp = hosp[hosp["Hospital Type"] == "Acute Care Hospitals"]
hosp = hosp[["Facility ID", "Facility Name", "City/Town", "State",
             "County/Parish", "Hospital overall rating"]]

# flag DFW hospitals
dfw_counties = ["COLLIN", "DALLAS", "DENTON", "ELLIS", "HUNT", "JOHNSON",
                "KAUFMAN", "PARKER", "ROCKWALL", "TARRANT", "WISE"]
hosp["dfw"] = (hosp["State"] == "TX") & (hosp["County/Parish"].str.upper().isin(dfw_counties))

# join everything onto the hospital list
combined = hosp.merge(ratings, on="Facility ID", how="left")
combined = combined.merge(deaths, on="Facility ID", how="left")
combined = combined.merge(readmits, on="Facility ID", how="left")

print("Acute care hospitals:", len(combined))
print(combined.isna().sum())

combined.to_csv("data/clean/hospitals_combined.csv", index=False)