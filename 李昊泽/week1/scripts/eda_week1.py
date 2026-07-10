#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第一周 EDA：数据理解、缺失值分析、可视化（中文版）"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

PROJECT_DIR = Path(r'H:\Trae Project\O3predict')
DATA_DIR = PROJECT_DIR / 'data_N95'
MATRIX_DIR = PROJECT_DIR / 'matrix_N95'
XLSX_DIR = PROJECT_DIR / 'xlsx_N95'
OUTPUT_DIR = PROJECT_DIR / 'eda_output'
OUTPUT_DIR.mkdir(exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("第一周 EDA：臭氧数据探索分析")
print("=" * 60)

# ============================================================
# 1. 加载处理后的 O3 数据
# ============================================================
print("\n--- 1. 处理后的O3数据 (matrix_N95/) ---")
o3_data = np.load(MATRIX_DIR / 'data.npy').astype(np.float32)
time_index = np.load(MATRIX_DIR / 'time_index.npy', allow_pickle=True)
print(f"O3数据形状: {o3_data.shape}  (站点数={o3_data.shape[0]}, 时间步={o3_data.shape[1]})")
print(f"时间范围: {time_index[0]} 至 {time_index[-1]}")

finite_mask = np.isfinite(o3_data)
print(f"\nO3 基本统计量:")
print(f"  最小值: {o3_data[finite_mask].min():.1f} μg/m³")
print(f"  最大值: {o3_data[finite_mask].max():.1f} μg/m³")
print(f"  均值:   {o3_data[finite_mask].mean():.1f} μg/m³")
print(f"  标准差: {o3_data[finite_mask].std():.1f}")
print(f"  中位数: {np.median(o3_data[finite_mask]):.1f} μg/m³")

total_values = o3_data.size
nan_count = np.sum(~finite_mask)
missing_rate = nan_count / total_values * 100
print(f"\n缺失值分析 (O3):")
print(f"  总数据量:   {total_values}")
print(f"  缺失数量:   {nan_count}")
print(f"  缺失率:     {missing_rate:.4f}%")

station_nan_rates = np.mean(~finite_mask, axis=1) * 100
print(f"\n逐站缺失率:")
print(f"  最低:  {station_nan_rates.min():.2f}%")
print(f"  最高:  {station_nan_rates.max():.2f}%")
print(f"  均值:  {station_nan_rates.mean():.2f}%")

# ============================================================
# 2. 气象数据
# ============================================================
print("\n--- 2. 气象因子数据 ---")
met_cache = np.load(MATRIX_DIR / 'met_raw_aligned_cache.npz', allow_pickle=True)
print(f"气象变量列表: {list(met_cache.keys())}")
for key in met_cache.keys():
    val = met_cache[key]
    if hasattr(val, 'shape'):
        print(f"  {key}: 形状={val.shape}, 类型={val.dtype}")

combined = np.load(MATRIX_DIR / 'data_combined_m15.npy').astype(np.float32)
print(f"\n组合数据 (O3 + 14个气象因子): 形状={combined.shape}")
print(f"  维度: (时间={combined.shape[0]}, 站点={combined.shape[1]}, 特征={combined.shape[2]})")

# ============================================================
# 3. 站点信息
# ============================================================
print("\n--- 3. 站点信息 ---")
station_df = pd.read_excel(XLSX_DIR / 'station_loc1.xlsx')
print(f"站点数量: {len(station_df)}")
print(f"列名: {list(station_df.columns)}")

# ============================================================
# 4. 原始CSV调研
# ============================================================
print("\n--- 4. 原始CSV调研 ---")
csv_files = sorted(DATA_DIR.glob('china_sites_*.csv'))
print(f"CSV文件总数: {len(csv_files)}")
print(f"日期范围: {csv_files[0].stem[-8:]} 至 {csv_files[-1].stem[-8:]}")

sample_csv = pd.read_csv(csv_files[0])
all_types = set()
for csv_f in csv_files[:5]:
    df_s = pd.read_csv(csv_f)
    all_types.update(df_s['type'].unique())
print(f"污染物类型: {sorted(all_types)}")

# ============================================================
# 5. 生成中文版图表
# ============================================================
print("\n--- 5. 生成中文版EDA图表 ---")
time_idx = pd.to_datetime(time_index)

# ===== 图1: EDA总览 (6子图) =====
fig, axes = plt.subplots(3, 2, figsize=(16, 14))

# 子图1: O3均值时间序列
ax = axes[0, 0]
station_mean = np.nanmean(o3_data, axis=0)
ax.plot(station_mean, linewidth=0.5, alpha=0.8, color='steelblue')
ax.set_title('95站点O3浓度均值时间序列 (2022年)', fontsize=13, fontweight='bold')
ax.set_xlabel('时间索引 (小时)')
ax.set_ylabel('O3浓度 (μg/m³)')
ax.grid(True, alpha=0.3)

# 子图2: 逐站缺失率
ax = axes[0, 1]
ax.bar(range(len(station_nan_rates)), sorted(station_nan_rates, reverse=True),
       alpha=0.7, color='steelblue')
ax.axhline(y=station_nan_rates.mean(), color='red', linestyle='--',
           label=f'均值: {station_nan_rates.mean():.2f}%')
ax.set_title('各站点O3缺失率分布 (从高到低排序)', fontsize=13, fontweight='bold')
ax.set_xlabel('站点序号 (按缺失率排序)')
ax.set_ylabel('缺失率 (%)')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 子图3: O3浓度分布直方图
ax = axes[1, 0]
valid_o3 = o3_data[finite_mask]
ax.hist(valid_o3, bins=100, alpha=0.7, edgecolor='black', linewidth=0.3, color='steelblue')
ax.axvline(x=valid_o3.mean(), color='red', linestyle='--',
           label=f'均值: {valid_o3.mean():.1f} μg/m³')
ax.axvline(x=np.median(valid_o3), color='orange', linestyle='--',
           label=f'中位数: {np.median(valid_o3):.1f} μg/m³')
ax.set_title('O3浓度分布直方图 (全部站点×全部时间)', fontsize=13, fontweight='bold')
ax.set_xlabel('O3浓度 (μg/m³)')
ax.set_ylabel('频数')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 子图4: 逐月箱线图
ax = axes[1, 1]
months = time_idx.month
monthly_data = []
for m in range(1, 13):
    mask_m = months == m
    vals = o3_data[:, mask_m].flatten()
    monthly_data.append(vals[np.isfinite(vals)])

bp = ax.boxplot(monthly_data, patch_artist=True, showfliers=False)
month_names = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
for patch, m in zip(bp['boxes'], range(1, 13)):
    patch.set_facecolor(plt.cm.RdYlGn(m / 12))
ax.set_title('O3浓度逐月分布 (95站点)', fontsize=13, fontweight='bold')
ax.set_xlabel('月份')
ax.set_ylabel('O3浓度 (μg/m³)')
ax.set_xticklabels(month_names)
ax.grid(True, alpha=0.3)

# 子图5: 示例站点时序
ax = axes[2, 0]
for i in range(min(4, o3_data.shape[0])):
    ax.plot(o3_data[i, :2000], linewidth=0.5, alpha=0.8, label=f'站点 {i+1}')
ax.set_title('前4个站点O3时间序列 (前2000小时)', fontsize=13, fontweight='bold')
ax.set_xlabel('时间索引 (小时)')
ax.set_ylabel('O3浓度 (μg/m³)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 子图6: 站点地理分布
ax = axes[2, 1]
lon_col = station_df.columns[3] if len(station_df.columns) > 3 else station_df.columns[-2]
lat_col = station_df.columns[4] if len(station_df.columns) > 4 else station_df.columns[-1]
sc = ax.scatter(station_df[lon_col], station_df[lat_col],
                c='steelblue', s=60, edgecolors='black', linewidth=0.5)
ax.set_title('95个空气质量监测站点地理分布', fontsize=13, fontweight='bold')
ax.set_xlabel('经度')
ax.set_ylabel('纬度')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'eda_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"  已保存: eda_overview.png")

# ===== 图2: 时间模式分析 (4子图) =====
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# 子图1: 缺失值热力图
ax = axes[0, 0]
sample_stations = min(30, o3_data.shape[0])
missing_sample = ~np.isfinite(o3_data[:sample_stations, ::50])
ax.imshow(missing_sample, aspect='auto', cmap='Reds', interpolation='nearest')
ax.set_title(f'缺失值分布热力图 (前{sample_stations}站, 每50小时采样)', fontsize=13, fontweight='bold')
ax.set_xlabel('时间 (每50小时)')
ax.set_ylabel('站点序号')

# 子图2: 日内变化
ax = axes[0, 1]
hours_of_day = time_idx.hour
hourly_mean, hourly_std = [], []
for h in range(24):
    mask_h = hours_of_day == h
    vals = o3_data[:, mask_h].flatten()
    vals = vals[np.isfinite(vals)]
    hourly_mean.append(vals.mean())
    hourly_std.append(vals.std())

ax.fill_between(range(24), np.array(hourly_mean)-np.array(hourly_std),
                np.array(hourly_mean)+np.array(hourly_std), alpha=0.3, color='steelblue')
ax.plot(range(24), hourly_mean, 'o-', linewidth=2, color='steelblue')
ax.set_title('O3浓度日内变化曲线 (全部站点×全部日期)', fontsize=13, fontweight='bold')
ax.set_xlabel('小时')
ax.set_ylabel('O3浓度 (μg/m³)')
ax.set_xticks(range(0, 24, 3))
ax.grid(True, alpha=0.3)

# 子图3: 站点互相关性
ax = axes[1, 0]
n_sample = 6
sample_idx = np.linspace(0, o3_data.shape[0]-1, n_sample, dtype=int)
corr_data = np.array([o3_data[i, :] for i in sample_idx])
valid_times = np.all(np.isfinite(corr_data), axis=0)
corr_mat = np.corrcoef(corr_data[:, valid_times])
im = ax.imshow(corr_mat, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax.set_title(f'{n_sample}个样本站点间相关系数矩阵', fontsize=13, fontweight='bold')
ax.set_xlabel('站点序号')
ax.set_ylabel('站点序号')
plt.colorbar(im, ax=ax, label='相关系数')

# 子图4: 周内变化
ax = axes[1, 1]
dow = time_idx.dayofweek
dow_names = ['周一','周二','周三','周四','周五','周六','周日']
dow_mean = []
for d in range(7):
    mask_d = dow == d
    vals = o3_data[:, mask_d].flatten()
    vals = vals[np.isfinite(vals)]
    dow_mean.append(vals.mean())
colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, 7))
ax.bar(range(7), dow_mean, alpha=0.8, color=colors, edgecolor='black', linewidth=0.5)
ax.set_title('O3浓度周内变化 (全部站点)', fontsize=13, fontweight='bold')
ax.set_xlabel('星期')
ax.set_ylabel('O3浓度 (μg/m³)')
ax.set_xticks(range(7))
ax.set_xticklabels(dow_names)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'eda_patterns.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"  已保存: eda_patterns.png")

# ============================================================
# 6. 生成中英文双语数据卡
# ============================================================
print("\n--- 6. 生成数据卡 ---")

met_var_names = {
    "blh": "边界层高度", "d2m": "露点温度", "fsr": "地表粗糙度",
    "kx": "K指数", "sp": "地表气压", "ssr": "地表太阳辐射",
    "ssrd": "地表太阳辐射下行", "t2m": "2米气温", "tcc": "总云量",
    "tcwv": "总柱水汽量", "tp": "总降水量", "u10": "10米纬向风",
    "v10": "10米经向风", "zust": "摩擦速度"
}

data_card = {
    "_说明": "本文件为第一周数据理解成果——数据卡。包含完整的数据元信息描述。",
    "项目名称": "基于PE-DiffWaveNet的多站点臭氧预测",
    "生成时间": str(pd.Timestamp.now()),
    "数据来源": "2022年全国95个空气质量监测站点逐小时数据",
    "目标变量": "O3 (臭氧, 单位: μg/m³)",
    "空间信息": {
        "_说明": "监测站点的空间分布信息",
        "站点数量": 95,
        "站点编号范围": f"{station_df.iloc[:, 0].min()} ~ {station_df.iloc[:, 0].max()}",
        "坐标信息": "经纬度详见 xlsx_N95/station_loc1.xlsx"
    },
    "时间信息": {
        "_说明": "数据的时间跨度和频率",
        "起止时间": f"{time_index[0]} 至 {time_index[-1]}",
        "时间步数": int(len(time_index)),
        "频率": "逐小时",
        "总小时数": int(len(time_index))
    },
    "特征信息": {
        "_说明": "模型使用的输入特征",
        "特征总数": 15,
        "特征组成": "O3 + 14个ERA5气象再分析因子",
        "气象变量中英文对照": met_var_names
    },
    "缺失值统计": {
        "_说明": "处理后95站点O3数据的缺失情况（原始CSV中约2000站点的缺失率见pm_stats_report.txt）",
        "O3缺失数量": int(nan_count),
        "O3缺失率": f"{missing_rate:.4f}%",
        "逐站缺失率最低": f"{station_nan_rates.min():.2f}%",
        "逐站缺失率最高": f"{station_nan_rates.max():.2f}%",
        "逐站缺失率均值": f"{station_nan_rates.mean():.2f}%"
    },
    "数据切分": {
        "_说明": "无数据泄漏(no-leak)切分协议：先沿时间轴切分，再在各自split内做滑窗，归一化参数仅用训练集拟合",
        "训练集比例": 0.8465,
        "切分协议": "no-leak: 时间轴切分→各自滑窗→训练段单独拟合归一化",
        "重要提示": "测试集信息未参与归一化、滑窗构造或图结构构建"
    },
    "输入输出规格": {
        "_说明": "模型的输入和输出维度",
        "默认输入窗口": "24小时",
        "默认预测步长": "6小时",
        "输入": "过去24小时的O3 + 14个气象因子",
        "输出": "未来6小时的O3预测值"
    },
    "关键文件": {
        "_说明": "项目中各文件的用途",
        "处理后O3数据": "matrix_N95/data.npy (95 × 8717)",
        "气象缓存": "matrix_N95/met_raw_aligned_cache.npz",
        "组合数据": "matrix_N95/data_combined_m15.npy (8717 × 95 × 15)",
        "原始CSV": "data_N95/china_sites_YYYYMMDD.csv (365个文件)",
        "站点信息": "xlsx_N95/station_loc1.xlsx"
    },
    "适用场景": [
        "多站点空气质量预测",
        "时空污染数据补全",
        "基于气象条件的臭氧情景生成"
    ],
    "局限性": [
        "仅含2022年单年数据，无法分析多年趋势",
        "95个站点主要分布在京津冀及周边，未均等覆盖全国",
        "气象数据为ERA5再分析资料，非原位实测",
        "扩散模型平均效应可能导致臭氧峰值被低估"
    ]
}

with open(OUTPUT_DIR / 'data_card.json', 'w', encoding='utf-8') as f:
    json.dump(data_card, f, ensure_ascii=False, indent=2)
print(f"  已保存: data_card.json")

# ============================================================
# 7. 总结
# ============================================================
print("\n" + "=" * 60)
print("EDA 完成！关键发现：")
print("=" * 60)
print(f"  1. 95个站点，8717小时（2022全年）")
print(f"  2. O3缺失率: {missing_rate:.4f}%（处理后数据无缺失）")
print(f"  3. O3范围: [{valid_o3.min():.1f}, {valid_o3.max():.1f}] μg/m³, 均值={valid_o3.mean():.1f}")
print(f"  4. 14个气象因子 (ERA5再分析)")
print(f"  5. No-leak切分: train_rate=0.8465")
print(f"  6. 默认任务: 24小时输入 → 6小时预测")
print(f"  7. 输出目录: {OUTPUT_DIR}")
print("=" * 60)
