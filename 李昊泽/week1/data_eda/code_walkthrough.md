# PE-DiffWaveNet 代码走读报告

## 整体架构

```
train_pediffwavenet_noleak.py (训练主脚本)
    ├── pediffwavenet_model.py (模型定义)
    │       ├── GaussianDiffusion (cosine schedule 扩散过程)
    │       ├── SinusoidalPosEmb (时间步嵌入)
    │       ├── GraphMixProp (图扩散卷积)
    │       ├── PEDilatedGraphBlock (PE-条件门控TCN + FiLM)
    │       ├── HorizonDenoiser (去噪网络)
    │       └── PEDiffWaveNet (主模型)
    └── train_atgcn_pe3_noleak.py (数据处理 + 训练工具)
            ├── prepare_noleak_data (无泄漏数据切分)
            ├── build_graphs (构建 S/T/PE 图)
            ├── build_pe_feature_matrix (PE特征提取)
            ├── load_met_data_raw (气象数据加载)
            └── 训练工具 (EMA, DDP, metrics)
```

## 数据流 (No-Leak Protocol)

```
1. 加载 O3 数据 (95×8717) + 时间索引 + 气象缓存
2. 按时间轴切分: train(0~7378) / valid(7379~8047) / test(8048~8716)
3. ONLY in train range:
   - 拟合 O3 max (归一化参数)
   - 拟合 met min/max
   - 构建 T 图 (时间相关性)
   - 构建 PE 图 (排列熵相似性)
4. 各自 split 内部做 sliding window
5. 训练时 model(trainX) → predict trainY (6h ahead)
```

## 模型结构 (PEDiffWaveNet)

### Encoder: 
- input → Conv2D → 8×PEDilatedGraphBlock (dilations=1,2,4,8,1,2,4,8)
- 每个 Block: Gated TCN → GraphProp → PE-FiLM → skip connection
- 输出: coarse prediction + context

### Denoiser (HorizonDenoiser):
- 输入: x_t (noisy) + y_coarse + context + time_emb + horizon_emb + PE
- 2×PEDilatedGraphBlock (dilations=1,2)
- 输出: denoised x0 prediction

### 图结构 (3 + 1 adaptive):
- S (空间距离图, 阈值高斯核)
- T (时间相关性图, Pearson corr + topk)
- PE (排列熵相似性图, 自适应阈值)
- Adaptive (可学习节点嵌入)

### PE Conditioning:
- PE Graph: 用排列熵相似性构建额外的图边
- PE FiLM: 将PE特征注入每个TCN block的feature-wise线性调制

## 关键超参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| seq_len | 24 | 输入历史窗口(hours) |
| pre_len | 6 | 预测步长(hours) |
| hidden_size | 64 | 隐藏维度 |
| diff_steps | 50 | 扩散步数 |
| pe_scales | 6,9,12,24,48,72 | PE多尺度 |
| use_pe_graph | 1 | PE图开关 |
| use_pe_film | 1 | PE-FiLM调制开关 |
| use_diffusion | 1 | 扩散精炼开关 |
| coarse_weight | 0.08 | 粗预测损失权重 |
| train_rate | 0.8465 | 训练集比例 |

## 消融实验设计

```bash
# 去掉扩散 (纯确定性)
USE_DIFFUSION=0 ...

# 去掉PE图
USE_PE_GRAPH=0 ...

# 去掉PE-FiLM
USE_PE_FILM=0 ...

# PE shuffle (破坏PE语义)
PE_SHUFFLE_SEED=52 ...
```
