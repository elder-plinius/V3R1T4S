# PREREG — run 2026-11-06-xs27-confirm, catagolue-glider-synthesis-cost-records, xs27_0ca1ugmicz651346, partial win p1 (frozen 2026-11-06T16:15:47Z, date -u)

null_test: not needed because the claim is one explicit object (a 32-glider RLE) checked by deterministic Life simulation against a live table value; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The synthesis search already ran, in the main workspace's harvest run 2026-11-03-glider (Nov 3 to Nov 6, 2026), and the
claimed RLE, its verifier output and a three-skeptic panel already exist there (panel written 2026-11-06, about 10:20 to
10:23 ET). That harvest never froze a PREREG.md before building its claims. This file does not pretend otherwise: it is
written now, before this run copies the claim and panel files in, to freeze how THIS run judges the already-built
claim, so the kit checker can evaluate it. The claimed numbers (32 vs 66) were already known when this was written.

## Criterion
Partial win p1, verbatim in target.md: a strictly cheaper true glider synthesis for an object whose current listed cost
is at least 60, verified as in the main criterion (clauses 1 to 4).

## Checkers and thresholds
1. Independent checker (attempts/indep-sim, standard-library Python, no lifelib or Shinjuku; the same life_check.py
   written for run 2026-11-06-xs26-confirm, plus a --controls-skip-rewind speed option for the drop-one controls only):
   (a) every generation-0 8-connected component is a glider; (b) rewinding each glider T generations along its own
   direction, for T = 4 x longer bounding-box side and T = 4 x ceil(bounding-box diagonal), the combined pattern equals
   the union of the separately evolved gliders at every generation and returns exactly to generation 0; (c) run
   forward until a state repeats exactly; the final cells must equal the target apgcode's cells under one of the 8
   symmetries plus a translation, nothing else live; (d) count gliders. Controls: removing each single glider must NOT
   give the target (32 known negatives); the sub-pattern without the final glider must give xs27_8ehf8bbgz6430321.
2. Author's verifier (code/verify_synthesis.py, lifelib + Shinjuku), re-run once now; one live object-page fetch.
3. Live table (scout.md): pass only if 32 is STRICTLY below the live true cost on the object page and in the xs27
   textcensus row, and that listed cost is at least 60.
Status allowed: CONFIRMED_PARTIAL (p1) only if checks 1 to 3 pass, the existing three-skeptic panel files (fresh
subagent contexts, 2026-11-06) all end pass: true, the gate copies the criterion panelist's confirmed_scope exactly, and
kit/check_run.py prints CHECK_RUN: PASS. Otherwise at most PROMISING. CONFIRMED_SOLUTION is not sought: the criterion
panelist's confirmed_scope is the p1 sentence.
