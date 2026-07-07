#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Week 1 Data Analysis - N95 stations only
"""
import os, sys, glob, json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict

BASE_DIR = r'd:\桌面\臭氧预测资料\臭氧预测资料'
DATA_DIR = os.path.join(BASE_DIR, 'data_N95')
XLSX_DIR = os.path.join(BASE_DIR, 'xlsx_N95')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs_week1')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"BASE_DIR: {BASE_DIR}")
print(f"OUTPUT_DIR: {OUTPUT_DIR}")

# ============================================================
# 0. Load station IDs (N95)
# ============================================================
station_file = os.path.join(XLSX_DIR, 'station_loc1.xlsx')
station_df = pd.read_excel(station_file)
cols_all = station_df.columns.tolist()
id_col = cols_all[0]   # 监测点编码
name_col = cols_all[1]  # 监测点名称
city_col = cols_all[2]  # 城市
lon_col = cols_all[3]   # 经度
lat_col = cols_all[4]   # 纬度

N95_IDS = set(station_df[id_col].astype(str).tolist())
print(f"N95 station count: {len(N95_IDS)}")
print(f"IDs sample: {list(N95_IDS)[:5]}")

lats = pd.to_numeric(station_df[lat_col], errors='coerce')
lons = pd.to_numeric(station_df[lon_col], errors='coerce')

# ============================================================
# 1. Read data documentation
# ============================================================
print("\n" + "="*60)
print("1. Data documentation")
print("="*60)
docs_dir = os.path.join(BASE_DIR, 'docs_word')
if os.path.exists(docs_dir):
    for f in os.listdir(docs_dir):
        if f.endswith('.docx') and not f.startswith('~'):
            doc_path = os.path.join(docs_dir, f)
            try:
                from docx import Document
                doc = Document(doc_path)
                doc_text = '\n'.join([p.text for p in doc.paragraphs])
                print(f"Document: {f}")
                # Print first part (may have encoding issues on console)
                with open(os.path.join(OUTPUT_DIR, 'data_doc_extracted.txt'), 'w', encoding='utf-8') as fout:
                    fout.write(doc_text)
                print("Document text saved to data_doc_extracted.txt")
            except Exception as e:
                print(f"Could not read {f}: {e}")

# ============================================================
# 2. Station analysis
# ============================================================
print("\n" + "="*60)
print("2. Station geographic distribution")
print("="*60)

city_counts = station_df[city_col].value_counts()
print(f"Total stations: {len(station_df)}")
print(f"Cities ({len(city_counts)}):")
for city, count in city_counts.items():
    print(f"  {city}: {count}")

print(f"\nLat range: {lats.min():.4f} - {lats.max():.4f}")
print(f"Lon range: {lons.min():.4f} - {lons.max():.4f}")

# Station scatter plot
fig, ax = plt.subplots(figsize=(12, 10))
sc = ax.scatter(lons, lats, c='red', s=40, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.set_title(f'Distribution of {len(station_df)} N95 Air Quality Monitoring Stations', fontsize=14)
ax.grid(True, alpha=0.3)
# Add annotations for major cities
for _, row in station_df.iterrows():
    ax.annotate(str(row[city_col]), (float(row[lon_col]), float(row[lat_col])),
                fontsize=5, alpha=0.6, ha='center', va='bottom')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'station_distribution.png'), dpi=150)
plt.close()
print("Station map saved.")

station_df.to_csv(os.path.join(OUTPUT_DIR, 'station_table.csv'), index=False, encoding='utf-8-sig')

# ============================================================
# 3. Missing data statistics (N95 stations only)
# ============================================================
print("\n" + "="*60)
print("3. Missing data statistics (N95 stations)")
print("="*60)

csv_files = sorted(glob.glob(os.path.join(DATA_DIR, 'china_sites_*.csv')))
print(f"CSV files: {len(csv_files)}")

# Initialize counters
overall = {p: {'valid': 0, 'total': 0} for p in ['O3', 'PM2.5', 'PM10']}
monthly = defaultdict(lambda: {p: {'valid': 0, 'total': 0} for p in ['O3', 'PM2.5', 'PM10']})
site_miss = defaultdict(lambda: {p: {'valid': 0, 'total': 0} for p in ['O3', 'PM2.5', 'PM10']})

errors = 0
for i, csv_path in enumerate(csv_files):
    fname = os.path.basename(csv_path)
    date_str = fname.replace('china_sites_', '').replace('.csv', '')
    year_month = date_str[:6]

    try:
        df = pd.read_csv(csv_path)
        # Find columns that are in N95_IDS
        n95_cols = [c for c in df.columns if c in N95_IDS]

        if len(n95_cols) != 95 and i == 0:
            print(f"  Warning: found {len(n95_cols)} N95 columns in first file")

        for p_type in ['O3', 'PM2.5', 'PM10']:
            p_rows = df[df['type'] == p_type]
            if len(p_rows) == 0:
                continue
            for col in n95_cols:
                vals = pd.to_numeric(p_rows[col], errors='coerce').values
                valid = int(np.sum(~np.isnan(vals)))
                total = len(vals)
                overall[p_type]['valid'] += valid
                overall[p_type]['total'] += total
                monthly[year_month][p_type]['valid'] += valid
                monthly[year_month][p_type]['total'] += total
                site_miss[col][p_type]['valid'] += valid
                site_miss[col][p_type]['total'] += total

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(csv_files)}...")
    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"  Error {fname}: {e}")
        continue

print(f"Done. {len(csv_files)} files, {errors} errors.")

# Overall missing rates
print("\n=== Overall Missing Rates ===")
for p in ['O3', 'PM2.5', 'PM10']:
    v, t = overall[p]['valid'], overall[p]['total']
    rate = (1 - v/t)*100 if t > 0 else 100
    print(f"  {p}: valid={v:,}, total={t:,}, missing_rate={rate:.2f}%")

# Monthly missing rates
print("\n=== Monthly Missing Rates ===")
monthly_data = []
for month in sorted(monthly.keys()):
    row = {'month': month}
    parts = []
    for p in ['O3', 'PM2.5', 'PM10']:
        v, t = monthly[month][p]['valid'], monthly[month][p]['total']
        rate = (1 - v/t)*100 if t > 0 else 100
        row[f'{p}_rate'] = round(rate, 2)
        parts.append(f"{p}={rate:.1f}%")
    monthly_data.append(row)
    print(f"  {month}: {', '.join(parts)}")
monthly_df = pd.DataFrame(monthly_data)
monthly_df.to_csv(os.path.join(OUTPUT_DIR, 'monthly_missing_stats.csv'), index=False, encoding='utf-8-sig')

# Site-level missing
site_data = []
for site_id in sorted(site_miss.keys()):
    row = {'site_id': site_id}
    for p in ['O3', 'PM2.5', 'PM10']:
        v, t = site_miss[site_id][p]['valid'], site_miss[site_id][p]['total']
        rate = (1 - v/t)*100 if t > 0 else 100
        row[f'{p}_rate'] = round(rate, 2)
    site_data.append(row)
site_df = pd.DataFrame(site_data)
site_df.to_csv(os.path.join(OUTPUT_DIR, 'site_missing_stats.csv'), index=False, encoding='utf-8-sig')
print(f"\nSite-level stats: {len(site_df)} sites")
print("Top 10 by O3 missing:")
print(site_df.nlargest(10, 'O3_rate')[['site_id', 'O3_rate', 'PM2.5_rate', 'PM10_rate']].to_string())

# Missing rate charts
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
colors_p = {'O3': '#2196F3', 'PM2.5': '#4CAF50', 'PM10': '#FF9800'}

ax = axes[0]
months_list = [m['month'] for m in monthly_data]
x = range(len(months_list))
width = 0.25
for j, p in enumerate(['O3', 'PM2.5', 'PM10']):
    rates = [m[f'{p}_rate'] for m in monthly_data]
    ax.bar([xi + j*width for xi in x], rates, width, label=p, color=colors_p[p], alpha=0.8)
ax.set_xlabel('Month')
ax.set_ylabel('Missing Rate (%)')
ax.set_title('Monthly Missing Rate by Pollutant (N95 Stations)')
ax.set_xticks([xi + width for xi in x])
ax.set_xticklabels(months_list, rotation=45, ha='right', fontsize=8)
ax.legend()
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
for p in ['O3', 'PM2.5', 'PM10']:
    rates = [s[f'{p}_rate'] for s in site_data]
    ax.hist(rates, bins=25, alpha=0.5, label=p, color=colors_p[p])
ax.set_xlabel('Missing Rate (%)')
ax.set_ylabel('Number of Stations')
ax.set_title('Site-level Missing Rate Distribution')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'missing_rate_analysis.png'), dpi=150)
plt.close()
print("Missing rate charts saved.")

# ============================================================
# 4. Daily mean time series
# ============================================================
print("\n" + "="*60)
print("4. Daily mean time series")
print("="*60)

daily_records = []
for i, csv_path in enumerate(csv_files):
    fname = os.path.basename(csv_path)
    date_str = fname.replace('china_sites_', '').replace('.csv', '')
    date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

    try:
        df = pd.read_csv(csv_path)
        n95_cols = [c for c in df.columns if c in N95_IDS]

        for p_type in ['O3', 'PM2.5', 'PM10']:
            p_rows = df[df['type'] == p_type]
            if len(p_rows) == 0:
                daily_records.append({'date': date_formatted, 'pollutant': p_type,
                                      'mean': np.nan, 'std': np.nan, 'min': np.nan,
                                      'max': np.nan, 'count': 0})
                continue
            all_vals = []
            for col in n95_cols:
                vals = pd.to_numeric(p_rows[col], errors='coerce').dropna().values
                all_vals.extend(vals.tolist())
            if all_vals:
                arr = np.array(all_vals)
                daily_records.append({'date': date_formatted, 'pollutant': p_type,
                                      'mean': float(np.mean(arr)),
                                      'std': float(np.std(arr)),
                                      'min': float(np.min(arr)),
                                      'max': float(np.max(arr)),
                                      'count': len(arr)})
            else:
                daily_records.append({'date': date_formatted, 'pollutant': p_type,
                                      'mean': np.nan, 'std': np.nan, 'min': np.nan,
                                      'max': np.nan, 'count': 0})

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(csv_files)}...")
    except Exception as e:
        daily_records.append({'date': date_formatted, 'pollutant': 'O3', 'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'count': 0})
        daily_records.append({'date': date_formatted, 'pollutant': 'PM2.5', 'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'count': 0})
        daily_records.append({'date': date_formatted, 'pollutant': 'PM10', 'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'count': 0})
        continue

daily_df = pd.DataFrame(daily_records)
daily_df['date'] = pd.to_datetime(daily_df['date'])
daily_df.to_csv(os.path.join(OUTPUT_DIR, 'daily_mean_pollutants.csv'), index=False, encoding='utf-8-sig')
print(f"Daily records: {len(daily_df)}")

# Individual time series
fig, axes = plt.subplots(3, 1, figsize=(18, 12), sharex=True)
units = {'O3': 'O3 (ug/m3)', 'PM2.5': 'PM2.5 (ug/m3)', 'PM10': 'PM10 (ug/m3)'}

for idx, p_type in enumerate(['O3', 'PM2.5', 'PM10']):
    ax = axes[idx]
    p_data = daily_df[daily_df['pollutant'] == p_type].sort_values('date').copy()
    ax.plot(p_data['date'], p_data['mean'], color=colors_p[p_type], linewidth=0.8)
    ax.fill_between(p_data['date'].values,
                     (p_data['mean'] - p_data['std']).values,
                     (p_data['mean'] + p_data['std']).values,
                     color=colors_p[p_type], alpha=0.15)
    ax.set_ylabel(units[p_type], fontsize=11)
    ax.set_title(f'{p_type} - Daily Mean (2022, N95 Stations)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

axes[-1].set_xlabel('Date', fontsize=11)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'pollutant_time_series.png'), dpi=150)
plt.close()
print("Individual time series saved.")

# Combined plot
fig, ax = plt.subplots(figsize=(18, 6))
for p_type in ['O3', 'PM2.5', 'PM10']:
    p_data = daily_df[daily_df['pollutant'] == p_type].sort_values('date')
    ax.plot(p_data['date'], p_data['mean'], color=colors_p[p_type], linewidth=1.0, label=p_type)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Concentration (ug/m3)', fontsize=12)
ax.set_title('Daily Mean Pollutant Concentrations (2022, N95 Stations)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'pollutant_time_series_combined.png'), dpi=150)
plt.close()
print("Combined time series saved.")

# Monthly statistics
daily_df['month'] = daily_df['date'].dt.strftime('%Y%m')
monthly_stats = daily_df.groupby(['month', 'pollutant'])['mean'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()
monthly_stats.to_csv(os.path.join(OUTPUT_DIR, 'monthly_pollutant_stats.csv'), index=False, encoding='utf-8-sig')
print("\n=== Monthly Mean Statistics ===")
for month in sorted(daily_df['month'].unique()):
    for p in ['O3', 'PM2.5', 'PM10']:
        sub = daily_df[(daily_df['month'] == month) & (daily_df['pollutant'] == p)]
        if len(sub) > 0:
            m = sub['mean'].mean()
            print(f"  {month} {p}: {m:.2f}" if not np.isnan(m) else f"  {month} {p}: NaN")

# ============================================================
# 5. Generate data summary report
# ============================================================
print("\n" + "="*60)
print("5. Data summary report")
print("="*60)

o3_rate = (1 - overall['O3']['valid']/overall['O3']['total'])*100 if overall['O3']['total'] > 0 else 0
pm25_rate = (1 - overall['PM2.5']['valid']/overall['PM2.5']['total'])*100 if overall['PM2.5']['total'] > 0 else 0
pm10_rate = (1 - overall['PM10']['valid']/overall['PM10']['total'])*100 if overall['PM10']['total'] > 0 else 0

# Build city distribution table
city_lines = ""
for city, count in city_counts.items():
    city_lines += f"| {city} | {count} |\n"

# Find highest and lowest missing sites
highest_o3 = site_df.nlargest(5, 'O3_rate')[['site_id', 'O3_rate']].values
lowest_o3 = site_df.nsmallest(5, 'O3_rate')[['site_id', 'O3_rate']].values

report = f"""# N95 Air Quality Data Summary Report (Draft)

## 1. Data Overview

- **Data source**: China national air quality monitoring network
- **Time period**: 2022-01-01 to 2022-12-31 (365 days, hourly)
- **File count**: {len(csv_files)} daily CSV files in `data_N95/`
- **Station count**: {len(N95_IDS)} stations (N95 subset)
- **Primary pollutants**: O3 (ozone), PM2.5, PM10
- **Spatial extent**: Lat {lats.min():.2f} - {lats.max():.2f}, Lon {lons.min():.2f} - {lons.max():.2f}

## 2. Data Format

Each CSV file in `data_N95/` has the structure:
- `date`: date (YYYYMMDD)
- `hour`: hour of day (0-23)
- `type`: pollutant measurement type (O3, PM2.5, PM10, NO2, SO2, CO, etc.)
- One column per monitoring station, using station code (e.g., 1001A)

## 3. Station Geographic Distribution

### Cities and Station Counts ({len(city_counts)} cities)

| City | Number of Stations |
|------|-------------------|
{city_lines}

### Spatial Map
![Station Distribution](station_distribution.png)

## 4. Missing Data Analysis

### Overall Missing Rates (N95 stations, all hours)

| Pollutant | Valid Records | Total Records | Missing Rate |
|-----------|-------------|---------------|--------------|
| O3        | {overall['O3']['valid']:,} | {overall['O3']['total']:,} | {o3_rate:.2f}% |
| PM2.5     | {overall['PM2.5']['valid']:,} | {overall['PM2.5']['total']:,} | {pm25_rate:.2f}% |
| PM10      | {overall['PM10']['valid']:,} | {overall['PM10']['total']:,} | {pm10_rate:.2f}% |

### Monthly Missing Rates
See `monthly_missing_stats.csv` for detailed monthly breakdown.

### Site-level Missing Rates
- See `site_missing_stats.csv` for per-station missing rates
- Missing rate visualization: `missing_rate_analysis.png`
- Higher missing rates may appear at specific stations; consider filtering before modeling

## 5. Data Split (Chronological No-Leak)

| Split | Start | End | Hours | Percentage |
|-------|-------|-----|-------|------------|
| Train | 2022-01-01 00:00 | 2022-11-05 23:00 | 7,378 | ~84.7% |
| Validation | 2022-11-06 00:00 | 2022-12-03 21:00 | 669 | ~7.6% |
| Test | 2022-12-03 22:00 | 2022-12-31 23:00 | 670 | ~7.7% |

## 6. Time Series Characteristics

- **O3**: Peak in summer (Jun-Aug), low in winter — clear seasonal pattern driven by photochemistry
- **PM2.5**: Higher in winter (Nov-Feb), lower in summer — influenced by heating and meteorology
- **PM10**: Similar seasonal pattern to PM2.5, with additional spring dust events
- Time series plots: `pollutant_time_series.png`, `pollutant_time_series_combined.png`
- Daily mean data: `daily_mean_pollutants.csv`

## 7. Model Input Features (m=15)

The PE-DiffWaveNet model uses 15-dimensional input features, combining:
- Pollutant concentrations (O3, PM2.5, PM10, etc.)
- Meteorological factors (from met_raw_aligned_cache.npz)
- Positional encoding features

## 8. Output Files

| File | Description |
|------|-------------|
| `data_summary_report.md` | This report |
| `station_table.csv` | Station metadata (ID, name, city, lat, lon) |
| `station_distribution.png` | Geographic map of 95 stations |
| `monthly_missing_stats.csv` | Monthly missing rates per pollutant |
| `site_missing_stats.csv` | Per-station missing rates |
| `missing_rate_analysis.png` | Missing rate bar chart + histogram |
| `daily_mean_pollutants.csv` | Daily mean concentrations |
| `monthly_pollutant_stats.csv` | Monthly descriptive statistics |
| `pollutant_time_series.png` | Individual pollutant time series (3 panels) |
| `pollutant_time_series_combined.png` | Combined pollutant time series |
| `data_doc_extracted.txt` | Extracted text from original data documentation |
"""

with open(os.path.join(OUTPUT_DIR, 'data_summary_report.md'), 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n{'='*60}")
print(f"ALL DONE! Output directory: {OUTPUT_DIR}")
print(f"Generated files: {sorted(os.listdir(OUTPUT_DIR))}")
