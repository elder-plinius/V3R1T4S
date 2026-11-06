# Least highway onset for Langton's ant with at most k black cells, k = 0..11 (local V3R1T4S target langton-ant-fT-minimal-seed)

> Target note: langton-ant-fT-minimal-seed is a user-added local target (not in the pinned V3R1T4S bank). It is a
> minimal-seed refinement of the bank's Langton highway target. It is not a claim about the highway conjecture.

## What
For Langton's ant (white right, black left), ant fixed at the origin facing north with y downward, g(k) for k=0..11 is 9977, 310, 162, 126, 67, 62, 49, 45, 40, 24, 17, 0 with minimiser counts 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2 in that frame modulo never-read cells, the 13 seeds in data/minimisers.txt, assuming the blank period-104 highway from update 9977 repeats forever.

(In this package the seed list is object/minimisers.txt; data/minimisers.txt is its name inside the claim folder.)

In plain words: g(k) is the earliest time at which Langton's ant can be on its period-104 highway when it starts on a
grid with at most k black cells. The empty grid takes 9977 updates (the classical value). One black cell brings that
down to 310, four cells to 67, ten cells to 17, and eleven cells can put the ant on the highway at time 0.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g(k) | 9977 | 310 | 162 | 126 | 67 | 62 | 49 | 45 | 40 | 24 | 17 | 0 |
| minimisers | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 |

Equivalently f(T) = least k with g(k) <= T. Onset convention: the number of updates already done when the highway
starts (blank grid 9977, OEIS A126978). how-we-built-it/fsearch/check_onset.py and the brute force print one less
throughout (blank 9976). That is only an indexing difference.

Minimality for k = 1..10 was proved by two separately written exhaustive searches with no shared code (fsearch and
lcone), each with blank and planted-positive controls. k = 1 and 2 were also checked by a box brute force. k = 0 is the
classical blank value, re-simulated. For k = 11 minimality is trivial (onset 0). The two 11-cell minimisers come from
exhaustive time-0 searches over all 104 highway phases by both checkers, and no 10-cell start is on the highway at time 0.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh and python3). Expected last line: `PASS`. Takes about
1 s. It re-simulates the blank grid and every minimiser. To re-prove minimality, rebuild the two searches in
how-we-built-it/ (fsearch and lcone; each finishes all k in a few minutes on one laptop core). See RUN_IT_YOURSELF.md.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| none published | g(k), k = 0..11 | no table found | see the-record-we-beat/RECORD.md | 2026-10-24T01:39:03Z |
| OEIS A126978 | g(0) | 9977 (known) | https://oeis.org/A126978 | 2026-10-24 (panel) |
| Jillhewar 2026 | 11-cell seed on the highway at time 0 | f(0) <= 11 (minimality not claimed there) | https://doi.org/10.21203/rs.3.rs-10516269/v1 | 2026-10-24 (panel) |
| H. Ke, four_cell_port | 4-cell boundary port, tail from 182 | different setting (fixed inward half-plane pose); not a free-grid onset | https://github.com/kehao95/langtons-ant-core | 2026-10-24T01:39:03Z |
| YouTube clip (2026-10-15) | one black cell below the ant | road after 310 steps (a single example, not minimality and not the table) | https://www.youtube.com/watch?v=22dfYC_q_ho | 2026-10-24 (panel) |

These known single points are consistent with our table. Ke's one-black witness list has minimum 310, which matches
g(1), but it is not stated there as a least-onset result. Details: the-record-we-beat/RECORD.md and panel/novelty.md.

## Not claimed
- Nothing about the highway conjecture itself. The result assumes the standard fact that the blank-grid highway from
  update 9977 repeats forever. That was checked numerically (to update 9977+30000 or more), not proved here.
- Only the fixed frame: ant at the origin facing north, y downward. Minimiser counts are for that frame, modulo cells
  that are never read. Other poses follow by rotation and translation, but the counts are not restated for them.
- k >= 12 is moot because g(11) = 0.
- The single values g(0) = 9977, the 11-cell time-0 seed, and a one-cell road at 310 were already public as examples.
  What is new is the full table with proofs of minimality for k = 1..10 and the complete minimiser lists.

## Credits
- C. G. Langton, "Studying artificial life with cellular automata", Physica D 22 (1986). OEIS A126978 (9977).
- Jillhewar, Research Square 2026, doi:10.21203/rs.3.rs-10516269/v1 (exact highway criterion, 11-cell seed).
- H. Ke, https://github.com/kehao95/langtons-ant-core (one-black and four-cell results, Zenodo 10.5281/zenodo.23341609
  and 10.5281/zenodo.23402414).
- Target format and verification method: the V3R1T4S bank (https://github.com/elder-plinius/V3R1T4S).
- Contributor: anonymous. Code and checks by V3R1T4S agent runs.
