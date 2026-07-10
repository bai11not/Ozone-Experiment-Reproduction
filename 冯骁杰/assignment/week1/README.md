# Week 1: 数据理解和代码跑通

> **完成日期**: 2026-07-06
> **对应任务**: 三周安排与分工 — 第 1 周

---

## 目录结构

```
week1/
├── README.md                              # 本文件
├── commands.sh                            # 全部运行命令
├── 代码修改记录.md                         # 代码修改追溯（实习报告素材）
│
├── 01_data_organization/                  # 步骤1: 数据整理
│   ├── data_organization.py               #   数据整理主脚本（590 行）
│   ├── regenerate_figures.py              #   图表修复脚本（中文乱码修复）
│   └── data_organization_output/
│       ├── data_description_draft.md      #   数据说明初稿
│       ├── station_missing_summary.csv    #   站点缺失汇总
│       ├── summary.json                   #   统计摘要
│       └── figures/                       #   8 张图表（中文标题版）
│
├── 02_baseline/                           # 步骤2: Baseline 调研与适配
│   └── baseline_report.md                 #   完整调研与适配报告
│
├── 03_pediffwavenet/                      # 步骤3: PE-DiffWaveNet 实验
│   └── pediffwavenet_experiment.md        #   模型原理 + Smoke test + 实验流程
│
└── 04_results_organization/               # 步骤4: 结果整理
    ├── results_organization_report.md     #   字段对齐 + 模板指南
    ├── chart_naming_convention.md         #   图表命名规范
    └── results.csv                        #   统一结果表
```

---

## 五大步骤完成情况

| # | 步骤 | 状态 | 核心产出 |
|:--:|------|:----:|----------|
| 1 | **数据整理** — 缺失统计、站点分布、时间序列、数据说明 | ✅ | `data_description_draft.md` + 8 张图 |
| 2 | **Baseline 调研与适配** — 已有 baseline 确认、DiffSTG 调研适配 | ✅ | `baseline_report.md` + DiffSTG 数据/脚本 |
| 3 | **PE-DiffWaveNet 实验** — Smoke test 复核、配置验证、命令记录 | ✅ | `pediffwavenet_experiment.md` |
| 4 | **结果整理** — 统一表、字段对齐、命名规范、模板 | ✅ | `results_organization_report.md` + `results.csv` |
| 5 | **汇总文件** — 周报总览、命令汇总、代码修改追溯 | ✅ | `README.md` + `commands.sh` + `代码修改记录.md` |

---

## 关键成果

### 数据
- O3 缺失率 **2.25%**, PM2.5 **1.33%**, PM10 **1.55%**
- 95 站点覆盖 20 城市, 8,717 时间点

### Baseline
- 确认 9 个 baseline/变体, MTGNN 最优 (RMSE=10.66)
- DiffSTG 完成数据适配和训练脚本

### PE-DiffWaveNet
- Smoke test 18 个输出文件全部正常
- 录制了主实验、消融、多 seed、多步长的完整命令

### 结果整理
- **5 个核心字段**: RMSE / MAE / MAPE / Peak RMSE / Step6 RMSE
- **3 个 paper_assets 表格字段** 完全对齐
- **图表命名规范** 覆盖 7 类 30+ 标准图表

### 汇总
- `README.md` — 第 1 周工作总览
- `commands.sh` — 全部可执行命令（按五大板块组织）
- `代码修改记录.md` — 11 项修改的完整追溯（五大步骤 × 11 个文件）

---

## 第 2 周预告

按实验矩阵批量运行:

| 实验类型 | 配置 |
|----------|------|
| 主模型多 seed | seed=42, 52, 62 |
| 输入窗口 | seq_len=12, 24, 48 |
| 预测步长 | pre_len=1, 3, 6, 12, 24 |
| 消融-无扩散 | USE_DIFFUSION=0 |
| 消融-无 PE 图 | USE_PE_GRAPH=0 |
| 消融-无 PE FiLM | USE_PE_FILM=0 |
| PE shuffle | PE_SHUFFLE_SEED=52 |
