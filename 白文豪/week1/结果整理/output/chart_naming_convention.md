# 图表命名规范

## 命名格式

```
{category}_{metric}_{method}_{config}_{date}.{ext}
```

## 参数说明

| 参数 | 示例 | 说明 |
|------|------|------|
| category | ts, spatial, ablation | 图表类别 |
| metric | rmse, mae, mape, loss | 指标类型 |
| method | pe_diffwavenet, mtgnn, gru | 方法名称 |
| config | p6_s42, p12_s52 | 配置（预测步长_种子） |
| date | 20260707 | 日期 |
| ext | png, pdf, svg | 文件格式 |

## 图表类别

| 类别 | 说明 | 示例 |
|------|------|------|
| ts | 时间序列图 | ts_o3_pe_diffwavenet_p6_s42_20260707.png |
| spatial | 空间分布图 | spatial_rmse_mtgnn_p6_s42_20260707.png |
| ablation | 消融实验图 | ablation_rmse_pe_diffwavenet_pe_vs_nope_20260707.png |
| comparison | 对比图 | comparison_rmse_all_methods_p6_s42_20260707.png |
| curve | 训练曲线 | curve_loss_pe_diffwavenet_p6_s42_20260707.png |

## 指标缩写

| 缩写 | 全称 | 说明 |
|------|------|------|
| rmse | Root Mean Squared Error | 均方根误差 |
| mae | Mean Absolute Error | 平均绝对误差 |
| mape | Mean Absolute Percentage Error | 平均绝对百分比误差 |
| loss | Training Loss | 训练损失 |
| peak | Peak RMSE | 峰值RMSE |

## 方法缩写

| 缩写 | 全称 |
|------|------|
| pe_diffwavenet | PE-DiffWaveNet |
| mtgnn | MTGNN |
| gwave | Graph WaveNet |
| agcrn | AGCRN |
| dcrnn | DCRNN |
| atgcn | ATGCN-PE3 |
| gru | GRU Baseline |
| linear | Linear Regression |
| persist | Persistence |
| hist_mean | Historical Mean |

## 示例

```
# 时间序列预测对比
ts_prediction_pe_diffwavenet_p6_s42_20260707.png

# 空间误差分布
spatial_error_distribution_pe_diffwavenet_p6_s42_20260707.png

# 消融实验对比
ablation_pe_components_pe_diffwavenet_20260707.png

# 所有方法对比柱状图
comparison_bar_rmse_all_methods_p6_s42_20260707.png

# 训练损失曲线
curve_train_loss_pe_diffwavenet_p6_s42_20260707.png
```

## 文件组织

```
results/
├── figures/
│   ├── ts/              # 时间序列图
│   ├── spatial/         # 空间分布图
│   ├── ablation/        # 消融实验图
│   ├── comparison/      # 对比图
│   └── curve/           # 训练曲线
├── tables/              # 表格文件
└── logs/                # 日志文件
```
