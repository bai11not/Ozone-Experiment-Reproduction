#!/usr/bin/env bash
# run_person_experiments.sh
# 批量运行指定人员的全部 8 组消融实验
#
# 用法:
#   bash run_person_experiments.sh A            # 全部 8 组
#   bash run_person_experiments.sh A 3          # 从第 3 组开始（断点续跑）
#   bash run_person_experiments.sh A 1 dry      # 仅打印命令

set -euo pipefail

PERSON="${1:?缺少人员编号 (A/B/C/D)}"
START_FROM="${2:-1}"
DRY_RUN="${3:-}"

# ========== 人员配置 ==========
# 每人: seed + 2 个消融类型
case "${PERSON}" in
  A) SEED=42;
     TYPES=("full 1 1 1" "no_diff 0 1 1")
     RESULT_DIR="person_A_seed42_full_nodiff" ;;
  B) SEED=42;
     TYPES=("no_graph 1 0 1" "no_film 1 1 0")
     RESULT_DIR="person_B_seed42_nograph_nofilm" ;;
  C) SEED=52;
     TYPES=("full 1 1 1" "no_diff 0 1 1")
     RESULT_DIR="person_C_seed52_full_nodiff" ;;
  D) SEED=52;
     TYPES=("no_graph 1 0 1" "no_film 1 1 0")
     RESULT_DIR="person_D_seed52_nograph_nofilm" ;;
  *) echo "错误: 人员编号必须是 A/B/C/D"; exit 1 ;;
esac

# 2 消融类型 × 2 seq_len × 2 pre_len = 8 组
# seq_len=12,24  pre_len=6,3
EXPERIMENTS=()
for type_info in "${TYPES[@]}"; do
  read -r ABL_NAME D_VAL G_VAL F_VAL <<< "${type_info}"
  for SEQ in 12 24; do
    for PRE in 6 3; do
      EXPERIMENTS+=("${ABL_NAME} ${D_VAL} ${G_VAL} ${F_VAL} ${SEQ} ${PRE}")
    done
  done
done

TOTAL=${#EXPERIMENTS[@]}
SUCCESS=0
FAIL=0
FAILED_LIST=()

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEEK2_DIR="$(dirname "${SCRIPT_DIR}")"
RESULT_PATH="${WEEK2_DIR}/results/${RESULT_DIR}"
mkdir -p "${RESULT_PATH}"

echo "========================================"
echo "  消融实验: Person ${PERSON}"
echo "  Seed: ${SEED}"
echo "  共 ${TOTAL} 组实验"
if [ "${START_FROM}" -gt 1 ]; then
  echo "  从第 ${START_FROM} 组开始"
fi
if [ "${DRY_RUN}" = "dry" ]; then
  echo "  [DRY RUN] 仅打印命令"
fi
echo "========================================"
echo ""

for ((i = START_FROM - 1; i < TOTAL; i++)); do
  EXP_NUM=$((i + 1))
  read -r ABL_NAME D_VAL G_VAL F_VAL SEQ PRE <<< "${EXPERIMENTS[$i]}"

  EXP_ID="$(printf '%s%02d' "${PERSON}" "${EXP_NUM}")"
  EXP_LABEL="s${SEED}-${ABL_NAME}-l${SEQ}-p${PRE}"
  EXP_NAME="${EXP_ID}_${EXP_LABEL}"

  echo ""
  echo "--- 实验 ${EXP_NUM} / ${TOTAL} : ${EXP_ID} (${EXP_LABEL}) ---"
  echo "    参数: seed=${SEED}, ablation=${ABL_NAME}, seq_len=${SEQ}, pre_len=${PRE}"
  echo "          use_diffusion=${D_VAL}, use_pe_graph=${G_VAL}, use_pe_film=${F_VAL}"

  if [ "${DRY_RUN}" = "dry" ]; then
    echo "    [DRY RUN] bash run_single_experiment.sh ${SEED} ${SEQ} ${PRE} ${D_VAL} ${G_VAL} ${F_VAL} ${EXP_NAME}"
    ((SUCCESS++)) || true
    continue
  fi

  START_TS=$(date +%s)

  if bash "${SCRIPT_DIR}/run_single_experiment.sh" \
    "${SEED}" "${SEQ}" "${PRE}" \
    "${D_VAL}" "${G_VAL}" "${F_VAL}" \
    "${EXP_NAME}"; then

    END_TS=$(date +%s)
    DURATION=$(( (END_TS - START_TS) / 60 ))

    SRC_DIR="d:/时空数据/臭氧预测资料/matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"
    DEST_DIR="${RESULT_PATH}/${EXP_ID}"
    mkdir -p "${DEST_DIR}"

    if [ -d "${SRC_DIR}" ]; then
      for f in metrics_summary.json config.json; do
        [ -f "${SRC_DIR}/${f}" ] && cp "${SRC_DIR}/${f}" "${DEST_DIR}/"
      done
    fi

    cat > "${DEST_DIR}/experiment_record.txt" << EOF
实验编号: ${EXP_ID}
实验标签: ${EXP_LABEL}
人员: Person ${PERSON}
运行时间: $(date '+%Y-%m-%d %H:%M:%S')
耗时: ${DURATION} 分钟
参数:
  seed: ${SEED}
  ablation: ${ABL_NAME}
  seq_len: ${SEQ}
  pre_len: ${PRE}
  use_diffusion: ${D_VAL}
  use_pe_graph: ${G_VAL}
  use_pe_film: ${F_VAL}
状态: 成功
EOF

    echo "    ✓ 完成 (耗时: ${DURATION} 分钟)"
    ((SUCCESS++)) || true
  else
    echo "    ✗ 失败"
    ((FAIL++)) || true
    FAILED_LIST+=("${EXP_ID}")

    DEST_DIR="${RESULT_PATH}/${EXP_ID}"
    mkdir -p "${DEST_DIR}"
    cat > "${DEST_DIR}/FAILURE_LOG.txt" << EOF
实验编号: ${EXP_ID}
实验标签: ${EXP_LABEL}
失败时间: $(date '+%Y-%m-%d %H:%M:%S')
参数:
  seed: ${SEED}
  ablation: ${ABL_NAME}
  seq_len: ${SEQ}
  pre_len: ${PRE}
  use_diffusion: ${D_VAL}
  use_pe_graph: ${G_VAL}
  use_pe_film: ${F_VAL}
EOF
  fi
done

# ========== 汇总 ==========
echo ""
echo "========================================"
echo "  Person ${PERSON} 实验完成"
echo "  成功: ${SUCCESS} / ${TOTAL}"
if [ "${FAIL}" -gt 0 ]; then
  echo "  失败: ${FAIL} / ${TOTAL}"
  echo "  失败列表: ${FAILED_LIST[*]}"
fi
echo "  结果目录: ${RESULT_PATH}"
echo "========================================"

SUMMARY_FILE="${RESULT_PATH}/person_${PERSON}_summary.csv"
echo "exp_id,seed,ablation,seq_len,pre_len,use_diffusion,use_pe_graph,use_pe_film,status,test_rmse,test_mae,test_mape,best_epoch" > "${SUMMARY_FILE}"

for ((i = 0; i < TOTAL; i++)); do
  EXP_NUM=$((i + 1))
  read -r ABL_NAME D_VAL G_VAL F_VAL SEQ PRE <<< "${EXPERIMENTS[$i]}"
  EXP_ID="$(printf '%s%02d' "${PERSON}" "${EXP_NUM}")"
  METRICS_FILE="${RESULT_PATH}/${EXP_ID}/metrics_summary.json"

  if [ -f "${METRICS_FILE}" ]; then
    RMSE=$(python -c "import json; print(json.load(open('${METRICS_FILE}'))['test_rmse'])" 2>/dev/null || echo "")
    MAE=$(python -c "import json; print(json.load(open('${METRICS_FILE}'))['test_mae'])" 2>/dev/null || echo "")
    MAPE=$(python -c "import json; print(json.load(open('${METRICS_FILE}'))['test_mape'])" 2>/dev/null || echo "")
    BEST_EPOCH=$(python -c "import json; print(json.load(open('${METRICS_FILE}'))['best_epoch'])" 2>/dev/null || echo "")
    echo "${EXP_ID},${SEED},${ABL_NAME},${SEQ},${PRE},${D_VAL},${G_VAL},${F_VAL},success,${RMSE},${MAE},${MAPE},${BEST_EPOCH}" >> "${SUMMARY_FILE}"
  else
    echo "${EXP_ID},${SEED},${ABL_NAME},${SEQ},${PRE},${D_VAL},${G_VAL},${F_VAL},failed,,,,," >> "${SUMMARY_FILE}"
  fi
done

echo ""
echo "汇总文件已保存: ${SUMMARY_FILE}"