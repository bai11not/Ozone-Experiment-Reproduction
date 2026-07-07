# Paper Assets 字段整理

## Table 1: 主对比表

**文件**: `table1_main_raw_comparison.csv`

**字段**: Method, RMSE, MAE, MAPE, Peak_RMSE, Step6_RMSE, Source

**说明**: 包含所有 baseline 方法和本文方法的对比结果

**方法列表**:
- MTGNN
- Graph WaveNet
- AGCRN
- DCRNN
- ATGCN-PE3
- PE-DiffWaveNet

## Table 2: 消融实验表

**文件**: `table2_ablation.csv`

**字段**: Variant, Seeds, RMSE, MAE, MAPE, Step4_6_RMSE, Step6_RMSE, Peak_RMSE

**说明**: 验证 PE 组件的有效性

**变体列表**:
- No-PE backbone
- Safe PE graph+FiLM
- Real PE-guided loss
- Shuffled PE-guided loss
- PE graph only
- PE FiLM only

## Table 3: PE 分层统计表

**文件**: `table3_pe_stratified_summary.csv`

**字段**: group, group_label, stratum, node_count, pe_score_mean, rmse_mean, rmse_std, mae_mean, mae_std, mape_mean, mape_std, step4_6_rmse_avg_mean, step4_6_rmse_avg_std, step6_rmse_mean, step6_rmse_std, rmse_peak_mean, rmse_peak_std, mae_peak_mean, mae_peak_std

**说明**: PE 分层统计结果

## 统一指标字段

| 字段名 | 全称 | 单位 | 说明 |
|--------|------|------|------|
| RMSE | Root Mean Squared Error | μg/m³ | 均方根误差 |
| MAE | Mean Absolute Error | μg/m³ | 平均绝对误差 |
| MAPE | Mean Absolute Percentage Error | % | 平均绝对百分比误差 |
| Peak_RMSE | Peak RMSE | μg/m³ | 峰值时刻 RMSE |
| Step6_RMSE | Step 6 RMSE | μg/m³ | 第6步预测 RMSE |
| Step4_6_RMSE | Steps 4-6 RMSE | μg/m³ | 第4-6步平均 RMSE |

## 数据源标记

| Source | 说明 |
|--------|------|
| official raw, seed42 | 官方代码原始结果，seed=42 |
| ATGCN raw, seed42 | ATGCN 原始结果，seed=42 |
| ours raw, seeds 42/52/62 | 本文方法，多个 seed 平均 |
| Week1 Baseline | Week1 新增 baseline 结果 |
| Week1 Experiment | Week1 实验结果 |
