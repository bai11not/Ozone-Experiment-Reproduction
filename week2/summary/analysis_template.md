# Week 2 实验结果汇总分析模板

## 一、数据汇总

将 4 人的 `person_X_summary.csv` 合并后进行分析。

### 合并命令 (PowerShell)

```powershell
cd week2
Get-Content results\person_A_seed42_nodiff\person_A_summary.csv,
          results\person_B_seed42_diff\person_B_summary.csv,
          results\person_C_seed52_nodiff\person_C_summary.csv,
          results\person_D_seed52_diff\person_D_summary.csv |
    Select-Object -Skip 1 |  # 跳过每个文件的 header
    Set-Content metrics\week2_summary.csv
```

---

## 二、分析维度

### 2.1 扩散模型的影响 (use_diffusion)

**对比方法**: 固定 seed, seq_len, pre_len, pe_graph, pe_film，比较 use_diffusion=0 vs use_diffusion=1

| seed | seq_len | pre_len | pe_graph | pe_film | RMSE(d=0) | RMSE(d=1) | ΔRMSE | 结论 |
|------|---------|---------|----------|---------|-----------|-----------|-------|------|
| 42 | 12 | 6 | 0 | 0 | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | ... | ... | |

**预期结论**: 扩散模型是否显著降低 RMSE？在哪些配置下收益最大？

### 2.2 输入窗口的影响 (seq_len)

**对比方法**: 固定其他参数，比较 seq_len=12 vs seq_len=24

| seed | pre_len | diffusion | pe_graph | pe_film | RMSE(l=12) | RMSE(l=24) | ΔRMSE | 结论 |
|------|---------|-----------|----------|---------|------------|------------|-------|------|
| 42 | 6 | 0 | 0 | 0 | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | ... | ... | |

### 2.3 预测步长的影响 (pre_len)

**对比方法**: 固定其他参数，比较 pre_len=6 vs pre_len=3

| seed | seq_len | diffusion | pe_graph | pe_film | RMSE(p=6) | RMSE(p=3) | 增幅 | 结论 |
|------|---------|-----------|----------|---------|-----------|-----------|------|------|
| 42 | 12 | 0 | 0 | 0 | ? | ? | ? | |
| ... | ... | ... | ... | ... | ... | ... | ... | |

### 2.4 PE 图结构的影响 (use_pe_graph)

**对比方法**: 固定其他参数，比较 use_pe_graph=0 vs use_pe_graph=1

### 2.5 PE FiLM 的影响 (use_pe_film)

**对比方法**: 固定其他参数，比较 use_pe_film=0 vs use_pe_film=1

### 2.6 种子稳定性

**对比方法**: 相同配置下 seed=42 vs seed=52

| 配置 | RMSE(s=42) | RMSE(s=52) | 差异 | 稳定？ |
|------|-----------|-----------|------|--------|
| d=1,l=24,p=3,g=1,f=1 | ? | ? | ? | |
| ... | ... | ... | ... | |

---

## 三、交互效应分析

### 3.1 Diffusion × PreLen

| pre_len | RMSE(d=0) | RMSE(d=1) | 改善 |
|---------|-----------|-----------|------|
| 6 | ? | ? | ? |
| 3 | ? | ? | ? |

**问题**: 扩散模型在长步预测时是否更有优势？

### 3.2 PE Graph × PE FiLM

| pe_graph | pe_film | RMSE |
|----------|---------|------|
| 0 | 0 | ? |
| 0 | 1 | ? |
| 1 | 0 | ? |
| 1 | 1 | ? |

**问题**: PE Graph 和 PE FiLM 是互补还是重叠？

### 3.3 SeqLen × Diffusion

**问题**: 更长输入窗口 + 扩散是否带来额外收益？

---

## 四、最佳配置推荐

综合 64 组实验结果，找出：

1. **最优配置**: 最低 RMSE 的参数组合
2. **最简配置**: RMSE 在最优 5% 内、参数最少的组合
3. **效率配置**: 训练/推理最快且 RMSE 可接受的组合

---

## 五、失败实验分析

1. 哪些参数组合导致训练失败？
2. 失败原因分类（数值不稳定/OOM/收敛问题）
3. 是否有参数组合无法工作？

---

## 六、可视化建议

1. 6 个参数的主效应图 (main effect plot)
2. Diffusion × PreLen 交互效应图
3. 64 组实验 RMSE 排序条形图
4. 种子稳定性散点图 (s=42 vs s=52)
5. 消融瀑布图 (从全配置逐步移除各组件的 RMSE 变化)