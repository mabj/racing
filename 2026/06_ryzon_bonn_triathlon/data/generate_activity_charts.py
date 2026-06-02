import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
from collections import defaultdict

DATA_DIR = r'C:\Users\marco\Documents\Research\racing\2026\06_ryzon_bonn_triathlon\data'
OUTPUT   = r'C:\Users\marco\Documents\Research\racing\2026\06_ryzon_bonn_triathlon\image'

# ── Colours (consistent with sleep charts) ───────────────────────────────────
C_RUN   = "#98c379"   # green
C_BIKE  = "#e5c07b"   # yellow/orange
C_SWIM  = "#61afef"   # blue
C_AXIS  = "#abb2bf"
C_TEXT  = "#555"
BAND_COLORS = ["#f8f9fa", "#eef2f7"]

plt.rcParams.update({"font.family": "DejaVu Sans",
                     "axes.spines.top": False,
                     "axes.spines.right": False})

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_time_minutes(t):
    """Parse HH:MM:SS (or MM:SS) to float minutes."""
    if not t or t == '--':
        return 0.0
    parts = t.strip().split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + float(parts[2]) / 60
        if len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60
    except ValueError:
        pass
    return 0.0

def sport_category(activity_type):
    if activity_type == 'Running':
        return 'Running'
    if activity_type in ('Road Cycling', 'Virtual Cycling', 'Cycling'):
        return 'Cycling'
    if activity_type in ('Open Water Swimming', 'Pool Swim'):
        return 'Swimming'
    return None

# ── Load full activity data ───────────────────────────────────────────────────

rows = []
with open(f'{DATA_DIR}/activities_full_data.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        rows.append(row)

# Monthly hours per sport (all available months)
monthly_hours = defaultdict(lambda: defaultdict(float))
for r in rows:
    cat = sport_category(r['Activity Type'])
    if cat is None:
        continue
    month = r['Date'][:7]   # "YYYY-MM"
    monthly_hours[month][cat] += parse_time_minutes(r['Time']) / 60

# Training cycle months (Feb–Jun 2026)
CYCLE_MONTHS = ['2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
CYCLE_LABELS = ["Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26"]

# History months in chronological order
HISTORY_MONTHS = sorted(monthly_hours.keys())
HISTORY_LABELS = []
for m in HISTORY_MONTHS:
    y, mo = m.split('-')
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    short_y = y[2:]
    HISTORY_LABELS.append(f"{months[int(mo)-1]} '{short_y}")

# ── Chart 1: Monthly Training Hours — stacked bar (Feb–Jun 2026) ─────────────

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(CYCLE_MONTHS))
swim_h  = [monthly_hours[m]['Swimming'] for m in CYCLE_MONTHS]
bike_h  = [monthly_hours[m]['Cycling']  for m in CYCLE_MONTHS]
run_h   = [monthly_hours[m]['Running']  for m in CYCLE_MONTHS]

bars_swim = ax.bar(x, swim_h, color=C_SWIM,  label='Swimming', alpha=0.9, width=0.55)
bars_bike = ax.bar(x, bike_h, color=C_BIKE,  label='Cycling',  alpha=0.9, width=0.55, bottom=swim_h)
bars_run  = ax.bar(x, run_h,  color=C_RUN,   label='Running',  alpha=0.9, width=0.55,
                   bottom=[s + b for s, b in zip(swim_h, bike_h)])

# Total annotations
for i, (s, b, r) in enumerate(zip(swim_h, bike_h, run_h)):
    total = s + b + r
    if total > 0:
        ax.text(i, total + 0.3, f"{total:.1f}h", ha='center', va='bottom',
                fontsize=9, fontweight='bold', color='#333')

ax.set_xticks(x)
ax.set_xticklabels(CYCLE_LABELS, fontsize=10)
ax.set_ylabel("Hours")
ax.set_title("Monthly Training Hours — Feb to Jun 2026", fontsize=13, pad=12)
ax.legend(frameon=False, fontsize=9, loc='upper left')
ax.set_ylim(0, max(s + b + r for s, b, r in zip(swim_h, bike_h, run_h)) * 1.18)
ax.spines['left'].set_color(C_AXIS)
ax.spines['bottom'].set_color(C_AXIS)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/activity_monthly_hours.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved activity_monthly_hours.png")

# ── Chart 2: Full Year Training History — line chart ─────────────────────────

fig, ax = plt.subplots(figsize=(14, 5))

hx    = np.arange(len(HISTORY_MONTHS))
h_run  = [monthly_hours[m]['Running']  for m in HISTORY_MONTHS]
h_bike = [monthly_hours[m]['Cycling']  for m in HISTORY_MONTHS]
h_swim = [monthly_hours[m]['Swimming'] for m in HISTORY_MONTHS]

ax.plot(hx, h_run,  color=C_RUN,  linewidth=2.5, marker='o', ms=6, label='Running',  zorder=3)
ax.plot(hx, h_bike, color=C_BIKE, linewidth=2.5, marker='s', ms=6, label='Cycling',  zorder=3)
ax.plot(hx, h_swim, color=C_SWIM, linewidth=2.5, marker='^', ms=6, label='Swimming', zorder=3)

# Cycle-start marker
cycle_start_idx = HISTORY_MONTHS.index('2026-02')
ax.axvline(cycle_start_idx - 0.5, color='#e06c75', linewidth=1.5, linestyle='--',
           alpha=0.7, zorder=2)
ax.text(cycle_start_idx - 0.4, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 0 else 15,
        "training cycle start", color='#e06c75', fontsize=8, va='top', style='italic')

ax.set_xticks(hx)
ax.set_xticklabels(HISTORY_LABELS, rotation=30, ha='right', fontsize=9)
ax.set_ylabel("Hours per month")
ax.set_title("Training History — Sep 2025 to Jun 2026", fontsize=13, pad=12)
ax.legend(frameon=False, fontsize=9)
ax.spines['left'].set_color(C_AXIS)
ax.spines['bottom'].set_color(C_AXIS)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/activity_training_history.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved activity_training_history.png")

# ── Chart 3: Sport Distribution — donut chart (Feb–Jun 2026) ─────────────────

total_swim = sum(monthly_hours[m]['Swimming'] for m in CYCLE_MONTHS)
total_bike = sum(monthly_hours[m]['Cycling']  for m in CYCLE_MONTHS)
total_run  = sum(monthly_hours[m]['Running']  for m in CYCLE_MONTHS)

# Session counts (from the same data)
sess_swim = sum(1 for r in rows
                if r['Date'] >= '2026-02' and sport_category(r['Activity Type']) == 'Swimming')
sess_bike = sum(1 for r in rows
                if r['Date'] >= '2026-02' and sport_category(r['Activity Type']) == 'Cycling')
sess_run  = sum(1 for r in rows
                if r['Date'] >= '2026-02' and sport_category(r['Activity Type']) == 'Running')

sizes  = [total_swim, total_bike, total_run]
colors = [C_SWIM, C_BIKE, C_RUN]
labels = [
    f"Swimming\n{total_swim:.1f}h · {sess_swim} sessions",
    f"Cycling\n{total_bike:.1f}h · {sess_bike} sessions",
    f"Running\n{total_run:.1f}h · {sess_run} sessions",
]

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors, autopct='%1.0f%%',
    startangle=90, pctdistance=0.75, labeldistance=1.18,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
    textprops=dict(fontsize=9),
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight('bold')
    at.set_color('white')

ax.set_title("Sport Distribution — Training Cycle (Feb–Jun 2026)\n"
             f"Total: {total_swim+total_bike+total_run:.1f}h · {sess_swim+sess_bike+sess_run} sessions",
             fontsize=12, pad=16)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/activity_sport_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved activity_sport_distribution.png")

# ── Print summary stats ───────────────────────────────────────────────────────
print("\n=== Training cycle stats (Feb–Jun 2026) ===")
total_min = (total_swim + total_bike + total_run) * 60
weeks = 18.1
print(f"  Swimming : {sess_swim:2d} sessions | {total_swim*60:5.0f} min | {total_swim:.1f}h")
print(f"  Cycling  : {sess_bike:2d} sessions | {total_bike*60:5.0f} min | {total_bike:.1f}h")
print(f"  Running  : {sess_run:2d} sessions | {total_run*60:5.0f} min | {total_run:.1f}h")
print(f"  All      : {sess_swim+sess_bike+sess_run:2d} sessions | {total_min:5.0f} min | {(total_swim+total_bike+total_run):.1f}h")
print(f"  Avg/week : {(total_swim+total_bike+total_run)/weeks:.1f}h/week over {weeks:.0f} weeks")
