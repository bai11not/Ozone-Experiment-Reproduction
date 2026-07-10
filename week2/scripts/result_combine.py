# result_combine.py
# 合并 4 人的实验结果到统一的 CSV 文件
# 用法: python result_combine.py

import os
import json
import csv
from pathlib import Path

WEEK2_DIR = Path(__file__).resolve().parent.parent  # week2/

PERSON_DIRS = {
    "A": WEEK2_DIR / "results" / "person_A_seed42_nodiff",
    "B": WEEK2_DIR / "results" / "person_B_seed42_diff",
    "C": WEEK2_DIR / "results" / "person_C_seed52_nodiff",
    "D": WEEK2_DIR / "results" / "person_D_seed52_diff",
}

OUTPUT_CSV = WEEK2_DIR / "metrics" / "week2_summary.csv"

HEADER = [
    "person", "exp_id", "seed", "seq_len", "pre_len",
    "use_diffusion", "use_pe_graph", "use_pe_film",
    "status", "test_rmse", "test_mae", "test_mape",
    "best_epoch", "best_valid_rmse", "best_valid_mae",
    "relative_rmse", "relative_mae",
    "train_scale_max", "per_step_rmse", "per_step_mae",
]


def extract_params_from_config(config: dict) -> dict:
    return {
        "seed": config.get("seed", ""),
        "seq_len": config.get("seq_len", ""),
        "pre_len": config.get("pre_len", ""),
        "use_diffusion": config.get("use_diffusion", ""),
        "use_pe_graph": config.get("use_pe_graph", ""),
        "use_pe_film": config.get("use_pe_film", ""),
    }


def main():
    rows = []

    for person, person_dir in PERSON_DIRS.items():
        if not person_dir.exists():
            print(f"[WARN] {person_dir} does not exist, skipping Person {person}")
            continue

        for exp_dir in sorted(person_dir.iterdir()):
            if not exp_dir.is_dir():
                continue

            exp_id = exp_dir.name
            if not exp_id.startswith(person):
                continue

            metrics_file = exp_dir / "metrics_summary.json"
            config_file = exp_dir / "config.json"

            row = {
                "person": person,
                "exp_id": exp_id,
                "status": "failed",
                "seed": "", "seq_len": "", "pre_len": "",
                "use_diffusion": "", "use_pe_graph": "", "use_pe_film": "",
                "test_rmse": "", "test_mae": "", "test_mape": "",
                "best_epoch": "", "best_valid_rmse": "", "best_valid_mae": "",
                "relative_rmse": "", "relative_mae": "",
                "train_scale_max": "",
                "per_step_rmse": "", "per_step_mae": "",
            }

            if config_file.exists():
                with open(config_file) as f:
                    config = json.load(f)
                params = extract_params_from_config(config)
                row.update(params)

            if metrics_file.exists():
                with open(metrics_file) as f:
                    metrics = json.load(f)

                row["status"] = "success"
                row["test_rmse"] = metrics.get("test_rmse", "")
                row["test_mae"] = metrics.get("test_mae", "")
                row["test_mape"] = metrics.get("test_mape", "")
                row["best_epoch"] = metrics.get("best_epoch", "")
                row["best_valid_rmse"] = metrics.get("best_valid_rmse", "")
                row["best_valid_mae"] = metrics.get("best_valid_mae", "")
                row["relative_rmse"] = metrics.get("relative_rmse", "")
                row["relative_mae"] = metrics.get("relative_mae", "")
                row["train_scale_max"] = metrics.get("train_scale_max", "")
                row["per_step_rmse"] = str(metrics.get("per_step_rmse", ""))
                row["per_step_mae"] = str(metrics.get("per_step_mae", ""))

            rows.append(row)
            print(f"  [{row['status']}] {exp_id}: RMSE={row['test_rmse']}, MAE={row['test_mae']}")

    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)

    success_count = sum(1 for r in rows if r["status"] == "success")
    fail_count = sum(1 for r in rows if r["status"] == "failed")
    print(f"\n总计: {len(rows)} 组, 成功: {success_count}, 失败: {fail_count}")
    print(f"输出文件: {OUTPUT_CSV}")

    # Print top 5 by RMSE
    successful = [r for r in rows if r["status"] == "success" and r["test_rmse"] != ""]
    successful.sort(key=lambda r: float(r["test_rmse"]))
    print("\n--- Top 5 最低 RMSE ---")
    for i, r in enumerate(successful[:5], 1):
        print(f"  {i}. {r['exp_id']}: RMSE={r['test_rmse']}, MAE={r['test_mae']}, "
              f"d={r['use_diffusion']}, g={r['use_pe_graph']}, f={r['use_pe_film']}, "
              f"l={r['seq_len']}, p={r['pre_len']}")


if __name__ == "__main__":
    main()