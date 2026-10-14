# PREREG (frozen 2026-10-14T05:23:35Z, before any hunt or re-optimisation output)
target: thomson-problem-live-tables (light comparison run, resuming dossier leads 2, 4, 5)
lines of work:
- evaluator-first: numba polisher (tools/fastpol.py); pass iff it reproduces Deeter posted E within 1e-6 for >=5 N.
- contrarian-crosscheck: align Deeter / CCD Riesz s=1 / CCD Thomson2 on overlapping N; flag disagreement beyond rounding at the aligned decimals; re-polish posted coordinates of flagged N; p1 iff posted E differs from own polished file by >1e-6.
- optimizer-defect: tools/hunt.py, 8 workers, 60 min wall, N=505..523 + flagged N<=1500 (512, 516 already in range; 1382 warm from Riesz file), seeds warm+defect kicks / N+1 remove / N-1 add / spiral / RSZ spiral / random; basin hopping T=2e-3, 200 hops/chain.
criterion/threshold: candidate iff min(live tables at N) - E_fine >= 1e-6, then mpmath 30 dps check; at most PROMISING (single-context, unpanelled).
null_test: not needed because results are explicit configurations judged by a deterministic energy checker.
metrics (comparable to morning caphop baseline: 65 chains, 1134 hops, 17.4 hops/chain, ~76 local opts/min over 8 workers): local opts/min, opts per chain, N covered, best gap vs Deeter per N.
