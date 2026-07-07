# Week 1 完成报告

## PPT 第 1 周任务对照

| PPT 任务 | 状态 | 产出 |
|----------|------|------|
| 阅读数据说明 | ✅ | 见 data_summary_report.md |
| 统计 O3/PM2.5/PM10 缺失 | ✅ | O3:2.25%, PM2.5:1.33%, PM10:1.55% |
| 画整体时间序列 | ✅ | pollutant_time_series.png |
| 确认 MTGNN/Graph WaveNet/AGCRN | ✅ | 论文结果已在 table1，本项目无源码 |
| 优先调研 DiffSTG | ✅ | diffstg_adaptation_plan.md + flow.npy/adj.npy 已生成 |
| 运行 smoke test | ✅ | 1 epoch, hidden_size=16, 通过 |
| 小配置跑 1-3 epoch | ✅ | PE-DiffWaveNet 3 epoch + ATGCN-PE3 3 epoch |

## 运行过的命令（3 条核心命令）

详见 `commands.sh`

1. **PE-DiffWaveNet smoke test** — 验证环境
   ```
   python train_pediffwavenet_noleak.py --epochs 1 --hidden_size 16 --max_train_windows 8 ...
   ```
2. **PE-DiffWaveNet debug** — 产出第一个有意义的指标
   ```
   python train_pediffwavenet_noleak.py --epochs 3 --hidden_size 16 --max_train_windows 64 ...
   ```
3. **ATGCN-PE3 debug** — baseline 对比
   ```
   python train_atgcn_pe3_noleak.py --epochs 3 --hidden_size 16 --max_train_windows 64 ...
   ```

## 输出目录清单

| 目录 | 内容 |
|------|------|
| `outputs_week1/` | 数据整理：站点表、缺失统计、时间序列图、报告 |
| `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/` | Smoke test 输出 |
| `matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/` | PE-DiffWaveNet 3-epoch debug |
| `matrix_N95_PE3_noleak_atgcn_pe3_cpu_debug/` | ATGCN-PE3 3-epoch debug |
| `data/dataset/AIR_N95/` | DiffSTG 适配数据（flow.npy + adj.npy） |

## Debug 运行指标（仅供参考，非正式结果）

| 模型 | RMSE | MAE | MAPE |
|------|------|-----|------|
| PE-DiffWaveNet (3 epoch) | 163.93 | 161.65 | 759.12% |
| ATGCN-PE3 (3 epoch) | 253.25 | 192.63 | 821.36% |

> ⚠️ 这些指标**没有参考意义**——hidden_size=16, diffusion_steps=10, 仅 3 epoch, 64 训练窗口。
> 论文中 PE-DiffWaveNet 正式结果：RMSE=10.94, MAE=7.56, MAPE=30.79%。

## 关键认知

1. **数据长什么样**：95 个站点 × 8717 小时，O3 + 14 个气象变量 (m=15)，先按时间切分再各自归一化（no-leak）
2. **命令怎么跑**：`train_pediffwavenet_noleak.py` 是主入口，`--device cpu` 可本地跑，关键参数 seq_len/pre_len/seed/hidden_size/diff_steps
3. **输出在哪里**：`matrix_N95_PEDiffWaveNet_noleak_<EXP_NAME>/` 下有 config.json, metrics_summary.json, split_summary.json, graph_summary.json

## 第二周计划

按照 PPT Slide 8 实验矩阵：
- [ ] 主模型完整训练 (hidden_size=64, epochs=120, seq_len=24, pre_len=6, seed=42) — **需要 GPU**
- [ ] 多 seed (42, 52, 62)
- [ ] 多窗口 (seq_len=12, 24, 48)
- [ ] 多步长 (pre_len=1, 3, 6, 12, 24)
- [ ] 消融实验 (USE_DIFFUSION=0 / USE_PE_GRAPH=0 / USE_PE_FILM=0)
- [ ] PE shuffle (PE_SHUFFLE_SEED=52)
- [ ] DiffSTG 正式训练 — **需要 GPU**
