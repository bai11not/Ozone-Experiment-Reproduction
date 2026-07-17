# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p6_l12_s62
- 模型：PE-DiffWaveNet (全组件: Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_pedw_p6_l12_s62"

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
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 `
  --pe_window_step 1 `
  --save_predictions 1 --use_met_cache 1 --amp 1 `
  --log_interval 50 `
  2>&1 | Tee-Object -FilePath "$ROOT\assignment\week2\$EXP\training.log"
```

## 关键配置

- seq_len: 12
- pre_len: 6
- seed: **62** ← 本次实验
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 22)
- batch_size: 16
- hidden_size: 64
- diff_steps: 50 / inference_steps: 50 / num_samples: 3
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_window_step: 1
- horizon_weights: [1.0, 1.0, 1.1, 1.2, 1.35, 1.5]（默认）
- PE 特征：从缓存加载

## 输出位置

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_pedw_p6_l12_s62/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_pedw_p6_l12_s62/
- 日志文件：assignment/week2/g3_pedw_p6_l12_s62/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step6 RMSE |
| --- | --- | --- | --- | --- | --- |
| 11.5357 | 8.2902 | 35.59% | 12.6472 | 7.1645 | 14.4262 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
| --- | --- | --- | --- | --- | --- |
| 7.1645 | 9.3897 | 10.9650 | 12.2740 | 13.4141 | 14.4262 |

## 同种子受控对比：PE Graph 消融（seed=62）

| 指标 | PE Graph=1 (本次) | PE Graph=0 (noPEgraph) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.5357 | 11.5357 | **0.0000** |
| MAE | 8.2902 | 8.2902 | 0.0000 |
| MAPE | 35.59% | 35.59% | 0.00pp |
| Peak RMSE | 12.6472 | 12.6472 | 0.0000 |
| Best Epoch | 22 | 22 | 0 |

## 现象和结论

1. **PE Graph 开启与关闭在同种子下结果完全一致**（小数点后 7 位相同），这是本次实验最重要的发现。说明在 seq_len=12、pre_len=6 配置下，PE Graph 对模型输出无任何影响。
2. 可能原因：
   - PE Graph 构造的邻接矩阵与已有的 S（空间距离）+ T（时间相关）邻接矩阵高度冗余；
   - PE-FiLM 已经通过特征调制将 PE 信息注入各层，PE Graph 作为额外的图结构连接未能提供增量信息；
   - 模型可能学会忽略 PE Graph 的弱连接（阈值=0.9，仅保留高相似度边）。
3. 结合之前的 diffusion 消融（整体 RMSE 影响 < 3%），PE Graph 是三个 PE 组件中对最终指标影响最小的模块。

## 与 seed=42 对比：随机种子效应

| 指标 | seed=42 (exp3) | seed=62 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 11.5857 | 11.5357 | −0.05 |
| MAPE | 34.50% | 35.59% | +1.09pp |
| Peak RMSE | 12.7160 | 12.6472 | −0.07 |
| Best Epoch | 30 | 22 | −8 |

种子变化引入的差异（RMSE Δ=0.05）与 PE Graph 开关的差异（Δ=0.00）量级不同，说明随机性 > PE Graph 贡献。

## 问题

- PE Graph=0 与 PE Graph=1 结果完全一致，需进一步验证是否 PE Graph 邻接矩阵的构造参数（pe_threshold=0.9）过于苛刻导致有效边太少。
