# Week 1: 数据理解和代码跑通

> **完成日期**: 2026-07-06
> **对应任务**: 三周安排与分工 — 第 1 周

---

## 目录结构

```
week1/
├── README.md                          # 本文件
├── commands.sh                        # 全部运行命令
│
├── 01_data_organization/              # 任务1: 数据整理
│   ├── data_organization.py           #   数据整理脚本
│   └── data_organization_output/
│       ├── data_description_draft.md  #   数据说明初稿
│       ├── station_missing_summary.csv
│       ├── summary.json
│       └── figures/                   #   8张图表
│
├── 02_baseline/                       # 任务2: Baseline 调研与适配
│   └── baseline_report.md             #   完整调研报告
│
├── 03_pediffwavenet/                  # 任务3: PE-DiffWaveNet 实验
│   └── pediffwavenet_experiment.md    #   Smoke test + 命令报告
│
└── 04_results_organization/           # 任务4: 结果整理
    ├── results_organization_report.md #   字段对齐 + 模板指南
    ├── chart_naming_convention.md     #   图表命名规范
    └── results.csv                    #   统一结果表
```

---

## 四组任务完成情况

| # | 任务 | 状态 | 核心产出 |
|:--:|------|:----:|----------|
| 1 | **数据整理** — 缺失统计、站点分布、时间序列、数据说明 | ✅ | `data_description_draft.md` + 8 张图 |
| 2 | **Baseline** — 已有 baseline 确认、DiffSTG 调研适配 | ✅ | `baseline_report.md` + DiffSTG 数据/脚本 |
| 3 | **PE-DiffWaveNet** — Smoke test 复核、配置验证、命令记录 | ✅ | `pediffwavenet_experiment.md` |
| 4 | **结果整理** — 统一表、字段对齐、命名规范、模板 | ✅ | `results_organization_report.md` + `results.csv` |

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
