# PE-DiffWaveNet 实验运行命令记录

## 实验目标

1. 运行 `scripts/run_smoke_cpu.sh` 验证环境和数据
2. 用小配置跑 1-3 个 epoch
3. 确认输出目录、日志、metrics_summary.json 是否正常
4. 记录首次可复现实验命令

## 运行命令

### 方式1：直接运行原脚本（推荐）

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
bash scripts/run_smoke_cpu.sh
```

### 方式2：运行自定义实验脚本

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
bash "白文豪/week1/PE-DiffWaveNet 实验/run_pe_diffwavenet_experiment.sh"
```

### 方式3：手动运行（3个 epoch）

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
export PYTHONPATH="/mnt/d/时空数据/臭氧预测资料/code:$PYTHONPATH"

python3 -u "code/train_pediffwavenet_noleak.py" \
  --data_dir "/mnt/d/时空数据/臭氧预测资料" \
  --device cuda \
  --exp_name student_smoke_gpu \
  --pre_len 6 \
  --seq_len 24 \
  --seed 42 \
  --N_node 95 \
  --m 15 \
  --hidden_size 16 \
  --batch_size 2 \
  --eval_batch_size 2 \
  --lr 7e-4 \
  --epochs 3 \
  --patience 1 \
  --diff_steps 3 \
  --inference_steps 2 \
  --num_samples 1 \
  --eval_inference_steps 2 \
  --eval_num_samples 1 \
  --use_diffusion 1 \
  --use_pe_graph 1 \
  --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 \
  --max_valid_windows 4 \
  --max_test_windows 4 \
  --save_predictions 1 \
  --save_train_arrays 0 \
  --use_met_cache 1 \
  --amp 1 \
  --log_interval 1
```

## 验证输出

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/PE-DiffWaveNet 实验/verify_experiment_output.py"
```

## 输出目录

| 目录 | 路径 |
|------|------|
| 结果目录 | `matrix_N95_PEDiffWaveNet_noleak_student_smoke_gpu/` |
| 权重目录 | `weights_N95/weights_pediffwavenet_noleak_student_smoke_gpu/` |

## 关键文件检查清单

- [ ] `metrics_summary.json` - 训练指标汇总
- [ ] `config.json` - 实验配置
- [ ] `train_loss.npy` - 训练损失曲线
- [ ] `valid_mae.npy` / `valid_rmse.npy` - 验证指标
- [ ] `testX.npy` / `testY.npy` - 测试数据
- [ ] `best_ema.pt` - 最佳权重
- [ ] `last.pt` - 最后权重

## 实验参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--device` | cuda | 使用 GPU |
| `--exp_name` | student_smoke_gpu | 实验名称 |
| `--seq_len` | 24 | 输入序列长度（小时） |
| `--pre_len` | 6 | 预测序列长度（小时） |
| `--epochs` | 3 | 训练轮数 |
| `--hidden_size` | 16 | 隐藏层维度（小配置） |
| `--batch_size` | 2 | 批次大小（小配置） |
| `--diff_steps` | 3 | 扩散步数（小配置） |
| `--max_train_windows` | 8 | 最大训练窗口数 |
| `--amp` | 1 | 启用混合精度 |

## 预期结果

- 训练正常完成，无报错
- 验证 MAE/RMSE 有合理数值
- 输出目录包含所有必要文件
- `metrics_summary.json` 包含训练统计信息