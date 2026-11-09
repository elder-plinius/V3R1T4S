<!-- provenance: saved verbatim by the run's main session (Opus 5.5) from the CRITERION skeptic subagent's returned final message (text between its BEGIN/END PANEL markers), 2026-10-15 ~20:24Z; subagents cannot write report-like files. -->
# Panel: CRITERION skeptic

context: subagent (Agent tool), model opus, fresh context seeing only claim/

Claimed partial win (bank, verbatim): "vsx-reproduce-known: Pipeline recovers, blind, the VSX period for at least 50 randomly drawn VSX EW/EA/RRAB/DSCT stars with ZTF coverage (within 0.1% or 2x alias) and reports its own false-alarm rate on 50 VSX 'constant' / non-variable comparison stars; saved as a table (calibration gate)."

The full success criterion is not claimed and not met.

## What I ran (all in a scratch copy; claim/ was not modified)
- I hashed code/*. The five scoring files match the hashes in both prereg files and in results/code_sha_at_decision.txt. The pools and draw orders match results/draw_sha.txt.
- **Draw reproduction.** The first call of default_rng(20261020).integers(0,1000) gives k = 851. Every OID in data/vsx_var_pool_tap.csv has MOD(OID,1000) = 851.
  - The variable pool has 388 rows (EW 268, EA 59, RRAB 48, DSCT 13), all with max between 13.5 and 18.996, Dec > -25 and a Period.
  - data/var_draw_order.csv is exactly the seeded permutation of that pool (0 OIDs removed as previously drawn).
  - data/cst_draw_order.csv is exactly the default_rng(SEED_C+1) permutation of the 76-row CST pool. All 76 are Type CST and meet the prereg magnitude/declination rule.
  - The Gaia pool (1302 rows) lies in [start, start+8000) with start = default_rng(SEED_C+2) first call = 136548133. data/gaia_draw_order.csv is that pool in random_index order. All rows are phot_variable_flag NOT_AVAILABLE, G 13.6 to 19.0, Dec > -25.
- **Fetch logs.**
  - data/fetch_var.tsv covers draws 0..81: 80 usable, 2 with no ZTF object within 1.5". The 80th usable star is draw 81.
  - data/fetch_cst.tsv covers draws 0..75, all of them: 67 usable.
  - data/fetch_gaia.tsv covers draws 0..365: 333 usable, reaching 400 usable controls in total.
  - All requests returned HTTP 200, with no STOP rows. No draws are missing or duplicated, and there is one saved JSON per draw.
  - Every URL uses the draw-order coordinates (0 mismatches).
  - Recomputing the "usable" status from the saved JSON with pipeline.bands gives 0 mismatches. Usability depends only on epoch counts.
- **Rescoring.** I ran REPRODUCE.md step 2 in full: run_many.py on all 82 + 76 + 366 saved light curves, then decide.py. The decision output (apart from its hard-coded command: line), results/vsx_reproduce_known_table.csv and results/controls_table.csv were all reproduced byte for byte.

## Clause by clause
- **"recovers ... the VSX period ... within 0.1% or 2x alias": met.**
  - 77/80 recovered. agree() in code/period_check.py tests |P1-P2|/P2 <= 1e-3 at 1x, and at 2x in either direction. My recomputation from P_rec and P_vsx agrees with the table for all 80.
  - 66 are recovered at P_rec = P_vsx/2 (58 EW, 8 EA) and 11 at 1x (8 RRAB, 3 DSCT).
  - Relative error: median 7.2e-6, maximum 1.3e-4.
  - The CLAIM.md wording "exactly 2x" means 2x within the same 0.1%, which is what the criterion's "2x alias" allows.
  - Failures: CzeV3793 (DSCT), CSS_J054215.5-041105 (EW) and ZTF J200952.16+010924.1 (EA; 2 x P_rec misses by 0.10%). All three are reported, not dropped.
- **"at least 50": met.** The 80 was fixed in the prereg before the draw. It is not "draw until 50 succeed": 77 of 80 is 96%.
  - Chance-agreement null: pairing P_rec(i) with P_vsx(j), j != i, agrees 8/6320 = 0.13% of the time, so about 0.1 chance recoveries would be expected in 80.
  - Pairing control P_rec values with variable P_vsx values agrees 28/32000 = 0.09% of the time.
- **"EW/EA/RRAB/DSCT": met, and all four types are present.** Recovered by type: EW 58/59, EA 8/9, RRAB 8/8, DSCT 3/4. The type match is exact (Type IN ('EW','EA','RRAB','DSCT')).
- **"randomly drawn": met.**
  - The pool is defined only by catalog fields (Type, Dec, max, Period not null, OID slice).
  - The slice and the permutation come from seeds written in prereg/PREREG_run1739.md, and both reproduce exactly.
  - The OID-mod-1000 slice is a seeded systematic 1/1000 sample, not a uniform random draw from all of VSX. Combined with the seeded permutation, I accept it as "randomly drawn".
- **"with ZTF coverage": met.** The rule is a SNAD ZTF object with >= 50 good epochs in zg or zr within 1.5" of the VizieR F9.5 position. It was frozen in PREREG.v2 and does not depend on S. The two stars that failed it are listed in the table.
- **"blind": met.**
  - pipeline.analyze() receives only the SNAD JSON. The keys in the saved files are lc.{mjd, mag, magerr, clrcoeff} and meta.{coord, duration, fieldid, filter, h3, ngoodobs, nobs, rcid}. There is no period and no type.
  - The frequency search is generic (0.01 to 20 c/d; picks restricted to f >= 0.05 c/d).
  - The alias mask, DELTA, FLOW and T were frozen in PREREG.v2 from "spent" run-1407 data. That was a different OID slice (798), and none of this sample's OIDs overlap with it.
  - P_vsx enters only decide.py's agree(), after select().
- **Ruling on vsx_eq_chen (ZTF-derived VSX periods).** According to results/variables.csv, 70 of the 77 recovered VSX periods are identical to a Chen+2020 ZTF period. That column is the claimant's own; I did not re-query Chen+2020. Only 7 recovered stars have VSX periods that do not equal a Chen period, so the strictest reading would leave far fewer than 50.
  - I rule that this does not break "blind". "Blind" means the pipeline has no access to the answer, and it doesn't. The criterion itself specifies ZTF coverage, and excluding ZTF-sourced entries would break "randomly drawn" from VSX: 72% of this pool is ZTF-named.
  - The ruling does limit what the gate shows. It is mainly a reproduction, by a different algorithm on a later and larger ZTF photometry set, of periods that VSX took from ZTF DR2. It is not confirmation by an independent survey. The scope sentence below says so.
  - One informative case: for PS1-3PI J185606.25-173857.2 the Chen period (0.533715) differs from the VSX period by 0.16%, and the pipeline matched VSX (0.534557), not Chen.
- **"reports its own false-alarm rate on 50 VSX 'constant' / non-variable comparison stars": met.**
  - The identical pipeline was run on 67 usable VSX Type-CST stars (>= 50) plus 333 Gaia DR3 non-variables.
  - FAR at the pre-frozen threshold T = 54.0 (set in PREREG.v2 on spent data): 0/67 CST, 0/333 Gaia, 0/400 overall. One-sided 95% upper limits are about 4.4%, 0.9% and 0.75%. This is reported in results/far.txt, results/far.json and results/decide_output.txt.
  - The FAR at the realised bar (the maximum control S, 21.10) is 0 by construction and is not the meaningful number. The T-based result stands without it: 73 of the 77 recovered stars also have S > 54.0.
  - Null model integrity:
    - every processed control is in the table (442 rows);
    - every usable control is scored (400; none usable but unscored);
    - decide.py applies no S-based exclusion;
    - the CST pool was processed exhaustively before the Gaia top-up.
- **"saved as a table": met.** results/vsx_reproduce_known_table.csv and results/controls_table.csv, with extended copies in results/variables.csv and results/controls.csv.

## Prereg timing
- prereg/PREREG.v2_run1643_frozen_statistic.md (statistic, pick rule, usable rule, T, hashes) states 2026-10-15T17:14:05Z.
- prereg/PREREG_run1739.md (seeds, pools, decision rule) states 17:48:06Z.
- Both times are self-declared in the files. The server-generated stamps on the VizieR ASU coordinate responses are 18:01:33Z (data/vsx_var_asu.0.tsv) and 18:01:52Z (data/vsx_cst_asu.0.tsv). Every variable and CST light-curve URL uses those coordinates, so those fetches came after both prereg times. This is consistent with the claim.
- The data/fetch_*.tsv logs have no time column. The timestamped log written by code/fetch_v3.py is not in claim/, so the Gaia fetch time cannot be bounded from claim/. That does not affect the variable recovery or the CST FAR.

## Issues outside the criterion (for the honesty gate and packaging)
1. **Rule 12.** Absolute local paths containing a user name appear in six files:
   - code/decide.py (lines 7 and 95)
   - code/draw_v3.py (line 20)
   - results/decide_output.txt
   - results/decision.txt
   - results/null_test.md
   - prereg/PREREG.v2_run1643_frozen_statistic.md

   decide.py is hash-frozen, so any redaction must be disclosed rather than made silently.
2. Adding the timestamped fetch log would let the fetch times be checked directly.
3. "Non-subsumed": as far as claim/ shows, this is the named partial win itself, computed by the pipeline rather than copied from a catalog. Whether an earlier run already holds this partial win cannot be seen from claim/ and is for the novelty check and the honesty gate.

confirmed_scope: The hash-pinned pipeline in code/, which never reads a catalog period, recovered the B/vsx (2026-10-05) period within 0.1% or at a 2x alias for 77 of 80 seeded-random VSX EW/EA/RRAB/DSCT stars with >= 50 ZTF epochs within 1.5 arcsec (70 of those 77 VSX periods being identical to Chen+2020 ZTF periods per results/variables.csv, so this is mainly a ZTF re-derivation, not independent-survey confirmation), and the identical pipeline on 67 VSX CST stars and 333 Gaia DR3 non-variables reports a false-alarm rate of 0/67 (CST) and 0/400 (all) at the pre-frozen threshold S > 54.0, saved per star in results/vsx_reproduce_known_table.csv and results/controls_table.csv.

pass: true
