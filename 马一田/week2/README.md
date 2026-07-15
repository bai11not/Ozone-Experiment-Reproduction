# Week 2: PE-DiffWaveNet 消融实验 — Person C (马一田)

## 实验目标

验证 **扩散模型** 对预测精度的贡献（full vs no_diff）。

## 我的实验 (Person C)

| 参数 | 值 |
|------|-----|
| seed | 52 |
| 消融类型 | full + no_diff |
| 实验数 | 8 组 |

## 实验清单

| # | 标签 | seed | seq_len | pre_len | diff | graph | film |
|---|------|------|---------|---------|:---:|:---:|:---:|
| C01 | s52-full-l12-p6 | 52 | 12 | 6 | 1 | 1 | 1 |
| C02 | s52-full-l12-p3 | 52 | 12 | 3 | 1 | 1 | 1 |
| C03 | s52-full-l24-p6 | 52 | 24 | 6 | 1 | 1 | 1 |
| C04 | s52-full-l24-p3 | 52 | 24 | 3 | 1 | 1 | 1 |
| C05 | s52-nodiff-l12-p6 | 52 | 12 | 6 | 0 | 1 | 1 |
| C06 | s52-nodiff-l12-p3 | 52 | 12 | 3 | 0 | 1 | 1 |
| C07 | s52-nodiff-l24-p6 | 52 | 24 | 6 | 0 | 1 | 1 |
| C08 | s52-nodiff-l24-p3 | 52 | 24 | 3 | 0 | 1 | 1 |

## 固定参数

N_node=95, m=15, hidden_size=64, batch_size=16, lr=7e-4, epochs=120, patience=15, diff_steps=50, inference_steps=50, num_samples=3, amp=1, device=cuda

## 目录结构

```
week2/
├── README.md
├── scripts/
│   ├── run_single_experiment.sh    ← 单组实验
│   ├── run_person_experiments.sh   ← 批量 8 组
│   ├── experiment_matrix.csv       ← 参数矩阵
│   └── result_combine.py          ← 合并结果
├── results/
│   └── person_C/                   ← 运行日志
├── metrics/
│   └── result_recording_template.md
└── summary/
    └── analysis_template.md
```

## 使用方法

```bash
# 单组 (示例: C01)
cd week2
bash scripts/run_single_experiment.sh 52 12 6 1 1 1 "s52-full-l12-p6"

# 全部 8 组
bash scripts/run_person_experiments.sh

# 合并结果
python scripts/result_combine.py
```
