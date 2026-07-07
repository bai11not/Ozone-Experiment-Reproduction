# Week 1 运行命令汇总
# 项目: PE-DiffWaveNet 臭氧预测
# 日期: 2026-07-07

# ====== 环境变量 ======
ROOT="d:/桌面/臭氧预测资料/臭氧预测资料"
PY=/c/Users/myt/AppData/Local/Python/bin/python.exe
export PYTHONPATH="${ROOT}/code"

# ====== 1. 安装依赖 ======
$PY -m pip install scikit-learn geopy openpyxl python-pptx

# ====== 2. 数据整理分析 ======
$PY -u C:/Users/myt/week1_analysis.py

# ====== 3. PE-DiffWaveNet Smoke Test (1 epoch, 8 windows) ======
$PY -u "${ROOT}/code/train_pediffwavenet_noleak.py" \
  --data_dir "${ROOT}" \
  --device cpu \
  --exp_name student_smoke_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 \
  --hidden_size 16 --batch_size 2 --eval_batch_size 2 \
  --lr 7e-4 --epochs 1 --patience 1 \
  --diff_steps 3 --inference_steps 2 \
  --num_samples 1 --eval_inference_steps 2 --eval_num_samples 1 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 --max_valid_windows 4 --max_test_windows 4 \
  --save_predictions 0 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 1

# ====== 4. PE-DiffWaveNet Debug (3 epoch, 64 windows) ======
$PY -u "${ROOT}/code/train_pediffwavenet_noleak.py" \
  --data_dir "${ROOT}" \
  --device cpu \
  --exp_name student_debug_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 \
  --hidden_size 16 --batch_size 8 --eval_batch_size 8 \
  --lr 7e-4 --epochs 3 --patience 5 \
  --diff_steps 10 --inference_steps 10 \
  --num_samples 2 --eval_inference_steps 5 --eval_num_samples 2 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 64 --max_valid_windows 32 --max_test_windows 32 \
  --save_predictions 1 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 10

# ====== 5. ATGCN-PE3 Baseline Debug (3 epoch, 64 windows) ======
$PY -u "${ROOT}/code/train_atgcn_pe3_noleak.py" \
  --data_dir "${ROOT}" \
  --device cpu \
  --exp_name atgcn_pe3_cpu_debug \
  --pre_len 6 --seq_len 12 --seed 42 \
  --N_node 95 --m 15 \
  --hidden_size 16 --batch_size 8 --eval_batch_size 8 \
  --lr 7e-4 --epochs 3 --patience 5 \
  --diff_steps 10 --inference_steps 10 \
  --num_samples 2 --eval_inference_steps 5 --eval_num_samples 2 \
  --max_train_windows 64 --max_valid_windows 32 --max_test_windows 32 \
  --save_predictions 1 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 10 \
  --pe_window_step 168

# ====== 6. 生成 DiffSTG 数据文件 ======
$PY -u "${ROOT}/gen_diffstg_data.py"

# ====== 输出目录 ======
# outputs_week1/              — 数据整理结果
# matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/  — Smoke test
# matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/  — Debug run
# matrix_N95_ATGCNPE3_noleak_atgcn_pe3_cpu_debug/     — ATGCN-PE3
# data/dataset/AIR_N95/       — DiffSTG 数据文件
