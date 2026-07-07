#!/bin/bash
# ============================================================
# 第 1 周 全部运行命令 — 数据整理 / Baseline / PE-DiffWaveNet
# ============================================================

PROJECT_DIR="/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
DIFFSTG_DIR="${PROJECT_DIR}/external_baselines/DiffSTG"

# ============================================================
# 一、数据整理
# ============================================================

# 1.1 缺失值统计 + 站点分布 + 时间序列图
cd "${PROJECT_DIR}"
python data_organization.py

# ============================================================
# 二、PE-DiffWaveNet 实验
# ============================================================

# 2.1 Smoke test — 最小配置验证代码/数据/路径 (1 epoch, CPU, 极小网络)
cd "${PROJECT_DIR}"
bash scripts/run_smoke_cpu.sh
# 等效命令:
# python -u code/train_pediffwavenet_noleak.py \
#   --data_dir . --device cpu --exp_name student_smoke_cpu \
#   --pre_len 6 --seq_len 24 --seed 42 --N_node 95 --m 15 \
#   --hidden_size 16 --batch_size 2 --eval_batch_size 2 --lr 7e-4 \
#   --epochs 1 --patience 1 --diff_steps 3 --inference_steps 2 \
#   --num_samples 1 --eval_inference_steps 2 --eval_num_samples 1 \
#   --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
#   --pe_window_step 168 --max_train_windows 8 --max_valid_windows 4 \
#   --max_test_windows 4 --save_predictions 0 --save_train_arrays 0 \
#   --use_met_cache 1 --amp 0 --log_interval 1

# 2.2 小配置调试 (CPU, 3 epochs, 验证收敛趋势)
cd "${PROJECT_DIR}"
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 \
  MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=student_debug_cpu \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 2.3 主实验 (GPU, 120 epochs, T_h=24, T_p=6, seed=42)
cd "${PROJECT_DIR}"
DEVICE=cuda EPOCHS=120 EXP_NAME=student_main_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 2.4 多 seed 实验
cd "${PROJECT_DIR}"
DEVICE=cuda EPOCHS=120 EXP_NAME=student_main_p6_s52 \
  bash scripts/run_train_pediffwavenet.sh 6 24 52

DEVICE=cuda EPOCHS=120 EXP_NAME=student_main_p6_s62 \
  bash scripts/run_train_pediffwavenet.sh 6 24 62

# 2.5 不同预测步长
cd "${PROJECT_DIR}"
for P in 1 3 12 24; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_p${P}_l24 \
    bash scripts/run_train_pediffwavenet.sh ${P} 24 42
done

# 2.6 不同输入窗口
cd "${PROJECT_DIR}"
for L in 12 48; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_p6_l${L} \
    bash scripts/run_train_pediffwavenet.sh 6 ${L} 42
done

# 2.7 消融实验
cd "${PROJECT_DIR}"
# 无扩散
USE_DIFFUSION=0 DEVICE=cuda EPOCHS=120 EXP_NAME=ablation_nodiff \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE 图
USE_PE_GRAPH=0 DEVICE=cuda EPOCHS=120 EXP_NAME=ablation_nopegraph \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE FiLM
USE_PE_FILM=0 DEVICE=cuda EPOCHS=120 EXP_NAME=ablation_nopefilm \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# PE shuffle
PE_SHUFFLE_SEED=52 DEVICE=cuda EPOCHS=120 EXP_NAME=ablation_peshuffle \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# ============================================================
# 三、Baseline
# ============================================================

# 3.1 ATGCN-PE3 noleak (T_h=12, T_p=6)
cd "${PROJECT_DIR}"
python code/train_atgcn_pe3_noleak.py \
    --seq_len 12 --pre_len 6 --seed 42 \
    --epochs 50 --batch_size 16 \
    --hidden_size 64 --lr 7e-4 \
    --device cuda \
    --exp_name baseline_l12_p6_s42

# 3.2 DiffSTG — 安装依赖 + 最小测试
pip install easydict
cd "${DIFFSTG_DIR}"
python train_air_n95.py \
    --T_h 12 --T_p 12 --epochs 1 --batch_size 8 \
    --device cpu --is_test 1 --exp_name debug

# 3.3 DiffSTG — 正式训练
cd "${DIFFSTG_DIR}"
python train_air_n95.py \
    --T_h 12 --T_p 12 --epochs 300 --batch_size 32 \
    --lr 0.0001 --hidden_size 32 --seed 42 --device cuda \
    --exp_name formal_l12_p12_s42

# ============================================================
# 四、读取指标
# ============================================================

cd "${PROJECT_DIR}"
python -c "
import json
with open('matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/metrics_summary.json') as f:
    m = json.load(f)
print(f'Smoke Test — RMSE: {m[\"test_rmse\"]:.4f}, MAE: {m[\"test_mae\"]:.4f}, MAPE: {m[\"test_mape\"]:.2f}%')
"

echo ""
echo "=== 第 1 周命令清单结束 ==="
