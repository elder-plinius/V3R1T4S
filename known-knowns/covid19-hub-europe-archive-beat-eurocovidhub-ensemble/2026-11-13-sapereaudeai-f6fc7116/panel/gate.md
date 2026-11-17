# Honesty gate (kit/RUN.md step 7), run 2026-11-13-0539, written 2026-11-13T06:11:42Z

claim: p3 of covid19-hub-europe-archive-beat-eurocovidhub-ensemble (claim/CLAIM.md)

Panel (three fresh subagent contexts, Claude Code Agent tool, each given only claim/):
- REPRODUCE: pass: true. Its own checker, written from the Bracher et al. definition, reproduces all 31,256 rows:
  31,253 exactly in floating point, and the 3 ties are exact half-integers that half-to-even rounding sends to the
  published integers. Under ECDC hospitalisation truth the same 7 models are over 1%, with the same percentages.
  The author's REPRODUCE steps 1-5 give byte-identical outputs. 5 re-fetched files match their sha256.
  It lists wording fixes; none changes a number.
- NOVELTY: pass: true. Status source fetched 2026-11-13T06:01:49Z, HTTP 200, same sha256. It found no earlier public
  independent recomputation of this scores.csv and no V3R1T4S PR or trophy for this target.
  Caveats: GitHub code search needs a login; two Europe PMC full texts returned 500.
  The reconciling OWID rule is stated in the hub's own data-truth README.
- CRITERION: pass: true. The claim meets p3 under the readings frozen in PREREG.md. The OWID file is a legitimate
  "why" under the pre-registered escape hatch; the verdict does not depend on it. Its confirmed_scope is below.

Gate checks:
- No panelist hedges on its verdict; all three end with pass: true.
- No reproduction mismatch: both skeptics who recomputed got the claimed numbers.
- Scope: the CRITERION sentence is no wider than what was reproduced. Not covered: the bias column, files outside
  the 357 fetched files, and other versions of scores.csv.
- p3 is a reproduction, not a record, so "strictly better than the live table" does not apply. The status table
  is unchanged (same sha256) as of 06:01:49Z, less than 6 hours ago.
- No table value obtained by evasion: single honest requests, no retries, no blocked route worked around.
- One object (the per-model reproduction table, with its row-level discrepancy lists).

Wording corrections from the panel. They are applied in the package's text files, never in panel/ or claim/, and
were verified by the main session from command output:
1. Of the 1,642 extra hospitalisation rows under the ECDC file, 1,608 are in 11 other countries. The other 34 are
   Czech weeks with an ECDC value but no OWID value.
2. The fetched files also hold 2,374 negative-horizon keys (-1: 1,383, -2: 754, -3: 237). The parser does not read
   them; they are not hub targets.
3. The 13,252 contrast figure counts matches on wis only.
4. scores.csv is not in fetch_log_all.tsv. Its fetch (2026-11-13T05:39:54Z, HTTP 200, sha256) is in scout.md and
   the-record-we-beat/.

status: CONFIRMED_PARTIAL
confirmed_scope: An independent Python recomputation (no R, no scoringutils) of the wis, sharpness, underprediction and overprediction values of all 31,256 rows (15 models, forecast dates 2023-10-30 to 2024-09-16) of the European COVID-19 Forecast Hub archive's evaluation/scores.csv (sha256 c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c) from the archive's data-processed files and truth data shows that, with the pre-registered ECDC truth for all three targets, exactly 7 models (EuroCOVIDhub-baseline, EuroCOVIDhub-ensemble, Lydia-SARIMA, Lydia-simpleARIMA, epiforecasts-tsensemble, epiforecasts-weeklygrowth, fjordhest-ensemble) have a per-model mean component more than 1% from the published mean (largest 2.14%, Lydia-simpleARIMA underprediction), and that all of this excess comes from the 531 Czech inc hosp rows, which match exactly when scored against the archive's OWID hospitalisation file, under which all 15 models agree within 1% on all four components (max 3.2e-6) and the only 3 non-matching rows are exact half-integer values that half-to-even rounding sends to the published integers.
