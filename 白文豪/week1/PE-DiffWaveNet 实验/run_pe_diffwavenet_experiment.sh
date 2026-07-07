#!/usr/bin/env bash
set -euo pipefail

ROOT="/mnt/d/时空数据/臭氧预测资料"
export PYTHONPATH="${ROOT}/code:${PYTHONPATH:-}"

echo "========================================"
echo "PE-DiffWaveNet 首次可复现实验"
echo "========================================"
echo "ROOT: ${ROOT}"
echo "PYTHONPATH: ${PYTHONPATH}"
echo ""

python3 -u "${ROOT}/code/train_pediffwavenet_noleak.py" \
  --data_dir "${ROOT}" \
  --device cuda \
  --exp_name student_smoke_gpu \
  --pre_len 6 \
  --seq_len 24 \
  --seed 42 \
  --N_node 95 \
  --m 15 \
  --hidden_size 16 \
  --batch_size 2 \
  --eval_batch_size 2 \
  --lr 7e-4 \
  --epochs 3 \
  --patience 1 \
  --diff_steps 3 \
  --inference_steps 2 \
  --num_samples 1 \
  --eval_inference_steps 2 \
  --eval_num_samples 1 \
  --use_diffusion 1 \
  --use_pe_graph 1 \
  --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 \
  --max_valid_windows 4 \
  --max_test_windows 4 \
  --save_predictions 1 \
  --save_train_arrays 0 \
  --use_met_cache 1 \
  --amp 1 \
  --log_interval 1

echo ""
echo "========================================"
echo "实验完成！检查输出目录："
echo "  结果目录: ${ROOT}/matrix_N95_PEDiffWaveNet_noleak_student_smoke_gpu"
echo "  权重目录: ${ROOT}/weights_N95/weights_pediffwavenet_noleak_student_smoke_gpu"
echo "========================================"