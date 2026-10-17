# How We Found It (contributor text, unverified)

## Brief & Observation
For `4x5x5` at its best known rank `m = 76` (`fmm_sota.json`), Perminov's live `addition_reduced_ZT` repository lists `cr = 299` (`U 75 + V 95 + W 129 = 299`), and merged V3R1T4S PR `#222` reached `cr = 281`.

## What Failed
Running CSE alone on Perminov's fixed `4x5x5_m76` scheme could not break below `281`, because `U`, `V`, and `W` were locked in a single bilinear basis.

## What Worked
We coupled ternary rank-preserving equivalence flips (`|c| <= 1` over `Z`) with multi-trajectory CSE evaluation (`ternary_addition_reducer`) and DAG exclusive-cone reduction (`dag_cone_collapse.py`), discovering a ternary basis whose straight-line program requires only `75 + 84 + 121 = 280` reduced additions (`cn = 482` naive additions, `fv = 115` fresh variables) while satisfying all `10,000` Brent equations over `Z` with `0` errors.
