# N95 Air Quality Data Summary Report (Draft)

## 1. Data Overview

- **Data source**: China national air quality monitoring network
- **Time period**: 2022-01-01 to 2022-12-31 (365 days, hourly)
- **File count**: 365 daily CSV files in `data_N95/`
- **Station count**: 95 stations (N95 subset)
- **Primary pollutants**: O3 (ozone), PM2.5, PM10
- **Spatial extent**: Lat 35.68 - 41.04, Lon 111.60 - 119.61

## 2. Data Format

Each CSV file in `data_N95/` has the structure:
- `date`: date (YYYYMMDD)
- `hour`: hour of day (0-23)
- `type`: pollutant measurement type (O3, PM2.5, PM10, NO2, SO2, CO, etc.)
- One column per monitoring station, using station code (e.g., 1001A)

## 3. Station Geographic Distribution

### Cities and Station Counts (20 cities)

| City | Number of Stations |
|------|-------------------|
| 北京 | 23 |
| 天津 | 15 |
| 太原 | 7 |
| 阳泉 | 5 |
| 张家口 | 4 |
| 承德 | 4 |
| 济南 | 4 |
| 朔州 | 4 |
| 石家庄 | 3 |
| 廊坊 | 3 |
| 沧州 | 3 |
| 呼和浩特 | 3 |
| 德州 | 3 |
| 乌兰察布 | 3 |
| 鹤壁 | 3 |
| 唐山 | 2 |
| 秦皇岛 | 2 |
| 保定 | 2 |
| 忻州 | 1 |
| 大同 | 1 |


### Spatial Map
![Station Distribution](station_distribution.png)

## 4. Missing Data Analysis

### Overall Missing Rates (N95 stations, all hours)

| Pollutant | Valid Records | Total Records | Missing Rate |
|-----------|-------------|---------------|--------------|
| O3        | 809,461 | 828,115 | 2.25% |
| PM2.5     | 817,129 | 828,115 | 1.33% |
| PM10      | 815,310 | 828,115 | 1.55% |

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
