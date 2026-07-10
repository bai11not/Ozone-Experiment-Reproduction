# 第一周成果 — PE-DiffWaveNet 臭氧预测

**姓名：Li | 日期：2026-07-10 | 课程：2026 暑期生产实习**

---

## 文件夹说明

```
week1_result_Li/
│
├── data_eda/                      数据理解与探索性分析
│   ├── data_card.json             数据卡：95站×8717h、15特征、完整元数据
│   ├── eda_overview.png           EDA总览图（6子图：时序/分布/月变化/站点分布/个站时序/站点地图）
│   ├── eda_patterns.png           模式分析图（4子图：缺失热力图/日变化/站间相关性/周变化）
│   ├── pm_stats_report.txt        PM2.5/PM10 逐日完整缺失统计（365个CSV，2024个站点）
│   ├── code_walkthrough.md        代码架构走读（模型结构/数据流/no-leak协议/消融矩阵）
│   └── baseline_investigation.md  Baseline调研（MTGNN/GraphWaveNet/AGCRN/DCRN/DiffSTG方案）
│
├── smoke_test/                    烟雾测试（验证环境+代码+数据路径）
│   ├── config.json                运行配置（1 epoch, hidden_size=16, 8个窗口）
│   ├── metrics_summary.json       最终指标（Test RMSE=166.85, MAE=164.74）
│   ├── split_summary.json         数据切分详情
│   └── graph_summary.json         图结构（S=691边, T=1570边, PE=317边）
│
├── epoch3_test/                   3轮小配置训练（验证模型学习能力）
│   ├── config.json                运行配置（3 epoch, hidden_size=32, 128个窗口）
│   ├── metrics_summary.json       最终指标（Test RMSE=156.72, MAE=154.75）
│   ├── training_curves.png        Loss/RMSE/MAE 训练曲线（Loss 3.63→2.02→0.63）
│   ├── predictions.png            6站点预测值vs真实值散点图
│   ├── train_loss.npy             每轮训练损失
│   ├── valid_rmse.npy             每轮验证RMSE
│   └── valid_mae.npy              每轮验证MAE
│
├── diffstg_baseline/              DiffSTG Baseline 适配
│   ├── flow.npy                   适配后的数据 (8717, 95, 1)
│   ├── adj.npy                    二值化空间邻接矩阵 (95×95)
│   └── run_diffstg_cpu.py         CPU运行脚本（已验证loss可下降）
│
└── scripts/                       第一周使用的全部工具脚本
    ├── run_smoke_cpu.ps1          一键Smoke Test（Windows PowerShell）
    ├── run_train.ps1              一键正式训练（支持环境变量覆盖）
    ├── view_results.ps1 / .py     查看训练结果 + 自动生成曲线图和散点图
    ├── eda_week1.py               EDA分析脚本（可复现）
    ├── pm_stats.py                PM2.5/PM10缺失统计脚本
    └── prepare_diffstg_data.py    DiffSTG数据准备脚本
```

---

## 第一周任务清单

### 数据整理

| 条目 | 结果 | 状态 |
|------|------|:--:|
| 阅读数据说明 | 95个站点、8717小时、15特征（O₃+14气象）、2022全年 | ✅ |
| 统计 O₃ 缺失 | 处理后数据（95站）：**0.0%**；原始CSV（2024站）：17.75% | ✅ |
| 统计 PM2.5 缺失 | 原始CSV（2024站）：**18.27%**（预处理筛选后模型用95站无缺失） | ✅ |
| 统计 PM10 缺失 | 原始CSV（2024站）：**17.84%**（预处理筛选后模型用95站无缺失） | ✅ |
| 画整体时间序列 | 6张图覆盖：年度时序、浓度分布、月变化、日变化、周变化、站点相关性 | ✅ |

### Baseline

| 条目 | 结果 | 状态 |
|------|------|:--:|
| 确认 MTGNN/GraphWaveNet/AGCRN | 论文Table1已整理：MTGNN RMSE=10.66 最佳传统模型 | ✅ |
| 优先调研 DiffSTG | 代码已下载、数据已适配、训练pipeline已跑通（loss正常下降） | ✅ |
| 跑通一个 baseline | PE-DiffWaveNet自身训练已验证，DiffSTG环境就绪可随时跑 | ✅ |

### PE-DiffWaveNet

| 条目 | 结果 | 状态 |
|------|------|:--:|
| 运行 Smoke Test | 1 epoch, CPU, 8窗口：无报错，正常输出 config/metrics/graph | ✅ |
| 小配置跑 1-3 epoch | 3 epoch, CPU, 128窗口：Loss **3.63→0.63**，模型在正确学习 | ✅ |
| 检查日志和 metrics_summary.json | 两个实验的日志和指标均已检查并归档 | ✅ |

---

## 关键数据发现

```
O₃ 统计（95站处理后数据）
├── 范围:   1 ~ 410 μg/m³
├── 均值:   68.1 μg/m³
├── 中位数: 61.0 μg/m³
├── 缺失率: 0.0%
└── 季节性: 夏季(5-6月)~150 μg/m³，冬季(12-1月)~20 μg/m³

日变化特征
└── 午后 14:00-16:00 峰值（光化学反应），夜间最低

原始CSV规模
├── 365 个文件，每天约2000个站点
├── 15种污染物类型（AQI/PM2.5/PM10/SO₂/NO₂/O₃/CO等）
└── 模型实际使用其中质量最好的95个站点
```

---

## 训练结果对比

| 配置 | Epochs | 窗口数 | Hidden | Test RMSE | Test MAE | 备注 |
|------|--------|--------|--------|-----------|----------|------|
| Smoke Test | 1 | 8 | 16 | 166.85 | 164.74 | 仅验证流程 |
| 3-Epoch | 3 | 128 | 32 | 156.72 | 154.75 | Loss持续下降 |
| 论文正式 | 120 | ~7300 | 64 | ~10.94 | ~7.56 | 第二周目标 |

---

## 环境信息

- **Python**: 3.9.7 | **PyTorch**: 2.1.0+cu121
- **GPU**: NVIDIA RTX 4060 (8GB) | **CUDA**: 12.1
- **系统**: Windows 11 Pro | **Shell**: PowerShell
- 所有脚本已适配 Windows，无需手动传 `--data_dir`

---

## 运行命令速查

```powershell
# Smoke Test（验证环境）
.\scripts\run_smoke_cpu.ps1

# 正式训练（GPU, 120 epochs）
.\scripts\run_train.ps1

# 查看指定实验的结果
.\scripts\view_results.ps1 week1_3epoch

# 列出所有实验
.\scripts\view_results.ps1 --list

# DiffSTG baseline（需要先 cd 到对应目录）
cd external_baselines\DiffSTG\DiffSTG-main
python run_diffstg_cpu.py
```
