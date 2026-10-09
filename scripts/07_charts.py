import pandas as pd
import matplotlib.pyplot as plt

FONT = ["Avenir Next", "Helvetica Neue", "Arial"]
INK = "#1f2a36"
MUTED = "#7d8794"
ACCENT = "#b5432c"
LIGHT = "#c9ced4"
GRID = "#e6e8eb"
SOURCE = "Source: CMS Care Compare, 2026 release. US acute care hospitals with 100+ patient surveys."

plt.rcParams["font.family"] = FONT
plt.rcParams["text.color"] = INK
plt.rcParams["axes.labelcolor"] = MUTED
plt.rcParams["xtick.color"] = MUTED
plt.rcParams["ytick.color"] = MUTED


def clean_axes(ax):
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(LIGHT)
    ax.tick_params(length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)


def add_titles(fig, title, subtitle):
    fig.text(0.06, 0.95, title, fontsize=15, fontweight="bold", ha="left")
    fig.text(0.06, 0.905, subtitle, fontsize=10.5, color=MUTED, ha="left")
    fig.text(0.06, 0.02, SOURCE, fontsize=8, color=MUTED, ha="left")


df = pd.read_csv("data/clean/hospitals_combined.csv", dtype={"Facility ID": str})
both = df.dropna(subset=["pct_9_10", "death_rate"]).copy()
median_death = both["death_rate"].median()

both["rating_group"] = pd.qcut(both["pct_9_10"], 5,
                               labels=["Lowest\nrated", "2", "3", "4", "Highest\nrated"])
both["above_median"] = both["death_rate"] > median_death
share = both.groupby("rating_group", observed=True)["above_median"].mean() * 100

fig, ax = plt.subplots(figsize=(8, 5.5))
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.08, right=0.97)
ax.bar(share.index.astype(str), share.values, color=INK, width=0.55)
for i, v in enumerate(share.values):
    ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=11, color=INK)
ax.set_ylim(0, 80)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_yticklabels(["0", "20", "40", "60", "80%"])
clean_axes(ax)
add_titles(fig,
           "Share of hospitals with an above-median death rate",
           "US hospitals split into five equal groups by patient rating")
plt.savefig("charts/national_rating_groups.png", dpi=200)
plt.close()

dfw = both[both["dfw"]]

labels = {
    "450015": ("Parkland", (-8, 4), "right"),
    "450021": ("Baylor University Medical Center", (-8, -14), "right"),
    "450044": ("UT Southwestern", (8, -4), "left"),
    "450135": ("Texas Health Fort Worth", (8, 4), "left"),
    "670132": ("Methodist Southlake", (-8, -24), "right"),
    "670060": ("Baylor Scott & White Sunnyvale", (8, -4), "left"),
}

fig, ax = plt.subplots(figsize=(9, 6.5))
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.97)
ax.scatter(dfw["pct_9_10"], dfw["death_rate"], s=45, color=LIGHT, edgecolor="white", linewidth=0.8)

for fid, (name, offset, side) in labels.items():
    row = dfw[dfw["Facility ID"] == fid]
    if len(row) == 0:
        continue
    x, y = row["pct_9_10"].iloc[0], row["death_rate"].iloc[0]
    ax.scatter(x, y, s=60, color=ACCENT, edgecolor="white", linewidth=0.8, zorder=3)
    ax.annotate(name, (x, y), xytext=offset, textcoords="offset points",
                fontsize=9, color=INK, ha=side)

ax.axhline(median_death, color=MUTED, linestyle=(0, (3, 3)), linewidth=1)
ax.text(ax.get_xlim()[0] + 0.3, median_death + 0.06, "US median", fontsize=8.5, color=MUTED, ha="left")
ax.set_xlabel("% of patients who rated the hospital 9 or 10 out of 10")
ax.set_ylabel("Hospital-wide 30-day death rate (%)")
clean_axes(ax)
add_titles(fig,
           "DFW hospitals: patient ratings vs. death rates",
           "Each dot is one hospital. Lower on the chart means fewer patients died within 30 days.")
plt.savefig("charts/dfw_scatter.png", dpi=200)
plt.close()

print("Charts saved to the charts folder")