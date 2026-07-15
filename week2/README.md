# Week 2: 消融实验

## 实验目标

对 **PE-DiffWaveNet** 进行消融实验，验证扩散模型、PE 图结构、PE FiLM 三个组件各自的贡献。

**Baseline**: 三个组件全开
**消融**: 每次只关闭其中一个，其他两个保持开启

## 实验矩阵

共 **32 组实验**（2 seed × 2 seq_len × 2 pre_len × 4 消融类型）：

| 参数 | 取值 |
|------|------|
| `seed` | 42, 52 |
| `seq_len` | 12, 24 |
| `pre_len` | 6, 3 |
| 消融类型 | full / no_diff / no_pe_graph / no_pe_film |

### 消融类型定义

| 类型 | d | g | f | 含义 |
|------|---|---|---|------|
| **full** | 1 | 1 | 1 | 完整模型（baseline） |
| **no_diff** | 0 | 1 | 1 | 去掉扩散模型 |
| **no_pe_graph** | 1 | 0 | 1 | 去掉 PE 图结构 |
| **no_pe_film** | 1 | 1 | 0 | 去掉 PE FiLM |

---

## 四人分工方案

**小组编号**: g3

| 人员 | seed | 消融类型 | 实验数 |
|------|------|----------|--------|
| **A** | 42 | full + no_diff | 8 |
| **B** | 42 | no_pe_graph + no_pe_film | 8 |
| **C** | 52 | full + no_diff | 8 |
| **D** | 52 | no_pe_graph + no_pe_film | 8 |

---

## 实验命名规则

格式: `g3_pedw_{ablation?}p{pre_len}_l{seq_len}_s{seed}`

| 例子 | 含义 |
|------|------|
| `g3_pedw_p6_l24_s42` | full 模型, pre_len=6, seq_len=24, seed=42 |
| `g3_pedw_no_diff_p6_l24_s42` | 无扩散, pre_len=6, seq_len=24, seed=42 |
| `g3_pedw_no_pe_graph_p6_l24_s42` | 无 PE 图, pre_len=6, seq_len=24, seed=42 |
| `g3_pedw_no_pe_film_p6_l24_s42` | 无 PE FiLM, pre_len=6, seq_len=24, seed=42 |

---

## 每人具体实验清单

### Person A: seed=42, full + no_diff

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 |
|---|------|---------|---------|---|---|---|--------|
| A01 | full | 12 | 6 | 1 | 1 | 1 | `g3_pedw_p6_l12_s42` |
| A02 | full | 12 | 3 | 1 | 1 | 1 | `g3_pedw_p3_l12_s42` |
| A03 | full | 24 | 6 | 1 | 1 | 1 | `g3_pedw_p6_l24_s42` |
| A04 | full | 24 | 3 | 1 | 1 | 1 | `g3_pedw_p3_l24_s42` |
| A05 | no_diff | 12 | 6 | 0 | 1 | 1 | `g3_pedw_no_diff_p6_l12_s42` |
| A06 | no_diff | 12 | 3 | 0 | 1 | 1 | `g3_pedw_no_diff_p3_l12_s42` |
| A07 | no_diff | 24 | 6 | 0 | 1 | 1 | `g3_pedw_no_diff_p6_l24_s42` |
| A08 | no_diff | 24 | 3 | 0 | 1 | 1 | `g3_pedw_no_diff_p3_l24_s42` |

### Person B: seed=42, no_pe_graph + no_pe_film

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 |
|---|------|---------|---------|---|---|---|--------|
| B01 | no_pe_graph | 12 | 6 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p6_l12_s42` |
| B02 | no_pe_graph | 12 | 3 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p3_l12_s42` |
| B03 | no_pe_graph | 24 | 6 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p6_l24_s42` |
| B04 | no_pe_graph | 24 | 3 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p3_l24_s42` |
| B05 | no_pe_film | 12 | 6 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p6_l12_s42` |
| B06 | no_pe_film | 12 | 3 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p3_l12_s42` |
| B07 | no_pe_film | 24 | 6 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p6_l24_s42` |
| B08 | no_pe_film | 24 | 3 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p3_l24_s42` |

### Person C: seed=52, full + no_diff

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 |
|---|------|---------|---------|---|---|---|--------|
| C01 | full | 12 | 6 | 1 | 1 | 1 | `g3_pedw_p6_l12_s52` |
| C02 | full | 12 | 3 | 1 | 1 | 1 | `g3_pedw_p3_l12_s52` |
| C03 | full | 24 | 6 | 1 | 1 | 1 | `g3_pedw_p6_l24_s52` |
| C04 | full | 24 | 3 | 1 | 1 | 1 | `g3_pedw_p3_l24_s52` |
| C05 | no_diff | 12 | 6 | 0 | 1 | 1 | `g3_pedw_no_diff_p6_l12_s52` |
| C06 | no_diff | 12 | 3 | 0 | 1 | 1 | `g3_pedw_no_diff_p3_l12_s52` |
| C07 | no_diff | 24 | 6 | 0 | 1 | 1 | `g3_pedw_no_diff_p6_l24_s52` |
| C08 | no_diff | 24 | 3 | 0 | 1 | 1 | `g3_pedw_no_diff_p3_l24_s52` |

### Person D: seed=52, no_pe_graph + no_pe_film

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 |
|---|------|---------|---------|---|---|---|--------|
| D01 | no_pe_graph | 12 | 6 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p6_l12_s52` |
| D02 | no_pe_graph | 12 | 3 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p3_l12_s52` |
| D03 | no_pe_graph | 24 | 6 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p6_l24_s52` |
| D04 | no_pe_graph | 24 | 3 | 1 | 0 | 1 | `g3_pedw_no_pe_graph_p3_l24_s52` |
| D05 | no_pe_film | 12 | 6 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p6_l12_s52` |
| D06 | no_pe_film | 12 | 3 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p3_l12_s52` |
| D07 | no_pe_film | 24 | 6 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p6_l24_s52` |
| D08 | no_pe_film | 24 | 3 | 1 | 1 | 0 | `g3_pedw_no_pe_film_p3_l24_s52` |

---

## 使用方法

```bash
cd week2
bash scripts/run_single_experiment.sh 42 12 6 1 0 1 "g3_pedw_no_pe_graph_p6_l12_s42"  # B01

# 批量运行
bash scripts/run_person_experiments.sh A
bash scripts/run_person_experiments.sh B
bash scripts/run_person_experiments.sh C
bash scripts/run_person_experiments.sh D
```

## 结果记录

按 `臭氧预测资料/templates/experiment_result_template.csv` 格式：

| 字段 | 说明 |
|------|------|
| group | g3 |
| student | 姓名 |
| experiment_id | 如 `g3_pedw_no_pe_graph_p6_l12_s42` |
| model | pedw |
| seq_len / pre_len | 12,24 / 6,3 |
| seed | 42 或 52 |
| use_diffusion / use_pe_graph / use_pe_film | 0 或 1 |
| rmse / mae / mape | 测试集指标 |
| peak_rmse / step1_rmse / step6_rmse | 额外指标 |
| output_dir | 输出目录名 |
| log_file | 日志文件路径 |
| notes | 备注 |

## 全部实验结果汇总

| # | 人员 | 消融 | seed | seq | pre | RMSE | MAE | MAPE |
|---|------|------|------|-----|-----|------|-----|------|
| A01 | A | no_diff | 42 | 12 | 3 | 9.17 | 6.37 | 26.84 |
| A02 | A | no_diff | 42 | 24 | 3 | 8.81 | 5.90 | 25.26 |
| A03 | A | no_diff | 42 | 12 | 6 | 11.31 | 7.75 | 31.26 |
| A04 | A | no_diff | 42 | 24 | 6 | 11.04 | 7.65 | 30.14 |
| A05 | A | full | 42 | 12 | 3 | 9.11 | 6.54 | 27.99 |
| A06 | A | full | 42 | 24 | 3 | **8.62** | 5.84 | 24.00 |
| A07 | A | full | 42 | 12 | 6 | 11.59 | 8.37 | 34.50 |
| A08 | A | full | 42 | 24 | 6 | 11.07 | 7.67 | 30.88 |
| B01 | B | no_pe_graph | 42 | 12 | 6 | 11.30 | 7.99 | 33.33 |
| B02 | B | no_pe_graph | 42 | 12 | 3 | 9.05 | 6.32 | 26.51 |
| B03 | B | no_pe_graph | 42 | 24 | 6 | 11.60 | 8.51 | 35.61 |
| B04 | B | no_pe_graph | 42 | 24 | 3 | 11.50 | 9.31 | 44.61 |
| B05 | B | no_pe_film | 42 | 12 | 6 | 12.11 | 8.44 | 33.35 |
| B06 | B | no_pe_film | 42 | 12 | 3 | 10.66 | 8.26 | 34.36 |
| B07 | B | no_pe_film | 42 | 24 | 6 | 12.06 | 8.87 | 36.57 |
| B08 | B | no_pe_film | 42 | 24 | 3 | 9.39 | 6.56 | 27.64 |
| C01 | C | full | 52 | 12 | 3 | 8.80 | 6.00 | 24.89 |
| C02 | C | full | 52 | 12 | 6 | 11.43 | 8.09 | 33.48 |
| C03 | C | full | 52 | 24 | 3 | 8.80 | 6.14 | 26.21 |
| C04 | C | full | 52 | 24 | 6 | 11.01 | 7.73 | 31.97 |
| C05 | C | no_diff | 52 | 12 | 3 | 9.14 | 6.50 | 28.05 |
| C06 | C | no_diff | 52 | 12 | 6 | 11.16 | 7.76 | 32.66 |
| C07 | C | no_diff | 52 | 24 | 3 | 8.79 | 5.95 | 25.20 |
| C08 | C | no_diff | 52 | 24 | 6 | 10.88 | 7.72 | 32.06 |
| D01 | D | no_pe_graph | 52 | 12 | 6 | 11.51 | 8.34 | 34.15 |
| D02 | D | no_pe_graph | 52 | 12 | 3 | 10.40 | 7.80 | 31.11 |
| D03 | D | no_pe_graph | 52 | 24 | 6 | 11.11 | 8.01 | 31.55 |
| D04 | D | no_pe_graph | 52 | 24 | 3 | 9.75 | 7.11 | 29.89 |
| D05 | D | no_pe_film | 52 | 12 | 6 | 12.01 | 8.47 | 34.20 |
| D06 | D | no_pe_film | 52 | 12 | 3 | 10.81 | 8.29 | 35.00 |
| D07 | D | no_pe_film | 52 | 24 | 6 | 11.31 | 7.93 | 30.44 |
| D08 | D | no_pe_film | 52 | 24 | 3 | 9.82 | 7.16 | 30.40 |
| E01 | E | full | 42 | 24 | 1 | 6.11 | 4.07 | 17.52 |
| E02 | E | full | 42 | 24 | 12 | 14.47 | 10.63 | 41.89 |
| E03 | E | full | 42 | 24 | 24 | 17.42 | 12.58 | 43.69 |

> E04-E06 (seed=52) 待运行

## 分析维度

1. **扩散贡献**: full vs no_diff
2. **PE 图贡献**: full vs no_pe_graph
3. **PE FiLM 贡献**: full vs no_pe_film
4. **seq_len 影响**: l=12 vs l=24
5. **pre_len 影响**: p=1→3→6→12→24 趋势
6. **种子稳定性**: seed=42 vs seed=52