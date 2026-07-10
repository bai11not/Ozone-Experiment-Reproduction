# 基于扩散模型的多站点空气质量预测实验平台

> **生产实习项目** · 2026 年夏季
> **题目**: 基于扩散模型的多站点空气质量预测实验平台构建
> **模型**: PE-DiffWaveNet (Diffusion + Permutation Entropy Graph + PE-FiLM)
> **数据**: 95 站点 O₃ 时空序列 (2022 全年, 8717 时间点)

---

## 仓库结构

```
📂 臭氧预测资料/                                  # 仓库根目录
├── 📄 README.md                                 # 本文件（与 assignment/ 同级）
│
├── 📂 assignment/                               # 个人 assignment 交付物
│   ├── 📄 PROJECT_REQUIREMENTS.md               #   项目全部规范要求（10 章汇总）
│   │
│   ├── 📂 week1/                                #   第 1 周: 数据理解和代码跑通
│   │   ├── 📄 README.md                         #     本周总结
│   │   ├── 📄 commands.sh                       #     全部可复现运行命令
│   │   ├── 📄 代码修改记录.md                    #     代码修改追溯（11 项修改）
│   │   │
│   │   ├── 📂 01_data_organization/             #     步骤①: 数据整理
│   │   │   ├── data_organization.py             #       主脚本（590 行）
│   │   │   ├── regenerate_figures.py            #       图表修复脚本（中文乱码修复）
│   │   │   └── data_organization_output/
│   │   │       ├── data_description_draft.md    #       数据说明初稿
│   │   │       ├── station_missing_summary.csv
│   │   │       ├── summary.json
│   │   │       └── figures/                     #       8 张数据探索图
│   │   │
│   │   ├── 📂 02_baseline/                      #     步骤②: Baseline 调研与适配
│   │   │   └── baseline_report.md               #       完整调研报告
│   │   │
│   │   ├── 📂 03_pediffwavenet/                 #     步骤③: PE-DiffWaveNet 实验
│   │   │   └── pediffwavenet_experiment.md      #       模型原理 + Smoke test + 实验流程
│   │   │
│   │   └── 📂 04_results_organization/          #     步骤④: 结果整理
│   │       ├── results_organization_report.md   #       字段对齐 + 模板指南
│   │       ├── chart_naming_convention.md       #       图表命名规范
│   │       └── results.csv                      #       统一结果表（27 行）
│   │
│   ├── 📂 week2/                                #   第 2 周: 批量实验（进行中）
│   └── 📂 week3/                                #   第 3 周: 图表、报告和验收

```

---

## 周进度

### ✅ 第 1 周: 数据理解和代码跑通

| # | 步骤 | 状态 | 核心产出 |
|:--:|------|:--:|------|
| 1 | 数据整理 — 缺失统计、站点分布、时间序列 | ✅ | 8 图 + data_description_draft.md |
| 2 | Baseline 调研与适配 — 已有 baseline 确认、DiffSTG 适配 | ✅ | baseline_report.md + DiffSTG 数据/脚本 |
| 3 | PE-DiffWaveNet 实验 — Smoke test 复核、命令记录 | ✅ | 18 文件 + pediffwavenet_experiment.md |
| 4 | 结果整理 — 统一表、字段对齐、命名规范 | ✅ | results.csv + chart_naming_convention.md |
| 5 | 汇总文件 — 周报总览、命令汇总、修改追溯 | ✅ | README.md + commands.sh + 代码修改记录.md |

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

*本文件位于该子仓库根目录，与 `assignment/` 文件夹同级，作为 GitHub 子仓库首页 README。assignment 子目录内为个人负责的三周交付物。*
