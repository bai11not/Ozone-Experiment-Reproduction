# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C09
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-full-l12-p6" \
  --pre_len 6 \
  --seq_len 12 \
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

- seq_len: 12
- pre_len: 6
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 15)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l12-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l12-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C09_s62-full-l12-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 12.37 | 9.24 | 40.24% | 13.11 | 15.20 |

## 现象和结论

⚠️ **重大改善**。递增权重重跑后 RMSE=12.37，比等权版本（13.93）大幅降低 1.56（-11.2%），MAPE 从 50.15% 降至 40.24%。初次运行时该配置仅训练 13 轮就 early stop（异常），重跑后训练 15 轮，虽然仍较早停，但指标已回归正常范围。Step6 RMSE 从 16.34 降至 15.20（-1.14），递增权重对远步预测的改善最为显著。但 RMSE=12.37 在 pre_len=6 组中仍是最差，说明 seed=62 + full + l=12 + p=6 是一个内在不稳定的配置组合。

## 问题

初次运行 early stop 于 epoch 13（RMSE=13.93），可能是等权 loss 导致优化方向不佳。重跑虽改善至 12.37，但仍为全部 16 组最差，建议该配置增加 patience 或使用更低学习率进一步尝试。
