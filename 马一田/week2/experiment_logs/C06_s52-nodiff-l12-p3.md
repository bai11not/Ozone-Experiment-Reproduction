# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-13
- 实验编号：C06
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-nodiff-l12-p3" \
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
- pre_len: 3
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 19)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l12-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-nodiff-l12-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed52_full_nodiff/run_log_C06_s52-nodiff-l12-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 9.14 | 6.50 | 28.05% | 8.84 | 11.13 |

## 现象和结论

关闭扩散模型后（no_diff），p=3 短预测任务 RMSE=9.14，比同配置 full（C02, RMSE=8.80）差 0.34（+3.9%），说明在短预测步上扩散模型有正向贡献。这与 p=6 的结论相反——在长预测步上 no_diff 反而优于 full。早停最早（epoch 19），训练收敛快但泛化能力有限。Step3 RMSE=11.13 为本组最差，远端步退化明显。

## 问题

无异常。
