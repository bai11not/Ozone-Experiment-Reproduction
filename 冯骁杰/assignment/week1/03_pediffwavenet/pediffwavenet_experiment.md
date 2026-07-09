# PE-DiffWaveNet 实验报告

> **生成日期**: 2026-07-06（更新于 2026-07-09）
> **对应任务**: 第 1 周 — 数据理解和代码跑通 → PE-DiffWaveNet 实验
> **模型**: PE-DiffWaveNet (Diffusion + Permutation Entropy Graph + PE-FiLM)

---

## 1. 模型原理

PE-DiffWaveNet 是本项目自主研发的臭氧浓度时空预测模型，融合了三个核心模块：**扩散模型（Diffusion）**、**排列熵图（PE Graph）** 和 **排列熵特征调制（PE-FiLM）**。其骨干网络继承自 DiffWave（Kong et al., ICLR 2021 Oral）——一种用于音频波形生成的非自回归扩散模型，本项目将其改造适配于时空图预测任务。

### 1.1 扩散模块（DiffWave Backbone）

#### 1.1.1 扩散模型原理

扩散模型的灵感来自非平衡态热力学：一个结构化的信号可以通过反复注入微小噪声逐步变成纯噪声（前向过程），而这个过程可以反向学习——从纯噪声出发，逐步去噪，恢复出原始信号（反向过程）。

**前向扩散过程**：从真实未来 O₃ 信号出发，分 N 步逐步添加高斯噪声。每步的噪声强度参数 β_n 按二次调度从 β_1=0.0001 增长到 β_N（在 0.1–0.4 之间选择），使得前期噪声加得慢（保留信号结构）、后期噪声加得快（快速趋于纯噪声）。通过重参数化技巧，可以直接从干净信号跳到任意噪声水平：

```
x_p^n = sqrt(ᾱ_n) × x_p⁰ + sqrt(1-ᾱ_n) × ε
```

其中 ᾱ_n 是前 n 步 (1-β_i) 的累积乘积，ε 是标准高斯噪声。

**条件反向去噪过程**：训练一个神经网络 ε_θ 来逆转扩散——以当前噪声信号、噪声水平 n、历史观测 x^h 和图结构 G 作为条件，输出去噪后的信号。训练目标是最小化噪声预测误差：

```
L = E[ || ε - ε_θ(x_p^n, n | x^h, G) ||² ]
```

即：让网络学会精确猜出"被加了多少噪声"。损失同时在历史和未来部分计算，数据利用率更高。

#### 1.1.2 DiffWave 骨干架构特点

PE-DiffWaveNet 的去噪网络采用 DiffWave 架构，其核心特点：

- **非自回归生成**：一次并行生成全部预测步，不需要"预测一步 → 当作输入 → 再预测下一步"。这彻底消除了自回归模型的误差累积问题——传统 RNN 中，第 1 步的误差会传播到第 2 步，第 2 步再传播到第 3 步，越往后越不可靠
- **双向扩张卷积**：使用扩张率逐层翻倍的因果+反因果卷积（dilation = 1, 2, 4, ..., 512），感受野指数级增长。浅层捕捉几小时内的短时波动，深层捕捉数周级别的长程趋势。双向设计使得当前位置同时看到"过去"和"未来"的上下文（在去噪场景中这不违反因果性，因为整个未来序列是同时生成的）
- **扩散步嵌入**：噪声水平 n 通过正弦位置编码注入每一层，让网络知道当前处于去噪的哪个阶段——噪声大时（早期）关注全局结构的重建，噪声小时（晚期）关注局部细节的精细调整
- **跳跃连接**：每层输出汇总到最终输出层，融合了从细粒度到粗粒度的所有尺度信息，避免深层网络中的信息丢失

#### 1.1.3 为什么扩散模型适合 O₃ 预测

1. **不确定性量化**：确定性模型只输出一个值（"明天 14:00 O₃ = 85.3 μg/m³"）。扩散模型多次采样可得均值和置信区间（"85.3 ± 12.5 μg/m³"），这对空气质量预警至关重要——决策者需要知道预测的可信度
2. **多模态分布捕捉**：O₃ 浓度受气象条件突变影响（如冷锋过境），可能存在多种可能的未来轨迹。扩散模型天然适合建模这种"一对多"映射
3. **训练稳定**：仅需简单的 L2 损失（预测噪声 vs 真实噪声），不需要 GAN 的对抗训练（易模式崩溃）或 VAE 的变分下界优化

### 1.2 排列熵图（PE Graph）

#### 1.2.1 什么是排列熵

排列熵（Permutation Entropy，PE）由 Bandt 和 Pompe 于 2002 年（Physical Review Letters）提出，是一种衡量时间序列**复杂度/不可预测性**的方法。其核心思想是：分析连续数据点的**排序模式**（而非具体数值）在序列中出现的频率。

计算过程（以嵌入维度 m=3 为例）：

1. **取窗口**：从 O₃ 时间序列中取出长度为 m=3 的连续片段，如 (1.3, 6.1, 2.5)
2. **排顺序**：将片段内值从小到大排序为 (1.3, 2.5, 6.1)，记录原始位置的排列模式——"最小-最大-中间"，编码为 (0, 2, 1)
3. **统计分布**：滑动窗口遍历整个序列，统计 m! = 6 种排列模式各自的出现频率 p(π_1), ..., p(π_6)
4. **计算熵**：H = -Σ p(π_i) × log₂(p(π_i))，归一化到 [0, 1] 范围

**直观理解**：
- PE ≈ 0：序列高度规律（如单调递增），排列模式固定不变 → 易预测
- PE ≈ 1：序列高度随机（如白噪声），各种模式均匀出现 → 难预测

#### 1.2.2 PE 在 O₃ 预测中的应用

本项目对每个站点的全年 O₃ 序列（8717 小时），用 m=3、滑动窗口步长=168 小时（一周）计算 PE 值，得到每个站点的 PE 特征向量（维度 6）。

**PE 值的站点含义**：
- **低 PE 站点**（如郊区背景站，PE ≈ 0.3–0.5）：O₃ 变化较规律，主要受太阳辐射日周期控制，可预测性高
- **高 PE 站点**（如城市交通站，PE ≈ 0.7–0.9）：O₃ 变化复杂，受交通排放、光化学反应、局地传输的多重影响，可预测性低

#### 1.2.3 PE 图构建

基于两两站点 PE 特征的相似度构建邻接矩阵：

```
A_PE(i,j) = exp(-|PE_i - PE_j|² / (2σ²))
```

两个站点 PE 值越接近（预测难度相似），连接权重越大。这构建了第三种图结构，与另外两种图互补：

| 图 | 非零元素 | 构建方法 | 物理含义 |
|------|:---:|------|------|
| S 矩阵（空间图） | 691 | 基于站点经纬度距离 | "这两个站点空间上很近" |
| T 矩阵（时间相关图） | 1570 | 基于 O₃ 时间序列皮尔逊相关 | "这两个站点 O₃ 变化同步" |
| PE 矩阵（复杂度图） | 317 | 基于排列熵特征相似度 | "这两个站点的复杂度相似" |

三种图以特定方式融合输入模型，让模型同时利用空间邻近、时间同步和复杂度相似三种不同的站点关系。

### 1.3 PE-FiLM（排列熵特征调制）

#### 1.3.1 FiLM 原理

FiLM（Feature-wise Linear Modulation）由 Perez 等人于 AAAI 2018 提出，是一种通用的神经网络条件注入方法。核心公式极简：

```
FiLM(特征) = γ × 特征 + β
```

关键设计：γ（缩放因子）和 β（平移因子）不是固定参数，而是从条件信息（如 PE 特征）通过一个可学习的小型 MLP **动态生成**的。每个站点因其 PE 特征不同而获得不同的 (γ, β)，从而实现**站点自适应处理**。

#### 1.3.2 PE-FiLM 工作流程

1. 对每个站点 i，计算 PE 特征向量 f_i（维度 6：m=3 排列熵及其变体）
2. 用一个小的 MLP 将 f_i 映射为缩放因子 γ_i 和平移因子 β_i
3. 在 DiffWave 骨干的每一层扩张卷积后，对输出特征逐通道应用：输出 = γ_i × 卷积输出 + β_i
4. 由于每个站点获得的 (γ_i, β_i) 不同，同一模型对不同站点自动采用不同的处理策略

**物理直觉**：
- 低 PE 站点（规律）：γ 接近 1, β 接近 0 → 近乎不变，网络正常处理
- 高 PE 站点（复杂）：γ 可能放大捕捉高频波动的通道、β 可能抑制对噪声敏感的通道 → 自适应调整

#### 1.3.3 为什么 PE-FiLM 适合 O₃ 预测

1. **站点异质性**：95 个站点覆盖城区/郊区/背景站，O₃ 生成机制和变化模式差异显著。PE-FiLM 让单个模型自适应处理所有站点，无需为每站训练独立模型
2. **数据效率**：PE 特征相当于"站点身份证"，告诉模型该站的行为模式，模型据此调整处理策略
3. **可解释性**：PE 值直接反映站点预测难度，可据此分层评估模型表现（对应 Table3 的 PE 分层统计——低/中/高 PE 站各自的表现）

---

## 2. 数据准备与图构建

### 2.1 输入特征与数据切分

**输入特征**：维度 m=15，包含 1 个目标变量（O₃）和 14 个气象因子：

| 类别 | 变量 | 说明 |
|------|------|------|
| 目标 | O₃ | 臭氧浓度（μg/m³），预测目标 |
| 气象 | blh, d2m, fsr, kx, sp, ssr, ssrd, t2m, tcc, tcwv, tp, u10, v10, zust | 边界层高度、2m 温度、地表辐射、风速分量等 |

所有气象因子通过 `met_raw_aligned_cache.npz` 预缓存加载（避免每次从 365 个原始 CSV 文件读取 6.8GB 数据），与 O₃ 数据对齐后形成 (8717, 95, 15) 的组合数据张量。

**No-Leak 数据切分**：训练/验证/测试严格按时序线性排列，归一化 Scaler 仅用训练集拟合：

| 集合 | 索引范围 | 步数 | 时间范围 |
|------|----------|:---:|------|
| Train | 0 – 7377 | 7378 | 2022-01-01 00:00 至 2022-11-05 23:00 |
| Valid | 7378 – 8046 | 669 | 2022-11-06 00:00 至 2022-12-03 21:00 |
| Test | 8047 – 8716 | 670 | 2022-12-03 22:00 至 2022-12-31 23:00 |

train_rate = 0.8465。切分点与所有 baseline 完全一致，确保对比公平。

### 2.2 三图并行构建

#### S 矩阵（空间图）

基于 95 个站点的经纬度坐标，用 Haversine 公式计算站间球面距离，再通过阈值或高斯核转化为邻接权重。非零元素 691 个，稀疏度 7.7%。物理含义："站点 A 和站点 B 空间上有多近"。

#### T 矩阵（时间相关图）

基于两两站点全年 O₃ 时间序列的皮尔逊相关系数，保留超过阈值的连接。非零元素 1570 个，稀疏度 17.4%。物理含义："站点 A 和站点 B 的 O₃ 变化是否同步"。

#### PE 矩阵（复杂度图）

基于两两站点排列熵特征的欧氏距离，经高斯核转化为相似度。非零元素 317 个，稀疏度 3.5%。物理含义："站点 A 和站点 B 的 O₃ 变化复杂度是否相似"。

---

## 3. Smoke Test 运行验证

### 3.1 运行命令

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh
```

等效 Python 命令:

```bash
python -u code/train_pediffwavenet_noleak.py \
  --data_dir . \
  --device cpu \
  --exp_name student_smoke_cpu \
  --pre_len 6 \
  --seq_len 24 \
  --seed 42 \
  --N_node 95 \
  --m 15 \
  --hidden_size 16 \
  --batch_size 2 \
  --eval_batch_size 2 \
  --lr 7e-4 \
  --epochs 1 \
  --patience 1 \
  --diff_steps 3 \
  --inference_steps 2 \
  --num_samples 1 \
  --eval_inference_steps 2 \
  --eval_num_samples 1 \
  --use_diffusion 1 \
  --use_pe_graph 1 \
  --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 \
  --max_valid_windows 4 \
  --max_test_windows 4 \
  --save_predictions 0 \
  --save_train_arrays 0 \
  --use_met_cache 1 \
  --amp 0 \
  --log_interval 1
```

### 3.2 Smoke Test 配置解析

| 参数 | Smoke Test 值 | 正式训练值 | 设计原因 |
|------|:---:|:---:|------|
| `epochs` | 1 | 120 | 仅验证一个 epoch 能完整走完 |
| `hidden_size` | 16 | 64 | 极小隐藏层，前向/反向几乎瞬时完成 |
| `batch_size` | 2 | 32 | 极小 batch，内存占用极低 |
| `diff_steps` | 3 | 50 | 极少扩散步数，训练近乎瞬间 |
| `inference_steps` | 2 | 50 | 推理加速到仅 2 步 |
| `max_train_windows` | 8 | ~7000+ | 仅用 8 个窗口，数据加载忽略不计 |
| `max_valid_windows` | 4 | ~600+ | 验证仅用 4 个窗口 |
| `max_test_windows` | 4 | ~600+ | 测试仅用 4 个窗口 |
| `device` | cpu | cuda | 无需 GPU，任何机器可运行 |

> **Smoke test 的设计目的**：用最极端的极小配置，以最快速度验证代码无语法错误、数据路径正确、输出目录正常。**指标本身无参考意义**——就像测试一辆车在 1 米轨道上开 1 秒，只能证明所有部件能动，完全不能代表真实性能。

### 3.3 Smoke Test 输出验证

输出目录: `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/`

#### 核心输出文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `config.json` | ✅ | 完整运行配置 (78 个字段) |
| `split_summary.json` | ✅ | no-leak 数据切分信息 |
| `metrics_summary.json` | ✅ | 完整指标 + per-step metrics |
| `graph_summary.json` | ✅ | S/T/PE 三图构建统计 |
| `met_stats.json` | ✅ | 14 个气象因子 min/max |
| `scale_stats.json` | ✅ | O₃ 归一化统计 |
| `train_loss.npy` | ✅ | 训练损失: 1.7658 |
| `valid_rmse.npy` | ✅ | 验证 RMSE: 171.92 |
| `valid_mae.npy` | ✅ | 验证 MAE: 170.01 |
| `valid_mape.npy` | ✅ | 验证 MAPE: 902.24% |
| `testX.npy` | ✅ | 测试输入 (4, 24, 95, 15) |
| `testY.npy` | ✅ | 测试目标 (4, 6, 95) |
| `validX.npy` | ✅ | 验证输入 (4, 24, 95, 15) |
| `validY.npy` | ✅ | 验证目标 (4, 6, 95) |
| `S_matrix.npy` | ✅ | 空间邻接矩阵 (95, 95) |
| `T_matrix.npy` | ✅ | 时间相关矩阵 (95, 95) |
| `PE_matrix.npy` | ✅ | PE 图邻接矩阵 (95, 95) |
| `pe_node_features.npy` | ✅ | PE 节点特征 (95, 6) |

#### 数据切分 (no-leak)

| 集合 | 索引范围 | 步数 | 时间范围 |
|------|----------|------|----------|
| Train | 0 ~ 7377 | 7,378 | 2022-01-01 00:00 ~ 2022-11-05 23:00 |
| Valid | 7378 ~ 8046 | 669 | 2022-11-06 00:00 ~ 2022-12-03 21:00 |
| Test | 8047 ~ 8716 | 670 | 2022-12-03 22:00 ~ 2022-12-31 23:00 |

#### 图构建统计

| 图 | 非零元素 | 说明 |
|-----|----------|------|
| S (空间图) | 691 | 基于站点经纬度距离 |
| T (时间图) | 1,570 | 基于 O₃ 时间序列相关性 |
| PE (PE图) | 317 | 基于 Permutation Entropy 特征相似度 |

### 3.4 Smoke Test 结果

| 指标 | 值 | 备注 |
|------|-----|------|
| Epoch | 1 | — |
| Train Loss | 1.7658 | — |
| Valid RMSE | 171.92 | 未收敛 |
| Valid MAE | 170.01 | 未收敛 |
| Valid MAPE | 902.24% | 未收敛 |
| Test RMSE | 166.79 | 未收敛 |
| Test MAE | 164.68 | 未收敛 |
| Test MAPE | 848.02% | 未收敛 |
| O₃ Max | 410.0 μg/m³ | 训练集 O₃ 最大值 |

> ⚠️ 指标极差是**预期行为**：仅训练 1 epoch，hidden_size=16, diff_steps=3, 8 个训练窗口。Smoke test 的唯一目的是验证管道畅通。

---

## 4. 第 1 周实验操作

> **第 1 周目标**：验证代码/数据/路径管道畅通，确认模型能正常训练和输出，而非获取有参考价值的预测指标。正式的全量实验（GPU 多 seed / 变体 / 消融）留给第 2 周执行。

第 1 周实际执行的操作包括以下三项：

---

### 4.1 Smoke Test — 管道验证（已执行 ✅）

**目的**：用极小配置（1 epoch, CPU）快速验证代码无语法错误、数据路径正确、输出文件完整。Smoke test 是第 1 周最先执行的操作，因为只有确认管道畅通后，后续调试和正式训练才有意义。

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh
```

> 等效 Python 命令和完整参数见第 3 节。Smoke test 的 18 个输出文件验证结果见 [3.3 节](#33-smoke-test-输出验证)。

**Smoke test 输出验证通过项**：

- [x] 18 个输出文件全部正常生成
- [x] `config.json` — 78 个参数字段完整
- [x] `split_summary.json` — no-leak 切分正确 (train_rate=0.8465)
- [x] `metrics_summary.json` — 包含 RMSE/MAE/MAPE/Peak/Per-step
- [x] `graph_summary.json` — S(691) / T(1570) / PE(317) 非零元素合理
- [x] `S_matrix.npy` / `T_matrix.npy` / `PE_matrix.npy` — shape = (95, 95)
- [x] `testX.npy` / `testY.npy` — 测试数据窗口 shape 正确

---

### 4.2 小配置调试 — 验证收敛趋势（已执行 ✅）

**目的**：Smoke test 只跑 1 个 epoch，无法观察 loss 是否在下降。小配置调试用 3 个 epoch 在 CPU 上验证：训练损失是否递减？验证指标是否在改善？确认模型在"学习"而非"随机输出"后，再投递 GPU 任务。

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 \
  MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=student_debug_cpu \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

| 参数 | 小配置调试值 | 与 Smoke test 的差异 | 设计原因 |
|------|:---:|------|------|
| `EPOCHS` | 3 | ↑ 从 1 增到 3 | 足够观察 loss 的下降趋势（2-3 个点即可判断方向） |
| `MAX_TRAIN_WINDOWS` | 64 | ↑ 从 8 增到 64 | 更多训练数据，让收敛趋势更明显 |
| `MAX_VALID_WINDOWS` | 32 | ↑ 从 4 增到 32 | 验证集更大，验证指标更稳定 |
| `MAX_TEST_WINDOWS` | 32 | ↑ 从 4 增到 32 | 测试集更大，最终指标稍微有参考性 |
| `HIDDEN_SIZE` | 16 | 不变 | 保持极小网络，CPU 上快速完成 |
| `DEVICE` | cpu | 不变 | 无需 GPU |

**调试检查清单**：

- [x] 训练损失是否随 epoch 递减？（预期：3 个 epoch 内 loss 从 ~1.8 降到 ~1.5 左右）
- [x] 验证 RMSE 是否在改善？（预期：趋势向下，即使绝对值仍然很高）
- [x] 无 NaN / Inf 出现在 loss 或梯度中
- [x] 输出目录和日志文件正常生成
- [x] `metrics_summary.json` 正常写入、可读取

---

### 4.3 输出验证 — 确认产出规范（已执行 ✅）

**目的**：在 Smoke test 和小配置调试运行完成后，逐项检查输出目录中的文件，确保后续所有实验（第 2-3 周批量 GPU 运行）的输出格式一致、字段完整。

**验证清单**（每次实验完成后均需检查）：

- [x] `config.json` — 配置正确，参数完整（78 个字段）
- [x] `split_summary.json` — no-leak 切分正确 (train_rate=0.8465)
- [x] `metrics_summary.json` — 包含 RMSE/MAE/MAPE/Peak/Per-step
- [x] `graph_summary.json` — S/T/PE 图非零元素合理
- [x] `train_loss.npy` — 训练损失递减趋势确认
- [x] `valid_rmse.npy` — 验证 RMSE 收敛趋势确认
- [x] `valid_mae.npy` — 验证 MAE 收敛趋势确认
- [x] `valid_mape.npy` — 验证 MAPE 收敛趋势确认
- [x] `testX.npy` / `testY.npy` — 测试数据 shape 正确
- [x] `validX.npy` / `validY.npy` — 验证数据 shape 正确
- [x] `S_matrix.npy` / `T_matrix.npy` / `PE_matrix.npy` — 图矩阵 shape = (95, 95)
- [x] `met_stats.json` — 14 个气象因子统计正常
- [x] `scale_stats.json` — O₃ 归一化统计正常
- [x] `pe_node_features.npy` — PE 节点特征 shape = (95, 6)

---

## 5. 第 2 周实验计划（命令已录制，待执行）

> 以下命令已在第 1 周完成设计和录制（写入 `commands.sh`），将在第 2 周 GPU 环境上正式执行。此处保留完整的实验设计说明，供第 2 周直接使用。

### 5.1 主实验（多 Seed）

**目的**：在标准配置下，用 3 个不同随机种子获取稳定、可比的性能指标。

```bash
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"

# seed=42
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# seed=52
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s52 \
  bash scripts/run_train_pediffwavenet.sh 6 24 52

# seed=62
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s62 \
  bash scripts/run_train_pediffwavenet.sh 6 24 62
```

**为什么需要 3 个 seed**：

1. **消除随机性**：神经网络初始化、dropout、扩散采样都涉及随机性。单次运行结果可能偏高或偏低，无法判断模型真实水平
2. **结果报告格式**：指标以"均值 ± 标准差"形式报告（如 Table1 中 PE-DiffWaveNet backbone 的 RMSE = 10.9380 ± 0.3353），这是学术论文的标准做法
3. **可复现性**：固定 seed 确保他人能精确复现结果。3 个 seed 也足以估计方差而不消耗过多 GPU 资源

预期输出目录:
- `matrix_N95_PEDiffWaveNet_noleak_student_pedw_p6_s{seed}/`
- `weights_N95/weights_pediffwavenet_noleak_student_pedw_p6_s{seed}/`

### 5.2 变体实验（不同窗口和步长）

**目的**：系统探索输入窗口长度和预测步长对模型性能的影响，找出最优配置。

#### 5.2.1 不同预测步长

```bash
# pre_len=1,3,12,24 — 固定 seq_len=24, seed=42
for P in 1 3 12 24; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p${P} \
    bash scripts/run_train_pediffwavenet.sh ${P} 24 42
done
```

| pre_len | 含义 | 难度 | 原因 |
|:---:|------|:---:|------|
| 1 | 预测未来 1 小时 | 最容易 | 短期外推，O₃ 在 1 小时内变化不大 |
| 3 | 预测未来 3 小时 | 中等 | 中等时间跨度 |
| 6 | 预测未来 6 小时 | 较难 | **标准配置**，主对比目标 |
| 12 | 预测未来 12 小时 | 难 | 覆盖半天变化周期 |
| 24 | 预测未来 24 小时 | 最难 | 完整日周期，不确定性显著增大 |

**为什么 pre_len 越大越难**：O₃ 的演变是非线性的——气象条件的微小变化可能在数小时后导致截然不同的 O₃ 浓度。预测步越长，不确定性累积越大。per-step 分析（Step1 RMSE vs Step6 RMSE）可以量化误差随步长的增长速率。

#### 5.2.2 不同输入窗口

```bash
# seq_len=12,48 — 固定 pre_len=6, seed=42
for L in 12 48; do
  DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_l${L} \
    bash scripts/run_train_pediffwavenet.sh 6 ${L} 42
done
```

| seq_len | 含义 | 信息量 | 潜在问题 |
|:---:|------|:---:|------|
| 12 | 用过去 12 小时 | 最少 | 无法完整捕捉前一日同时段的日周期模式 |
| 24 | 用过去 24 小时 | 充足 | **标准配置**，覆盖一个完整日周期 |
| 48 | 用过去 48 小时 | 最多 | 两天前的信息可能与当前 O₃ 相关性很弱，引入噪声 |

**为什么不是 seq_len 越大越好**：24 小时覆盖完整日周期（O₃ 有强日变化规律），这是最有信息量的窗口。48 小时引入两天前的数据，相关性可能已衰减到接近随机水平，徒增计算开销。

### 5.3 消融实验（Ablation Study）

**目的**：逐一"关掉"模型的某个模块来验证每个模块是否真的贡献了性能提升。这是判断模型创新点有效性的金标准。

```bash
# 无扩散 (USE_DIFFUSION=0) — 验证扩散模块的贡献
USE_DIFFUSION=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nodiff \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE 图 (USE_PE_GRAPH=0) — 验证 PE 图的贡献
USE_PE_GRAPH=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nopegraph \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# 无 PE FiLM (USE_PE_FILM=0) — 验证 PE FiLM 的贡献
USE_PE_FILM=0 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_nopefilm \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# PE shuffle (PE_SHUFFLE_SEED=52) — 验证 PE 特征信息的特异性
PE_SHUFFLE_SEED=52 DEVICE=cuda EPOCHS=120 EXP_NAME=student_ablation_peshuffle \
  bash scripts/run_train_pediffwavenet.sh 6 24 42
```

| 消融变体 | 关闭了哪个模块 | 要验证的科学问题 |
|------|------|------|
| **无扩散** | 扩散去噪模块 | 扩散的概率建模是否比直接确定性回归更好？去掉扩散后模型退化为一个普通的 WaveNet 式回归器 |
| **无 PE 图** | PE 复杂度图 | 基于站点复杂度的图是否比纯空间图 + 时序相关图提供额外有用信息？ |
| **无 PE FiLM** | PE 特征调制 | 站点自适应调制是否有助于处理 95 个站点的异质性？去掉后所有站点被同等对待 |
| **PE shuffle** | PE 特征 → 随机打乱 | PE 特征的贡献是否真的来自复杂度信息？将北京站的 PE 特征随机赋给天津站，如果指标不变则说明 PE 特征的信息未被模型真正利用 |

**消融实验的推理逻辑**：如果关掉某个模块后指标显著变差（如 RMSE 上升 >0.3），则证明该模块是关键创新。如果关掉后指标几乎不变，则该模块可能是冗余的。PE shuffle 是特别的——它不改变模型结构和参数量，只改变 PE 特征与站点的对应关系，是最干净的对照实验。

### 5.4 第 2 周实验汇总

| 实验类型 | 配置数 | 预计 GPU 时间 |
|------|:---:|------|
| 主实验（多 seed） | 3 | 3 × ~4h = 12h |
| 变体-预测步长 | 4 | 4 × ~4h = 16h |
| 变体-输入窗口 | 2 | 2 × ~4h = 8h |
| 消融实验 | 4 | 4 × ~4h = 16h |
| **合计** | **13** | **~52 GPU 小时** |

> ⚠️ 第 1 周仅执行 Smoke test（1 epoch CPU）和小配置调试（3 epochs CPU），以上 GPU 训练任务均计划在第 2 周执行。

---

## 6. 核心指标说明与预期范围

### 6.1 核心指标说明

| 指标 | 全称 | 含义 |
|------|------|------|
| RMSE | Root Mean Square Error | 均方根误差（μg/m³），对大误差敏感 |
| MAE | Mean Absolute Error | 平均绝对误差（μg/m³），对所有误差等权 |
| MAPE | Mean Absolute Percentage Error | 相对误差百分比（%） |
| Peak RMSE | — | 仅在高 O₃ 浓度区间（>阈值）计算 RMSE，评估对污染事件峰值的捕捉能力 |
| Step6 RMSE | — | 仅在第 6 预测步（最远预测步）计算 RMSE，评估长期预测的可靠性 |

### 6.2 预期指标范围

正式训练（120 epochs, T_h=24, T_p=6, GPU）的预期表现：

| 指标 | 预期范围 | 对比：MTGNN L=24（最佳 baseline） |
|------|:---:|:---:|
| Test RMSE | 10.5 – 12.0 | 10.6620 |
| Test MAE | 7.0 – 8.5 | 7.3383 |
| Test MAPE | 29% – 32% | 29.99% |
| Peak RMSE | 13.0 – 14.5 | 13.3536 |
| Step6 RMSE | 13.0 – 14.0 | 13.1806 |

---

## 7. 环境依赖

```bash
# 核心依赖
torch >= 2.0
numpy
pandas
scipy
geopy
openpyxl

# 安装命令
pip install torch numpy pandas scipy geopy openpyxl
```

当前可用环境: `torch_env` (PyTorch 2.5.1+cu121, CUDA available)

---

## 8. 首次可复现实验命令 (第 1 周实际执行)

> 以下为第 1 周在 Linux 服务器上实际执行的命令序列，按执行顺序记录。Step 1-2 为 Smoke test 管道验证，Step 3 为小配置收敛趋势验证，Step 4-5 为输出检查。GPU 正式训练命令已录制在 `commands.sh` 中，将在第 2 周执行。

```bash
# ============================================================
# 环境: Linux, CUDA GPU 服务器
# 项目路径: /home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet
# Python 环境: torch_env (PyTorch 2.5.1+cu121)
# ============================================================

# Step 1: Smoke test — 极简配置验证管道 (CPU, 1 epoch)
cd "/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet"
bash scripts/run_smoke_cpu.sh

# Step 2: 检查 Smoke test 输出是否完整
echo "=== Smoke Test 输出文件列表 ==="
ls matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/

echo ""
echo "=== 数据切分信息 ==="
cat matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/split_summary.json

echo ""
echo "=== 图构建信息 ==="
cat matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/graph_summary.json

echo ""
echo "=== 指标汇总 ==="
cat matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/metrics_summary.json

# Step 3: 小配置调试 — 验证收敛趋势 (CPU, 3 epochs)
DEVICE=cpu EPOCHS=3 HIDDEN_SIZE=16 \
  MAX_TRAIN_WINDOWS=64 MAX_VALID_WINDOWS=32 MAX_TEST_WINDOWS=32 \
  EXP_NAME=student_debug_cpu \
  bash scripts/run_train_pediffwavenet.sh 6 24 42

# Step 4: 检查小配置调试输出
echo "=== 调试输出文件列表 ==="
ls matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/

echo ""
echo "=== 训练损失 (验证收敛趋势) ==="
python -c "
import numpy as np
loss = np.load('matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/train_loss.npy')
print(f'Train loss 序列: {loss}')
print(f'Loss 递减: {loss[-1] < loss[0]}')
"

echo ""
echo "=== 验证指标 ==="
python -c "
import json
with open('matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/metrics_summary.json') as f:
    m = json.load(f)
print(f\"Test RMSE: {m['test_rmse']:.4f}\")
print(f\"Test MAE:  {m['test_mae']:.4f}\")
print(f\"Test MAPE: {m['test_mape']:.2f}%\")
"

# Step 5: 读取指标（Smoke test 结果）
python -c "
import json
with open('matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/metrics_summary.json') as f:
    m = json.load(f)
print(f'Smoke Test — RMSE: {m[\"test_rmse\"]:.4f}, MAE: {m[\"test_mae\"]:.4f}, MAPE: {m[\"test_mape\"]:.2f}%')
"
```

**关键输出确认**：

| 检查项 | Smoke test | 小配置调试 |
|------|:---:|:---:|
| 18 个输出文件 | ✅ 全部生成 | ✅ 全部生成 |
| `config.json` 78 字段 | ✅ 完整 | ✅ 完整 |
| `split_summary.json` | ✅ train_rate=0.8465 | ✅ 同 |
| `graph_summary.json` | ✅ S=691, T=1570, PE=317 | ✅ 同 |
| `metrics_summary.json` | ✅ 可读取 | ✅ 可读取 |
| Train loss 递减 | N/A (仅 1 epoch) | ✅ 确认下降 |
| 无 NaN / Inf | ✅ | ✅ |
| 权重文件 | N/A (仅 1 epoch 不保存) | N/A (3 epoch 不保存) |

---

*本报告为第 1 周 PE-DiffWaveNet 实验产出。第 1 周实际执行：Smoke test（管道验证）+ 小配置调试（收敛趋势验证）+ 输出检查 + 命令录制。正式 GPU 训练（主实验/变体/消融共 13 个任务）计划在第 2 周执行。*
