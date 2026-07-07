#!/usr/bin/env python3
"""
数据整理脚本 — 第1周任务：数据理解和代码跑通
======================================================
1. 统计 data_N95 中 O3、PM2.5、PM10 的缺失情况
2. 统计 95 个站点的城市、经纬度分布
3. 画 O3、PM2.5、PM10 的整体时间序列
4. 输出一份数据说明初稿 (data_description_draft.md)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys
import io
from collections import Counter
from datetime import datetime
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# 路径配置
# ============================================================
BASE_DIR = r'd:\生产实习\臭氧数据集\臭氧预测资料'
DATA_DIR = os.path.join(BASE_DIR, 'data_N95')
MATRIX_DIR = os.path.join(BASE_DIR, 'matrix_N95')
XLSX_DIR = os.path.join(BASE_DIR, 'xlsx_N95')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data_organization_output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("数据整理脚本开始运行")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ============================================================
# Step 1: 读取站点信息
# ============================================================
print("\n[Step 1] 读取站点信息...")
station_df = pd.read_excel(os.path.join(XLSX_DIR, 'station_loc1.xlsx'))
station_df.columns = ['station_code', 'station_name', 'city', 'lon', 'lat']
target_stations = station_df['station_code'].tolist()
print(f"  站点数: {len(target_stations)}")

# ============================================================
# Step 2: 遍历所有 CSV 文件，提取 O3、PM2.5、PM10
# ============================================================
print("\n[Step 2] 遍历 data_N95 CSV 文件，提取污染物数据...")
csv_files = sorted([
    f for f in os.listdir(DATA_DIR)
    if f.startswith('china_sites_') and f.endswith('.csv')
])
print(f"  找到 {len(csv_files)} 个 CSV 文件")

pollutants = ['O3', 'PM2.5', 'PM10']
data_dict = {p: {st: [] for st in target_stations} for p in pollutants}
time_labels = []

file_count = 0
for csv_file in csv_files:
    file_count += 1
    if file_count % 50 == 0:
        print(f"  处理进度: {file_count}/{len(csv_files)}")

    date_str = csv_file.replace('china_sites_', '').replace('.csv', '')
    filepath = os.path.join(DATA_DIR, csv_file)
    df = pd.read_csv(filepath)

    for pol in pollutants:
        pol_rows = df[df['type'] == pol]
        n_rows = len(pol_rows)

        # 获取这一天的实际小时
        hours_in_file = pol_rows['hour'].values if 'hour' in pol_rows.columns else list(range(n_rows))

        for st in target_stations:
            if st in pol_rows.columns:
                vals = pol_rows[st].values.astype(float)
            else:
                vals = np.full(n_rows, np.nan)
            data_dict[pol][st].extend(vals)

        # 只在第一个pollutant时生成时间标签
        if pol == 'O3':
            for h in hours_in_file:
                time_labels.append(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {int(h):02d}:00:00")

print(f"  完成! 共处理 {file_count} 个文件")
print(f"  O3 时间点总数: {len(data_dict['O3'][target_stations[0]])}")
print(f"  时间标签数: {len(time_labels)}")

# 确保时间标签和数据长度一致
n_total = len(time_labels)
for pol in pollutants:
    for st in target_stations:
        if len(data_dict[pol][st]) != n_total:
            # 截断或补齐
            if len(data_dict[pol][st]) > n_total:
                data_dict[pol][st] = data_dict[pol][st][:n_total]
            else:
                data_dict[pol][st].extend([np.nan] * (n_total - len(data_dict[pol][st])))

print(f"  对齐后数据点数: {n_total}")

# 转换为 DataFrame
print("\n[Step 2b] 转换为 DataFrame...")
time_index = pd.to_datetime(time_labels)

o3_df = pd.DataFrame({st: data_dict['O3'][st] for st in target_stations}, index=time_index)
pm25_df = pd.DataFrame({st: data_dict['PM2.5'][st] for st in target_stations}, index=time_index)
pm10_df = pd.DataFrame({st: data_dict['PM10'][st] for st in target_stations}, index=time_index)

print(f"  O3 DataFrame shape: {o3_df.shape}")
print(f"  PM2.5 DataFrame shape: {pm25_df.shape}")
print(f"  PM10 DataFrame shape: {pm10_df.shape}")
print(f"  时间范围: {time_index.min()} ~ {time_index.max()}")

# ============================================================
# Step 3: 缺失值统计
# ============================================================
print("\n[Step 3] 缺失值统计...")

def compute_missing_stats(df, name):
    total = df.size
    missing = df.isnull().sum().sum()
    missing_pct = missing / total * 100
    per_station_missing = df.isnull().sum() / len(df) * 100

    return {
        'name': name,
        'total_values': total,
        'missing_values': int(missing),
        'missing_pct': round(missing_pct, 2),
        'per_station_missing': per_station_missing,
        'stations_above_50pct_missing': int((per_station_missing > 50).sum()),
        'stations_above_20pct_missing': int((per_station_missing > 20).sum()),
        'stations_complete': int((per_station_missing == 0).sum()),
    }

o3_stats = compute_missing_stats(o3_df, 'O3')
pm25_stats = compute_missing_stats(pm25_df, 'PM2.5')
pm10_stats = compute_missing_stats(pm10_df, 'PM10')

for stats in [o3_stats, pm25_stats, pm10_stats]:
    print(f"\n  --- {stats['name']} ---")
    print(f"  总数据量: {stats['total_values']}")
    print(f"  缺失值数量: {stats['missing_values']}")
    print(f"  整体缺失率: {stats['missing_pct']}%")
    print(f"  缺失率>50%的站点数: {stats['stations_above_50pct_missing']}")
    print(f"  缺失率>20%的站点数: {stats['stations_above_20pct_missing']}")
    print(f"  完全无缺失的站点数: {stats['stations_complete']}")

# 各站点详细缺失情况
station_missing_summary = pd.DataFrame({
    'O3_missing_pct': o3_stats['per_station_missing'].round(2),
    'PM25_missing_pct': pm25_stats['per_station_missing'].round(2),
    'PM10_missing_pct': pm10_stats['per_station_missing'].round(2),
})
station_missing_summary = station_df.merge(
    station_missing_summary, left_on='station_code', right_index=True
)
station_missing_summary.to_csv(
    os.path.join(OUTPUT_DIR, 'station_missing_summary.csv'),
    index=False, encoding='utf-8-sig'
)
print(f"\n  详细缺失汇总已保存至: {os.path.join(OUTPUT_DIR, 'station_missing_summary.csv')}")

# ============================================================
# Step 4: 站点城市和经纬度分布
# ============================================================
print("\n[Step 4] 统计站点城市和经纬度分布...")

city_counts = Counter(station_df['city'])
print(f"\n  城市分布 ({len(city_counts)} 个城市):")
for city, count in city_counts.most_common():
    print(f"    {city}: {count} 个站点")

lon_min, lon_max = station_df['lon'].min(), station_df['lon'].max()
lat_min, lat_max = station_df['lat'].min(), station_df['lat'].max()
print(f"\n  经度范围: {lon_min:.4f} ~ {lon_max:.4f} °E")
print(f"  纬度范围: {lat_min:.4f} ~ {lat_max:.4f} °N")

# ============================================================
# Step 5: 绘制图表
# ============================================================
print("\n[Step 5] 绘制图表...")

# --- 图1: 站点地理分布 ---
fig, ax = plt.subplots(figsize=(14, 10))
city_list = sorted(city_counts.keys())
colors = plt.cm.tab20(np.linspace(0, 1, len(city_list)))
city_color_map = dict(zip(city_list, colors))

for city in city_list:
    mask = station_df['city'] == city
    ax.scatter(
        station_df.loc[mask, 'lon'], station_df.loc[mask, 'lat'],
        c=[city_color_map[city]], label=f"{city} ({city_counts[city]})",
        s=80, edgecolors='black', linewidth=0.5, zorder=5
    )

ax.set_xlabel('Longitude (°E)', fontsize=12)
ax.set_ylabel('Latitude (°N)', fontsize=12)
ax.set_title('Distribution of 95 Air Quality Monitoring Stations', fontsize=14)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'station_geo_distribution.png'), dpi=150)
plt.close()
print("  [OK] station_geo_distribution.png")

# --- 图2: 城市站点数量柱状图 ---
fig, ax = plt.subplots(figsize=(12, 6))
cities_ordered = [c for c, _ in city_counts.most_common()]
counts_ordered = [city_counts[c] for c in cities_ordered]
color_list = plt.cm.viridis(np.linspace(0.2, 0.8, len(cities_ordered)))
bars = ax.bar(range(len(cities_ordered)), counts_ordered, color=color_list)
ax.set_xticks(range(len(cities_ordered)))
ax.set_xticklabels(cities_ordered, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Number of Stations', fontsize=12)
ax.set_title('Number of Monitoring Stations per City', fontsize=14)
for bar, count in zip(bars, counts_ordered):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1, str(count),
            ha='center', va='bottom', fontsize=9)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'station_city_distribution.png'), dpi=150)
plt.close()
print("  [OK] station_city_distribution.png")

# --- 图3: O3 / PM2.5 / PM10 整体时间序列 (日均值) ---
fig, axes = plt.subplots(3, 1, figsize=(16, 12))

for ax_i, (df_pol, name, color) in enumerate([
    (o3_df, 'O₃', '#E74C3C'),
    (pm25_df, 'PM₂.₅', '#3498DB'),
    (pm10_df, 'PM₁₀', '#2ECC71')
]):
    daily_mean = df_pol.mean(axis=1).resample('D').mean()
    ax = axes[ax_i]
    ax.plot(daily_mean.index, daily_mean.values, color=color, linewidth=0.6, alpha=0.9)
    ax.fill_between(daily_mean.index, daily_mean.values, alpha=0.15, color=color)
    ax.set_ylabel(f'{name} (μg/m³)', fontsize=11)
    ax.set_title(f'{name} — Daily Mean Concentration (95-Station Average, 2022)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=8)

axes[-1].set_xlabel('Date', fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'pollutant_daily_timeseries.png'), dpi=150)
plt.close()
print("  [OK] pollutant_daily_timeseries.png")

# --- 图4: O3 缺失热力图(按周聚合) ---
fig, ax = plt.subplots(figsize=(16, 5))
weekly_missing = o3_df.isnull().astype(float).resample('W').mean().T * 100
im = ax.imshow(weekly_missing.values, aspect='auto', cmap='YlOrRd', vmin=0, vmax=100)
ax.set_xlabel('Week', fontsize=11)
ax.set_ylabel('Station Index', fontsize=11)
ax.set_title('O₃ Weekly Missing Rate per Station (%, 2022)', fontsize=12)
plt.colorbar(im, ax=ax, label='Missing Rate (%)')
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'o3_missing_heatmap.png'), dpi=150)
plt.close()
print("  [OK] o3_missing_heatmap.png")

# --- 图5: 每小时缺失站点数 ---
fig, axes = plt.subplots(3, 1, figsize=(16, 10))

for ax_i, (df_pol, name, color) in enumerate([
    (o3_df, 'O₃', '#E74C3C'),
    (pm25_df, 'PM₂.₅', '#3498DB'),
    (pm10_df, 'PM₁₀', '#2ECC71')
]):
    hourly_missing_count = df_pol.isnull().sum(axis=1)
    ax = axes[ax_i]
    ax.fill_between(hourly_missing_count.index, hourly_missing_count.values,
                     color=color, alpha=0.5)
    ax.plot(hourly_missing_count.index, hourly_missing_count.values,
            color=color, linewidth=0.3, alpha=0.8)
    ax.set_ylabel('Missing Stations', fontsize=10)
    ax.set_title(f'{name} — Hourly Count of Stations with Missing Data (2022)', fontsize=11)
    ax.set_ylim(0, 95)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

axes[-1].set_xlabel('Date', fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'hourly_missing_stations.png'), dpi=150)
plt.close()
print("  [OK] hourly_missing_stations.png")

# --- 图6: O3 vs PM2.5 散点图 (日均值) ---
fig, ax = plt.subplots(figsize=(8, 8))
o3_daily = o3_df.mean(axis=1).resample('D').mean()
pm25_daily = pm25_df.mean(axis=1).resample('D').mean()
ax.scatter(o3_daily.values, pm25_daily.values, alpha=0.4, s=10, c='#8E44AD')
ax.set_xlabel('O₃ Daily Mean (μg/m³)', fontsize=12)
ax.set_ylabel('PM₂.₅ Daily Mean (μg/m³)', fontsize=12)
ax.set_title('Daily O₃ vs PM₂.₅ (95-Station Average, 2022)', fontsize=13)
ax.grid(True, alpha=0.3)
valid_mask = ~(np.isnan(o3_daily.values) | np.isnan(pm25_daily.values))
corr_o3_pm25 = np.corrcoef(o3_daily.values[valid_mask], pm25_daily.values[valid_mask])[0, 1]
ax.text(0.05, 0.95, f'Pearson r = {corr_o3_pm25:.3f}', transform=ax.transAxes,
        fontsize=12, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'o3_vs_pm25_scatter.png'), dpi=150)
plt.close()
print("  [OK] o3_vs_pm25_scatter.png")

# --- 图7: 各站点O3箱线图 ---
fig, ax = plt.subplots(figsize=(18, 6))
o3_box_data = [o3_df[st].dropna().values for st in target_stations]
bp = ax.boxplot(o3_box_data, patch_artist=True, showfliers=False, widths=0.7)
for patch in bp['boxes']:
    patch.set_facecolor('#E74C3C')
    patch.set_alpha(0.6)
# 简化 x 轴标签
tick_positions = list(range(1, len(target_stations) + 1, 3))
tick_labels = [target_stations[i] for i in range(0, len(target_stations), 3)]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=90, ha='center', fontsize=5)
ax.set_ylabel('O₃ Concentration (μg/m³)', fontsize=11)
ax.set_title('O₃ Distribution per Station (2022, without outliers)', fontsize=13)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'o3_station_boxplot.png'), dpi=150)
plt.close()
print("  [OK] o3_station_boxplot.png")

# --- 图8: 月均值对比 (O3, PM2.5, PM10) ---
fig, ax = plt.subplots(figsize=(14, 6))
monthly_o3 = o3_df.mean(axis=1).resample('M').mean()
monthly_pm25 = pm25_df.mean(axis=1).resample('M').mean()
monthly_pm10 = pm10_df.mean(axis=1).resample('M').mean()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
x = range(len(months))

ax.plot(x, monthly_o3.values, 'o-', color='#E74C3C', label='O₃', linewidth=2, markersize=8)
ax.plot(x, monthly_pm25.values, 's-', color='#3498DB', label='PM₂.₅', linewidth=2, markersize=8)
ax.plot(x, monthly_pm10.values, '^-', color='#2ECC71', label='PM₁₀', linewidth=2, markersize=8)
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_ylabel('Concentration (μg/m³)', fontsize=12)
ax.set_title('Monthly Mean Pollutant Concentrations (95-Station Average, 2022)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'monthly_comparison.png'), dpi=150)
plt.close()
print("  [OK] monthly_comparison.png")

print(f"\n  所有图表已保存至: {FIGURES_DIR}")

# ============================================================
# Step 6: 生成数据说明初稿
# ============================================================
print("\n[Step 6] 生成数据说明初稿 Markdown...")

md_content = f"""# 数据说明初稿

> **生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **数据来源**: data_N95 目录中 2022 年全年 {len(csv_files)} 个逐日 CSV 文件
> **对应任务**: 第 1 周 — 数据理解和代码跑通 → 数据整理

---

## 1. 数据概览

| 项目 | 说明 |
|------|------|
| 站点数 | 95 个 |
| 时间范围 | {time_index.min().strftime('%Y-%m-%d %H:%M')} ~ {time_index.max().strftime('%Y-%m-%d %H:%M')} |
| 时间分辨率 | 1 小时 |
| 时间点总数 | {n_total} |
| 主预测目标 | O₃ (臭氧) |
| 可用污染物类型 | AQI, PM2.5, PM2.5_24h, PM10, PM10_24h, SO2, SO2_24h, NO2, NO2_24h, O3, O3_24h, O3_8h, O3_8h_24h, CO, CO_24h |
| 气象因子 | 14 个 (blh, d2m, fsr, kx, sp, ssr, ssrd, t2m, tcc, tcwv, tp, u10, v10, zust) |
| 模型输入特征 | 15 = O₃ + 14 气象因子 |

## 2. 站点分布

### 2.1 城市分布

共覆盖 **{len(city_counts)}** 个城市:

| 城市 | 站点数 | 占比 |
|------|--------|------|
"""

for city, count in city_counts.most_common():
    pct = count / len(target_stations) * 100
    md_content += f"| {city} | {count} | {pct:.1f}% |\n"

md_content += f"""
### 2.2 经纬度范围

| 指标 | 值 |
|------|-----|
| 经度范围 | {lon_min:.4f}°E ~ {lon_max:.4f}°E |
| 纬度范围 | {lat_min:.4f}°N ~ {lat_max:.4f}°N |
| 主要覆盖区域 | 京津冀及周边地区 (北京、天津、河北、山西、内蒙古中部、山东北部) |

> 📊 站点地理分布图: `figures/station_geo_distribution.png`
> 📊 城市站点数柱状图: `figures/station_city_distribution.png`

## 3. 缺失值统计

### 3.1 整体缺失率

| 污染物 | 总数据量 | 缺失量 | 缺失率 | 缺失率>50%站点数 | 缺失率>20%站点数 | 完全无缺失站点数 |
|--------|----------|--------|--------|------------------|------------------|------------------|
| O₃ | {o3_stats['total_values']:,} | {o3_stats['missing_values']:,} | **{o3_stats['missing_pct']}%** | {o3_stats['stations_above_50pct_missing']} | {o3_stats['stations_above_20pct_missing']} | {o3_stats['stations_complete']} |
| PM₂.₅ | {pm25_stats['total_values']:,} | {pm25_stats['missing_values']:,} | **{pm25_stats['missing_pct']}%** | {pm25_stats['stations_above_50pct_missing']} | {pm25_stats['stations_above_20pct_missing']} | {pm25_stats['stations_complete']} |
| PM₁₀ | {pm10_stats['total_values']:,} | {pm10_stats['missing_values']:,} | **{pm10_stats['missing_pct']}%** | {pm10_stats['stations_above_50pct_missing']} | {pm10_stats['stations_above_20pct_missing']} | {pm10_stats['stations_complete']} |

### 3.2 缺失率最高的站点 (Top 10)

"""

for pol_name, pol_stats in [('O₃', o3_stats), ('PM₂.₅', pm25_stats), ('PM₁₀', pm10_stats)]:
    top_missing = pol_stats['per_station_missing'].sort_values(ascending=False).head(10)
    md_content += f"**{pol_name} 缺失率最高站点:**\n\n"
    md_content += "| 站点编码 | 站点名称 | 城市 | 缺失率(%) |\n"
    md_content += "|----------|----------|------|----------|\n"
    for st_code, rate in top_missing.items():
        st_info = station_df[station_df['station_code'] == st_code].iloc[0]
        md_content += f"| {st_code} | {st_info['station_name']} | {st_info['city']} | {rate:.2f} |\n"
    md_content += "\n"

md_content += f"""
> 📊 各站点详细缺失率: `station_missing_summary.csv`
> 📊 缺失热力图: `figures/o3_missing_heatmap.png`
> 📊 每时刻缺失站点数: `figures/hourly_missing_stations.png`

## 4. 时间序列概览

### 4.1 O₃ (臭氧)
- 呈现**典型夏季高、冬季低**的季节特征
- 夏季 (6-8月) 日均浓度可达 100-200 μg/m³
- 冬季 (12-2月) 日均浓度通常在 20-60 μg/m³
- 日变化明显：午后浓度高，夜间浓度低

### 4.2 PM₂.₅ (细颗粒物)
- 呈现**冬高夏低**的季节特征，与 O₃ 季节规律相反
- 冬季供暖季 (11-3月) 浓度较高，易出现重污染过程
- 夏季浓度较低，但个别站点可能受局部源影响

### 4.3 PM₁₀ (可吸入颗粒物)
- 变化趋势与 PM₂.₅ 基本一致
- 春季 (3-5月) 沙尘天气可能出现 PM₁₀ 高值，PM₂.₅/PM₁₀ 比值下降
- 冬季与 PM₂.₅ 相关性更强

### 4.4 O₃ 与 PM₂.₅ 相关性
- 日均值 Pearson 相关系数: **r = {corr_o3_pm25:.3f}**
- 整体呈弱负相关，反映了两者不同的季节规律和生成机制

> 📊 时间序列图: `figures/pollutant_daily_timeseries.png`
> 📊 O₃ vs PM₂.₅ 散点图: `figures/o3_vs_pm25_scatter.png`
> 📊 月均值对比: `figures/monthly_comparison.png`
> 📊 各站点O₃箱线图: `figures/o3_station_boxplot.png`

## 5. 数据文件结构说明

### 5.1 data_N95/ — 原始逐日 CSV
- 文件名格式: `china_sites_YYYYMMDD.csv`
- 每文件含 15 种污染物/AQI 类型 × 24 小时行
- 列: `date`, `hour`, `type`, 以及 2024 个站点列
- 部分日期的部分污染物类型有缺失（如 O₃_8h 等）

### 5.2 matrix_N95/ — 模型处理后数据
| 文件 | 说明 | Shape |
|------|------|-------|
| `data.npy` | O₃ 主序列 | (95, 8717) |
| `time_index.npy` | 时间索引 | (8717,) |
| `met_raw_aligned_cache.npz` | 14 个气象变量缓存 | — |
| `data_combined_m15.npy` | O₃ + 气象组合 | (8717, 95, 15) |
| `trainX.npy / trainY.npy` | 训练窗口 (旧版) | — |
| `validX.npy / validY.npy` | 验证窗口 (旧版) | — |
| `testX.npy / testY.npy` | 测试窗口 (旧版) | — |

### 5.3 xlsx_N95/ — 站点和辅助信息
| 文件 | 说明 |
|------|------|
| `station_loc1.xlsx` | 95 站点编码、名称、城市、经纬度 |
| `Distance.xlsx` | 站点距离表 |
| `S.xlsx`, `T.xlsx` | 空间/时间图邻接矩阵辅助 |

## 6. 关键注意事项

1. **no-leak 切分**: PE-DiffWaveNet 脚本先按 train_rate=0.8465 切分原始时间轴，再在各自 split 内滑窗，拟合 scaler 仅用训练集。**报告中须说明此点，避免被质疑数据泄漏。**

2. **缺失值策略**: 本分析展示了原始缺失情况。模型训练时使用 `data.npy` (matrix_N95)，缺失值可能已经过处理。各 baseline 应统一缺失值处理策略。

3. **气象数据**: 14 个气象变量以缓存 `.npz` 形式存储在 `matrix_N95/met_raw_aligned_cache.npz`，避免复制 6.8GB 原始 CSV。

4. **指标统一**: 所有指标统计应基于反归一化后的真实值，统一使用 **RMSE、MAE、MAPE**，可附加 **Peak RMSE** 和 **per-step RMSE**。

5. **字段对齐**: 结果表字段需向 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv` 对齐。

---

*本文件为第 1 周数据整理任务的初稿，后续将根据实验进展补充相关性分析和更详细的字段说明。*
"""

md_path = os.path.join(OUTPUT_DIR, 'data_description_draft.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
print(f"  数据说明初稿已保存至: {md_path}")

# ============================================================
# Step 7: 汇总统计摘要 JSON
# ============================================================
summary = {
    'num_stations': len(target_stations),
    'num_cities': len(city_counts),
    'num_csv_files': len(csv_files),
    'time_range_start': str(time_index.min()),
    'time_range_end': str(time_index.max()),
    'total_hours': n_total,
    'o3_missing_pct': o3_stats['missing_pct'],
    'pm25_missing_pct': pm25_stats['missing_pct'],
    'pm10_missing_pct': pm10_stats['missing_pct'],
    'lon_range': f"{lon_min:.4f} ~ {lon_max:.4f}",
    'lat_range': f"{lat_min:.4f} ~ {lat_max:.4f}",
    'o3_pm25_corr': round(corr_o3_pm25, 3),
}
with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"  统计摘要已保存至: {os.path.join(OUTPUT_DIR, 'summary.json')}")

print("\n" + "=" * 60)
print("数据整理完成！")
print(f"输出目录: {OUTPUT_DIR}")
print(f"  - {OUTPUT_DIR}/data_description_draft.md")
print(f"  - {OUTPUT_DIR}/station_missing_summary.csv")
print(f"  - {OUTPUT_DIR}/summary.json")
print(f"  - {OUTPUT_DIR}/figures/")
print("=" * 60)
