# 实验记录

## 基本信息

- 组别：3
- 学生：
- 日期：2026-07-14
- 实验编号：g3_pedw_p6_l24_s42
- 模型：PE-DiffWaveNet (Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_pedw_p6_l24_s42"

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
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 `
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
- epochs: 120 (early stop @ 50)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50
- inference_steps: 50
- num_samples: 3
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1 (逐时 PE 计算)
- pe_adaptive_loss: 0

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p6_l24_s42/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_pedw_p6_l24_s42/
- 日志文件：assignment/week2/g3_pedw_p6_l24_s42/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.0658 | 7.6683 | 30.88% | 13.9266 | 6.6469 | 13.8245 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 6.6469 | 9.0763 | 10.6717 | 11.7926 | 12.8095 | 13.8245 |

## 现象和结论

1. 本次实验为 PE-DiffWaveNet 主模型标准配置（pre_len=6, seq_len=24, seed=42），使用 pe_window_step=1 进行逐时 PE 计算，相比默认 step=168 提供了更密集的排列熵特征。
2. 训练在 epoch 50 触发 early stop（patience=15），best valid RMSE=12.1143。Test RMSE=11.0658 落在预期范围 [10.5, 12.0] 内，与论文 Table1 中 MTGNN 最佳 baseline (10.6620) 接近。
3. Per-step RMSE 从 6.65 (step1) 单调递增至 13.82 (step6)，符合预测步长越长误差越大的预期规律。
4. Peak RMSE=13.93 高于整体 RMSE，说明模型在高 O3 浓度区间的预测误差更大，符合臭氧预测的典型特征。

## 问题

1. WSL (Linux) 环境下 Python 3.11 + numpy 2.4.6 存在 C 扩展层 segfault，step=1 的 PE 密集计算在 WSL 下无法完成。最终切换到 Windows 原生 conda 环境 (torch_env) 解决。
2. geographiclib 2.0/2.1 在 WSL Python 3.11 下均有兼容性问题，已在 train_atgcn_pe3.py 中替换为纯 Python Haversine 实现。
3. pe_step1_fix.py 为新增文件，使用滑动直方图算法替代原始逐窗 PE 计算，将复杂度从 O(W·N) 降至 O(N)，避免内循环中创建 numpy 数组。
