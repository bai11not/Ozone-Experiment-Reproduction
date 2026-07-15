# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_nodiff_pe_p6_l12_s42
- 模型：PE-Graph (no Diffusion) — PE Graph + PE-FiLM，无扩散模块
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_nodiff_pe_p6_l12_s42"

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
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 12
- pre_len: 6
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 19)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: **0** ← 消融变量
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.1, 1.2, 1.35, 1.5]（默认）
- pe_adaptive_loss: 0
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_nodiff_pe_p6_l12_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_nodiff_pe_p6_l12_s42/
- 日志文件：assignment/week2/g3_nodiff_pe_p6_l12_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.3065 | 7.7523 | 31.26% | 14.5219 | 6.6742 | 14.2207 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 6.6742 | 9.0721 | 10.7927 | 12.1122 | 13.2193 | 14.2207 |

## 消融对比：Diffusion vs noDiff（seq_len=12, pre_len=6）

| 指标 | PE-DiffWaveNet (exp3) | PE-Graph noDiff (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.5857 | 11.3065 | **−0.28** ↓ |
| MAE | 8.3674 | 7.7523 | **−0.62** ↓ |
| MAPE | 34.50% | 31.26% | **−3.24pp** ↓ |
| Peak RMSE | 12.7160 | 14.5219 | **+1.81** ↑ |
| Best Epoch | 30 | 19 | −11 |

## 现象和结论

1. seq_len=12 + pre_len=6 下关闭扩散模块后，整体 RMSE/MAE/MAPE 反而略优于扩散版本（RMSE 11.31 vs 11.59），与 exp5 的趋势一致——在短历史窗口下扩散模块的收益有限甚至为负。
2. Peak RMSE 仍然遵循扩散→无扩散恶化的规律（+1.81），再次验证扩散过程的核心价值在于峰值预测精度。
3. 无扩散模型收敛更快（best epoch 19 vs 30），但也更早进入过拟合（Val RMSE 在 epoch 19 后持续上升）。
4. 训练初期（epoch 1-3）出现大量 `skip non-finite grad` 警告，说明无扩散 + 短序列组合下梯度稳定性较差。

## 问题

1. 训练初期频繁出现梯度溢出警告，可能导致模型收敛于次优解。
2. Val RMSE 在 best epoch 后快速反弹（11.98→13.51），说明无扩散模型的泛化能力较弱。
