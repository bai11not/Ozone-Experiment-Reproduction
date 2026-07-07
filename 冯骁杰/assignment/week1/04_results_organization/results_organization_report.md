# 结果整理报告

> **生成日期**: 2026-07-06
> **对应任务**: 第 1 周 — 数据理解和代码跑通 → 结果整理
> **对齐目标**: `paper_assets_pediffwavenet/` 表格字段

---

## 1. 统一指标字段确认

### 1.1 核心字段 (所有实验必须包含)

| 字段 | 英文名 | 类型 | 说明 |
|------|--------|------|------|
| RMSE | Root Mean Square Error | float | 均方根误差，单位 μg/m³ |
| MAE | Mean Absolute Error | float | 平均绝对误差，单位 μg/m³ |
| MAPE | Mean Absolute Percentage Error | float | 平均绝对百分比误差，单位 % |
| Peak RMSE | Peak RMSE | float | 高值区(O3>阈值)的 RMSE |
| Step6 RMSE | Per-step RMSE at horizon 6 | float | 第 6 预测步的 RMSE |

### 1.2 扩展字段 (推荐包含)

| 字段 | 说明 |
|------|------|
| Step1 RMSE | 第 1 预测步的 RMSE |
| Step4_6_RMSE | 第 4-6 步平均 RMSE (table2 使用) |
| Per-step RMSE | 每步 RMSE 列表 (1..pre_len) |
| Per-step MAE | 每步 MAE 列表 |
| Relative RMSE | RMSE / O3_train_max × 100 |
| Relative MAE | MAE / O3_train_max × 100 |
| Peak Count | 高值样本数 |
| Peak Ratio | 高值样本占比 |

### 1.3 实验追踪字段

| 字段 | 来源 | 示例 |
|------|------|------|
| `model` | 模型名称 | PE-DiffWaveNet, MTGNN, AGCRN |
| `seq_len` | 输入窗口长度 | 24 |
| `pre_len` | 预测步长 | 6 |
| `seed` | 随机种子 | 42 |
| `use_diffusion` | 是否使用扩散 | 1 |
| `use_pe_graph` | 是否使用 PE 图 | 1 |
| `use_pe_film` | 是否使用 PE FiLM | 1 |
| `pe_adaptive_loss` | PE 自适应损失 | 0 |
| `lr` | 学习率 | 7e-4 |
| `epochs` | 训练轮数 | 120 |
| `best_epoch` | 最佳 epoch | 45 |
| `output_dir` | 输出目录路径 | matrix_N95_PEDiffWaveNet_noleak_xxx |
| `log_file` | 日志文件路径 | — |
| `notes` | 备注 | 异常/失败原因 |

---

## 2. Paper Assets 表格字段对齐

### 2.1 table1 — 主对比表

**原文件**: `paper_assets_pediffwavenet/table1_main_raw_comparison.csv`

| 原始字段 | 类型 | 说明 |
|----------|------|------|
| Method | str | 模型名 + 配置 (如 "MTGNN (L=24)") |
| RMSE | float | 测试集 RMSE |
| MAE | float | 测试集 MAE |
| MAPE | float | 测试集 MAPE |
| Peak_RMSE | float | 高值区 RMSE |
| Step6_RMSE | float | 第 6 步 RMSE |
| Source | str | 数据来源标注 |

**新增字段对齐** (学生结果需补充):

| 建议新增 | 对应模板字段 |
|----------|-------------|
| Seeds | 多 seed 时注明 (如 "42,52,62") |
| Config | 关键配置摘要 (如 "L=24, P=6") |
| Status | 结果来源 (如 "reproduced", "from paper") |

### 2.2 table2 — 消融实验表

**原文件**: `paper_assets_pediffwavenet/table2_ablation.csv`

| 原始字段 | 类型 | 说明 |
|----------|------|------|
| Variant | str | 变体名称 |
| Seeds | str | seed 列表 |
| RMSE | str | 均值 ± 标准差 |
| MAE | str | 均值 ± 标准差 |
| MAPE | str | 均值 ± 标准差 |
| Step4_6_RMSE | str | 第 4-6 步平均 RMSE (均值 ± 标准差) |
| Step6_RMSE | str | 第 6 步 RMSE |
| Peak_RMSE | str | 高值区 RMSE |

**消融变体清单**:

| 变体 | use_diffusion | use_pe_graph | use_pe_film | pe_adaptive_loss |
|------|:---:|:---:|:---:|:---:|
| 完整模型 (backbone) | 1 | 1 | 1 | 0 |
| Safe PE graph+FiLM | 1 | 1 | 1 | 0 |
| PE-guided loss | 1 | 1 | 1 | 1 |
| Shuffled PE-guided loss | 1 | 1 | 1 | 1† |
| PE graph only | 1 | 1 | 0 | 0 |
| PE FiLM only | 1 | 0 | 1 | 0 |
| 无扩散 (No diffusion) | 0 | 1 | 1 | 0 |

> † PE_SHUFFLE_SEED=52

### 2.3 table3 — PE 分层统计表

**原文件**: `paper_assets_pediffwavenet/table3_pe_stratified_summary.csv`

| 原始字段 | 类型 | 说明 |
|----------|------|------|
| group | str | 实验组 (如 `base_hw`, `pe_loss`) |
| group_label | str | 组标签 |
| stratum | str | 分层 (all_nodes, low_pe, mid_pe, high_pe) |
| node_count | int | 该层站点数 |
| pe_score_mean | float | PE 得分均值 |
| rmse_mean / rmse_std | float | RMSE 均值和标准差 |
| mae_mean / mae_std | float | MAE 均值和标准差 |
| mape_mean / mape_std | float | MAPE 均值和标准差 |
| step4_6_rmse_avg_mean / std | float | 第 4-6 步平均 RMSE |
| step6_rmse_mean / std | float | 第 6 步 RMSE |
| rmse_peak_mean / std | float | 高值区 RMSE |
| mae_peak_mean / std | float | 高值区 MAE |

**PE 分层定义**:
- `low_pe`: PE 得分最低的 1/3 站点 (较规律)
- `mid_pe`: PE 得分中等的 1/3 站点
- `high_pe`: PE 得分最高的 1/3 站点 (较复杂)

---

## 3. 模板使用指南

### 3.1 实验记录模板 (`templates/experiment_log_template.md`)

每次实验填写一份，包含:
1. **基本信息**: 组别、学生、日期、实验编号
2. **运行命令**: 完整的 bash 命令
3. **关键配置**: seq_len, pre_len, seed, device, epochs, batch_size, use_diffusion, use_pe_graph, use_pe_film, pe_adaptive_loss
4. **输出位置**: 输出目录、权重目录、日志文件
5. **指标**: RMSE / MAE / MAPE / Peak RMSE / Step6 RMSE
6. **现象和结论**: 3-5 句话分析
7. **问题**: 报错/异常/显存不足等

### 3.2 结果汇总模板 (`templates/experiment_result_template.csv`)

字段列表:
```
group, student, experiment_id, model, seq_len, pre_len, seed,
use_diffusion, use_pe_graph, use_pe_film, pe_adaptive_loss,
lr, epochs, best_epoch,
rmse, mae, mape, peak_rmse, step1_rmse, step6_rmse,
output_dir, log_file, notes
```

### 3.3 报告提纲模板 (`templates/report_outline.md`)

8 个章节: 实习背景 → 数据集 → 方法 → 实验设置 → 结果 → 分析 → 问题改进 → 总结

---

## 4. 统一结果表构建

### 4.1 已有结果 (来自 paper_assets)

见 `assignment/week1/results.csv` — 包含 table1 全部 9 行 + smoke test 记录。

### 4.2 待填充的实验

| 序号 | 实验 | 模型 | 配置 | 状态 |
|------|------|------|------|------|
| 1 | 主实验 | PE-DiffWaveNet | L=24, P=6, S=42 | ⏳ 待运行 |
| 2 | 主实验 | PE-DiffWaveNet | L=24, P=6, S=52 | ⏳ 待运行 |
| 3 | 主实验 | PE-DiffWaveNet | L=24, P=6, S=62 | ⏳ 待运行 |
| 4 | 消融-无扩散 | PE-DiffWaveNet | L=24, P=6, D=0 | ⏳ 待运行 |
| 5 | 消融-无PE图 | PE-DiffWaveNet | L=24, P=6, G=0 | ⏳ 待运行 |
| 6 | 消融-无PE FiLM | PE-DiffWaveNet | L=24, P=6, F=0 | ⏳ 待运行 |
| 7 | 消融-PE shuffle | PE-DiffWaveNet | L=24, P=6, shuffle=52 | ⏳ 待运行 |
| 8 | 输入窗口12 | PE-DiffWaveNet | L=12, P=6 | ⏳ 待运行 |
| 9 | 输入窗口48 | PE-DiffWaveNet | L=48, P=6 | ⏳ 待运行 |
| 10 | 预测步长1 | PE-DiffWaveNet | L=24, P=1 | ⏳ 待运行 |
| 11 | 预测步长3 | PE-DiffWaveNet | L=24, P=3 | ⏳ 待运行 |
| 12 | 预测步长12 | PE-DiffWaveNet | L=24, P=12 | ⏳ 待运行 |
| 13 | 预测步长24 | PE-DiffWaveNet | L=24, P=24 | ⏳ 待运行 |
| 14 | ATGCN-PE3 | ATGCN-PE3 | L=12, P=6, noleak | ⏳ 待复核 |
| 15 | DiffSTG | DiffSTG | L=12, P=12 | ⏳ 待运行 |

---

## 5. 结果提交流程

```
单个实验
  │
  ├── 填写 experiment_log_template.md (实验记录)
  ├── 更新 results.csv (追加一行)
  ├── 保存输出目录 (metrics_summary.json + 预测文件)
  └── 生成图表 (按命名规范)

汇总阶段 (结果整理组)
  │
  ├── 合并所有 results.csv → merged_results.csv
  ├── 生成 table1 / table2 / table3 风格表格
  ├── 按 chart_naming_convention.md 统一图表命名
  └── 写入报告对应章节
```

---

## 6. 交付产物清单

```
assignment/week1/
├── results_organization_report.md   # 本文件 ★
├── chart_naming_convention.md       # 图表命名规范 ★
├── results.csv                      # 统一结果表 (已有 + 待填充)
├── data_organization_output/        # 数据整理结果
├── baseline_report.md               # Baseline 调研报告
├── pediffwavenet_experiment.md      # PE-DiffWaveNet 实验报告
├── commands.sh                      # 所有运行命令
└── README.md                        # 第 1 周总览
```

---

*本报告为第 1 周结果整理任务产出，定义了后续两周实验的统一字段、命名规范和提交流程。*
