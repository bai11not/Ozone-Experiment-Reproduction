# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_nodiff_pe_p3_l24_s42
- 模型：PE-Graph (no Diffusion) — PE Graph + PE-FiLM，无扩散模块
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_nodiff_pe_p3_l24_s42"

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
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --horizon_weights "1.0,1.0,1.0" `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 24
- pre_len: 3
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 44)
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

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_nodiff_pe_p3_l24_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_nodiff_pe_p3_l24_s42/
- 日志文件：assignment/week2/g3_nodiff_pe_p3_l24_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 8.8114 | 5.9033 | 25.26% | 9.8056 | 6.3289 | 10.6172 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 6.3289 | 8.9523 | 10.6172 |

## 消融对比：Diffusion vs noDiff（seq_len=24, pre_len=3）

| 指标 | PE-DiffWaveNet (exp1) | PE-Graph noDiff (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 8.6170 | 8.8114 | **+0.19** ↑ |
| MAE | 5.8386 | 5.9033 | +0.06 |
| MAPE | 24.00% | 25.26% | +1.26pp |
| Peak RMSE | 9.8890 | 9.8056 | −0.08 |
| Best Epoch | 52 | 44 | −8 |

## 现象和结论

1. 关闭扩散模块后，RMSE 仅微增 0.19（8.62→8.81），MAPE +1.26pp，与第一次消融实验（pre_len=6 时 RMSE 甚至略优）的趋势一致：PE Graph + PE-FiLM 已能捕获主要的时空依赖关系。
2. Peak RMSE 在无扩散条件下持平（9.81 vs 9.89），与 pre_len=6 消融实验（peak RMSE 大幅恶化从 13.93 到 15.36）形成对比，说明在短预测步长下扩散模块对峰值的贡献较小。
3. 无扩散模型收敛更快（best epoch 44 vs 52）。
4. 首次运行时因进程超时退出（epoch 48 中断），重跑后正常完成。

## 问题

1. 首次运行在 epoch 48 被 Windows exit code 5 (ACCESS_DENIED) 中断，原因可能是 GPU 资源争用或系统文件锁，重跑后顺利通过。
2. 训练过程中频繁出现 `[WARN] skip non-finite grad` 警告，表明无扩散模型的梯度稳定性略差于扩散版本。
