# 图表命名规范

> **版本**: v1.0
> **日期**: 2026-07-06
> **用途**: 统一所有实验产出的图表命名，确保可追溯

---

## 1. 命名规则

```
{category}_{content}_{config}[_{suffix}].{ext}
```

### 1.1 分类前缀 (category)

| 前缀 | 用途 |
|------|------|
| `ts_` | 时间序列图 (Time Series) |
| `cmp_` | 对比图 (Comparison) |
| `err_` | 误差分析图 (Error Analysis) |
| `dist_` | 分布图 (Distribution) |
| `heat_` | 热力图 (Heatmap) |
| `bar_` | 柱状图 (Bar Chart) |
| `scatter_` | 散点图 (Scatter) |
| `box_` | 箱线图 (Boxplot) |
| `map_` | 地图/空间分布 (Map) |
| `ablation_` | 消融分析图 (Ablation) |

### 1.2 内容标识 (content)

| 标识 | 说明 |
|------|------|
| `o3` / `pm25` / `pm10` | 污染物类型 |
| `pred_vs_true` | 预测值 vs 真实值 |
| `per_step` | 逐预测步长 |
| `station` | 站点维度 |
| `daily` / `monthly` / `seasonal` | 时间聚合粒度 |
| `missing` | 缺失值相关 |
| `pe_stratified` | PE 分层 |
| `correlation` | 相关性分析 |
| `peak` | 高值区 |

### 1.3 配置标识 (config)

| 标识 | 格式 | 示例 |
|------|------|------|
| 序列长度 | `L{seq_len}` | `L24` |
| 预测步长 | `P{pre_len}` | `P6` |
| 随机种子 | `S{seed}` | `S42` |
| 扩散开关 | `D1` / `D0` | `D1` |
| PE图开关 | `G1` / `G0` | `G1` |
| PE FiLM开关 | `F1` / `F0` | `F1` |
| 模型名 | `{model}` | `pedw`, `mtgnn`, `agcrn` |

---

## 2. 标准图表清单

### 2.1 主对比图

| 文件名 | 说明 |
|--------|------|
| `cmp_main_rmse_bar.png` | 主模型 vs baseline RMSE 柱状图 |
| `cmp_main_mae_bar.png` | 主模型 vs baseline MAE 柱状图 |
| `cmp_main_table.png` | Table1 风格汇总表 |
| `ts_pred_vs_true_L24_P6_S42.png` | 真实值 vs 预测值曲线 |
| `ts_pred_vs_true_L24_P6_S42_test.png` | 测试集真实值 vs 预测值 |

### 2.2 多步长预测图

| 文件名 | 说明 |
|--------|------|
| `err_per_step_rmse_all.png` | 所有模型 per-step RMSE 曲线 |
| `err_per_step_mae_all.png` | 所有模型 per-step MAE 曲线 |
| `err_per_step_rmse_pedw_P1_3_6_12_24.png` | PE-DiffWaveNet 不同 pre_len 的 per-step RMSE |

### 2.3 消融分析图

| 文件名 | 说明 |
|--------|------|
| `ablation_rmse_bar.png` | 消融实验 RMSE 柱状图 |
| `ablation_mae_bar.png` | 消融实验 MAE 柱状图 |
| `ablation_per_step_rmse.png` | 消融 per-step RMSE 对比 |
| `ablation_table.png` | Table2 风格消融表 |

### 2.4 站点误差分析图

| 文件名 | 说明 |
|--------|------|
| `dist_station_rmse_hist.png` | 站点 RMSE 分布直方图 |
| `dist_station_mae_hist.png` | 站点 MAE 分布直方图 |
| `map_station_rmse_geo.png` | 站点 RMSE 地理分布热力图 |
| `box_station_o3_rmse.png` | 各站点 O3 RMSE 箱线图 |

### 2.5 PE 分层分析图

| 文件名 | 说明 |
|--------|------|
| `bar_pe_stratified_rmse.png` | PE 分层 RMSE (low/mid/high) |
| `bar_pe_stratified_mae.png` | PE 分层 MAE |
| `scatter_pe_score_vs_rmse.png` | PE score vs 站点 RMSE 散点图 |
| `heat_pe_stratified_per_step.png` | PE 分层 per-step RMSE 热力图 |

### 2.6 高值区分析图

| 文件名 | 说明 |
|--------|------|
| `err_peak_scatter_L24_P6_S42.png` | 高值区预测 vs 真实散点图 |
| `err_peak_rmse_bar.png` | 高值区 / 整体 RMSE 对比 |
| `ts_peak_events_L24_P6_S42.png` | 典型高值事件预测曲线 |

### 2.7 数据探索图 (Week 1)

| 文件名 | 说明 |
|--------|------|
| `map_station_geo_distribution.png` | 站点地理分布 |
| `bar_station_city_distribution.png` | 城市站点数柱状图 |
| `ts_pollutant_daily_timeseries.png` | O3/PM2.5/PM10 日均时间序列 |
| `heat_o3_missing_heatmap.png` | O3 缺失热力图 |
| `ts_hourly_missing_stations.png` | 每时缺失站点数 |
| `scatter_o3_vs_pm25_daily.png` | O3 vs PM2.5 散点图 |
| `box_o3_station_boxplot.png` | 各站点 O3 箱线图 |
| `cmp_monthly_pollutants.png` | 月均值对比 |

---

## 3. 输出目录规范

```
figures/
├── data_exploration/        # 数据探索图 (Week 1)
├── main_comparison/         # 主对比图 (Week 2-3)
├── per_step/                # 逐步长预测图 (Week 2-3)
├── ablation/                # 消融实验图 (Week 2-3)
├── station_error/           # 站点误差图 (Week 3)
├── pe_stratified/           # PE 分层图 (Week 3)
└── peak_analysis/           # 高值区分析图 (Week 3)
```

---

## 4. 格式规范

| 参数 | 值 |
|------|-----|
| 分辨率 | 150 dpi (屏幕), 300 dpi (报告) |
| 格式 | PNG (默认), PDF (论文用) |
| 字体 | DejaVu Sans / SimHei (中文), 字号 8-14 |
| 颜色 | Tableau 10 / Viridis colormap |
| 图例 | 置于图外右侧或下方，字号 ≥ 8 |
| 坐标轴标签 | 含单位和中文/英文说明 |

---

## 5. 与 paper_assets 的对应关系

| Paper Assets 表 | 对应图表 |
|-----------------|---------|
| `table1_main_raw_comparison.csv` | `cmp_main_rmse_bar.png` + `cmp_main_table.png` |
| `table2_ablation.csv` | `ablation_rmse_bar.png` + `ablation_per_step_rmse.png` |
| `table3_pe_stratified_summary.csv` | `bar_pe_stratified_rmse.png` + `scatter_pe_score_vs_rmse.png` |
