import os
import pandas as pd

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '臭氧预测资料', 'xlsx_N95', 'station_loc1.xlsx')

def analyze_stations():
    try:
        df = pd.read_excel(FILE_PATH)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    print("\n" + "="*60)
    print("站点位置信息统计报告")
    print("="*60)
    print(f"\n原始数据列名: {df.columns.tolist()}")
    print(f"\n数据预览（前5行）:")
    print(df.head())
    print(f"\n数据形状: {df.shape}")
    print(f"\n数据描述:")
    print(df.describe(include='all'))
    
    print("\n" + "-"*60)
    print("按城市统计")
    print("-"*60)
    
    if 'city' in df.columns.str.lower():
        city_col = [c for c in df.columns if c.lower() == 'city'][0]
    elif '城市' in df.columns:
        city_col = '城市'
    elif 'city_name' in df.columns.str.lower():
        city_col = [c for c in df.columns if c.lower() == 'city_name'][0]
    else:
        city_col = df.columns[1] if len(df.columns) > 1 else None
    
    if city_col and city_col in df.columns:
        city_counts = df[city_col].value_counts().reset_index()
        city_counts.columns = ['城市', '站点数']
        print(f"\n共 {len(city_counts)} 个城市:")
        print(city_counts.to_string(index=False))
        
        print(f"\n城市分布详情:")
        for _, row in city_counts.iterrows():
            city = row['城市']
            count = row['站点数']
            city_df = df[df[city_col] == city]
            lon_min = city_df['经度'].min() if '经度' in city_df.columns else "N/A"
            lon_max = city_df['经度'].max() if '经度' in city_df.columns else "N/A"
            lat_min = city_df['纬度'].min() if '纬度' in city_df.columns else "N/A"
            lat_max = city_df['纬度'].max() if '纬度' in city_df.columns else "N/A"
            lon_range = f"{lon_min:.4f} ~ {lon_max:.4f}" if isinstance(lon_min, (int, float)) else "N/A"
            lat_range = f"{lat_min:.4f} ~ {lat_max:.4f}" if isinstance(lat_min, (int, float)) else "N/A"
            print(f"  {city}: {count}个站点, 经度范围: {lon_range}, 纬度范围: {lat_range}")
    else:
        print("未找到城市列")
    
    print("\n" + "-"*60)
    print("经纬度分布")
    print("-"*60)
    
    if '经度' in df.columns and '纬度' in df.columns:
        lon_col = '经度'
        lat_col = '纬度'
        
        print(f"\n经度({lon_col}):")
        print(f"  最小值: {df[lon_col].min():.4f}")
        print(f"  最大值: {df[lon_col].max():.4f}")
        print(f"  平均值: {df[lon_col].mean():.4f}")
        print(f"  标准差: {df[lon_col].std():.4f}")
        print(f"  范围: {df[lon_col].max() - df[lon_col].min():.4f}")
        
        print(f"\n纬度({lat_col}):")
        print(f"  最小值: {df[lat_col].min():.4f}")
        print(f"  最大值: {df[lat_col].max():.4f}")
        print(f"  平均值: {df[lat_col].mean():.4f}")
        print(f"  标准差: {df[lat_col].std():.4f}")
        print(f"  范围: {df[lat_col].max() - df[lat_col].min():.4f}")
        
        print(f"\n经纬度范围:")
        print(f"  经度: {df[lon_col].min():.4f}°E ~ {df[lon_col].max():.4f}°E")
        print(f"  纬度: {df[lat_col].min():.4f}°N ~ {df[lat_col].max():.4f}°N")
        
        print(f"\n站点密度估算:")
        lon_span = df[lon_col].max() - df[lon_col].min()
        lat_span = df[lat_col].max() - df[lat_col].min()
        area = lon_span * lat_span
        density = len(df) / area
        print(f"  覆盖区域: {lon_span:.2f}° × {lat_span:.2f}°")
        print(f"  站点密度: {density:.2f} 个/度²")
        
        print("\n全部站点详细信息:")
        print("-"*80)
        print(f"{'序号':<4} {'站点ID':<10} {'城市':<15} {'经度':<12} {'纬度':<12}")
        print("-"*80)
        for idx, row in df.iterrows():
            lon = f"{row[lon_col]:.4f}" if pd.notna(row[lon_col]) else "N/A"
            lat = f"{row[lat_col]:.4f}" if pd.notna(row[lat_col]) else "N/A"
            city = str(row[city_col]) if city_col else "N/A"
            print(f"{idx+1:<4} {str(row.iloc[0]):<10} {city:<15} {lon:<12} {lat:<12}")
    else:
        print("列数不足，无法分析经纬度")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    analyze_stations()