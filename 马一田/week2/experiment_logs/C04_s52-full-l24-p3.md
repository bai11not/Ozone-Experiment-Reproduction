# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-13
- 实验编号：C04
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-full-l24-p3" \
  --pre_len 3 \
  --seq_len 24 \
  --seed 52 \
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
- pre_len: 3
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 35)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l24-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l24-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed52_full_nodiff/run_log_C04_s52-full-l24-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 8.80 | 6.14 | 26.21% | 8.85 | 10.60 |

## 现象和结论

Full 模型在 l=24, p=3 配置下 RMSE=8.80，与 l=12 版本（C02）完全相同，说明对于短预测（p=3），增大历史窗口没有带来额外收益。MAE=6.14 略高于 C02（6.00），MAPE 也略高（26.21% vs 24.89%）。早停于 epoch 35，比 C02（62）早得多，可能因更大输入导致更快过拟合。Peak RMSE=8.85 为 p=3 组最低之一，对峰值预测能力较好。

## 问题

无异常。
