# Baseline 调研报告

## 已有基线结果 (来自论文 Table 1)

| 方法 | RMSE | MAE | MAPE | Peak_RMSE |
|------|------|-----|------|-----------|
| **MTGNN (L=24)** | 10.66 | 7.34 | 29.99% | 13.35 |
| MTGNN (L=12) | 10.80 | 7.35 | 30.50% | 13.30 |
| Graph WaveNet (L=12) | 11.54 | 7.80 | 33.60% | 11.82 |
| AGCRN (L=12) | 11.69 | 8.21 | 34.78% | 15.02 |
| DCRNN | 12.28 | 8.51 | 36.46% | 15.57 |
| ATGCN-PE3 noleak | 11.89 | 8.60 | 35.46% | 16.11 |
| **PE-DiffWaveNet (ours)** | **10.94** | **7.56** | **30.79%** | **13.83** |

> 任务: 24h 输入 → 6h 预测 O3, seed=42

## 推荐新基线: DiffSTG

- **论文**: ACM SIGSPATIAL 2023, arxiv: 2301.13629
- **代码**: github.com/wenhaomin/DiffSTG (MIT license, PyTorch)
- **匹配度**: 非常贴合 — 同是扩散+时空图预测, 天然支持 95 站点场景
- **依赖**: torch, easydict, nni

### 适配计划

将本项目数据转为 DiffSTG 格式:
```python
# 生成 flow.npy: (T, N, F) = (8717, 95, 1)
o3 = np.load('matrix_N95/data.npy')  # (95, 8717)
flow = o3.T[:, :, None]  # (8717, 95, 1)
np.save('flow.npy', flow)

# 生成 adj.npy: (N, N) = (95, 95)
S = np.load('matrix_N95/S_matrix.npy')
np.save('adj.npy', S)
```

### 最低目标
1. 下载并跑通 DiffSTG 官方代码
2. 用本项目 data.npy 生成 flow.npy 和 adj.npy
3. 跑 seq_len=24, pre_len=6, seed=42
4. 输出 RMSE、MAE、MAPE 填入结果模板

### 备选方案: CSDI
- arxiv: 2107.03502, github.com/ermongroup/CSDI
- 优点是自带 PM2.5 实验, 缺点是偏向补全任务

## 消融实验矩阵 (已跑通框架)

| 实验 | 开关配置 | 预期效果 |
|------|----------|----------|
| Baseline (No-PE) | 默认 | RMSE ~10.94 |
| +PE graph+FiLM | use_pe_graph=1 use_pe_film=1 | RMSE ~10.98 |
| +PE-guided loss | pe_adaptive_loss=1 | RMSE ~11.10 |
| PE shuffle ablation | pe_shuffle_seed=52 | RMSE ~11.14 |
| PE graph only | use_pe_graph=1 use_pe_film=0 | RMSE ~11.05 |
| PE FiLM only | use_pe_graph=0 use_pe_film=1 | RMSE ~12.19 |
| No diffusion | use_diffusion=0 | TBD |
