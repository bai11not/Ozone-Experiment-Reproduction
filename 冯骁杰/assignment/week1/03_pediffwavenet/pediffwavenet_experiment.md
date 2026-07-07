# PE-DiffWaveNet 实验报告

> **生成日期**: 2026-07-06
> **对应任务**: 第 1 周 — 数据理解和代码跑通 → PE-DiffWaveNet 实验
> **模型**: PE-DiffWaveNet (Diffusion + Permutation Entropy Graph + PE-FiLM)

---

## 1. Smoke Test 运行验证

### 1.1 运行命令

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh
```

等效 Python 命令:

```bash
python -u code/train_pediffwavenet_noleak.py \
  --data_dir . \
  --device cpu \
  --exp_name student_smoke_cpu \
  --pre_len 6 \
  --seq_len 24 \
  --seed 42 \
  --N_node 95 \
  --m 15 \
  --hidden_size 16 \
  --batch_size 2 \
  --eval_batch_size 2 \
  --lr 7e-4 \
  --epochs 1 \
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
  --save_predictions 0 \
  --save_train_arrays 0 \
  --use_met_cache 1 \
  --amp 0 \
  --log_interval 1
```

### 1.2 Smoke Test 配置解析

| 参数 | 值 | 说明 |
|------|-----|------|
| `pre_len` | 6 | 预测未来 6 小时 O3 |
| `seq_len` | 24 | 使用过去 24 小时作为输入 |
| `hidden_size` | 16 | **极小**隐藏层 (正式用 64) |
| `epochs` | 1 | 仅跑 1 轮验证管道 |
| `diff_steps` | 3 | **极小**扩散步数 (正式用 50) |
| `inference_steps` | 2 | 推理采样步数 |
| `max_train_windows` | 8 | 仅用 8 个训练窗口 |
| `max_valid_windows` | 4 | 仅用 4 个验证窗口 |
| `max_test_windows` | 4 | 仅用 4 个测试窗口 |
| `batch_size` | 2 | 极小 batch |
| `device` | cpu | CPU 运行 (无 GPU) |

> 📌 Smoke test 的设计目的：用最小配置验证代码无语法错误、数据路径正确、输出目录正常，**指标本身无参考意义**。

### 1.3 Smoke Test 输出验证

输出目录: `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/`

#### 核心输出文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `config.json` | ✅ | 完整运行配置 (78 个字段) |
| `split_summary.json` | ✅ | no-leak 数据切分信息 |
| `metrics_summary.json` | ✅ | 完整指标 + per-step metrics |
| `graph_summary.json` | ✅ | S/T/PE 三图构建统计 |
| `met_stats.json` | ✅ | 14 个气象因子 min/max |
| `scale_stats.json` | ✅ | O3 归一化统计 |
| `train_loss.npy` | ✅ | 训练损失: 1.7658 |
| `valid_rmse.npy` | ✅ | 验证 RMSE: 171.92 |
| `valid_mae.npy` | ✅ | 验证 MAE: 170.01 |
| `valid_mape.npy` | ✅ | 验证 MAPE: 902.24% |
| `testX.npy` | ✅ | 测试输入 (4, 24, 95, 15) |
| `testY.npy` | ✅ | 测试目标 (4, 6, 95) |
| `validX.npy` | ✅ | 验证输入 (4, 24, 95, 15) |
| `validY.npy` | ✅ | 验证目标 (4, 6, 95) |
| `S_matrix.npy` | ✅ | 空间邻接矩阵 (95, 95) |
| `T_matrix.npy` | ✅ | 时间相关矩阵 (95, 95) |
| `PE_matrix.npy` | ✅ | PE 图邻接矩阵 (95, 95) |
| `pe_node_features.npy` | ✅ | PE 节点特征 (95, 6) |

#### 数据切分 (no-leak)

| 集合 | 索引范围 | 步数 | 时间范围 |
|------|----------|------|----------|
| Train | 0 ~ 7377 | 7,378 | 2022-01-01 00:00 ~ 2022-11-05 23:00 |
| Valid | 7378 ~ 8046 | 669 | 2022-11-06 00:00 ~ 2022-12-03 21:00 |
| Test | 8047 ~ 8716 | 670 | 2022-12-03 22:00 ~ 2022-12-31 23:00 |

#### 图构建统计

| 图 | 非零元素 | 说明 |
|-----|----------|------|
| S (空间图) | 691 | 基于站点经纬度距离 |
| T (时间图) | 1,570 | 基于 O3 时间序列相关性 |
| PE (PE图) | 317 | 基于 Permutation Entropy 特征相似度 |

### 1.4 Smoke Test 结果

| 指标 | 值 | 备注 |
|------|-----|------|
| Epoch | 1 | — |
| Train Loss | 1.7658 | — |
| Valid RMSE | 171.92 | 未收敛 |
| Valid MAE | 170.01 | 未收敛 |
| Valid MAPE | 902.24% | 未收敛 |
| Test RMSE | 166.79 | 未收敛 |
| Test MAE | 164.68 | 未收敛 |
| Test MAPE | 848.02% | 未收敛 |
| O3 Max | 410.0 μg/m³ | 训练集 O3 最大值 |

> ⚠️ 指标极差是**预期行为**：仅训练 1 epoch，hidden_size=16, diff_steps=3, 8 个训练窗口。Smoke test 的唯一目的是验证管道畅通。

---

## 2. 正式训练命令

### 2.1 主实验 (seq_len=24, pre_len=6, seed=42)

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"

DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

预期输出目录:
- `matrix_N95_PEDiffWaveNet_noleak_student_pedw_p6_s42/`
- `weights_N95/weights_pediffwavenet_noleak_student_pedw_p6_s42/`

### 2.2 小配置调试 (CPU, 3 epochs)

```bash
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=student_debug_cpu \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

### 2.3 多 Seed 实验

```bash
# seed=52
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s52 \
  bash scripts/run_train_pediffwavenet.sh 6 24 52

# seed=62
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s62 \
  bash scripts/run_train_pediffwavenet.sh 6 24 62
```

### 2.4 不同预测步长

```bash
# pre_len=1,3,12,24
for P in 1 3 12 24; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p${P} \
    bash scripts/run_train_pediffwavenet.sh ${P} 24 42
done
```

### 2.5 不同输入窗口

```bash
# seq_len=12,48
for L in 12 48; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_l${L} \
    bash scripts/run_train_pediffwavenet.sh 6 ${L} 42
done
```

### 2.6 消融实验

```bash
# 无扩散 (USE_DIFFUSION=0)
USE_DIFFUSION=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nodiff \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE 图 (USE_PE_GRAPH=0)
USE_PE_GRAPH=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nopegraph \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE FiLM (USE_PE_FILM=0)
USE_PE_FILM=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nopefilm \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# PE shuffle (PE_SHUFFLE_SEED=52)
PE_SHUFFLE_SEED=52 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_peshuffle \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

---

## 3. 输出验证清单

每次实验完成后，检查以下内容:

- [ ] `config.json` — 配置正确，参数完整
- [ ] `split_summary.json` — no-leak 切分正确 (train_rate=0.8465)
- [ ] `metrics_summary.json` — 包含 RMSE/MAE/MAPE/Peak/Per-step
- [ ] `graph_summary.json` — S/T/PE 图非零元素合理
- [ ] `train_loss.npy` — 训练损失递减
- [ ] `valid_rmse.npy` — 验证 RMSE 收敛
- [ ] `valid_mae.npy` — 验证 MAE 收敛
- [ ] `valid_mape.npy` — 验证 MAPE 收敛
- [ ] `testX.npy` / `testY.npy` — 测试数据 shape 正确
- [ ] `S_matrix.npy` / `T_matrix.npy` / `PE_matrix.npy` — 图矩阵 shape = (95, 95)
- [ ] 权重文件 `best_ema.pt` / `last.pt` — 可正常加载

### 预期指标范围 (正式训练, 120 epochs)

| 指标 | 预期范围 |
|------|----------|
| Test RMSE | ~10.5 - 12.0 |
| Test MAE | ~7.0 - 8.5 |
| Test MAPE | ~29% - 32% |
| Peak RMSE | ~13.0 - 14.5 |
| Step6 RMSE | ~13.0 - 14.0 |

---

## 4. 环境依赖

```bash
# 核心依赖
torch >= 2.0
numpy
pandas
scipy
geopy
openpyxl

# 安装命令
pip install torch numpy pandas scipy geopy openpyxl
```

当前可用环境: `torch_env` (PyTorch 2.5.1+cu121, CUDA available)

---

## 5. 首次可复现实验命令 (记录)

```bash
# ============================================================
# 环境: Linux, CUDA GPU
# 项目路径: /home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet
# ============================================================

# Step 1: Smoke test — 验证管道
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh

# Step 2: 检查输出
ls matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/
cat matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/metrics_summary.json

# Step 3: 正式训练 — 主实验
DEVICE=cuda EPOCHS=120 EXP_NAME=student_main \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# Step 4: 获取指标
python -c "
import json
with open('matrix_N95_PEDiffWaveNet_noleak_student_main/metrics_summary.json') as f:
    m = json.load(f)
print(f\"RMSE={m['test_rmse']:.4f}, MAE={m['test_mae']:.4f}, MAPE={m['test_mape']:.2f}%\")
"
```

---

*本报告为第 1 周 PE-DiffWaveNet 实验产出，Smoke test 已验证通过，正式训练待 GPU 环境执行。*
