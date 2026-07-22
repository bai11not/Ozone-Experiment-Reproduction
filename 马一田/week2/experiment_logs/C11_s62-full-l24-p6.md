# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C11
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-full-l24-p6" \
  --pre_len 6 \
  --seq_len 24 \
  --seed 62 \
  --N_node 95 \
  --m 15 \
  --hidden_size 64 \
  --batch_size 16 \
  --eval_batch_size 16 \
  --lr 7e-4 \
  --epochs 120 \
  --patience 15 \
  --diff_steps 50 \
  --inference_steps 50 \
  --num_samples 3 \
  --eval_inference_steps 50 \
  --eval_num_samples 3 \
  --use_diffusion 1 \
  --use_pe_graph 1 \
  --use_pe_film 1 \
  --use_adaptive_adj 1 \
  --pe_source train \
  --pe_window_step 168 \
  --amp 1 \
  --save_predictions 1 \
  --log_interval 50 \
  --use_met_cache 1 \
  --max_train_windows 0 \
  --max_valid_windows 0 \
  --max_test_windows 0
```

## 关键配置

- seq_len: 24
- pre_len: 6
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 18)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l24-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l24-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C11_s62-full-l24-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.68 | 8.70 | 36.23% | 14.04 | 13.88 |

## 现象和结论

递增权重重跑后 RMSE=11.68，比等权版本（11.97）降低 0.29（-2.4%），MAPE 从 38.48% 降至 36.23%（-2.25pp）。远步 RMSE 同步改善：Step5 从 13.12→13.03，Step6 从 14.14→13.88。验证了递增权重对 seed=62 full 模型的正向作用。但 RMSE 仍显著高于同配置 seed=52（C03, 11.01），Δ=0.67，种子差异依然存在。训练 18 轮后早停，收敛偏快。

## 问题

与 C03（seed=52 同配置）的种子差异 ΔRMSE=0.67，full 模型在 seed=62 下表现系统性偏弱，值得进一步分析。
