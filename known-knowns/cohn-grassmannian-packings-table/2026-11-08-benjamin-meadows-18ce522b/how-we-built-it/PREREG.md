# PREREG: cohn-grassmannian-packings-table, cell 11-4-66

written_utc: 2026-11-08T02:31Z

## Timing, stated plainly

The object was found by an unattended search lane on 2026-11-06 or 2026-11-07, checked against the table as it read on 2026-11-07 and released in packing-records version 1.3 (https://doi.org/10.5281/zenodo.24046261) on 2026-11-08. This file was written after that and before any panel ran. It freezes the judging, not the search; it is not a pre-registration of the search. The criterion is quoted from the public bank, `bank/targets.json` on the main branch of https://github.com/elder-plinius/V3R1T4S (read 2026-11-08). No threshold or margin below was chosen by us.

## Criterion: cohn-grassmannian-packings-table

> Success means N matrices U_i (m x n, >= 20 significant digits) for an UNSTARRED (m, n, N) row of the live table at https://cohn.mit.edu/grassmannian (re-fetched immediately before claiming) whose note does not say 'optimal packing' or 'proof of optimality', such that after orthonormalising each U_i in mpmath at 50 digits, the minimum over i < j of n - ||U_i^T U_j||_F^2 is STRICTLY GREATER (direction: max) than the table's squared chordal distance for (m, n, N) by at least 1e-9. It must also not exceed the row's listed bound by more than 1e-10 (a larger value means a bug). And no value for (m, n, N) published after the table's last change, found in an arXiv search (Grassmannian / line packing / fusion frame with m, n, N), is larger.

Cell: 11-4-66.

## Statistic and thresholds

Exactly as in the criterion above. The table is re-fetched by the panel. Null test: not applicable; a deterministic construction checked against a definition.

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), new subagents, each seeing only the claim folder and writing its own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
