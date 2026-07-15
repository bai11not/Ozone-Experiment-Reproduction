#!/bin/bash
cd /mnt/d/生产实习_new/臭氧预测资料
export PYTHONPATH="${PWD}/code:${PYTHONPATH}"

python -u code/train_pediffwavenet_noleak.py \
  --data_dir . \
  --device cuda \
  --exp_name g3_pedw_p6_l24_s42 \
  --pre_len 6 \
  --seq_len 24 \
  --seed 42 \
  --N_node 95 \
  --m 15 \
  --hidden_size 64 \
  --batch_size 16 \
  --eval_batch_size 16 \
  --lr 7e-4 \
  --lr_min 1e-5 \
  --epochs 120 \
  --patience 15 \
  --min_delta 0.001 \
  --diff_steps 50 \
  --inference_steps 50 \
  --num_samples 3 \
  --t_start_ratio 0.25 \
  --eval_inference_steps 0 \
  --eval_num_samples 0 \
  --use_diffusion 1 \
  --use_pe_graph 1 \
  --use_pe_film 1 \
  --use_adaptive_adj 1 \
  --pe_source train \
  --pe_scales 6,9,12,24,48,72 \
  --pe_dim 3 \
  --pe_delay 1 \
  --pe_window_step 1 \
  --pe_threshold 0.9 \
  --pe_sigma 0.1 \
  --save_predictions 1 \
  --save_train_arrays 0 \
  --use_met_cache 1 \
  --amp 1 \
  --grad_clip 1.0 \
  --weight_decay 1e-4 \
  --log_interval 50
