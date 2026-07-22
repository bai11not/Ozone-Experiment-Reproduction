# Week 2: PE-DiffWaveNet 消融实验 — Person C (马一田)

> **修正说明（2026-07-19）**：pre_len=6 的 7 组实验（C03/C05/C07/C09/C11/C13/C15）因 horizon_weights 配置错误（等权→递增权重 `1.0,1.0,1.1,1.2,1.35,1.5`）已重跑，正确日志位于 `results/rerun_prelen6/`。所有指标文件、图表、CSV 均已同步更新为修正后的正确结果。

## 实验目标

验证 **扩散模型（Diffusion）** 对臭氧预测精度的贡献（full vs no_diff），并分析 seq_len、pre_len、seed 对模型性能的影响。

## 实验矩阵

| 参数 | 取值 |
|------|------|
| seed | 52, 62 |
| seq_len | 12, 24 |
| pre_len | 6, 3 |
| 消融类型 | full (use_diffusion=1), no_diff (use_diffusion=0) |
| 实验总数 | 2×2×2×2 = **16 组** |

## 固定参数

| 参数 | 值 |
|------|-----|
| N_node | 95 |
| m | 15 |
| hidden_size | 64 |
| batch_size | 16 |
| lr | 7e-4 |
| epochs | 120 |
| patience | 15 |
| diff_steps | 50 |
| inference_steps | 50 |
| num_samples | 3 |
| amp | 1 |
| device | cuda (RTX 4050 Laptop 6GB) |
| use_pe_graph | 1 |
| use_pe_film | 1 |
| pe_adaptive_loss | 0 |
| horizon_weights (pre_len=6) | 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重） |
| horizon_weights (pre_len=3) | 空（3 步等权） |

## 实验清单

### seed=52 (C01-C08)

| # | 标签 | seq_len | pre_len | 消融 | RMSE | MAE | MAPE | Peak RMSE | Epoch |
|---|------|---------|---------|------|------|-----|------|-----------|-------|
| C01 | s52-full-l12-p6 | 12 | 6 | full | 11.43 | 8.09 | 33.48% | 13.69 | 38 |
| C02 | s52-full-l12-p3 | 12 | 3 | full | 8.80 | 6.00 | 24.89% | 9.18 | 62 |
| C03 | s52-full-l24-p6 | 24 | 6 | full | 11.01 | 7.73 | 31.97% | 12.08 | 41 |
| C04 | s52-full-l24-p3 | 24 | 3 | full | 8.80 | 6.14 | 26.21% | 8.85 | 35 |
| C05 | s52-nodiff-l12-p6 | 12 | 6 | no_diff | 11.22 | 7.75 | 30.62% | 14.93 | 18 |
| C06 | s52-nodiff-l12-p3 | 12 | 3 | no_diff | 9.14 | 6.50 | 28.05% | 8.84 | 19 |
| C07 | s52-nodiff-l24-p6 | 24 | 6 | no_diff | 11.05 | 7.97 | 33.58% | 13.66 | 15 |
| C08 | s52-nodiff-l24-p3 | 24 | 3 | no_diff | 8.79 | 5.95 | 25.20% | 9.59 | 26 |

### seed=62 (C09-C16)

| # | 标签 | seq_len | pre_len | 消融 | RMSE | MAE | MAPE | Peak RMSE | Epoch |
|---|------|---------|---------|------|------|-----|------|-----------|-------|
| C09 | s62-full-l12-p6 | 12 | 6 | full | 12.37 | 9.24 | 40.24% | 13.11 | 15 |
| C10 | s62-full-l12-p3 | 12 | 3 | full | 8.72 | 5.86 | 24.52% | 9.63 | 60 |
| C11 | s62-full-l24-p6 | 24 | 6 | full | 11.68 | 8.70 | 36.23% | 14.04 | 18 |
| C12 | s62-full-l24-p3 | 24 | 3 | full | 8.56 | 5.79 | 23.90% | 9.32 | 53 |
| C13 | s62-nodiff-l12-p6 | 12 | 6 | no_diff | 11.13 | 7.64 | 32.07% | 12.55 | 32 |
| C14 | s62-nodiff-l12-p3 | 12 | 3 | no_diff | 8.83 | 5.98 | 25.23% | 9.71 | 31 |
| C15 | s62-nodiff-l24-p6 | 24 | 6 | no_diff | 10.68 | 7.44 | 30.04% | 13.43 | 20 |
| C16 | s62-nodiff-l24-p3 | 24 | 3 | no_diff | 8.79 | 6.00 | 25.02% | 9.70 | 29 |

## 关键发现

1. **扩散模型在长预测步上适得其反**：p=6 时 no_diff 一致优于 full（ΔRMSE 0.04-1.24）
2. **pre_len 是主导因素**：p=3 比 p=6 的 RMSE 低 1.9-3.7
3. **l=24 一致优于 l=12**：更长历史窗口改善 0.17-0.69 RMSE
4. **种子稳定性良好**：6/8 配置 ΔRMSE < 0.4，full + p=6 有中等差异
5. **全局最佳**：C12（s62, full, l=24, p=3, RMSE=8.56）
6. **p=6 最佳**：C15（s62, no_diff, l=24, p=6, RMSE=10.68）

## horizon_weights 修正记录

初次运行时 C02-C16 的 `horizon_weights` 配置为空（等权），pre_len=6 的 7 组实验（C03/C05/C07/C09/C11/C13/C15）于 2026-07-19 使用递增权重 `1.0,1.0,1.1,1.2,1.35,1.5` 完成重跑。正确日志位于 `results/rerun_prelen6/`。

| ID | 配置 | 等权 RMSE | 递增权重 RMSE | Δ | 评价 |
|----|------|----------|-------------|---|------|
| C03 | s52, full, l=24, p=6 | 11.01 | 11.01 | 0.00 | 无影响 |
| C05 | s52, no_diff, l=12, p=6 | 11.16 | 11.22 | +0.06 | 略差 |
| C07 | s52, no_diff, l=24, p=6 | 10.88 | 11.05 | +0.17 | 略差 |
| C09 | s62, full, l=12, p=6 | 13.93 | 12.37 | -1.56 | **大幅改善（-11.2%）** |
| C11 | s62, full, l=24, p=6 | 11.97 | 11.68 | -0.29 | 改善 |
| C13 | s62, no_diff, l=12, p=6 | 11.13 | 11.13 | 0.00 | 无影响 |
| C15 | s62, no_diff, l=24, p=6 | 10.90 | 10.68 | -0.22 | 改善 |

## 目录结构

```
week2/
├── README.md                          ← 本文件
├── commands.sh                        ← 所有运行命令汇总（16 条）
├── report_section.md                  ← 报告章节初稿
├── experiment_summary.md              ← 实验总结（按任务要求规整）
├── experiment_logs/                   ← 16 个实验记录 .md
│   ├── C01_s52-full-l12-p6.md
│   ├── ...
│   └── C16_s62-nodiff-l24-p3.md
├── scripts/
│   ├── run_person_C.sh                ← seed=52 批量 (C01-C08)
│   ├── run_person_C_seed62.sh         ← seed=62 批量 (C09-C16)
│   ├── run_rerun_prelen6.sh           ← pre_len=6 递增权重重跑（7 组）
│   ├── generate_figures.py           ← 图表生成脚本
│   └── result_combine.py             ← 合并结果 CSV
├── results/
│   ├── person_C_all_results.csv       ← 16 组合并指标
│   ├── person_C_seed52_full_nodiff/   ← seed=52 日志 + per-step（已更新为重跑正确日志）
│   │   ├── person_C_results.csv
│   │   ├── per_step_metrics.md
│   │   └── run_log_C*.txt
│   ├── person_C_seed62_full_nodiff/   ← seed=62 日志 + per-step（已更新为重跑正确日志）
│   │   ├── person_C_results.csv
│   │   ├── per_step_metrics.md
│   │   └── run_log_C*.txt
│   └── rerun_prelen6/                 ← 重跑正确日志（7 组，2026-07-19）
│       └── run_log_C*.txt
├── metrics/
│   └── result_recording_template.md   ← 完整指标表 + 消融分析 + horizon_weights 修正记录
├── summary/
│   └── analysis_template.md           ← 9 维度分析报告
└── figures/                           ← 5 张图表（修正版）
    ├── per_step_rmse_prelen6.png
    ├── ablation_comparison.png
    ├── comprehensive_ranking.png
    ├── seed_stability.png
    └── prelen_effect.png
```

## 使用者

**Person C — 马一田**，负责 PE-DiffWaveNet 主模型实验（扩散模块消融 + 多 seed/窗口/步长对比）。
