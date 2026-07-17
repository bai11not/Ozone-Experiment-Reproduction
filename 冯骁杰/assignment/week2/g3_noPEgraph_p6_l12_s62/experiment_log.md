# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_noPEgraph_p6_l12_s62
- 模型：PE-DiffWaveNet (Diffusion + PE-FiLM，无 PE Graph)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_noPEgraph_p6_l12_s62"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 6 --seq_len 12 --seed 62 `
  --N_node 95 --m 15 `
  --hidden_size 64 --batch_size 16 `
  --lr 7e-4 --epochs 120 --patience 15 `
  --diff_steps 50 --inference_steps 50 --num_samples 3 `
  --use_diffusion 1 --use_pe_graph 0 --use_pe_film 1 `
  --pe_window_step 1 `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 12
- pre_len: 6
- seed: **62** ← 变更
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 22)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: 1
- use_pe_graph: **0** ← 消融变量
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.1, 1.2, 1.35, 1.5]（默认）
- pe_adaptive_loss: 0
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_noPEgraph_p6_l12_s62/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_noPEgraph_p6_l12_s62/
- 日志文件：assignment/week2/g3_noPEgraph_p6_l12_s62/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.5357 | 8.2902 | 35.59% | 12.6472 | 7.1645 | 14.4262 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 7.1645 | 9.3897 | 10.9650 | 12.2740 | 13.4141 | 14.4262 |

## 对比：PE Graph 消融（seq=12, pre=6, diff=1）

| 指标 | PE Graph=1 (exp3, s42) | PE Graph=0 (本次, s62) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.5857 | 11.5357 | −0.05 |
| MAE | 8.3674 | 8.2902 | −0.08 |
| MAPE | 34.50% | 35.59% | **+1.09pp** |
| Peak RMSE | 12.7160 | 12.6472 | −0.07 |
| Best Epoch | 30 | 22 | −8 |

> 注：种子不同（42 vs 62），非严格受控对比。

## 现象和结论

1. 关闭 PE Graph 后，RMSE 和 Peak RMSE 几乎无变化（分别 −0.05 和 −0.07），说明 PE Graph 在 seq_len=12 的短序列场景下对整体预测精度的贡献有限。
2. MAPE 略有上升（+1.09pp），可能与不同种子引入的随机性有关，也可能是 PE Graph 的边缘贡献。
3. 无 PE Graph 模型收敛更快（best epoch 22 vs 30），训练效率更高。
4. 与之前的消融结论一致：PE Graph 和 Diffusion 模块对整体 RMSE 的影响均较小（< 3%），但对不同指标维度（MAPE、Peak RMSE）有差异化贡献。

## 问题

- 种子不同的对比不够严格，后续可在固定种子下重新验证 PE Graph 消融效果。
