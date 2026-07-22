# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-13
- 实验编号：C08
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-nodiff-l24-p3" \
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
  --use_diffusion 0 \
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
- epochs: 120 (best at 26)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l24-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l24-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed52_full_nodiff/run_log_C08_s52-nodiff-l24-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 8.79 | 5.95 | 25.20% | 9.59 | 10.62 |

## 现象和结论

No_diff 模型在 l=24, p=3 下 RMSE=8.79，是 seed=52 中 p=3 组最优结果（与 C02/C04 的 8.80 基本持平）。MAE=5.95 为全部 16 组中最低之一。l=24 相比 l=12 no_diff（C06, RMSE=9.14）改善了 0.35，说明当关闭扩散后，更长的历史窗口对预测更有帮助。然而早停仅 26 epoch，模型可能欠充分训练。

## 问题

无异常。
