#!/usr/bin/env bash
# Experiment: g3_noPEgraph_p6_l12_s62 — PE-DiffWaveNet without PE Graph, seed=62
# Run on Windows native (torch_env conda), RTX 4070 8GB

export PYTHONIOENCODING="utf-8"
export PYTHONPATH="d:/生产实习_new/臭氧预测资料/code"
ROOT="d:/生产实习_new/臭氧预测资料"
EXP="g3_noPEgraph_p6_l12_s62"

python -u \
  "$ROOT/code/train_pediffwavenet_noleak.py" \
  --data_dir "$ROOT" \
  --device cuda \
  --exp_name "$EXP" \
  --pre_len 6 --seq_len 12 --seed 62 \
  --N_node 95 --m 15 \
  --hidden_size 64 --batch_size 16 \
  --lr 7e-4 --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 --num_samples 3 \
  --use_diffusion 1 --use_pe_graph 0 --use_pe_film 1 \
  --pe_window_step 1 \
  --save_predictions 1 --use_met_cache 1 --amp 1 \
  --log_interval 50 \
  2>&1 | tee "$ROOT/assignment/week2/$EXP/training.log"
