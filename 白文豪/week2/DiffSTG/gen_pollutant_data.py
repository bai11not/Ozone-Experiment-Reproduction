# -*- coding: utf-8 -*-
"""从 daily CSVs 提取 PM2.5 和 PM10 数据，生成 DiffSTG 格式的 flow.npy"""

import numpy as np
import pandas as pd
import os, glob

DATA_DIR = "/mnt/d/时空数据/臭氧预测资料"
SITES_FILE = os.path.join(DATA_DIR, "xlsx_N95", "station_loc1.xlsx")
CSV_DIR = os.path.join(DATA_DIR, "data_N95")
OUT_DIR = os.path.join(DATA_DIR, "matrix_N95_pollutants")

# 1. 读取 95 个站点 ID
sites = pd.read_excel(SITES_FILE)
station_ids = sites.iloc[:, 0].astype(str).tolist()  # 列名如 '1001A'
print(f"站点数: {len(station_ids)}")

# 2. 读取所有 CSV 并提取 PM2.5 和 PM10
csv_files = sorted(glob.glob(os.path.join(CSV_DIR, "china_sites_2022*.csv")))

# 按时间收集数据: {(date, hour): {station_id: value}}
from collections import defaultdict
pm25_data = defaultdict(dict)
pm10_data = defaultdict(dict)
time_keys = []

for fpath in csv_files:
    df = pd.read_csv(fpath)
    df.columns = df.columns.astype(str)

    for ptype, storage in [("PM2.5", pm25_data), ("PM10", pm10_data)]:
        rows = df[df["type"] == ptype]
        for _, row in rows.iterrows():
            date = str(int(row["date"]))
            hour = int(row["hour"])
            key = (date, hour)
            if key not in time_keys:
                time_keys.append(key)
            for sid in station_ids:
                if sid in df.columns:
                    val = row.get(sid, np.nan)
                    try:
                        val = float(val)
                    except (ValueError, TypeError):
                        val = np.nan
                    if not np.isnan(val):
                        storage[key][sid] = val

print(f"时间点数: {len(time_keys)}")

# 3. 构建 (T, N) 矩阵，对齐 O3 data.npy 的时间
# 用 O3 数据做时间对齐: matrix_N95/data.npy shape=(95, 8717)
o3_data = np.load(os.path.join(DATA_DIR, "matrix_N95", "data.npy"))  # (95, 8717)

# 也从 daily CSVs 提取 O3 做对齐
o3_csv = defaultdict(dict)
for fpath in csv_files:
    df = pd.read_csv(fpath)
    df.columns = df.columns.astype(str)
    rows = df[df["type"] == "O3"]
    for _, row in rows.iterrows():
        date = str(int(row["date"]))
        hour = int(row["hour"])
        key = (date, hour)
        for sid in station_ids:
            if sid in df.columns:
                val = row.get(sid, np.nan)
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    val = np.nan
                if not np.isnan(val):
                    o3_csv[key][sid] = val

# 提取 O3 的 CSV 数据矩阵
time_keys_sorted = sorted(time_keys)
T = len(time_keys_sorted)
o3_from_csv = np.full((T, len(station_ids)), np.nan)
for t_idx, key in enumerate(time_keys_sorted):
    d = o3_csv.get(key, {})
    for s_idx, sid in enumerate(station_ids):
        o3_from_csv[t_idx, s_idx] = d.get(sid, np.nan)

# 找到 CSV O3 和 data.npy O3 的时间对齐
# data.npy 是 (95, T_real), 转置后 (T_real, 95)
o3_real = o3_data.T  # (8717, 95)

# 用简单的滑窗匹配法: 对每个站点找到匹配的起始位置
# 用所有站点的平均值做对齐
o3_csv_mean = np.nanmean(o3_from_csv, axis=1)  # (T,)
o3_real_mean = np.nanmean(o3_real, axis=1)     # (8717,)

# 找最佳对齐偏移
best_offset = 0
best_corr = -1
for offset in range(len(o3_csv_mean) - len(o3_real_mean) + 1):
    csv_slice = o3_csv_mean[offset:offset + len(o3_real_mean)]
    valid = ~np.isnan(csv_slice)
    if valid.sum() < 100:
        continue
    corr = np.corrcoef(csv_slice[valid], o3_real_mean[valid])[0, 1]
    if corr > best_corr:
        best_corr = corr
        best_offset = offset

print(f"最佳偏移: {best_offset}, 相关系数: {best_corr:.4f}")

# 4. 用对齐后的时间提取 PM2.5 和 PM10
aligned_keys = time_keys_sorted[best_offset:best_offset + o3_real.shape[0]]
print(f"对齐后时间点数: {len(aligned_keys)}")

for name, storage in [("PM2.5", pm25_data), ("PM10", pm10_data)]:
    flow = np.full((len(aligned_keys), len(station_ids)), np.nan)
    for t_idx, key in enumerate(aligned_keys):
        d = storage.get(key, {})
        for s_idx, sid in enumerate(station_ids):
            flow[t_idx, s_idx] = d.get(sid, np.nan)

    # 插值填补缺失值
    flow_df = pd.DataFrame(flow)
    flow_df = flow_df.interpolate(method='linear', limit_direction='both', axis=0)
    flow_df = flow_df.bfill().ffill()
    flow = flow_df.values

    # 归一化到 [0,1]
    flow_min = np.nanmin(flow)
    flow_max = np.nanmax(flow)
    print(f"{name}: min={flow_min:.1f}, max={flow_max:.1f}")
    flow_norm = (flow - flow_min) / (flow_max - flow_min + 1e-8)

    # 保存为 (T, N, 1) 格式
    flow_out = flow_norm[:, :, np.newaxis].astype(np.float32)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"flow_{name.replace('.','')}.npy")
    np.save(out_path, flow_out)
    print(f"保存: {out_path}, shape={flow_out.shape}")

print("\n完成! 请将 flow_PM25.npy / flow_PM10.npy 复制到 DiffSTG data 目录")