# Person C 消融实验

**固定**: seed=52, 消融类型: full + no_diff

| # | exp_id | 消融 | seq_len | pre_len | d | g | f | 标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|------|---------|---------|---|---|---|------|------|------|-----|------|
| 1 | C01 | full | 12 | 6 | 1 | 1 | 1 | s52-full-l12-p6 | ⬜ | | | |
| 2 | C02 | full | 12 | 3 | 1 | 1 | 1 | s52-full-l12-p3 | ⬜ | | | |
| 3 | C03 | full | 24 | 6 | 1 | 1 | 1 | s52-full-l24-p6 | ⬜ | | | |
| 4 | C04 | full | 24 | 3 | 1 | 1 | 1 | s52-full-l24-p3 | ⬜ | | | |
| 5 | C05 | no_diff | 12 | 6 | 0 | 1 | 1 | s52-nodiff-l12-p6 | ⬜ | | | |
| 6 | C06 | no_diff | 12 | 3 | 0 | 1 | 1 | s52-nodiff-l12-p3 | ⬜ | | | |
| 7 | C07 | no_diff | 24 | 6 | 0 | 1 | 1 | s52-nodiff-l24-p6 | ⬜ | | | |
| 8 | C08 | no_diff | 24 | 3 | 0 | 1 | 1 | s52-nodiff-l24-p3 | ⬜ | | | |

状态: ⬜待运行 | ✅完成 | ❌失败

```bash
cd week2
bash scripts/run_person_experiments.sh C   # 批量 8 组
```