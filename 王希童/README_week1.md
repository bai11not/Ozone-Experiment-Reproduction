# 第 1 周：数据理解和代码跑通 —— 完成说明

> **组别**：______  **学生**：______  **日期**：2026-07-08

---

## 目录

1. [数据是什么](#1-数据是什么)
2. [输出是什么](#2-输出是什么)
3. [任务 1：数据整理](#3-任务-1数据整理)
4. [任务 2：Baseline](#4-任务-2baseline)
5. [任务 3：PE-DiffWaveNet 实验](#5-任务-3pe-diffwavenet-实验)
6. [任务 4：结果整理](#6-任务-4结果整理)
7. [附录：命令速查](#7-附录命令速查)

---

## 1. 数据是什么

### 1.1 数据来源

- **95 个空气质量监测站点**，位于京津冀及周边地区（20 个城市）
- **时间范围**：2022-01-01 00:00 ~ 2022-12-31 23:00，共 365 天 × 24 小时 = **8,717 个时间点**
- **时间分辨率**：1 小时

### 1.2 原始数据格式

`data_N95/` 目录下包含 365 个 CSV 文件，每天一个（命名 `china_sites_YYYYMMDD.csv`）：

```
date,hour,type,1001A,1002A,...,1395A
2022-01-01,0,O3,45.0,38.0,...,52.0
2022-01-01,0,PM2.5,78.0,65.0,...,82.0
...
```

- `date` / `hour`：日期和小时（0-23）
- `type`：污染物类型（O3, PM2.5, PM10, SO2, NO2, CO, AQI 等）
- 后续列为各站点编号（如 `1001A`），共 95 列

### 1.3 预处理后的模型输入（matrix_N95/）

| 文件 | 形状 | 说明 |
|------|------|------|
| `data_combined_m15.npy` | (8717, 95, 15) | O3 + 14 个气象因子 |
| `trainX.npy` | (N_windows, 24, 95, 15) | 训练输入窗口 |
| `trainY.npy` | (N_windows, 6, 95) | 训练标签（未来 6h O3） |
| `validX.npy` / `validY.npy` | 同上 | 验证集 |
| `testX.npy` / `testY.npy` | 同上 | 测试集 |
| `S_matrix.npy` | (95, 95) | 空间邻接矩阵 |
| `T_matrix_1.npy` | (95, 95) | 时间模式相似度矩阵 |
| `met_raw_aligned_cache.npz` | — | 气象因子缓存 |

### 1.4 气象因子（14 维）

`blh, d2m, fsr, kx, sp, ssr, ssrd, t2m, tcc, tcwv, tp, u10, v10, zust`

加上 O3 自身，模型输入共 **m=15 维**。

### 1.5 数据切分（no-leak 方案）

先按原始时间轴切分，再在各 split 内部滑窗，杜绝时间泄漏：

| 集合 | 时间范围 | 时间点数 | 占比 |
|------|----------|----------|------|
| Train | 2022-01-01 ~ 2022-11-05 | 7,378 | 84.65% |
| Valid | 2022-11-06 ~ 2022-12-03 | 669 | 7.67% |
| Test | 2022-12-03 ~ 2022-12-31 | 670 | 7.68% |

---

## 2. 输出是什么

### 2.1 模型预测目标

- **输入**：过去 24 小时（seq_len=24）的 O3 + 气象因子（95 站点 × 15 维）
- **输出**：未来 6 小时（pre_len=6）的 O3 浓度（95 站点 × 1 维）
- **单位**：μg/m³

### 2.2 每次实验的输出文件

成功运行后，`matrix_N95_PEDiffWaveNet_noleak_{exp_name}/` 目录下包含：

| 文件 | 说明 |
|------|------|
| `config.json` | 完整超参数记录 |
| `split_summary.json` | 数据切分方式与时间范围 |
| `graph_summary.json` | 图构建信息（S/T/PE 边数） |
| `metrics_summary.json` | 最终测试指标（RMSE, MAE, MAPE） |
| `train_loss.npy` | 训练 loss 曲线 |
| `valid_rmse.npy` / `valid_mae.npy` / `valid_mape.npy` | 验证集指标曲线 |
| `testX.npy` / `testY.npy` | 测试集输入/标签 |
| `S_matrix.npy` / `T_matrix.npy` / `PE_matrix.npy` | 图结构矩阵 |

权重文件保存在 `weights_N95/weights_pediffwavenet_noleak_{exp_name}/`。

### 2.3 核心评价指标

| 指标 | 全称 | 含义 | 方向 |
|------|------|------|------|
| **RMSE** | Root Mean Square Error | 均方根误差 (μg/m³) | ↓ |
| **MAE** | Mean Absolute Error | 平均绝对误差 (μg/m³) | ↓ |
| **MAPE** | Mean Absolute Percentage Error | 平均绝对百分比误差 (%) | ↓ |
| **Peak_RMSE** | Peak RMSE | 高值区（>160 μg/m³）RMSE | ↓ |
| **Step6_RMSE** | Step-6 RMSE | 最远预测步（第 6 小时）RMSE | ↓ |
| **Step4_6_RMSE** | Step 4-6 Avg RMSE | 第 4~6 步平均 RMSE | ↓ |

---

## 3. 任务 1：数据整理

### 3.1 阅读 `docs_word/03_数据说明.md`

原始文档为 `docs_word/03_数据说明.docx`（Word 格式）。关键信息已提取到 `outputs_data_report/data_report_draft.md`。

### 3.2 O3、PM2.5、PM10 缺失统计

运行 `scripts/data_exploration.py` 得到以下结果：

| 污染物 | 总数据量 | 缺失量 | 缺失率 |
|--------|----------|--------|--------|
| O3 | 828,115 | 18,654 | **2.25%** |
| PM2.5 | 828,115 | 10,986 | **1.33%** |
| PM10 | 828,115 | 12,805 | **1.55%** |

- O3 缺失率最高，主要集中在夜间时段（夜间臭氧浓度极低，部分站点不观测）
- PM2.5 和 PM10 缺失率较低且分布均匀

### 3.3 95 站点城市与经纬度分布

站点信息文件：`xlsx_N95/station_loc1.xlsx`

- **覆盖城市**：约 20 个城市，集中在京津冀及周边（北京、天津、石家庄、太原、济南等）
- **纬度范围**：35.68°N ~ 41.04°N
- **经度范围**：111.60°E ~ 119.61°E
- 站点编号从 `1001A` 到 `1395A`，并非连续

### 3.4 O3、PM2.5、PM10 整体时间序列

运行 `scripts/data_exploration.py` 生成：

- 图表输出：`outputs_data_report/time_series_O3_PM25_PM10.png`
- 展示 2022 年全年三种污染物的日均值变化趋势

### 3.5 数据说明初稿

已输出到 `outputs_data_report/data_report_draft.md`，包含：
- 数据来源与规模
- 污染物类型
- 缺失统计
- 站点分布
- 模型输入说明

### 3.6 数据探索命令

```bash
/d/python/python.exe -X utf8 scripts/data_exploration.py
```

---

## 4. 任务 2：Baseline

### 4.1 已有 Baseline 主对比表

来自 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv`：

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE |
|--------|------|-----|------|-----------|------------|
| **MTGNN (L=24)** | **10.6620** | **7.3383** | **29.99** | 13.3536 | 13.1806 |
| MTGNN (L=12) | 10.8028 | 7.3465 | 30.50 | 13.3002 | 13.3112 |
| Graph WaveNet (L=12) | 11.5354 | 7.7982 | 33.60 | 11.8217 | 14.6265 |
| AGCRN (L=12) | 11.6858 | 8.2093 | 34.78 | 15.0214 | 14.5599 |
| DCRNN | 12.2813 | 8.5124 | 36.46 | 15.5737 | 15.7136 |
| ATGCN-PE3 noleak | 11.8944 | 8.6023 | 35.46 | 16.1119 | 14.6744 |
| ATGCN-PE3 + hw loss | 11.7549 | 8.4868 | 35.98 | 15.6276 | 14.5510 |
| **PE-DiffWaveNet backbone** | **10.9380** ±0.34 | **7.5618** ±0.20 | **30.79** ±0.85 | 13.8293 | 13.6100 |
| PE-DiffWaveNet + PE loss | 11.1021 ±0.15 | 7.7966 ±0.13 | 31.88 ±0.52 | 13.8010 | 13.6831 |

**关键发现**：
1. MTGNN (L=24) 在 RMSE 上最佳（10.662），是主要对比目标
2. PE-DiffWaveNet backbone 排名第二（RMSE=10.938），是本文核心方法
3. Graph WaveNet 在 Peak_RMSE 上最佳（11.8217）

### 4.2 DiffSTG Baseline 调研与适配

**论文**：Wen et al., "DiffSTG: Probabilistic Spatio-Temporal Graph Forecasting with Denoising Diffusion Models", SIGSPATIAL 2023

**适配工作**（`external_baselines/DiffSTG/`）：
- 编写 `run_air_n95.py`：独立运行脚本，绕过 NNI，直接适配 AIR_N95 数据
- 数据格式转换：`scripts/prepare_diffstg_data.py` 将 matrix_N95 转为 DiffSTG 所需的 `flow.npy` (8717, 95, 1) 和 `adj.npy` (95, 95)
- 切分对齐：镜像 PE-DiffWaveNet 的 no-leak 切分（train_rate=0.8465）

### 4.3 DiffSTG 运行验证 ✅

**Smoke test 命令**：
```bash
cd "D:\shengchan\external_baselines\DiffSTG"
/d/python/python.exe -X utf8 run_air_n95.py
```

**Smoke test 结果**（CPU, 2 epochs, hidden_size=16, N=10）：
- 数据加载：✅ flow=(8717, 95, 1), adj=(95, 95)
- 模型参数：255,741
- 训练收敛：✅ Loss 6.96 → 4.71
- Test RMSE: 61.33（仅 2 epochs，需完整训练）

### 4.4 DiffSTG 正式训练命令

修改 `run_air_n95.py` 中的配置：
```python
config.model.d_h = 64        # hidden_size
config.model.N = 200          # diffusion steps
config.model.sample_steps = 200
config.epoch = 300
config.batch_size = 32
device_str = 'cuda'
```

---

## 5. 任务 3：PE-DiffWaveNet 实验

### 5.1 Smoke Test ✅

**命令**：

```bash
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

也可直接用封装脚本：
```bash
bash scripts/run_smoke_cpu.sh
```

**验证通过项**：

| 检查项 | 结果 |
|--------|------|
| 数据加载 | ✅ trainX=(8,24,95,15), trainY=(8,6,95) |
| PE 特征构建 | ✅ 95/95 nodes, scales=[6,9,12,24,48,72] |
| 图构建 | ✅ S=691 nnz, T=1570 nnz, PE=317 nnz |
| 模型参数 | ✅ 46,451 |
| 训练收敛 | ✅ Loss ≈ 1.77（仅 1 epoch，正常） |
| 输出目录 | ✅ `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/` |
| 权重保存 | ✅ `weights_N95/weights_pediffwavenet_noleak_student_smoke_cpu/` |
| config.json | ✅ 完整记录所有超参 |
| metrics_summary.json | ✅ test_rmse=166.78, test_mae=164.68, test_mape=848.01 |
| split_summary.json | ✅ 记录 no-leak 切分 |

> **说明**：Smoke test 指标数值很高是因为只用了 8 个训练窗口、hidden_size=16、1 个 epoch——仅验证代码跑通，不代表模型真实性能。

### 5.2 小配置 Debug 训练（1-3 epochs）✅

**命令**（CPU, 3 epochs, hidden_size=32, 64 个训练窗口）：

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

### 5.3 正式训练命令（GPU）

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

或使用封装脚本：
```bash
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

### 5.4 关键超参数说明

| 参数 | Smoke Test | Debug | 正式训练 | 含义 |
|------|-----------|-------|---------|------|
| `seq_len` | 24 | 24 | 24 | 输入历史窗口（小时） |
| `pre_len` | 6 | 6 | 6 | 预测未来步长（小时） |
| `seed` | 42 | 42 | 42 | 随机种子 |
| `hidden_size` | 16 | 32 | 64 | 隐藏层维度 |
| `batch_size` | 2 | 4 | 16 | 批大小 |
| `epochs` | 1 | 3 | 120 | 训练轮数 |
| `diff_steps` | 3 | 10 | 50 | 扩散步数（训练） |
| `inference_steps` | 2 | 5 | 50 | 推理采样步数 |
| `num_samples` | 1 | 1 | 3 | 推理采样次数 |
| `pe_window_step` | 168 | 168 | 168 | PE 窗口步长 |
| `use_diffusion` | 1 | 1 | 1 | 是否使用扩散模块 |
| `use_pe_graph` | 1 | 1 | 1 | 是否使用 PE 图 |
| `use_pe_film` | 1 | 1 | 1 | 是否使用 PE FiLM |

### 5.5 输出目录命名规范

```
matrix_N95_PEDiffWaveNet_noleak_{exp_name}/
weights_N95/weights_pediffwavenet_noleak_{exp_name}/
```

---

## 6. 任务 4：结果整理

### 6.1 统一结果表

已建立 `outputs_data_report/unified_results.csv`，字段定义：

| 字段 | 类型 | 说明 |
|------|------|------|
| `group` | str | 分组（reference / student / smoke_test） |
| `experiment_id` | str | 唯一实验 ID |
| `model` | str | 模型名称 |
| `seq_len` | int | 输入窗口长度 |
| `pre_len` | int | 预测步长 |
| `seed` | int/str | 随机种子（多 seed 用 / 分隔） |
| `use_diffusion` | 0/1 | 是否使用扩散 |
| `use_pe_graph` | 0/1 | 是否使用 PE 图 |
| `use_pe_film` | 0/1 | 是否使用 PE FiLM |
| `pe_adaptive_loss` | 0/1 | 是否使用 PE 自适应 loss |
| `lr` | float | 学习率 |
| `epochs` | int | 训练轮数 |
| `best_epoch` | int | 最佳 epoch |
| `rmse` | float | 测试 RMSE |
| `mae` | float | 测试 MAE |
| `mape` | float | 测试 MAPE |
| `peak_rmse` | float | 峰值 RMSE |
| `step1_rmse` ~ `step6_rmse` | float | 逐步 RMSE |
| `step4_6_rmse` | float | 第 4-6 步平均 RMSE |
| `output_dir` | str | 输出目录 |
| `log_file` | str | 日志文件路径 |
| `notes` | str | 备注 |

### 6.2 图表命名规范

```
{model}_{pollutant}_{metric}_{detail}.{ext}
```

**示例**：

| 文件名 | 含义 |
|--------|------|
| `pediffwavenet_O3_ts_pred_vs_true.png` | PE-DiffWaveNet O3 预测 vs 真实 |
| `comparison_O3_rmse_bar.png` | 各模型 RMSE 柱状图 |
| `ablation_O3_rmse_bar.png` | 消融实验 RMSE |
| `station_map_95.png` | 95 站点地图 |
| `missing_heatmap_O3.png` | O3 缺失热力图 |
| `time_series_O3_PM25_PM10.png` | 三污染物时间序列 |

**命名要素**：
- `model`：pediffwavenet / mtgnn / graphwavenet / agcrn / dcrnn / atgcn_pe3
- `pollutant`：O3 / PM25 / PM10
- `metric`：rmse / mae / mape / peak / step6
- `detail`：bar / box / scatter / ts / heatmap

### 6.3 Paper Assets 表格字段整理

`paper_assets_pediffwavenet/` 目录包含三张论文表格：

| 文件 | 内容 | 关键字段 |
|------|------|----------|
| `table1_main_raw_comparison.csv` | 主模型对比 | Method, RMSE, MAE, MAPE, Peak_RMSE, Step6_RMSE, Source |
| `table2_ablation.csv` | 消融实验 | Variant, Seeds, RMSE, MAE, MAPE, Step4_6_RMSE, Step6_RMSE, Peak_RMSE |
| `table3_pe_stratified_summary.csv` | PE 分层统计 | stratum (low/mid/high PE), node_count, pe_score_mean, 各指标均值±标准差 |

学生新结果**不要覆盖**这些文件，应写入自己的 `unified_results.csv`，由结果整理组统一合并。

### 6.4 实验记录模板

使用 `templates/experiment_log_template.md`，每个实验必须记录：
- 运行命令或配置
- 日志文件
- 输出目录
- 指标结果
- 1 页以内实验结论
- 可放入报告的图表

---

## 7. 附录：命令速查

### 7.1 环境信息

| 项目 | 值 |
|------|-----|
| Python | `D:\python\python.exe` (3.12.2) |
| PyTorch | 2.9.1+cpu |
| 关键依赖 | numpy, pandas, scikit-learn, matplotlib, openpyxl, geopy, easydict, nni |
| 项目根目录 | `D:\shengchan\鑷哀棰勬祴璧勬枡` |

### 7.2 所有可复现命令汇总

```bash
# ===== 0. 设置环境 =====
export PYTHONPATH="D:\shengchan\鑷哀棰勬祴璧勬枡\code"

# ===== 1. 数据探索 =====
/d/python/python.exe -X utf8 scripts/data_exploration.py
/d/python/python.exe -X utf8 scripts/prepare_diffstg_data.py

# ===== 2. PE-DiffWaveNet Smoke Test (CPU, 1 epoch) =====
# 方式 A: Shell 脚本
bash scripts/run_smoke_cpu.sh

# 方式 B: Python 直接调用（见 5.1 节完整命令）

# ===== 3. PE-DiffWaveNet Debug 训练 (CPU, 3 epochs) =====
# 见 5.2 节完整命令

# ===== 4. PE-DiffWaveNet 正式训练 (GPU, 120 epochs) =====
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 多 seed 实验
for seed in 42 52 62; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s${seed} \
    bash scripts/run_train_pediffwavenet.sh 6 24 ${seed}
done

# ===== 5. DiffSTG Baseline =====
cd external_baselines/DiffSTG
/d/python/python.exe -X utf8 run_air_n95.py
```

### 7.3 第一次可复现实验记录

| 项目 | 值 |
|------|-----|
| **实验名称** | `student_smoke_cpu` |
| **命令** | `bash scripts/run_smoke_cpu.sh` |
| **随机种子** | `42` |
| **输入窗口 (seq_len)** | `24`（过去 24 小时） |
| **预测步长 (pre_len)** | `6`（未来 6 小时） |
| **扩散步数** | `diff_steps=3, inference_steps=2` |
| **PE 配置** | `use_pe_graph=1, use_pe_film=1, pe_window_step=168` |
| **设备** | `cpu` |
| **Epochs** | `1` |
| **输出目录** | `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/` |
| **权重目录** | `weights_N95/weights_pediffwavenet_noleak_student_smoke_cpu/` |
| **验证状态** | ✅ 通过 |

### 7.4 输出检查清单

每个实验完成后确认：

- [ ] `matrix_N95_PEDiffWaveNet_noleak_{exp_name}/` 目录存在
- [ ] `config.json` 记录所有超参
- [ ] `metrics_summary.json` 包含 RMSE / MAE / MAPE
- [ ] `split_summary.json` 记录切分方式
- [ ] `graph_summary.json` 记录图结构
- [ ] `weights_N95/weights_pediffwavenet_noleak_{exp_name}/` 保存了 best checkpoint
- [ ] 日志文件完整
- [ ] 结果已填入 `outputs_data_report/unified_results.csv`
- [ ] 如有图表，已按命名规范保存

---

## 8. 本周小结

第 1 周完成了以下核心工作：

1. **数据理解**：明确了 95 站点 × 8717 小时的数据规模，O3 缺失率 2.25%，训练/验证/测试按 no-leak 方式切分
2. **Baseline 确认**：已有 MTGNN (L=24) 为最强 baseline (RMSE=10.662)，DiffSTG 已适配并跑通 smoke test
3. **PE-DiffWaveNet 跑通**：smoke test 和 debug 训练均验证通过，输出目录、日志、metrics_summary.json 正常
4. **结果框架建立**：统一结果表、图表命名规范、实验模板均已就位

下一周可进入正式训练、多 seed 实验和消融实验阶段。
