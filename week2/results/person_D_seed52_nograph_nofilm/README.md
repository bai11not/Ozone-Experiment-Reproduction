# Person D 消融实验

**固定**: seed=52, 消融类型: no_graph + no_film

| # | exp_id | 消融 | seq_len | pre_len | d | g | f | 标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|------|---------|---------|---|---|---|------|------|------|-----|------|
| 1 | D01 | no_graph | 12 | 6 | 1 | 0 | 1 | s52-nograph-l12-p6 | ⬜ | | | |
| 2 | D02 | no_graph | 12 | 3 | 1 | 0 | 1 | s52-nograph-l12-p3 | ⬜ | | | |
| 3 | D03 | no_graph | 24 | 6 | 1 | 0 | 1 | s52-nograph-l24-p6 | ⬜ | | | |
| 4 | D04 | no_graph | 24 | 3 | 1 | 0 | 1 | s52-nograph-l24-p3 | ⬜ | | | |
| 5 | D05 | no_film | 12 | 6 | 1 | 1 | 0 | s52-nofilm-l12-p6 | ⬜ | | | |
| 6 | D06 | no_film | 12 | 3 | 1 | 1 | 0 | s52-nofilm-l12-p3 | ⬜ | | | |
| 7 | D07 | no_film | 24 | 6 | 1 | 1 | 0 | s52-nofilm-l24-p6 | ⬜ | | | |
| 8 | D08 | no_film | 24 | 3 | 1 | 1 | 0 | s52-nofilm-l24-p3 | ⬜ | | | |

状态: ⬜待运行 | ✅完成 | ❌失败

```bash
cd week2
bash scripts/run_person_experiments.sh D   # 批量 8 组
```