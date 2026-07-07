# 可复现实验命令参考

## 环境
- Python: `D:\python\python.exe` (3.12.2)
- PyTorch: 2.9.1+cpu
- 依赖: numpy, pandas, scikit-learn, matplotlib, openpyxl, geopy, python-docx, easydict, nni

## 1. PE-DiffWaveNet Smoke Test (CPU, 已验证 ✅)

```bash
# Windows bash (Git Bash)
cd "D:\shengchan\鑷哀棰勬祴璧勬枡"
export PYTHONPATH="D:\shengchan\鑷哀棰勬祴璧勬枡\code"

/d/python/python.exe -u code/train_pediffwavenet_noleak.py \
  --data_dir "D:\shengchan\鑷哀棰勬祴璧勬枡" \
  --device cpu --exp_name student_smoke_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 --hidden_size 16 \
  --batch_size 2 --eval_batch_size 2 \
  --epochs 1 --patience 1 \
  --diff_steps 3 --inference_steps 2 \
  --num_samples 1 --eval_inference_steps 2 --eval_num_samples 1 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 --max_valid_windows 4 --max_test_windows 4 \
  --save_predictions 0 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 1
```

**验证通过**:
- 数据加载: trainX=(8,24,95,15), trainY=(8,6,95)
- PE特征: 95/95, scales=[6,9,12,24,48,72]
- 图构建: S=691, T=1570, PE=317
- 模型参数: 46,451
- 输出: matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/
- 权重: weights_N95/weights_pediffwavenet_noleak_student_smoke_cpu/

## 2. PE-DiffWaveNet Debug 训练 (CPU, 3 epochs)

```bash
cd "D:\shengchan\鑷哀棰勬祴璧勬枡"
export PYTHONPATH="D:\shengchan\鑷哀棰勬祴璧勬枡\code"

/d/python/python.exe -u code/train_pediffwavenet_noleak.py \
  --data_dir "D:\shengchan\鑷哀棰勬祴璧勬枡" \
  --device cpu --exp_name student_debug_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 --hidden_size 32 \
  --batch_size 4 --eval_batch_size 4 \
  --epochs 3 --patience 3 \
  --diff_steps 10 --inference_steps 5 \
  --num_samples 1 --eval_inference_steps 5 --eval_num_samples 1 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 64 --max_valid_windows 32 --max_test_windows 32 \
  --save_predictions 0 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 10
```

## 3. PE-DiffWaveNet 正式训练 (GPU, 120 epochs)

```bash
cd "D:\shengchan\鑷哀棰勬祴璧勬枡"
export PYTHONPATH="D:\shengchan\鑷哀棰勬祴璧勬枡\code"

/d/python/python.exe -u code/train_pediffwavenet_noleak.py \
  --data_dir "D:\shengchan\鑷哀棰勬祴璧勬枡" \
  --device cuda --exp_name student_pedw_p6_s42 \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 --hidden_size 64 \
  --batch_size 16 --eval_batch_size 16 \
  --epochs 120 --patience 15 \
  --diff_steps 50 --inference_steps 50 \
  --num_samples 3 --eval_inference_steps 50 --eval_num_samples 3 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --use_met_cache 1 --amp 1
```

## 4. DiffSTG Baseline (CPU smoke test, 已验证 ✅)

```bash
cd "D:\shengchan\鑷哀棰勬祴璧勬枡\external_baselines\DiffSTG"

/d/python/python.exe -X utf8 run_air_n95.py
```

**验证通过**:
- 数据加载: flow.npy (8717,95,1), adj.npy (95,95)
- 模型参数: 255,741 (hidden_size=16)
- 训练: 2 epochs, Loss 6.96 → 4.71
- Test RMSE: 61.33 (仅2 epochs, 需要更多训练)

## 5. DiffSTG 正式训练 (GPU, 300 epochs)

修改 `run_air_n95.py` 中 `default_config()` 的参数:
- `config.model.d_h = 64`
- `config.model.N = 200`
- `config.model.sample_steps = 200`
- `config.epoch = 300`
- `config.batch_size = 32`
- `device_str = 'cuda'`

或在 train.py 中添加 AIR_N95 配置后:
```bash
python train.py --data AIR_N95 --T_h 6 --hidden_size 64 --batch_size 32
```

## 6. 数据探索

```bash
/d/python/python.exe -X utf8 scripts/data_exploration.py
# 或精简版
/d/python/python.exe -X utf8 scripts/prepare_diffstg_data.py
```

## 关键输出检查清单

每个实验完成后确认:
- [ ] `output_dir/` 存在
- [ ] `config.json` 记录所有超参
- [ ] `metrics_summary.json` 包含 RMSE/MAE/MAPE
- [ ] `split_summary.json` 记录切分方式
- [ ] `weights/` 保存了 best checkpoint
- [ ] 日志文件完整
- [ ] 结果已填入 `unified_results.csv`
