# PREREG: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 29)

written_utc: 2026-11-19T05:09Z

## Timing, stated plainly

The object was found by unattended numerical search jobs that ran on 2026-11-17 and 2026-11-18 (UTC). It has not been published anywhere before this claim (it is not in packing-records and not in our open pull request 20 to the leaderboard repository). This file was written after the search and before any panel ran. It freezes the judging, not the search; it is not a pre-registration of the search. The criterion is quoted from the public bank, `bank/targets.json` on the main branch of https://github.com/elder-plinius/V3R1T4S (read 2026-11-19). No threshold or margin below was chosen by us, except the extra bar against open pull requests, which only makes the claim stricter.

## Criterion: game-of-sloanes-complex-line-packings

> Success means n unit vectors in C^d, 3 <= d <= 7, for a (d,n) row of the live leaderboard (https://github.com/gnikylime/GameofSloanes README table, re-fetched live immediately before claiming) whose coherence mu = max_{j<k} |<phi_j,phi_k>|, computed in mpmath at 40 digits after normalising each vector, is STRICTLY LOWER (direction: min) than the listed 'Best Coherence' by at least 1e-8 (the table's resolution and the maintainers' stated acceptance threshold), the row is not marked provably optimal, mu is at least the listed lower bound (a value below it means a bug), and the vectors are given to >= 16 significant digits in the repository's file format (real parts of all vectors vector-by-vector, then imaginary parts).

Cell: (d, n) = (7, 29).

## Statistic and thresholds

Exactly as in the criterion above: leaderboard Best Coherence minus mu >= 1e-8, mu >= the listed lower bound, row not marked provably optimal, every coordinate written with >= 16 significant digits. Extra bar set by us before the panel: mu is at least 1e-7 below the coherence of every packing for this cell in the open pull requests to https://github.com/gnikylime/GameofSloanes, our own pull request 20 included. The README and the pull requests are re-read by the panel. Null test: not applicable; a deterministic construction checked against a definition.

## Panel

Three fresh reviewers (REPRODUCE, NOVELTY, CRITERION), each started in a new context for its role, each seeing only the claim folder (CLAIM.md and object/) and the public pages, and each writing its own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
