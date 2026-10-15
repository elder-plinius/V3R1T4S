# Robust forecast aggregation, unknown-state conditionally-independent cell: a lower bound > 31/1326 (exact)

## What

In the model of Section 2 of arXiv:2604.24517v2 restricted to the class Pi_CI (two experts whose signals are conditionally independent given a binary state whose values in [0,1] are unknown to the aggregator, squared loss, additive regret against the omniscient aggregator), the uniform mixture of the two explicit rational environments in claim/mixture.json certifies through Yao's principle, as in the proof of that paper's Theorem 3.4, that every aggregation function f has worst-case regret at least 1652448303171916717080006468042849/70681471350112364987160770000000000 ≈ 0.0233788045, which exceeds that paper's lower bound 31/1326 by exactly 612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.22e-7.

(Panel status: CONFIRMED_SOLUTION, `panel/gate.md`. The panel's `claim/mixture.json` is this package's
`object/mixture.json`, byte-identical, sha256 c8c3d23d5e791ec2c2d51a0ce5555fa7af7e9712d0c0ad0acd31f7bdbdc0b971.)

In words: an adversary who picks one of two explicit two-expert environments with probability 1/2 each forces every
aggregation function to have expected regret at least LB = 1652448303171916717080006468042849/70681471350112364987160770000000000
on this mixture, so its worst-case regret is at least LB, and LB > 31/1326 as exact rationals (PROVED-HERE: exact
rational certificate, the same value from three exact computations in two separately written programs, using the
Yao-principle argument of the proof of
Theorem 3.4 of arXiv:2604.24517v2). The two environments are listed in plain JSON in `object/mixture.json`; the
values of `theta`, `prior`, `likelihoods` and `weight` define them, and `mu` and `reports` are declared for the reader
and checked for consistency.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (after `three exact computations agree: LB = 1652448303171916717080006468042849/70681471350112364987160770000000000 > 31/1326; declared fields consistent`).
About 2 seconds on a laptop; needs only `sh` and Python 3 (standard library); nothing is downloaded. Details:
`RUN_IT_YOURSELF.md`; real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| cell | published value | source | URL | fetched (UTC) |
|---|---|---|---|---|
| unknown-state conditionally-independent, lower bound | **31/1326** (printed ≈ 0.023379; exactly 0.0233785822…) | Table 1 and Theorem 3.4 of arXiv:2604.24517v2 (v2 of 23 May 2026) | https://arxiv.org/abs/2604.24517 | 2026-10-15T03:18:04Z, HTTP 200 (first fetched 2026-10-14T17:20:50Z, same sha256 523d3c01…) |
| this object | **1652448303171916717080006468042849/70681471350112364987160770000000000** (≈ 0.0233788045) | `object/mixture.json` | — | — |

Exact margin: 612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.22e-7. Full snapshot with
hashes: `the-record-we-beat/RECORD.md`. The panel's own fetches and searches: `panel/novelty.md`.

## Not claimed

- Nothing about the upper bound 0.025512 of this cell (Theorem 3.2 of the paper), and nothing about the minimax value
  itself: the gap between the two bounds stays almost as wide as before.
- Nothing about the binary-state cell (states known to be {0, 1}; bounds (5√5 − 11)/8 and 0.022599).
- The improvement is about 2.2e-7. Both 31/1326 and the new value print as 0.023379 at the paper's six decimals, so
  the comparison exists only in exact arithmetic: the claim is LB > 31/1326 (exact), nothing about any rounded value.
- The paper also prints "0.02344" once, in the opening sentence of its Section 3.2, as a lower bound. The panel's
  NOVELTY skeptic traced it to a commented-out draft formula in the paper's LaTeX source, with no construction or proof
  anywhere in v1 or v2; Table 1, Theorem 3.4, Figure 1 and the introduction all give 31/1326. This object does not
  reach 0.02344 (it is below it); if a valid certificate for 0.02344 is ever published, it supersedes this one.
- Not a new kind of construction. The object has the same shape as the paper's own Table 3 adversary (the proof of
  Theorem 3.4): two conditionally independent environments with weight 1/2, both experts alike, binary signals, the
  second environment the mirror image of the first under x ↦ 1 − x. Only the numbers move: reports from 1/6 and 5/6 to
  6693/40000 and 33307/40000, states from {0, 5/6} and {1/6, 1} to {0, 33307/40000} and {6693/40000, 1}, and the priors
  accordingly (prior means from 5/12 and 7/12 to 417121/1000000 and 582879/1000000).
- Not optimal and not the end of the search: only two-environment, two-report mixtures were searched for this object.
- The literature check by the panel could not reach some secondary indexes (Semantic Scholar 429, arXiv API 429,
  Google Scholar error page, ACM DL 403; none retried); the primary status source was read (`panel/novelty.md`).
- Not submitted anywhere; the authors were not contacted.

## Credits

- Zhi Chen, Cheng Peng, Wei Tang, "Prior-Agnostic Robust Forecast Aggregation", arXiv:2604.24517
  (https://arxiv.org/abs/2604.24517): the model and definitions used here (Section 2, Lemma 2.1, the class of
  conditionally independent structures in Section 3), the value compared against (31/1326, Table 1 and Theorem 3.4),
  and the Theorem 3.4 construction (Table 3) and Yao-principle argument that this object re-tunes.
- Itai Arieli, Yakov Babichenko, Rann Smorodinsky, "Robust forecast aggregation", PNAS 2018
  (https://arxiv.org/abs/1710.02838): the robust forecast aggregation framework the paper above builds on.
- Tools: Python (standard library `fractions` for every exact check), NumPy (the float search in `how-we-built-it/`).
