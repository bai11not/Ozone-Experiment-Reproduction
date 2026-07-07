# 代码修改记录

## 修改时间：2026-07-06

### 1. 文件夹重命名

**问题**：`d:\时空数据\臭氧预测资料` 下的文件夹 `鑷哀棰勬祴璧勬枡` 是乱码

**解决方案**：重命名为 `臭氧预测资料`

**路径**：`d:\时空数据\臭氧预测资料\臭氧预测资料`（已删除嵌套，见下方说明）

---

### 2. README.md 路径修改

**文件**：[README.md](file:///d:/时空数据/臭氧预测资料/README.md)

**修改内容**：将文档中的 Linux 路径改为本地 Windows 路径

| 行号 | 修改前 | 修改后 |
|------|--------|--------|
| 28 | `/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet` | `d:\时空数据\臭氧预测资料` |
| 39 | `/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet` | `d:\时空数据\臭氧预测资料` |

---

### 3. run_smoke_cpu.sh 设备修改

**文件**：[scripts/run_smoke_cpu.sh](file:///d:/时空数据/臭氧预测资料/scripts/run_smoke_cpu.sh)

**修改内容**：将训练设备从 CPU 改为 GPU，并启用混合精度训练

| 参数 | 修改前 | 修改后 | 说明 |
|------|--------|--------|------|
| `--device` | `cpu` | `cuda` | 使用 GPU 训练 |
| `--exp_name` | `student_smoke_cpu` | `student_smoke_gpu` | 区分实验名称 |
| `--amp` | `0` | `1` | 启用混合精度加速 |

---

### 4. 环境配置建议

**虚拟环境**：在 `d:\时空数据\臭氧预测资料` 目录下使用 Python 3.11 创建虚拟环境 `.venv`

**依赖安装**：
```bash
pip install numpy pandas scikit-learn matplotlib openpyxl geopy -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

**WSL 配置**：修改 `.wslconfig` 禁用 Windows PATH 继承以避免路径转换错误

---

### 5. 运行方式

**GPU 训练（推荐）**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
bash scripts/run_smoke_cpu.sh
```

**正式训练**：
```bash
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 bash scripts/run_train_pediffwavenet.sh 6 24 42
```

---

### 6. 缺失数据统计脚本

**文件**：[白文豪/week1/数据整理/analyze_missing_data.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/analyze_missing_data.py)

**功能**：统计 `data_N95` 目录中 O3、PM2.5、PM10 的缺失情况

**统计结果**：

| 污染物 | 总记录数 | 有效记录 | 缺失记录 | 缺失率 |
|--------|----------|----------|----------|--------|
| O3 | 739,404 | 610,714 | 128,690 | 17.40% |
| PM2.5 | 739,404 | 609,772 | 129,632 | 17.53% |
| PM10 | 739,404 | 612,568 | 126,836 | 17.15% |

**关键发现**：
- 三种污染物缺失率均在 17% 左右，呈系统性缺失
- 2022年全年每一天都存在缺失数据
- 2022-07-15 缺失量最大（O3: 635, PM2.5: 660, PM10: 621）

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/数据整理/analyze_missing_data.py"
```

---

### 7. 站点位置分析脚本

**文件**：[白文豪/week1/数据整理/analyze_station_locations.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/analyze_station_locations.py)

**功能**：统计 95 个站点的城市分布和经纬度信息

**数据来源**：[xlsx_N95/station_loc1.xlsx](file:///d:/时空数据/臭氧预测资料/xlsx_N95/station_loc1.xlsx)

**城市分布**（共 20 个城市）：

| 城市 | 站点数 | 城市 | 站点数 |
|------|--------|------|--------|
| 北京 | 23 | 天津 | 15 |
| 太原 | 7 | 阳泉 | 5 |
| 张家口 | 4 | 承德 | 4 |
| 济南 | 4 | 朔州 | 4 |
| 石家庄 | 3 | 廊坊 | 3 |
| 沧州 | 3 | 呼和浩特 | 3 |
| 德州 | 3 | 乌兰察布 | 3 |
| 鹤壁 | 3 | 唐山 | 2 |
| 秦皇岛 | 2 | 保定 | 2 |
| 忻州 | 1 | 大同 | 1 |

**经纬度范围**：
- 经度：111.5968°E ~ 119.6105°E
- 纬度：35.6822°N ~ 41.0385°N
- 平均经度：115.6370°E
- 平均纬度：39.1953°N
- 站点密度：2.21 个/度²

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/数据整理/analyze_station_locations.py"
```

---

### 8. 污染物时间序列绘图脚本

**文件**：[白文豪/week1/数据整理/plot_time_series.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/plot_time_series.py)

**功能**：绘制 O3、PM2.5、PM10 的日平均浓度时间序列图（含7日滚动平均）

**数据来源**：[data_N95/](file:///d:/时空数据/臭氧预测资料/data_N95) 目录下的 CSV 文件

**输出**：
- 图像文件：`白文豪/week1/output/pollutants_time_series.png`
- 统计摘要：各污染物的平均值、最大值、最小值、标准差及对应日期

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/数据整理/plot_time_series.py"
```

---

### 9. 数据说明文档

**文件**：[数据说明.md](file:///d:/时空数据/臭氧预测资料/数据说明.md)

**功能**：数据集完整说明文档，包含数据概述、目录结构、站点信息、污染物数据、预处理说明、使用建议等

**内容结构**：
1. 数据集概述（数据来源、时间范围、覆盖站点）
2. 数据目录结构
3. 站点信息（城市分布、经纬度分布、空间特点）
4. 污染物数据（数据格式、缺失统计、时间序列统计、季节性特征）
5. 数据预处理说明
6. 使用建议（缺失处理、季节性分析、空间分析）
7. 分析脚本说明

---

## 修改时间：2026-07-07

### 10. README.md 移动到根目录

**文件**：[README.md](file:///d:/时空数据/README.md)

**修改内容**：将 `臭氧预测资料/臭氧预测资料/README.md` 移动到项目根目录 `d:\时空数据\README.md`

**目的**：让 GitHub 仓库首页直接显示项目说明文档

---

### 11. Baseline 评估脚本

**文件**：[run_baseline_evaluation.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/baseline/run_baseline_evaluation.py)

**功能**：实现4种 baseline 模型的训练和评估

**Baseline 模型**：

| 模型 | 说明 |
|------|------|
| Persistence | 持续预测，使用最后一个时间步的值 |
| Historical Mean | 历史均值预测，使用输入序列的均值 |
| GRU Baseline | 基于 GRU 的时空预测模型 |
| Linear Regression | 线性回归模型 |

**评估指标**：RMSE、MAE、MAPE、Peak_RMSE、Step6_RMSE

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/baseline/run_baseline_evaluation.py"
```

**结果输出**：`白文豪/week1/output/baseline_results.csv`

---

### 12. Baseline 结果汇总脚本

**文件**：[baseline_summary.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/baseline/baseline_summary.py)

**功能**：将 baseline 结果与主表 `table1_main_raw_comparison.csv` 对齐

**转换逻辑**：将归一化 scale 的指标乘以 max_value 转换为真实 scale

**输出文件**：
- `baseline_aligned_with_main_table.csv` - 与主表对齐的 baseline 结果
- `combined_comparison_table.csv` - 合并后的完整对比表

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/baseline/baseline_summary.py"
```

---

### 13. Baseline 运行命令记录

**文件**：[baseline_run_commands.md](file:///d:/时空数据/臭氧预测资料/白文豪/week1/baseline/baseline_run_commands.md)

**功能**：记录 baseline 运行命令和结果汇总

**包含内容**：
- 主表已有 baseline 确认（MTGNN、Graph WaveNet、AGCRN、DCRNN）
- 新增 baseline 运行命令
- baseline 结果表格（归一化 scale 和真实 scale）
- 结果文件位置说明
- DiffSTG 适配说明

---

### 14. Baseline 评估结果（真实 scale）

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE |
|--------|------|-----|------|-----------|------------|
| Persistence (L=12) | 4.76 | 3.18 | 95.12% | 5.73 | 6.39 |
| Historical Mean (L=12) | 5.82 | 4.65 | 189.38% | 7.90 | 6.36 |
| GRU Baseline | 3.48 | 2.57 | 92.68% | 4.47 | 4.43 |
| Linear Regression | 4.58 | 3.49 | 131.33% | 5.22 | 5.69 |

---

### 15. 主表已有 Baseline 确认

主表 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv` 包含：

| Method | RMSE | MAE | MAPE |
|--------|------|-----|------|
| MTGNN (L=24) | 10.66 | 7.34 | 29.99% |
| MTGNN (L=12) | 10.80 | 7.35 | 30.50% |
| Graph WaveNet (L=12) | 11.54 | 7.80 | 33.60% |
| AGCRN (L=12) | 11.69 | 8.21 | 34.78% |
| DCRNN | 12.28 | 8.51 | 36.46% |

---

### 16. 脚本路径修复

**原因**：删除嵌套文件夹后，相对路径 `../data_N95` 失效

**修改文件**：
- [plot_time_series.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/plot_time_series.py)
- [analyze_missing_data.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/analyze_missing_data.py)
- [analyze_station_locations.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/数据整理/analyze_station_locations.py)

**修改内容**：将路径从 `../data_N95` 改为 `../../../data_N95`

---

### 17. PE-DiffWaveNet 实验脚本

**目录**：`白文豪/week1/PE-DiffWaveNet 实验/`

**文件列表**：
- [run_pe_diffwavenet_experiment.sh](file:///d:/时空数据/臭氧预测资料/白文豪/week1/PE-DiffWaveNet 实验/run_pe_diffwavenet_experiment.sh) - 实验运行脚本（3个epoch）
- [verify_experiment_output.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/PE-DiffWaveNet 实验/verify_experiment_output.py) - 输出验证脚本
- [experiment_run_commands.md](file:///d:/时空数据/臭氧预测资料/白文豪/week1/PE-DiffWaveNet 实验/experiment_run_commands.md) - 运行命令记录

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
bash "白文豪/week1/PE-DiffWaveNet 实验/run_pe_diffwavenet_experiment.sh"
```

**验证输出**：
```bash
python3 "白文豪/week1/PE-DiffWaveNet 实验/verify_experiment_output.py"
```

**实验配置**：
- epochs: 3
- hidden_size: 16
- batch_size: 2
- seq_len: 24
- pre_len: 6
- device: cuda
- amp: 1（混合精度）

---

### 18. 结果整理脚本

**目录**：`白文豪/week1/结果整理/`

**文件列表**：
- [consolidate_results.py](file:///d:/时空数据/臭氧预测资料/白文豪/week1/结果整理/consolidate_results.py) - 统一结果整理脚本

**输出文件**（位于 `白文豪/week1/结果整理/output/`）：
- `unified_results_table.csv` - 统一结果表（合并主表、baseline、实验结果）
- `metrics_template.csv` - 指标模板
- `chart_naming_convention.md` - 图表命名规范
- `paper_assets_summary.json` - Paper Assets 字段摘要（JSON）
- `paper_assets_summary.md` - Paper Assets 字段摘要（Markdown）

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/结果整理/consolidate_results.py"
```

**统一指标字段**：

| 字段名 | 全称 | 单位 |
|--------|------|------|
| RMSE | Root Mean Squared Error | μg/m³ |
| MAE | Mean Absolute Error | μg/m³ |
| MAPE | Mean Absolute Percentage Error | % |
| Peak_RMSE | Peak RMSE | μg/m³ |
| Step6_RMSE | Step 6 RMSE | μg/m³ |
| Step4_6_RMSE | Steps 4-6 RMSE | μg/m³ |

---

### 19. 当前目录结构

```
臭氧预测资料/
├── .venv/                      # 虚拟环境
├── code/                       # 核心代码
│   ├── train_pediffwavenet_noleak.py
│   ├── eval_pediffwavenet_noleak.py
│   └── pediffwavenet_model.py
├── data_N95/                   # 原始污染物数据（365个CSV）
├── matrix_N95/                 # 处理后的数据矩阵
├── matrix_N95_PEDiffWaveNet_noleak_student_smoke_gpu/  # 实验输出目录
├── paper_assets_pediffwavenet/ # 论文表格
│   ├── table1_main_raw_comparison.csv
│   ├── table2_ablation.csv
│   └── table3_pe_stratified_summary.csv
├── scripts/                    # 运行脚本
│   ├── run_smoke_cpu.sh
│   └── run_train_pediffwavenet.sh
├── templates/                  # 模板文件
├── weights_N95/                # 模型权重
├── xlsx_N95/                   # 站点信息
├── 白文豪/                     # 个人工作区
│   ├── week1/
│   │   ├── 数据整理/           # 数据整理脚本
│   │   │   ├── analyze_missing_data.py
│   │   │   ├── analyze_station_locations.py
│   │   │   └── plot_time_series.py
│   │   ├── baseline/           # Baseline脚本
│   │   │   ├── run_baseline_evaluation.py
│   │   │   ├── baseline_summary.py
│   │   │   └── baseline_run_commands.md
│   │   ├── PE-DiffWaveNet 实验/ # 实验脚本
│   │   │   ├── run_pe_diffwavenet_experiment.sh
│   │   │   ├── verify_experiment_output.py
│   │   │   └── experiment_run_commands.md
│   │   ├── 结果整理/           # 结果整理脚本
│   │   │   └── consolidate_results.py
│   │   └── output/             # 输出文件
│   │       ├── baseline_results.csv
│   │       ├── baseline_aligned_with_main_table.csv
│   │       └── pollutants_time_series.png
│   └── MODIFICATIONS.md        # 修改记录
├── README.md                   # 项目说明
├── data说明.md                  # 数据说明
└── environment.yml             # 环境配置