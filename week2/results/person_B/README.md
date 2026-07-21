# Person B 消融实验 (g3)

**固定**: seed=42, 消融: no_pe_graph + no_pe_film

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 | 状态 | RMSE | MAE | MAPE |
|---|------|---------|---------|---|---|---|--------|------|------|-----|------|
| B01 | no_pe_graph | 12 | 6 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p6_l12_s42 | ✅ | 11.30 | 7.99 | 33.33 |
| B02 | no_pe_graph | 12 | 3 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p3_l12_s42 | ✅ | **9.05** | 6.32 | 26.51 |
| B03 | no_pe_graph | 24 | 6 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p6_l24_s42 | ✅ | 11.60 | 8.51 | 35.61 |
| B04 | no_pe_graph | 24 | 3 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p3_l24_s42 | ✅ | 11.50 | 9.31 | 44.61 |
| B05 | no_pe_film | 12 | 6 | 1 | 1 | 0 | g3_pedw_no_pe_film_p6_l12_s42 | ✅ | 12.11 | 8.44 | 33.35 |
| B06 | no_pe_film | 12 | 3 | 1 | 1 | 0 | g3_pedw_no_pe_film_p3_l12_s42 | ✅ | 10.66 | 8.26 | 34.36 |
| B07 | no_pe_film | 24 | 6 | 1 | 1 | 0 | g3_pedw_no_pe_film_p6_l24_s42 | ✅ | 12.06 | 8.87 | 36.57 |
| B08 | no_pe_film | 24 | 3 | 1 | 1 | 0 | g3_pedw_no_pe_film_p3_l24_s42 | ✅ | **9.39** | 6.56 | 27.64 |

状态: ⬜待运行 | ✅完成 | ❌失败

**最优**: B02 (no_pe_graph, seq=12, pre=3) RMSE=9.05
**次优**: B08 (no_pe_film, seq=24, pre=3) RMSE=9.39