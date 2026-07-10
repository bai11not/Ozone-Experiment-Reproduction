# Week 2 消融实验结果分析模板

## 一、数据汇总

合并 4 人的 `person_X_summary.csv`：

```bash
cd week2
head -1 results/person_A_seed42_full_nodiff/person_A_summary.csv > metrics/week2_summary.csv
tail -n +2 results/person_A_seed42_full_nodiff/person_A_summary.csv >> metrics/week2_summary.csv
tail -n +2 results/person_B_seed42_nograph_nofilm/person_B_summary.csv >> metrics/week2_summary.csv
tail -n +2 results/person_C_seed52_full_nodiff/person_C_summary.csv >> metrics/week2_summary.csv
tail -n +2 results/person_D_seed52_nograph_nofilm/person_D_summary.csv >> metrics/week2_summary.csv
```

---

## 二、核心分析：消融对比

### 2.1 扩散模型贡献 (full vs no_diff)

固定 seed, seq_len, pre_len，对比 full(d=1) vs no_diff(d=0)

| seed | seq_len | pre_len | RMSE(full) | RMSE(no_diff) | Δ | 结论 |
|------|---------|---------|------------|---------------|-----|------|
| 42 | 12 | 6 | ? | ? | ? | |
| 42 | 12 | 3 | ? | ? | ? | |
| 42 | 24 | 6 | ? | ? | ? | |
| 42 | 24 | 3 | ? | ? | ? | |
| 52 | 12 | 6 | ? | ? | ? | |
| 52 | 12 | 3 | ? | ? | ? | |
| 52 | 24 | 6 | ? | ? | ? | |
| 52 | 24 | 3 | ? | ? | ? | |

### 2.2 PE 图结构贡献 (full vs no_graph)

| seed | seq_len | pre_len | RMSE(full) | RMSE(no_graph) | Δ | 结论 |
|------|---------|---------|------------|----------------|-----|------|
| 42 | 12 | 6 | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | |

### 2.3 PE FiLM 贡献 (full vs no_film)

| seed | seq_len | pre_len | RMSE(full) | RMSE(no_film) | Δ | 结论 |
|------|---------|---------|------------|---------------|-----|------|
| 42 | 12 | 6 | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | |

---

## 三、辅助分析

### 3.1 seq_len 影响 (l=12 vs l=24)

固定 full 模型比较:

| seed | pre_len | RMSE(l=12) | RMSE(l=24) | 结论 |
|------|---------|------------|------------|------|
| 42 | 6 | ? | ? | |
| 42 | 3 | ? | ? | |
| 52 | 6 | ? | ? | |
| 52 | 3 | ? | ? | |

### 3.2 pre_len 影响 (p=6 vs p=3)

固定 full 模型比较:

| seed | seq_len | RMSE(p=6) | RMSE(p=3) | 结论 |
|------|---------|-----------|-----------|------|
| 42 | 12 | ? | ? | |
| 42 | 24 | ? | ? | |

### 3.3 种子稳定性

相同 full 配置下 seed=42 vs seed=52:

| seq_len | pre_len | RMSE(s=42) | RMSE(s=52) | 差异 | 稳定？ |
|---------|---------|-----------|-----------|------|--------|
| 24 | 6 | ? | ? | ? | |
| 24 | 3 | ? | ? | ? | |

---

## 四、结论模板

1. **哪个组件最关键？** (按 ΔRMSE 排序: diffusion vs PE graph vs PE FiLM)
2. **长序列预测 (pre_len=6) 时，扩散模型是否更重要？**
3. **不同 seq_len 下消融效果是否一致？**
4. **推荐配置**: 是否三个组件都值得保留？