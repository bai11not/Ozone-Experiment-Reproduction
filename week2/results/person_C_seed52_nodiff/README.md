# Person C 实验清单

**固定参数**: seed=52, use_diffusion=0 (无扩散)

## 实验列表

| # | exp_id | seq_len | pre_len | use_pe_graph | use_pe_film | 实验标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|---------|---------|--------------|-------------|----------|------|------|-----|------|
| 1 | C01 | 12 | 6 | 0 | 0 | s52-d0-l12-p6-g0-f0 | ⬜ | | | |
| 2 | C02 | 12 | 6 | 0 | 1 | s52-d0-l12-p6-g0-f1 | ⬜ | | | |
| 3 | C03 | 12 | 6 | 1 | 0 | s52-d0-l12-p6-g1-f0 | ⬜ | | | |
| 4 | C04 | 12 | 6 | 1 | 1 | s52-d0-l12-p6-g1-f1 | ⬜ | | | |
| 5 | C05 | 12 | 3 | 0 | 0 | s52-d0-l12-p3-g0-f0 | ⬜ | | | |
| 6 | C06 | 12 | 3 | 0 | 1 | s52-d0-l12-p3-g0-f1 | ⬜ | | | |
| 7 | C07 | 12 | 3 | 1 | 0 | s52-d0-l12-p3-g1-f0 | ⬜ | | | |
| 8 | C08 | 12 | 3 | 1 | 1 | s52-d0-l12-p3-g1-f1 | ⬜ | | | |
| 9 | C09 | 24 | 6 | 0 | 0 | s52-d0-l24-p6-g0-f0 | ⬜ | | | |
| 10 | C10 | 24 | 6 | 0 | 1 | s52-d0-l24-p6-g0-f1 | ⬜ | | | |
| 11 | C11 | 24 | 6 | 1 | 0 | s52-d0-l24-p6-g1-f0 | ⬜ | | | |
| 12 | C12 | 24 | 6 | 1 | 1 | s52-d0-l24-p6-g1-f1 | ⬜ | | | |
| 13 | C13 | 24 | 3 | 0 | 0 | s52-d0-l24-p3-g0-f0 | ⬜ | | | |
| 14 | C14 | 24 | 3 | 0 | 1 | s52-d0-l24-p3-g0-f1 | ⬜ | | | |
| 15 | C15 | 24 | 3 | 1 | 0 | s52-d0-l24-p3-g1-f0 | ⬜ | | | |
| 16 | C16 | 24 | 3 | 1 | 1 | s52-d0-l24-p3-g1-f1 | ⬜ | | | |

状态: ⬜ 待运行 | ✅ 已完成 | ❌ 失败

## 运行命令模板

```powershell
cd week2
.\scripts\run_single_experiment.ps1 `
    -Seed 52 -SeqLen <L> -PreLen <P> `
    -UseDiffusion 0 -UsePEGraph <G> -UsePEFiLM <F> `
    -ExpName "<exp_id>_s52-d0-l<L>-p<P>-g<G>-f<F>"
```

## 批量运行

```powershell
cd week2
.\scripts\run_person_experiments.ps1 -Person C
```