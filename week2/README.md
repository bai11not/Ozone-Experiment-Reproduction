# Week 2: 消融实验

## 实验目标

对 **PE-DiffWaveNet** 进行消融实验，验证扩散模型、PE 图结构、PE FiLM 三个组件各自的贡献。

**Baseline**: 三个组件全开 `use_diffusion=1, use_pe_graph=1, use_pe_film=1`
**消融**: 每次只关闭其中一个，其他两个保持开启

## 实验矩阵

共 **32 组实验**（2 seed × 2 seq_len × 2 pre_len × 4 消融类型）：

| 参数 | 取值 |
|------|------|
| `seed` | 42, 52 |
| `seq_len` | 12, 24 |
| `pre_len` | 6, 3 |
| 消融类型 | full / no_diff / no_graph / no_film |

### 消融类型定义

| 类型 | use_diffusion | use_pe_graph | use_pe_film | 含义 |
|------|:---:|:---:|:---:|------|
| **full** | 1 | 1 | 1 | 完整模型（baseline） |
| **no_diff** | 0 | 1 | 1 | 去掉扩散模型 |
| **no_graph** | 1 | 0 | 1 | 去掉 PE 图结构 |
| **no_film** | 1 | 1 | 0 | 去掉 PE FiLM |

### 固定参数

| 参数 | 值 |
|------|-----|
| `--N_node` | 95 |
| `--m` | 15 |
| `--hidden_size` | 64 |
| `--batch_size` | 16 |
| `--lr` | 7e-4 |
| `--epochs` | 120 |
| `--patience` | 15 |
| `--diff_steps` | 50 |
| `--inference_steps` | 50 |
| `--num_samples` | 3 |
| `--use_adaptive_adj` | 1 |
| `--pe_source` | train |
| `--amp` | 1 |

---

## 四人分工方案

每人固定 `seed`，跑 2 种消融类型 × 2 seq_len × 2 pre_len = **8 组实验**：

| 人员 | seed | 消融类型 | 实验数 |
|------|------|----------|--------|
| **A** | 42 | full + no_diff | 8 |
| **B** | 42 | no_graph + no_film | 8 |
| **C** | 52 | full + no_diff | 8 |
| **D** | 52 | no_graph + no_film | 8 |

---

## 每人具体实验清单

### Person A: seed=42, full + no_diff

| # | 消融类型 | seq_len | pre_len | d | g | f | 实验标签 |
|---|----------|---------|---------|---|---|---|----------|
| A01 | full | 12 | 6 | 1 | 1 | 1 | `s42-full-l12-p6` |
| A02 | full | 12 | 3 | 1 | 1 | 1 | `s42-full-l12-p3` |
| A03 | full | 24 | 6 | 1 | 1 | 1 | `s42-full-l24-p6` |
| A04 | full | 24 | 3 | 1 | 1 | 1 | `s42-full-l24-p3` |
| A05 | no_diff | 12 | 6 | 0 | 1 | 1 | `s42-nodiff-l12-p6` |
| A06 | no_diff | 12 | 3 | 0 | 1 | 1 | `s42-nodiff-l12-p3` |
| A07 | no_diff | 24 | 6 | 0 | 1 | 1 | `s42-nodiff-l24-p6` |
| A08 | no_diff | 24 | 3 | 0 | 1 | 1 | `s42-nodiff-l24-p3` |

### Person B: seed=42, no_graph + no_film

| # | 消融类型 | seq_len | pre_len | d | g | f | 实验标签 |
|---|----------|---------|---------|---|---|---|----------|
| B01 | no_graph | 12 | 6 | 1 | 0 | 1 | `s42-nograph-l12-p6` |
| B02 | no_graph | 12 | 3 | 1 | 0 | 1 | `s42-nograph-l12-p3` |
| B03 | no_graph | 24 | 6 | 1 | 0 | 1 | `s42-nograph-l24-p6` |
| B04 | no_graph | 24 | 3 | 1 | 0 | 1 | `s42-nograph-l24-p3` |
| B05 | no_film | 12 | 6 | 1 | 1 | 0 | `s42-nofilm-l12-p6` |
| B06 | no_film | 12 | 3 | 1 | 1 | 0 | `s42-nofilm-l12-p3` |
| B07 | no_film | 24 | 6 | 1 | 1 | 0 | `s42-nofilm-l24-p6` |
| B08 | no_film | 24 | 3 | 1 | 1 | 0 | `s42-nofilm-l24-p3` |

### Person C: seed=52, full + no_diff

| # | 消融类型 | seq_len | pre_len | d | g | f | 实验标签 |
|---|----------|---------|---------|---|---|---|----------|
| C01 | full | 12 | 6 | 1 | 1 | 1 | `s52-full-l12-p6` |
| C02 | full | 12 | 3 | 1 | 1 | 1 | `s52-full-l12-p3` |
| C03 | full | 24 | 6 | 1 | 1 | 1 | `s52-full-l24-p6` |
| C04 | full | 24 | 3 | 1 | 1 | 1 | `s52-full-l24-p3` |
| C05 | no_diff | 12 | 6 | 0 | 1 | 1 | `s52-nodiff-l12-p6` |
| C06 | no_diff | 12 | 3 | 0 | 1 | 1 | `s52-nodiff-l12-p3` |
| C07 | no_diff | 24 | 6 | 0 | 1 | 1 | `s52-nodiff-l24-p6` |
| C08 | no_diff | 24 | 3 | 0 | 1 | 1 | `s52-nodiff-l24-p3` |

### Person D: seed=52, no_graph + no_film

| # | 消融类型 | seq_len | pre_len | d | g | f | 实验标签 |
|---|----------|---------|---------|---|---|---|----------|
| D01 | no_graph | 12 | 6 | 1 | 0 | 1 | `s52-nograph-l12-p6` |
| D02 | no_graph | 12 | 3 | 1 | 0 | 1 | `s52-nograph-l12-p3` |
| D03 | no_graph | 24 | 6 | 1 | 0 | 1 | `s52-nograph-l24-p6` |
| D04 | no_graph | 24 | 3 | 1 | 0 | 1 | `s52-nograph-l24-p3` |
| D05 | no_film | 12 | 6 | 1 | 1 | 0 | `s52-nofilm-l12-p6` |
| D06 | no_film | 12 | 3 | 1 | 1 | 0 | `s52-nofilm-l12-p3` |
| D07 | no_film | 24 | 6 | 1 | 1 | 0 | `s52-nofilm-l24-p6` |
| D08 | no_film | 24 | 3 | 1 | 1 | 0 | `s52-nofilm-l24-p3` |

---

## 文件结构

```
week2/
├── README.md
├── scripts/
│   ├── run_single_experiment.sh       ← bash 单组实验
│   ├── run_person_experiments.sh      ← bash 批量 8 组
│   ├── run_single_experiment.ps1      ← PowerShell 单组
│   ├── run_person_experiments.ps1     ← PowerShell 批量
│   ├── experiment_matrix.csv          ← 32组参数矩阵
│   └── result_combine.py              ← 合并结果脚本
├── results/
│   ├── person_A_seed42_full_nodiff/
│   ├── person_B_seed42_nograph_nofilm/
│   ├── person_C_seed52_full_nodiff/
│   └── person_D_seed52_nograph_nofilm/
├── metrics/
│   └── result_recording_template.md
└── summary/
    └── analysis_template.md
```

## 使用方法

```bash
# 单组实验
cd week2
bash scripts/run_single_experiment.sh 42 12 6 1 1 1 "A01_s42-full-l12-p6"

# 批量运行（每人自己的命令）
bash scripts/run_person_experiments.sh A   # Person A
bash scripts/run_person_experiments.sh B   # Person B
bash scripts/run_person_experiments.sh C   # Person C
bash scripts/run_person_experiments.sh D   # Person D
```

## 实验标签命名规则

格式: `s{seed}-{ablation}-l{seq_len}-p{pre_len}`

| 字段 | 含义 | 取值 |
|------|------|------|
| `s` | seed | 42, 52 |
| ablation | 消融类型 | full, nodiff, nograph, nofilm |
| `l` | seq_len | 12, 24 |
| `p` | pre_len | 6, 3 |

## 每次实验必须记录

| 项目 | 说明 |
|------|------|
| 命令 | 完整运行命令 |
| seed | 42 或 52 |
| seq_len / pre_len | 12,24 / 6,3 |
| 消融类型 | full / no_diff / no_graph / no_film |
| 输出目录 | 臭氧预测资料/matrix_N95_PEDiffWaveNet_noleak_{exp_name}/ |
| test_rmse | 测试集 RMSE |
| test_mae | 测试集 MAE |
| test_mape | 测试集 MAPE |
| 失败原因 | 异常日志 |

## 分析维度

1. **扩散贡献**: full vs no_diff（相同 seed, seq_len, pre_len）
2. **PE 图贡献**: full vs no_graph
3. **PE FiLM 贡献**: full vs no_film
4. **seq_len 影响**: l=12 vs l=24
5. **pre_len 影响**: p=6 vs p=3
6. **种子稳定性**: seed=42 vs seed=52（相同配置）