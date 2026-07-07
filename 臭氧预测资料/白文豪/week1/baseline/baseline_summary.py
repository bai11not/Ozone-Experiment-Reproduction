#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Baseline results summary script.

Aligns baseline results with the main comparison table format (table1_main_raw_comparison.csv).
Converts normalized metrics to real-scale metrics using max_value.
"""

import argparse
import json
import os
import numpy as np
import pandas as pd


def load_main_table(main_table_path):
    df = pd.read_csv(main_table_path)
    return df


def load_baseline_results(baseline_results_path):
    df = pd.read_csv(baseline_results_path)
    return df


def normalize_to_real(df, max_value=100.0):
    metrics_to_convert = ['RMSE', 'MAE', 'Peak_RMSE', 'Step6_RMSE']
    df_real = df.copy()
    for metric in metrics_to_convert:
        if metric in df.columns:
            df_real[metric] = df_real[metric] * max_value
    return df_real


def align_with_main_table(baseline_df, max_value=100.0):
    baseline_real = normalize_to_real(baseline_df, max_value)
    
    aligned_df = baseline_real.copy()
    aligned_df['Source'] = 'baseline script, seed42'
    
    columns_order = ['Method', 'RMSE', 'MAE', 'MAPE', 'Peak_RMSE', 'Step6_RMSE', 'Source']
    aligned_df = aligned_df[columns_order]
    
    return aligned_df


def main():
    parser = argparse.ArgumentParser(description='Baseline results summary')
    parser.add_argument('--main_table', type=str, 
                        default='/mnt/d/时空数据/臭氧预测资料/paper_assets_pediffwavenet/table1_main_raw_comparison.csv',
                        help='Path to main comparison table')
    parser.add_argument('--baseline_results', type=str,
                        default='/mnt/d/时空数据/臭氧预测资料/白文豪/week1/新增代码/output/baseline_results.csv',
                        help='Path to baseline results CSV')
    parser.add_argument('--output_dir', type=str,
                        default='/mnt/d/时空数据/臭氧预测资料/白文豪/week1/新增代码/output',
                        help='Output directory')
    parser.add_argument('--max_value', type=float, default=100.0,
                        help='Max O3 concentration for normalization')
    args = parser.parse_args()
    
    print(f"Loading main table: {args.main_table}")
    main_table = load_main_table(args.main_table)
    print("Main table contents:")
    print(main_table.to_string(index=False))
    print()
    
    print(f"Loading baseline results: {args.baseline_results}")
    baseline_df = load_baseline_results(args.baseline_results)
    print("Baseline results (normalized):")
    print(baseline_df.to_string(index=False))
    print()
    
    print(f"Converting to real scale (max_value={args.max_value})...")
    aligned_df = align_with_main_table(baseline_df, args.max_value)
    print("Aligned baseline results (real scale):")
    print(aligned_df.to_string(index=False))
    print()
    
    combined_df = pd.concat([main_table, aligned_df], ignore_index=True)
    print("Combined comparison table:")
    print(combined_df.to_string(index=False))
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    aligned_path = os.path.join(args.output_dir, 'baseline_aligned_with_main_table.csv')
    aligned_df.to_csv(aligned_path, index=False)
    print(f"\nAligned baseline results saved to: {aligned_path}")
    
    combined_path = os.path.join(args.output_dir, 'combined_comparison_table.csv')
    combined_df.to_csv(combined_path, index=False)
    print(f"Combined comparison table saved to: {combined_path}")
    
    summary = {
        'max_value': args.max_value,
        'main_table_source': args.main_table,
        'baseline_results_source': args.baseline_results,
        'baseline_methods': list(baseline_df['Method']),
        'conversion_note': 'All metrics except MAPE are multiplied by max_value to convert from normalized scale'
    }
    with open(os.path.join(args.output_dir, 'baseline_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Summary metadata saved to: {os.path.join(args.output_dir, 'baseline_summary.json')}")


if __name__ == '__main__':
    main()