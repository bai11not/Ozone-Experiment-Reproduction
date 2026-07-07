# 代码修改记录

## 修改时间：2026-07-06

### 1. 文件夹重命名

**问题**：`d:\时空数据\臭氧预测资料` 下的文件夹 `鑷哀棰勬祴璧勬枡` 是乱码

**解决方案**：重命名为 `臭氧预测资料`

**路径**：`d:\时空数据\臭氧预测资料\臭氧预测资料`

---

### 2. README.md 路径修改

**文件**：[README.md](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/README.md)

**修改内容**：将文档中的 Linux 路径改为本地 Windows 路径

| 行号 | 修改前 | 修改后 |
|------|--------|--------|
| 28 | `/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet` | `d:\时空数据\臭氧预测资料\臭氧预测资料` |
| 39 | `/home/chenxudong/graduate/代码 2/代码/代码/production_internship_pediffwavenet` | `d:\时空数据\臭氧预测资料\臭氧预测资料` |

---

### 3. run_smoke_cpu.sh 设备修改

**文件**：[scripts/run_smoke_cpu.sh](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/scripts/run_smoke_cpu.sh)

**修改内容**：将训练设备从 CPU 改为 GPU，并启用混合精度训练

| 参数 | 修改前 | 修改后 | 说明 |
|------|--------|--------|------|
| `--device` | `cpu` | `cuda` | 使用 GPU 训练 |
| `--exp_name` | `student_smoke_cpu` | `student_smoke_gpu` | 区分实验名称 |
| `--amp` | `0` | `1` | 启用混合精度加速 |

---

### 4. 环境配置建议

**虚拟环境**：使用 Python 3.11 创建虚拟环境 `.venv`

**依赖安装**：
```bash
pip install numpy pandas scikit-learn matplotlib openpyxl geopy torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**WSL 配置**：修改 `.wslconfig` 禁用 Windows PATH 继承以避免路径转换错误

---

### 5. 运行方式

**GPU 训练（推荐）**：
```bash
cd /mnt/d/时空数据/臭氧预测资料/臭氧预测资料
source .venv/bin/activate
bash scripts/run_smoke_cpu.sh
```

**正式训练**：
```bash
DEVICE=cuda EPOCHS=120 EXP_NAME=student_pedw_p6_s42 bash scripts/run_train_pediffwavenet.sh 6 24 42
```

---

### 6. 缺失数据统计脚本

**文件**：[新增代码/analyze_missing_data.py](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/新增代码/analyze_missing_data.py)

**功能**：统计 `data_N95` 目录中 O3、PM2.5、PM10 的缺失情况

**统计结果**：

| 污染物 | 总记录数 | 有效记录 | 缺失记录 | 缺失率 |
|--------|----------|----------|----------|--------|
| O3 | 739,404 | 610,714 | 128,690 | 17.40% |
| PM2.5 | 739,404 | 609,772 | 129,632 | 17.53% |
| PM10 | 739,404 | 612,568 | 126,836 | 17.15% |

**关键发现**：
- 三种污染物缺失率均在 17% 左右，呈系统性缺失
- 2022年全年每一天都存在缺失数据
- 2022-07-15 缺失量最大（O3: 635, PM2.5: 660, PM10: 621）

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料/臭氧预测资料
source .venv/bin/activate
python 新增代码/analyze_missing_data.py
```

---

### 7. 站点位置分析脚本

**文件**：[新增代码/analyze_station_locations.py](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/新增代码/analyze_station_locations.py)

**功能**：统计 95 个站点的城市分布和经纬度信息

**数据来源**：[臭氧预测资料/xlsx_N95/station_loc1.xlsx](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/xlsx_N95/station_loc1.xlsx)

**城市分布**（共 20 个城市）：

| 城市 | 站点数 | 城市 | 站点数 |
|------|--------|------|--------|
| 北京 | 23 | 天津 | 15 |
| 太原 | 7 | 阳泉 | 5 |
| 张家口 | 4 | 承德 | 4 |
| 济南 | 4 | 朔州 | 4 |
| 石家庄 | 3 | 廊坊 | 3 |
| 沧州 | 3 | 呼和浩特 | 3 |
| 德州 | 3 | 乌兰察布 | 3 |
| 鹤壁 | 3 | 唐山 | 2 |
| 秦皇岛 | 2 | 保定 | 2 |
| 忻州 | 1 | 大同 | 1 |

**经纬度范围**：
- 经度：111.5968°E ~ 119.6105°E
- 纬度：35.6822°N ~ 41.0385°N
- 平均经度：115.6370°E
- 平均纬度：39.1953°N
- 站点密度：2.21 个/度²

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料/臭氧预测资料
source .venv/bin/activate
python 新增代码/analyze_station_locations.py
```

---

### 8. 污染物时间序列绘图脚本

**文件**：[新增代码/plot_time_series.py](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/新增代码/plot_time_series.py)

**功能**：绘制 O3、PM2.5、PM10 的日平均浓度时间序列图（含7日滚动平均）

**数据来源**：[臭氧预测资料/data_N95/](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/data_N95) 目录下的 CSV 文件

**输出**：
- 图像文件：`新增代码/output/pollutants_time_series.png`
- 统计摘要：各污染物的平均值、最大值、最小值、标准差及对应日期

**运行方式**：
```bash
cd /mnt/d/时空数据/臭氧预测资料/臭氧预测资料
source .venv/bin/activate
python 新增代码/plot_time_series.py
```

---

### 9. 数据说明文档

**文件**：[数据说明.md](file:///d:/时空数据/臭氧预测资料/臭氧预测资料/数据说明.md)

**功能**：数据集完整说明文档，包含数据概述、目录结构、站点信息、污染物数据、预处理说明、使用建议等

**内容结构**：
1. 数据集概述（数据来源、时间范围、覆盖站点）
2. 数据目录结构
3. 站点信息（城市分布、经纬度分布、空间特点）
4. 污染物数据（数据格式、缺失统计、时间序列统计、季节性特征）
5. 数据预处理说明
6. 使用建议（缺失处理、季节性分析、空间分析）
7. 分析脚本说明