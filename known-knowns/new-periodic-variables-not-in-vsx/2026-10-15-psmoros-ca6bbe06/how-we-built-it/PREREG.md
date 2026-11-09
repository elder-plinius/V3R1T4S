# PREREG: run 2026-10-15-1739, target new-periodic-variables-not-in-vsx (written 2026-10-15T17:48:06Z by `date -u`,
# before any light curve of this run was fetched or scored)

null_test: required

This file is frozen once the lenses start. A lens that must refine a line writes a new timestamped file
`PREREG.<line>.v2.md` in the run folder BEFORE fetching the data it will score, with `date -u` and the sha256 of its
code; the report says so. Nothing below may be loosened by such a file.

Shared frozen tools (sha256 from `shasum -a 256` at 2026-10-15T17:49:13Z, paths relative to runs/):
```
5a282bcfc275c5e021ad7984ff3f637bdb21139aafe3bb904065f7e4db2a3692  2026-10-15-1643/attempts/calibrator-v2/code/pipeline.py
3493a309a204bee305a4cde8d5ca1a03a92dea99068a90db57f56b405135358f  2026-10-15-1643/attempts/calibrator-v2/code/params.py
8822324f1aaa65fa5b5d15efec7e3057d03fa90e12f7679326049fdf880c8807  2026-10-15-1643/attempts/calibrator-v2/code/run_many.py
b2a35e292e1b993c0833b614ef4debe589ec1a01b16235b7d782f95227a171e9  2026-10-15-1643/attempts/calibrator-v2/code/decide.py
d438901fb8da176bb464e1d6631fe5a55f7e9af08d2aed3e3360c0b56008a1cc  2026-10-15-1643/attempts/calibrator-v2/code/fetch.py
ee5cba70fa1a38bbc217ffbdf9f77a8f1c67bd4272ec05f876158743e12ec903  2026-10-15-1643/attempts/calibrator-v2/code/fetch_lcs.py
4663077cb8c9ec96ae710ed917501776ab1782417d7cf262f8583d0cf685950b  2026-10-15-1407/code/period_check.py
fe9a6d6f659c095ce091f6820064b58989c65a5909943e0819edd6257a66cf2a  2026-10-15-1407/attempts/skeptic/code/absence_patched.py
```
- S pipeline: "S", "P_rec", "usable LC" and the alias-masked period-pick rule mean exactly what
  runs/2026-10-15-1643/PREREG.v2.md defines, with the code above (identical to the hashes listed in that file). The
  code may be COPIED into a lens folder; copies must hash identically.
- agree(): runs/2026-10-15-1407/code/period_check.py (hash above), unchanged: within 0.1% or exactly 2x.
- Absence checker: runs/2026-10-15-1407/attempts/skeptic/code/absence_patched.py (fixes the defects listed in the
  dossier), plus the dossier's extra catalogs. A failed or blocked catalog query is "unknown", never "absent".
- T = 54.0 (the PREREG.v2 threshold, chosen on spent data).

Access rules: one plain GET per request, User-Agent naming V3R1T4S, pacing >= 1 s per host per lens, no retries after
401/403/405/429/503 or a challenge page (that host is then PENDING TABLE CHECK for the lens). Bulk VSX checks use CDS
B/vsx (version 2026-10-05) via VizieR; the live VSX API only for final pre-claim cones (<= 30 per lens, >= 2 s apart).

## Line A: calibration gate (bank partial win vsx-reproduce-known), lens calibrator-v3

Criterion (verbatim): "vsx-reproduce-known: Pipeline recovers, blind, the VSX period for at least 50 randomly drawn
VSX EW/EA/RRAB/DSCT stars with ZTF coverage (within 0.1% or 2x alias) and reports its own false-alarm rate on 50 VSX
'constant' / non-variable comparison stars; saved as a table (calibration gate)."

A1 (completion of a test frozen before its data, reported, not the claim): finish run 1643's stage B exactly as its
PREREG.md and PREREG.v2.md say, from its fetched files (verify the files listed in its data/fetch_*.tsv), scoring the
control light curves not yet scored with the frozen run_many.py, then the frozen decide.py. Work on a copy inside
attempts/calibrator-v3/; never edit run 1643's folder.

A2 (fresh replication; the only basis for a claim from line A). Same pipeline, same decision rule, fresh draws:
- SEED_C = 20261020 (numpy default_rng). Variable pool: one VizieR query of B/vsx/vsx, Type IN ('EW','EA','RRAB',
  'DSCT') exactly, DEJ2000 > -25, Period not null, 13.5 <= max <= 19.0, MOD(OID,1000) = k where k is the first call
  of default_rng(SEED_C).integers(0,1000) (if k equals run 1407's or run 1643's slice 718, take the next call).
  Exclude every OID drawn in runs 1407 and 1643. Order by the same rng's next call (a permutation). Process in that
  order; stop after EXACTLY 80 variables with usable LCs. Full-precision coordinates (VizieR ASU, F9.5) or a 3" cone.
- Controls: (a) every B/vsx Type = 'CST' star with 13.5 <= max <= 19.0 and -25 < DEJ2000 <= 0, plus every CST with
  DEJ2000 > 0 and max in [13.0, 13.5) or (19.0, 19.5], none used in runs 1407/1643, in default_rng(SEED_C+1)
  permutation order; (b) topped up with Gaia DR3 gaia_source stars, G 13.5-19, dec > -25, NOT in vari_summary and
  phot_variable_flag != 'VARIABLE', by random_index order from random_index >= default_rng(SEED_C+2).integers(0,
  10**9) (first call), excluding runs 1407/1643 Gaia controls; processed until >= 400 controls are usable in total
  (all CST of (a) are processed first; every processed control is counted; none is dropped after scoring).
- LC route: SNAD ZTF DB API v3 latest circle 1.5" (as PREREG.v2), one GET per star.
- Decision (unchanged from run 1643's PREREG.md): Recovered(i) = agree(P_rec, P_vsx); Detected(i) = S(i) > max S over
  ALL A2 controls; PASS iff #(Recovered and Detected) >= 50 of the 80. FAR reported at T = 54.0 and at the realised
  bar, overall, for VSX CST and for Gaia controls separately, with the full S table.
- null_test.md (if line A carries the claim): controls = A2 controls run; best_control = max control S; real = the
  50th-highest S among Recovered A2 variables (0 if fewer than 50); real_beats_all_controls = yes iff real >
  best_control; command = the rerun command.

## Line B: the full criterion (a batch of >= 10 new periodic variables), lens hunter

Criterion: the bank success criterion in target.md, conditions (1)-(7), read literally. Frozen operational choices:
- ZTF leg: S and P_rec from the frozen pipeline. A candidate is Detected only if S > max S over >= 400 controls from
  the SAME ZTF field and CCD-quadrant (ZTF oid prefix oid // 10**8) within +-0.5 mag, Gaia-matched, not in Gaia
  vari_summary and not within 5" of any VSX/Chen+2020/ASAS-SN/ATLAS variable, processed by the identical pipeline;
  the control set for a quadrant is fixed (by a seeded rule written in PREREG.B.v2.md) before candidate S is read.
- Bootstrap FAP (condition 4), per survey: block bootstrap that resamples whole observing nights (ground surveys) or
  1-day blocks (TESS) with replacement, 20,000 replicates on the same frequency grid; FAP = (1 + #replicates whose
  peak power >= the observed peak power) / 20,001; must be < 1e-4.
- Second survey: TESS FFI (TESScut cutout, own aperture photometry), PS1 DR2, CRTS DR2 or ASAS-SN Sky Patrol, named
  per star before its second-survey period is computed. Agreement: agree(P_ZTF, P_2). For an EB-type candidate the
  TESS leg is allowed only if the TESS 10k EB table (arXiv:2506.05631) is obtained, checked and saved.
- Conditions (5) and (6) as written; condition (7): >= 50 VSX CST stars plus enough Gaia non-variable controls for
  >= 400 controls, through the identical two-survey pipeline, must yield zero objects passing (4)-(5).
- Absence (1)-(3): patched checker; the dossier's extra catalogs (Fetherolf+2023, IJspeert+2021, Sesar+2017, Jestin+,
  Kuhn+2021, TESS 10k EB, Gao+2024, unTimely) are also checked; any "unknown" leg blocks a claim.
- A claim needs >= 10 objects passing everything. null_test.md (if line B carries the claim): controls = number of
  controls through the pipeline; best_control = max over controls of the ZTF S; real = min ZTF S over the claimed
  batch; real_beats_all_controls = yes iff real > best_control AND zero controls pass (4)-(5).

## Line C: bank partial win vsx-period-corrections, lens period-corrections

Criterion (verbatim): "vsx-period-corrections: A table of >= 20 VSX entries imported from Gaia DR3 whose VSX period is
a wrong alias (the AAVSO forum notes many are), with the correct period demonstrated in ZTF + a second survey;
checkable by re-folding."
Frozen operational choices:
- Pool: B/vsx entries (VizieR, version 2026-10-05) identified as imported from Gaia DR3 by a rule the lens writes in
  PREREG.C.v2.md BEFORE fetching any light curve (for example the name prefix "Gaia DR3"; the rule must be checked on
  the VSX documentation or records, not on light curves), Period not null, 0.05 <= Period <= 20 d, DEJ2000 > -25,
  13.5 <= max <= 19.0, processed in default_rng(20261021) permutation order.
- ZTF: frozen pipeline -> P_ztf, S. A star is a correction candidate iff S > T = 54.0 AND NOT agree(P_ztf, P_vsx).
- "Wrong alias": f_vsx = |(a/b) f_ztf + m F| within 0.1% of f_vsx, for integers 1 <= a, b <= 4, |m| <= 4, and
  F in {1.0 c/d, 1.0027379093 c/d, 4.0 c/d, 1/62.97 c/d, 1/365.25 c/d}; (a, b, m) = (1, 1, 0) and exact 2x are not
  aliases (they agree). A disagreement outside this family is reported as "disagreement, not an alias" and not
  counted.
- Second survey: TESS FFI, ASAS-SN Sky Patrol, PS1 DR2 or CRTS DR2, chosen per star before its period is computed.
  "Demonstrated" iff the second survey's own highest periodogram peak (0.05-20 d, same alias mask as the pipeline)
  agrees with P_ztf, does not agree with P_vsx, and has block-bootstrap FAP < 1e-4 (20,000 replicates, as line B).
- Novelty screen: a star is excluded from the count if any catalog within 3" (Chen+2020, ASAS-SN variables, ATLAS,
  CRTS, WISE, OGLE, Gaia DR3 vari tables other than the one VSX imported, SIMBAD measurements where readable)
  already gives a period that agrees with P_ztf. Counts before and after the screen are both reported; only the
  screened count counts.
- Null (>= 400 controls): the identical correction pipeline on B/vsx entries NOT imported from Gaia whose VSX period is
  confirmed by an independent catalog (agree() with Chen+2020 or ASAS-SN within 3"), in default_rng(20261022) order.
  Per-star correction score K = S if the star is counted as a demonstrated alias correction, else 0. null_test.md (if
  line C carries the claim): controls = number run; best_control = max K over controls; real = the 20th-highest K
  among screened corrections (0 if fewer than 20); real_beats_all_controls = yes iff real > best_control.
- Claim needs >= 20 screened, demonstrated alias corrections and real > best_control.

## Exploratory (no claim from these)
Anything not frozen above (other catalogs, single-star leads, new statistics) is exploratory and reported as such.
