# Person B 实验清单

**固定参数**: seed=42, use_diffusion=1 (有扩散)

## 实验列表

| # | exp_id | seq_len | pre_len | use_pe_graph | use_pe_film | 实验标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|---------|---------|--------------|-------------|----------|------|------|-----|------|
| 1 | B01 | 12 | 6 | 0 | 0 | s42-d1-l12-p6-g0-f0 | ⬜ | | | |
| 2 | B02 | 12 | 6 | 0 | 1 | s42-d1-l12-p6-g0-f1 | ⬜ | | | |
| 3 | B03 | 12 | 6 | 1 | 0 | s42-d1-l12-p6-g1-f0 | ⬜ | | | |
| 4 | B04 | 12 | 6 | 1 | 1 | s42-d1-l12-p6-g1-f1 | ⬜ | | | |
| 5 | B05 | 12 | 3 | 0 | 0 | s42-d1-l12-p3-g0-f0 | ⬜ | | | |
| 6 | B06 | 12 | 3 | 0 | 1 | s42-d1-l12-p3-g0-f1 | ⬜ | | | |
| 7 | B07 | 12 | 3 | 1 | 0 | s42-d1-l12-p3-g1-f0 | ⬜ | | | |
| 8 | B08 | 12 | 3 | 1 | 1 | s42-d1-l12-p3-g1-f1 | ⬜ | | | |
| 9 | B09 | 24 | 6 | 0 | 0 | s42-d1-l24-p6-g0-f0 | ⬜ | | | |
| 10 | B10 | 24 | 6 | 0 | 1 | s42-d1-l24-p6-g0-f1 | ⬜ | | | |
| 11 | B11 | 24 | 6 | 1 | 0 | s42-d1-l24-p6-g1-f0 | ⬜ | | | |
| 12 | B12 | 24 | 6 | 1 | 1 | s42-d1-l24-p6-g1-f1 | ⬜ | | | |
| 13 | B13 | 24 | 3 | 0 | 0 | s42-d1-l24-p3-g0-f0 | ⬜ | | | |
| 14 | B14 | 24 | 3 | 0 | 1 | s42-d1-l24-p3-g0-f1 | ⬜ | | | |
| 15 | B15 | 24 | 3 | 1 | 0 | s42-d1-l24-p3-g1-f0 | ⬜ | | | |
| 16 | B16 | 24 | 3 | 1 | 1 | s42-d1-l24-p3-g1-f1 | ⬜ | | | |

状态: ⬜ 待运行 | ✅ 已完成 | ❌ 失败

## 运行命令模板

```powershell
cd week2
.\scripts\run_single_experiment.ps1 `
    -Seed 42 -SeqLen <L> -PreLen <P> `
    -UseDiffusion 1 -UsePEGraph <G> -UsePEFiLM <F> `
    -ExpName "<exp_id>_s42-d1-l<L>-p<P>-g<G>-f<F>"
```

## 批量运行

```powershell
cd week2
.\scripts\run_person_experiments.ps1 -Person B
```