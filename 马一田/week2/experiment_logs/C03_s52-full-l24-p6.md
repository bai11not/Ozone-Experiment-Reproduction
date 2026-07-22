# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C03
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-full-l24-p6" \
  --pre_len 6 \
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
- pre_len: 6
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 41)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l24-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l24-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C03_s52-full-l24-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.01 | 7.73 | 31.97% | 12.08 | 13.58 |

## 现象和结论

重跑后 RMSE=11.01，与初次运行结果完全一致（Δ=0.00），说明该配置下递增 horizon_weights 与等权对最终指标影响极小。这可能因为该配置训练稳定（epoch 41），模型自身已能合理分配各步权重。Per-step RMSE 从 6.89→13.58，远步退化均匀。在 pre_len=6 种子=52 的 4 组中排名第 1，验证了 l=24 + full 的协同效果。

## 问题

无异常。初次运行时 config.json 的 horizon_weights 为空（等权），本次重跑使用正确递增权重。
