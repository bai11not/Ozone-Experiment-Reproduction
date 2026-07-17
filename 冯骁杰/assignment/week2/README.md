# Week 2: 批量实验

> **完成日期**: 2026-07-14 ~ 2026-07-15
> **对应任务**: 三周安排与分工 — 第 2 周
> **模型**: PE-DiffWaveNet | **数据**: matrix_N95 (95 站点 O₃, 2022 全年)

---

## 目录结构

```
week2/
├── README.md                              # 本文件
├── experiment_comparison_summary.md       # 12 组实验多维度对比分析报告
├── experiment_reflection.md               # 实验心得与体会
├── results_summary_all.csv                # 汇总结果表（12 组有效 + 1 组已删除）
│
├── g3_pedw_p6_l24_s42/                    # 实验 0: 基准实验（全组件 s42）
├── g3_nodiff_pe_p6_l24_s42/               # 实验 0b: 基准 noDiff 消融
├── g3_pedw_p3_l24_s42/                    # 实验 1: pre_len=3 s42
├── g3_pedw_p3_l12_s42/                    # 实验 2: seq12 pre3 s42
├── g3_pedw_p6_l12_s42/                    # 实验 3: seq12 pre6 s42
├── g3_nodiff_pe_p3_l24_s42/               # 实验 4: noDiff pre3 s42
├── g3_nodiff_pe_p3_l12_s42/               # 实验 5: noDiff seq12 pre3 s42
├── g3_nodiff_pe_p6_l12_s42/               # 实验 6: noDiff seq12 pre6 s42
├── g3_pedw_p6_l12_s62/                    # 实验 7: 主实验 seq12 pre6 s62
├── g3_pedw_p3_l12_s62/                    # 实验 8: 主实验 seq12 pre3 s62
├── g3_pedw_p3_l24_s62/                    # 实验 9: 主实验 seq24 pre3 s62
└── g3_pedw_p6_l24_s62/                    # 实验 10: 主实验 seq24 pre6 s62

每组实验均按规范包含 4 个文件（training.log / results.csv / experiment_log.md / commands.sh）
```

---

## 实验矩阵完成情况

### 参数扫描 + 多种子（7 组）

| # | 实验 ID | seq/pre | diff | PE Graph | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:--:|
| 0 | `g3_pedw_p6_l24_s42` | 24/6 | 1 | 1 | 42 | ✅ 基准 |
| 1 | `g3_pedw_p3_l24_s42` | 24/3 | 1 | 1 | 42 | ✅ |
| 2 | `g3_pedw_p3_l12_s42` | 12/3 | 1 | 1 | 42 | ✅ |
| 3 | `g3_pedw_p6_l12_s42` | 12/6 | 1 | 1 | 42 | ✅ |
| 7 | `g3_pedw_p6_l12_s62` | 12/6 | 1 | 1 | 62 | ✅ |
| 8 | `g3_pedw_p3_l12_s62` | 12/3 | 1 | 1 | 62 | ✅ |
| 9 | `g3_pedw_p3_l24_s62` | 24/3 | 1 | 1 | 62 | ✅ |
| 10 | `g3_pedw_p6_l24_s62` | 24/6 | 1 | 1 | 62 | ✅ |

### 扩散模块消融（4 组，seed=42）

| # | 实验 ID | seq/pre | diff | PE Graph | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:--:|
| 0b | `g3_nodiff_pe_p6_l24_s42` | 24/6 | **0** | 1 | 42 | ✅ |
| 4 | `g3_nodiff_pe_p3_l24_s42` | 24/3 | **0** | 1 | 42 | ✅ |
| 5 | `g3_nodiff_pe_p3_l12_s42` | 12/3 | **0** | 1 | 42 | ✅ |
| 6 | `g3_nodiff_pe_p6_l12_s42` | 12/6 | **0** | 1 | 42 | ✅ |

### 待实验

| 实验类型 | 配置 | 状态 |
|----------|------|:--:|
| PE Graph 消融 | use_pe_graph=0 × 4 配置 (seed=62) | ⚠️ 需重跑（代码 bug 已修复） |
| PE FiLM 消融 | USE_PE_FILM=0 | ⏳ |
| PE shuffle | PE_SHUFFLE_SEED=52 | ⏳ |
| Baseline | ATGCN-PE3, DiffSTG | ⏳ |

> ⚠️ 之前 4 组 noPEgraph 实验因 PE 缓存代码 bug（`PE_mat` 置零未生效）实为完整 PE Graph=1 主实验，已更名为 `g3_pedw_*` 归入参数扫描。

---

## 关键成果

### 参数分析

- **pre_len 是第一因素**：6→3，RMSE ↓ **22%**，MAPE ↓ **6-7pp**
- **seq_len 其次**：24→12，RMSE ↑ **5%**，MAPE ↑ **3-4pp**
- 参数重要性排序：`pre_len ≫ seq_len ≫ seed > diffusion`

### 扩散模块消融

- 关闭扩散后整体 RMSE 变化 < 3%，但 **Peak RMSE 恶化 1.4~1.8**
- 扩散模块的核心价值在**高浓度 O₃ 峰值预测**，而非平均精度
- 短预测步长（pre_len=3）下扩散的峰值优势减弱

### 多种子

- seed 42→62：RMSE Δ 0.05~0.76（seq24 pre6 波动最大）
- **跨种子对比不可靠**，消融实验必须同种子

### 最佳配置

`seed=42, seq_len=24, pre_len=3, use_diffusion=1` → **RMSE=8.62, MAPE=24.00%**

---

## 代码修改

| 文件 | 修改内容 |
|------|----------|
| `code/pe_step1_fix.py` | **新建**：纯 Python PE 滑动计算（替代 numpy 向量化版本，避免内存损坏） |
| `code/train_atgcn_pe3_noleak.py` | 导入 `average_sliding_pe_fast`；委托 `average_sliding_pe` |
| `code/train_atgcn_pe3.py` | 替换 geographiclib 为纯 Python Haversine；导入 `S_adjacency_matrix` |
| `code/train_pediffwavenet_noleak.py` | PE 缓存加载逻辑；导入 `S_adjacency_matrix`/`T_adjacency_from_o3`；**bug 修复**：PE Graph 置零移到缓存分支外 |

---

## 汇总文件

| 文件 | 说明 |
|------|------|
| [experiment_comparison_summary.md](experiment_comparison_summary.md) | 多维度对比分析（含消融、种子效应、Per-Step 对比） |
| [experiment_reflection.md](experiment_reflection.md) | 实验心得与体会 |
| [results_summary_all.csv](results_summary_all.csv) | 13 行数据（12 组有效 + 1 组已删除） |

---

## 第 3 周预告

- [ ] 主对比图表（Table 1 风格）
- [ ] 消融分析图表（Table 2 风格）：需先完成 PE Graph 消融重跑
- [ ] PE 分层分析（Table 3 风格）
- [ ] 站点误差地理分布可视化
- [ ] 报告初稿 & PPT
