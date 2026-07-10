# Person A 实验清单

**固定参数**: seed=42, use_diffusion=0 (无扩散)

## 实验列表

| # | exp_id | seq_len | pre_len | use_pe_graph | use_pe_film | 实验标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|---------|---------|--------------|-------------|----------|------|------|-----|------|
| 1 | A01 | 12 | 6 | 0 | 0 | s42-d0-l12-p6-g0-f0 | ⬜ | | | |
| 2 | A02 | 12 | 6 | 0 | 1 | s42-d0-l12-p6-g0-f1 | ⬜ | | | |
| 3 | A03 | 12 | 6 | 1 | 0 | s42-d0-l12-p6-g1-f0 | ⬜ | | | |
| 4 | A04 | 12 | 6 | 1 | 1 | s42-d0-l12-p6-g1-f1 | ⬜ | | | |
| 5 | A05 | 12 | 3 | 0 | 0 | s42-d0-l12-p3-g0-f0 | ⬜ | | | |
| 6 | A06 | 12 | 3 | 0 | 1 | s42-d0-l12-p3-g0-f1 | ⬜ | | | |
| 7 | A07 | 12 | 3 | 1 | 0 | s42-d0-l12-p3-g1-f0 | ⬜ | | | |
| 8 | A08 | 12 | 3 | 1 | 1 | s42-d0-l12-p3-g1-f1 | ⬜ | | | |
| 9 | A09 | 24 | 6 | 0 | 0 | s42-d0-l24-p6-g0-f0 | ⬜ | | | |
| 10 | A10 | 24 | 6 | 0 | 1 | s42-d0-l24-p6-g0-f1 | ⬜ | | | |
| 11 | A11 | 24 | 6 | 1 | 0 | s42-d0-l24-p6-g1-f0 | ⬜ | | | |
| 12 | A12 | 24 | 6 | 1 | 1 | s42-d0-l24-p6-g1-f1 | ⬜ | | | |
| 13 | A13 | 24 | 3 | 0 | 0 | s42-d0-l24-p3-g0-f0 | ⬜ | | | |
| 14 | A14 | 24 | 3 | 0 | 1 | s42-d0-l24-p3-g0-f1 | ⬜ | | | |
| 15 | A15 | 24 | 3 | 1 | 0 | s42-d0-l24-p3-g1-f0 | ⬜ | | | |
| 16 | A16 | 24 | 3 | 1 | 1 | s42-d0-l24-p3-g1-f1 | ⬜ | | | |

状态: ⬜ 待运行 | ✅ 已完成 | ❌ 失败

## 运行命令模板

```powershell
cd week2
.\scripts\run_single_experiment.ps1 `
    -Seed 42 -SeqLen <L> -PreLen <P> `
    -UseDiffusion 0 -UsePEGraph <G> -UsePEFiLM <F> `
    -ExpName "<exp_id>_s42-d0-l<L>-p<P>-g<G>-f<F>"
```

## 批量运行

```powershell
cd week2
.\scripts\run_person_experiments.ps1 -Person A
```