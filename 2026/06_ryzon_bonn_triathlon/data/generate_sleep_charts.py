import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT = r'C:\Users\marco\Documents\Research\racing\2026\06_ryzon_bonn_triathlon\image'

# Sep 3, 2025 – Jun 2, 2026 (chronological order)
weeks = [
    # ── Sep 2025 ──────────────────────────────────────────────────────────────
    ("Sep 3-9",         82, "Good", 7*60+38, 8*60+ 7),
    ("Sep 10-16",       78, "Fair", 7*60+22, 8*60+ 6),
    ("Sep 17-23",       83, "Good", 7*60+54, 7*60+39),
    ("Sep 24-30",       87, "Good", 8*60+ 3, 7*60+33),
    # ── Oct 2025 ──────────────────────────────────────────────────────────────
    ("Oct 1-7",         78, "Fair", 7*60+14, 8*60+ 0),
    ("Oct 8-14",        66, "Fair", 7*60+22, 8*60+21),
    ("Oct 15-21",       78, "Fair", 7*60+20, 8*60+16),
    ("Oct 22-28",       82, "Good", 7*60+32, 7*60+23),
    ("Oct 29-Nov 4",    82, "Good", 7*60+42, 8*60+ 0),
    # ── Nov 2025 ──────────────────────────────────────────────────────────────
    ("Nov 5-11",        77, "Fair", 7*60+45, 7*60+43),
    ("Nov 12-18",       74, "Fair", 6*60+53, 8*60+ 0),
    ("Nov 19-25",       48, "Poor", 3*60+42, 8*60+13),
    ("Nov 26-Dec 2",    61, "Fair", 5*60+52, 8*60+17),
    # ── Dec 2025 ──────────────────────────────────────────────────────────────
    ("Dec 3-9",         57, "Poor", 5*60+14, 8*60+44),
    ("Dec 10-16",       65, "Fair", 6*60+12, 8*60+53),
    ("Dec 17-23",       63, "Fair", 5*60+44, 8*60+49),
    ("Dec 24-30",       62, "Fair", 5*60+39, 8*60+40),
    ("Dec 31-Jan 6",    54, "Poor", 5*60+11, 8*60+49),
    # ── Jan 2026 ──────────────────────────────────────────────────────────────
    ("Jan 7-13",        61, "Fair", 5*60+29, 8*60+40),
    ("Jan 14-20",       70, "Fair", 5*60+42, 8*60+23),
    ("Jan 21-27",       65, "Fair", 5*60+43, 8*60+40),
    ("Jan 28-Feb 3",    64, "Fair", 5*60+50, 8*60+11),
    # ── Feb 2026 ──────────────────────────────────────────────────────────────
    ("Feb 4-10",        58, "Poor", 5*60+ 5, 9*60+ 0),
    ("Feb 11-17",       60, "Fair", 5*60+59, 8*60+54),
    ("Feb 18-24",       67, "Fair", 5*60+55, 8*60+44),
    ("Feb 25-Mar 3",    66, "Fair", 6*60+ 8, 8*60+40),
    # ── Mar 2026 ──────────────────────────────────────────────────────────────
    ("Mar 4-10",        69, "Fair", 6*60+ 3, 8*60+57),
    ("Mar 11-17",       55, "Poor", 5*60+41, 8*60+51),
    ("Mar 18-24",       63, "Fair", 5*60+59, 9*60+ 0),
    ("Mar 25-31",       66, "Fair", 6*60+51, 8*60+27),
    # ── Apr 2026 ──────────────────────────────────────────────────────────────
    ("Apr 1-7",         61, "Fair", 6*60+52, 8*60+39),
    ("Apr 8-14",        66, "Fair", 6*60+18, 8*60+54),
    ("Apr 15-21",       64, "Fair", 6*60+27, 8*60+53),
    ("Apr 22-28",       71, "Fair", 6*60+54, 8*60+30),
    ("Apr 29-May 5",    66, "Fair", 6*60+19, 8*60+49),
    # ── May 2026 ──────────────────────────────────────────────────────────────
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

# Month metadata: label, first week index, last week index
month_meta = [
    ("Sep '25",  0,  3),
    ("Oct '25",  4,  8),
    ("Nov '25",  9, 12),
    ("Dec '25", 13, 17),
    ("Jan '26", 18, 21),
    ("Feb '26", 22, 25),
    ("Mar '26", 26, 29),
    ("Apr '26", 30, 34),
    ("May '26", 35, 38),
]
month_band_colors = ["#f8f9fa", "#eef2f7"]

quality_colors = {"Poor": "#e06c75", "Fair": "#e5c07b", "Good": "#98c379"}
bar_colors = [quality_colors[q] for q in quality]

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def add_month_bands(ax, meta, band_colors, y_label=True, ylim=None):
    """Draw alternating background bands and month labels."""
    for i, (name, start, end) in enumerate(meta):
        ax.axvspan(start - 0.5, end + 0.5, color=band_colors[i % 2], alpha=0.5, zorder=0)
        mid = (start + end) / 2
        y_pos = (ylim[0] + (ylim[1] - ylim[0]) * 0.03) if ylim else ax.get_ylim()[0]
        ax.text(mid, y_pos, name, ha="center", va="bottom", fontsize=7.5,
                color="#555", fontweight="bold", zorder=5)
    ax.set_xticks([])


# ── Chart 1: Sleep Score Trend ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 5))
add_month_bands(ax, month_meta, month_band_colors, ylim=(40, 95))
ax.plot(x, scores, color="#61afef", linewidth=2, zorder=3)
ax.scatter(x, scores, c=bar_colors, s=60, zorder=4, edgecolors="white", linewidth=0.8)
avg = np.mean(scores)
ax.axhline(avg, color="#abb2bf", linewidth=1, linestyle="--", zorder=2)
ax.fill_between(x, scores, avg, alpha=0.08, color="#61afef", zorder=1)
ax.set_ylabel("Sleep Score")
ax.set_title("Weekly Sleep Score — Sep 2025 to Jun 2026", fontsize=13, pad=12)
ax.set_ylim(40, 95)
ax.set_xlim(-0.5, len(weeks) - 0.5)
legend_patches = [
    mpatches.Patch(color=quality_colors["Good"], label="Good"),
    mpatches.Patch(color=quality_colors["Fair"], label="Fair"),
    mpatches.Patch(color=quality_colors["Poor"], label="Poor"),
    mpatches.Patch(color="#abb2bf", label=f"Average ({avg:.0f})"),
]
ax.legend(handles=legend_patches, loc="upper right", frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_score_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_score_trend.png")

# ── Chart 2: Duration vs Sleep Need (weekly) ─────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 5))
add_month_bands(ax, month_meta, month_band_colors, ylim=(0, 10.5))
bw = 0.38
ax.bar(x - bw/2, dur_h,  width=bw, color="#61afef", label="Actual Duration", alpha=0.9, zorder=3)
ax.bar(x + bw/2, need_h, width=bw, color="#abb2bf", label="Sleep Need",      alpha=0.7, zorder=3)
ax.set_ylabel("Hours")
ax.set_title("Sleep Duration vs Sleep Need — Sep 2025 to Jun 2026", fontsize=13, pad=12)
ax.set_ylim(0, 10.5)
ax.set_xlim(-0.5, len(weeks) - 0.5)
ax.legend(frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_duration_vs_need.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_duration_vs_need.png")

# ── Chart 3: Monthly averages ─────────────────────────────────────────────────
month_labels = [m[0] for m in month_meta]
monthly_indices = {m[0]: list(range(m[1], m[2] + 1)) for m in month_meta}

avg_score = [np.mean([scores[i] for i in idx]) for idx in monthly_indices.values()]
avg_dur   = [np.mean([dur_h[i]  for i in idx]) for idx in monthly_indices.values()]
avg_need  = [np.mean([need_h[i] for i in idx]) for idx in monthly_indices.values()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
mx = np.arange(len(month_labels))

ax1.bar(mx, avg_score, color="#61afef", alpha=0.9, width=0.55)
for i, v in enumerate(avg_score):
    ax1.text(i, v + 0.5, f"{v:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax1.set_xticks(mx)
ax1.set_xticklabels(month_labels, rotation=30, ha="right", fontsize=9)
ax1.set_ylim(0, 95)
ax1.set_ylabel("Average Score")
ax1.set_title("Monthly Avg Sleep Score", fontsize=12, pad=10)

bw = 0.38
ax2.bar(mx - bw/2, avg_dur,  width=bw, color="#61afef", label="Actual", alpha=0.9)
ax2.bar(mx + bw/2, avg_need, width=bw, color="#abb2bf", label="Need",   alpha=0.7)
for i, (d, n) in enumerate(zip(avg_dur, avg_need)):
    ax2.text(i - bw/2, d + 0.05, f"{d:.1f}h", ha="center", va="bottom", fontsize=8)
    ax2.text(i + bw/2, n + 0.05, f"{n:.1f}h", ha="center", va="bottom", fontsize=8)
ax2.set_xticks(mx)
ax2.set_xticklabels(month_labels, rotation=30, ha="right", fontsize=9)
ax2.set_ylabel("Hours")
ax2.set_title("Monthly Avg Duration vs Need", fontsize=12, pad=10)
ax2.legend(frameon=False, fontsize=9)

fig.suptitle("Monthly Sleep Summary — Sep 2025 to May 2026", fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_monthly_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_monthly_summary.png")

# ── Print stats for README ────────────────────────────────────────────────────
print(f"\nTotal weeks:          {len(weeks)}")
print(f"Overall avg score:    {np.mean(scores):.1f}")
print(f"Overall avg duration: {np.mean(dur_h):.2f}h  ({np.mean(dur_min):.0f} min)")
deficit_h = np.mean(need_h) - np.mean(dur_h)
print(f"Overall avg deficit:  {deficit_h:.2f}h  ({deficit_h*60:.0f} min)")
print(f"Best week:  {labels[int(np.argmax(scores))]} ({max(scores)})")
print(f"Worst week: {labels[int(np.argmin(scores))]} ({min(scores)})")
print(f"Good weeks: {quality.count('Good')}/{len(quality)}")
print(f"Fair weeks: {quality.count('Fair')}/{len(quality)}")
print(f"Poor weeks: {quality.count('Poor')}/{len(quality)}")
print("\nMonthly breakdown:")
for name, idx in monthly_indices.items():
    s = np.mean([scores[i] for i in idx])
    d = np.mean([dur_min[i] for i in idx])
    n = np.mean([need_min[i] for i in idx])
    def_ = n - d
    print(f"  {name}: score {s:.1f}, duration {d//60:.0f}h{d%60:.0f}min, deficit {def_//60:.0f}h{def_%60:.0f}min")
