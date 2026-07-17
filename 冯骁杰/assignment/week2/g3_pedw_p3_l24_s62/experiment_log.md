# 实验记录

## 基本信息

- 组别：3
- 学生：A
- 日期：2026-07-15
- 实验编号：g3_pedw_p3_l24_s62
- 模型：PE-DiffWaveNet (全组件: Diffusion + PE Graph + PE-FiLM)
- 数据目录：matrix_N95/

## 运行命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONPATH = "d:\生产实习_new\臭氧预测资料\code"
$ROOT = "d:\生产实习_new\臭氧预测资料"
$EXP = "g3_noPEgraph_p3_l24_s62"

& 'E:\Anaconda_envs\envs\torch_env\python.exe' -u `
  "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir $ROOT `
  --device cuda `
  --exp_name $EXP `
  --pre_len 3 --seq_len 24 --seed 62 `
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

- seq_len: 24
- pre_len: 3
- seed: 62
- device: cuda (RTX 4070 8GB)
- epochs: 120 (early stop @ 52)
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

- 输出目录：matrix_N95_PEDiffWaveNet_noleak_g3_noPEgraph_p3_l24_s62/
- 权重目录：weights_N95/weights_pediffwavenet_noleak_g3_noPEgraph_p3_l24_s62/
- 日志文件：assignment/week2/g3_noPEgraph_p3_l24_s62/training.log

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Step1 RMSE | Step3 RMSE |
| --- | --- | --- | --- | --- | --- |
| 8.7856 | 6.0620 | 24.95% | 9.4334 | 6.4858 | 10.5211 |

### Per-Step RMSE

| Step 1 | Step 2 | Step 3 |
| --- | --- | --- |
| 6.4858 | 8.8769 | 10.5211 |

## 对比：PE Graph 消融（seed=62, seq24, pre3）

| 指标 | PE Graph=1 (待补) | PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | — | 8.7856 | — |
| MAE | — | 6.0620 | — |
| MAPE | — | 24.95% | — |
| Peak RMSE | — | 9.4334 | — |

> 同种子主实验（g3_pedw_p3_l24_s62, PE Graph=1）由其他小组成员运行，完成后可填入对比。

## 跨种子参考

| 指标 | seed=42 PE Graph=1 (exp1) | seed=62 PE Graph=0 (本次) | Δ |
| --- | --- | --- | --- |
| RMSE | 8.6170 | 8.7856 | +0.17 |
| MAE | 5.8386 | 6.0620 | +0.22 |
| MAPE | 24.00% | 24.95% | +0.95pp |
| Peak RMSE | 9.8890 | 9.4334 | −0.46 |

> 注：种子不同，且 PE Graph 不同，Δ 来自双重差异之和。

## 现象和结论

1. seed=62 + no PE Graph + seq24 pre3 获得 RMSE=8.79，与 seed=42 主实验（8.62）差距 0.17，考虑到种子差异的量级（之前 pre6 实验中种子 Δ=0.05），无法判断这 0.17 来自种子还是 PE Graph 消融。
2. 等小组成员完成同种子主实验后可做受控对比。
3. 训练过程顺利，首次运行因 pandas 3.0.3 偶发兼容性问题失败、第二次因 GPU DLL 冲突失败，第三次成功。

## 问题

1. pandas 3.0.3 在 `df.apply(pd.to_numeric)` 时偶发 `'Series' object does not support the context manager protocol` 错误。
2. 连续启动 Python 进程时偶发 torch `shm.dll` DLL 初始化失败（WinError 1114），需间隔 10s 后重试。
