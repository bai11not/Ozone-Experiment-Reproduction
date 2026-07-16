#!/bin/bash
# ============================================================
# Week 2: Person C seed=62 批量消融实验 (C09-C16)
# seed=62, full + no_diff, 共 8 组
# 每组独立日志，关机不影响已完成实验
# 用法: bash run_person_C_seed62.sh
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/../results/person_C_seed62_full_nodiff"
mkdir -p "${RESULTS_DIR}"

ROOT="d:/桌面/臭氧预测资料/臭氧预测资料"
PY="/d/anacoda/envs/pytorch/python.exe"
export PYTHONPATH="${ROOT}/code"

# 固定参数
N_NODE=95; M=15; HIDDEN_SIZE=64; BATCH_SIZE=16; LR=7e-4
EPOCHS=120; PATIENCE=15; DIFF_STEPS=50; INFERENCE_STEPS=50; NUM_SAMPLES=3
USE_ADAPTIVE_ADJ=1; PE_SOURCE="train"; AMP=1; PE_WINDOW_STEP=168
EVAL_INFERENCE_STEPS=50; EVAL_NUM_SAMPLES=3; SAVE_PREDICTIONS=1
LOG_INTERVAL=50; USE_MET_CACHE=1; MAX_WINDOWS=0

SEED=62
TOTAL=8; CURRENT=0

run_exp() {
  local SEQ_LEN=$1 PRE_LEN=$2 USE_DIFFUSION=$3 USE_PE_GRAPH=$4 USE_PE_FILM=$5 EXP_ID=$6 EXP_LABEL=$7

  CURRENT=$((CURRENT + 1))
  EXP_NAME="student_w2_${EXP_LABEL}"
  OUTPUT_DIR="${ROOT}/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"
  LOG_FILE="${RESULTS_DIR}/run_log_${EXP_ID}_${EXP_LABEL}.txt"

  {
    echo "=========================================="
    echo "[${CURRENT}/${TOTAL}] ${EXP_ID}: ${EXP_LABEL}"
    echo "=========================================="
    echo "Seed: ${SEED} | Seq: ${SEQ_LEN} | Pre: ${PRE_LEN}"
    echo "Diff: ${USE_DIFFUSION} | PE Graph: ${USE_PE_GRAPH} | PE FiLM: ${USE_PE_FILM}"
    echo "Output: ${OUTPUT_DIR}"
    echo "Log:    ${LOG_FILE}"
    echo "Start:  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="

    $PY -u "${ROOT}/code/train_pediffwavenet_noleak.py" \
      --data_dir "${ROOT}" --device cuda --exp_name "${EXP_NAME}" \
      --pre_len ${PRE_LEN} --seq_len ${SEQ_LEN} --seed ${SEED} \
      --N_node ${N_NODE} --m ${M} --hidden_size ${HIDDEN_SIZE} \
      --batch_size ${BATCH_SIZE} --eval_batch_size ${BATCH_SIZE} \
      --lr ${LR} --epochs ${EPOCHS} --patience ${PATIENCE} \
      --diff_steps ${DIFF_STEPS} --inference_steps ${INFERENCE_STEPS} \
      --num_samples ${NUM_SAMPLES} \
      --eval_inference_steps ${EVAL_INFERENCE_STEPS} --eval_num_samples ${EVAL_NUM_SAMPLES} \
      --use_diffusion ${USE_DIFFUSION} --use_pe_graph ${USE_PE_GRAPH} --use_pe_film ${USE_PE_FILM} \
      --use_adaptive_adj ${USE_ADAPTIVE_ADJ} --pe_source ${PE_SOURCE} \
      --pe_window_step ${PE_WINDOW_STEP} --amp ${AMP} \
      --save_predictions ${SAVE_PREDICTIONS} --log_interval ${LOG_INTERVAL} \
      --use_met_cache ${USE_MET_CACHE} \
      --max_train_windows ${MAX_WINDOWS} --max_valid_windows ${MAX_WINDOWS} --max_test_windows ${MAX_WINDOWS}

    EXIT_CODE=$?
    echo ""
    echo "--- ${EXP_ID} ${EXP_LABEL} finished at $(date '+%Y-%m-%d %H:%M:%S') | Exit: ${EXIT_CODE} ---"
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
  } 2>&1 | tee "${LOG_FILE}"
}

echo "============================================="
echo "Person C seed=62 — C09-C16"
echo "Log dir: ${RESULTS_DIR}"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

# C09: full, l=12, p=6
run_exp 12 6 1 1 1 "C09" "s62-full-l12-p6"

# C10: full, l=12, p=3
run_exp 12 3 1 1 1 "C10" "s62-full-l12-p3"

# C11: full, l=24, p=6
run_exp 24 6 1 1 1 "C11" "s62-full-l24-p6"

# C12: full, l=24, p=3
run_exp 24 3 1 1 1 "C12" "s62-full-l24-p3"

# C13: no_diff, l=12, p=6
run_exp 12 6 0 1 1 "C13" "s62-nodiff-l12-p6"

# C14: no_diff, l=12, p=3
run_exp 12 3 0 1 1 "C14" "s62-nodiff-l12-p3"

# C15: no_diff, l=24, p=6
run_exp 24 6 0 1 1 "C15" "s62-nodiff-l24-p6"

# C16: no_diff, l=24, p=3
run_exp 24 3 0 1 1 "C16" "s62-nodiff-l24-p3"

echo ""
echo "============================================="
echo "Person C seed=62: C09-C16 all done!"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Logs: ${RESULTS_DIR}/"
echo "============================================="
