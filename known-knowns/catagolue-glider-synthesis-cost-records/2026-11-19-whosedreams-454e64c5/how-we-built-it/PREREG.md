# PREREG — packaging run 2026-11-19-harvest-pack, catagolue-glider-synthesis-cost-records, xs31_g8e1ugmmzd553w643, partial win p1 (frozen 2026-11-19T00:33:00Z, date -u)

null_test: not needed because the claim is one explicit object (a 14-glider RLE) checked by deterministic Life simulation against a live table value; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The synthesis search already ran, in the harvest of 2026-11-15, and the claimed RLE and a later scripted 415-object
panel (2026-11-17, single-agent, not a three-skeptic panel) already exist. That harvest never froze a PREREG.md before
building its claims. This file does not pretend otherwise: it is written now, before this packaging run copies the
already-built RLE in, to freeze how THIS run judges the already-built claim. The claimed numbers (14 vs 60)
were already known when this was written. A live Catagolue refetch was required, and was done, immediately before
packaging; if the live cost had been 14 or lower, the object would have been dropped.

## Criterion
Partial win p1, verbatim: a strictly cheaper true glider synthesis for an object whose current listed cost is at least 60, verified as in the main criterion (clauses 1 to 4). The listed cost must be at least 60 and 14 must be strictly below it.

## Checkers and thresholds
1. Independent checker (verify-it-yourself/life_check.py, standard-library Python, no lifelib or Shinjuku):
   (a) every generation-0 8-connected component is a glider; (b) rewinding each glider T generations along its own
   direction, for T = 4 x longer bounding-box side and T = 4 x ceil(bounding-box diagonal), the combined pattern equals
   the union of the separately evolved gliders at every generation and returns exactly to generation 0; (c) run
   forward until a state repeats exactly; the final cells must equal the target apgcode's cells under one of the 8
   symmetries plus a translation, nothing else live; (d) count gliders and require the count to be strictly below the
   live table cost 60.
2. The harvest's own verifier output from 2026-11-15 (how-we-built-it/data/harvest_verify.json, lifelib + Shinjuku) is
   kept as a supporting record. This packaging run treats the standard-library checker as the one a stranger can run
   without extra packages. A prior scripted criterion pass used a fresh lifelib/Shinjuku script; that is not an
   independent cross-check, and it is not what this run relies on.
3. Live table (the-record-we-beat/RECORD.md): pass only if 14 is STRICTLY below the live true cost on the object
   page and in the xs31 textcensus row, and that listed cost is at least 60.
Status allowed: CONFIRMED_PARTIAL (p1) only if checks 1 to 3 pass, a three-skeptic panel (fresh contexts) all end pass: true, the gate copies the criterion panelist's confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS. Otherwise at most PROMISING. This packaging run writes PROMISING and does not stamp CONFIRMED_*.
