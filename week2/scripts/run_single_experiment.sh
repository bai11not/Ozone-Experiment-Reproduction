#!/usr/bin/env bash
# run_single_experiment.sh
# 运行单组 PE-DiffWaveNet 实验
#
# 用法:
#   bash run_single_experiment.sh 42 12 6 0 0 0 "A01_s42-d0-l12-p6-g0-f0"
#
# 参数顺序: seed seq_len pre_len use_diffusion use_pe_graph use_pe_film exp_name

set -euo pipefail

SEED="${1:?缺少 seed}"
SEQ_LEN="${2:?缺少 seq_len}"
PRE_LEN="${3:?缺少 pre_len}"
USE_DIFFUSION="${4:?缺少 use_diffusion}"
USE_PE_GRAPH="${5:?缺少 use_pe_graph}"
USE_PE_FILM="${6:?缺少 use_pe_film}"
EXP_NAME="${7:?缺少 exp_name}"

# ========== 路径配置（按需修改） ==========
DATA_DIR="d:/时空数据/臭氧预测资料"
DEVICE="${DEVICE:-cuda}"
PYTHON_BIN="${PYTHON_BIN:-python}"

# ========== 固定参数 ==========
N_NODE=95
INPUT_DIM=15
HIDDEN_SIZE=64
BATCH_SIZE=16
EVAL_BATCH_SIZE=16
LR="7e-4"
LR_MIN="1e-5"
EPOCHS=120
PATIENCE=15
MIN_DELTA="0.001"
DIFF_STEPS=50
INFERENCE_STEPS=50
NUM_SAMPLES=3
T_START_RATIO="0.25"
COARSE_WEIGHT="0.08"
USE_ADAPTIVE_ADJ=1
PE_SOURCE="train"
PE_SCALES="6,9,12,24,48,72"
PE_DIM=3
PE_DELAY=1
PE_WINDOW_STEP=1
PE_GRAPH_ALPHA="1.0"
PE_FILM_SCALE="1.0"
PE_FILM_ZERO_INIT=0
NORMALIZE_PE_FEATURES=1
AMP=1
GRAD_CLIP="1.0"
WEIGHT_DECAY="1e-4"
LOG_INTERVAL=50
SAVE_PREDICTIONS=1
USE_MET_CACHE=1

# 自动生成 horizon_weights
HORIZON_WEIGHTS="1.0"
for ((i = 2; i <= PRE_LEN; i++)); do
  HORIZON_WEIGHTS="${HORIZON_WEIGHTS},1.0"
done

export PYTHONPATH="${DATA_DIR}/code:${PYTHONPATH:-}"

echo "========================================"
echo " PE-DiffWaveNet 单次实验"
echo "========================================"
echo "  实验名称:     ${EXP_NAME}"
echo "  Seed:         ${SEED}"
echo "  Seq Len:      ${SEQ_LEN}"
echo "  Pre Len:      ${PRE_LEN}"
echo "  UseDiffusion: ${USE_DIFFUSION}"
echo "  UsePEGraph:   ${USE_PE_GRAPH}"
echo "  UsePEFiLM:    ${USE_PE_FILM}"
echo "  Device:       ${DEVICE}"
echo "========================================"
echo ""

START_TIME=$(date +%s)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始训练..."

$PYTHON_BIN -u "${DATA_DIR}/code/train_pediffwavenet_noleak.py" \
  --data_dir "${DATA_DIR}" \
  --device "${DEVICE}" \
  --exp_name "${EXP_NAME}" \
  --seed "${SEED}" \
  --seq_len "${SEQ_LEN}" \
  --pre_len "${PRE_LEN}" \
  --use_diffusion "${USE_DIFFUSION}" \
  --use_pe_graph "${USE_PE_GRAPH}" \
  --use_pe_film "${USE_PE_FILM}" \
  --N_node "${N_NODE}" \
  --m "${INPUT_DIM}" \
  --hidden_size "${HIDDEN_SIZE}" \
  --batch_size "${BATCH_SIZE}" \
  --eval_batch_size "${EVAL_BATCH_SIZE}" \
  --lr "${LR}" \
  --lr_min "${LR_MIN}" \
  --epochs "${EPOCHS}" \
  --patience "${PATIENCE}" \
  --min_delta "${MIN_DELTA}" \
  --diff_steps "${DIFF_STEPS}" \
  --inference_steps "${INFERENCE_STEPS}" \
  --num_samples "${NUM_SAMPLES}" \
  --t_start_ratio "${T_START_RATIO}" \
  --coarse_weight "${COARSE_WEIGHT}" \
  --horizon_weights "${HORIZON_WEIGHTS}" \
  --use_adaptive_adj "${USE_ADAPTIVE_ADJ}" \
  --pe_source "${PE_SOURCE}" \
  --pe_scales "${PE_SCALES}" \
  --pe_dim "${PE_DIM}" \
  --pe_delay "${PE_DELAY}" \
  --pe_window_step "${PE_WINDOW_STEP}" \
  --pe_graph_alpha "${PE_GRAPH_ALPHA}" \
  --pe_film_scale "${PE_FILM_SCALE}" \
  --pe_film_zero_init "${PE_FILM_ZERO_INIT}" \
  --normalize_pe_features "${NORMALIZE_PE_FEATURES}" \
  --amp "${AMP}" \
  --grad_clip "${GRAD_CLIP}" \
  --weight_decay "${WEIGHT_DECAY}" \
  --log_interval "${LOG_INTERVAL}" \
  --save_predictions "${SAVE_PREDICTIONS}" \
  --use_met_cache "${USE_MET_CACHE}"

EXIT_CODE=$?
END_TIME=$(date +%s)
DURATION=$(( (END_TIME - START_TIME) / 60 ))

if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 训练完成! 耗时: ${DURATION} 分钟"
  echo ""
  echo "========== 结果文件 =========="
  OUT_DIR="${DATA_DIR}/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"
  if [ -f "${OUT_DIR}/metrics_summary.json" ]; then
    echo "  metrics_summary.json:"
    cat "${OUT_DIR}/metrics_summary.json" | python -m json.tool 2>/dev/null || cat "${OUT_DIR}/metrics_summary.json"
  fi
  echo "  输出目录: ${OUT_DIR}"
  echo "=============================="
else
  echo ""
  echo "[ERROR] 训练失败! 退出码: ${EXIT_CODE}"
  exit $EXIT_CODE
fi