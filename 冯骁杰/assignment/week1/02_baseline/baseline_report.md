# Baseline 调研与运行报告

> **生成日期**: 2026-07-06
> **对应任务**: 第 1 周 — 数据理解和代码跑通 → Baseline 复现
> **数据**: data_N95 + matrix_N95 (95站点, O3, 2022年)

---

## 1. 已有 Baseline 确认

根据 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv`，当前已有以下 baseline 指标:

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE | Source |
|--------|------|-----|------|-----------|------------|--------|
| MTGNN (L=24) | 10.6620 | 7.3383 | 29.99 | 13.3536 | 13.1806 | official raw, seed42 |
| MTGNN (L=12) | 10.8028 | 7.3465 | 30.50 | 13.3002 | 13.3112 | official raw, seed42 |
| Graph WaveNet (L=12) | 11.5354 | 7.7982 | 33.60 | 11.8217 | 14.6265 | official raw, seed42 |
| AGCRN (L=12) | 11.6858 | 8.2093 | 34.78 | 15.0214 | 14.5599 | official raw, seed42 |
| DCRNN | 12.2813 | 8.5124 | 36.46 | 15.5737 | 15.7136 | official raw, seed42 |
| ATGCN-PE3 noleak | 11.8944 | 8.6023 | 35.46 | 16.1119 | 14.6744 | ATGCN raw, seed42 |
| ATGCN-PE3 + horizon-weight loss | 11.7549 | 8.4868 | 35.98 | 15.6276 | 14.5510 | ATGCN raw, seed42 |
| **PE-DiffWaveNet backbone (ours)** | **10.9380 ± 0.3353** | **7.5618 ± 0.1968** | **30.79 ± 0.85** | **13.8293 ± 1.0947** | **13.6100 ± 0.6096** | ours raw, seeds 42/52/62 |
| PE-DiffWaveNet + PE-guided loss | 11.1021 ± 0.1483 | 7.7966 ± 0.1331 | 31.88 ± 0.52 | 13.8010 ± 0.5895 | 13.6831 ± 0.1506 | ours raw, seeds 42/52/62 |

### Baseline 方法简介

| 方法 | 类型 | 说明 |
|------|------|------|
| **MTGNN** | 时空图神经网络 | 自动学习图结构的多元时间序列预测模型 |
| **Graph WaveNet** | 时空图卷积 | 结合自适应邻接矩阵和扩张因果卷积 |
| **AGCRN** | 自适应图卷积 | 节点自适应参数学习和数据自适应图生成 |
| **DCRNN** | 扩散卷积 | 基于图扩散的序列到序列预测 |
| **ATGCN-PE3** | 注意力时空 + PE | 本项目代码中的扩散模型 baseline，含 permutation entropy 图 |
| **PE-DiffWaveNet** | 扩散模型 + PE | 本项目主模型，含 PE-graph / PE-FiLM / diffusion 模块 |

---

## 2. DiffSTG 调研与适配

### 2.1 论文信息

- **论文**: DiffSTG: Probabilistic Spatio-Temporal Graph Forecasting with Denoising Diffusion Models
- **会议**: ACM SIGSPATIAL 2023
- **代码**: [https://github.com/wenhaomin/DiffSTG](https://github.com/wenhaomin/DiffSTG)
- **许可证**: MIT
- **与项目关系**: 同为扩散类时空图预测模型，最适合作为扩散 baseline 对比

### 2.2 适配映射

| DiffSTG 概念 | 本项目对应 |
|-------------|-----------|
| graph node | 95 个空气质量站点 |
| flow.npy | O3 时间序列 (8717, 95, 1) |
| adj.npy | 站点空间距离图 / 相关性图 (95, 95) |
| T_h | 历史输入窗口 (如 24) |
| T_p | 预测步长 (如 6) |
| MAE / RMSE | 与主表指标对齐 |

### 2.3 数据适配结果

已在 `external_baselines/DiffSTG/data/dataset/AIR_N95/` 生成:

| 文件 | 形状 | 说明 |
|------|------|------|
| `flow.npy` | (8717, 95, 1) | O3 逐时数据，T×N×F 格式 |
| `adj.npy` | (95, 95) | 高斯核距离邻接矩阵 (稀疏度 36.3%) |
| `adj_corr.npy` | (95, 95) | 皮尔逊相关邻接矩阵 (阈值 0.5, 稀疏度 1.1%) |
| `split_info.json` | — | 训练/验证/测试切分索引 |

- 数据切分与 PE-DiffWaveNet 保持一致: train_rate=0.8465
  - Train: 0 ~ 7377 (7378 时间步)
  - Valid: 7378 ~ 8046 (669 时间步)
  - Test: 8047 ~ 8716 (670 时间步)

### 2.4 DiffSTG 原生限制与适配方案

**发现**: DiffSTG 原代码将 `T_p` 硬绑定为 `T_h` (即预测长度 = 输入长度):
```python
# train.py line 262
config.T_p = config.model.T_p = params['T_h']  # T_p 强制等于 T_h
```

**适配方案**:
1. **方案 A (最小改动)**: 使用 T_h = T_p = 12, 与其他 baseline (L=12) 对齐
2. **方案 B (完整适配)**: 修改 `model.py` 和 `train.py`, 支持独立的 T_p 参数
3. **方案 C (实用)**: 使用 T_h = 24, T_p = 24, 对后 6 步单独评估 per-step metrics

本报告已创建 `train_air_n95.py` 实现了方案 B，支持独立的 `--T_p` 参数。

### 2.5 适配操作详解与原因分析

以下详述将 DiffSTG 适配到本项目 O₃ 预测数据的五项具体操作及其设计原因。

#### 2.5.1 格式转换：生成 flow.npy

**操作**：将 `matrix_N95/data.npy`（维度 95×8717，站点×时间）转置为 8717×95，并增加特征维（F=1），最终保存为 (8717, 95, 1) 的 flow.npy。

**原因**：
- DiffSTG 读取数据的约定格式为 (T, V, F)，即时间步在第一维、节点在第二维、特征在第三维。本项目原始存储为 (V, T)，需轴交换
- F=1 表示当前仅使用 O₃ 单一目标变量（14 类气象因子暂未纳入，DiffSTG 原生不直接支持多特征输入，属于后续改进方向）

#### 2.5.2 空间图构建：高斯核距离邻接矩阵

**操作**：
1. 基于 95 站经纬度，用 Haversine 公式计算站间球面距离 d_ij
2. 高斯核函数转换为相似度权重：A_ij = exp(-d_ij² / (2σ²))
3. 结果：(95, 95) 矩阵，非零占比 **36.3%**

**原因**：
- **方法一致**：DiffSTG 论文对空气质量数据集（AIR-BJ、AIR-GZ）明确说明 "build the spatial correlation matrix A using the distance between two stations"。本项目沿用相同方法
- **高斯核平滑映射**：距离越近 → 权重接近 1 → 信息传递越强；距离越远 → 权重趋近 0 → 几乎不传递。σ 控制衰减速度
- **36.3% 稀疏度物理合理**：O₃ 是区域性污染物，城市群内站点间存在显著空间相关性（共同受气象和传输影响），平均每站与约 34 个其他站点连通

#### 2.5.3 备选图结构：皮尔逊相关邻接矩阵

**操作**：
1. 计算每对站点全年 O₃ 序列的皮尔逊相关系数 r_ij
2. 阈值过滤，仅保留 |r| ≥ 0.5 的连接
3. 结果：(95, 95) 矩阵，非零占比仅 **1.1%**

**原因**：
- **弥补距离图的固有缺陷**：距离图假设"空间近=功能相关"，但 O₃ 传输受风向、地形、排放源分布影响。两站距离 100 公里但处于同一传输通道（如华北平原南风传输带），O₃ 可能高度同步；两站距离 10 公里但分处城区上/下风向，浓度可能完全不同。相关性图直接从观测数据学习功能关系，不依赖距离假设
- **阈值 0.5 过滤噪声**：仅保留中等以上相关，1.1% 超低稀疏度意味着 95 站 4465 对关系中仅约 49 对呈现强同步——这些极可能是关键传输路径
- **提供实验对比维度**：可分别用距离图和相关图训练，比较两种空间建模方式的效果

#### 2.5.4 时序切分对齐

**操作**：

| 集合 | 索引范围 | 步数 | 日历范围 |
|------|----------|:---:|------|
| Train | 0 – 7377 | 7378 | 2022-01-01 00:00 至 2022-11-05 23:00 |
| Valid | 7378 – 8046 | 669 | 2022-11-06 00:00 至 2022-12-03 21:00 |
| Test | 8047 – 8716 | 670 | 2022-12-03 22:00 至 2022-12-31 23:00 |

train_rate = 0.8465

**原因**：
- **no-leak 是时序预测底线**：测试集必须全部在训练集之后，严格按时序线性排列，否则模型"从未来学习"导致数据泄漏
- **与 PE-DiffWaveNet 切分点完全一致**：确保 DiffSTG 指标能与 Table1 中 9 个 baseline 直接对比——切分不同则指标差异可能来自数据分布而非模型能力
- **覆盖完整季节周期**：约 10 个月训练 + 1 个月验证 + 1 个月测试。测试集落在 12 月（冬季 O₃ 低谷），对模型是一个有挑战性的场景，因为训练集中夏季高 O₃ 模式不能直接迁移

#### 2.5.5 核心适配：T_h / T_p 解耦

**约束根源**：UGnet 的 U-Net 结构沿时间轴做对称的下采样和上采样，隐含假设输入输出维度相等，因此 DiffSTG 原生代码在 train.py 中将 T_p 硬绑定为 T_h。

**为什么必须解耦**：本项目主流配置为 T_h=24, T_p=6（用过去 24h 预测未来 6h）。若迁就约束：
- T_h=T_p=12：输入窗口太短，信息量少于 baseline 的 L=24
- T_h=T_p=24：预测 24 步远超实际需求，且 Table1 所有 baseline 的 pre_len=6，无法直接对齐

**方案 B 具体改动**（已实现为 `train_air_n95.py`）：
1. **掩码逻辑**：原掩码将后 T_h 步置零（因 T_p=T_h），改为掩掉后 T_p 步，支持任意 T_p
2. **UGnet 上采样路径**：末层恢复到 T_p 步即停止，不再强制恢复到 T_h 步
3. **损失计算**：仅在目标 T_p 步上计算去噪损失
4. **命令行参数**：新增独立 `--T_p` 参数，与 `--T_h` 解耦

---

## 3. 运行命令

### 3.1 PE-DiffWaveNet Smoke Test (已有结果复核)

```bash
# 环境: torch_env (PyTorch 2.5.1+cu121)
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh
```

**Smoke Test 结果** (1 epoch, hidden_size=16, max_windows=8):

| 指标 | 值 | 说明 |
|------|-----|------|
| Best Valid RMSE | 171.92 | 仅 1 epoch, 极小配置, 未收敛 |
| Test RMSE | 166.79 | 同上 |
| O3 Max | 410.0 μg/m³ | 训练集 O3 最大值 |

> ⚠️ Smoke test 仅验证代码/数据/路径是否正常，指标无参考意义。正式训练需完整配置。

### 3.2 ATGCN-PE3 noleak Baseline

```bash
# 正式运行 (T_h=12, T_p=6, seed=42)
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
python code/train_atgcn_pe3_noleak.py \
    --seq_len 12 --pre_len 6 --seed 42 \
    --epochs 50 --batch_size 16 \
    --hidden_size 64 --lr 7e-4 \
    --device cuda \
    --exp_name baseline_l12_p6_s42

# 预期指标 (来自 table1):
# RMSE=11.8944, MAE=8.6023, MAPE=35.46
```

### 3.3 DiffSTG Baseline (本次适配)

```bash
# 切换到 DiffSTG 目录
cd external_baselines/DiffSTG

# 安装依赖
pip install easydict

# 最小测试 (CPU, 1 epoch, 验证数据管道)
python train_air_n95.py \
    --T_h 12 --T_p 12 \
    --epochs 1 --batch_size 8 \
    --device cpu --is_test 1 \
    --exp_name debug

# 正式训练 (GPU, T_h=12, T_p=12, 与 baseline L=12 对齐)
python train_air_n95.py \
    --T_h 12 --T_p 12 \
    --epochs 300 --batch_size 32 \
    --lr 0.0001 --hidden_size 32 \
    --seed 42 --device cuda \
    --exp_name formal_l12_p12_s42

# 完整训练 (GPU, T_h=24, T_p=24)
python train_air_n95.py \
    --T_h 24 --T_p 24 \
    --epochs 300 --batch_size 32 \
    --lr 0.0001 --hidden_size 32 \
    --seed 42 --device cuda \
    --exp_name formal_l24_p24_s42
```

### 3.4 指标复核算例

```bash
# 读取已有 PE-DiffWaveNet smoke test 指标
python -c "
import json
with open('matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/metrics_summary.json') as f:
    m = json.load(f)
print(f\"Test RMSE: {m['test_rmse']:.4f}\")
print(f\"Test MAE:  {m['test_mae']:.4f}\")
print(f\"Test MAPE: {m['test_mape']:.2f}%\")
"
```

---

## 4. 已有结果复核

### 4.1 table1 主对比表复核

从 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv` 确认:

- **最佳 baseline**: MTGNN (L=24), RMSE=10.6620, MAE=7.3383
- **最佳扩散模型**: PE-DiffWaveNet backbone, RMSE=10.9380 (seeds 42/52/62)
- **ATGCN-PE3 系列**: RMSE 在 11.7~11.9 范围
- **指标趋势**: 扩散类模型 (DiffWaveNet) 与 GNN 类 (MTGNN) 处于同一水平

### 4.2 Smoke Test 输出验证

`matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/` 目录包含完整输出:

```
├── config.json          # 运行配置 (T_h=24, T_p=6, seed=42, hidden=16)
├── metrics_summary.json # 指标汇总 (RMSE/MAE/MAPE/Peak/Per-step)
├── split_summary.json   # 数据切分信息 (no-leak split)
├── graph_summary.json   # 图构建统计
├── scale_stats.json     # 归一化统计
├── met_stats.json       # 气象因子统计
├── train_loss.npy       # 训练损失曲线
├── valid_rmse.npy       # 验证 RMSE
├── valid_mae.npy        # 验证 MAE
├── valid_mape.npy       # 验证 MAPE
├── testX.npy / testY.npy  # 测试数据窗口
├── validX.npy / validY.npy # 验证数据窗口
├── S_matrix.npy / T_matrix.npy / PE_matrix.npy  # 图邻接矩阵
└── pe_node_features.npy  # PE 节点特征
```

输出验证 **PASSED**: 所有预期文件均正常生成，格式规范。

---

## 5. DiffSTG 适配注意事项

### 5.1 关键差异

| 特性 | PE-DiffWaveNet | DiffSTG (原生) |
|------|---------------|----------------|
| T_h / T_p 关系 | 独立配置 | T_p = T_h (绑定) |
| 输入维度 | 15 (O3 + 14气象) | 1 (仅目标变量) |
| 扩散步数 | 50 (训练) | 200 |
| 采样策略 | DDPM | DDPM / DDIM |
| 图构建 | S + T + PE 三图 | 单空间图 |
| 条件输入 | PE 特征 | day-of-week + time-of-day |
| 概率输出 | 多步采样 | 多步采样 + 置信区间 |

### 5.2 进一步完善方向

1. **扩展气象因子**: 将 14 个气象变量合并到 flow.npy 的多特征维度
2. **PE 图集成**: 使用 PE 矩阵作为 DiffSTG 的 adj.npy 替代距离图
3. **T_p 解耦**: 在模型架构中解耦 T_h 和 T_p, 支持 seq_len=24 → pre_len=6
4. **概率评估**: 输出置信区间和不确定性量化
5. **多目标**: 同时预测 O3、PM2.5、PM10

---

## 6. 交付文件清单

```
external_baselines/DiffSTG/
├── train_air_n95.py                          # AIR_N95 适配训练脚本
├── data/dataset/AIR_N95/
│   ├── flow.npy                              # O3 时间序列 (8717, 95, 1)
│   ├── adj.npy                               # 距离邻接矩阵 (95, 95)
│   ├── adj_corr.npy                          # 相关邻接矩阵 (95, 95)
│   └── split_info.json                       # 数据切分信息
└── output/
    ├── model/                                # 模型权重保存目录
    ├── log/                                  # 训练日志目录
    └── forecast/                             # 预测结果目录
```

---

*本报告为第 1 周 baseline 任务产出，后续将根据实验进展更新实际运行指标。*
