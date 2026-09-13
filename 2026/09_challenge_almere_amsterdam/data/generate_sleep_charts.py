import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
import re

DATA_DIR = r'C:\Users\marco\Documents\Research\racing\2026\09_challenge_almere_amsterdam\data'
OUTPUT   = r'C:\Users\marco\Documents\Research\racing\2026\09_challenge_almere_amsterdam\image'

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_hm(s):
    """Parse '7h 54min' (or '8h 4min') to total minutes."""
    m = re.match(r'(\d+)h\s*(\d+)min', s.strip())
    if not m:
        raise ValueError(f"Cannot parse duration: {s!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

# ── Load weekly sleep data (Sleep.csv is written newest-first; reverse to chronological) ──

with open(f'{DATA_DIR}/Sleep.csv', encoding='utf-8-sig') as f:
    reader = list(csv.DictReader(f))
reader.reverse()

labels   = [r['Date'] for r in reader]
scores   = [int(r['Avg Score']) for r in reader]
quality  = [r['Avg Quality'] for r in reader]
dur_min  = [parse_hm(r['Avg Duration']) for r in reader]
need_min = [parse_hm(r['Avg Sleep Need']) for r in reader]
dur_h    = [d / 60 for d in dur_min]
need_h   = [n / 60 for n in need_min]
x        = np.arange(len(reader))

# Month metadata for background bands: derive from each week's first token ("Jun 15-21" -> Jun)
month_order = []
month_start = {}
for i, lab in enumerate(labels):
    mon = lab.split()[0]
    if mon not in month_start:
        month_start[mon] = i
        month_order.append(mon)
month_meta = []
for i, mon in enumerate(month_order):
    start = month_start[mon]
    end = (month_start[month_order[i + 1]] - 1) if i + 1 < len(month_order) else len(labels) - 1
    month_meta.append((f"{mon} '26", start, end))
month_band_colors = ["#f8f9fa", "#eef2f7"]

quality_colors = {"Poor": "#e06c75", "Fair": "#e5c07b", "Good": "#98c379"}
bar_colors = [quality_colors[q] for q in quality]

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def add_month_bands(ax, meta, band_colors, ylim=None):
    """Draw alternating background bands and month labels."""
    for i, (name, start, end) in enumerate(meta):
        ax.axvspan(start - 0.5, end + 0.5, color=band_colors[i % 2], alpha=0.5, zorder=0)
        mid = (start + end) / 2
        y_pos = (ylim[0] + (ylim[1] - ylim[0]) * 0.03) if ylim else ax.get_ylim()[0]
        ax.text(mid, y_pos, name, ha="center", va="bottom", fontsize=7.5,
                color="#555", fontweight="bold", zorder=5)
    ax.set_xticks([])


# ── Chart 1: Sleep Score Trend ───────────────────────────────────────────────
score_lo, score_hi = min(scores) - 8, max(scores) + 8
fig, ax = plt.subplots(figsize=(12, 5))
add_month_bands(ax, month_meta, month_band_colors, ylim=(score_lo, score_hi))
ax.plot(x, scores, color="#61afef", linewidth=2, zorder=3)
ax.scatter(x, scores, c=bar_colors, s=60, zorder=4, edgecolors="white", linewidth=0.8)
avg = np.mean(scores)
ax.axhline(avg, color="#abb2bf", linewidth=1, linestyle="--", zorder=2)
ax.fill_between(x, scores, avg, alpha=0.08, color="#61afef", zorder=1)
ax.set_ylabel("Sleep Score")
ax.set_title("Weekly Sleep Score — Training Cycle (Jun–Sep 2026)", fontsize=13, pad=12)
ax.set_ylim(score_lo, score_hi)
ax.set_xlim(-0.5, len(reader) - 0.5)
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
fig, ax = plt.subplots(figsize=(12, 5))
add_month_bands(ax, month_meta, month_band_colors, ylim=(0, 10.5))
bw = 0.38
ax.bar(x - bw/2, dur_h,  width=bw, color="#61afef", label="Actual Duration", alpha=0.9, zorder=3)
ax.bar(x + bw/2, need_h, width=bw, color="#abb2bf", label="Sleep Need",      alpha=0.7, zorder=3)
ax.set_ylabel("Hours")
ax.set_title("Sleep Duration vs Sleep Need — Training Cycle (Jun–Sep 2026)", fontsize=13, pad=12)
ax.set_ylim(0, 10.5)
ax.set_xlim(-0.5, len(reader) - 0.5)
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
mx = np.arange(len(month_labels))

ax1.bar(mx, avg_score, color="#61afef", alpha=0.9, width=0.55)
for i, v in enumerate(avg_score):
    ax1.text(i, v + 0.5, f"{v:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax1.set_xticks(mx)
ax1.set_xticklabels(month_labels, fontsize=9)
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
ax2.set_xticklabels(month_labels, fontsize=9)
ax2.set_ylabel("Hours")
ax2.set_title("Monthly Avg Duration vs Need", fontsize=12, pad=10)
ax2.legend(frameon=False, fontsize=9)

fig.suptitle("Monthly Sleep Summary — Jun to Sep 2026", fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/sleep_monthly_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved sleep_monthly_summary.png")

# ── Print stats for README ────────────────────────────────────────────────────
print(f"\nTotal weeks:          {len(reader)}")
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
    print(f"  {name}: score {s:.1f}, duration {d//60:.0f}h{d%60:.0f}min, need {n//60:.0f}h{n%60:.0f}min, deficit {def_//60:.0f}h{def_%60:.0f}min")
