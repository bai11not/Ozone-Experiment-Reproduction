#!/bin/bash
# ============================================================
# Week 2 Person C: 所有运行命令汇总
# 环境: conda pytorch, GPU RTX 4050 Laptop (6GB)
# Python: /d/anacoda/envs/pytorch/python.exe
# PYTHONPATH: d:/桌面/臭氧预测资料/臭氧预测资料/code
# ============================================================

ROOT="d:/桌面/臭氧预测资料/臭氧预测资料"

# ============================================================
# seed=52 (C01-C08): 使用 run_person_C.sh 批量运行
# 日志目录: week2/results/person_C_seed52_full_nodiff/
# ============================================================

# --- C01: full, l=12, p=6 (唯一初次运行即使用正确 horizon_weights 的实验) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-full-l12-p6" \
  --pre_len 6 --seq_len 12 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C02: full, l=12, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-full-l12-p3" \
  --pre_len 3 --seq_len 12 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C03: full, l=24, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-full-l24-p6" \
  --pre_len 6 --seq_len 24 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C04: full, l=24, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-full-l24-p3" \
  --pre_len 3 --seq_len 24 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C05: no_diff, l=12, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-nodiff-l12-p6" \
  --pre_len 6 --seq_len 12 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C06: no_diff, l=12, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-nodiff-l12-p3" \
  --pre_len 3 --seq_len 12 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C07: no_diff, l=24, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-nodiff-l24-p6" \
  --pre_len 6 --seq_len 24 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C08: no_diff, l=24, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s52-nodiff-l24-p3" \
  --pre_len 3 --seq_len 24 --seed 52 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# ============================================================
# seed=62 (C09-C16): 使用 run_person_C_seed62.sh 批量运行
# 日志目录: week2/results/person_C_seed62_full_nodiff/
# ============================================================

# --- C09: full, l=12, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-full-l12-p6" \
  --pre_len 6 --seq_len 12 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C10: full, l=12, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-full-l12-p3" \
  --pre_len 3 --seq_len 12 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C11: full, l=24, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-full-l24-p6" \
  --pre_len 6 --seq_len 24 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C12: full, l=24, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-full-l24-p3" \
  --pre_len 3 --seq_len 24 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C13: no_diff, l=12, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-nodiff-l12-p6" \
  --pre_len 6 --seq_len 12 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C14: no_diff, l=12, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-nodiff-l12-p3" \
  --pre_len 3 --seq_len 12 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C15: no_diff, l=24, p=6 (重跑版 — 使用递增 horizon_weights) ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-nodiff-l24-p6" \
  --pre_len 6 --seq_len 24 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0

# --- C16: no_diff, l=24, p=3 ---
python -u ${ROOT}/code/train_pediffwavenet_noleak.py \
  --data_dir "${ROOT}" --device cuda \
  --exp_name "student_w2_s62-nodiff-l24-p3" \
  --pre_len 3 --seq_len 24 --seed 62 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 0 --use_pe_graph 1 --use_pe_film 1 \
  --use_adaptive_adj 1 --pe_source train --pe_window_step 168 \
  --amp 1 --save_predictions 1 --log_interval 50 \
  --use_met_cache 1 --max_train_windows 0 --max_valid_windows 0 --max_test_windows 0
