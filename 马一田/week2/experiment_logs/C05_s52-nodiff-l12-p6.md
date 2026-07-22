# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C05
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-nodiff-l12-p6" \
  --pre_len 6 \
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
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 18)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l12-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l12-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C05_s52-nodiff-l12-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.22 | 7.75 | 30.62% | 14.93 | 14.11 |

## 现象和结论

递增权重重跑后 RMSE=11.22，比等权版本（11.16）略高 0.06（+0.5%），近步（Step1-3）RMSE 轻微上升，但 MAPE 从 32.66% 降至 30.62%，改善了 2 个百分点。早停仅 18 epoch，收敛偏快。Peak RMSE=14.93 显著升高（原 12.99），递增权重可能放大了峰值预测的误差。作为 no_diff + l=12 组合，RMSE 与同配置 full（C01, 11.43）接近，说明该配置下扩散贡献有限。

## 问题

Peak RMSE 异常升高（12.99→14.93），需关注递增权重对峰值样本的影响。
