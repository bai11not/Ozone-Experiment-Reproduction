#!/bin/bash
# ============================================================
# Week 2: 重跑 7 组 pre_len=6 实验（递增 horizon_weights）
# C03/C05/C07 (seed=52) + C09/C11/C13/C15 (seed=62)
# 每组独立日志，关机不影响已完成实验
# 用法: bash run_rerun_prelen6.sh
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/../results/rerun_prelen6"
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

TOTAL=7; CURRENT=0

run_exp() {
  local SEED=$1 SEQ_LEN=$2 PRE_LEN=$3 USE_DIFFUSION=$4 USE_PE_GRAPH=$5 USE_PE_FILM=$6 EXP_ID=$7 EXP_LABEL=$8

  CURRENT=$((CURRENT + 1))
  EXP_NAME="student_w2_${EXP_LABEL}"
  OUTPUT_DIR="${ROOT}/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"
  LOG_FILE="${RESULTS_DIR}/run_log_${EXP_ID}_${EXP_LABEL}.txt"

  {
    echo "=========================================="
    echo "[${CURRENT}/${TOTAL}] ${EXP_ID}: ${EXP_LABEL} (RERUN with horizon_weights)"
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
echo "Rerun pre_len=6 experiments with correct horizon_weights"
echo "7 experiments: C03/C05/C07 (seed=52) + C09/C11/C13/C15 (seed=62)"
echo "Log dir: ${RESULTS_DIR}"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

# ==================== seed=52 ====================

# C03: s52-full-l24-p6
run_exp 52 24 6 1 1 1 "C03" "s52-full-l24-p6"

# C05: s52-nodiff-l12-p6
run_exp 52 12 6 0 1 1 "C05" "s52-nodiff-l12-p6"

# C07: s52-nodiff-l24-p6
run_exp 52 24 6 0 1 1 "C07" "s52-nodiff-l24-p6"

# ==================== seed=62 ====================

# C09: s62-full-l12-p6
run_exp 62 12 6 1 1 1 "C09" "s62-full-l12-p6"

# C11: s62-full-l24-p6
run_exp 62 24 6 1 1 1 "C11" "s62-full-l24-p6"

# C13: s62-nodiff-l12-p6
run_exp 62 12 6 0 1 1 "C13" "s62-nodiff-l12-p6"

# C15: s62-nodiff-l24-p6
run_exp 62 24 6 0 1 1 "C15" "s62-nodiff-l24-p6"

echo ""
echo "============================================="
echo "All 7 reruns done!"
echo "Finished: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Logs: ${RESULTS_DIR}/"
echo "============================================="
