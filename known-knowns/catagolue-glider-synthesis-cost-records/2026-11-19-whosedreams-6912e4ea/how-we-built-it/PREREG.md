# PREREG — run 2026-11-19-seed-pack, catagolue-glider-synthesis-cost-records, xs26_8kk69ba952zw3453, main success criterion (frozen 2026-11-19, before this package was assembled)

null_test: not needed because the claim is one explicit object (a 13-glider RLE) checked by deterministic Life simulation against a live table value; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The synthesis search already ran, in an earlier harvest search (Nov 3 to Nov 6, 2026), and the claimed RLE and its
verifier output already existed from it. That harvest never froze a PREREG.md before building its claims. This file
does not pretend otherwise: it freezes how THIS run judges the already-built claim. The claimed numbers (13 vs 32)
were already known when this was written.

## Criterion
Main success criterion, verbatim in TARGET_CRITERION.md (clauses 1 to 4). Partial win p1 is not sought: the listed
cost 32 is below 60.

## Checkers and thresholds
1. Independent checker (standard-library Python, no lifelib or Shinjuku; packaged as verify-it-yourself/life_check.py, byte-identical
   to the file in the merged #970 package): (a) every generation-0 8-connected component is a glider; (b) rewinding each
   glider T generations along its own direction, for T = 4 x longer bounding-box side and T = 4 x ceil(bounding-box
   diagonal), the combined pattern equals the union of the separately evolved gliders at every generation and returns
   exactly to generation 0; (c) run forward until a state repeats exactly; the final cells must equal the target
   apgcode's cells under one of the 8 symmetries plus a translation, nothing else live; (d) count gliders. Controls:
   removing each single glider must NOT give the target (13 known negatives); the sub-pattern without the added glider
   must give xs27_g88ehmkia4z0178a6.
2. Author's verifier (code/verify_synthesis.py, lifelib + Shinjuku), re-run once now; it does one live object-page fetch.
3. Live table (recorded in the-record-we-beat/RECORD.md): pass only if 13 is STRICTLY below the live true cost on the object page and in the xs26
   textcensus row.
Status allowed: CONFIRMED_SOLUTION only if checks 1 to 3 pass, a three-skeptic panel of fresh contexts all end pass: true, the
gate copies the criterion panelist's confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS. Otherwise at
most PROMISING. This packaging run writes PROMISING only.
