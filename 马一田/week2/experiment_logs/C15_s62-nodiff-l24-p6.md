# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C15
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-nodiff-l24-p6" \
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
- pre_len: 6
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 20)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l24-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l24-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C15_s62-nodiff-l24-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 10.68 | 7.44 | 30.04% | 13.43 | 13.12 |

## 现象和结论

🏆 **pre_len=6 全局最佳**。递增权重重跑后 RMSE=10.68，比等权版本（10.90）降低 0.22（-2.0%），MAPE 从 29.67% 微升至 30.04%。Step6 RMSE=13.12 为全部 p=6 实验中最低，递增权重对远步改善效果明确（旧 Step6=13.52，Δ=-0.40）。该配置为 no_diff + l=24，无需扩散模型即可达到最优，再次印证扩散在长预测步上可能引入噪声。与 seed=52 同配置（C07, 11.05）相比优 0.37，seed=62 在该配置下表现更好。

## 问题

无异常。该配置表现优异，建议作为 pre_len=6 的推荐基线。
