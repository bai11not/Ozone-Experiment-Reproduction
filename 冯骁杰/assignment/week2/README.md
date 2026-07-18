# Week 2: 批量实验

> **完成日期**: 2026-07-14 ~ 2026-07-15
> **对应任务**: 三周安排与分工 — 第 2 周
> **模型**: PE-DiffWaveNet | **数据**: matrix_N95 (95 站点 O₃, 2022 全年)

---

## 目录结构

```
week2/
├── README.md                              # 本文件
├── experiment_comparison_summary.md       # 18 组实验多维度对比分析报告
├── experiment_reflection.md               # 实验心得与体会
├── results_summary_all.csv                # 汇总结果表（18 组）
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
├── g3_pedw_p6_l24_s62/                    # 实验 10: 主实验 seq24 pre6 s62
├── g3_noPEgraph_p6_l12_s62/               # 实验 11: no PE Graph seq12 pre6
├── g3_noPEgraph_p3_l12_s62/               # 实验 12: no PE Graph seq12 pre3
├── g3_noPEgraph_p3_l24_s62/               # 实验 13: no PE Graph seq24 pre3
├── g3_noPEgraph_p6_l24_s62/               # 实验 14: no PE Graph seq24 pre6
├── g3_noPEfilm_p6_l12_s62/                # 实验 15: no PE-FiLM seq12 pre6
└── g3_noPEfilm_p3_l12_s62/                # 实验 16: no PE-FiLM seq12 pre3

每组实验均按规范包含 4 个文件（training.log / results.csv / experiment_log.md / commands.sh）
```

---

## 实验矩阵完成情况

### 参数扫描（8 组，s42 ×4 + s62 ×4）

| # | 实验 ID | seq/pre | diff | PG | PF | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:---:|:--:|
| 0 | `g3_pedw_p6_l24_s42` | 24/6 | 1 | 1 | 1 | 42 | ✅ 基准 |
| 1 | `g3_pedw_p3_l24_s42` | 24/3 | 1 | 1 | 1 | 42 | ✅ |
| 2 | `g3_pedw_p3_l12_s42` | 12/3 | 1 | 1 | 1 | 42 | ✅ |
| 3 | `g3_pedw_p6_l12_s42` | 12/6 | 1 | 1 | 1 | 42 | ✅ |
| 7 | `g3_pedw_p6_l12_s62` | 12/6 | 1 | 1 | 1 | 62 | ✅ |
| 8 | `g3_pedw_p3_l12_s62` | 12/3 | 1 | 1 | 1 | 62 | ✅ |
| 9 | `g3_pedw_p3_l24_s62` | 24/3 | 1 | 1 | 1 | 62 | ✅ |
| 10 | `g3_pedw_p6_l24_s62` | 24/6 | 1 | 1 | 1 | 62 | ✅ |

### 扩散模块消融（4 组，seed=42）

| # | 实验 ID | seq/pre | diff | PG | PF | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:---:|:--:|
| 0b | `g3_nodiff_pe_p6_l24_s42` | 24/6 | **0** | 1 | 1 | 42 | ✅ |
| 4 | `g3_nodiff_pe_p3_l24_s42` | 24/3 | **0** | 1 | 1 | 42 | ✅ |
| 5 | `g3_nodiff_pe_p3_l12_s42` | 12/3 | **0** | 1 | 1 | 42 | ✅ |
| 6 | `g3_nodiff_pe_p6_l12_s42` | 12/6 | **0** | 1 | 1 | 42 | ✅ |

### PE Graph 消融（4 组，seed=62，同种子受控）

| # | 实验 ID | seq/pre | diff | PG | PF | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:---:|:--:|
| 11 | `g3_noPEgraph_p6_l12_s62` | 12/6 | 1 | **0** | 1 | 62 | ✅ |
| 12 | `g3_noPEgraph_p3_l12_s62` | 12/3 | 1 | **0** | 1 | 62 | ✅ |
| 13 | `g3_noPEgraph_p3_l24_s62` | 24/3 | 1 | **0** | 1 | 62 | ✅ |
| 14 | `g3_noPEgraph_p6_l24_s62` | 24/6 | 1 | **0** | 1 | 62 | ✅ |

### PE-FiLM 消融（2 组，seed=62，同种子受控）

| # | 实验 ID | seq/pre | diff | PG | PF | seed | 状态 |
|:--:|---------|:---:|:---:|:---:|:---:|:---:|:--:|
| 15 | `g3_noPEfilm_p6_l12_s62` | 12/6 | 1 | 1 | **0** | 62 | ✅ |
| 16 | `g3_noPEfilm_p3_l12_s62` | 12/3 | 1 | 1 | **0** | 62 | ✅ |

### 待实验

| 实验类型 | 配置 | 状态 |
|----------|------|:--:|
| PE-FiLM 消融（续） | seq24 pre3, seq24 pre6 (s62) | ⏳ |
| PE shuffle | PE_SHUFFLE_SEED=52 | ⏳ |
| Baseline | ATGCN-PE3, DiffSTG | ⏳ |

> ⚠️ 首次 4 组 noPEgraph 因代码 bug（PE 缓存中 `PE_mat` 未置零）无效，已修复并完成正确重跑。

---

## 关键成果

### 组件重要性排序

**PE-FiLM ≫ pre_len ≫ seq_len ≫ PE Graph ≈ diffusion ≈ seed**

| 消融组件 | Δ RMSE (12/6) | 影响等级 |
|------|:---:|:---:|
| no PE-FiLM | **+1.82** | **巨大** |
| no PE Graph | +0.45 | 中等 |
| no Diffusion | +0.28* | 中等 |

> *Diffusion 消融为 seed=42 数据

### 扩散模块消融

- 整体 RMSE 影响 < 3%，但 **Peak RMSE 恶化 1.4~1.8**
- 核心价值在**高浓度 O₃ 峰值预测**

### PE Graph 消融

- 贡献因配置而异：seq12 下关闭有损（+0.45~0.63），seq24 pre6 下反而有益（−0.66）
- 与 S/T 邻接矩阵存在复杂交互

### PE-FiLM 消融

- **三个 PE 组件中贡献最大**，关闭后 Step5-6 RMSE 急剧恶化
- 长时预测的特征调制是其核心功能

### 多种子

- seed 42→62：RMSE Δ 0.05~0.76
- 消融实验必须同种子

### 最佳配置

`seed=42, seq24, pre3, diff=1, PG=1, PF=1` → **RMSE=8.62, MAPE=24.00%**

---

## 代码修改

| 文件 | 修改内容 |
|------|----------|
| `code/pe_step1_fix.py` | **新建**：纯 Python PE 滑动计算 |
| `code/train_atgcn_pe3_noleak.py` | 导入 `average_sliding_pe_fast` |
| `code/train_atgcn_pe3.py` | 纯 Python Haversine 替换 geographiclib |
| `code/train_pediffwavenet_noleak.py` | PE 缓存逻辑；**bug 修复**：PE Graph 置零移到缓存分支外 |

---

## 汇总文件

| 文件 | 说明 |
|------|------|
| [experiment_comparison_summary.md](experiment_comparison_summary.md) | 18 组多维度对比分析 |
| [experiment_reflection.md](experiment_reflection.md) | 实验心得与体会 |
| [results_summary_all.csv](results_summary_all.csv) | 18 组统一指标表 |

---

## 第 3 周预告

- [ ] 主对比图表（Table 1 风格）
- [ ] 消融分析图表（Table 2 风格）
- [ ] PE 分层分析（Table 3 风格）
- [ ] 站点误差地理分布可视化
- [ ] 报告初稿 & PPT
