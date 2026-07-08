# 基于扩散模型的多站点空气质量预测实验平台

> **生产实习项目** · 2026 年夏季
> **题目**: 基于扩散模型的多站点空气质量预测实验平台构建
> **模型**: PE-DiffWaveNet (Diffusion + Permutation Entropy Graph + PE-FiLM)
> **数据**: 95 站点 O₃ 时空序列 (2022 全年, 8717 时间点)
> 
---

## 仓库结构

```
📂 assignment/
├── 📄 README.md                         # 本文件
├── 📄 PROJECT_REQUIREMENTS.md           # 项目全部规范要求 (10章汇总)
│
└── 📂 week1/                            # 第 1 周: 数据理解和代码跑通
    ├── 📄 README.md                     #   本周总结
    ├── 📄 commands.sh                   #   全部可复现运行命令
    │
    ├── 📂 01_data_organization/         #   任务①: 数据整理
    │   ├── data_organization.py         #     主脚本
    │   └── data_organization_output/
    │       ├── data_description_draft.md #    数据说明初稿
    │       ├── station_missing_summary.csv
    │       ├── summary.json
    │       └── figures/                 #     8 张数据探索图
    │
    ├── 📂 02_baseline/                  #   任务②: Baseline 调研与适配
    │   └── baseline_report.md           #     完整调研报告
    │
    ├── 📂 03_pediffwavenet/             #   任务③: PE-DiffWaveNet 实验
    │   └── pediffwavenet_experiment.md  #     Smoke test + 命令记录
    │
    └── 📂 04_results_organization/      #   任务④: 结果整理
        ├── results_organization_report.md
        ├── chart_naming_convention.md   #     图表命名规范
        └── results.csv                  #     统一结果表 (27 行)
```

---

## 周进度

### ✅ 第 1 周: 数据理解和代码跑通

| # | 任务 | 状态 | 核心产出 |
|:--:|------|:--:|------|
| 1 | 数据整理 — 缺失统计、站点分布、时间序列 | ✅ | 8 图 + data_description_draft.md |
| 2 | Baseline — 已有 baseline 确认、DiffSTG 适配 | ✅ | baseline_report.md + DiffSTG 数据/脚本 |
| 3 | PE-DiffWaveNet — Smoke test 复核、命令记录 | ✅ | 18 文件 + pediffwavenet_experiment.md |
| 4 | 结果整理 — 统一表、字段对齐、命名规范 | ✅ | results.csv + chart_naming_convention.md |

**关键发现**:
- O₃ 缺失率 2.25%, PM₂.₅ 1.33%, PM₁₀ 1.55% — 数据质量良好
- 确认 9 个 baseline/变体，MTGNN (L=24) 最优 RMSE=10.662
- PE-DiffWaveNet backbone RMSE=10.938，与最优 GNN baseline 同水平
- DiffSTG 完成数据适配，T_p=T_h 限制已解耦

### 🔄 第 2 周: 批量实验

| 实验类型 | 配置 | 状态 |
|----------|------|:--:|
| 主模型多 seed | seed=42, 52, 62 | ⏳ |
| 多预测步长 | pre_len=1, 3, 6, 12, 24 | ⏳ |
| 多输入窗口 | seq_len=12, 24, 48 | ⏳ |
| 消融-无扩散 | USE_DIFFUSION=0 | ⏳ |
| 消融-无 PE 图 | USE_PE_GRAPH=0 | ⏳ |
| 消融-无 PE FiLM | USE_PE_FILM=0 | ⏳ |
| PE shuffle | PE_SHUFFLE_SEED=52 | ⏳ |
| Baseline 正式运行 | ATGCN-PE3, DiffSTG | ⏳ |

### 📅 第 3 周: 图表、报告和验收

- [ ] 主对比图表 (Table 1 风格)
- [ ] 消融分析图表 (Table 2 风格)
- [ ] PE 分层分析 (Table 3 风格)
- [ ] 站点误差地理分布
- [ ] 报告初稿 & PPT

---

*本仓库仅包含个人负责的 assignment 交付物，完整项目代码见主仓库。*
