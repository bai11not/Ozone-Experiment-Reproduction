#!/usr/bin/env python
# ============================================================
# Week 2: Person C 消融实验结果合并 (seed=52 + seed=62)
# 用法: python result_combine.py
# ============================================================
import json
import csv
from pathlib import Path

ROOT = Path("d:/桌面/臭氧预测资料/臭氧预测资料")
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

EXPERIMENTS = [
    # seed=52 (C01-C08)
    ("C01", 52, 12, 6, 1, 1, 1, "s52-full-l12-p6"),
    ("C02", 52, 12, 3, 1, 1, 1, "s52-full-l12-p3"),
    ("C03", 52, 24, 6, 1, 1, 1, "s52-full-l24-p6"),
    ("C04", 52, 24, 3, 1, 1, 1, "s52-full-l24-p3"),
    ("C05", 52, 12, 6, 0, 1, 1, "s52-nodiff-l12-p6"),
    ("C06", 52, 12, 3, 0, 1, 1, "s52-nodiff-l12-p3"),
    ("C07", 52, 24, 6, 0, 1, 1, "s52-nodiff-l24-p6"),
    ("C08", 52, 24, 3, 0, 1, 1, "s52-nodiff-l24-p3"),
    # seed=62 (C09-C16)
    ("C09", 62, 12, 6, 1, 1, 1, "s62-full-l12-p6"),
    ("C10", 62, 12, 3, 1, 1, 1, "s62-full-l12-p3"),
    ("C11", 62, 24, 6, 1, 1, 1, "s62-full-l24-p6"),
    ("C12", 62, 24, 3, 1, 1, 1, "s62-full-l24-p3"),
    ("C13", 62, 12, 6, 0, 1, 1, "s62-nodiff-l12-p6"),
    ("C14", 62, 12, 3, 0, 1, 1, "s62-nodiff-l12-p3"),
    ("C15", 62, 24, 6, 0, 1, 1, "s62-nodiff-l24-p6"),
    ("C16", 62, 24, 3, 0, 1, 1, "s62-nodiff-l24-p3"),
]


def get_ablation_type(d, g, f):
    if d and g and f:
        return "full"
    if not d:
        return "no_diff"
    return "unknown"


def main():
    rows = []
    for exp_id, seed, sl, pl, d, g, f, label in EXPERIMENTS:
        output_dir = ROOT / f"matrix_N95_PEDiffWaveNet_noleak_student_w2_{label}"
        metrics_file = output_dir / "metrics_summary.json"

        row = {
            "experiment_id": exp_id,
            "exp_label": label,
            "seed": seed,
            "seq_len": sl,
            "pre_len": pl,
            "ablation": get_ablation_type(d, g, f),
            "use_diffusion": d,
            "use_pe_graph": g,
            "use_pe_film": f,
        }

        if metrics_file.exists():
            try:
                m = json.loads(metrics_file.read_text(encoding="utf-8"))
                row["test_rmse"] = m.get("test_rmse")
                row["test_mae"] = m.get("test_mae")
                row["test_mape"] = m.get("test_mape")
                row["peak_rmse"] = m.get("rmse_peak")
                row["best_epoch"] = m.get("best_epoch")
                row["status"] = "done"
            except Exception as e:
                row["status"] = f"parse_error: {e}"
        else:
            row["status"] = "not_run"

        rows.append(row)

    fieldnames = [
        "experiment_id", "exp_label", "seed", "seq_len", "pre_len",
        "ablation", "use_diffusion", "use_pe_graph", "use_pe_film",
        "test_rmse", "test_mae", "test_mape", "peak_rmse", "best_epoch", "status"
    ]

    # 分别输出两个 seed 的 CSV
    for seed_val, subdir in [(52, "person_C_seed52_full_nodiff"), (62, "person_C_seed62_full_nodiff")]:
        out_csv = RESULTS_DIR / subdir / "person_C_results.csv"
        seed_rows = [r for r in rows if r["seed"] == seed_val]
        with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(seed_rows)
        done = [r for r in seed_rows if r["status"] == "done"]
        print(f"seed={seed_val}: {len(done)}/{len(seed_rows)} done → {out_csv}")

    # 合并 CSV
    out_all = RESULTS_DIR / "person_C_all_results.csv"
    with open(out_all, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    done_all = [r for r in rows if r["status"] == "done"]
    print(f"All: {len(done_all)}/{len(rows)} done → {out_all}")

    # 打印汇总
    print(f"\n{'ID':<4} {'Label':<23} {'Seed':>4} {'RMSE':>8} {'MAE':>8} {'MAPE':>8} {'Peak':>8}")
    for r in rows:
        if r["status"] == "done":
            print(f"{r['experiment_id']:<4} {r['exp_label']:<23} {r['seed']:>4} {r['test_rmse']:>8.2f} {r['test_mae']:>8.2f} {r['test_mape']:>7.1f}% {r['peak_rmse']:>8.2f}")


if __name__ == "__main__":
    main()
