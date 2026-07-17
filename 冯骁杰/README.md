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
│   │   ├── 📂 01_data_organization/             #     步骤①: 数据整理
│   │   ├── 📂 02_baseline/                      #     步骤②: Baseline 调研与适配
│   │   ├── 📂 03_pediffwavenet/                 #     步骤③: PE-DiffWaveNet 实验
│   │   └── 📂 04_results_organization/          #     步骤④: 结果整理
│   │
│   ├── 📂 week2/                                #   第 2 周: 批量实验
│   │   ├── 📄 experiment_comparison_summary.md   #     实验对比总结报告
│   │   ├── 📄 experiment_reflection.md           #     实验心得与体会
│   │   ├── 📄 results_summary_all.csv            #     汇总结果表（13 组）
│   │   │
│   │   ├── 📂 g3_pedw_p6_l24_s42/               #     实验 0: 基准实验
│   │   ├── 📂 g3_nodiff_pe_p6_l24_s42/          #     实验 0b: 基准 noDiff 消融
│   │   ├── 📂 g3_pedw_p3_l24_s42/               #     实验 1: pre_len=3
│   │   ├── 📂 g3_pedw_p3_l12_s42/               #     实验 2: seq12 pre3
│   │   ├── 📂 g3_pedw_p6_l12_s42/               #     实验 3: seq12 pre6
│   │   ├── 📂 g3_nodiff_pe_p3_l24_s42/          #     实验 4: noDiff pre3
│   │   ├── 📂 g3_nodiff_pe_p3_l12_s42/          #     实验 5: noDiff seq12 pre3
│   │   ├── 📂 g3_nodiff_pe_p6_l12_s42/          #     实验 6: noDiff seq12 pre6
│   │   ├── 📂 g3_pedw_p6_l12_s62/               #     实验 7: seed=62 主实验
│   │   ├── 📂 g3_noPEgraph_p6_l12_s62/          #     实验 8: no PE Graph seq12 pre6
│   │   ├── 📂 g3_noPEgraph_p3_l12_s62/          #     实验 9: no PE Graph seq12 pre3
│   │   ├── 📂 g3_noPEgraph_p3_l24_s62/          #     实验 10: no PE Graph seq24 pre3
│   │   └── 📂 g3_noPEgraph_p6_l24_s62/          #     实验 11: no PE Graph seq24 pre6
│   │
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

**关键发现**: O₃ 缺失率 2.25%, MTGNN (L=24) 最优 RMSE=10.662, PE-DiffWaveNet backbone RMSE=10.938

---

### ✅ 第 2 周: 批量实验（13 组完成）

> 详见 [experiment_comparison_summary.md](week2/experiment_comparison_summary.md) 和 [experiment_reflection.md](week2/experiment_reflection.md)

| 维度 | 实验范围 | 组数 | 状态 |
|------|----------|:--:|:--:|
| 参数扫描 | pre_len=3/6, seq_len=12/24 | 3 | ✅ |
| 扩散消融 | use_diffusion=0 × 4 配置 | 4 | ✅ |
| PE Graph 消融 | use_pe_graph=0 × 4 配置 (seed=62) | 4 | ✅ |
| 多种子 | seed=42 vs seed=62 | 2 | ✅ |

**核心结论**:

| 发现 | 详细 |
|------|------|
| 参数重要性 | pre_len ≫ seq_len ≫ seed ≈ diffusion > PE Graph |
| 扩散模块价值 | 整体 RMSE 影响 < 3%，但 Peak RMSE 恶化 1.4~1.8 |
| PE Graph 贡献 | 同种子下开关结果完全一致（Δ=0.00），与 S/T 矩阵高度冗余 |
| 最佳配置 | seed=42, seq24, pre3, diff=1 → RMSE=8.62, MAPE=24.00% |
| 跨种子对比 | 种子差异 ~0.05，与消融效应同量级，不可混用 |

**待补**: seed=62 的 PE Graph=1 主实验（3 组，由小组成员运行）

### 📅 第 3 周: 图表、报告和验收

- [ ] 主对比图表 (Table 1 风格)
- [ ] 消融分析图表 (Table 2 风格)
- [ ] PE 分层分析 (Table 3 风格)
- [ ] 站点误差地理分布
- [ ] 报告初稿 & PPT

---

*本文件位于该子仓库根目录，与 `assignment/` 文件夹同级，作为 GitHub 子仓库首页 README。assignment 子目录内为个人负责的三周交付物。*
