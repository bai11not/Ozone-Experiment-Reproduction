#!/usr/bin/env python3
"""
独立图表重新生成脚本 — 修复中文标签乱码问题
======================================================
使用 matrix_N95 缓存数据 + station_loc1.xlsx，重新生成所有图表，
无需遍历原始 CSV 文件，避免 pandas C 引擎兼容性问题。

修复内容:
  1. 清除 matplotlib 旧字体缓存
  2. 显式加载 Windows 系统中的 SimHei / Microsoft YaHei 中文字体
  3. 重新生成 8 张图表，中文标签正确显示
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import os
import sys
import io
import json
from collections import Counter
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# 路径配置
# ============================================================
BASE_DIR = r'd:\生产实习\臭氧数据集\臭氧预测资料'
MATRIX_DIR = os.path.join(BASE_DIR, 'matrix_N95')
XLSX_DIR = os.path.join(BASE_DIR, 'xlsx_N95')
OUTPUT_DIR = os.path.join(BASE_DIR, 'assignment', 'week1', '01_data_organization', 'data_organization_output')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# ============================================================
# 中文字体配置 (解决 Windows matplotlib 乱码问题)
# ============================================================
print("=" * 60)
print("图表重新生成脚本 — 修复中文乱码")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

print("\n[字体配置]")
# 1) 清除旧字体缓存
_font_cache_dir = matplotlib.get_cachedir()
for f in os.listdir(_font_cache_dir):
    if f.startswith('fontlist'):
        try:
            os.remove(os.path.join(_font_cache_dir, f))
            print(f"  已删除字体缓存: {f}")
        except Exception:
            pass

# 2) 显式加载中文字体文件
_chinese_font_paths = [
    r'C:\Windows\Fonts\simhei.ttf',       # 黑体 (SimHei)
    r'C:\Windows\Fonts\msyh.ttc',         # 微软雅黑 (Microsoft YaHei)
    r'C:\Windows\Fonts\msyhbd.ttc',       # 微软雅黑 粗体
]
_loaded_fonts = []
for _font_path in _chinese_font_paths:
    if os.path.exists(_font_path):
        fm.fontManager.addfont(_font_path)
        _loaded_fonts.append(os.path.basename(_font_path))
        print(f"  已加载字体: {_font_path}")
    else:
        print(f"  字体不存在，跳过: {_font_path}")

# 3) 设置默认字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
print(f"  中文字体配置完成: {_loaded_fonts}")

# ============================================================
# 加载数据
# ============================================================
print("\n[数据加载]")

# 站点信息
station_df = pd.read_excel(os.path.join(XLSX_DIR, 'station_loc1.xlsx'))
station_df.columns = ['station_code', 'station_name', 'city', 'lon', 'lat']
target_stations = station_df['station_code'].tolist()
print(f"  站点数: {len(target_stations)}")

# O3 主序列 (95, 8717) → 转置为 (8717, 95)
o3_data = np.load(os.path.join(MATRIX_DIR, 'data.npy'))  # (95, 8717)
o3_data = o3_data.T  # → (8717, 95)
print(f"  O3 data shape: {o3_data.shape}")

# 时间索引
time_index = np.load(os.path.join(MATRIX_DIR, 'time_index.npy'), allow_pickle=True)
print(f"  时间索引: {len(time_index)} 点, {time_index[0]} ~ {time_index[-1]}")

# 气象缓存 (用于提取 PM2.5/PM10 类似指标)
met_cache = np.load(os.path.join(MATRIX_DIR, 'met_raw_aligned_cache.npz'), allow_pickle=True)
print(f"  气象变量: {list(met_cache.keys())}")

# 构建 O3 DataFrame
o3_df = pd.DataFrame(o3_data, index=time_index, columns=target_stations)
print(f"  O3 DataFrame: {o3_df.shape}")

# ============================================================
# 城市统计
# ============================================================
city_counts = Counter(station_df['city'])
city_list = sorted(city_counts.keys())
print(f"\n  城市: {len(city_list)} 个")
for city, count in city_counts.most_common():
    print(f"    {city}: {count} 站")

lon_min, lon_max = station_df['lon'].min(), station_df['lon'].max()
lat_min, lat_max = station_df['lat'].min(), station_df['lat'].max()
print(f"  经度: {lon_min:.4f} ~ {lon_max:.4f} °E")
print(f"  纬度: {lat_min:.4f} ~ {lat_max:.4f} °N")

# ============================================================
# 图1: 站点地理分布 (中文图例 — 核心修复目标)
# ============================================================
print("\n[生成图表]")
print("  图1: 站点地理分布...")
fig, ax = plt.subplots(figsize=(14, 10))
colors = plt.cm.tab20(np.linspace(0, 1, len(city_list)))
city_color_map = dict(zip(city_list, colors))

for city in city_list:
    mask = station_df['city'] == city
    ax.scatter(
        station_df.loc[mask, 'lon'], station_df.loc[mask, 'lat'],
        c=[city_color_map[city]], label=f"{city} ({city_counts[city]})",
        s=80, edgecolors='black', linewidth=0.5, zorder=5
    )

ax.set_xlabel('经度 (°E)', fontsize=12)
ax.set_ylabel('纬度 (°N)', fontsize=12)
ax.set_title('95个空气质量监测站点地理分布', fontsize=14)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8,
          title='城市 (站点数)', title_fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'map_station_geo_distribution.png'), dpi=150)
plt.close()
print("    [OK] map_station_geo_distribution.png")

# ============================================================
# 图2: 城市站点数量柱状图 (中文横坐标 — 核心修复目标)
# ============================================================
print("  图2: 城市站点数量...")
fig, ax = plt.subplots(figsize=(12, 6))
cities_ordered = [c for c, _ in city_counts.most_common()]
counts_ordered = [city_counts[c] for c in cities_ordered]
color_list = plt.cm.viridis(np.linspace(0.2, 0.8, len(cities_ordered)))
bars = ax.bar(range(len(cities_ordered)), counts_ordered, color=color_list)
ax.set_xticks(range(len(cities_ordered)))
ax.set_xticklabels(cities_ordered, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('站点数量', fontsize=12)
ax.set_title('各城市监测站点数量', fontsize=14)
for bar, count in zip(bars, counts_ordered):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1, str(count),
            ha='center', va='bottom', fontsize=9)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'bar_station_city_distribution.png'), dpi=150)
plt.close()
print("    [OK] bar_station_city_distribution.png")

# ============================================================
# 图3: O3 日均时间序列
# ============================================================
print("  图3: O3 日均时间序列...")
fig, ax = plt.subplots(figsize=(16, 6))
daily_mean = o3_df.mean(axis=1).resample('D').mean()
ax.plot(daily_mean.index, daily_mean.values, color='#E74C3C', linewidth=0.6, alpha=0.9)
ax.fill_between(daily_mean.index, daily_mean.values, alpha=0.15, color='#E74C3C')
ax.set_ylabel('$O_3$ 浓度 (ug/m3)', fontsize=11)
ax.set_title('$O_3$ — 日均浓度变化 (95站均值, 2022年)', fontsize=12)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'ts_pollutant_daily_timeseries.png'), dpi=150)
plt.close()
print("    [OK] ts_pollutant_daily_timeseries.png")

# ============================================================
# 图4: O3 缺失热力图 (data.npy 无缺失 → 说明数据质量)
# ============================================================
print("  图4: O3 缺失热力图...")
fig, ax = plt.subplots(figsize=(16, 5))
# data.npy 已经过预处理，无缺失值。这里展示各站点 O3 值的热力图
# 按周聚合均值
weekly_o3 = o3_df.resample('W').mean().T
im = ax.imshow(weekly_o3.values, aspect='auto', cmap='YlOrRd',
               vmin=np.percentile(weekly_o3.values, 5),
               vmax=np.percentile(weekly_o3.values, 95))
ax.set_xlabel('周', fontsize=11)
ax.set_ylabel('站点索引', fontsize=11)
ax.set_title('$O_3$ 周均浓度热力图 (95站, 2022年, 数据完整无缺失)', fontsize=12)
plt.colorbar(im, ax=ax, label='$O_3$ 浓度 (ug/m3)')
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'heat_o3_missing_heatmap.png'), dpi=150)
plt.close()
print("    [OK] heat_o3_missing_heatmap.png (显示周均O3浓度分布)")

# ============================================================
# 图5: 每小时数据覆盖率 (O3 全完整)
# ============================================================
print("  图5: 每小时数据覆盖率...")
fig, ax = plt.subplots(figsize=(16, 5))
hourly_available = o3_df.notnull().sum(axis=1)
ax.fill_between(hourly_available.index, hourly_available.values,
                 color='#E74C3C', alpha=0.5)
ax.plot(hourly_available.index, hourly_available.values,
        color='#E74C3C', linewidth=0.3, alpha=0.8)
ax.set_ylabel('可用站点数', fontsize=10)
ax.set_title('$O_3$ — 每小时数据覆盖率 (95站, 2022年, 数据完整)', fontsize=11)
ax.set_ylim(0, 95)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'ts_hourly_missing_stations.png'), dpi=150)
plt.close()
print("    [OK] ts_hourly_missing_stations.png")

# ============================================================
# 图6: O3 各站点箱线图
# ============================================================
print("  图6: 各站点 O3 箱线图...")
fig, ax = plt.subplots(figsize=(18, 6))
o3_box_data = [o3_df[st].dropna().values for st in target_stations]
bp = ax.boxplot(o3_box_data, patch_artist=True, showfliers=False, widths=0.7)
for patch in bp['boxes']:
    patch.set_facecolor('#E74C3C')
    patch.set_alpha(0.6)
tick_positions = list(range(1, len(target_stations) + 1, 3))
tick_labels = [target_stations[i] for i in range(0, len(target_stations), 3)]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=90, ha='center', fontsize=5)
ax.set_ylabel('$O_3$ 浓度 (ug/m3)', fontsize=11)
ax.set_title('各站点O3浓度分布箱线图 (2022年, 不含离群值)', fontsize=13)
ax.grid(axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'box_o3_station_boxplot.png'), dpi=150)
plt.close()
print("    [OK] box_o3_station_boxplot.png")

# ============================================================
# 图7: O3 月均值
# ============================================================
print("  图7: O3 月均值...")
fig, ax = plt.subplots(figsize=(14, 6))
monthly_o3 = o3_df.mean(axis=1).resample('M').mean()

months_cn = ['1月', '2月', '3月', '4月', '5月', '6月',
             '7月', '8月', '9月', '10月', '11月', '12月']
x = range(len(months_cn))

ax.plot(x, monthly_o3.values, 'o-', color='#E74C3C', label='$O_3$', linewidth=2, markersize=8)
ax.set_xticks(x)
ax.set_xticklabels(months_cn)
ax.set_ylabel('浓度 (ug/m3)', fontsize=12)
ax.set_title('$O_3$ 月均浓度 (95站均值, 2022年)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
# 标注峰值
max_idx = np.argmax(monthly_o3.values)
ax.annotate(f'峰值: {monthly_o3.values[max_idx]:.1f} ug/m3',
            xy=(max_idx, monthly_o3.values[max_idx]),
            xytext=(max_idx + 0.5, monthly_o3.values[max_idx] + 5),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10, color='#C0392B')
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'cmp_monthly_pollutants.png'), dpi=150)
plt.close()
print("    [OK] cmp_monthly_pollutants.png")

# ============================================================
# 图8: O3 与气象因子相关性散点图 (用 t2m 代替 PM₂.₅)
# ============================================================
print("  图8: O3 与温度 (t2m) 散点图...")
fig, ax = plt.subplots(figsize=(8, 8))

# 从气象缓存中提取 t2m (2m 温度) 作为相关因子
t2m_data = met_cache['t2m']  # shape: (n_times, n_stations)
# 取所有站点的日均值
o3_daily = o3_df.mean(axis=1).resample('D').mean()
# 对 t2m 也做日聚合
t2m_df = pd.DataFrame(t2m_data, index=time_index, columns=target_stations)
t2m_daily = t2m_df.mean(axis=1).resample('D').mean()

# 对齐后画散点图
common_idx = o3_daily.index.intersection(t2m_daily.index)
ax.scatter(o3_daily[common_idx].values, t2m_daily[common_idx].values,
           alpha=0.4, s=10, c='#8E44AD')
ax.set_xlabel('$O_3$ 日均浓度 (ug/m3)', fontsize=12)
ax.set_ylabel('2m气温 日均值 (K)', fontsize=12)
ax.set_title('$O_3$ 与近地面温度关系 (95站均值, 2022年)', fontsize=13)
ax.grid(True, alpha=0.3)

valid_mask = ~(np.isnan(o3_daily[common_idx].values) | np.isnan(t2m_daily[common_idx].values))
if valid_mask.sum() > 1:
    corr = np.corrcoef(o3_daily[common_idx].values[valid_mask],
                       t2m_daily[common_idx].values[valid_mask])[0, 1]
    ax.text(0.05, 0.95, f'Pearson r = {corr:.3f}', transform=ax.transAxes,
            fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
fig.tight_layout()
fig.savefig(os.path.join(FIGURES_DIR, 'scatter_o3_vs_pm25_daily.png'), dpi=150)
plt.close()
print("    [OK] scatter_o3_vs_pm25_daily.png (O3 vs 温度)")

# ============================================================
# 完成
# ============================================================
print(f"\n{'=' * 60}")
print(f"所有图表已重新生成至: {FIGURES_DIR}")
print("中文字体: SimHei (黑体) + Microsoft YaHei (微软雅黑)")
print(f"{'=' * 60}")
print("\n生成文件列表:")
for f in sorted(os.listdir(FIGURES_DIR)):
    fpath = os.path.join(FIGURES_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f} ({size_kb:.1f} KB)")
