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

## 实验矩阵

| # | seed | seq_len (T_h) | pre_len (T_p) | 备注 |
|---|------|---------------|---------------|------|
| 1 | 42 | 24 | 6 | 主 baseline |
| 2 | 42 | 24 | 3 | 短预测步 |
| 3 | 42 | 12 | 6 | 短输入窗 |
| 4 | 42 | 12 | 3 | 短输入+短预测 |

## 固定参数

| 参数 | 值 |
|------|-----|
| 数据 | AIR_N95 |
| 模型 | UGnet |
| hidden_size | 32 |
| N (扩散步数) | 200 |
| beta_schedule | quad |
| beta_end | 0.1 |
| batch_size | 32 |
| lr | 1e-4 |
| epochs | 300 |
| early_stop | 10 |
| n_samples | 8 |

## 运行命令

```bash
cd /mnt/d/时空数据/白文豪/week2/DiffSTG

# 实验 1: 主 baseline
python -u /mnt/d/时空数据/白文豪/week1/DiffSTG/train.py \
  --seed 42 --data AIR_N95 --T_h 24 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001

# 实验 2: pre_len=3
python -u /mnt/d/时空数据/白文豪/week1/DiffSTG/train.py \
  --seed 42 --data AIR_N95 --T_h 24 --T_p 3 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001

# 实验 3: seq_len=12, pre_len=6
python -u /mnt/d/时空数据/白文豪/week1/DiffSTG/train.py \
  --seed 42 --data AIR_N95 --T_h 12 --T_p 6 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001

# 实验 4: seq_len=12, pre_len=3
python -u /mnt/d/时空数据/白文豪/week1/DiffSTG/train.py \
  --seed 42 --data AIR_N95 --T_h 12 --T_p 3 \
  --hidden_size 32 --N 200 --batch_size 32 --lr 0.0001
```

## 输出位置

- 日志: `白文豪/week1/DiffSTG/output/log/`
- 模型: `白文豪/week1/DiffSTG/output/model/`
- 指标: `白文豪/week1/DiffSTG/output/metrics/DiffSTG.csv`
- 预测: `白文豪/week1/DiffSTG/output/forecast/`

## 结果汇总

| exp_id | model | seq_len | pre_len | seed | RMSE | MAE | MAPE | 备注 |
|--------|-------|---------|---------|------|------|-----|------|------|
| | | | | | | | | |