"""提取真实值 vs 预测值 CSV -- 用于 Origin 图表 4"""
import numpy as np

# 使用 B08 (no_pe_film, seq=24, pre=3, seed=42) 的预测文件
DIR = r"d:\时空数据\臭氧预测资料\matrix_N95_PEDiffWaveNet_noleak_g3_pedw_no_pe_film_p3_l24_s42"

pred = np.load(f"{DIR}/test_predictions.npy")   # (N_test, n_samples, pre_len, N_node) 或类似
targ = np.load(f"{DIR}/test_targets.npy")        # (N_test, pre_len, N_node)

print(f"predictions shape: {pred.shape}")
print(f"targets shape: {targ.shape}")

# 取预测均值 (axis=1 是采样维) 和第一个站点 (station=0)
if pred.ndim == 4:
    pred_mean = pred.mean(axis=1)  # (N_test, pre_len, N_node)
elif pred.ndim == 3:
    pred_mean = pred  # (N_test, pre_len, N_node)
else:
    raise ValueError(f"Unexpected pred shape: {pred.shape}")

# 输出: 时间步， 预测值， 真实值
# 取所有站点平均，时间片取前 100 个
N = min(100, targ.shape[0])
stations = [0, 10, 20, 30, 40]  # 挑 5 个代表性站点

for station in stations:
    out = []
    for t in range(N):
        for step in range(pred_mean.shape[1]):
            p = pred_mean[t, step, station]
            g = targ[t, step, station]
            out.append([t * pred_mean.shape[1] + step, p, g])
    arr = np.array(out)
    np.savetxt(
        rf"d:\时空数据\week3\data\4_predictions_station{station}.csv",
        arr, delimiter=",", fmt="%.4f",
        header="Time, Predicted, GroundTruth", comments=""
    )
    print(f"站点 {station}: {len(arr)} 行 -> 4_predictions_station{station}.csv")

print("\n完成! 每个 CSV 选一个站点在 Origin 里画双线图")