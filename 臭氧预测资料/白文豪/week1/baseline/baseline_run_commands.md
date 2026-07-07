# Baseline 运行命令记录

## 已有主表 baseline 确认

主表 `paper_assets_pediffwavenet/table1_main_raw_comparison.csv` 包含以下 baseline：
- MTGNN (L=24): RMSE=10.6620, MAE=7.3383, MAPE=29.99%
- MTGNN (L=12): RMSE=10.8028, MAE=7.3465, MAPE=30.50%
- Graph WaveNet (L=12): RMSE=11.5354, MAE=7.7982, MAPE=33.60%
- AGCRN (L=12): RMSE=11.6858, MAE=8.2093, MAPE=34.78%
- DCRNN: RMSE=12.2813, MAE=8.5124, MAPE=36.46%

## 新增 Baseline 运行命令

### 运行全部 baseline

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/新增代码/run_baseline_evaluation.py"
```

### 指定参数运行

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/新增代码/run_baseline_evaluation.py" \
  --data_dir "/mnt/d/时空数据/臭氧预测资料" \
  --output_dir "/mnt/d/时空数据/臭氧预测资料/白文豪/week1/新增代码/output" \
  --max_value 100.0 \
  --gru_epochs 50 \
  --gru_lr 0.001 \
  --linear_epochs 100 \
  --linear_lr 0.01 \
  --seed 42
```

### 生成对齐主表的汇总结果

```bash
cd /mnt/d/时空数据/臭氧预测资料
source .venv/bin/activate
python3 "白文豪/week1/新增代码/baseline_summary.py"
```

## Baseline 结果（归一化 scale）

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE |
|--------|------|-----|------|-----------|------------|
| Persistence (L=12) | 0.0476 | 0.0318 | 95.12% | 0.0573 | 0.0639 |
| Historical Mean (L=12) | 0.0582 | 0.0465 | 189.38% | 0.0790 | 0.0636 |
| GRU Baseline | 0.0348 | 0.0257 | 92.68% | 0.0447 | 0.0443 |
| Linear Regression | 0.0458 | 0.0349 | 131.33% | 0.0522 | 0.0569 |

## Baseline 结果（真实 scale, max_value=100）

| Method | RMSE | MAE | MAPE | Peak_RMSE | Step6_RMSE |
|--------|------|-----|------|-----------|------------|
| Persistence (L=12) | 4.76 | 3.18 | 95.12% | 5.73 | 6.39 |
| Historical Mean (L=12) | 5.82 | 4.65 | 189.38% | 7.90 | 6.36 |
| GRU Baseline | 3.48 | 2.57 | 92.68% | 4.47 | 4.43 |
| Linear Regression | 4.58 | 3.49 | 131.33% | 5.22 | 5.69 |

## 结果文件位置

- 原始 baseline 结果: `output/baseline_results.csv`
- 与主表对齐的结果: `output/baseline_aligned_with_main_table.csv`
- 合并后的完整对比表: `output/combined_comparison_table.csv`
- 汇总元数据: `output/baseline_summary.json`

## DiffSTG 适配说明

DiffSTG 是推荐的扩散类时空图 baseline，需从 GitHub 获取代码并适配到本项目数据格式：

1. 克隆 DiffSTG 仓库
2. 将 `matrix_N95/` 中的数据转换为 DiffSTG 所需格式
3. 配置 DiffSTG 的训练参数
4. 运行训练和评估
5. 将结果转换为主表格式

推荐参考文档: `docs_word/05_有代码论文推荐.docx`