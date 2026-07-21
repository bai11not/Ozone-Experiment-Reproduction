# 统一结果框架

## 1. 标准指标字段

| 字段 | 说明 | 方向 |
|------|------|------|
| RMSE | 均方根误差 (μg/m³) | ↓ 越小越好 |
| MAE | 平均绝对误差 (μg/m³) | ↓ 越小越好 |
| MAPE | 平均绝对百分比误差 (%) | ↓ 越小越好 |
| Peak_RMSE | 峰值 RMSE（预测>160μg/m³的窗口） | ↓ 越小越好 |
| Step6_RMSE | 第6步（最远预测步）RMSE | ↓ 越小越好 |
| Step4_6_RMSE | 第4-6步平均 RMSE | ↓ 越小越好 |

## 2. 图表命名规范

```
{model}_{pollutant}_{metric}_{detail}.{ext}

示例:
  pediffwavenet_O3_ts_pred_vs_true.png     # PE-DiffWaveNet O3预测vs真实时间序列
  pediffwavenet_O3_scatter_test.png         # 测试集散点图
  comparison_O3_rmse_bar.png                # 各模型RMSE柱状图
  ablation_O3_rmse_bar.png                  # 消融实验RMSE
  pe_stratified_O3_rmse_box.png             # PE分层RMSE箱线图
  station_map_95.png                        # 95站点地图
  missing_heatmap_O3.png                    # O3缺失热力图
  time_series_O3_PM25_PM10.png             # 三污染物时间序列
```

### 命名要素
- `model`: pediffwavenet / mtgnn / graphwavenet / agcrn / dcrnn / atgcn_pe3
- `pollutant`: O3 / PM25 / PM10
- `metric`: rmse / mae / mape / peak / step6
- `detail`: bar / box / scatter / ts (time series) / heatmap

## 3. 统一结果表 (CSV)

见 `unified_results.csv`，字段对齐 paper_assets 的 table1。

## 4. 已有结果汇总

### Table 1: 主对比表 (O3, seq_len=24, pre_len=6)

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE | Source |
|--------|------|-----|------|-----------|------------|--------|
| MTGNN (L=24) | 10.6620 | 7.3383 | 29.99 | 13.3536 | 13.1806 | official raw, seed42 |
| MTGNN (L=12) | 10.8028 | 7.3465 | 30.50 | 13.3002 | 13.3112 | official raw, seed42 |
| Graph WaveNet (L=12) | 11.5354 | 7.7982 | 33.60 | 11.8217 | 14.6265 | official raw, seed42 |
| AGCRN (L=12) | 11.6858 | 8.2093 | 34.78 | 15.0214 | 14.5599 | official raw, seed42 |
| DCRNN | 12.2813 | 8.5124 | 36.46 | 15.5737 | 15.7136 | official raw, seed42 |
| ATGCN-PE3 noleak | 11.8944 | 8.6023 | 35.46 | 16.1119 | 14.6744 | ATGCN raw, seed42 |
| ATGCN-PE3 + hw loss | 11.7549 | 8.4868 | 35.98 | 15.6276 | 14.5510 | ATGCN raw, seed42 |
| **PE-DiffWaveNet backbone** | **10.9380** ±0.34 | **7.5618** ±0.20 | **30.79** ±0.85 | 13.8293 | 13.6100 | seeds 42/52/62 |
| PE-DiffWaveNet + PE loss | 11.1021 ±0.15 | 7.7966 ±0.13 | 31.88 ±0.52 | 13.8010 | 13.6831 | seeds 42/52/62 |

### Table 2: 消融实验

| Variant | RMSE | MAE | MAPE | Step6_RMSE | Peak_RMSE |
|---------|------|-----|------|------------|-----------|
| No-PE backbone | 10.9380 | 7.5618 | 30.79 | 13.6100 | 13.8293 |
| Safe PE graph+FiLM | 10.9812 | 7.6301 | 31.66 | 13.6922 | 13.4515 |
| Real PE-guided loss | 11.1021 | 7.7966 | 31.88 | 13.6831 | 13.8010 |
| Shuffled PE-guided loss | 11.1371 | 7.7180 | 31.46 | 13.8141 | 13.7986 |
| PE graph only | 11.0501 | 7.7438 | 31.47 | 13.7110 | 13.6175 |
| PE FiLM only | 12.1876 | 8.9160 | 37.11 | 14.7159 | 13.7838 |

### 关键发现
1. MTGNN (L=24) 在 RMSE 上微弱领先 (10.662 vs 10.938)
2. PE-DiffWaveNet backbone 是综合最优的内部方法
3. PE FiLM only 表现最差 (RMSE=12.19)，说明 PE graph 是核心组件
4. Real PE-guided loss 反而略差于 backbone，需要分析原因

## 5. Smoke Test 验证结果

**命令**（Windows, CPU）:
```bash
export PYTHONPATH="<ROOT>/code"
python -u code/train_pediffwavenet_noleak.py \
  --data_dir "<ROOT>" \
  --device cpu --exp_name student_smoke_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 --hidden_size 16 \
  --batch_size 2 --eval_batch_size 2 \
  --epochs 1 --patience 1 \
  --diff_steps 3 --inference_steps 2 \
  --num_samples 1 --eval_inference_steps 2 --eval_num_samples 1 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 --max_valid_windows 4 --max_test_windows 4 \
  --save_predictions 0 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 1
```

**验证结果**:
- 数据加载: ✅ trainX=(8,24,95,15), trainY=(8,6,95)
- PE特征构建: ✅ 95/95 nodes, scales=[6,9,12,24,48,72]
- 图构建: ✅ S=691 nnz, T=1570 nnz, PE=317 nnz
- 模型参数: ✅ 46,451
- 训练收敛: ✅ Loss 1.77 (仅1 epoch，指标正常)
- 输出文件: ✅ metrics_summary.json, config.json, split_summary.json, checkpoints
- 输出目录: ✅ matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/
- 权重目录: ✅ weights_N95/weights_pediffwavenet_noleak_student_smoke_cpu/

**数据切分**（no-leak）:
- Train: 7378 时间点 (2022-01-01 ~ 2022-11-05)
- Valid: 669 时间点 (2022-11-06 ~ 2022-12-03)
- Test: 670 时间点 (2022-12-03 ~ 2022-12-31)
