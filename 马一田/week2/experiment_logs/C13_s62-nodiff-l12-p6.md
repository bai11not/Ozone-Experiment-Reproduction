# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C13
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-nodiff-l12-p6" \
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

- seq_len: 12
- pre_len: 6
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 32)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l12-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l12-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C13_s62-nodiff-l12-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.13 | 7.64 | 32.07% | 12.55 | 13.96 |

## 现象和结论

重跑后 RMSE=11.13，与等权版本（11.13）完全一致，和 C03 情况类似——递增权重对该配置影响极小。训练充分（epoch 32），MAPE=32.07% 在 pre_len=6 组中处于中等水平。Peak RMSE=12.55 为 pre_len=6 组中最优，说明 no_diff + l=12 组合在峰值预测上有优势。与同配置 seed=52（C05, 11.22）相比略优（-0.09），种子稳定性好。

## 问题

无异常。递增权重对该配置无显著影响。
