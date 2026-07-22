# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-15
- 实验编号：C14
- 模型：PE-DiffWaveNet noleak (no_diff)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-nodiff-l12-p3" \
  --pre_len 3 \
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
- pre_len: 3
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 31)
- batch_size: 16
- use_diffusion: 0
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l12-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-nodiff-l12-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed62_full_nodiff/run_log_C14_s62-nodiff-l12-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 8.83 | 5.98 | 25.23% | 9.71 | 10.81 |

## 现象和结论

No_diff 模型 seed=62 在 l=12, p=3 下 RMSE=8.83，比同配置 full（C10, RMSE=8.72）差 0.11（+1.3%），与 seed=52 的 full vs no_diff 对比结论一致——在 p=3 短预测上扩散模型有轻微正向贡献。早停于 epoch 31，收敛速度快但最终指标略逊。与 seed=52 同配置（C06, RMSE=9.14）相比改善了 0.31，seed=62 在该配置下表现更好。

## 问题

无异常。
