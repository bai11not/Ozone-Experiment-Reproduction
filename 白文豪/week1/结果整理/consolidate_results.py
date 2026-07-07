#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""统一结果整理脚本"""

import argparse
import os
import csv
import json
import numpy as np
import pandas as pd


def load_main_table(path):
    df = pd.read_csv(path)
    return df


def load_baseline_results(path):
    df = pd.read_csv(path)
    return df


def load_metrics_summary(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def create_unified_table(main_table_path, baseline_path, experiment_metrics_path, output_dir):
    main_table = load_main_table(main_table_path)
    baseline_results = load_baseline_results(baseline_path)
    
    unified_rows = []
    
    for _, row in main_table.iterrows():
        unified_rows.append({
            'Method': row['Method'],
            'RMSE': row['RMSE'],
            'MAE': row['MAE'],
            'MAPE': row['MAPE'],
            'Peak_RMSE': row['Peak_RMSE'],
            'Step6_RMSE': row['Step6_RMSE'],
            'Source': row['Source'],
            'Category': 'Main Table'
        })
    
    for _, row in baseline_results.iterrows():
        unified_rows.append({
            'Method': row['Method'],
            'RMSE': row['RMSE'],
            'MAE': row['MAE'],
            'MAPE': row['MAPE'],
            'Peak_RMSE': row['Peak_RMSE'],
            'Step6_RMSE': row['Step6_RMSE'],
            'Source': 'Week1 Baseline',
            'Category': 'Baseline'
        })
    
    experiment_metrics = load_metrics_summary(experiment_metrics_path)
    if experiment_metrics:
        unified_rows.append({
            'Method': 'PE-DiffWaveNet (smoke)',
            'RMSE': experiment_metrics.get('test_rmse', ''),
            'MAE': experiment_metrics.get('test_mae', ''),
            'MAPE': experiment_metrics.get('test_mape', ''),
            'Peak_RMSE': '',
            'Step6_RMSE': '',
            'Source': 'Week1 Experiment',
            'Category': 'PE-DiffWaveNet'
        })
    
    unified_df = pd.DataFrame(unified_rows)
    
    os.makedirs(output_dir, exist_ok=True)
    unified_df.to_csv(os.path.join(output_dir, 'unified_results_table.csv'), index=False, encoding='utf-8-sig')
    print(f"✓ 统一结果表已保存: {output_dir}/unified_results_table.csv")
    
    return unified_df


def create_metrics_template(output_dir):
    template = [
        {'Method': '', 'RMSE': '', 'MAE': '', 'MAPE': '', 'Peak_RMSE': '', 'Step6_RMSE': '', 
         'Step4_6_RMSE': '', 'Source': '', 'Category': '', 'Notes': ''}
    ]
    df = pd.DataFrame(template)
    df.to_csv(os.path.join(output_dir, 'metrics_template.csv'), index=False, encoding='utf-8-sig')
    print(f"✓ 指标模板已保存: {output_dir}/metrics_template.csv")


def create_chart_naming_convention(output_dir):
    convention = """# 图表命名规范

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
"""
    with open(os.path.join(output_dir, 'chart_naming_convention.md'), 'w', encoding='utf-8') as f:
        f.write(convention)
    print(f"✓ 图表命名规范已保存: {output_dir}/chart_naming_convention.md")


def create_paper_assets_summary(paper_assets_dir, output_dir):
    summary = {
        'table1_main': {
            'file': 'table1_main_raw_comparison.csv',
            'fields': ['Method', 'RMSE', 'MAE', 'MAPE', 'Peak_RMSE', 'Step6_RMSE', 'Source'],
            'description': '主对比表，包含所有 baseline 和本文方法',
            'rows': 10,
            'methods': ['MTGNN', 'Graph WaveNet', 'AGCRN', 'DCRNN', 'ATGCN-PE3', 'PE-DiffWaveNet']
        },
        'table2_ablation': {
            'file': 'table2_ablation.csv',
            'fields': ['Variant', 'Seeds', 'RMSE', 'MAE', 'MAPE', 'Step4_6_RMSE', 'Step6_RMSE', 'Peak_RMSE'],
            'description': '消融实验表，验证 PE 组件的有效性',
            'rows': 7,
            'variants': ['No-PE backbone', 'Safe PE graph+FiLM', 'Real PE-guided loss', 
                        'Shuffled PE-guided loss', 'PE graph only', 'PE FiLM only']
        },
        'table3_pe_stratified': {
            'file': 'table3_pe_stratified_summary.csv',
            'fields': [],
            'description': 'PE 分层统计',
            'rows': 0,
            'variants': []
        }
    }
    
    table3_path = os.path.join(paper_assets_dir, 'table3_pe_stratified_summary.csv')
    if os.path.exists(table3_path):
        df = pd.read_csv(table3_path)
        summary['table3_pe_stratified']['fields'] = df.columns.tolist()
        summary['table3_pe_stratified']['rows'] = len(df)
    
    with open(os.path.join(output_dir, 'paper_assets_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    summary_md = f"""# Paper Assets 字段整理

## Table 1: 主对比表

**文件**: `table1_main_raw_comparison.csv`

**字段**: {', '.join(summary['table1_main']['fields'])}

**说明**: 包含所有 baseline 方法和本文方法的对比结果

**方法列表**:
{chr(10).join([f"- {m}" for m in summary['table1_main']['methods']])}

## Table 2: 消融实验表

**文件**: `table2_ablation.csv`

**字段**: {', '.join(summary['table2_ablation']['fields'])}

**说明**: 验证 PE 组件的有效性

**变体列表**:
{chr(10).join([f"- {v}" for v in summary['table2_ablation']['variants']])}

## Table 3: PE 分层统计表

**文件**: `table3_pe_stratified_summary.csv`

**字段**: {', '.join(summary['table3_pe_stratified']['fields']) if summary['table3_pe_stratified']['fields'] else '待确认'}

**说明**: PE 分层统计结果

## 统一指标字段

| 字段名 | 全称 | 单位 | 说明 |
|--------|------|------|------|
| RMSE | Root Mean Squared Error | μg/m³ | 均方根误差 |
| MAE | Mean Absolute Error | μg/m³ | 平均绝对误差 |
| MAPE | Mean Absolute Percentage Error | % | 平均绝对百分比误差 |
| Peak_RMSE | Peak RMSE | μg/m³ | 峰值时刻 RMSE |
| Step6_RMSE | Step 6 RMSE | μg/m³ | 第6步预测 RMSE |
| Step4_6_RMSE | Steps 4-6 RMSE | μg/m³ | 第4-6步平均 RMSE |

## 数据源标记

| Source | 说明 |
|--------|------|
| official raw, seed42 | 官方代码原始结果，seed=42 |
| ATGCN raw, seed42 | ATGCN 原始结果，seed=42 |
| ours raw, seeds 42/52/62 | 本文方法，多个 seed 平均 |
| Week1 Baseline | Week1 新增 baseline 结果 |
| Week1 Experiment | Week1 实验结果 |
"""
    
    with open(os.path.join(output_dir, 'paper_assets_summary.md'), 'w', encoding='utf-8') as f:
        f.write(summary_md)
    print(f"✓ Paper Assets 摘要已保存: {output_dir}/paper_assets_summary.md")


def parse_args():
    parser = argparse.ArgumentParser(description='Consolidate results')
    parser.add_argument('--base_dir', type=str, default='/mnt/d/时空数据',
                        help='Base directory')
    parser.add_argument('--output_dir', type=str, default='白文豪/week1/结果整理/output',
                        help='Output directory')
    return parser.parse_args()


def main():
    args = parse_args()
    
    base_dir = args.base_dir
    output_dir = os.path.join(base_dir, args.output_dir)
    
    ozone_dir = os.path.join(base_dir, '臭氧预测资料')
    main_table_path = os.path.join(ozone_dir, 'paper_assets_pediffwavenet', 'table1_main_raw_comparison.csv')
    baseline_path = os.path.join(base_dir, '白文豪/week1/output', 'baseline_aligned_with_main_table.csv')
    experiment_metrics_path = os.path.join(ozone_dir, 'matrix_N95_PEDiffWaveNet_noleak_student_smoke_gpu', 'metrics_summary.json')
    paper_assets_dir = os.path.join(ozone_dir, 'paper_assets_pediffwavenet')
    
    print("="*60)
    print("统一结果整理")
    print("="*60)
    
    create_unified_table(main_table_path, baseline_path, experiment_metrics_path, output_dir)
    create_metrics_template(output_dir)
    create_chart_naming_convention(output_dir)
    create_paper_assets_summary(paper_assets_dir, output_dir)
    
    print("\n" + "="*60)
    print("所有结果整理完成！")
    print(f"输出目录: {output_dir}")
    print("="*60)


if __name__ == '__main__':
    main()