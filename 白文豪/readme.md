# 白文豪 - Week1 工作内容

## 目录结构

```
week1/
├── 数据整理/           # 数据整理与分析
│   ├── analyze_missing_data.py      # 缺失数据统计
│   ├── analyze_station_locations.py # 站点位置分析
│   └── plot_time_series.py          # 污染物时间序列绘图
├── baseline/           # Baseline 评估
│   ├── run_baseline_evaluation.py   # 4种baseline评估脚本
│   ├── baseline_summary.py          # 结果汇总与对齐
│   └── baseline_run_commands.md     # 运行命令记录
├── PE-DiffWaveNet 实验/ # 模型实验
│   ├── run_pe_diffwavenet_experiment.sh  # 实验运行脚本
│   ├── verify_experiment_output.py      # 输出验证脚本
│   └── experiment_run_commands.md       # 运行命令记录
├── DiffSTG/            # DiffSTG 扩散模型
│   ├── train.py                        # 训练与测试脚本
│   ├── gen_diffstg_data.py             # 数据预处理脚本
│   ├── algorithm/diffstg/model.py      # DiffSTG 模型核心
│   ├── algorithm/diffstg/ugnet.py      # UGnet 噪声预测网络
│   ├── data/dataset/AIR_N95/           # AIR_N95 数据集
│   │   ├── flow.npy                    # O3 时间序列 (T, V, 1)
│   │   └── adj.npy                     # 空间邻接矩阵 (V, V)
│   └── output/                         # 训练输出
│       ├── model/                      # 模型权重
│       ├── log/                        # 训练日志
│       └── forecast/                   # 预测结果
├── 结果整理/           # 结果整理与规范
│   ├── 整理说明.md                     # 统一结果说明文档
│   ├── Baseline/                       # Baseline 结果
│   ├── DiffSTG/                        # DiffSTG 结果
│   ├── PE-DiffWaveNet/                 # PE-DiffWaveNet 结果
│   └── unified_results_table.csv       # 统一结果表
└── output/             # 公共输出文件
    ├── baseline_results.csv
    ├── baseline_aligned_with_main_table.csv
    ├── combined_comparison_table.csv
    └── pollutants_time_series.png
```

## 完成内容

### 1. 数据整理
- O3、PM2.5、PM10 缺失统计（缺失率约17%）
- 95个站点城市分布和经纬度分析
- 污染物日平均浓度时间序列图

### 2. Baseline 评估
- Persistence（持续预测）
- Historical Mean（历史均值）
- GRU Baseline
- Linear Regression
- 结果与主表对齐（RMSE、MAE、MAPE、Peak_RMSE、Step6_RMSE）

### 3. PE-DiffWaveNet 实验
- 首次可复现实验（3个epoch小配置）
- 输出验证脚本
- 运行命令记录

### 4. DiffSTG 扩散模型实验
- AIR_N95 数据集适配（95站点、O3特征）
- 数据预处理脚本（生成 flow.npy 和 adj.npy）
- 模型训练与测试（T_h=24, T_p=6）
- 修复测试阶段内存溢出问题（GPU→CPU数据累积）
- Smoke Test 和 Full Train 实验结果

### 5. 结果整理
- 统一结果表（Baseline + DiffSTG + PE-DiffWaveNet）
- 图表命名规范
- Paper Assets 字段摘要
- 各方法结果文件详细说明

## 运行命令

```bash
# 数据整理
python3 "week1/数据整理/analyze_missing_data.py"
python3 "week1/数据整理/analyze_station_locations.py"
python3 "week1/数据整理/plot_time_series.py"

# Baseline评估
python3 "week1/baseline/run_baseline_evaluation.py"
python3 "week1/baseline/baseline_summary.py"

# PE-DiffWaveNet实验
bash "week1/PE-DiffWaveNet 实验/run_pe_diffwavenet_experiment.sh"

# DiffSTG数据预处理
python3 "week1/DiffSTG/gen_diffstg_data.py"

# DiffSTG快速测试 (Smoke Test)
python3 "week1/DiffSTG/train.py" --data AIR_N95 --T_h 24 --T_p 6 --batch_size 16 --lr 0.002 --n_epochs 50 --is_train True --is_test True

# DiffSTG完整训练
python3 "week1/DiffSTG/train.py" --data AIR_N95 --T_h 24 --T_p 6 --batch_size 32 --lr 0.0001 --n_epochs 200 --is_train True --is_test True

# 结果整理
python3 "week1/结果整理/consolidate_results.py"
```

## 依赖数据

所有脚本依赖 `../臭氧预测资料/` 目录下的数据：
- `data_N95/` - 原始污染物CSV
- `xlsx_N95/` - 站点信息（station_loc1.xlsx）
- `matrix_N95/` - 处理后数据矩阵（data_combined_m15.npy）
- `paper_assets_pediffwavenet/` - 论文表格

## DiffSTG 数据集说明

| 数据集 | 站点数 | 时间步 | 特征数 | 用途 |
|--------|--------|--------|--------|------|
| AIR_N95 | 95 | 8,717 | 1 (O3) | 臭氧预测任务 |
| PEMS08 | 170 | 17,856 | 3 | 原始论文示例（交通流量） |

**注意**：训练臭氧预测任务应使用 `AIR_N95` 数据集。