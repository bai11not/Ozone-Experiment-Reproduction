"""
生成 DiffSTG 所需的数据文件:
  1. flow.npy  — (T, V, 1) O3 时间序列
  2. adj.npy   — (V, V) 空间距离邻接矩阵

用法: python gen_diffstg_data.py
输出: data/dataset/AIR_N95/flow.npy, adj.npy
"""
import numpy as np
import pandas as pd
import os

PROJECT = r"d:\桌面\臭氧预测资料\臭氧预测资料"
MATRIX = os.path.join(PROJECT, "matrix_N95")
STATION_XLSX = os.path.join(PROJECT, "xlsx_N95", "station_loc1.xlsx")
OUT = os.path.join(PROJECT, "data", "dataset", "AIR_N95")

# ============================================================
# 1. 生成 flow.npy — O3 时间序列
# ============================================================
print("=" * 50)
print("Step 1: 生成 flow.npy")
data = np.load(os.path.join(MATRIX, "data_combined_m15.npy"))  # (8717, 95, 15)
print(f"  data_combined_m15: {data.shape}")

# 第 0 列是 O3
o3 = data[:, :, 0:1].astype(np.float32)  # (8717, 95, 1)
print(f"  O3 slice: {o3.shape}")

# 统计基本信息
print(f"  O3 range: [{np.nanmin(o3):.1f}, {np.nanmax(o3):.1f}]")
print(f"  O3 mean:  {np.nanmean(o3):.1f}")
print(f"  NaN count: {np.sum(np.isnan(o3))} / {o3.size} ({100*np.sum(np.isnan(o3))/o3.size:.2f}%)")

# NaN 填 0（DiffSTG 的 AIR 数据集处理方式）
o3 = np.nan_to_num(o3, nan=0.0)
print(f"  After nan_to_num — NaN count: {np.sum(o3 == 0)}")

# ============================================================
# 2. 生成 adj.npy — 空间距离邻接矩阵
# ============================================================
print("\n" + "=" * 50)
print("Step 2: 生成 adj.npy")

df = pd.read_excel(STATION_XLSX)
# 列名可能是中文乱码，按位置取
lng = df.iloc[:, 3].values.astype(np.float64)  # 经度
lat = df.iloc[:, 4].values.astype(np.float64)  # 纬度
print(f"  站点数: {len(lng)}")
print(f"  经度范围: [{lng.min():.4f}, {lng.max():.4f}]")
print(f"  纬度范围: [{lat.min():.4f}, {lat.max():.4f}]")

# Haversine 距离 (km)
def haversine_dist(lat1, lng1, lat2, lng2):
    """计算两组经纬度之间的距离矩阵 (km)"""
    R = 6371.0
    lat1, lng1 = np.radians(lat1), np.radians(lng1)
    lat2, lng2 = np.radians(lat2), np.radians(lng2)
    dlat = lat1[:, None] - lat2[None, :]
    dlng = lng1[:, None] - lng2[None, :]
    a = np.sin(dlat/2)**2 + np.cos(lat1[:, None]) * np.cos(lat2[None, :]) * np.sin(dlng/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

dist_km = haversine_dist(lat, lng, lat, lng)
print(f"  距离范围: [{dist_km.min():.1f}, {dist_km.max():.1f}] km")
print(f"  平均距离: {dist_km.mean():.1f} km")

# 阈值高斯核邻接矩阵
sigma = 50.0        # 50km 衰减尺度
threshold = 150.0   # 150km 以外权重为 0

adj = np.exp(-dist_km**2 / (2 * sigma**2))
adj[dist_km > threshold] = 0.0

print(f"\n  邻接矩阵统计:")
print(f"  非零边: {np.count_nonzero(adj)} / {adj.size} ({100*np.count_nonzero(adj)/adj.size:.1f}%)")
print(f"  平均度: {np.mean(np.count_nonzero(adj, axis=1)):.1f}")
print(f"  孤立节点: {np.sum(np.count_nonzero(adj, axis=1) == 0)}")

# 如果存在孤立节点，用 k-NN 补连
isolated = np.where(np.count_nonzero(adj, axis=1) == 0)[0]
if len(isolated) > 0:
    print(f"\n  ⚠ 发现 {len(isolated)} 个孤立节点: {isolated}")
    print(f"  使用 5-NN 补连...")
    k = 5
    for i in isolated:
        nn = np.argsort(dist_km[i])[1:k+1]  # 跳过自己
        for j in nn:
            adj[i, j] = np.exp(-dist_km[i, j]**2 / (2 * sigma**2))
            adj[j, i] = adj[i, j]  # 对称
    print(f"  修复后孤立节点: {np.sum(np.count_nonzero(adj, axis=1) == 0)}")

adj = adj.astype(np.float32)

# ============================================================
# 3. 保存
# ============================================================
print("\n" + "=" * 50)
print("Step 3: 保存文件")
os.makedirs(OUT, exist_ok=True)

flow_path = os.path.join(OUT, "flow.npy")
adj_path = os.path.join(OUT, "adj.npy")

np.save(flow_path, o3)
np.save(adj_path, adj)

print(f"  flow.npy → {flow_path}")
print(f"    shape: {o3.shape}, dtype: {o3.dtype}, size: {os.path.getsize(flow_path)/1024/1024:.1f} MB")
print(f"  adj.npy  → {adj_path}")
print(f"    shape: {adj.shape}, dtype: {adj.dtype}, size: {os.path.getsize(adj_path)/1024:.1f} KB")

# 验证可读
print("\n  ✅ 验证:")
_v = np.load(flow_path)
print(f"    flow.npy loaded: {_v.shape}, range [{_v.min():.1f}, {_v.max():.1f}]")
_v = np.load(adj_path)
print(f"    adj.npy loaded:  {_v.shape}, range [{_v.min():.4f}, {_v.max():.4f}]")

print("\n✅ DiffSTG 数据文件生成完成!")
