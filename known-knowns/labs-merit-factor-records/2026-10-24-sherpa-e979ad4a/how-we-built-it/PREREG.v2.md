# Pre-registration v2 — GPU skew-symmetric self-avoiding-walk search, LABS

Sealed 2026-10-24T16:20:50Z (from `date -u`), **before any search output on the lengths below exists.** `PREREG.md` (CPU plan,
L = 587..600, sealed earlier today) is left unedited. Its line of work is closed as a dead lens and reported in
`attempts/cpu-optimizer/report.md`. This document opens a new round; it does not reinterpret the old one.

## 0. What is known at sealing time (all from calibration on lengths outside the target set, or from the literature)

- GPU kernels are correct: the move energies match brute force for every move at 16 lengths 5..599, and the tracked
  energies stay exact over long runs. On solved cells the memetic tabu searcher reaches the proven skew optima at
  L = 107, 113 and 119 in 2-18 s and never goes below them.
- Against strong published *search* records the searcher is weak. With 2-5 min per length it reaches F 6.86 at L = 461
  (Dimitrov 7.54), and warm starts from Dimitrov's L = 499 sequence give no improvement. **The planned 401..449
  attack is therefore not run.** Those calibration results are recorded in `attempts/calibration/`.
- At L = 579 (calibration, outside the target set) the self-avoiding-walk mode reaches F 6.687 in 180 s; the
  Legendre construction there gives 6.25.
- Literature (see `scout.md`): for the 22 odd lengths below there is **no tabulated value in any source** (the bank's
  named sources, Dimitrov 2022, arXiv:2409.07222, arXiv:2607.09688, the borkob archive). The only public values are
  rotated/periodically-extended Legendre constructions and, at neighbouring lengths only, GitHub mdayan8's
  continuation sequences (528..536 and 567..586).

## 1. Criterion (verbatim from the bank)

Success means an explicit +-1 sequence of length L with 67 <= L <= 600 whose exactly computed integer energy E = sum_{k>=1} C_k^2 is STRICTLY SMALLER (direction: min) than the best published energy for that L at verification time, taken as the minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. LABS records repository cited there, and any newer arXiv result. Compare integer energies, never rounded merit factors. For L <= 66 the optimum is proven; lower energy there means a bug.

How it is applied here: for these lengths none of the named tables lists a value, so "best published energy" is
replaced by a **stricter bar** B(L) = the minimum of (a) the best rotated, periodically extended Legendre sequence
over every prime 0.80L <= p <= 1.10L, every rotation and both choices at multiples of p; (b) every public sequence of
length L (mdayan8 GitHub, arXiv:2607.09688 L = 573); and (c) every end-derivation of those public sequences from
lengths L-4..L+4 (remove 0..2 and add 0..2 symbols at each end, all signs). Computed exactly by `code/legendre_bar.py`
into `data/bar_soft_odd.json`. **A record at L requires an explicit sequence with integer energy E < B(L).** Before any
claim is made, the novelty step must also search for other construction tables at these lengths (e.g. Baden 2011,
Jedwab-Katz-Schmidt 2013). If one is lower, it replaces B(L).

## 2. Target set and bars (frozen)

| L | B(L) | F at bar | source |
|---|---|---|---|
| 537 | 22716 | 6.3473 | Legendre p=503 rot=113 chi0=1 |
| 539 | 22941 | 6.3319 | Legendre p=503 rot=111 chi0=1 |
| 541 | 23110 | 6.3323 | Legendre p=503 rot=109 chi0=1 |
| 543 | 23395 | 6.3015 | Legendre p=503 rot=107 chi0=1 |
| 545 | 23544 | 6.3079 | Legendre p=503 rot=105 chi0=1 |
| 547 | 23809 | 6.2835 | Legendre p=503 rot=103 chi0=1 |
| 549 | 24066 | 6.262 | Legendre p=503 rot=101 chi0=1 |
| 551 | 24187 | 6.2761 | Legendre p=523 rot=109 chi0=1 |
| 553 | 24344 | 6.281 | Legendre p=523 rot=111 chi0=1 |
| 555 | 24429 | 6.3045 | Legendre p=523 rot=109 chi0=1 |
| 557 | 24598 | 6.3064 | Legendre p=523 rot=109 chi0=1 |
| 559 | 24811 | 6.2972 | Legendre p=523 rot=114 chi0=1 |
| 561 | 24964 | 6.3035 | Legendre p=541 rot=125 chi0=-1 |
| 563 | 25097 | 6.3149 | Legendre p=523 rot=110 chi0=1 |
| 565 | 25274 | 6.3153 | Legendre p=523 rot=109 chi0=1 |
| 587 | 27477 | 6.2701 | Legendre p=563 rot=413 chi0=1 |
| 589 | 27562 | 6.2935 | Legendre p=563 rot=411 chi0=1 |
| 591 | 27707 | 6.3031 | Legendre p=563 rot=409 chi0=1 |
| 593 | 27876 | 6.3074 | Legendre p=563 rot=406 chi0=1 |
| 595 | 28041 | 6.3126 | Legendre p=563 rot=405 chi0=1 |
| 597 | 28254 | 6.3072 | Legendre p=563 rot=403 chi0=1 |
| 599 | 28479 | 6.2994 | Legendre p=571 rot=420 chi0=1 |

## 3. Method (frozen; code hashes below)

`code/gpu/search.py --mode saw --walk 4000 --prandom 0.5 --pcross 0.9 --heads auto --exploit 0.7 --top-arms 6`,
skew-symmetric space, head-partition arms r1 = round(0.0545L)+-2, r2 = round(0.0279L)+-2, r3 = round(0.0209L)+-1,
**300 s per length**, seed = 1000 + L, one length at a time on the GPU, in the order 587, 589, ..., 599, 537, ..., 565.
Every walk starts from a random sequence inside its arm or from a recombination of this run's own pool. **No published
or constructed sequence is ever used as a seed**, so a result cannot be an end-extension of a published instance.

- `data/bar_soft_odd.json` sha256 2df7dd3aadb90e407a251720111128192e17dd544441f2ae1d133ef5eb01fbf3
- `code/gpu/skew_kernels.cu` sha256 c366e248c1a87f54b8e988e5b9a2e9974979f25c642a21a1df22c6cfef16898a
- `code/gpu/search.py` sha256 89923c635120db49c025e4f31f1e3f147fe393e551a2af88011627e7c656077b
- `code/gpu/labsgpu.py` sha256 84d54ed2acd7b38f4512956dd1d5380bb1a4e832a8a14b987c35ce7c7022ecfc
- `code/check_labs.py` sha256 494fca5cc04c39094d5e1c5ca0180664540e63c172bfd01ed23b1d29dd0914b1
- `code/legendre_bar.py` sha256 d294e843bd4d955c2d69c67f3ee6278d8793b3a41e0cbb2a63bac9cfd508ec2c

## 4. Verification of each candidate (before any claim)

1. `code/check_labs.py SEQ --L L --below B(L)` (Python standard library, independent of the search code) prints PASS.
2. Recomputed again with numpy integer correlation; length and alphabet checked; skew symmetry reported.
3. Distance to every bar-defining and derived sequence at length L, minimised over the 8 energy-preserving symmetries
   (reversal, negation, alternating negation), is reported. Below L/10 would be flagged as a possible near-copy.

## 5. Forecast (written before the run)

- The bar is beaten at **>= 20 of the 22** lengths, by 4-10% in energy, with F >= 6.55 at >= 15 lengths and the best
  F <= 6.95.
- No F >= 7.2 anywhere (that would be suspicious at this budget and would trigger a bug hunt before any claim).
- Results are *first search values* at these lengths, not improvements on anyone's search. The report and claim
  will say so plainly.

## 6. Reporting and stopping

Every length in the set is run with the frozen budget and reported, including failures. After the first pass,
remaining budget may go to a second pass of up to 600 s per length on any length. That pass uses the same method and
is reported as a separate line. Any change of method is a new `PREREG.v3.md`. Stop starting new searches at
20:40 UTC.

null_test: not needed because each claim is an explicit sequence whose exact integer energy is checked by a deterministic checker against a fixed numeric bar
