# Results for (d=29, N=60)

Contributor text. This is the row for (d=29, N=60) from the search agent's results table, trimmed on 2026-10-27 to
this row. The agent's other rows are not part of this claim and are not shown. The minimal angle is corrected: the
agent's table gave 88.150016797797149449 degrees, and arccos of the c* below is 88.150016722088 degrees.

| (d, N) | `/plain` cos (12 decimals) | Our c* (12 decimals) | Our c* (30 digits) | Improvement | Minimal angle (degrees) | Contacts within 1e-9 | Table attribution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| (29, 60) | 0.032282791684 | 0.032282689322 | 0.032282689322403249986273377213 | 1.023616e-07 | 88.150016722088 | 1273 | Ilmari Vahteristo, annealing solver |

The search code is `sc_opt.c` (Riemannian L-BFGS on a log-sum-exp smoothing of the largest inner product, with
basin-hopping kicks). The candidate was normalised by a separate 50-digit script, which is not shipped, and its
coordinates are written to 30 significant digits. The active contacts agree only to about 1e-10 (1198 pairs within
1e-10 of c*, 33 within 1e-12). The contact count was recounted on 2026-10-28 with 60-digit arithmetic (the agent's
table gave 1345, which was wrong); `../verify-it-yourself/` does not check it.
