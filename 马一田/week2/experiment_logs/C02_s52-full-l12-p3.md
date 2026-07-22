# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-13
- 实验编号：C02
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-full-l12-p3" \
  --pre_len 3 \
  --seq_len 12 \
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

- seq_len: 12
- pre_len: 3
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 62)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l12-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l12-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed52_full_nodiff/run_log_C02_s52-full-l12-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 8.80 | 6.00 | 24.89% | 9.18 | 10.67 |

## 现象和结论

Full 模型在 p=3 短预测窗口下表现优异，RMSE=8.80，比同配置 p=6（C01, RMSE=11.43）降低 2.63。预训练最充分（epoch 62），说明短预测任务允许更多有效训练轮次。Per-step RMSE 从 6.30（Step1）增至 10.67（Step3）。在 seed=52 的 p=3 组中与 C04（l=24）持平（RMSE 同为 8.80），说明对于短预测，历史窗口从 12 扩至 24 无明显增益。

## 问题

首次运行时因 horizon_weights 长度不匹配报错（pre_len=3 无法使用默认的 6 个权重值），修改默认值为空后重新运行成功。
