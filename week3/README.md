# Week 3: 图表数据整理

> 所有图在 Origin 中完成，本文件夹只存数据和图表项目文件。

## 文件架构

```
week3/
├── README.md                    ← 本文件
├── data/                        ← 提取好的 CSV 数据
│   ├── 1_main_table.csv
│   ├── 2_ablation_table.csv
│   ├── 3_perstep_rmse.csv
│   ├── 4_predictions.csv        ← 需从输出目录提取
│   ├── 5_station_error.csv      ← 需从输出目录提取
│   ├── 6_peak_error.csv
│   └── 7_pe_waterfall.csv
├── charts/                      ← Origin .opju 项目文件
└── output/                      ← 导出的 PNG/TIFF
```

---

## 图表 1: 主对比表

**说明**: PE-DiffWaveNet vs DiffSTG，列出最优配置的 RMSE/MAE/MAPE

**数据来源**: `week2/metrics/week2_summary.csv`

**数据行**:
- PE-DiffWaveNet full, seq=24, pre=6, seed=42 → A08: RMSE 11.07
- PE-DiffWaveNet full, seq=24, pre=3, seed=42 → A06: RMSE **8.62** (最佳)
- PE-DiffWaveNet full, seq=24, pre=6, seed=52 → C04: RMSE 11.01
- DiffSTG O3 → RMSE 0.0628 (z-score, 需换算)
- DiffSTG PM2.5 → RMSE 0.0537
- DiffSTG PM10 → RMSE 0.0400

**操作**: 手动录入 Origin 工作簿，加表头格式导出

---

## 图表 2: 消融实验表

**说明**: 固定 pre=6, seq=24，4 种消融类型的 RMSE 对比

**数据来源**: `week2_summary.csv`

**数据**:
| 消融 | seed=42 | seed=52 |
|------|:---:|:---:|
| full | A08: 11.07 | C04: 11.01 |
| no_diff | A04: 11.04 | C08: 10.88 |
| no_pe_graph | B03: 11.60 | D03: 11.11 |
| no_pe_film | B07: 12.06 | D07: 11.31 |

**Origin**: 分组柱状图，X=消融类型，Y=RMSE，两组柱=seed42/52

---

## 图表 3: 不同预长误差曲线

**说明**: per-step RMSE 折线图，看 RMSE 随预测步长增长

**数据来源**: 每个实验的 `metrics_summary.json` → `per_step_rmse`

**数据提取**: 见下方说明

**图 3A**: full 模型 pre=1,3,6,12,24 的 per-step RMSE
- E01 (pre=1): 1 个值
- A06 (pre=3): 3 个值
- A08 (pre=6): 6 个值
- E02 (pre=12): 12 个值
- E03 (pre=24): 24 个值

**图 3B**: 同 pre=6，4 种消融对比
- full (A08), no_diff (A04), no_pe_graph (B03), no_pe_film (B07)

**Origin**: X=Step, Y=RMSE，每条曲线一个实验

---

## 图表 4: 真实值 vs 预测值 ⚠️

**说明**: 取最佳模型 (A06)，选某个站点某个时间段画预测 vs 真实对比

**数据来源**: A06 的 `test_predictions.npy` + `test_targets.npy`

**文件位置**: 
```
臭氧预测资料/matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p3_l24_s42/
├── test_predictions.npy   ← 预测值
└── test_targets.npy       ← 真实值
```

**提取方法**: 把你的文件路径告诉我，我帮你跑脚本提取成 CSV

**Origin**: 散点图或折线图，X=时间, Y=臭氧值, 两条线=真实/预测

---

## 图表 5: 站点误差分布 ⚠️

**说明**: 95 个站点各自的 RMSE，看哪些站点预测不准

**数据来源**: 同上文件，按站点算 RMSE

**提取方法**: `test_predictions.npy` shape=(N_test, pre_len, 95)，第 3 维=站点

**Origin**: 柱状图，X=站点ID, Y=RMSE

---

## 图表 6: 高值区误差

**说明**: 峰值时刻的预测误差

**数据来源**: 每个实验 `metrics_summary.json` → `peak_rmse`、`peak_mae`

**数据**: 直接从已有 metrics_summary.json 取值，和图表 2 一起画

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