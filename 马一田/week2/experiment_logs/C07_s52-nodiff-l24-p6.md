# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-19（重跑）
- 实验编号：C07
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-nodiff-l24-p6" \
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
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 15)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，重跑修正）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l24-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l24-p6/checkpoints/`
- 日志文件：`week2/results/rerun_prelen6/run_log_C07_s52-nodiff-l24-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.05 | 7.97 | 33.58% | 13.66 | 13.50 |

## 现象和结论

递增权重重跑后 RMSE=11.05，比等权版本（10.88）升高 0.17（+1.6%），MAPE 从 32.06% 升至 33.58%。早停最早（epoch 15），是所有实验中收敛最快的。Step6 RMSE=13.50 与等权版本一致，说明递增权重在该配置下并未有效改善远步预测。MAE=7.97 为 pre_len=6 组中最差，模型对整体误差的控制能力下降。递增权重对 no_diff + l=24 组合产生了负面影响。

## 问题

MAPE 和 MAE 同步升高，递增权重似乎削弱了该配置的整体预测精度。早停过快（15 epoch），可能权重调整后需要更大的 patience。
