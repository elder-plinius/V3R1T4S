# PREREG.v2 — run 2026-10-14-0717 (written 2026-10-14T07:47:47Z, from date -u)

Why a v2: plan change after the first hunt pass (the criterion, statistic, checker and thresholds of PREREG.md are UNCHANGED).
Changes: (1) add the Riesz s=1 rows that no other live table lists, N = 620, 660, 722, 739, 740, 743, 745, 750, 753, 755, 759, 777, 780, 900, 920, 960 (files fetched once each, data/fetch_log.txt), seeded from the Riesz file; (2) phase 2 chains may compose 1..K defect kicks before each polish (--kicks K), same T = 2e-3, 200 hops, restart rule 0.1, 8 workers; (3) re-weight jobs towards Riesz-only rows.
Every new low still goes through the PREREG.md certification (MPFR Newton < 1e-20, Weyl-bounded Hessian, same-routine polish of every posted file, >= 1e-6 below the minimum of all live tables re-fetched before claiming).
null_test: not needed because claims are explicit configurations checked deterministically against table values.
