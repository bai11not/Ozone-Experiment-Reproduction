# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p3_l12_s42
- 模型：PE-DiffWaveNet (Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_pedw_p3_l12_s42"

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
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --horizon_weights "1.0,1.0,1.0" `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: **12** ← 本次实验变更
- pre_len: **3** ← 本次实验变更
- seed: 42
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 32)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.0]（pre_len=3，均匀权重）
- pe_adaptive_loss: 0
- PE 特征：从 exp1 缓存加载（跳过重复计算）

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p3_l12_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_pedw_p3_l12_s42/
- 日志文件：assignment/week2/g3_pedw_p3_l12_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 9.1081 | 6.5377 | 27.99% | 9.0892 | 7.2571 | 10.6671 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 7.2571 | 9.0786 | 10.6671 |

## 对比：seq_len=12 vs seq_len=24（pre_len=3 固定）

| 指标 | seq_len=24 (exp1) | seq_len=12 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 8.6170 | 9.1081 | **+0.49** ↑ |
| MAE | 5.8386 | 6.5377 | **+0.70** ↑ |
| MAPE | 24.00% | 27.99% | **+3.99pp** ↑ |
| Peak RMSE | 9.8890 | 9.0892 | **−0.80** ↓ |
| Step1 RMSE | 6.3280 | 7.2571 | +0.93 |

## 现象和结论

1. 将 seq_len 从 24 降至 12 后，整体预测精度下降：RMSE +0.49、MAPE +3.99pp，说明更短的历史窗口丢失了重要的时间依赖信息。
2. 然而 Peak RMSE 却略有改善（9.09 vs 9.89），可能是因为短序列使模型更关注近期变化，对高浓度峰值的时间定位更准确。
3. 收敛速度加快：best epoch 从 52 降至 32，短序列的训练效率更高。
4. 三步预测均表现出 RMSE 随步长递增的规律（7.26→9.08→10.67），与理论预期一致。

## 问题

1. PE 计算在 seq_len=12 配置下反复出现 Python 对象类型损坏的瞬态错误，最终通过 PE 缓存策略（从 exp1 复用预计算文件）绕过。
2. horizon_weights 使用均匀权重 `[1.0, 1.0, 1.0]`，与基准实验的递增权重不完全可比。
