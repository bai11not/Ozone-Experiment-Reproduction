# 第二周实验记录 — 李昊泽

**固定参数**: seed=42, seq_len=24, hidden_size=64, epochs=120, batch_size=16, diff_steps=50, lr=7e-4, device=cuda

| # | pre_len | diffusion | PE graph | PE FiLM | 输出目录 | RMSE | MAE | MAPE | 备注 |
|---|:---:|:---:|:---:|:---:|------|:---:|:---:|:---:|------|
| 1 | 1 | 1 | 1 | 1 | ...pedw_p1_l24_s42 | **6.11** | **4.07** | **17.52%** | ✅ epoch 56/68 |
| 2 | 12 | 1 | 1 | 1 | ...pedw_p12_l24_s42 | **14.47** | **10.63** | **41.89%** | ✅ epoch 29/44 |
| 3 | 24 | 1 | 1 | 1 | ...pedw_p24_l24_s42 | **17.42** | **12.58** | **43.69%** | ✅ epoch 20/35 |

## 运行命令

### 实验1
```powershell
$env:PYTHONPATH = "H:\Trae Project\O3predict\code"
python -u code/train_pediffwavenet_noleak.py --device cuda --exp_name "pedw_p1_l24_s42" --pre_len 1 --seq_len 24 --seed 42 --horizon_weights "1.0" --epochs 120 --save_predictions 1
```

### 实验2
```powershell
python -u code/train_pediffwavenet_noleak.py --device cuda --exp_name "pedw_p12_l24_s42" --pre_len 12 --seq_len 24 --seed 42 --horizon_weights "1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0" --epochs 120 --save_predictions 1
```

### 实验3
```powershell
python -u code/train_pediffwavenet_noleak.py --device cuda --exp_name "pedw_p24_l24_s42" --pre_len 24 --seq_len 24 --seed 42 --horizon_weights "1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0" --epochs 120 --save_predictions 1
```
