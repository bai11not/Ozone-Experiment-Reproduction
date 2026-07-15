# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-14
- 实验编号：g3_nodiff_pe_p6_l24_s42
- 模型：PE-Graph (no Diffusion) — PE Graph + PE-FiLM，无扩散模块
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_nodiff_pe_p6_l24_s42"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 6 --seq_len 24 --seed 42 `
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

- seq_len: 24
- pre_len: 6
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 15)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: **0** ← 本次实验变更
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1（逐时 PE 计算）
- pe_adaptive_loss: 0

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_nodiff_pe_p6_l24_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_nodiff_pe_p6_l24_s42/
- 日志文件：assignment/week2/g3_nodiff_pe_p6_l24_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.0391 | 7.6533 | 30.14% | 15.3579 | 6.6513 | 13.7737 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 6.6513 | 9.0059 | 10.6116 | 11.7895 | 12.8265 | 13.7737 |

## 对比：扩散 vs 无扩散

| 指标 | PE-DiffWaveNet (exp1) | PE-Graph noDiff (exp2) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.0658 | 11.0391 | **-0.0267** ↓ |
| MAE | 7.6683 | 7.6533 | **-0.0150** ↓ |
| MAPE | 30.88% | 30.14% | **-0.74pp** ↓ |
| Peak RMSE | 13.9266 | 15.3579 | +1.4313 ↑ |
| Step1 RMSE | 6.6469 | 6.6513 | +0.0044 |
| Step6 RMSE | 13.8245 | 13.7737 | **-0.0508** ↓ |
| Best Epoch | 50 | 15 | -35 |

## 现象和结论

1. 关闭扩散模块后，整体 RMSE/MAE/MAPE 与完整 PE-DiffWaveNet 基本持平（RMSE 11.04 vs 11.07），说明 PE Graph + PE-FiLM 在无扩散条件下已能捕获主要的时空依赖关系。
2. 无扩散模型收敛更快（best epoch 15 vs 50），但 Peak RMSE 明显上升（15.36 vs 13.93），说明扩散模块在高浓度 O3 事件上的预测能力更强，扩散过程有助于细化峰值预测。
3. Per-step RMSE 从 6.65 单调递增至 13.77，与完整模型趋势一致，但 step4-6 的误差增长略缓。
4. 首次运行时遇到 `pe_step1_fix.py` 中 `TypeError: 'function' object is not iterable` 的瞬态错误（第二次 PE 构建时发生），清除 `__pycache__` 后重跑成功，疑为 numpy C 扩展内存状态残留。

## 问题

1. 首次运行 PE 第二次构建时出现瞬态 Python 对象类型错误（`sum(counts)` 中 `counts` 被错误解释为 function），清除 `__pycache__` 后消失，原因未完全定位。
2. training.log 中中文仍存在 UTF-16 编码导致的乱码问题，但不影响指标提取。
