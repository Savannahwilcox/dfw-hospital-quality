# Bar chart of the share of each DFW health system's hospitals that CMS
# rates better than national on at least one 30-day mortality measure.

import pandas as pd
import matplotlib.pyplot as plt

FONT = ["Avenir Next", "Helvetica Neue", "Arial"]
INK = "#1f2a36"
MUTED = "#7d8794"
ACCENT = "#b5432c"
LIGHT = "#c9ced4"
GRID = "#e6e8eb"
SOURCE = "Source: CMS Care Compare, 2026 release. DFW acute care hospitals with 3+ CMS mortality measures. System assigned by facility name."

plt.rcParams["font.family"] = FONT
plt.rcParams["text.color"] = INK
plt.rcParams["xtick.color"] = MUTED
plt.rcParams["ytick.color"] = INK


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
    return "All other"


df = pd.read_csv("data/clean/mortality_compare.csv", dtype={"Facility ID": str})
dfw = df[df["dfw"]].copy()
dfw["system"] = dfw["Facility Name"].apply(system)
dfw["rated_better"] = dfw["old_rating"].isin(["Better on 1+", "Mixed"])

summary = dfw.groupby("system").agg(
    hospitals=("system", "size"),
    rated_better=("rated_better", "sum"),
    pct_9_10=("pct_9_10", "mean"),
)
summary["share"] = summary["rated_better"] / summary["hospitals"] * 100
summary = summary.sort_values("share")

fig, ax = plt.subplots(figsize=(9, 5))
fig.subplots_adjust(top=0.78, bottom=0.14, left=0.30, right=0.80)

colors = [ACCENT if s == "Baylor Scott & White" else LIGHT for s in summary.index]
ax.barh(summary.index, summary["share"], color=colors, height=0.55)

for i, row in enumerate(summary.itertuples()):
    ax.text(row.share + 1.5, i, f"{row.rated_better:.0f} of {row.hospitals}",
            va="center", fontsize=10, color=INK)
    ax.text(103, i, f"{row.pct_9_10:.0f}%", va="center", ha="left", fontsize=10, color=MUTED)

ax.text(103, len(summary) - 0.4, "Patients rating\n9 or 10", fontsize=8.5, color=MUTED, ha="left", va="bottom")

ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100%"])
ax.tick_params(length=0)
for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
ax.xaxis.grid(True, color=GRID, linewidth=1)
ax.set_axisbelow(True)

fig.text(0.04, 0.93, "Share of DFW hospitals CMS rates better than national on death rates",
         fontsize=14, fontweight="bold", ha="left")
fig.text(0.04, 0.88, "Better than national on at least one of CMS's death rate measures",
         fontsize=10, color=MUTED, ha="left")
fig.text(0.04, 0.03, SOURCE, fontsize=7.5, color=MUTED, ha="left")

plt.savefig("charts/dfw_systems_mortality.png", dpi=200)
plt.close()
print("Saved charts/dfw_systems_mortality.png")