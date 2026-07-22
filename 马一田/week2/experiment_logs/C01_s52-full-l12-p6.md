# 实验记录

## 基本信息

- 组别：Person C
- 学生：马一田
- 日期：2026-07-13
- 实验编号：C01
- 模型：PE-DiffWaveNet noleak (full)
- 数据目录：`d:/桌面/臭氧预测资料/臭氧预测资料/`

## 运行命令

```bash
python -u d:/桌面/臭氧预测资料/臭氧预测资料/code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cuda \
  --exp_name "student_w2_s52-full-l12-p6" \
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
- seed: 52
- device: cuda (RTX 4050 Laptop)
- epochs: 120 (best at 38)
- batch_size: 16
- use_diffusion: 1
- use_pe_graph: 1
- use_pe_film: 1
- pe_adaptive_loss: 0
- horizon_weights: 1.0, 1.0, 1.1, 1.2, 1.35, 1.5（递增权重，唯一一组在发现 bug 前使用正确权重的实验）

## 输出位置

- 输出目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l12-p6/`
- 权重目录：`matrix_N95_PEDiffWaveNet_noleak_student_w2_s52-full-l12-p6/checkpoints/`
- 日志文件：`week2/results/person_C_seed52_full_nodiff/run_log_C01_s52-full-l12-p6.txt`

## 指标

| RMSE | MAE | MAPE | Peak RMSE | Last Step RMSE (Step6) |
| --- | --- | --- | --- | --- |
| 11.43 | 8.09 | 33.48% | 13.69 | 14.32 |

## 现象和结论

这是 Person C 的基准实验（seed=52, full 模型, l=12, p=6）。使用递增 horizon_weights（1.0→1.5），远端预测步的 loss 权重更大。RMSE=11.43，在 p=6 的四组 seed=52 实验中排名第 3。早停于 epoch 38，训练稳定。full 模型在该配置下略差于 no_diff（11.16），扩散模型在长预测步上可能引入额外噪声。Per-step RMSE 从 Step1=6.82 单调递增至 Step6=14.32，远步预测难度显著增加。

## 问题

无异常。训练过程顺利，无报错。
