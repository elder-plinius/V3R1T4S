# PREREG — run 2026-11-19-seed-pack, catagolue-glider-synthesis-cost-records, xs27_08e1ugmicz651346, partial win p1 (frozen 2026-11-19, before this package was assembled)

null_test: not needed because the claim is one explicit object (a 29-glider RLE) checked by deterministic Life simulation against a live table value; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The synthesis search already ran, in an earlier harvest search (Nov 3 to Nov 6, 2026), and the claimed RLE and its
verifier output already existed from it. That harvest never froze a PREREG.md before building its claims. This file
does not pretend otherwise: it freezes how THIS run judges the already-built claim. The claimed numbers (29 vs 62)
were already known when this was written.

## Criterion
Partial win p1, verbatim in TARGET_CRITERION.md: a strictly cheaper true glider synthesis for an object whose current listed cost
is at least 60, verified as in the main criterion (clauses 1 to 4).

## Checkers and thresholds
1. Independent checker (standard-library Python, no lifelib or Shinjuku; packaged as verify-it-yourself/life_check.py, byte-identical
   to the file in the merged #970 package): (a) every generation-0 8-connected component is a glider; (b) rewinding each
   glider T generations along its own direction, for T = 4 x longer bounding-box side and T = 4 x ceil(bounding-box
   diagonal), the combined pattern equals the union of the separately evolved gliders at every generation and returns
   exactly to generation 0; (c) run forward until a state repeats exactly; the final cells must equal the target
   apgcode's cells under one of the 8 symmetries plus a translation, nothing else live; (d) count gliders. Controls:
   removing each single glider must NOT give the target (29 known negatives); the sub-pattern without the added glider
   must give xs27_caar4kl3z330343.
2. Author's verifier (code/verify_synthesis.py, lifelib + Shinjuku), re-run once now; it does one live object-page fetch.
3. Live table (recorded in the-record-we-beat/RECORD.md): pass only if 29 is STRICTLY below the live true cost on the object page and in the xs27
   textcensus row, and that listed cost is at least 60.
Status allowed: CONFIRMED_PARTIAL (p1) only if checks 1 to 3 pass, a three-skeptic panel of fresh contexts all end pass: true, the
gate copies the criterion panelist's confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS. Otherwise at
most PROMISING. This packaging run writes PROMISING only.
