# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_nodiff_pe_p3_l12_s42
- 模型：PE-Graph (no Diffusion) — PE Graph + PE-FiLM，无扩散模块
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_nodiff_pe_p3_l12_s42"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 3 --seq_len 12 --seed 42 `
  --N_node 95 --m 15 `
  --hidden_size 64 --batch_size 16 `
  --lr 7e-4 --epochs 120 --patience 15 `
  --diff_steps 50 --inference_steps 50 --num_samples 3 `
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --horizon_weights "1.0,1.0,1.0" `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 12
- pre_len: 3
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 13)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: **0** ← 消融变量
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.0]
- pe_adaptive_loss: 0
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_nodiff_pe_p3_l12_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_nodiff_pe_p3_l12_s42/
- 日志文件：assignment/week2/g3_nodiff_pe_p3_l12_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 9.1661 | 6.3666 | 26.84% | 10.8466 | 6.7057 | 11.0991 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 6.7057 | 9.1594 | 11.0991 |

## 消融对比：Diffusion vs noDiff（seq_len=12, pre_len=3）

| 指标 | PE-DiffWaveNet (exp2) | PE-Graph noDiff (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 9.1081 | 9.1661 | **+0.058** ↑ |
| MAE | 6.5377 | 6.3666 | −0.17 |
| MAPE | 27.99% | 26.84% | −1.15pp |
| Peak RMSE | 9.0892 | 10.8466 | **+1.76** ↑ |
| Best Epoch | 32 | 13 | −19 |

## 现象和结论

1. seq_len=12 + pre_len=3 下关闭扩散模块，RMSE 几乎不变（+0.06），MAE 甚至略优（−0.17），MAPE 也略有改善（−1.15pp），说明在短序列短预测场景下扩散模块的贡献非常有限。
2. Peak RMSE 在无扩散条件下恶化明显（9.09→10.85, +1.76），与之前的消融实验规律一致：扩散模块有助于峰值预测精度。
3. 无扩散模型收敛极快（best epoch 13 vs 32），说明模型更简单、更容易优化，但可能损失了对极端值的拟合能力。
4. 对比 exp4（seq24 pre3 noDiff, RMSE=8.81），seq_len=12 的 RMSE 为 9.17（+0.35），再次验证长历史窗口的重要性。

## 问题

- 无明显问题。训练顺利，无梯度异常警告。
