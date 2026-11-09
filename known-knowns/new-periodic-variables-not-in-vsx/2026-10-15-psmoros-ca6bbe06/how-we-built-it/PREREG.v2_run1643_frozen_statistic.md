# PREREG.v2: run 2026-10-15-1643, calibrator-v2 lens (written 2026-10-15T17:14:05Z by `date -u`, before any fresh light curve of this run was fetched)

Frozen from this point. This file is never edited. It refines PREREG.md (which stays binding) with the stage-A choices.
Code folder: runs/2026-10-15-1643/attempts/calibrator-v2/code (cwd for all commands: attempts/calibrator-v2).

## Statistic S (exact)
pipeline.analyze(d) on the SNAD API v3 circle json d of one star:
- Bands: for zg and zr separately, the ZTF object in the cone with the most good epochs (SNAD `lc` entries) in that
  band; a band is used if it has >= 20 epochs.
- Multi-band periodogram on one common grid f = FMIN..FMAX step 0.2/T (FMIN 0.01, FMAX 20 c/d, T = full span over both
  bands): Z_b(f) = -(N_b - 3)/2 * log10(1 - p_b(f)), p_b = astropy 1-term floating-mean Lomb-Scargle power
  (standard normalization, method 'fast', trig_sum oversampling 2); Z(f) = sum over used bands of Z_b(f).
- The 60 highest local maxima of Z are refined with exact LS (method 'cython') on a +-3 step 61-point grid.
- Split-half replicates: epochs split at the median time of all used epochs (H1 before, H2 at/after);
  Zh1(f), Zh2(f) = the summed Z computed exactly AT f from the H1 (H2) epochs only.
pipeline.select(rec, DELTA=5e-5, FLOW=0.05, MODE='full') (values in code/params.py):
- Period-pick rule: eligible candidates have alias distance > DELTA c/d from every m*day/k + s*b (day in {1 solar,
  1.0027379093 sidereal}, k = 1..4, m >= 0 integer, s = +-1, b in {0, j/29.530589, j/365.25 for j = 1..4}) and
  f >= FLOW (P <= 20 d). f* = the eligible candidate with the largest Z; P_rec = 1/f*. The pipeline never sees P_vsx.
- S = min(Zh1(f*), Zh2(f*)). No eligible candidate -> S = 0, P_rec = NaN.

## Threshold T (for FAR only; the PASS rule is PREREG.md's "beats ALL stage-B controls")
T = 54.0. On spent run-1407 data (out/spent.jsonl, out/stage_a_full.txt): 512 usable controls (CST 165 files /
Gaia 396 files) max S = 53.2 (Gaia control draw 19, P_rec 0.1555 d, amplitude 0.31 mag: probably a real variable);
69/69 spent variables recovered, 68/69 with S > 53.2; 50th-highest recovered S = 133.6.

## Usable LC rule
At least one band (zg or zr) with >= 50 good epochs for the ZTF object chosen in that band, within a 1.5" cone.
Otherwise the star is recorded ("no ZTF object within 1.5 arcsec" / "no band with >= 50 good epochs" /
"fetch error") and skipped. Usability uses epoch counts only, never S.

## LC route (one route for all stage-B stars)
SNAD ZTF DB API v3: https://db.ztf.snad.space/api/v3/data/latest/circle/full/json?ra=&dec=&radius_arcsec=1.5,
one GET per star, User-Agent "V3R1T4S-run (research; honest client)", 0.6 s pacing, no retries; 401/403/429/503 stop
the host. IRSA was not chosen: ~146 s per cone cannot cover ~500 stars before the 18:40Z deadline.
Coordinates: VSX stars from VizieR ASU F9.5 (RAJ2000/DEJ2000 for the TAP-pool OIDs; TAPVizieR stores ~6 significant
digits); Gaia controls at Gaia DR3 ra/dec.

## Draws (already made, no light curves involved; tables in attempts/calibrator-v2/data)
- k_var = 718 (first call of default_rng(20261016); != 798). Pool 322 (EW 236, EA 55, RRAB 24, DSCT 7), sorted by OID,
  permuted by the same rng's next call; 0 OIDs overlap run 1407. Processed in order until EXACTLY 80 usable.
- CST: all 165 B/vsx CST stars (Dec > 0, 13.5 <= max <= 19) had LC requests in run 1407 -> 0 fresh CST controls.
- Gaia: start = default_rng(20261018).integers(0, 1e9) = 694304025. The unbounded TOP-1500 ORDER BY random_index query
  returned HTTP 408 (server timeout; saved); the query actually used bounds random_index to [start, start+8000)
  (740 rows, same order, 0 overlap with run 1407 Gaia controls). Processed in random_index order until 400 usable.
- Run 1407's 6 coordinate-precision misses (var draws 9, 15, 25, 36, 60, 66): ASU F9.5 coordinates, same route, scored
  with the frozen pipeline; reported only.

## Decision (PREREG.md, literally): code/decide.py
Recovered = agree(P_rec, P_vsx) (run-1407 period_check.py, unchanged); Detected = S > max S over all scored stage-B
controls; PASS iff stage B complete (80 variables, >= 400 controls) and #(Recovered and Detected) >= 50.
real = 50th-highest S among Recovered (0 if < 50). FAR = fraction of controls with S > T (by set).
Provenance split: VSX name starting "ZTF " = ZTF-derived; others = other/unknown (B/vsx has no period-reference
column; this proxy is stated as such).

## Commands
```
P=[workspace]/venv/bin/python
$P -I code/fetch_lcs.py var 80 ; $P -I code/fetch_lcs.py gaia 400 ; $P -I code/misses.py
OMP_NUM_THREADS=1 $P -I code/run_many.py out/var.jsonl 4 data/lc_var/*.json      # likewise gaia -> out/gaia.jsonl, lc_miss -> out/miss.jsonl
$P -I code/decide.py ; $P -I code/misses_score.py
```

## sha256 (shasum -a 256, 2026-10-15T17:14:05Z)
```
5a282bcfc275c5e021ad7984ff3f637bdb21139aafe3bb904065f7e4db2a3692  code/pipeline.py
3493a309a204bee305a4cde8d5ca1a03a92dea99068a90db57f56b405135358f  code/params.py
8822324f1aaa65fa5b5d15efec7e3057d03fa90e12f7679326049fdf880c8807  code/run_many.py
b2a35e292e1b993c0833b614ef4debe589ec1a01b16235b7d782f95227a171e9  code/decide.py
d438901fb8da176bb464e1d6631fe5a55f7e9af08d2aed3e3360c0b56008a1cc  code/fetch.py
ee5cba70fa1a38bbc217ffbdf9f77a8f1c67bd4272ec05f876158743e12ec903  code/fetch_lcs.py
36f12c46ab86cb97bf8b5d03be940e6c00583dd18102a8e1af5287c6b4367267  code/draw.py
b43797d216f407a4d12c067f1dfa032bff556c98faf79fd5d06fdd1dd20ba16e  code/misses.py
0a069064c452d2c8c332065a4e8b1ef959a7e7d61350426e7f1f9130c159404f  code/misses_score.py
4663077cb8c9ec96ae710ed917501776ab1782417d7cf262f8583d0cf685950b  runs/2026-10-15-1407/code/period_check.py
bd22a8d41136c55ae6543cf35c0f9a981b355e4be45b9d4c7b51df5901bc391a  data/var_draw_order.csv
7c81113a65fd46e2bda90b9a233e89e983973f422d86805810724bf1148337b3  data/gaia_draw_order.csv
26ffae4ec3bdc13a4747b3b65f2c4fa8a4f2e59cd60cf516b92b968526ee313b  data/cst_draw_order.csv
```
