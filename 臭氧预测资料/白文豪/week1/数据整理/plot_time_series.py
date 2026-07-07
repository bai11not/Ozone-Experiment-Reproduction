import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data_N95')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

pollutants = ['O3', 'PM2.5', 'PM10']

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_time_series():
    csv_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.csv')])
    if not csv_files:
        print("未找到CSV文件")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_data = {p: [] for p in pollutants}
    all_dates = []
    
    for idx, csv_file in enumerate(csv_files):
        file_path = os.path.join(DATA_DIR, csv_file)
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"读取文件失败 {csv_file}: {e}")
            continue
        
        date_str = csv_file.replace('china_sites_', '').replace('.csv', '')
        date = pd.to_datetime(date_str, format='%Y%m%d')
        all_dates.append(date)
        
        station_cols = [col for col in df.columns if col not in ['date', 'hour', 'type']]
        
        for pollutant in pollutants:
            mask = df['type'] == pollutant
            if not mask.any():
                all_data[pollutant].append(np.nan)
                continue
            
            row = df[mask].iloc[0]
            station_data = pd.to_numeric(row[station_cols], errors='coerce')
            daily_mean = station_data.mean()
            all_data[pollutant].append(daily_mean)
        
        if (idx + 1) % 30 == 0:
            print(f"已处理 {idx + 1}/{len(csv_files)} 个文件...")
    
    dates = pd.to_datetime(all_dates)
    
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    colors = {'O3': '#FF6B6B', 'PM2.5': '#4ECDC4', 'PM10': '#45B7D1'}
    units = {'O3': 'μg/m³', 'PM2.5': 'μg/m³', 'PM10': 'μg/m³'}
    
    for i, pollutant in enumerate(pollutants):
        ax = axes[i]
        ax.plot(dates, all_data[pollutant], color=colors[pollutant], linewidth=1.2, alpha=0.8)
        
        ax.fill_between(dates, all_data[pollutant], alpha=0.1, color=colors[pollutant])
        
        rolling_mean = pd.Series(all_data[pollutant], index=dates).rolling(window=7).mean()
        ax.plot(dates, rolling_mean, color=colors[pollutant], linewidth=2.5, linestyle='--', alpha=0.9, label='7-day rolling average')
        
        ax.set_title(f'{pollutant} Daily Mean Concentration Time Series', fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel(f'Concentration ({units[pollutant]})', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend(fontsize=10)
        
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    axes[0].set_xlim(dates.min(), dates.max())
    
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'pollutants_time_series.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n时间序列图已保存到: {output_path}")
    
    print("\n" + "="*60)
    print("时间序列统计摘要")
    print("="*60)
    for pollutant in pollutants:
        data = pd.Series(all_data[pollutant], index=dates).dropna()
        print(f"\n[{pollutant}]")
        print(f"  数据天数: {len(data)}天")
        print(f"  平均值: {data.mean():.2f} {units[pollutant]}")
        print(f"  最大值: {data.max():.2f} {units[pollutant]}")
        print(f"  最小值: {data.min():.2f} {units[pollutant]}")
        print(f"  标准差: {data.std():.2f}")
        
        max_date = data.idxmax().strftime('%Y-%m-%d')
        min_date = data.idxmin().strftime('%Y-%m-%d')
        print(f"  最大值日期: {max_date}")
        print(f"  最小值日期: {min_date}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    plot_time_series()