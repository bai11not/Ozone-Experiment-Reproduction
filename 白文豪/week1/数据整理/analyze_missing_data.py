import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '臭氧预测资料', 'data_N95')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

pollutants = ['O3', 'PM2.5', 'PM10']

def analyze_missing_data():
    csv_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.csv')])
    if not csv_files:
        print("未找到CSV文件")
        return

    total_records = {p: 0 for p in pollutants}
    total_missing = {p: 0 for p in pollutants}
    total_valid = {p: 0 for p in pollutants}
    
    date_missing = {}
    total_stations = 0

    for idx, csv_file in enumerate(csv_files):
        file_path = os.path.join(DATA_DIR, csv_file)
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"读取文件失败 {csv_file}: {e}")
            continue
        
        station_cols = [col for col in df.columns if col not in ['date', 'hour', 'type']]
        
        if total_stations == 0:
            total_stations = len(station_cols)
        
        date_str = csv_file.replace('china_sites_', '').replace('.csv', '')
        
        for pollutant in pollutants:
            mask = df['type'] == pollutant
            if not mask.any():
                continue
            
            row = df[mask].iloc[0]
            station_data = row[station_cols]
            
            records = len(station_data)
            missing = station_data.isna().sum() + (station_data == '').sum()
            valid = records - missing
            
            total_records[pollutant] += records
            total_missing[pollutant] += missing
            total_valid[pollutant] += valid
            
            if missing > 0:
                if date_str not in date_missing:
                    date_missing[date_str] = {}
                date_missing[date_str][pollutant] = int(missing)
        
        if (idx + 1) % 30 == 0:
            print(f"已处理 {idx + 1}/{len(csv_files)} 个文件...")

    print("\n" + "="*60)
    print("数据缺失统计报告")
    print("="*60)
    print(f"总文件数: {len(csv_files)}")
    print(f"时间范围: {csv_files[0].replace('china_sites_', '').replace('.csv', '')} ~ {csv_files[-1].replace('china_sites_', '').replace('.csv', '')}")
    print(f"站点数: {len(station_cols)}")
    print(f"总小时数: {len(csv_files) * 24}")
    print("\n" + "-"*60)
    
    for pollutant in pollutants:
        total = total_records[pollutant]
        missing = total_missing[pollutant]
        valid = total_valid[pollutant]
        missing_rate = (missing / total) * 100 if total > 0 else 0
        
        print(f"\n[{pollutant}]")
        print(f"  总记录数: {total:,}")
        print(f"  有效记录: {valid:,}")
        print(f"  缺失记录: {missing:,}")
        print(f"  缺失率: {missing_rate:.2f}%")
    
    print("\n" + "-"*60)
    print("按日期统计缺失情况（仅显示有缺失的日期）")
    print("-"*60)
    
    sorted_dates = sorted(date_missing.keys())
    for date in sorted_dates:
        date_info = date_missing[date]
        missing_str = ", ".join([f"{p}: {v}个" for p, v in date_info.items()])
        print(f"  {date}: {missing_str}")
    
    print("\n" + "="*60)
    
    results = []
    for pollutant in pollutants:
        total = total_records[pollutant]
        missing = total_missing[pollutant]
        valid = total_valid[pollutant]
        missing_rate = (missing / total) * 100 if total > 0 else 0
        results.append({
            'Pollutant': pollutant,
            'Total_Records': total,
            'Valid_Records': valid,
            'Missing_Records': missing,
            'Missing_Rate': missing_rate
        })
    
    summary_df = pd.DataFrame(results)
    summary_path = os.path.join(OUTPUT_DIR, 'missing_data_summary.csv')
    summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
    print(f"\n缺失数据统计摘要已保存到: {summary_path}")
    
    date_missing_df = pd.DataFrame(date_missing).T.fillna(0)
    date_missing_df = date_missing_df.sort_index()
    date_missing_path = os.path.join(OUTPUT_DIR, 'missing_data_by_date.csv')
    date_missing_df.to_csv(date_missing_path, encoding='utf-8-sig')
    print(f"按日期缺失统计已保存到: {date_missing_path}")
    
    with open(os.path.join(OUTPUT_DIR, 'missing_data_report.txt'), 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("数据缺失统计报告\n")
        f.write("="*60 + "\n")
        f.write(f"总文件数: {len(csv_files)}\n")
        f.write(f"时间范围: {csv_files[0].replace('china_sites_', '').replace('.csv', '')} ~ {csv_files[-1].replace('china_sites_', '').replace('.csv', '')}\n")
        f.write(f"站点数: {len(station_cols)}\n")
        f.write(f"总小时数: {len(csv_files) * 24}\n")
        f.write("\n" + "-"*60 + "\n")
        for pollutant in pollutants:
            total = total_records[pollutant]
            missing = total_missing[pollutant]
            valid = total_valid[pollutant]
            missing_rate = (missing / total) * 100 if total > 0 else 0
            f.write(f"\n[{pollutant}]\n")
            f.write(f"  总记录数: {total:,}\n")
            f.write(f"  有效记录: {valid:,}\n")
            f.write(f"  缺失记录: {missing:,}\n")
            f.write(f"  缺失率: {missing_rate:.2f}%\n")
    print(f"完整报告已保存到: {os.path.join(OUTPUT_DIR, 'missing_data_report.txt')}")

if __name__ == '__main__':
    analyze_missing_data()