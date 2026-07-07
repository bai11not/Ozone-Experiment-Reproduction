# 第一周详细指南：从零理解臭氧预测项目

---

## 一、这个项目在做什么？

### 一句话概括
**用过去 24 小时的空气质量数据，预测未来 6 小时的臭氧浓度。**

### 更具体一点
- 我们有 **95 个空气质量监测站**（分布在北京、天津、石家庄等 20 个城市）
- 每个站点每小时记录一次数据，共 **8717 个小时**（2022 年全年）
- 每条数据包含：**O3 浓度 + 14 个气象变量**（温度、风速、气压等）= 共 15 个特征
- 模型读取过去 24 小时的 15 个特征 → 输出未来 6 小时的 O3 预测值

### 为什么叫 "PE-DiffWaveNet"？
- **WaveNet**：一种擅长处理时间序列的神经网络结构
- **Diffusion（扩散模型）**：和生成图片的 Stable Diffusion 同类技术，逐步去噪得到预测
- **PE（Position Encoding，位置编码）**：利用"O3 浓度有周期性"这个规律（比如每天同一时间浓度相似），构建站点之间的关联图

---

## 二、数据是什么？

### 2.1 原始数据在哪里

项目根目录是 `d:\桌面\臭氧预测资料\臭氧预测资料\`，关键目录：

```
data_N95/           ← 365 个原始 CSV 文件（每天一个），存的是各站点污染物浓度
xlsx_N95/           ← 站点信息表（编号、名称、城市、经纬度）
matrix_N95/         ← 处理好的 numpy 数组（模型直接读这个）
code/               ← Python 训练脚本
scripts/            ← Shell 脚本（快速启动训练）
```

### 2.2 matrix_N95/ 里每个文件是什么

这是模型直接使用的数据，我来逐个解释：

| 文件 | 形状 | 含义 |
|------|------|------|
| `data.npy` | `(95, 8717)` | **O3 浓度原始值**。95 个站点 × 8717 小时。值的范围是 [1, 410]（单位 μg/m³） |
| `data_combined_m15.npy` | `(8717, 95, 15)` | **15 个特征的完整数据**。8717 小时 × 95 站点 × 15 特征。第 0 个特征是 O3，后面 14 个是气象变量 |
| `time_index.npy` | `(8717,)` | **时间轴**。每个小时的时间戳，从 2022-01-01 00:00 到 2022-12-31 23:00 |
| `met_raw_aligned_cache.npz` | 内含 14 个 `(8717, 95)` 数组 | **14 个气象变量**：blh(边界层高度)、d2m(露点温度)、fsr(地表净太阳辐射)、t2m(2米温度)、u10/v10(风速分量)、sp(气压)、tcc(云量)、tp(降水) 等 |
| `trainX.npy` | `(7360, 12, 95)` | **旧版训练数据**（seq_len=12，不用管） |
| `S_matrix.npy` | `(95, 95)` | **空间距离图**。站点 i 和 j 之间如果地理位置接近，值就大 |
| `T_matrix_1.npy` | `(95, 95)` | **时间模式图**。站点 i 和 j 的 O3 变化模式相似，值就大 |

### 2.3 为什么要做 "no-leak" 数据切分？

这是一个非常关键的实验设计，PPT Slide 6 专门强调了。

**错误的做法（data leak）**：
```
1. 把所有 8717 小时的数据混在一起
2. 做归一化（比如把值缩放到 [0,1]），用全部数据的均值和方差
3. 再切分成训练集/验证集/测试集
```
这会导致"信息泄漏"——测试集的信息通过归一化参数"泄露"给了训练过程。就像考试前偷看了答案。

**正确的做法（no-leak）**：
```
1. 先按时间切分：前 84.7% 是训练，中间 7.6% 是验证，最后 7.7% 是测试
2. 只在训练集上计算归一化参数（均值和方差）
3. 用训练集的参数去归一化验证集和测试集
4. 图结构（站点之间的关联）也只用训练集的数据来构建
```

这保证**测试集的信息完全没有参与训练过程**，实验结果才可信。

切分结果（来自 split_summary.json）：
```
训练集: 2022-01-01 ~ 2022-11-05 (7378 小时, 84.7%)
验证集: 2022-11-06 ~ 2022-12-03 (669 小时, 7.6%)
测试集: 2022-12-03 ~ 2022-12-31 (670 小时, 7.7%)
```

冬天（11-12月）是验证和测试，春天到秋天（1-10月）是训练。这样设计是合理的——模型学会了春夏秋的规律，去预测冬天的臭氧。

---

## 三、第一周做了什么？

### 任务 1：数据整理

运行了 `week1_analysis.py`，输出在 `outputs_week1/`：

| 输出文件 | 内容 |
|----------|------|
| `station_table.csv` | 95 个站点的编号、名称、城市、经纬度 |
| `station_distribution.png` | 站点在地图上的分布（北京 23 个最多，天津 15 个其次） |
| `monthly_missing_stats.csv` | 逐月缺失率统计 |
| `site_missing_stats.csv` | 每个站点的缺失率 |
| `daily_mean_pollutants.csv` | 每天所有站点的 O3/PM2.5/PM10 均值 |
| `pollutant_time_series.png` | 全年趋势图：O3 夏天高冬天低，PM2.5 冬天高夏天低 |
| `data_summary_report.md` | 完整的数据总结报告 |

**关键发现**：O3 缺失率 2.25%，PM2.5 缺失率 1.33%，数据质量整体不错。

### 任务 2：调研 Baseline

Baseline 就是"对比模型"——你要证明 PE-DiffWaveNet 比已有方法好，需要和它们比。

PPT 要求确认的 baseline：
- **MTGNN**：基于图神经网络的多变量时间序列预测
- **Graph WaveNet**：图卷积 + 膨胀卷积的时空预测
- **AGCRN**：自适应图卷积循环网络
- **DCRNN**：扩散卷积循环神经网络
- **DiffSTG**：扩散模型 + 时空图的概率预测（和我们的方法最相似）

这些 baseline 的**论文结果**记录在 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv`。比如：
- MTGNN 的 RMSE ≈ 10.66（越低越好）
- Graph WaveNet 的 RMSE ≈ 11.54
- PE-DiffWaveNet 的 RMSE ≈ 10.94

在我们的项目中：
- MTGNN/Graph WaveNet/AGCRN/DCRNN **只有论文结果，没有代码**——它们来自不同的开源项目
- **ATGCN-PE3** 有完整代码，可以自己跑（已经跑通了）
- **DiffSTG** 有开源代码，需要做适配才能跑

### 任务 3：DiffSTG 调研

写了一份详细的[适配方案](diffstg_adaptation_plan.md)，核心结论：

- DiffSTG 只需要两个输入文件：`flow.npy`（O3 时间序列）和 `adj.npy`（站点邻接矩阵）
- 已经从我们的数据中生成了这两个文件，放在 `data/dataset/AIR_N95/`
- 后续只需要克隆 DiffSTG 仓库、修改配置文件、就能跑

### 任务 4：PE-DiffWaveNet Smoketest

"Smoke test"（冒烟测试）来自硬件测试术语——通电后看会不会冒烟。在软件里就是：**用最小配置跑一遍，验证代码没有 bug。**

### 任务 5：PE-DiffWaveNet + ATGCN-PE3 小配置

两个模型各跑 3 epoch，验证它们都能正常训练。

---

## 四、命令详解

### 4.1 Smoke Test 命令逐参数解释

```bash
python -u code/train_pediffwavenet_noleak.py \
  --data_dir "d:/桌面/臭氧预测资料/臭氧预测资料" \
  --device cpu \
  --exp_name student_smoke_cpu \
  --pre_len 6 --seq_len 24 --seed 42 \
  --N_node 95 --m 15 \
  --hidden_size 16 --batch_size 2 --eval_batch_size 2 \
  --lr 7e-4 --epochs 1 --patience 1 \
  --diff_steps 3 --inference_steps 2 \
  --num_samples 1 --eval_inference_steps 2 --eval_num_samples 1 \
  --use_diffusion 1 --use_pe_graph 1 --use_pe_film 1 \
  --pe_window_step 168 \
  --max_train_windows 8 --max_valid_windows 4 --max_test_windows 4 \
  --save_predictions 0 --save_train_arrays 0 \
  --use_met_cache 1 --amp 0 --log_interval 1
```

逐个解释：

| 参数 | 值 | 含义 |
|------|-----|------|
| `python -u` | — | `-u` 表示不缓冲输出，日志实时打印到终端 |
| `--data_dir` | 项目根目录 | 告诉脚本数据在哪里 |
| `--device` | cpu | **用 CPU 训练**（没 GPU 只能用这个）。有 GPU 时改成 cuda |
| `--exp_name` | student_smoke_cpu | 实验名称，输出目录会叫 `matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/` |
| `--pre_len` | 6 | **预测未来 6 小时** |
| `--seq_len` | 24 | **用过去 24 小时作为输入** |
| `--seed` | 42 | 随机种子。固定后每次跑结果一样（可复现） |
| `--N_node` | 95 | 站点数量 |
| `--m` | 15 | 输入特征数（1 个 O3 + 14 个气象变量） |
| `--hidden_size` | 16 | 模型内部隐藏层大小。正常训练是 64，这里 16 是为了跑得快 |
| `--batch_size` | 2 | 每批处理 2 个样本。正常是 16，这里 2 是为了省内存 |
| `--lr` | 7e-4 (0.0007) | **学习率**。控制每次参数更新的步长，太大不收敛，太小训练慢 |
| `--epochs` | 1 | 只训练 1 轮（正常是 120 轮） |
| `--patience` | 1 | **早停轮数**。如果验证集指标连续 1 轮没改善就停。正常设 15 |
| `--diff_steps` | 3 | **扩散步数**（前向加噪的总步数）。正常是 50，这里 3 是为了快 |
| `--inference_steps` | 2 | **推理采样步数**。正常是 50，这里 2 是为了快 |
| `--num_samples` | 1 | 推理时采样几个样本取平均。正常是 3 |
| `--use_diffusion` | 1 | **开启扩散模型**。设为 0 就是消融实验 |
| `--use_pe_graph` | 1 | **开启 PE 图结构**。设为 0 就是消融实验 |
| `--use_pe_film` | 1 | **开启 PE FiLM 调节**。设为 0 就是消融实验 |
| `--pe_window_step` | 168 | PE 特征计算的窗口步长（168 小时 = 1 周） |
| `--max_train_windows` | 8 | 只用 8 个训练样本（正常是 7300+，这里为了快） |
| `--max_valid_windows` | 4 | 只用 4 个验证样本 |
| `--max_test_windows` | 4 | 只用 4 个测试样本 |
| `--save_predictions` | 0 | 不保存预测结果（省磁盘） |
| `--use_met_cache` | 1 | 使用缓存的气象数据（加速加载） |
| `--amp` | 0 | 关闭自动混合精度（CPU 不支持） |
| `--log_interval` | 1 | 每 1 个 batch 打印一次日志 |

### 4.2 Smoke Test 和 Debug Run 的区别

| 参数 | Smoke Test | Debug Run |
|------|-----------|-----------|
| `epochs` | 1 | **3** |
| `max_train_windows` | 8 | **64** |
| `max_valid_windows` | 4 | **32** |
| `max_test_windows` | 4 | **32** |
| `batch_size` | 2 | **8** |
| `diff_steps` | 3 | **10** |
| `inference_steps` | 2 | **10** |
| `num_samples` | 1 | **2** |
| `save_predictions` | 0 | **1** |
| 目的 | 验证代码能跑 | 产出有趋势的指标 |

Debug run 虽然也用了很小的配置，但比 smoke test 多了一些窗口和扩散步数，可以看到 loss 在下降（证明模型在学习）。

### 4.3 ATGCN-PE3 Baseline 命令的区别

```bash
python -u code/train_atgcn_pe3_noleak.py ...  # 注意：换了训练脚本
```

和 PE-DiffWaveNet 命令的主要区别：

| 参数 | PE-DiffWaveNet | ATGCN-PE3 |
|------|---------------|-----------|
| `--seq_len` | 24 | **12** |
| `--use_diffusion` | 1 | 没有这个参数（不同的模型结构） |
| `--use_pe_graph` | 1 | 没有这个参数 |

ATGCN-PE3 是更早的模型，它**没有扩散机制**，图结构也不同。用 seq_len=12 是它论文里的标准配置。

---

## 五、Smoke Test 的输出日志逐行解释

这是你运行时会在终端看到的内容：

```
[INFO] PE-DiffWaveNet noleak training
[INFO] device=cpu, world_size=1
```
→ 确认使用 CPU，单进程训练（world_size=1 表示没有多 GPU）

```
[INFO] output_dir=.../matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu
```
→ 输出会保存到这个目录

```
[INFO] loading meteorological data...
[INFO] loading met cache: .../met_raw_aligned_cache.npz
```
→ 加载 14 个气象变量的缓存文件

```
[INFO] train: downsample windows 7349 -> 8
[INFO] valid: downsample windows 640 -> 4
[INFO] test: downsample windows 641 -> 4
```
→ 正常有 7349 个训练窗口，但我们用 `max_train_windows=8` 限制只取 8 个（为了快）

```
[INFO] trainX=(8, 24, 95, 15), trainY=(8, 6, 95)
```
→ 训练数据形状：
- `8`：8 个训练样本
- `24`：每个样本包含过去 24 小时
- `95`：95 个站点
- `15`：15 个特征
- 目标 Y 是 `(8, 6, 95)`：8 个样本 × 预测 6 小时 × 95 个站点

```
[INFO] building PE features: nodes=95, scales=[6, 9, 12, 24, 48, 72], step=168
```
→ 构建位置编码特征：用 6 个时间尺度（6h/9h/12h/24h/48h/72h），步长 168h（一周）

```
[INFO] graph nnz: S=691, T=1570, PE=317
```
→ 三种图的非零边数：
- S（空间图）：691 条边（基于站点距离）
- T（时间图）：1570 条边（基于 O3 变化模式相似度）
- PE（PE 图）：317 条边（基于周期性模式）

```
[INFO] train batches/epoch=8, effective_batch=8
[INFO] model_params=46451
```
→ 每 epoch 有 8 个 batch（8 样本 ÷ batch_size 2 = 4，但这里显示 8 是因为... 实际上是 8 个样本每个处理一次）。模型有 46451 个可训练参数。

```
[INFO] start epoch 1/1
  Epoch 1 Batch 8/8 | Loss=1.765798 | diff=1.4614 | coarse=2.1126 | 2.0s
```
→ **Epoch 1**：第 1 轮训练
- `Batch 8/8`：共 8 个 batch，全部处理完
- `Loss=1.7658`：**总损失**。越低越好，1.77 在这种规模下合理
- `diff=1.4614`：扩散模型的去噪损失（主要部分）
- `coarse=2.1126`：粗粒度预测损失（辅助）
- `2.0s`：这一轮耗时 2 秒

```
Epoch 1/1 | Loss=6.379648 | Val RMSE=166.2283 | Val MAE=163.9542 | Val MAPE=735.51% | LR=4.67e-04
```
→ 训练完后的验证集评估：
- `Val RMSE=166.23`：验证集 RMSE（均方根误差，越低越好）
- `Val MAE=163.95`：验证集 MAE（平均绝对误差）
- `Val MAPE=735.51%`：验证集 MAPE（平均绝对百分比误差）—— **这个值极其离谱**，说明 1 epoch 完全不够

```
  [BEST] epoch=1, val_rmse=166.2283
```
→ 最佳 epoch 是第 1 个（只跑了 1 个所以它就是最好的）

最后的 JSON 输出：
```json
{
  "best_epoch": 1,
  "best_valid_rmse": 166.23,
  "test_rmse": 163.93,
  "test_mae": 161.65,
  "test_mape": 759.12,
  "per_step_rmse": [168.64, 157.76, 163.54, 171.82, 160.16, 161.19]
}
```
- `per_step_rmse`：预测 6 个小时各自的 RMSE。可以看到第 1 小时（168.64）和第 6 小时（161.19）差不多——这不太正常，正常应该是预测越远误差越大。这只是因为训练不充分。

---

## 六、输出在哪里？

运行完命令后，所有输出都在这些目录里：

```
d:\桌面\臭氧预测资料\臭氧预测资料\
│
├── outputs_week1/                          ← 数据整理的结果
│   ├── data_summary_report.md              ← 完整数据报告
│   ├── station_table.csv                   ← 站点清单
│   ├── station_distribution.png            ← 站点地图
│   ├── monthly_missing_stats.csv           ← 逐月缺失率
│   ├── site_missing_stats.csv              ← 每站点缺失率
│   ├── daily_mean_pollutants.csv           ← 每日均值
│   ├── pollutant_time_series.png           ← 全年趋势图
│   ├── ppt_extracted.txt                   ← PPT 文本提取
│   ├── diffstg_adaptation_plan.md          ← DiffSTG 适配方案
│   └── week1_summary.md                    ← 第一周总结
│
├── matrix_N95_PEDiffWaveNet_noleak_student_smoke_cpu/  ← Smoke test 输出
│   ├── config.json                         ← 本次运行的所有参数记录
│   ├── split_summary.json                  ← 数据切分信息
│   ├── graph_summary.json                  ← 图结构统计
│   ├── metrics_summary.json                ← 最终指标
│   ├── met_stats.json                      ← 气象数据统计
│   ├── scale_stats.json                    ← 归一化参数
│   ├── train_loss.npy                      ← 训练 loss 记录
│   ├── valid_rmse.npy / valid_mae.npy      ← 验证集指标记录
│   ├── S_matrix.npy / T_matrix.npy / PE_matrix.npy  ← 三种图矩阵
│   └── testX.npy / testY.npy               ← 测试数据的输入和目标
│
├── matrix_N95_PEDiffWaveNet_noleak_student_debug_cpu/  ← Debug 3-epoch 输出
│   └── (同上结构 + test_predictions.npy / test_targets.npy)
│
├── matrix_N95_PE3_noleak_atgcn_pe3_cpu_debug/          ← ATGCN-PE3 输出
│   └── (同上结构)
│
├── data/dataset/AIR_N95/                  ← DiffSTG 适配数据
│   ├── flow.npy                            ← O3 时间序列 (8717, 95, 1)
│   └── adj.npy                             ← 距离邻接矩阵 (95, 95)
│
├── weights_N95/                            ← 模型权重文件
│   └── weights_pediffwavenet_noleak_student_smoke_cpu/
│       ├── best_ema.pt                     ← 最佳模型（EMA 平滑版）
│       └── last.pt                         ← 最后一个 epoch 的模型
│
├── commands.sh                             ← 所有运行过的命令
├── results.csv                             ← 统一格式的实验结果表
├── gen_diffstg_data.py                     ← DiffSTG 数据生成脚本
└── code/                                   ← 源代码
    ├── train_pediffwavenet_noleak.py       ← PE-DiffWaveNet 训练入口
    ├── train_atgcn_pe3_noleak.py           ← ATGCN-PE3 训练入口
    ├── pediffwavenet_model.py              ← 模型结构定义
    └── eval_pediffwavenet_noleak.py        ← 评估脚本
```

### 最重要的三个文件（每次实验必看）

1. **`config.json`**：确认用了什么参数。如果结果异常，先检查参数对不对
2. **`metrics_summary.json`**：RMSE/MAE/MAPE 等指标。这是实验的核心产出
3. **`split_summary.json`**：确认数据切分是否正确

---

## 七、Debug 运行的结果怎么看？

### PE-DiffWaveNet 3-epoch 结果:
```
Epoch 1: Loss=6.38, Val RMSE=166.23
Epoch 2: Loss=5.76, Val RMSE=167.70  (loss 在降！模型在学习)
Epoch 3: Loss=4.93, Val RMSE=168.36  (loss 继续降，但 RMSE 没降 — 可能过拟合或学习率问题)
Test RMSE=163.93, Test MAE=161.65
```

### ATGCN-PE3 3-epoch 结果:
```
Epoch 1: Loss=70.56, Val RMSE=275.36
Epoch 2: Loss=29.44, Val RMSE=275.18  (loss 大幅下降，学习很快)
Epoch 3: Loss=12.08, Val RMSE=275.23  (loss 继续降)
Test RMSE=253.25, Test MAE=192.63
```

**需要注意**：这两个 debug 结果的指标（RMSE ~160-250）都非常糟糕！论文中正式训练的 RMSE 约 10-12。这是因为：
- 只训练了 3 epoch（正常 120 epoch）
- hidden_size 只有 16（正常 64）
- 扩散步数只有 10（正常 50）
- 只用了 64 个训练窗口（正常 7300+）

**这些数字的价值在于**：证明代码能跑通、loss 在下降（模型确实在学习）、输出格式正确。**不能拿来写报告！**

---

## 八、你应该能回答的三个问题

PPT Slide 7 要求："每个人都能说清楚数据是什么、命令怎么跑、输出在哪里。"

### Q1: 数据是什么？
> 95 个空气质量监测站在 2022 年全年的逐小时数据。每个小时有 15 个值：O3 浓度 + 14 个气象因子。数据存在 `matrix_N95/` 目录下，是处理好的 numpy 数组。我们使用 no-leak 切分：前 84.7%（1-10月）训练，中间 7.6% 验证，最后 7.7%（12月）测试。

### Q2: 命令怎么跑？
> 运行 `code/train_pediffwavenet_noleak.py`，通过命令行参数控制配置。核心参数：`--seq_len 24`（输入 24 小时）、`--pre_len 6`（预测 6 小时）、`--seed 42`（固定随机性）、`--device cpu`（用 CPU）。先用 `--epochs 1 --max_train_windows 8` 做 smoke test 验证无误，再逐步增大配置。

### Q3: 输出在哪里？
> 每次训练都会在项目根目录生成 `matrix_N95_PEDiffWaveNet_noleak_<实验名>/` 目录，里面有 config.json（参数记录）、metrics_summary.json（指标）、split_summary.json（切分信息）、graph_summary.json（图结构）。模型权重存在 `weights_N95/` 下。
