# Week 1 交付物

## 目录结构

```
week1_deliverables/
├── 01_数据整理/            ← 数据理解、缺失统计、可视化
│   ├── 报告/               ← data_summary_report.md, week1_detailed_guide.md
│   ├── 表格/               ← 站点表、缺失率表、日均值表
│   ├── 图表/               ← 站点分布图、时间序列图、缺失率图
│   └── 脚本/               ← week1_analysis.py
│
├── 02_Baseline/            ← Baseline 调研与实验
│   ├── DiffSTG调研/        ← 适配方案文档
│   ├── DiffSTG数据/        ← flow.npy + adj.npy + 生成脚本
│   ├── ATGCN-PE3实验/      ← 3-epoch debug 训练输出
│   └── Baseline论文结果/   ← 论文中 baseline 对比表
│
├── 03_PE-DiffWaveNet/      ← 本模型实验
│   ├── Smoke_Test/         ← 1-epoch smoke test 输出
│   ├── Debug_Run/          ← 3-epoch debug 训练输出
│   ├── weights_smoke/      ← smoke test 的模型权重
│   ├── weights_debug/      ← debug run 的模型权重
│   └── 脚本/               ← run_smoke_cpu.sh, run_train_pediffwavenet.sh
│
└── 04_结果整理/            ← 汇总交付物
    ├── results.csv         ← 统一格式实验指标表
    ├── commands.sh         ← 所有运行过的命令
    ├── week1_summary.md    ← 第一周完成总结
    └── week1_detailed_guide.md ← 详细指南（参数解释、日志解读）
```

## 源数据（不在此目录中）

源数据保持在以下目录不动：
- `data_N95/` — 原始逐日 CSV
- `matrix_N95/` — 处理后的 numpy 数组
- `xlsx_N95/` — 站点信息 Excel
- `code/` — 训练代码
