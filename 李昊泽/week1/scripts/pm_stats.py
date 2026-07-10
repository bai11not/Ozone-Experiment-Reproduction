#!/usr/bin/env python
"""完整遍历 365 个 CSV，统计 PM2.5 和 PM10 缺失值。"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(r'H:\Trae Project\O3predict\data_N95')
csv_files = sorted(DATA_DIR.glob('china_sites_*.csv'))

print(f'正在扫描 {len(csv_files)} 个CSV文件，统计 PM2.5 / PM10 / O3 缺失值...')

results = {'PM2.5': {'valid': 0, 'total': 0, 'days_with_data': 0, 'days_total': 0},
           'PM10':  {'valid': 0, 'total': 0, 'days_with_data': 0, 'days_total': 0},
           'O3':    {'valid': 0, 'total': 0, 'days_with_data': 0, 'days_total': 0}}

n = 0
for csv_f in csv_files:
    n += 1
    if n % 50 == 0:
        print(f'  进度: {n}/{len(csv_files)}...')

    df = pd.read_csv(csv_f)
    # Station columns are everything except date, hour, type
    station_cols = [c for c in df.columns if c not in ('date', 'hour', 'type')]
    # There are exactly 24 hours per day per pollutant type
    for pollutant in ['PM2.5', 'PM10', 'O3']:
        sub = df[df['type'] == pollutant]
        results[pollutant]['days_total'] += 1
        if len(sub) > 0:
            results[pollutant]['days_with_data'] += 1
            total_cells = len(sub) * len(station_cols)
            valid_cells = int(sub[station_cols].notna().sum().sum())
            results[pollutant]['valid'] += valid_cells
            results[pollutant]['total'] += total_cells

print(f'\n{"="*55}')
print(f'  污染物      |   有效数据量    |   总数据量     |   缺失率')
print(f'{"="*55}')
for name, r in results.items():
    if r['total'] > 0:
        rate = (1 - r['valid']/r['total']) * 100
        print(f'  {name:10s} | {r["valid"]:>13,d} | {r["total"]:>13,d} | {rate:>10.4f}%')
    else:
        print(f'  {name:10s} | {"无数据":>13}')
print(f'{"="*55}')

# 逐污染物天数覆盖
for name, r in results.items():
    print(f'\n  {name}: {r["days_with_data"]}/{r["days_total"]} 天有数据')

# 站点列数
sample = pd.read_csv(csv_files[0])
station_cols = [c for c in sample.columns if c not in ('date', 'hour', 'type')]
print(f'\n  CSV中站点列总数: {len(station_cols)}')
print(f'  说明: 原始CSV包含约2000+个站点，但模型仅使用筛选后的95个高质量站点。')
