# Person D 实验清单

**固定参数**: seed=52, use_diffusion=1 (有扩散)

## 实验列表

| # | exp_id | seq_len | pre_len | use_pe_graph | use_pe_film | 实验标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|---------|---------|--------------|-------------|----------|------|------|-----|------|
| 1 | D01 | 12 | 6 | 0 | 0 | s52-d1-l12-p6-g0-f0 | ⬜ | | | |
| 2 | D02 | 12 | 6 | 0 | 1 | s52-d1-l12-p6-g0-f1 | ⬜ | | | |
| 3 | D03 | 12 | 6 | 1 | 0 | s52-d1-l12-p6-g1-f0 | ⬜ | | | |
| 4 | D04 | 12 | 6 | 1 | 1 | s52-d1-l12-p6-g1-f1 | ⬜ | | | |
| 5 | D05 | 12 | 3 | 0 | 0 | s52-d1-l12-p3-g0-f0 | ⬜ | | | |
| 6 | D06 | 12 | 3 | 0 | 1 | s52-d1-l12-p3-g0-f1 | ⬜ | | | |
| 7 | D07 | 12 | 3 | 1 | 0 | s52-d1-l12-p3-g1-f0 | ⬜ | | | |
| 8 | D08 | 12 | 3 | 1 | 1 | s52-d1-l12-p3-g1-f1 | ⬜ | | | |
| 9 | D09 | 24 | 6 | 0 | 0 | s52-d1-l24-p6-g0-f0 | ⬜ | | | |
| 10 | D10 | 24 | 6 | 0 | 1 | s52-d1-l24-p6-g0-f1 | ⬜ | | | |
| 11 | D11 | 24 | 6 | 1 | 0 | s52-d1-l24-p6-g1-f0 | ⬜ | | | |
| 12 | D12 | 24 | 6 | 1 | 1 | s52-d1-l24-p6-g1-f1 | ⬜ | | | |
| 13 | D13 | 24 | 3 | 0 | 0 | s52-d1-l24-p3-g0-f0 | ⬜ | | | |
| 14 | D14 | 24 | 3 | 0 | 1 | s52-d1-l24-p3-g0-f1 | ⬜ | | | |
| 15 | D15 | 24 | 3 | 1 | 0 | s52-d1-l24-p3-g1-f0 | ⬜ | | | |
| 16 | D16 | 24 | 3 | 1 | 1 | s52-d1-l24-p3-g1-f1 | ⬜ | | | |

状态: ⬜ 待运行 | ✅ 已完成 | ❌ 失败

## 运行命令模板

```powershell
cd week2
.\scripts\run_single_experiment.ps1 `
    -Seed 52 -SeqLen <L> -PreLen <P> `
    -UseDiffusion 1 -UsePEGraph <G> -UsePEFiLM <F> `
    -ExpName "<exp_id>_s52-d1-l<L>-p<P>-g<G>-f<F>"
```

## 批量运行

```powershell
cd week2
.\scripts\run_person_experiments.ps1 -Person D
```