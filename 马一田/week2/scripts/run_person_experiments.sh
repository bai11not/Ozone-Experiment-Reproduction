#!/bin/bash
# ============================================================
# Week 2: Person C 批量消融实验 (马一田)
# seed=52, full + no_diff, 共 8 组
# 用法: bash run_person_experiments.sh
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${SCRIPT_DIR}/../results/person_C/run_log_${TIMESTAMP}.txt"
mkdir -p "$(dirname "${LOG_FILE}")"

echo "============================================="
echo "Week 2: Person C (马一田) - Ablation Experiments"
echo "seed=52, full + no_diff"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

# C01: full, l=12, p=6
echo "[C01/8] s52-full-l12-p6"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 12 6 1 1 1 "s52-full-l12-p6" 2>&1 | tee -a "${LOG_FILE}"

# C02: full, l=12, p=3
echo "[C02/8] s52-full-l12-p3"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 12 3 1 1 1 "s52-full-l12-p3" 2>&1 | tee -a "${LOG_FILE}"

# C03: full, l=24, p=6
echo "[C03/8] s52-full-l24-p6"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 24 6 1 1 1 "s52-full-l24-p6" 2>&1 | tee -a "${LOG_FILE}"

# C04: full, l=24, p=3
echo "[C04/8] s52-full-l24-p3"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 24 3 1 1 1 "s52-full-l24-p3" 2>&1 | tee -a "${LOG_FILE}"

# C05: no_diff, l=12, p=6
echo "[C05/8] s52-nodiff-l12-p6"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 12 6 0 1 1 "s52-nodiff-l12-p6" 2>&1 | tee -a "${LOG_FILE}"

# C06: no_diff, l=12, p=3
echo "[C06/8] s52-nodiff-l12-p3"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 12 3 0 1 1 "s52-nodiff-l12-p3" 2>&1 | tee -a "${LOG_FILE}"

# C07: no_diff, l=24, p=6
echo "[C07/8] s52-nodiff-l24-p6"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 24 6 0 1 1 "s52-nodiff-l24-p6" 2>&1 | tee -a "${LOG_FILE}"

# C08: no_diff, l=24, p=3
echo "[C08/8] s52-nodiff-l24-p3"
bash "${SCRIPT_DIR}/run_single_experiment.sh" 52 24 3 0 1 1 "s52-nodiff-l24-p3" 2>&1 | tee -a "${LOG_FILE}"

echo ""
echo "Person C done! All 8 experiments completed."
echo "Log: ${LOG_FILE}"
