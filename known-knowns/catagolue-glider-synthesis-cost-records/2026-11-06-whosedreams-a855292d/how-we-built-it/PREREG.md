# PREREG — run 2026-11-06-xs26-confirm, catagolue-glider-synthesis-cost-records, xs26_08ehmkk8z6a87066 (frozen 2026-11-06T16:06:59Z, date -u)

null_test: not needed because the claim is one explicit object (a 12-glider RLE) checked by deterministic Life simulation against a live table value; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The synthesis search already ran, in the main workspace's harvest run 2026-11-03-glider (Nov 3 to Nov 6, 2026), and the
claimed RLE, its verifier output and a three-skeptic panel already exist there (panel written 2026-11-06, about 10:15 to
10:25 ET). That harvest never froze a PREREG.md before building its claims. This file does not pretend otherwise: it is
written now, before this run copies the claim and panel files in, to freeze how THIS run judges the already-built
claim, so the kit checker can evaluate it. Nothing below was chosen to fit a result this run had not yet seen; the
claimed numbers (12 vs 58) were already known when this was written.

## Criterion
Verbatim in target.md (bank success_criterion, main criterion). Not partial win p1: p1 needs a listed cost of at
least 60, and the listed cost is 58.

## Checkers and thresholds
1. Independent checker (attempts/indep-sim, standard-library Python, no lifelib or Shinjuku), written from the
   definition: (a) every generation-0 8-connected component is a glider (one of the 16 phase/orientation shapes);
   (b) rewinding each glider T generations along its own direction, for T = 4 x longer bounding-box side and
   T = 4 x ceil(bounding-box diagonal), the combined pattern equals the union of the separately evolved gliders at
   every generation and returns exactly to generation 0; (c) run forward until a state repeats exactly; the final
   cells must equal the target apgcode's cells (decoded from its extended Wechsler string) under one of the 8
   symmetries plus a translation, with nothing else live; (d) count gliders. Controls: removing each single glider
   in turn must NOT give the target (12 known negatives), and the 11-glider sub-pattern that leaves out the final
   transfer glider must give xs28_651ugmmz69706221 (known positive for a published route).
2. Author's verifier (code/verify_synthesis.py, lifelib + Shinjuku gset rewind_check), re-run once now; it makes one
   live object-page fetch.
3. Live table: object page #CSYNTH line and the xs26 textcensus row, fetched once each (scout.md). Pass only if the
   glider count is STRICTLY below the live true cost on both.
Status allowed: CONFIRMED_SOLUTION only if checks 1 to 3 pass, the existing three-skeptic panel files (reproduce,
novelty, criterion; fresh subagent contexts, 2026-11-06) all end pass: true, the gate copies the criterion
panelist's confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS. Otherwise at most PROMISING.
