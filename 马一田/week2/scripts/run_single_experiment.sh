#!/bin/bash
# ============================================================
# Week 2: 单组消融实验运行脚本
# 用法: bash run_single_experiment.sh <seed> <seq_len> <pre_len> <use_diffusion> <use_pe_graph> <use_pe_film> <exp_label>
# 示例: bash run_single_experiment.sh 52 12 6 1 1 1 "s52-full-l12-p6"
# ============================================================
set -euo pipefail

# ====== 参数 ======
SEED=${1:?missing seed}
SEQ_LEN=${2:?missing seq_len}
PRE_LEN=${3:?missing pre_len}
USE_DIFFUSION=${4:?missing use_diffusion}
USE_PE_GRAPH=${5:?missing use_pe_graph}
USE_PE_FILM=${6:?missing use_pe_film}
EXP_LABEL=${7:?missing exp_label}

# ====== 路径 ======
ROOT="d:/桌面/臭氧预测资料/臭氧预测资料"
PY=/c/Users/myt/AppData/Local/Python/bin/python.exe
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

# ====== 输出目录 ======
EXP_NAME="student_w2_${EXP_LABEL}"
OUTPUT_DIR="${ROOT}/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"

echo "=========================================="
echo "Week 2 Ablation Experiment"
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

# ====== 运行 ======
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
  --max_train_windows 0 \
  --max_valid_windows 0 \
  --max_test_windows 0

EXIT_CODE=$?

echo ""
echo "=========================================="
echo "Experiment ${EXP_LABEL} finished at $(date '+%Y-%m-%d %H:%M:%S')"
echo "Exit code: ${EXIT_CODE}"
echo "Output:    ${OUTPUT_DIR}"

if [ ${EXIT_CODE} -eq 0 ]; then
    echo "Status:    SUCCESS"
    # 打印关键指标
    METRICS_FILE="${OUTPUT_DIR}/metrics_summary.json"
    if [ -f "${METRICS_FILE}" ]; then
        echo "--- Metrics ---"
        $PY -c "import json; m=json.load(open('${METRICS_FILE}')); print(f'RMSE={m[\"test\"][\"rmse\"]:.4f}, MAE={m[\"test\"][\"mae\"]:.4f}, MAPE={m[\"test\"][\"mape\"]:.2f}%')"
    fi
else
    echo "Status:    FAILED"
fi
echo "=========================================="
