# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-15
- 实验编号：C12
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s62-full-l24-p3" \
  --pre_len 3 \
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
- pre_len: 3
- seed: 62
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 53)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: ""（空 = 3 步等权，符合 pre_len=3 的实验设计）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l24-p3/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s62-full-l24-p3/checkpoints/`
- 日志文件：`week2/results/person_C_seed62_full_nodiff/run_log_C12_s62-full-l12-p3.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step3) |
| --- | --- | --- | --- | --- |
| 8.56 | 5.79 | 23.90% | 9.32 | 10.24 |

## 现象和结论

🏆 **全局最佳**。Full 模型 seed=62, l=24, p=3 下 RMSE=8.56，为全部 16 组实验最低。MAE=5.79、MAPE=23.90% 同样为全局最优。充分训练至 epoch 53，长历史窗口（l=24）+ 扩散模型在短预测步（p=3）配置下发挥了最佳协同效果。Per-step RMSE（6.24→8.70→10.24）各步均为所有实验中最低。与 seed=52 同配置（C04, RMSE=8.80）差异 0.24，种子稳定性良好。

## 问题

无异常。
