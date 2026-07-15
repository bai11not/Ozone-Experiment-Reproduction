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

# ========== 小组和人员配置 ==========
GROUP="g3"

case "${PERSON}" in
  A) SEED=42;
     TYPES=("full 1 1 1" "no_diff 0 1 1")
     RESULT_DIR="person_A_seed42_full_nodiff" ;;
  B) SEED=42;
     TYPES=("no_pe_graph 1 0 1" "no_pe_film 1 1 0")
     RESULT_DIR="person_B_seed42_nograph_nofilm" ;;
  C) SEED=52;
     TYPES=("full 1 1 1" "no_diff 0 1 1")
     RESULT_DIR="person_C_seed52_full_nodiff" ;;
  D) SEED=52;
     TYPES=("no_pe_graph 1 0 1" "no_pe_film 1 1 0")
     RESULT_DIR="person_D_seed52_nograph_nofilm" ;;
  *) echo "错误: 人员编号必须是 A/B/C/D"; exit 1 ;;
esac

# 构建 8 组实验: 2 消融 × 2 seq_len × 2 pre_len
EXPERIMENTS=()
for type_info in "${TYPES[@]}"; do
  read -r ABL_NAME D_VAL G_VAL F_VAL <<< "${type_info}"
  for SEQ in 12 24; do
    for PRE in 6 3; do
      # 新命名: g3_pedw_{ablation?}p{pre_len}_l{seq_len}_s{seed}
      if [ "${ABL_NAME}" = "full" ]; then
        EXP_NAME="${GROUP}_pedw_p${PRE}_l${SEQ}_s${SEED}"
      else
        EXP_NAME="${GROUP}_pedw_${ABL_NAME}_p${PRE}_l${SEQ}_s${SEED}"
      fi
      EXPERIMENTS+=("${ABL_NAME} ${D_VAL} ${G_VAL} ${F_VAL} ${SEQ} ${PRE} ${EXP_NAME}")
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
echo "  消融实验: Person ${PERSON} (${GROUP})"
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
  read -r ABL_NAME D_VAL G_VAL F_VAL SEQ PRE EXP_NAME <<< "${EXPERIMENTS[$i]}"

  EXP_ID="$(printf '%s%02d' "${PERSON}" "${EXP_NUM}")"

  echo ""
  echo "--- 实验 ${EXP_NUM} / ${TOTAL} : ${EXP_ID} (${EXP_NAME}) ---"
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
实验名称: ${EXP_NAME}
人员: Person ${PERSON} (${GROUP})
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
  fi
done

# ========== 汇总 CSV（按模板格式） ==========
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
# 按模板格式: group,student,experiment_id,model,seq_len,pre_len,seed,use_diffusion,use_pe_graph,use_pe_film,pe_adaptive_loss,lr,epochs,best_epoch,rmse,mae,mape,peak_rmse,step1_rmse,step6_rmse,output_dir,log_file,notes
echo "group,student,experiment_id,model,seq_len,pre_len,seed,use_diffusion,use_pe_graph,use_pe_film,pe_adaptive_loss,lr,epochs,best_epoch,rmse,mae,mape,peak_rmse,step1_rmse,step6_rmse,output_dir,log_file,notes" > "${SUMMARY_FILE}"

for ((i = 0; i < TOTAL; i++)); do
  EXP_NUM=$((i + 1))
  read -r ABL_NAME D_VAL G_VAL F_VAL SEQ PRE EXP_NAME <<< "${EXPERIMENTS[$i]}"
  EXP_ID="$(printf '%s%02d' "${PERSON}" "${EXP_NUM}")"
  METRICS_FILE="${RESULT_PATH}/${EXP_ID}/metrics_summary.json"
  OUTPUT_DIR="matrix_N95_PEDiffWaveNet_noleak_${EXP_NAME}"

  if [ -f "${METRICS_FILE}" ]; then
    RMSE=$(python -c "import json;print(json.load(open('${METRICS_FILE}'))['test_rmse'])" 2>/dev/null || echo "")
    MAE=$(python -c "import json;print(json.load(open('${METRICS_FILE}'))['test_mae'])" 2>/dev/null || echo "")
    MAPE=$(python -c "import json;print(json.load(open('${METRICS_FILE}'))['test_mape'])" 2>/dev/null || echo "")
    BEST_EPOCH=$(python -c "import json;print(json.load(open('${METRICS_FILE}'))['best_epoch'])" 2>/dev/null || echo "")
    PEAK_RMSE=$(python -c "import json;m=json.load(open('${METRICS_FILE}'));print(m.get('rmse_peak',''))" 2>/dev/null || echo "")
    # step1_rmse 和 step6_rmse 从 per_step_rmse 数组提取
    STEP1=$(python -c "import json;m=json.load(open('${METRICS_FILE}'));a=m.get('per_step_rmse',[]);print(a[0] if len(a)>0 else '')" 2>/dev/null || echo "")
    STEP6=$(python -c "import json;m=json.load(open('${METRICS_FILE}'));a=m.get('per_step_rmse',[]);print(a[-1] if len(a)>0 else '')" 2>/dev/null || echo "")
    PE_ADAPTIVE=$(python -c "import json;m=json.load(open('${METRICS_FILE}'));print(m.get('pe_adaptive_loss','0'))" 2>/dev/null || echo "")
    echo "${GROUP},,${EXP_NAME},pedw,${SEQ},${PRE},${SEED},${D_VAL},${G_VAL},${F_VAL},${PE_ADAPTIVE},,,${BEST_EPOCH},${RMSE},${MAE},${MAPE},${PEAK_RMSE},${STEP1},${STEP6},${OUTPUT_DIR},," >> "${SUMMARY_FILE}"
  else
    echo "${GROUP},,${EXP_NAME},pedw,${SEQ},${PRE},${SEED},${D_VAL},${G_VAL},${F_VAL},,,,,,,,,,${OUTPUT_DIR},,failed" >> "${SUMMARY_FILE}"
  fi
done

echo ""
echo "汇总文件已保存: ${SUMMARY_FILE}"