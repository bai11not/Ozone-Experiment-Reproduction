# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p3_l12_s62
- 模型：PE-DiffWaveNet (全组件: Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_noPEgraph_p3_l12_s62"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 3 --seq_len 12 --seed 62 `
  --N_node 95 --m 15 `
  --hidden_size 64 --batch_size 16 `
  --lr 7e-4 --epochs 120 --patience 15 `
  --diff_steps 50 --inference_steps 50 --num_samples 3 `
  --use_diffusion 1 --use_pe_graph 0 --use_pe_film 1 `
  --pe_window_step 1 `
  --horizon_weights "1.0,1.0,1.0" `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 12
- pre_len: 3
- seed: 62
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 46)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50 / inference_steps: 50 / num_samples: 3
- use_diffusion: 1
- use_pe_graph: **0** ← 消融变量
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.0]
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_noPEgraph_p3_l12_s62/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_noPEgraph_p3_l12_s62/
- 日志文件：assignment/week2/g3_noPEgraph_p3_l12_s62/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 8.7201 | 5.9289 | 24.14% | 9.3522 | 6.2127 | 10.5361 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 6.2127 | 8.8609 | 10.5361 |

## 对比：PE Graph 消融（seed=62, seq12, pre3）

| 指标 | PE Graph=1 (待补) | PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | — | 8.7201 | — |
| MAE | — | 5.9289 | — |
| MAPE | — | 24.14% | — |
| Peak RMSE | — | 9.3522 | — |

> 同种子主实验（g3_pedw_p3_l12_s62, PE Graph=1）由其他小组成员运行，完成后可填入对比。

## 跨种子参考（seed=42 主实验 vs seed=62 noPEgraph）

| 指标 | seed=42 PE Graph=1 (exp2) | seed=62 PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 9.1081 | 8.7201 | −0.39 |
| MAE | 6.5377 | 5.9289 | −0.61 |
| MAPE | 27.99% | 24.14% | −3.85pp |
| Peak RMSE | 9.0892 | 9.3522 | +0.26 |

> 注：种子不同，对比仅供参考。seed=62 的 RMSE 反而更优（−0.39），可能来自随机种子效应而非 PE Graph 的贡献。

## 现象和结论

1. seed=62 + no PE Graph + pre_len=3 获得 RMSE=8.72，表现良好。
2. 与 seed=42 主实验相比 RMSE 反而更低（8.72 vs 9.11），但这更可能来自种子差异而非 PE Graph 消融的正面效果——参考 pre_len=6 的同种子消融（PE Graph Δ=0.00）。
3. 等小组成员完成 seed=62 PE Graph=1 主实验后，可做严格受控对比。
