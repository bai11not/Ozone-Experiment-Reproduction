#!/usr/bin/env python
# ============================================================
# Week 2 Person C: 图表生成
# 用法: python generate_figures.py
# ============================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

# ---------- 中文字体 ----------
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# ============================================================
# 数据
# ============================================================

# Per-step RMSE (pre_len=6) — 修正版
steps = [1, 2, 3, 4, 5, 6]
per_step_rmse = {
    "s52-full-l12-p6":      [6.82, 9.24, 10.98, 12.26, 13.26, 14.32],
    "s52-full-l24-p6":      [6.89, 9.20, 10.60, 11.76, 12.67, 13.58],
    "s52-nodiff-l12-p6":    [6.51, 8.96, 10.66, 12.05, 13.19, 14.11],
    "s52-nodiff-l24-p6":    [7.09, 9.31, 10.72, 11.76, 12.66, 13.50],
    "s62-full-l12-p6":      [8.76, 10.40, 11.81, 12.82, 14.07, 15.20],
    "s62-full-l24-p6":      [8.56, 10.30, 11.39, 12.12, 13.03, 13.88],
    "s62-nodiff-l12-p6":    [6.36, 8.86, 10.62, 12.03, 13.10, 13.96],
    "s62-nodiff-l24-p6":    [6.60, 8.91, 10.36, 11.43, 12.30, 13.12],
}

# 消融对比 (full vs no_diff, p=6)
ablation_labels = ["l=12,p=6,s52", "l=24,p=6,s52", "l=12,p=6,s62", "l=24,p=6,s62"]
full_rmse  = [11.43, 11.01, 12.37, 11.68]
nodiff_rmse = [11.22, 11.05, 11.13, 10.68]

# 综合排名 (16 groups)
ranking_data = [
    ("C12 s62,full,l=24,p=3", 8.56),
    ("C10 s62,full,l=12,p=3", 8.72),
    ("C16 s62,nodiff,l=24,p=3", 8.79),
    ("C08 s52,nodiff,l=24,p=3", 8.79),
    ("C02 s52,full,l=12,p=3", 8.80),
    ("C04 s52,full,l=24,p=3", 8.80),
    ("C14 s62,nodiff,l=12,p=3", 8.83),
    ("C06 s52,nodiff,l=12,p=3", 9.14),
    ("C15 s62,nodiff,l=24,p=6", 10.68),
    ("C03 s52,full,l=24,p=6", 11.01),
    ("C07 s52,nodiff,l=24,p=6", 11.05),
    ("C13 s62,nodiff,l=12,p=6", 11.13),
    ("C05 s52,nodiff,l=12,p=6", 11.22),
    ("C01 s52,full,l=12,p=6", 11.43),
    ("C11 s62,full,l=24,p=6", 11.68),
    ("C09 s62,full,l=12,p=6", 12.37),
]

# 种子稳定性
seed_stability = [
    ("full,l=12,p=6", 11.43, 12.37),
    ("full,l=12,p=3", 8.80, 8.72),
    ("full,l=24,p=6", 11.01, 11.68),
    ("full,l=24,p=3", 8.80, 8.56),
    ("nodiff,l=12,p=6", 11.22, 11.13),
    ("nodiff,l=12,p=3", 9.14, 8.83),
    ("nodiff,l=24,p=6", 11.05, 10.68),
    ("nodiff,l=24,p=3", 8.79, 8.79),
]

# ============================================================
# Figure 1: Per-Step RMSE (pre_len=6)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

colors_s52 = {"full": "#2196F3", "no_diff": "#FF9800"}
colors_s62 = {"full": "#1565C0", "no_diff": "#E65100"}
linestyles = {"l=12": "--", "l=24": "-"}

# seed=52
ax = axes[0]
for label, rmse_vals in per_step_rmse.items():
    if "s52" not in label:
        continue
    parts = label.split("-")
    abl = "full" if "full" in label else "no_diff"
    sl = "l=12" if "l12" in label else "l=24"
    ls = linestyles[sl]
    c = colors_s52[abl]
    ax.plot(steps, rmse_vals, marker="o", linestyle=ls, color=c, linewidth=1.8,
            markersize=6, label=f"{abl}, {sl}")
ax.set_xlabel("Prediction Step", fontsize=12)
ax.set_ylabel("RMSE", fontsize=12)
ax.set_title("Per-Step RMSE — seed=52 (pre_len=6)", fontsize=13, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xticks(steps)

# seed=62
ax = axes[1]
for label, rmse_vals in per_step_rmse.items():
    if "s62" not in label:
        continue
    parts = label.split("-")
    abl = "full" if "full" in label else "no_diff"
    sl = "l=12" if "l12" in label else "l=24"
    ls = linestyles[sl]
    c = colors_s62[abl]
    ax.plot(steps, rmse_vals, marker="s", linestyle=ls, color=c, linewidth=1.8,
            markersize=6, label=f"{abl}, {sl}")
ax.set_xlabel("Prediction Step", fontsize=12)
ax.set_ylabel("RMSE", fontsize=12)
ax.set_title("Per-Step RMSE — seed=62 (pre_len=6)", fontsize=13, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xticks(steps)

plt.tight_layout()
fig.savefig(OUT / "per_step_rmse_prelen6.png", dpi=200, bbox_inches="tight")
plt.close()
print("[OK] per_step_rmse_prelen6.png")

# ============================================================
# Figure 2: Ablation Comparison (full vs no_diff, p=6)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(ablation_labels))
w = 0.35
bars1 = ax.bar(x - w/2, full_rmse, w, label="full (with diffusion)", color="#2196F3", edgecolor="black", linewidth=0.5)
bars2 = ax.bar(x + w/2, nodiff_rmse, w, label="no_diff (without diffusion)", color="#FF9800", edgecolor="black", linewidth=0.5)

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, f"{bar.get_height():.2f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold")
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, f"{bar.get_height():.2f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_ylabel("RMSE", fontsize=12)
ax.set_title("Ablation: Diffusion Module Contribution (pre_len=6)", fontsize=14, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(ablation_labels, fontsize=10)
ax.legend(fontsize=11)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, max(full_rmse + nodiff_rmse) * 1.15)

plt.tight_layout()
fig.savefig(OUT / "ablation_comparison.png", dpi=200, bbox_inches="tight")
plt.close()
print("[OK] ablation_comparison.png")

# ============================================================
# Figure 3: Comprehensive Ranking (16 experiments)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6.5))
labels = [r[0] for r in reversed(ranking_data)]
values = [r[1] for r in reversed(ranking_data)]

# Color by pre_len
colors = []
for label in labels:
    if "p=3" in label:
        colors.append("#4CAF50")  # green for p=3
    else:
        colors.append("#F44336")  # red for p=6

bars = ax.barh(range(len(labels)), values, height=0.7, color=colors, edgecolor="black", linewidth=0.3)

for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height()/2, f"{val:.2f}",
            va="center", fontsize=9, fontweight="bold")

ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels, fontsize=8.5, fontfamily="monospace")
ax.set_xlabel("RMSE", fontsize=12)
ax.set_title("Person C — 16 Experiments Ranking (lower is better)", fontsize=14, fontweight="bold")
ax.set_xlim(0, max(values) * 1.12)
ax.grid(axis="x", alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor="#4CAF50", label="pre_len=3 (short prediction)"),
                   Patch(facecolor="#F44336", label="pre_len=6 (long prediction)")]
ax.legend(handles=legend_elements, fontsize=10, loc="lower right")

plt.tight_layout()
fig.savefig(OUT / "comprehensive_ranking.png", dpi=200, bbox_inches="tight")
plt.close()
print("[OK] comprehensive_ranking.png")

# ============================================================
# Figure 4: Seed Stability Scatter
# ============================================================
fig, ax = plt.subplots(figsize=(9, 7))

configs = [s[0] for s in seed_stability]
s52_vals = [s[1] for s in seed_stability]
s62_vals = [s[2] for s in seed_stability]

# Color by pre_len
pt_colors = ["#F44336" if "p=6" in c else "#4CAF50" for c in configs]
# Marker by ablation
markers = ["o" if "full" in c else "s" for c in configs]

for i, (cfg, s52, s62) in enumerate(seed_stability):
    ax.scatter(s52, s62, c=pt_colors[i], marker=markers[i], s=120, edgecolors="black", linewidth=0.5, zorder=5)
    ax.annotate(cfg.replace(",", "\n"), (s52, s62), textcoords="offset points",
                xytext=(8, 5), fontsize=7, alpha=0.85)

# Diagonal line (perfect stability)
mi = min(min(s52_vals), min(s62_vals)) - 0.3
ma = max(max(s52_vals), max(s62_vals)) + 0.3
ax.plot([mi, ma], [mi, ma], "k--", alpha=0.3, linewidth=1, label="perfect stability")

ax.set_xlabel("seed=52 RMSE", fontsize=12)
ax.set_ylabel("seed=62 RMSE", fontsize=12)
ax.set_title("Seed Stability: seed=52 vs seed=62", fontsize=14, fontweight="bold")
ax.grid(alpha=0.3)
ax.set_xlim(mi, ma)
ax.set_ylim(mi, ma)
ax.set_aspect("equal")

# Legend
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
leg = [Patch(facecolor="#4CAF50", label="pre_len=3"),
       Patch(facecolor="#F44336", label="pre_len=6"),
       Line2D([0], [0], marker="o", color="w", markerfacecolor="gray", markersize=10, label="full"),
       Line2D([0], [0], marker="s", color="w", markerfacecolor="gray", markersize=10, label="no_diff")]
ax.legend(handles=leg, fontsize=9, loc="upper left")

plt.tight_layout()
fig.savefig(OUT / "seed_stability.png", dpi=200, bbox_inches="tight")
plt.close()
print("[OK] seed_stability.png")

# ============================================================
# Figure 5: pre_len Effect (p=6 vs p=3)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
categories = ["full\nl=12", "full\nl=24", "nodiff\nl=12", "nodiff\nl=24"]
p6_s52 = [11.43, 11.01, 11.22, 11.05]
p3_s52 = [8.80, 8.80, 9.14, 8.79]
p6_s62 = [12.37, 11.68, 11.13, 10.68]
p3_s62 = [8.72, 8.56, 8.83, 8.79]

x = np.arange(len(categories))
w = 0.2
ax.bar(x - 1.5*w, p6_s52, w, label="p=6, s52", color="#F44336", edgecolor="black", linewidth=0.3)
ax.bar(x - 0.5*w, p6_s62, w, label="p=6, s62", color="#FF8A80", edgecolor="black", linewidth=0.3)
ax.bar(x + 0.5*w, p3_s52, w, label="p=3, s52", color="#4CAF50", edgecolor="black", linewidth=0.3)
ax.bar(x + 1.5*w, p3_s62, w, label="p=3, s62", color="#81C784", edgecolor="black", linewidth=0.3)

ax.set_ylabel("RMSE", fontsize=12)
ax.set_title("pre_len Effect: p=6 vs p=3", fontsize=14, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10)
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
fig.savefig(OUT / "prelen_effect.png", dpi=200, bbox_inches="tight")
plt.close()
print("[OK] prelen_effect.png")

print(f"\nAll figures saved to: {OUT}")
