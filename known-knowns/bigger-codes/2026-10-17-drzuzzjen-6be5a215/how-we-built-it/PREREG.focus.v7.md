# PREREG v7: focused stage on A(26,6,9): plateau-walk stopped by rule; method 3 (kick-regrow) with a calibration gate

frozen_utc: 2026-10-17T02:03:49Z
(frozen before any kick or batch 6 job is run; PREREG.md and v2-v6 unchanged)

## Batch 5 result and the stop (PREREG.md rule)
Batch 5 (2026-10-17T01:02:27Z-02:02:33Z, 11 walks x 2 threads continuing the batch-4 final states, seeds 501-511,
all rc 0): every walk ended at 5996 (2473-2508 rounds), no *_best.json. Batches 4 and 5 are two consecutive batches
without gain, so the plateau-walk search of A(26,6,9) STOPS here. Negative result: about 54,600 further rounds
(batches 4-5) of the default neighbourhood (rmax 8, KB 3) from 11 + 11 distinct 5996 codes found no 5997; the final
states keep moving on the plateau (each 168-213 words from its start per batch, all valid, 02:03:17Z-02:03:32Z,
logs/cur_check_b5/). Best of this cell in this campaign: 5996 (confirmed; reproduced by the Mac 00:28:21Z).

## Method 3: kick-regrow (new; same engine plus a random removal)
Hypothesis: the plateau walk is stuck in a basin of 5996 codes; removing R random words and letting the same engine
regrow can reach other basins. Tool: tools/kick.py (uniform random removal, numpy default_rng(seed)); engine
lb_lns_gen.py unchanged (default neighbourhood), 2 threads, 3600 s, --rounds 1000000.
Batch 6 = calibration batch (60 min, 11 jobs x 2 threads = 22 threads): starts are the 11 batch-5 final states
(seeds/cur_b5/), one kick each:
| R | starts (cur_b5, sorted order) | kick seeds | walk seeds |
|---|---|---|---|
| 25 | 1-3 | 601-603 | 601-603 |
| 50 | 4-6 | 604-606 | 604-606 |
| 100 | 7-9 | 607-609 | 607-609 |
| 200 | 10-11 | 610-611 | 610-611 |
Calibration gate (decided before any result): for each R, the setting is CALIBRATED if at least one of its walks
regrows to >= 5996 (the start size, a value known to be reachable) within the 60 min; an R whose walks all end below
5996 is dead. If no R is calibrated, method 3 is dead and the focused stage on this cell closes with the negative
result. Any code above 5996 is frozen, checked by both checkers and paneled at the batch end as before (immediately
if >= 6001).
Next batch (if any R is calibrated): only calibrated R values, from the best codes; its design is frozen in v8.

Correction appended 2026-10-17T02:04:04Z, before any kick or batch 6 job is run (arithmetic only, no decision changed): batches 4-5 ran 54,412 rounds (27,147 + 27,265, sums of the last 'round' lines of the 22 logs), not 'about 54,600'.
