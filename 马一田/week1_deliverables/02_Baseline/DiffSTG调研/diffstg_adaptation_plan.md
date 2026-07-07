# DiffSTG 适配方案

## 1. DiffSTG 简介

| 项目 | 内容 |
|------|------|
| 论文 | DiffSTG: Probabilistic Spatio-Temporal Graph Forecasting with Denoising Diffusion Models |
| 发表 | ACM SIGSPATIAL 2023 |
| 作者 | Wen Haomin et al. |
| 代码 | https://github.com/wenhaomin/DiffSTG |
| 许可 | MIT |
| 框架 | PyTorch |
| 依赖 | torch, easydict, nni |

### 核心思路
- 首次将 DDPM（去噪扩散概率模型）应用于时空图预测
- 非自回归框架，一次输出全部预测步长
- 去噪网络 UGnet：U-Net 结构，结合 TCN（时序卷积）+ GCN（图卷积）
- 支持 DDPM 和 DDIM 两种采样策略
- 输出多样本，可计算概率指标（CRPS, MIS）

## 2. 代码结构

```
DiffSTG/
├── train.py                          # 主入口，含参数解析、训练循环
├── algorithm/
│   ├── dataset.py                    # CleanDataset + TrafficDataset
│   └── diffstg/
│       ├── model.py                  # DiffSTG 扩散模型（DDPM/DDIM）
│       ├── ugnet.py                  # UGnet 去噪网络（U-Net + TCN + GCN）
│       └── graph_algo.py             # 图矩阵预处理（asym_adj 等）
├── data/dataset/
│   ├── AIR_GZ/                       # 41 站点空气质量数据
│   │   └── readme.txt
│   └── PEMS08/                       # 170 传感器交通数据
│       ├── flow.npy   (T,170,3)
│       └── adj.npy    (170,170)
└── utils/
    ├── eval.py                       # 评估指标（MAE, RMSE, MAPE, CRPS, MIS）
    ├── common_utils.py
    └── gpu_dispatch.py
```

## 3. 数据格式要求

### flow.npy
```
形状: (T, V, F)
 - T: 时间步数（我们: 8717 小时）
 - V: 站点数（我们: 95）
 - F: 特征数（通常 1，仅 O3 浓度）
```

加载逻辑（`dataset.py:read_data`）：
- AIR 数据集：取 `[:, :, 0]`，NaN 填 0 → `(T, V, 1)`
- 在训练集上做 Z-score 归一化

### adj.npy
```
形状: (V, V)    二值或加权邻接矩阵
```

预处理（`graph_algo.py`）：
- `load_graph_data` 会减去单位阵（去自环）：`adj - np.eye(V)`
- UGnet 使用 `asym_adj`（D⁻¹A，行归一化）
- 同时使用 A 和 Aᵀ 两个方向的支持矩阵

### 样本构造
```
每个样本: (label, feature, pos_w, pos_d)
 - label:    (T_p, V, 1)  — 未来 T_p 小时的真值
 - feature:  (T_h, V, 1)  — 过去 T_h 小时的历史值
 - pos_w:    (T_h,)       — 星期几 (0-6)
 - pos_d:    (T_h,)       — 一天内第几小时 (0-23)
```

训练时：将 feature 和 label 拼接成 `(T_h+T_p, V, 1)`，mask 掉预测部分作为条件输入，模型学习去噪还原未来部分。

## 4. 默认超参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| T_h | 12 | 输入窗口 |
| T_p | 12 | 预测步长 |
| hidden_size (d_h) | 32 | 隐藏维度 |
| N | 200 | 扩散步数 |
| sample_steps | 200 | 采样步数 |
| beta_schedule | 'quad' | 噪声调度 |
| beta_end | 0.02 | 终止噪声方差 |
| batch_size | 32 | 批大小 |
| lr | 1e-4 | 学习率 |
| epochs | 300 | 训练轮数 |
| early_stop | 10 | 早停轮数 |
| epsilon_theta | 'UGnet' | 去噪网络类型 |
| channel_multipliers | [1, 2] | U-Net 通道倍增 |
| mask_ratio | 0.0 | 历史观察的随机 mask 比例 |

## 5. 适配 N95 数据的步骤

### Step 1: 生成 flow.npy

从现有数据提取 O3 序列：

```python
import numpy as np
import pandas as pd
import os

DATA_DIR = "d:/桌面/臭氧预测资料/臭氧预测资料"
MATRIX_DIR = os.path.join(DATA_DIR, "matrix_N95")

# 方案A: 从 data_combined_m15.npy 提取第 0 列（O3）
data = np.load(os.path.join(MATRIX_DIR, "data_combined_m15.npy"))  # (8717, 95, 15)
o3_data = data[:, :, 0:1]  # (8717, 95, 1)

# NaN 填 0（与 DiffSTG AIR 处理一致）
o3_data = np.nan_to_num(o3_data, nan=0.0)

np.save("AIR_N95/flow.npy", o3_data.astype(np.float32))
print(f"flow.npy shape: {o3_data.shape}")  # (8717, 95, 1)
```

### Step 2: 生成 adj.npy

从站点经纬度构建距离图：

```python
import numpy as np
import pandas as pd

# 读取站点坐标
station_df = pd.read_excel(
    "d:/桌面/臭氧预测资料/臭氧预测资料/xlsx_N95/station_loc1.xlsx"
)

lng = station_df["经度"].values  # 95 个站点的经度
lat = station_df["纬度"].values  # 95 个站点的纬度

# 计算距离矩阵（简化：用欧氏距离近似，实际应用可用 haversine）
dlng = lng[None, :] - lng[:, None]
dlat = lat[None, :] - lat[:, None]
dist = np.sqrt(dlng**2 + dlat**2)  # (95, 95)

# 阈值高斯核: w_ij = exp(-dist²/σ²) if dist < threshold else 0
sigma = 0.5
threshold = 3.0  # 约 300km（经纬度单位粗略换算）
adj = np.exp(-dist**2 / sigma**2)
adj[dist > threshold] = 0

# 或直接用二值图：距离 < threshold 的站点相连
# adj = (dist < threshold).astype(np.float32)

# DiffSTG 代码会自行去自环
np.save("AIR_N95/adj.npy", adj.astype(np.float32))
print(f"adj.npy shape: {adj.shape}")  # (95, 95)
```

### Step 3: 添加 AIR_N95 配置

修改 DiffSTG 的 `train.py` 中 `default_config` 函数，添加：

```python
elif data == 'AIR_N95':
    config = edict({
        'data': {
            'name': 'AIR_N95',
            'data_path': 'data/dataset/AIR_N95/flow.npy',
            'spatial_adj_path': 'data/dataset/AIR_N95/adj.npy',
            'num_recent': 1,
            'points_per_hour': 1,
            'day_len': 24,
            'week_len': 7,
        },
        'model': {
            'T_p': 6,       # 预测 6 小时
            'T_h': 24,      # 输入 24 小时
            'V': 95,
            'F': 1,
            'd_h': 32,
            'N': 200,
            'sample_steps': 200,
            'channel_multipliers': [1, 2],
            'supports_len': 2,
            'epsilon_theta': 'UGnet',
            'is_label_condition': True,
            'beta_end': 0.02,
            'beta_schedule': 'quad',
            'sample_strategy': 'ddpm',
            'n_samples': 2,
        },
        'train': {
            'model_name': 'DiffSTG',
            'epoch': 300,
            'lr': 1e-4,
            'batch_size': 32,
            'wd': 1e-5,
            'early_stop': 10,
        },
        'val_start_idx': 7378,   # 与 no-leak split 一致
        'test_start_idx': 8047,  # 与 no-leak split 一致
    })
```

注意：DiffSTG 内部的 split 逻辑：
- train: `[0+T_h, val_start_idx - T_p + 1)`
- val: `[val_start_idx + T_p, test_start_idx - T_p + 1)`
- test: `[test_start_idx + T_p, total_len - T_p + 1)`

这与我们的 no-leak split 不完全一致（我们是先严格按时间切分再分别做窗口），但近似可接受。若要严格一致，需修改 `get_idx_lst` 方法。

### Step 4: 运行

```bash
# 克隆仓库
git clone https://github.com/wenhaomin/DiffSTG.git
cd DiffSTG

# 安装依赖
pip install easydict nni

# 放入数据
mkdir -p data/dataset/AIR_N95
cp /path/to/flow.npy data/dataset/AIR_N95/
cp /path/to/adj.npy data/dataset/AIR_N95/

# 运行训练（CPU 调试）
python train.py \
  --data AIR_N95 \
  --T_h 24 --T_p 6 \
  --batch_size 4 \
  --N 50 --sample_steps 50 \
  --hidden_size 16 \
  --is_train True --is_test True

# 完整训练（需要 GPU）
python train.py \
  --data AIR_N95 \
  --T_h 24 --T_p 6 \
  --batch_size 32 \
  --lr 1e-4
```

## 6. 关键风险与注意事项

| 风险 | 说明 | 应对 |
|------|------|------|
| **数据切分不一致** | DiffSTG 的 split 是简单索引切分，我们是"先切时间轴再各自做窗口" | 优先用 DiffSTG 默认方式，在报告中标注差异；或修改 `get_idx_lst` 严格适配 |
| **缺少气象因子** | DiffSTG 只用 O3 单变量（F=1），PE-DiffWaveNet 用了 m=15 | 这是 baseline 对比的正常差异；若要公平对比，PE-DiffWaveNet 也只用 O3 跑一次 |
| **GPU 需求** | 300 epoch × N=200 diffusion steps，CPU 上很慢 | CPU 调试用 N=10，正式训练需 GPU |
| **nni 依赖** | nni 是可选的超参调优工具，但 `train.py` 会 import | 可去掉 nni 导入或不使用 --nni 参数 |
| **邻接矩阵质量** | 距离阈值和 σ 的选择影响图结构 | 建议同时试距离图和 PE 相关图，选效果好的 |
| **评估指标对齐** | DiffSTG 输出 RMSE/MAE/MAPE，需确认计算方式与主表一致 | 对比 paper_assets 中 ATGCN-PE3 的指标，确认量级一致 |

## 7. 最低交付目标（PPT Slide 12）

- [x] 论文阅读与代码结构理解
- [ ] 克隆仓库，安装依赖
- [ ] 生成 AIR_N95/flow.npy 和 adj.npy
- [ ] 修改配置支持 AIR_N95 + seq_len=24 + pre_len=6 + seed=42
- [ ] 跑通训练（至少完成几个 epoch）
- [ ] 输出 RMSE, MAE, MAPE 并填入 results.csv

## 8. 调研结论

DiffSTG **适合**作为扩散类时空图 baseline：
- 与 PE-DiffWaveNet 同为扩散模型，对比有说服力
- 代码结构清晰，数据格式要求简单（flow.npy + adj.npy）
- 适配 N95 只需：生成数据文件 + 添加配置项

**工作量估算**：数据准备 0.5h + 代码适配 1h + CPU 验证 0.5h + GPU 训练 2-4h
