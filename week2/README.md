# Week 2: 批量消融实验

## 实验目标

对 **PE-DiffWaveNet** 模型进行系统性的消融实验，通过控制变量法评估扩散模型、PE 图结构、PE FiLM 等组件对臭氧预测性能的影响。

## 实验矩阵

共 **64 组实验**，6 个二值参数的全因子设计 (2⁶ = 64)：

| 参数 | 含义 | 取值 A | 取值 B |
|------|------|--------|--------|
| `seed` | 随机种子 | 42 | 52 |
| `seq_len` | 输入历史窗口长度 (小时) | 12 | 24 |
| `pre_len` | 预测步长 (小时) | 6 | 3 |
| `use_diffusion` | 是否使用扩散模型 | 0 (无扩散) | 1 (有扩散) |
| `use_pe_graph` | 是否使用 PE 图结构 | 0 (无) | 1 (有) |
| `use_pe_film` | 是否使用 PE FiLM | 0 (无) | 1 (有) |

### 固定参数（所有实验共用）

| 参数 | 值 | 说明 |
|------|-----|------|
| `--N_node` | 95 | 臭氧站点数 |
| `--m` | 15 | 输入特征维度 |
| `--hidden_size` | 64 | 隐藏层维度 |
| `--batch_size` | 16 | 批次大小 |
| `--lr` | 7e-4 | 学习率 |
| `--epochs` | 120 | 最大训练轮数 |
| `--patience` | 15 | 早停耐心值 |
| `--diff_steps` | 50 | 扩散步数 |
| `--inference_steps` | 50 | 推理采样步数 |
| `--num_samples` | 3 | 评估采样数 |
| `--use_adaptive_adj` | 1 | 使用自适应邻接矩阵 |
| `--pe_source` | train | PE 特征来源 |
| `--amp` | 1 | 混合精度训练 |

### 数据

- 数据集: 95 个站点的臭氧数据 (`matrix_N95/data.npy`)
- 气象数据: 自动加载
- 训练/验证/测试划分: 无泄漏划分 (noleak split)

---

## 四人分工方案

采用**裂区设计 (split-plot design)**：每人固定 `seed` 和 `USE_DIFFUSION`，在其内部遍历剩余 4 个参数的全部组合 (2⁴ = 16 组)。

### 分工总览

| 人员 | 固定 seed | 固定 USE_DIFFUSION | 实验数 | 结果目录 |
|------|-----------|---------------------|--------|----------|
| **A** | 42 | 0 (无扩散) | 16 | `results/person_A_seed42_nodiff/` |
| **B** | 42 | 1 (有扩散) | 16 | `results/person_B_seed42_diff/` |
| **C** | 52 | 0 (无扩散) | 16 | `results/person_C_seed52_nodiff/` |
| **D** | 52 | 1 (有扩散) | 16 | `results/person_D_seed52_diff/` |

### 为什么这样分工？

1. **seed** 和 **USE_DIFFUSION** 是最高层参数，影响最大
2. 每人固定这 2 个参数后，内部的 16 个实验覆盖了 (seq_len, pre_len, USE_PE_GRAPH, USE_PE_FILM) 的完整 2×2×2×2 组合
3. 4 人的结果合并后，可以在任意维度上对比分析
4. 每人工作量均等（16 组实验）

---

## 每人具体实验清单

### Person A: seed=42, USE_DIFFUSION=0

| # | seq_len | pre_len | PE_GRAPH | PE_FILM | 实验标签 |
|---|---------|---------|----------|---------|----------|
| A01 | 12 | 6 | 0 | 0 | `s42-d0-l12-p6-g0-f0` |
| A02 | 12 | 6 | 0 | 1 | `s42-d0-l12-p6-g0-f1` |
| A03 | 12 | 6 | 1 | 0 | `s42-d0-l12-p6-g1-f0` |
| A04 | 12 | 6 | 1 | 1 | `s42-d0-l12-p6-g1-f1` |
| A05 | 12 | 3 | 0 | 0 | `s42-d0-l12-p3-g0-f0` |
| A06 | 12 | 3 | 0 | 1 | `s42-d0-l12-p3-g0-f1` |
| A07 | 12 | 3 | 1 | 0 | `s42-d0-l12-p3-g1-f0` |
| A08 | 12 | 3 | 1 | 1 | `s42-d0-l12-p3-g1-f1` |
| A09 | 24 | 6 | 0 | 0 | `s42-d0-l24-p6-g0-f0` |
| A10 | 24 | 6 | 0 | 1 | `s42-d0-l24-p6-g0-f1` |
| A11 | 24 | 6 | 1 | 0 | `s42-d0-l24-p6-g1-f0` |
| A12 | 24 | 6 | 1 | 1 | `s42-d0-l24-p6-g1-f1` |
| A13 | 24 | 3 | 0 | 0 | `s42-d0-l24-p3-g0-f0` |
| A14 | 24 | 3 | 0 | 1 | `s42-d0-l24-p3-g0-f1` |
| A15 | 24 | 3 | 1 | 0 | `s42-d0-l24-p3-g1-f0` |
| A16 | 24 | 3 | 1 | 1 | `s42-d0-l24-p3-g1-f1` |

### Person B: seed=42, USE_DIFFUSION=1

| # | seq_len | pre_len | PE_GRAPH | PE_FILM | 实验标签 |
|---|---------|---------|----------|---------|----------|
| B01 | 12 | 6 | 0 | 0 | `s42-d1-l12-p6-g0-f0` |
| B02 | 12 | 6 | 0 | 1 | `s42-d1-l12-p6-g0-f1` |
| B03 | 12 | 6 | 1 | 0 | `s42-d1-l12-p6-g1-f0` |
| B04 | 12 | 6 | 1 | 1 | `s42-d1-l12-p6-g1-f1` |
| B05 | 12 | 3 | 0 | 0 | `s42-d1-l12-p3-g0-f0` |
| B06 | 12 | 3 | 0 | 1 | `s42-d1-l12-p3-g0-f1` |
| B07 | 12 | 3 | 1 | 0 | `s42-d1-l12-p3-g1-f0` |
| B08 | 12 | 3 | 1 | 1 | `s42-d1-l12-p3-g1-f1` |
| B09 | 24 | 6 | 0 | 0 | `s42-d1-l24-p6-g0-f0` |
| B10 | 24 | 6 | 0 | 1 | `s42-d1-l24-p6-g0-f1` |
| B11 | 24 | 6 | 1 | 0 | `s42-d1-l24-p6-g1-f0` |
| B12 | 24 | 6 | 1 | 1 | `s42-d1-l24-p6-g1-f1` |
| B13 | 24 | 3 | 0 | 0 | `s42-d1-l24-p3-g0-f0` |
| B14 | 24 | 3 | 0 | 1 | `s42-d1-l24-p3-g0-f1` |
| B15 | 24 | 3 | 1 | 0 | `s42-d1-l24-p3-g1-f0` |
| B16 | 24 | 3 | 1 | 1 | `s42-d1-l24-p3-g1-f1` |

### Person C: seed=52, USE_DIFFUSION=0

| # | seq_len | pre_len | PE_GRAPH | PE_FILM | 实验标签 |
|---|---------|---------|----------|---------|----------|
| C01 | 12 | 6 | 0 | 0 | `s52-d0-l12-p6-g0-f0` |
| C02 | 12 | 6 | 0 | 1 | `s52-d0-l12-p6-g0-f1` |
| C03 | 12 | 6 | 1 | 0 | `s52-d0-l12-p6-g1-f0` |
| C04 | 12 | 6 | 1 | 1 | `s52-d0-l12-p6-g1-f1` |
| C05 | 12 | 3 | 0 | 0 | `s52-d0-l12-p3-g0-f0` |
| C06 | 12 | 3 | 0 | 1 | `s52-d0-l12-p3-g0-f1` |
| C07 | 12 | 3 | 1 | 0 | `s52-d0-l12-p3-g1-f0` |
| C08 | 12 | 3 | 1 | 1 | `s52-d0-l12-p3-g1-f1` |
| C09 | 24 | 6 | 0 | 0 | `s52-d0-l24-p6-g0-f0` |
| C10 | 24 | 6 | 0 | 1 | `s52-d0-l24-p6-g0-f1` |
| C11 | 24 | 6 | 1 | 0 | `s52-d0-l24-p6-g1-f0` |
| C12 | 24 | 6 | 1 | 1 | `s52-d0-l24-p6-g1-f1` |
| C13 | 24 | 3 | 0 | 0 | `s52-d0-l24-p3-g0-f0` |
| C14 | 24 | 3 | 0 | 1 | `s52-d0-l24-p3-g0-f1` |
| C15 | 24 | 3 | 1 | 0 | `s52-d0-l24-p3-g1-f0` |
| C16 | 24 | 3 | 1 | 1 | `s52-d0-l24-p3-g1-f1` |

### Person D: seed=52, USE_DIFFUSION=1

| # | seq_len | pre_len | PE_GRAPH | PE_FILM | 实验标签 |
|---|---------|---------|----------|---------|----------|
| D01 | 12 | 6 | 0 | 0 | `s52-d1-l12-p6-g0-f0` |
| D02 | 12 | 6 | 0 | 1 | `s52-d1-l12-p6-g0-f1` |
| D03 | 12 | 6 | 1 | 0 | `s52-d1-l12-p6-g1-f0` |
| D04 | 12 | 6 | 1 | 1 | `s52-d1-l12-p6-g1-f1` |
| D05 | 12 | 3 | 0 | 0 | `s52-d1-l12-p3-g0-f0` |
| D06 | 12 | 3 | 0 | 1 | `s52-d1-l12-p3-g0-f1` |
| D07 | 12 | 3 | 1 | 0 | `s52-d1-l12-p3-g1-f0` |
| D08 | 12 | 3 | 1 | 1 | `s52-d1-l12-p3-g1-f1` |
| D09 | 24 | 6 | 0 | 0 | `s52-d1-l24-p6-g0-f0` |
| D10 | 24 | 6 | 0 | 1 | `s52-d1-l24-p6-g0-f1` |
| D11 | 24 | 6 | 1 | 0 | `s52-d1-l24-p6-g1-f0` |
| D12 | 24 | 6 | 1 | 1 | `s52-d1-l24-p6-g1-f1` |
| D13 | 24 | 3 | 0 | 0 | `s52-d1-l24-p3-g0-f0` |
| D14 | 24 | 3 | 0 | 1 | `s52-d1-l24-p3-g0-f1` |
| D15 | 24 | 3 | 1 | 0 | `s52-d1-l24-p3-g1-f0` |
| D16 | 24 | 3 | 1 | 1 | `s52-d1-l24-p3-g1-f1` |

---

## 文件结构说明

```
week2/
├── README.md                          ← 本文件（实验总方案）
├── scripts/
│   ├── run_single_experiment.ps1      ← Windows 单次实验运行脚本
│   ├── run_person_experiments.ps1     ← 批量运行某人全部16组实验
│   └── experiment_matrix.csv          ← 全部64组实验的参数矩阵
├── results/
│   ├── person_A_seed42_nodiff/        ← A的结果 (seed=42, 无扩散)
│   │   ├── A01/                       ← 每组实验: 存放 metrics_summary.json 等
│   │   ├── A02/
│   │   └── ... (共16个子目录)
│   ├── person_B_seed42_diff/          ← B的结果 (seed=42, 有扩散)
│   ├── person_C_seed52_nodiff/        ← C的结果 (seed=52, 无扩散)
│   └── person_D_seed52_diff/          ← D的结果 (seed=52, 有扩散)
├── logs/                              ← 汇总训练日志（可选, 从 output 目录复制）
├── models/                            ← 汇总最优模型权重（可选, 从 weights 目录复制）
├── metrics/
│   └── week2_summary.csv              ← 汇总指标表（所有人结果合并）
└── summary/
    └── analysis_template.md           ← 结果分析模板

# PE-DiffWaveNet 的实际输出目录（在 臭氧预测资料 下）:
臭氧预测资料/
├── matrix_N95_PEDiffWaveNet_noleak_{exp_name}/  ← 每组实验输出
│   ├── metrics_summary.json           ← 核心: 测试集 RMSE/MAE/MAPE
│   ├── config.json                    ← 实验配置快照
│   ├── train_loss.npy                 ← 训练损失曲线
│   ├── valid_rmse.npy / valid_mae.npy ← 验证集指标
│   ├── test_predictions.npy           ← 测试集预测值
│   ├── test_targets.npy               ← 测试集真实值
│   └── ...
└── weights_N95/weights_pediffwavenet_noleak_{exp_name}/  ← 模型权重
    ├── best_ema.pt                    ← 最佳 EMA 权重
    └── last.pt                        ← 最后轮次权重
```

> **重要**: 每组实验完成后，请将 `metrics_summary.json` 和 `config.json` 复制到 `week2/results/` 对应目录下。

---

## 实验执行流程

### 1. 环境准备（每人必须做）

代码位于 `臭氧预测资料/code/train_pediffwavenet_noleak.py`，已支持所有 6 个参数，无需修改代码。

```powershell
# 克隆仓库
git clone <仓库地址>
cd 时空数据

# 激活 Python 环境（需要 Python 3.8+, PyTorch 1.10+）
# 如果在 Windows 上使用 conda:
conda activate <环境名>

# 如果在 WSL/Linux 上:
source .venv/bin/activate
```

### 2. 每人操作步骤

**推荐方式：使用提供的批量运行脚本**

```powershell
# 进入 week2 目录
cd week2

# 运行自己分配的实验组（以 Person A 为例）
.\scripts\run_person_experiments.ps1 -Person A
```

**手动方式：逐组运行**

```powershell
# 设置环境变量
$env:PYTHONPATH = "d:\时空数据\臭氧预测资料\code;$env:PYTHONPATH"

# 运行单组实验（以 Person A 第 1 组为例）
python -u "d:\时空数据\臭氧预测资料\code\train_pediffwavenet_noleak.py" `
    --data_dir "d:\时空数据\臭氧预测资料" `
    --device cuda `
    --exp_name "A01_s42-d0-l12-p6-g0-f0" `
    --seed 42 `
    --seq_len 12 `
    --pre_len 6 `
    --use_diffusion 0 `
    --use_pe_graph 0 `
    --use_pe_film 0 `
    --N_node 95 `
    --m 15 `
    --hidden_size 64 `
    --batch_size 16 `
    --eval_batch_size 16 `
    --lr 7e-4 `
    --epochs 120 `
    --patience 15 `
    --diff_steps 50 `
    --inference_steps 50 `
    --num_samples 3 `
    --use_adaptive_adj 1 `
    --pe_source train `
    --amp 1 `
    --save_predictions 1 `
    --use_met_cache 1
```

### 3. 每次实验必须记录

| 项目 | 说明 |
|------|------|
| 命令 | 完整运行命令 |
| seed | 随机种子值 |
| seq_len / pre_len | 输入窗口 / 预测步长 |
| USE_DIFFUSION | 是否使用扩散 (0/1) |
| USE_PE_GRAPH | 是否使用 PE 图 (0/1) |
| USE_PE_FILM | 是否使用 PE FiLM (0/1) |
| 输出目录 | 日志和模型存放路径 |
| RMSE | 最终测试集 RMSE |
| MAE | 最终测试集 MAE |
| MAPE | 最终测试集 MAPE (%) |
| 失败原因 | 如实验异常，记录错误日志 |

### 4. 结果提交

每人完成后将结果 Push 到自己的目录：

```
git add week2/results/person_X_XXX/
git commit -m "Person X: 完成16组实验"
git push origin master
```

---

## 实验标签命名规则

格式: `s{seed}-d{diff}-l{seq_len}-p{pre_len}-g{graph}-f{film}`

| 字段 | 含义 | 取值 |
|------|------|------|
| `s` | seed | 42, 52 |
| `d` | USE_DIFFUSION | 0, 1 |
| `l` | seq_len (T_h) | 12, 24 |
| `p` | pre_len (T_p) | 6, 3 |
| `g` | USE_PE_GRAPH | 0, 1 |
| `f` | USE_PE_FILM | 0, 1 |

示例: `s42-d1-l24-p3-g1-f0` 表示 seed=42, 有扩散, seq_len=24, pre_len=3, 有PE图, 无PE_FiLM

---

## 分析维度（合并后可做）

1. **扩散 vs 无扩散**: 固定其他参数，比较 d=0 vs d=1
2. **seq_len 影响**: 固定其他参数，比较 l=12 vs l=24
3. **pre_len 影响**: 固定其他参数，比较 p=6 vs p=3
4. **PE Graph 贡献**: 固定其他参数，比较 g=0 vs g=1
5. **PE FiLM 贡献**: 固定其他参数，比较 f=0 vs f=1
6. **种子稳定性**: 相同配置下 seed=42 vs seed=52
7. **交互效应**: 如 diffusion × pre_len, graph × film 等