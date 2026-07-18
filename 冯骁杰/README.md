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
│   ├── 📂 week2/                                #   第 2 周: 批量实验（18 组）
│   │   ├── 📄 experiment_comparison_summary.md   #     实验对比总结报告
│   │   ├── 📄 experiment_reflection.md           #     实验心得与体会
│   │   ├── 📄 results_summary_all.csv            #     汇总结果表（18 组）
│   │   │
│   │   ├── 📂 g3_pedw_p6_l24_s42/               #     实验 0: 基准 s42 ×4 参数扫描
│   │   ├── 📂 g3_pedw_p3_l24_s42/               #     实验 1-3
│   │   ├── 📂 g3_pedw_p3_l12_s42/
│   │   ├── 📂 g3_pedw_p6_l12_s42/
│   │   ├── 📂 g3_nodiff_pe_p*_s42/              #     实验 0b,4-6: 扩散消融 ×4
│   │   ├── 📂 g3_pedw_p*_s62/                   #     实验 7-10: seed=62 主实验 ×4
│   │   ├── 📂 g3_noPEgraph_p*_s62/              #     实验 11-14: PE Graph 消融 ×4
│   │   └── 📂 g3_noPEfilm_p*_s62/               #     实验 15-16: PE-FiLM 消融 ×2
│   │
│   └── 📂 week3/                                #   第 3 周: 图表、报告和验收
│
├── 📂 code/                                     # 通用代码（模型、训练脚本、PE 实现）
├── 📂 templates/                                # 实验输出规范模板
│   ├── 📄 experiment_output_standard.md
│   ├── 📄 experiment_result_template.csv
│   └── 📄 experiment_log_template.md
│
├── 📂 matrix_N95/                               # 数据矩阵（原始 O₃ + 气象缓存）
├── 📂 weights_N95/                              # 模型权重文件
└── 📂 matrix_N95_PEDiffWaveNet_noleak_*/       # 各实验的输出目录
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

### ✅ 第 2 周: 批量实验（18 组完成）

> 详见 [experiment_comparison_summary.md](week2/experiment_comparison_summary.md) 和 [experiment_reflection.md](week2/experiment_reflection.md)

| 维度 | 实验范围 | 组数 | 状态 |
|------|----------|:--:|:--:|
| 参数扫描 + 多种子 | pre_len=3/6, seq_len=12/24, seed=42/62 | 8 | ✅ |
| 扩散消融 | use_diffusion=0 × 4 配置 (seed=42) | 4 | ✅ |
| PE Graph 消融 | use_pe_graph=0 × 4 配置 (seed=62, 同种子受控) | 4 | ✅ |
| PE-FiLM 消融 | use_pe_film=0 × 2 配置 (seed=62) | 2 | ✅ |

**核心结论**:

| 发现 | 详细 |
|------|------|
| 组件重要性 | **PE-FiLM ≫ pre_len ≫ seq_len ≫ PE Graph ≈ diffusion ≈ seed** |
| PE-FiLM | 关闭后 RMSE 暴涨 1.12~1.82（10~16%），Step5-6 尤其恶化，是三个 PE 组件中贡献最大的 |
| PE Graph | 贡献因配置而异——seq12 下关闭有损（+0.45~0.63），seq24 pre6 下反而有益（−0.66） |
| 扩散模块价值 | 整体 RMSE 影响有限（< 3%），但 Peak RMSE 恶化 1.4~1.8，核心价值在峰值预测 |
| 最佳配置 | seed=42, seq24, pre3, diff=1, PG=1, PF=1 → RMSE=8.62, MAPE=24.00% |
| 代码 bug | PE 缓存中 `use_pe_graph=0` 置零未生效，4 组消融实验作废并重跑，教训已记录 |

**待补**: PE-FiLM 消融剩余 2 组（seq24 pre3/pre6）；PE shuffle；Baseline 对比

### 📅 第 3 周: 图表、报告和验收

- [ ] 主对比图表 (Table 1 风格)
- [ ] 消融分析图表 (Table 2 风格)
- [ ] PE 分层分析 (Table 3 风格)
- [ ] 站点误差地理分布
- [ ] 报告初稿 & PPT

---

*本文件位于该子仓库根目录，与 `assignment/` 文件夹同级，作为 GitHub 子仓库首页 README。assignment 子目录内为个人负责的三周交付物。*
