# 🌫️ 臭氧预测实验复现项目

> Ozone Prediction Experiment Reproduction

---

## 🏗️ 核心架构

```
Ozone-Experiment-Reproduction/
├── 臭氧预测资料/              # 核心数据与代码
│   ├── code/                   # PE-DiffWaveNet 模型代码
│   ├── data_N95/               # N95 站点原始数据 (365天)
│   ├── matrix_N95/             # 预处理特征矩阵
│   ├── weights_N95/            # 训练好的模型权重
│   └── xlsx_N95/               # 站点经纬度信息
├── week1/                      # 第一周：Baseline + DiffSTG
├── week2/                      # 第二周：PE-DiffWaveNet 消融实验
└── week3/                      # 第三周：论文图表与分析
```

### 模型框架

| 模型 | 方法 | 任务 | 状态 |
|------|------|------|------|
| **DiffSTG** | 扩散模型 + 时空图 | 概率预测 | ✅ 已复现 |
| **PE-DiffWaveNet** | 位置编码 + 差分波浪网络 | 确定性预测 | ✅ 已复现 |
| **Baseline** | GRU / LR / Persistence / Mean | 基准对比 | ✅ 已完成 |

### 数据集

| 数据集 | 站点数 | 时间步 | 特征 | 用途 |
|--------|--------|--------|------|------|
| **AIR_N95** | 95 | 8,717 | O₃ | 臭氧预测任务 |
| **PEMS08** | 170 | 17,856 | 流量/速度/占用 | 原始论文示例 |

---

## 📁 目录索引

### 核心资源

* [💻 代码库](./臭氧预测资料/code/) —— 模型训练、预测、评估脚本
* [📊 数据文件](./臭氧预测资料/data_N95/) —— N95 站点原始数据集
* [📈 特征矩阵](./臭氧预测资料/matrix_N95/) —— 模型输入特征矩阵
* [⚖️ 模型权重](./臭氧预测资料/weights_N95/) —— 已训练好的权重文件
* [📋 站点信息](./臭氧预测资料/xlsx_N95/) —— 95个站点经纬度表格

### 实验成果

* [📊 Week1 结果](./week1/) —— Baseline 评估、DiffSTG 实验、结果汇总
* [📊 Week2 结果](./week2/) —— PE-DiffWaveNet 消融实验、多组对比实验
* [📊 Week3 结果](./week3/) —— 论文图表、详细分析数据

### 团队工作区

* [👤 白文豪](./白文豪/) —— DiffSTG 扩散模型实验、结果整理
* [👤 冯骁杰](./冯骁杰/) —— 数据组织、PE-DiffWaveNet 实验
* [👤 李昊泽](./李昊泽/) —— 数据探索分析、基线实验
* [👤 马一田](./马一田/) —— PE-DiffWaveNet 消融实验、DiffSTG 适配
* [👤 王希童](./王希童/) —— 统一结果框架、时间序列分析

### 文档资料

* [📝 技术文档](./臭氧预测资料/docs_word/) —— Word 格式说明文档
* [📄 论文素材](./臭氧预测资料/paper_assets_pediffwavenet/) —— 论文插图、表格资源
* [📜 运行脚本](./臭氧预测资料/scripts/) —— 实验流程脚本说明

---

## 👥 团队成员工作导航

### 白文豪

**核心工作**：DiffSTG 扩散模型复现、Baseline 评估、实验结果整理

| 模块 | 内容 | 关键文件 | 链接 |
|------|------|----------|------|
| **DiffSTG 训练** | 训练脚本、数据预处理 | `train.py`, `gen_diffstg_data.py` | [查看](./白文豪/week1/DiffSTG/train.py) |
| **Baseline 评估** | 4种基线方法评估 | `run_baseline_evaluation.py` | [查看](./白文豪/week1/baseline/run_baseline_evaluation.py) |
| **PE-DiffWaveNet 实验** | 实验运行脚本 | `run_pe_diffwavenet_experiment.sh` | [查看](./白文豪/week1/PE-DiffWaveNet%20实验/run_pe_diffwavenet_experiment.sh) |
| **结果整理** | 统一结果表、各方法结果 | `unified_results_table.csv` | [查看](./白文豪/week1/结果整理/output/unified_results_table.csv) |
| **Week2 扩展实验** | 不同污染物、历史长度实验 | `experiment_result.csv` | [查看](./白文豪/week2/DiffSTG/experiment_result.csv) |

**关键成果**：
- DiffSTG 在 AIR_N95 数据集上的完整训练流程
- 统一结果表（Baseline + DiffSTG + PE-DiffWaveNet）
- 各方法结果文件详细说明文档

---

### 冯骁杰

**核心工作**：数据组织与可视化、PE-DiffWaveNet 消融实验

| 模块 | 内容 | 关键文件 | 链接 |
|------|------|----------|------|
| **数据组织** | 数据探索、可视化图表 | `data_organization.py` | [查看](./冯骁杰/assignment/week1/01_data_organization/data_organization.py) |
| **Baseline 报告** | 基线方法分析报告 | `baseline_report.md` | [查看](./冯骁杰/assignment/week1/02_baseline/baseline_report.md) |
| **PE-DiffWaveNet** | 实验文档与结果 | `pediffwavenet_experiment.md` | [查看](./冯骁杰/assignment/week1/03_pediffwavenet/pediffwavenet_experiment.md) |
| **结果整理** | 结果汇总与图表规范 | `results.csv` | [查看](./冯骁杰/assignment/week1/04_results_organization/results.csv) |
| **Week2 消融实验** | 8组 PE-DiffWaveNet 对比实验 | `results_summary_all.csv` | [查看](./冯骁杰/assignment/week2/results_summary_all.csv) |

**关键成果**：
- 数据缺失分析、站点分布可视化
- PE-DiffWaveNet 多组消融实验（不同 pre_len、不同模型配置）
- 实验对比总结报告

---

### 李昊泽

**核心工作**：数据探索分析、DiffSTG 基线实验

| 模块 | 内容 | 关键文件 | 链接 |
|------|------|----------|------|
| **数据探索分析** | EDA 分析、数据卡片 | `data_card.json`, `eda_overview.png` | [查看](./李昊泽/week1/data_eda/data_card.json) |
| **DiffSTG 基线** | 数据预处理、CPU 运行脚本 | `run_diffstg_cpu.py` | [查看](./李昊泽/week1/diffstg_baseline/run_diffstg_cpu.py) |
| **Smoke Test** | 小规模测试结果 | `metrics_summary.json` | [查看](./李昊泽/week1/smoke_test/metrics_summary.json) |
| **Epoch3 测试** | 3轮训练测试结果 | `training_curves.png`, `predictions.png` | [查看](./李昊泽/week1/epoch3_test/metrics_summary.json) |
| **运行脚本** | 训练、查看结果脚本 | `run_train.ps1`, `view_results.py` | [查看](./李昊泽/week1/scripts/run_train.ps1) |

**关键成果**：
- 完整的 EDA 分析报告
- DiffSTG 数据预处理流程
- 测试结果可视化图表

---

### 马一田

**核心工作**：PE-DiffWaveNet 消融实验、DiffSTG 适配与数据准备

| 模块 | 内容 | 关键文件 | 链接 |
|------|------|----------|------|
| **Week1 交付物** | 数据整理、Baseline、PE-DiffWaveNet、结果整理 | `week1_summary.md` | [查看](./马一田/week1_deliverables/04_结果整理/week1_summary.md) |
| **数据整理** | 站点统计、缺失分析、时间序列图表 | `data_summary_report.md`, `station_distribution.png` | [查看](./马一田/week1_deliverables/01_数据整理/报告/data_summary_report.md) |
| **Baseline** | ATGCN-PE3 实验、DiffSTG 数据准备 | `gen_diffstg_data.py`, `adj.npy`, `flow.npy` | [查看](./马一田/week1_deliverables/02_Baseline/DiffSTG数据/gen_diffstg_data.py) |
| **PE-DiffWaveNet** | Smoke Test、Debug Run、模型权重 | `metrics_summary.json` | [查看](./马一田/week1_deliverables/03_PE-DiffWaveNet/Smoke_Test/metrics_summary.json) |
| **Week2 消融实验** | Person C (seed=52/62) 8组实验 | `person_C_results.csv`, `run_person_experiments.sh` | [查看](./马一田/week2/results/person_C_seed52_full_nodiff/person_C_results.csv) |

**关键成果**：
- PE-DiffWaveNet 消融实验（full vs no_diff，验证扩散模型对预测精度的贡献）
- DiffSTG 数据预处理流程
- 完整的 Week1 交付物整理

---

### 王希童

**核心工作**：统一结果框架、时间序列分析

| 模块 | 内容 | 关键文件 | 链接 |
|------|------|----------|------|
| **统一结果框架** | 结果汇总框架设计 | `unified_result_framework.md` | [查看](./王希童/unified_result_framework.md) |
| **时间序列分析** | O₃/PM2.5/PM10 时间序列图 | `time_series_O3_PM25_PM10.png` | [查看](./王希童/time_series_O3_PM25_PM10.png) |
| **统一结果表** | 各方法结果汇总 | `unified_results.csv` | [查看](./王希童/unified_results.csv) |
| **数据报告** | 数据报告草稿 | `data_report_draft.md` | [查看](./王希童/data_report_draft.md) |
| **运行命令参考** | 实验运行命令汇总 | `run_commands_reference.md` | [查看](./王希童/run_commands_reference.md) |

**关键成果**：
- 统一结果框架设计文档
- 污染物时间序列可视化
- 运行命令参考文档

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/bai11not/Ozone-Experiment-Reproduction.git
cd Ozone-Experiment-Reproduction

# 安装依赖
pip install -r 臭氧预测资料/requirements.txt

# PE-DiffWaveNet 训练
python 臭氧预测资料/code/train_pediffwavenet_noleak.py

# DiffSTG 训练（白文豪）
python 白文豪/week1/DiffSTG/train.py --data AIR_N95 --T_h 24 --T_p 6 --batch_size 32 --lr 0.0001 --n_epochs 200 --is_train True --is_test True
```

---

## 📚 参考文献

### DiffSTG
| 项目 | 信息 |
|------|------|
| **会议** | ACM SIGSPATIAL 2023 |
| **论文** | [https://arxiv.org/abs/2301.13629](https://arxiv.org/abs/2301.13629) |
| **代码** | [https://github.com/wenhaomin/DiffSTG](https://github.com/wenhaomin/DiffSTG) |

---

> 📅 最后更新：2026-07-18