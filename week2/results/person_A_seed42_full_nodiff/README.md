# Person A 消融实验

**固定**: seed=42, 消融类型: full + no_diff

| # | exp_id | 消融 | seq_len | pre_len | d | g | f | 标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|------|---------|---------|---|---|---|------|------|------|-----|------|
| 1 | A01 | full | 12 | 6 | 1 | 1 | 1 | s42-full-l12-p6 | ⬜ | | | |
| 2 | A02 | full | 12 | 3 | 1 | 1 | 1 | s42-full-l12-p3 | ⬜ | | | |
| 3 | A03 | full | 24 | 6 | 1 | 1 | 1 | s42-full-l24-p6 | ⬜ | | | |
| 4 | A04 | full | 24 | 3 | 1 | 1 | 1 | s42-full-l24-p3 | ⬜ | | | |
| 5 | A05 | no_diff | 12 | 6 | 0 | 1 | 1 | s42-nodiff-l12-p6 | ⬜ | | | |
| 6 | A06 | no_diff | 12 | 3 | 0 | 1 | 1 | s42-nodiff-l12-p3 | ⬜ | | | |
| 7 | A07 | no_diff | 24 | 6 | 0 | 1 | 1 | s42-nodiff-l24-p6 | ⬜ | | | |
| 8 | A08 | no_diff | 24 | 3 | 0 | 1 | 1 | s42-nodiff-l24-p3 | ⬜ | | | |

状态: ⬜待运行 | ✅完成 | ❌失败

```bash
cd week2
bash scripts/run_single_experiment.sh 42 12 6 1 1 1 "A01_s42-full-l12-p6"   # A01
bash scripts/run_person_experiments.sh A   # 批量 8 组
```