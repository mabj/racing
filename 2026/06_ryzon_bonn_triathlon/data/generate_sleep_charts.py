import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT = r'C:\Users\marco\Documents\Research\racing\2026\06_ryzon_bonn_triathlon\image'

# Jan 7 – Jun 2, 2026 (start-of-week order)
weeks = [
    ("Jan 7-13",        61, "Fair", 5*60+29, 8*60+40),
    ("Jan 14-20",       70, "Fair", 5*60+42, 8*60+23),
    ("Jan 21-27",       65, "Fair", 5*60+43, 8*60+40),
    ("Jan 28-Feb 3",    64, "Fair", 5*60+50, 8*60+11),
    ("Feb 4-10",        58, "Poor", 5*60+ 5, 9*60+ 0),
    ("Feb 11-17",       60, "Fair", 5*60+59, 8*60+54),
    ("Feb 18-24",       67, "Fair", 5*60+55, 8*60+44),
    ("Feb 25-Mar 3",    66, "Fair", 6*60+ 8, 8*60+40),
    ("Mar 4-10",        69, "Fair", 6*60+ 3, 8*60+57),
    ("Mar 11-17",       55, "Poor", 5*60+41, 8*60+51),
    ("Mar 18-24",       63, "Fair", 5*60+59, 9*60+ 0),
    ("Mar 25-31",       66, "Fair", 6*60+51, 8*60+27),
    ("Apr 1-7",         61, "Fair", 6*60+52, 8*60+39),
    ("Apr 8-14",        66, "Fair", 6*60+18, 8*60+54),
    ("Apr 15-21",       64, "Fair", 6*60+27, 8*60+53),
    ("Apr 22-28",       71, "Fair", 6*60+54, 8*60+30),
    ("Apr 29-May 5",    66, "Fair", 6*60+19, 8*60+49),
    ("May 6-12",        56, "Poor", 5*60+53, 8*60+57),
    ("May 13-19",       55, "Poor", 6*60+19, 8*60+44),
    ("May 20-26",       66, "Fair", 6*60+40, 8*60+27),
    ("May 27-Jun 2",    78, "Fair", 7*60+13, 8*60+20),
]

labels   = [w[0] for w in weeks]
scores   = [w[1] for w in weeks]
quality  = [w[2] for w in weeks]
dur_min  = [w[3] for w in weeks]
need_min = [w[4] for w in weeks]
dur_h    = [d / 60 for d in dur_min]
need_h   = [n / 60 for n in need_min]
x        = np.arange(len(weeks))

quality_colors = {"Poor": "#e06c75", "Fair": "#e5c07b", "Good": "#98c379"}
bar_colors = [quality_colors[q] for q in quality]

FONT = {"family": "DejaVu Sans"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})

# ── Chart 1: Sleep Score Trend ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(x, scores, color="#61afef", linewidth=2, zorder=3)
ax.scatter(x, scores, c=bar_colors, s=60, zorder=4, edgecolors="white", linewidth=0.8)
ax.axhline(np.mean(scores), color="#abb2bf", linewidth=1, linestyle="--", label=f"Avg {np.mean(scores):.0f}")
ax.fill_between(x, scores, np.mean(scores), alpha=0.08, color="#61afef")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Sleep Score")
ax.set_title("Weekly Sleep Score — Jan to Jun 2026", fontsize=13, pad=12)
ax.set_ylim(45, 90)
legend_patches = [
    mpatches.Patch(color=quality_colors["Poor"], label="Poor"),
    mpatches.Patch(color=quality_colors["Fair"], label="Fair"),
    mpatches.Patch(color="#abb2bf", label=f"Average ({np.mean(scores):.0f})"),
]
ax.legend(handles=legend_patches, loc="upper left", frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_score_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_score_trend.png")

# ── Chart 2: Duration vs Sleep Need (weekly) ─────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
w = 0.38
ax.bar(x - w/2, dur_h,  width=w, color="#61afef", label="Actual Duration", alpha=0.9)
ax.bar(x + w/2, need_h, width=w, color="#abb2bf", label="Sleep Need",      alpha=0.6)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Hours")
ax.set_title("Sleep Duration vs Sleep Need — Jan to Jun 2026", fontsize=13, pad=12)
ax.legend(frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_duration_vs_need.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_duration_vs_need.png")

# ── Chart 3: Monthly averages ─────────────────────────────────────────────────
months = ["Jan", "Feb", "Mar", "Apr", "May"]
monthly = {
    "Jan": [0, 1, 2, 3],
    "Feb": [4, 5, 6, 7],
    "Mar": [8, 9, 10, 11],
    "Apr": [12, 13, 14, 15, 16],
    "May": [17, 18, 19, 20],
}
avg_score = [np.mean([scores[i] for i in idx]) for idx in monthly.values()]
avg_dur   = [np.mean([dur_h[i]  for i in idx]) for idx in monthly.values()]
avg_need  = [np.mean([need_h[i] for i in idx]) for idx in monthly.values()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

mx = np.arange(len(months))
ax1.bar(mx, avg_score, color="#61afef", alpha=0.9, width=0.5)
for i, v in enumerate(avg_score):
    ax1.text(i, v + 0.5, f"{v:.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax1.set_xticks(mx); ax1.set_xticklabels(months)
ax1.set_ylim(0, 85)
ax1.set_ylabel("Average Score")
ax1.set_title("Monthly Avg Sleep Score", fontsize=12, pad=10)

w = 0.38
ax2.bar(mx - w/2, avg_dur,  width=w, color="#61afef", label="Actual", alpha=0.9)
ax2.bar(mx + w/2, avg_need, width=w, color="#abb2bf", label="Need",   alpha=0.6)
for i, (d, n) in enumerate(zip(avg_dur, avg_need)):
    ax2.text(i - w/2, d + 0.05, f"{d:.1f}h", ha="center", va="bottom", fontsize=8)
    ax2.text(i + w/2, n + 0.05, f"{n:.1f}h", ha="center", va="bottom", fontsize=8)
ax2.set_xticks(mx); ax2.set_xticklabels(months)
ax2.set_ylabel("Hours")
ax2.set_title("Monthly Avg Duration vs Need", fontsize=12, pad=10)
ax2.legend(frameon=False, fontsize=9)

fig.suptitle("Monthly Sleep Summary — Jan to May 2026", fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_monthly_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_monthly_summary.png")

# ── Print stats for README ────────────────────────────────────────────────────
print(f"\nOverall avg score:    {np.mean(scores):.1f}")
print(f"Overall avg duration: {np.mean(dur_h):.2f}h  ({np.mean(dur_min):.0f} min)")
print(f"Best week:  {labels[np.argmax(scores)]} ({max(scores)})")
print(f"Worst week: {labels[np.argmin(scores)]} ({min(scores)})")
print(f"Poor weeks: {quality.count('Poor')}/{len(quality)}")
print(f"Fair weeks: {quality.count('Fair')}/{len(quality)}")
print(f"Good weeks: {quality.count('Good')}/{len(quality)}")
print(f"\nMonthly avg scores: { {m: round(s,1) for m,s in zip(months, avg_score)} }")
print(f"Monthly avg duration: { {m: round(d,2) for m,d in zip(months, avg_dur)} }")
