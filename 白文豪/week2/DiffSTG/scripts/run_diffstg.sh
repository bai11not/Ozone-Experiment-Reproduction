#!/usr/bin/env bash
# run_diffstg.sh
# DiffSTG 单次实验运行脚本
# 用法: bash run_diffstg.sh <seed> <T_h> <T_p> <exp_name>

set -euo pipefail

SEED="${1:?缺少 seed}"
T_H="${2:?缺少 T_h (seq_len)}"
T_P="${3:?缺少 T_p (pre_len)}"
EXP_NAME="${4:?缺少 exp_name}"

# ========== 路径 ==========
DIFFSTG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${DIFFSTG_DIR}/../../week1/DiffSTG"
DATA_DIR="${DIFFSTG_DIR}/../../week1/DiffSTG"

export PYTHONPATH="${CODE_DIR}:${PYTHONPATH:-}"

# ========== 固定参数 ==========
DATA="AIR_N95"
HIDDEN_SIZE=32
N=200
BATCH_SIZE=32
LR=0.0001
EPOCHS=300
BETA_SCHEDULE="quad"
BETA_END=0.1
SAMPLE_STEPS=200
N_SAMPLES=8
EARLY_STOP=10

echo "========================================"
echo " DiffSTG 实验"
echo "========================================"
echo "  实验: ${EXP_NAME}"
echo "  seed: ${SEED}"
echo "  T_h:  ${T_H}"
echo "  T_p:  ${T_P}"
echo "  data: ${DATA}"
echo "========================================"
echo ""

START_TIME=$(date +%s)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始训练..."

python -u "${CODE_DIR}/train.py" \
  --seed "${SEED}" \
  --data "${DATA}" \
  --T_h "${T_H}" \
  --T_p "${T_P}" \
  --hidden_size "${HIDDEN_SIZE}" \
  --N "${N}" \
  --batch_size "${BATCH_SIZE}" \
  --lr "${LR}" \
  --beta_schedule "${BETA_SCHEDULE}" \
  --beta_end "${BETA_END}" \
  --sample_steps "${SAMPLE_STEPS}" \
  --n_samples "${N_SAMPLES}" \
  --is_train True \
  --is_test False

EXIT_CODE=$?
DURATION=$(( ($(date +%s) - START_TIME) / 60 ))

if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 完成! 耗时: ${DURATION} 分钟"
  echo "输出目录: ${CODE_DIR}/output/"
else
  echo "[ERROR] 失败! 退出码: ${EXIT_CODE}"
  exit $EXIT_CODE
fi