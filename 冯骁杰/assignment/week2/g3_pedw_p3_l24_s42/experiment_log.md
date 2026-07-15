# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-14
- 实验编号：g3_pedw_p3_l24_s42
- 模型：PE-DiffWaveNet (Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_pedw_p3_l24_s42"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 3 --seq_len 24 --seed 42 `
  --N_node 95 --m 15 `
  --hidden_size 64 --batch_size 16 `
  --lr 7e-4 --epochs 120 --patience 15 `
  --diff_steps 50 --inference_steps 50 --num_samples 3 `
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --horizon_weights "1.0,1.0,1.0" `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 24
- pre_len: **3** ← 本次实验变更
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 52)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.0]（pre_len=3，使用均匀权重）
- pe_adaptive_loss: 0

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p3_l24_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_pedw_p3_l24_s42/
- 日志文件：assignment/week2/g3_pedw_p3_l24_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 8.6170 | 5.8386 | 24.00% | 9.8890 | 6.3280 | 10.3011 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 6.3280 | 8.7523 | 10.3011 |

## 对比：pre_len=3 vs pre_len=6（基准）

| 指标 | pre_len=6 (基准) | pre_len=3 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.0658 | 8.6170 | **-2.45** ↓ |
| MAE | 7.6683 | 5.8386 | **-1.83** ↓ |
| MAPE | 30.88% | 24.00% | **-6.88pp** ↓ |
| Peak RMSE | 13.9266 | 9.8890 | **-4.04** ↓ |
| Step1 RMSE | 6.6469 | 6.3280 | -0.32 |

## 现象和结论

1. 预测步长从 6 缩至 3 后，所有指标大幅改善：RMSE 从 11.07 降至 8.62（-22%），MAPE 从 30.88% 降至 24.00%（-6.88pp），符合短时预测精度更高的预期。
2. Peak RMSE 从 13.93 降至 9.89（-29%），说明短预测范围内对高浓度峰值的捕获更为准确。
3. Step1 RMSE 基本持平（6.33 vs 6.65），说明即时预测精度主要受历史信息制约，与预测步长关系较小。
4. 收敛速度：best epoch 52，与基准实验 epoch 50 接近。

## 问题

1. horizon_weights 从默认 6 值改为 3 值均匀权重 `[1.0, 1.0, 1.0]`，与基准实验的递增权重方案不完全可比，需在对比时注意。
