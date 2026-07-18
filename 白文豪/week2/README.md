# Week 2: DiffSTG Baseline 实验

## 实验目标

完成 DiffSTG 最低要求：
1. 用本项目 AIR_N95 数据跑通 DiffSTG
2. 跑 seq_len=24, pre_len=6, seed=42 作为主 baseline
3. 输出 RMSE、MAE、MAPE
4. 填入 experiment_result_template.csv

## 与 PE-DiffWaveNet 的关系

- **PE-DiffWaveNet**: 面向空气质量复杂性、PE 特征增强的扩散预测模型（我们的主模型）
- **DiffSTG**: 通用概率时空图扩散预测模型（对比 baseline）

## 进阶实验目标

1. 不同预测步长：pre_len=1, 3, 6, 12, 24
2. 多污染物预测：O3、PM2.5、PM10
3. 不同邻接矩阵：空间距离图、相关图（CORR）、PE 图
4. 概率预测指标（CRPS）和置信区间分析

## 实验矩阵与结果

### 1. 不同预测步长（O3, 空间距离图, seed=42）

| # | T_h | T_p | best_epoch | Test RMSE | Test MAE | Test MAPE | Test CRPS | 状态 |
|---|-----|-----|------------|-----------|---------|-----------|-----------|------|
| 1 | 24 | 1 | 47 | 0.0244 | 0.0192 | 87.54 | 0.1766 | ✅ 完成 |
| 2 | 24 | 3 | 90 | 0.0452 | 0.0373 | 200.26 | 0.3403 | ✅ 完成 |
| 3 | 24 | 6 | 45 | 0.0628 | 0.0505 | 290.32 | 0.4775 | ✅ 完成 |
| 4 | 24 | 12 | 15 | 0.0809 | 0.0653 | 393.28 | 0.6207 | ✅ 完成 |
| 5 | 24 | 24 | — | — | — | — | — | 🔄 运行中 |

### 2. 多污染物预测（T_h=24, T_p=6, 空间距离图, seed=42）

| # | 污染物 | best_epoch | Test RMSE | Test MAE | Test MAPE | Test CRPS | 状态 |
|---|--------|------------|-----------|---------|-----------|-----------|------|
| 1 | O3 | 45 | 0.0628 | 0.0505 | 290.32 | 0.4775 | ✅ 完成 |
| 2 | PM2.5 | 48 | 0.0537 | 0.0283 | — | 0.3709 | ✅ 完成 |
| 3 | PM10 | 27 | 0.0400 | 0.0140 | 63.28 | 0.3969 | ✅ 完成 |

### 3. 不同邻接矩阵（T_h=24, T_p=6, O3, seed=42）

| # | 邻接矩阵 | 说明 | best_epoch | Test RMSE | Test MAE | Test CRPS | 状态 |
|---|---------|------|------------|-----------|---------|-----------|------|
| 1 | 空间距离图 | 高斯核（σ=50km, 阈值150km） | 45 | 0.0628 | 0.0505 | 0.4775 | ✅ 完成 |
| 2 | 相关图 (CORR) | 基于O3时间序列相关性 | 28 | 0.0629 | 0.0504 | 0.4774 | ✅ 完成 |
| 3 | PE 图 | 基于位置编码相似性 | 55 | 0.0568 | 0.0455 | 0.4218 | ✅ 完成 |

### 4. 概率预测指标

所有实验均已记录 CRPS（连续排名概率评分）和 MIS（区间评分），用于评估概率预测质量。置信区间可视化待完成。

## 固定参数

| 参数 | 值 |
|------|-----|
| 模型 | UGnet |
| hidden_size | 32 |
| N (扩散步数) | 200 |
| beta_schedule | quad |
| beta_end | 0.1 |
| batch_size | 32 |
| lr | 1e-4 |
| epochs | 300 |
| early_stop | 10 |
| min_delta | 0.001 |
| n_samples | 8 |
| sample_strategy | ddim_multi |
| sample_steps | 40 |

## 运行命令

```bash
cd /mnt/d/时空数据/白文豪/week2/DiffSTG

# pre_len=1
python -u train_full.py --seed 42 --data AIR_N95 --T_h 24 --T_p 1 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/prelen1_train.log

# pre_len=3
python -u train_full.py --seed 42 --data AIR_N95 --T_h 24 --T_p 3 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pre3_train.log

# pre_len=6 (baseline)
python -u train_full.py --seed 42 --data AIR_N95 --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/baseline_train.log

# pre_len=12
python -u train_full.py --seed 42 --data AIR_N95 --T_h 24 --T_p 12 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pre12_train.log

# pre_len=24 (运行中)
python -u train_full.py --seed 42 --data AIR_N95 --T_h 24 --T_p 24 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pre24_train.log

# PM2.5
python -u train_full.py --seed 42 --data AIR_N95_PM25 --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pm25_train.log

# PM10
python -u train_full.py --seed 42 --data AIR_N95_PM10 --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pm10_train.log

# CORR 邻接矩阵
python -u train_full.py --seed 42 --data AIR_N95_CORR --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/corr_train.log

# PE 邻接矩阵
python -u train_full.py --seed 42 --data AIR_N95_PE --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001 \
  --epochs 300 --early_stop 10 --min_delta 0.001 \
  --output_dir ./output 2>&1 | tee ./output/pe_train.log
```

## 输出位置

- 日志: `白文豪/week2/DiffSTG/output/*.log`
- JSON 指标: `白文豪/week2/DiffSTG/results/*.json`
- 模型权重: `白文豪/week1/DiffSTG/output/model/`
- 预测: `白文豪/week1/DiffSTG/output/forecast/`

## 指标说明

- MAE/RMSE 为 z-score 归一化值（不是原始 μg/m³）
- MAPE 在 O3 数据上偏大（含接近0的值，百分比放大）
- CRPS 和 MIS 为概率预测指标，越低越好