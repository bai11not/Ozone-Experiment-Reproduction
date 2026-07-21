# Person D 消融实验 (g3)

**固定**: seed=52, 消融: no_pe_graph + no_pe_film

| # | 消融 | seq_len | pre_len | d | g | f | 实验名 | 状态 | RMSE | MAE | MAPE |
|---|------|---------|---------|---|---|---|--------|------|------|-----|------|
| D01 | no_pe_graph | 12 | 6 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p6_l12_s52 | ✅ | 11.51 | 8.34 | 34.15 |
| D02 | no_pe_graph | 12 | 3 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p3_l12_s52 | ✅ | 10.40 | 7.80 | 31.11 |
| D03 | no_pe_graph | 24 | 6 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p6_l24_s52 | ✅ | 11.11 | 8.01 | 31.55 |
| D04 | no_pe_graph | 24 | 3 | 1 | 0 | 1 | g3_pedw_no_pe_graph_p3_l24_s52 | ✅ | **9.75** | 7.11 | 29.89 |
| D05 | no_pe_film | 12 | 6 | 1 | 1 | 0 | g3_pedw_no_pe_film_p6_l12_s52 | ✅ | 12.01 | 8.47 | 34.20 |
| D06 | no_pe_film | 12 | 3 | 1 | 1 | 0 | g3_pedw_no_pe_film_p3_l12_s52 | ✅ | 10.81 | 8.29 | 35.00 |
| D07 | no_pe_film | 24 | 6 | 1 | 1 | 0 | g3_pedw_no_pe_film_p6_l24_s52 | ✅ | 11.31 | 7.93 | 30.44 |
| D08 | no_pe_film | 24 | 3 | 1 | 1 | 0 | g3_pedw_no_pe_film_p3_l24_s52 | ✅ | 9.82 | 7.16 | 30.40 |

**最优**: D04 (no_pe_graph, seq=24, pre=3) RMSE=9.75