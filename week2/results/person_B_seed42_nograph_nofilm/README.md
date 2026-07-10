# Person B 消融实验

**固定**: seed=42, 消融类型: no_graph + no_film

| # | exp_id | 消融 | seq_len | pre_len | d | g | f | 标签 | 状态 | RMSE | MAE | MAPE |
|---|--------|------|---------|---------|---|---|---|------|------|------|-----|------|
| 1 | B01 | no_graph | 12 | 6 | 1 | 0 | 1 | s42-nograph-l12-p6 | ⬜ | | | |
| 2 | B02 | no_graph | 12 | 3 | 1 | 0 | 1 | s42-nograph-l12-p3 | ⬜ | | | |
| 3 | B03 | no_graph | 24 | 6 | 1 | 0 | 1 | s42-nograph-l24-p6 | ⬜ | | | |
| 4 | B04 | no_graph | 24 | 3 | 1 | 0 | 1 | s42-nograph-l24-p3 | ⬜ | | | |
| 5 | B05 | no_film | 12 | 6 | 1 | 1 | 0 | s42-nofilm-l12-p6 | ⬜ | | | |
| 6 | B06 | no_film | 12 | 3 | 1 | 1 | 0 | s42-nofilm-l12-p3 | ⬜ | | | |
| 7 | B07 | no_film | 24 | 6 | 1 | 1 | 0 | s42-nofilm-l24-p6 | ⬜ | | | |
| 8 | B08 | no_film | 24 | 3 | 1 | 1 | 0 | s42-nofilm-l24-p3 | ⬜ | | | |

状态: ⬜待运行 | ✅完成 | ❌失败

```bash
cd week2
bash scripts/run_person_experiments.sh B   # 批量 8 组
```