#!/bin/bash
# ============================================================
# Week 2: Person C 批量消融实验
# seed=52, full + no_diff, 共 8 组
# 使用 conda pytorch 环境 (GPU: RTX 4050 Laptop)
# 用法: bash run_person_C.sh
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
RESULTS_DIR="${SCRIPT_DIR}/../results/person_C_seed52_full_nodiff"
LOG_FILE="${RESULTS_DIR}/run_log_${TIMESTAMP}.txt"
mkdir -p "${RESULTS_DIR}"

# ====== 路径 ======
ROOT="d:/桌面/臭氧预测资料/臭氧预测资料"
PY="/d/anacoda/envs/pytorch/python.exe"
export PYTHONPATH="${ROOT}/code"

# ====== 固定参数 ======
N_NODE=95
M=15
HIDDEN_SIZE=64
BATCH_SIZE=16
LR=7e-4
EPOCHS=120
PATIENCE=15
DIFF_STEPS=50
INFERENCE_STEPS=50
NUM_SAMPLES=3
USE_ADAPTIVE_ADJ=1
PE_SOURCE="train"
AMP=1
PE_WINDOW_STEP=168
EVAL_INFERENCE_STEPS=50
EVAL_NUM_SAMPLES=3
SAVE_PREDICTIONS=1
LOG_INTERVAL=50
USE_MET_CACHE=1
MAX_WINDOWS=0

TOTAL=8
CURRENT=0

run_exp() {
  local SEED=$1
  local SEQ_LEN=$2
  local PRE_LEN=$3
  local USE_DIFFUSION=$4
  local USE_PE_GRAPH=$5
  local USE_PE_FILM=$6
  local EXP_LABEL=$7

  CURRENT=$((CURRENT + 1))
  EXP_NAME="student_w2_${EXP_LABEL}"
  OUTPUT_DIR="${ROOT}/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"

  echo ""
  {
    echo "=========================================="
    echo "[${CURRENT}/${TOTAL}] ${EXP_LABEL}"
    echo "=========================================="
    echo "Label:        ${EXP_LABEL}"
    echo "Seed:         ${SEED}"
    echo "Seq Len:      ${SEQ_LEN}"
    echo "Pre Len:      ${PRE_LEN}"
    echo "Diffusion:    ${USE_DIFFUSION}"
    echo "PE Graph:     ${USE_PE_GRAPH}"
    echo "PE FiLM:      ${USE_PE_FILM}"
    echo "Output:       ${OUTPUT_DIR}"
    echo "Start:        $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="

    $PY -u "${ROOT}/code/train_pediffwavenet_noleak.py" \
      --data_dir "${ROOT}" \
      --device cuda \
      --exp_name "${EXP_NAME}" \
      --pre_len ${PRE_LEN} \
      --seq_len ${SEQ_LEN} \
      --seed ${SEED} \
      --N_node ${N_NODE} \
      --m ${M} \
      --hidden_size ${HIDDEN_SIZE} \
      --batch_size ${BATCH_SIZE} \
      --eval_batch_size ${BATCH_SIZE} \
      --lr ${LR} \
      --epochs ${EPOCHS} \
      --patience ${PATIENCE} \
      --diff_steps ${DIFF_STEPS} \
      --inference_steps ${INFERENCE_STEPS} \
      --num_samples ${NUM_SAMPLES} \
      --eval_inference_steps ${EVAL_INFERENCE_STEPS} \
      --eval_num_samples ${EVAL_NUM_SAMPLES} \
      --use_diffusion ${USE_DIFFUSION} \
      --use_pe_graph ${USE_PE_GRAPH} \
      --use_pe_film ${USE_PE_FILM} \
      --use_adaptive_adj ${USE_ADAPTIVE_ADJ} \
      --pe_source ${PE_SOURCE} \
      --pe_window_step ${PE_WINDOW_STEP} \
      --amp ${AMP} \
      --save_predictions ${SAVE_PREDICTIONS} \
      --log_interval ${LOG_INTERVAL} \
      --use_met_cache ${USE_MET_CACHE} \
      --max_train_windows ${MAX_WINDOWS} \
      --max_valid_windows ${MAX_WINDOWS} \
      --max_test_windows ${MAX_WINDOWS}

    EXIT_CODE=$?

    echo ""
    echo "--- [${CURRENT}/${TOTAL}] ${EXP_LABEL} finished at $(date '+%Y-%m-%d %H:%M:%S') ---"
    echo "Exit code: ${EXIT_CODE}"

    if [ ${EXIT_CODE} -eq 0 ]; then
      echo "Status: SUCCESS"
      METRICS_FILE="${OUTPUT_DIR}/metrics_summary.json"
      if [ -f "${METRICS_FILE}" ]; then
        echo "--- Metrics ---"
        $PY -c "import json; m=json.load(open('${METRICS_FILE}')); print(f'RMSE={m[\"test_rmse\"]:.4f}, MAE={m[\"test_mae\"]:.4f}, MAPE={m[\"test_mape\"]:.2f}%')"
      fi
    else
      echo "Status: FAILED"
    fi
    echo ""
  } 2>&1 | tee -a "${LOG_FILE}"
}

# ==================== 8 组实验 ====================

echo "============================================="
echo "Week 2: Person C - Ablation Experiments"
echo "seed=52, full + no_diff, 共 8 组"
echo "GPU: RTX 4050 Laptop"
echo "Log: ${LOG_FILE}"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

# C01: full, l=12, p=6
run_exp 52 12 6 1 1 1 "s52-full-l12-p6"

# C02: full, l=12, p=3
run_exp 52 12 3 1 1 1 "s52-full-l12-p3"

# C03: full, l=24, p=6
run_exp 52 24 6 1 1 1 "s52-full-l24-p6"

# C04: full, l=24, p=3
run_exp 52 24 3 1 1 1 "s52-full-l24-p3"

# C05: no_diff, l=12, p=6
run_exp 52 12 6 0 1 1 "s52-nodiff-l12-p6"

# C06: no_diff, l=12, p=3
run_exp 52 12 3 0 1 1 "s52-nodiff-l12-p3"

# C07: no_diff, l=24, p=6
run_exp 52 24 6 0 1 1 "s52-nodiff-l24-p6"

# C08: no_diff, l=24, p=3
run_exp 52 24 3 0 1 1 "s52-nodiff-l24-p3"

echo ""
echo "============================================="
echo "Person C: All 8 experiments completed!"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Log: ${LOG_FILE}"
echo "============================================="
