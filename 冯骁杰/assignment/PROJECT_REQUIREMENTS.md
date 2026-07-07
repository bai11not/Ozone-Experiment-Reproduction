# 项目要求汇总

> **项目题目**: 基于扩散模型的多站点空气质量预测实验平台构建
> **来源文档**: 01_生产实习任务书 / 03_数据说明 / 04_运行与提交规范 / 05_有代码论文推荐
> **整理日期**: 2026-07-06

---

## 目录

1. [项目概述](#1-项目概述)
2. [数据规范](#2-数据规范)
3. [模型与 Baseline](#3-模型与-baseline)
4. [实验要求](#4-实验要求)
5. [指标与评估](#5-指标与评估)
6. [交付物规范](#6-交付物规范)
7. [命名与字段规范](#7-命名与字段规范)
8. [禁止事项](#8-禁止事项)
9. [环境与运行](#9-环境与运行)
10. [DiffSTG 适配指南](#10-diffstg-适配指南)

---

## 1. 项目概述

### 1.1 总目标

| # | 任务 | 说明 |
|:--:|------|------|
| 1 | 理解并整理数据 | O3、PM、站点信息和气象因子 |
| 2 | 跑通模型/baseline | 至少一个指定模型或 baseline |
| 3 | 生成统一指标 | 统一格式的 RMSE/MAE/MAPE |
| 4 | 完成实验分析 | 至少一类实验分析 |
| 5 | 提交可复现资产 | 代码、日志、表格、图表、报告 |

> 核心定位：不是提出全新模型，而是把真实数据和已有模型跑通，形成**可复现、可整理、可写入报告**的实验资产。

### 1.2 三周节奏

| 周次 | 主题 | 核心任务 |
|:----:|------|----------|
| 第 1 周 | 数据理解和代码跑通 | 数据整理、baseline 确认、smoke test、结果字段对齐 |
| 第 2 周 | 批量实验 | 按实验矩阵跑主实验/消融/多步长/多seed |
| 第 3 周 | 图表、报告和验收 | 汇总表格、画图、报告初稿、PPT |

### 1.3 任务分组

| 组别 | 任务 | 职责 |
|:----:|------|------|
| 1 | 数据整理 | 清洗说明、字段解释、缺失统计、站点分布、相关性分析 |
| 2 | Baseline 复现 | 跑通已有 baseline/DiffSTG，输出统一指标 |
| 3 | PE-DiffWaveNet 实验 | 主模型训练、多 seed、多步长、消融实验 |
| 4 | 结果整理和报告 | 汇总结果、论文风格表格图表、报告初稿 |

---

## 2. 数据规范

### 2.1 数据范围

| 项目 | 值 |
|------|-----|
| 站点数 | **95** |
| 主预测目标 | **O₃** (臭氧) |
| 时间范围 | 2022-01-01 00:00 ~ 2022-12-31 23:00 |
| 时间索引长度 | **8,717** |
| 输入特征数 | **15** = O₃ + 14 个气象变量 |
| train_rate | **0.8465** |
| 训练集 | 0 ~ 7377 (7,378 steps) |
| 验证集 | 7378 ~ 8046 (669 steps) |
| 测试集 | 8047 ~ 8716 (670 steps) |

### 2.2 目录结构

| 目录 | 内容 | 关键文件 |
|------|------|----------|
| `data_N95/` | 原始逐日 CSV (365个) | `china_sites_YYYYMMDD.csv` |
| `matrix_N95/` | 模型处理后数据 | `data.npy` (95,8717), `time_index.npy` (8717,), `met_raw_aligned_cache.npz` |
| `xlsx_N95/` | 站点和辅助信息 | `station_loc1.xlsx` (95站点编码/名称/城市/经纬度) |
| `paper_assets_pediffwavenet/` | 已有论文表格 | table1/table2/table3 |
| `docs_word/` | 任务文档 | 任务书/安排/数据说明/提交规范 |
| `code/` | 核心代码 | train_pediffwavenet_noleak.py, train_atgcn_pe3_noleak.py |
| `scripts/` | 运行脚本 | run_smoke_cpu.sh, run_train_pediffwavenet.sh |
| `templates/` | 模板 | 实验记录/结果CSV/报告提纲 |

### 2.3 气象因子 (14个)

```
blh, d2m, fsr, kx, sp, ssr, ssrd, t2m, tcc, tcwv, tp, u10, v10, zust
```

> 原始气象 CSV 约 6.8GB，项目中使用 `matrix_N95/met_raw_aligned_cache.npz` 缓存即可。
> 原始气象 CSV 路径: `/home/chenxudong/graduate/代码 2/代码/代码/Var_Values_Hourly_2022`

### 2.4 污染物类型 (data_N95 CSV 中的 type 字段)

```
AQI, PM2.5, PM2.5_24h, PM10, PM10_24h,
SO2, SO2_24h, NO2, NO2_24h,
O3, O3_8h, O3_8h_24h, O3_24h,
CO, CO_24h
```

### 2.5 数据切分 (no-leak 流程)

1. 先按 train_rate=0.8465 切分原始时间轴
2. **只在训练集**拟合 O₃ 最大值和气象变量 min/max
3. 分别在 train/valid/test 内部做滑动窗口
4. **只用训练集**构建 T 图和 PE 图

> ⚠️ 报告中必须说明 no-leak 切分方式，避免被质疑数据泄漏。

### 2.6 训练脚本实际读取

**输入**:
- `matrix_N95/data.npy`
- `matrix_N95/time_index.npy`
- `matrix_N95/met_raw_aligned_cache.npz`
- `xlsx_N95/station_loc1.xlsx`

**输出**:
- `matrix_N95_PEDiffWaveNet_noleak_<EXP_NAME>/`
- `weights_N95/weights_pediffwavenet_noleak_<EXP_NAME>/`

---

## 3. 模型与 Baseline

### 3.1 主模型: PE-DiffWaveNet

- **类型**: 扩散模型 + Permutation Entropy 图 + PE-FiLM
- **核心模块**: Diffusion (扩散去噪) / PE Graph (PE 图卷积) / PE FiLM (PE 特征调制)
- **代码**: `code/train_pediffwavenet_noleak.py`

### 3.2 已有 Baseline (来自 table1)

| 方法 | 类型 |
|------|------|
| MTGNN | 时空图神经网络 |
| Graph WaveNet | 时空图卷积 |
| AGCRN | 自适应图卷积 |
| DCRNN | 扩散卷积循环网络 |
| ATGCN-PE3 | 本项目实现的扩散 baseline |
| DiffSTG (推荐新增) | 扩散时空图预测 |

### 3.3 DiffSTG (优先调研 baseline)

- **论文**: SIGSPATIAL 2023
- **代码**: <https://github.com/wenhaomin/DiffSTG>
- **许可证**: MIT
- **定位**: 扩散类时空图 baseline，与 PE-DiffWaveNet 形成对照
  - DiffSTG: 通用概率时空图扩散预测
  - PE-DiffWaveNet: 面向空气质量复杂性的 PE 增强扩散预测
- **备选**: CSDI (<https://github.com/ermongroup/CSDI>)

---

## 4. 实验要求

### 4.1 必须记录的参数

每次实验必须记录:

| 参数 | 示例 |
|------|------|
| 运行命令 | 完整 bash 命令 |
| seed | 42 |
| seq_len (输入窗口) | 24 |
| pre_len (预测步长) | 6 |
| use_diffusion | 1 或 0 |
| use_pe_graph | 1 或 0 |
| use_pe_film | 1 或 0 |
| 输出目录 | 完整路径 |
| RMSE / MAE / MAPE | 数值 |

### 4.2 推荐实验矩阵

| 实验类型 | 配置 |
|----------|------|
| 主模型 | PE-DiffWaveNet, seq_len=24, pre_len=6, seed=42 |
| 多 seed | seed=42, 52, 62 |
| 输入窗口 | seq_len=12, 24, 48 |
| 预测步长 | pre_len=1, 3, 6, 12, 24 |
| 无扩散 (消融) | USE_DIFFUSION=0 |
| 无 PE 图 (消融) | USE_PE_GRAPH=0 |
| 无 PE FiLM (消融) | USE_PE_FILM=0 |
| PE shuffle | PE_SHUFFLE_SEED=52 |
| 小样本 debug | 限制 MAX_*_WINDOWS |

### 4.3 可接受的 Debug 实验

资源不足时可先跑小配置:

```bash
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 \
  MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=debug_cpu bash scripts/run_train_pediffwavenet.sh 6 24 42
```

> debug 结果只用于检查流程，**正式报告中必须标注为 debug**。

---

## 5. 指标与评估

### 5.1 核心指标 (必须)

| 指标 | 全称 | 说明 |
|------|------|------|
| **RMSE** | Root Mean Square Error | 均方根误差 (μg/m³) |
| **MAE** | Mean Absolute Error | 平均绝对误差 (μg/m³) |
| **MAPE** | Mean Absolute Percentage Error | 平均绝对百分比误差 (%) |

### 5.2 扩展指标 (推荐)

| 指标 | 说明 |
|------|------|
| **Peak RMSE** | 高值区 (O₃ > 90th percentile) 的 RMSE |
| **Step6 RMSE** | 第 6 预测步的 RMSE |
| Per-step RMSE | 每预测步 RMSE 列表 (1..pre_len) |
| Relative RMSE | RMSE / O₃_train_max × 100% |

### 5.3 字段对齐

所有结果表字段必须向 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv` 对齐。

---

## 6. 交付物规范

### 6.1 每组必须提交

| 文件 | 说明 |
|------|------|
| `README.md` | 说明本组做了什么 |
| `commands.sh` | 实际运行命令 |
| `results.csv` | 统一指标表 |
| `figures/` | 图表 |
| `logs/` | 关键日志 |
| `report_section.md` | 本组报告段落 |

### 6.2 Smoke Test 通过标准

- [ ] 没有 `FileNotFoundError`
- [ ] 能打印 train/valid/test shape
- [ ] 能生成输出目录
- [ ] 能完成 1 个 epoch
- [ ] 能保存 config.json / split_summary.json / graph_summary.json

### 6.3 最终汇总

各组产出最终汇总到一份完整实习报告 + PPT 中。

---

## 7. 命名与字段规范

### 7.1 实验命名

格式: `{组名}_{模型}_{关键配置}_{seed}`

| 示例 | 含义 |
|------|------|
| `g3_pedw_p6_l24_s42` | 组3, PE-DiffWaveNet, pre_len=6, seq_len=24, seed=42 |
| `g3_pedw_no_diff_p6_l24_s42` | 消融: 无扩散 |
| `g3_pedw_no_pe_graph_p6_l24_s42` | 消融: 无 PE 图 |

### 7.2 结果表字段 (对齐模板)

```
group, student, experiment_id, model, seq_len, pre_len, seed,
use_diffusion, use_pe_graph, use_pe_film, pe_adaptive_loss,
rmse, mae, mape, peak_rmse, step6_rmse, output_dir, log_file, notes
```

模板文件: `templates/experiment_result_template.csv`

### 7.3 报告结构 (参考 templates/report_outline.md)

1. 实习背景与任务
2. 数据集说明
3. 方法介绍
4. 实验设置
5. 实验结果 (主对比表 + 消融表 + 多步长 + 可视化)
6. 结果分析
7. 问题与改进
8. 总结

---

## 8. 禁止事项

| # | 禁止行为 |
|:--:|------|
| 1 | 只提交截图，无实际代码/日志 |
| 2 | 说"跑了但没保存日志" |
| 3 | 修改核心模型代码但不说明 |
| 4 | 混用其他数据集的结果 |
| 5 | 把 debug 小样本结果当正式结果 |
| 6 | 自行替换数据为公开数据 |
| 7 | 随意改动核心模型结构（除非任务明确要求） |

---

## 9. 环境与运行

### 9.1 推荐环境

```bash
conda env create -f environment.yml
conda activate atgcn
```

### 9.2 Smoke Test

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh
```

### 9.3 正式训练

```bash
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

### 9.4 小配置调试 (CPU)

```bash
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 \
  MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=student_debug_cpu \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

---

## 10. DiffSTG 适配指南

### 10.1 数据映射

| DiffSTG 概念 | 本项目对应 | 格式 |
|-------------|-----------|------|
| graph node | 95 个空气质量站点 | — |
| flow.npy | O₃ 时间序列 | (T, N, F) = (8717, 95, 1) |
| adj.npy | 站点空间图/相关图/PE 图 | (N, N) = (95, 95) |
| T_h | 历史输入窗口 | 12 / 24 / 48 |
| T_p | 预测步长 | 1 / 3 / 6 / 12 / 24 |

### 10.2 数据路径

```
external_baselines/DiffSTG/data/dataset/AIR_N95/
├── flow.npy      # (8717, 95, 1)
└── adj.npy       # (95, 95)
```

### 10.3 最低目标

1. 下载并跑通官方代码
2. 用 `matrix_N95/data.npy` + `station_loc1.xlsx` 生成 DiffSTG 数据
3. 跑 seq_len=24, pre_len=6, seed=42
4. 输出 RMSE / MAE / MAPE
5. 填入 `templates/experiment_result_template.csv`

### 10.4 进阶目标

- 跑 pre_len=1, 3, 6, 12, 24
- 跑 O₃ / PM₂.₅ / PM₁₀ 单目标
- 对比不同邻接矩阵 (空间距离 / 相关 / PE)
- 增加概率预测指标或置信区间图

### 10.5 已知限制

DiffSTG 原生代码中 T_p (预测长度) 硬绑定为 T_h (输入长度)。如需 T_h=24, T_p=6，需修改 `train.py` 和 `model.py` 解耦。已在 `external_baselines/DiffSTG/train_air_n95.py` 中实现适配。

---

*本文件汇总了生产实习项目的全部规范要求，后续任务执行时以此为基准参考。*
