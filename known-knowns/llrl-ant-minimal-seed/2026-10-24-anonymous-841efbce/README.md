# Least highway onset for the LLRL ant with at most k non-zero cells, k = 0..5, and K0 = 12 (local V3R1T4S target llrl-ant-minimal-seed, partial win p1)

> Target note: llrl-ant-minimal-seed is a user-added local target (not in the pinned V3R1T4S bank), a fork of the
> bank's Langton highway target. Partial win p1 of that target is claimed, not the full table up to K0.

## What
For LLRL in the fixed frame (origin, facing north, y down), g(0)=256241 on the blank grid; g(1)=555, g(2)=318, g(3)=245, g(4)=195, g(5)=174, each with exactly one minimiser modulo never-read cells, namely (1,0,1), (1,0,2)+(1,-1,1), that pair plus (0,2,3), (-1,0,2)+(0,-1,2)+(0,2,1)+(1,-2,1), and (0,1,3)+(2,1,3)+(0,2,2)+(1,2,3)+(3,0,1); K0=12 with exactly the 10 onset-0 seeds in data/minimisers.txt, and no 11-cell seed has onset 0 on H384.

(In this package the seed list is object/minimisers.txt; data/minimisers.txt is its name inside the claim folder.)

In plain words: LLRL is the 4-colour Langton ant that turns left on colours 0, 1 and 3, right on colour 2, and adds 1
(mod 4) to each cell it leaves. From an empty grid it wanders for 256241 updates and then builds a period-384
highway. g(k) is the earliest time the ant can be on that highway when it starts with at most k non-zero cells.
One cell brings 256241 down to 555, five cells to 174; twelve cells can put the ant on the highway at time 0, and
eleven cannot.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 12 |
|---|---|---|---|---|---|---|---|
| g(k) | 256241 | 555 | 318 | 245 | 195 | 174 | 0 |
| minimisers | 1 | 1 | 1 | 1 | 1 | 1 | 10 |

Onset convention: the number of updates already done when the reads become the blank grid's period-384 highway word.
Minimality for k = 1..5 was proved by two separately written exhaustive searches with no shared code (hsearch: a
first-read DFS with a 384-phase completion test; lcb/lcb_fast: a fixed-depth light-cone DFS with its own blank word and
certificate), each with blank, planted-positive and known-negative controls. g(5) was run twice by hsearch with
different splits (4-way, 284,939,308 nodes; 40-piece queue, 285,750,820 nodes) and once by lcb_fast (542,179,718 leaves).
K0 = 12 comes from exhaustive time-0 searches by both checkers. g(6) to g(11) are not claimed.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh and python3). Expected last line: `PASS`. Takes about
3 s. It re-simulates the blank grid and all 15 listed seeds and checks each enters the blank highway word at exactly the
listed update. To re-prove minimality, rebuild the two searches in how-we-built-it/code (see RUN_IT_YOURSELF.md;
k <= 4 take seconds to minutes, k = 5 about 1 CPU-hour for hsearch and a few CPU-minutes for lcb_fast).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| none published | g(k), k = 1..5; K0 | no table found | see the-record-we-beat/RECORD.md | 2026-10-24T16:05:56Z |
| Gajardo, Lutfalla, Rao (GLR), arXiv 2409.10124 | g(0) | "after 256100 steps" (rounded; ours 256241) | https://arxiv.org/abs/2409.10124 | 2026-10-24T16:05:56Z |
| YouTube video (2026-10-15) | g(0) | "256,241 steps" (blank grid only) | https://www.youtube.com/watch?v=22dfYC_q_ho | 2026-10-24 (panel) |
| Lutfalla simulator presets | onset-0 H384 grid | a 13-cell snapshot (no minimality; not below 12) | https://lutfalla.fr/ant/js/highway.js | 2026-10-24 (panel) |

These known points are consistent with the table. Details: the-record-we-beat/RECORD.md and panel/novelty.md.

## Not claimed
- Nothing about whether highways always appear. The result assumes the H384 highway, once its reads repeat under the
  translation certificate, continues forever (the certificate is a sufficient condition; see how-we-built-it/code/sim/CERT.md).
- Only the fixed frame: ant at the origin facing north, y downward. Minimiser counts are for that frame, modulo cells
  that are never read.
- g(6) to g(11) are open (only g(6) <= 174 is known). The full success criterion of the target is not met.
- Only the period-384 highway is considered; GLR's rare highways (periods 308, 380, 388, 928) are not part of g(k).
- g(0) = 256241 is not new (GLR give it rounded; the video gives it exactly).

## Credits
- A. Gajardo, V. Lutfalla, M. Rao, "Ants on the highway", arXiv 2409.10124 (Natural Computing 2025): the LLRL period-384 highway and blank onset.
- V. Lutfalla, generalized Langton's ants simulator (lutfalla.fr/ant).
- C. G. Langton, "Studying artificial life with cellular automata", Physica D 22 (1986).
- Target format and verification method: the V3R1T4S bank (https://github.com/elder-plinius/V3R1T4S).
- Contributor: anonymous. Code and checks by V3R1T4S agent runs.
