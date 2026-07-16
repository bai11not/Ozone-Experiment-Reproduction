"""提取站点误差分布 CSV -- 用于 Origin 图表 5"""
import numpy as np
import pandas as pd

DIR = r"d:\时空数据\臭氧预测资料\matrix_N95_PEDiffWaveNet_noleak_g3_pedw_no_pe_film_p3_l24_s42"

pred = np.load(f"{DIR}/test_predictions.npy")
targ = np.load(f"{DIR}/test_targets.npy")

# 取预测均值
if pred.ndim == 4:
    pred_mean = pred.mean(axis=1)  # (N_test, pre_len, N_node)
else:
    pred_mean = pred

# 按站点算 RMSE
n_stations = targ.shape[-1]
results = []
for s in range(n_stations):
    p = pred_mean[:, :, s].flatten()
    g = targ[:, :, s].flatten()
    rmse = np.sqrt(np.mean((p - g) ** 2))
    mae = np.mean(np.abs(p - g))
    results.append([s + 1, rmse, mae])

# 读取站点名称
sites = pd.read_excel(
    r"d:\时空数据\臭氧预测资料\xlsx_N95\station_loc1.xlsx"
)
site_names = sites.iloc[:, 1].tolist()  # 第 2 列是站点名

out = []
for i, (sid, rmse, mae) in enumerate(results):
    name = site_names[i] if i < len(site_names) else f"Station{sid}"
    out.append([sid, name, rmse, mae])

arr = np.array(out, dtype=object)
import csv
with open(r"d:\时空数据\week3\data\5_station_error.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["StationID", "StationName", "RMSE", "MAE"])
    for row in out:
        w.writerow(row)

print(f"{n_stations} 个站点 误差已导出 -> 5_station_error.csv")
print(f"\nRMSE 范围: {min(r[1] for r in results):.2f} - {max(r[1] for r in results):.2f}")
print(f"平均 RMSE: {np.mean([r[1] for r in results]):.2f}")