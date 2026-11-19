# PREREG: spherical-codes-cohn-table, cell 29-727

written_utc: 2026-11-08T02:31Z

## Timing, stated plainly

The object was found by an unattended search lane on 2026-11-06 or 2026-11-07, checked against the table as it read on 2026-11-07 and released in packing-records version 1.3 (https://doi.org/10.5281/zenodo.24046261) on 2026-11-08. This file was written after that and before any panel ran. It freezes the judging, not the search; it is not a pre-registration of the search. The criterion is quoted from the public bank, `bank/targets.json` on the main branch of https://github.com/elder-plinius/V3R1T4S (read 2026-11-08). No threshold or margin below was chosen by us.

## Criterion: spherical-codes-cohn-table

> Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Cell: 29-727.

## Statistic and thresholds

Exactly as in the criterion above. The table is re-fetched by the panel. Null test: not applicable; a deterministic construction checked against a definition.

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), new subagents, each seeing only the claim folder and writing its own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
