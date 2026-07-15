# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p6_l12_s42
- 模型：PE-DiffWaveNet (Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_pedw_p6_l12_s42"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 6 --seq_len 12 --seed 42 `
  --N_node 95 --m 15 `
  --hidden_size 64 --batch_size 16 `
  --lr 7e-4 --epochs 120 --patience 15 `
  --diff_steps 50 --inference_steps 50 --num_samples 3 `
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: **12** ← 本次实验变更
- pre_len: 6
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 30)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.1, 1.2, 1.35, 1.5]（默认）
- pe_adaptive_loss: 0
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p6_l12_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_pedw_p6_l12_s42/
- 日志文件：assignment/week2/g3_pedw_p6_l12_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.5857 | 8.3674 | 34.50% | 12.7160 | 7.4382 | 14.1008 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 7.4382 | 10.0812 | 11.1313 | 12.2592 | 13.2435 | 14.1008 |

## 对比：seq_len=12 vs seq_len=24（pre_len=6 固定）

| 指标 | seq_len=24 (基准) | seq_len=12 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.0658 | 11.5857 | **+0.52** ↑ |
| MAE | 7.6683 | 8.3674 | **+0.70** ↑ |
| MAPE | 30.88% | 34.50% | **+3.62pp** ↑ |
| Peak RMSE | 13.9266 | 12.7160 | **−1.21** ↓ |
| Step1 RMSE | 6.6469 | 7.4382 | +0.79 |
| Step6 RMSE | 13.8245 | 14.1008 | +0.28 |

## 现象和结论

1. seq_len=12 + pre_len=6 在所有主流指标上均劣于 seq_len=24 + pre_len=6（RMSE +0.52, MAPE +3.62pp），进一步验证了更长历史窗口对长期预测的重要性。
2. 与 exp2（seq_len=12, pre_len=3）相比：pre_len 从 3 升至 6 导致 RMSE 从 9.11 升至 11.59（+27%），说明在短历史窗口下，长预测步长的难度显著增加。
3. Peak RMSE 方面，seq_len=12 反而更好（12.72 vs 13.93），与 exp2 的发现一致——短序列模型可能对峰值定位更敏感。
4. Per-step RMSE 保持单调递增趋势（7.44→14.10），符合扩散预测的典型衰减特征。

## 问题

1. PE 计算在此配置下同样出现瞬态内存错误，通过 PE 缓存策略绕过。
2. seq_len=12 的训练数据窗口数更多（7361 vs 7349），但信息量更少，导致模型性能下降。
