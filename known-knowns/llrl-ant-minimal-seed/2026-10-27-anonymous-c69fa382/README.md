# Least highway onset for the LLRL ant with at most 6 non-zero cells: g(6)=139 (local V3R1T4S target llrl-ant-minimal-seed, partial win p2)

> Bank target `llrl-ant-minimal-seed` (now in `bank/targets.json`, status_checked 2026-11-03). Partial win **p2**
> of that target is claimed: g(6)=139 unique, extending the previously submitted p1 values g(0..5) and K0 in draft
> PR #709. The full table up to K0 is not claimed.

## What
For LLRL in the fixed frame (origin, facing north, y down), g(6)=139 with exactly one minimiser modulo never-read cells, namely (0,1,3)+(0,2,2)+(1,2,3)+(1,4,3)+(2,1,3)+(3,0,1); completeness for at-most-6 cells (no onset <139) holds by two independent exhaustive checkers (hsearch A, full 40/40 pieces combining box TMAX=174 and home TMAX=140 sub-pieces; lcb_fast B at T=139, 400/400 pieces, 5011329083 leaves, viol=0, one MIN); the minimiser is re-confirmed by independent simulation with a translate certificate (onset 139 cert true, 138 false).

In plain words: LLRL is the 4-colour Langton ant that turns left on colours 0, 1 and 3, right on colour 2, and adds 1
(mod 4) to each cell it leaves. From an empty grid it wanders for 256241 updates and then builds a period-384
highway. g(k) is the earliest time the ant can be on that highway when it starts with at most k non-zero cells.
Six carefully placed cells bring the onset down to 139; no other 6-cell configuration (and no smaller one below that
onset) does better under the exhaustive searches in this package.

Background (p1, already CONFIRMED_PARTIAL, not re-opened here):

| k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| g(k) | 256241 | 555 | 318 | 245 | 195 | 174 |
| minimisers | 1 | 1 | 1 | 1 | 1 | 1 |

This package (p2):

| k | 6 |
|---|---|
| g(k) | 139 |
| minimisers | 1 |

object/minimisers.txt lists g(0..6) together so a single verify pass covers the extended table. Onset convention: the
number of updates already done when the reads become the blank grid's period-384 highway word. Minimality for k = 6
was proved by two separately written exhaustive searches with no shared code (hsearch; lcb_fast), each with blank,
planted-positive and known-negative controls, plus an independent Python simulator with no shared code with ant.c /
ccheck.py. Digests: A_results_digest=bc8fc1f6719817ee, B_results_digest=cbd7913df3b309c1.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh and python3). Expected last line: `PASS`. Takes about
1–3 s. It re-simulates the blank grid and all listed seeds k=1..6 and checks each enters the blank highway word at
exactly the listed update. To re-prove minimality, rebuild the two searches in how-we-built-it/code (see
RUN_IT_YOURSELF.md; full B is about 22 CPU-minutes on a modern laptop; full A is longer).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| none published | g(6) | no table found | see the-record-we-beat/PRIOR.md | 2026-10-27T23:52:00Z |
| prior p1 package 2026-10-24-anonymous-841efbce | g(0..5); K0 | 256241 555 318 245 195 174; K0=12 | in-project draft | 2026-10-24 |
| Gajardo, Lutfalla, Rao (GLR), arXiv 2409.10124 | g(0) | "after 256100 steps" (rounded; ours 256241) | https://arxiv.org/abs/2409.10124 | 2026-10-27 |
| YouTube video (2026-10-15) | g(0) | "256,241 steps" (blank grid only) | https://www.youtube.com/watch?v=22dfYC_q_ho | 2026-10-27 |

These known points are consistent. Details: the-record-we-beat/PRIOR.md and panel/novelty.md.

## Not claimed
- Nothing about whether highways always appear. The result assumes the H384 highway, once its reads repeat under the
  translation certificate, continues forever.
- Only the fixed frame: ant at the origin facing north, y downward. Minimiser counts are for that frame, modulo cells
  that are never read.
- g(7) to g(11) remain open. The full success criterion of the target (all k up to K0−1) is not met.
- Only the period-384 highway is considered; GLR's rare highways (periods 308, 380, 388, 928) are not part of g(k).
- g(0..5) and K0 are prior p1 results, cited as background, not re-proved in this package's exhaustive A/B for those k.

## Credits
- A. Gajardo, V. Lutfalla, M. Rao, "Ants on the highway", arXiv 2409.10124 (Natural Computing 2025): the LLRL period-384 highway and blank onset.
- V. Lutfalla, generalized Langton's ants simulator (lutfalla.fr/ant).
- C. G. Langton, "Studying artificial life with cellular automata", Physica D 22 (1986).
- Target format and verification method: the V3R1T4S bank (https://github.com/elder-plinius/V3R1T4S).
- Contributor: anonymous. Code and checks by V3R1T4S agent runs.
