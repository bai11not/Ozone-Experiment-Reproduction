# Week 3: 图表数据整理

> 所有图在 Origin 中完成，本文件夹只存数据和图表项目文件。

## 文件架构

```
week3/
├── README.md                    ← 本文件
├── data/                        ← 提取好的 CSV 数据
│   ├── 1_main_table.csv         ← 主对比表
│   ├── 2_ablation_table.csv     ← 消融实验表（含 seed=42/52/62）
│   ├── 3a_perstep_prelen.csv    ← 不同预测步长 per-step RMSE
│   ├── 3b_perstep_ablation.csv  ← 消融对比 per-step RMSE（含 seed=42/52/62）
│   ├── 4_predictions_station0~40.csv
│   ├── 5_station_error.csv
│   ├── 6_peak_error.csv         ← 峰值误差对比（含 seed=42/52/62）
│   ├── 7_pe_features.csv        ← PE 多尺度特征
│   ├── 8_ci_avg_station20.csv
│   └── 8_ci_station20.csv
├── scripts/                     ← 数据提取脚本
│   ├── extract_predictions.py
│   └── extract_station_error.py
└── output/                      ← 导出的 PNG/TIFF
```

---

## 图表 1: 主对比表

**说明**: PE-DiffWaveNet vs DiffSTG，列出最优配置的 RMSE/MAE/MAPE

**数据来源**: `week2/metrics/week2_summary.csv`

**数据行**:
- PE-DiffWaveNet full, seq=24, pre=6, seed=42 → A08: RMSE 11.07
- PE-DiffWaveNet full, seq=24, pre=3, seed=42 → A06: RMSE **8.62** (最佳)

**Origin**: 手动录入或导入 `1_main_table.csv`

---

## 图表 2: 消融实验表

**说明**: 固定 pre=6, seq=24，4 种消融类型的 RMSE 对比（3 seed）

**数据来源**: `2_ablation_table.csv`

| 消融 | seed=42 | seed=52 | seed=62 |
|------|:-------:|:-------:|:-------:|
| full | A08: 11.07 | C03: 11.01 | C11: 11.68 |
| no_diff | A04: 11.04 | C07: 11.05 | C15: 10.68 |
| no_pe_graph | B03: 11.60 | D03: 11.44 | A12: 11.16 |
| no_pe_film | B07: 12.06 | D07: 11.60 | E08: 12.49 |

**Origin**: 分组柱状图，X=消融类型，Y=RMSE，每组 3 根柱=seed42/52/62

---

## 图表 3: 不同预长误差曲线

**说明**: per-step RMSE 折线图，看 RMSE 随预测步长增长

**数据来源**: `3a_perstep_prelen.csv`

**图 3A**: full 模型 pre=1,3,6,12,24 的 per-step RMSE
- E01 (pre=1): 1 个值
- A06 (pre=3): 3 个值
- A08 (pre=6): 6 个值
- E02 (pre=12): 12 个值
- E03 (pre=24): 24 个值

**图 3B**: 同 pre=6，4 种消融对比（seed=42）
- full (A08), no_diff (A04), no_pe_graph (B03), no_pe_film (B07)

**Origin**: X=Step, Y=RMSE，每条曲线一个实验

---

## 图表 4: 真实值 vs 预测值

**说明**: 取最佳模型 (A06)，选某个站点画预测 vs 真实对比

**数据来源**: A06 的 `test_predictions.npy` + `test_targets.npy`，已提取为 `4_predictions_station*.csv`

**Origin**: 折线图，X=时间, Y=臭氧值, 两条线=真实/预测

---

## 图表 5: 站点误差分布

**说明**: 95 个站点各自的 RMSE

**数据来源**: `5_station_error.csv`

**Origin**: 柱状图，X=站点ID, Y=RMSE

---

## 图表 6: 峰值误差对比

**说明**: 峰值时刻的预测误差（3 seed × 4 消融类型）

**数据来源**: `6_peak_error.csv`

| 消融 | seed=42 RMSE | seed=52 RMSE | seed=62 RMSE |
|------|:-----------:|:-----------:|:-----------:|
| full | 13.93 | 12.08 | 14.04 |
| no_diff | 15.36 | 13.66 | 13.43 |
| no_pe_graph | 13.19 | 12.69 | 13.39 |
| no_pe_film | 13.16 | 15.17 | 13.79 |

**Origin**: 分组柱状图，和图表 2 样式一致

---

## 图表 7: PE 消融瀑布图

**说明**: 从 full 模型开始，逐个关闭组件，RMSE 如何退化

**数据**: 固定 seed=42, pre=6, seq=24
| 配置 | RMSE |
|------|:---:|
| full (d=1,g=1,f=1) | A08: 11.07 |
| no_diff (d=0) | A04: 11.04 |
| no_pe_graph (g=0) | B03: 11.60 |
| no_pe_film (f=0) | B07: 12.06 |

**Origin**: 瀑布图 (Waterfall)

---

## 图表 8: DiffSTG 概率预测

**说明**: DiffSTG 的概率预测结果可视化

- DiffSTG 不同预测步长误差曲线
- DiffSTG 多污染物预测对比
- DiffSTG 概率预测置信区间
- DIFFSTG 各实验概率评分（CRPS）对比
- DiffSTG 邻接矩阵对比

**数据来源**: DiffSTG 实验输出