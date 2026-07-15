import json, os, csv
from pathlib import Path

WEEK2_DIR = Path(r"d:\时空数据\week2")
RESULTS_DIR = WEEK2_DIR / "results"

PERSON_DIRS = {
    "A": RESULTS_DIR / "person_A_seed42_full_nodiff",
    "B": RESULTS_DIR / "person_B_seed42_nograph_nofilm",
    "C": RESULTS_DIR / "person_C_seed52_full_nodiff",
    "D": RESULTS_DIR / "person_D_seed52_nograph_nofilm",
    "E": RESULTS_DIR / "extra_prelen_scan",
}

OUTPUT_CSV = WEEK2_DIR / "metrics" / "week2_summary.csv"

HEADER = [
    "person", "exp_id", "seed", "seq_len", "pre_len",
    "use_diffusion", "use_pe_graph", "use_pe_film",
    "ablation", "status", "test_rmse", "test_mae", "test_mape",
    "best_epoch", "best_valid_rmse", "best_valid_mae",
    "relative_rmse", "relative_mae",
]

def main():
    rows = []
    for person, person_dir in PERSON_DIRS.items():
        if not person_dir.exists():
            continue
        for exp_dir in sorted(person_dir.iterdir()):
            if not exp_dir.is_dir():
                continue
            exp_id = exp_dir.name
            mf = exp_dir / "metrics_summary.json"
            cf = exp_dir / "config.json"
            if not mf.exists():
                continue

            m = json.load(open(mf, encoding="utf-8"))
            c = json.load(open(cf, encoding="utf-8")) if cf.exists() else {}

            # 消融类型
            d = int(m.get("use_diffusion", c.get("use_diffusion", -1)))
            g = int(m.get("use_pe_graph", c.get("use_pe_graph", -1)))
            f = int(m.get("use_pe_film", c.get("use_pe_film", -1)))
            if d == 1 and g == 1 and f == 1:
                ablation = "full"
            elif d == 0 and g == 1 and f == 1:
                ablation = "no_diff"
            elif d == 1 and g == 0 and f == 1:
                ablation = "no_pe_graph"
            elif d == 1 and g == 1 and f == 0:
                ablation = "no_pe_film"
            else:
                ablation = f"d{d}g{g}f{f}"

            row = {
                "person": person,
                "exp_id": exp_id,
                "seed": c.get("seed", m.get("seed", "")),
                "seq_len": c.get("seq_len", ""),
                "pre_len": c.get("pre_len", ""),
                "use_diffusion": d,
                "use_pe_graph": g,
                "use_pe_film": f,
                "ablation": ablation,
                "status": "success",
                "test_rmse": round(m["test_rmse"], 2),
                "test_mae": round(m["test_mae"], 2),
                "test_mape": round(m["test_mape"], 2),
                "best_epoch": m.get("best_epoch", ""),
                "best_valid_rmse": round(m.get("best_valid_rmse", 0), 2),
                "best_valid_mae": round(m.get("best_valid_mae", 0), 2),
                "relative_rmse": round(m.get("relative_rmse", 0), 2),
                "relative_mae": round(m.get("relative_mae", 0), 2),
            }
            rows.append(row)
            print(f"  [{ablation}] {exp_id}: RMSE={row['test_rmse']}, MAE={row['test_mae']}")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)

    success = sum(1 for r in rows if r["status"] == "success")
    print(f"\n总计: {len(rows)} 组, 成功: {success}")
    print(f"输出: {OUTPUT_CSV}")

    sorted_rows = sorted(rows, key=lambda r: r["test_rmse"])
    print("\n--- Top 5 最低 RMSE ---")
    for i, r in enumerate(sorted_rows[:5], 1):
        print(f"  {i}. {r['exp_id']}: RMSE={r['test_rmse']}, MAE={r['test_mae']}, {r['ablation']}, seq={r['seq_len']}, pre={r['pre_len']}")

if __name__ == "__main__":
    main()