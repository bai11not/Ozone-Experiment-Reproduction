# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p6_l24_s62
- 模型：PE-DiffWaveNet (全组件: Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_noPEgraph_p6_l24_s62"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 6 --seq_len 24 --seed 62 `
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

- seq_len: 24
- pre_len: 6
- seed: 62
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 15)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50 / inference_steps: 50 / num_samples: 3
- use_diffusion: 1
- use_pe_graph: **0** ← 消融变量
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.1, 1.2, 1.35, 1.5]（默认）
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_noPEgraph_p6_l24_s62/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_noPEgraph_p6_l24_s62/
- 日志文件：assignment/week2/g3_noPEgraph_p6_l24_s62/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.8211 | 8.4736 | 33.77% | 13.9880 | 8.1810 | 14.2306 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 8.1810 | 10.1420 | 11.3190 | 12.5702 | 13.4165 | 14.2306 |

## 对比：PE Graph 消融（seed=62, seq24, pre6）

| 指标 | PE Graph=1 (待补) | PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | — | 11.8211 | — |
| Peak RMSE | — | 13.9880 | — |

> 同种子主实验（g3_pedw_p6_l24_s62, PE Graph=1）由其他小组成员运行，完成后可填入对比。

## 跨种子参考

| 指标 | seed=42 PE Graph=1 (基准) | seed=62 PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.0658 | 11.8211 | +0.76 |
| MAE | 7.6683 | 8.4736 | +0.81 |
| MAPE | 30.88% | 33.77% | +2.89pp |
| Peak RMSE | 13.9266 | 13.9880 | +0.06 |

> 注：种子不同（42 vs 62），PE Graph 不同（1 vs 0），Δ 来自双重差异。

## 现象和结论

1. seed=62 + no PE Graph + 完整 seq/pre 获得 RMSE=11.82，与 seed=42 基准（11.07）差距 0.76。但此差异主要由种子变化引起还是 PE Graph 消融引起，需同种子主实验确认。
2. 收敛极快（best epoch 15），与之前无扩散消融的收敛加速现象类似。
3. Step1 RMSE（8.18）相比基准（6.65）明显恶化，但同样无法解耦种子和 PE Graph 的影响。
4. 等小组成员完成同种子主实验后可做严格消融对比。
