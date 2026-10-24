# Pre-registration — LABS merit factor records

Sealed 2026-10-24, **before any measurement it describes.**

## 0. Target

`labs-merit-factor-records`: Find a +-1 sequence of length L (67 ≤ L ≤ 600) whose integer
energy E = sum_{k=1}^{L-1} C_k^2 is strictly smaller than the best published energy for that L.

## 1. What is known at sealing time

- Optimal E proven for all L ≤ 66 (Packebusch-Mertens 2016, arXiv:1512.02475).
- Optimal skew-symmetric E proven for odd L ≤ 119 (same).
- arXiv:2504.00987 (2025): improved 16 lengths in 92..120.
- arXiv:2409.07222 (Dimitrov, 2024): search records for L=450-527, F ≈ 7.0-7.5.
- arXiv:2607.09688 (Psenicnik et al., Jun 2026): improved 35 lengths in 450-527 + L=573.
  L=451 reaches F=8.0555. Uses Thompson sampling + parallel self-avoiding walks on GPU.
- GitHub `mdayan8/labs-continuation` (Oct 2026): 31 records at L=463, 464, 485, 528-586 via
  continuation from the 2607.09688 sequences. Not on arXiv.
- GitHub `thakrarsagar/labs`: 5 unverified candidates via endpoint edits. Not on arXiv.
- For L=528-600 (and beyond), the only arXiv-published values are Legendre constructions (F ≈ 6.3).
- For L=587-600, no search results from ANY source exist (not even GitHub repos).

## 2. Plan

**Stage 1 — Legendre baseline**: Generate the best rotated Legendre/Jacobi sequence for every L
in 587-600 as a calibration and seed.

**Stage 2 — Tabu search**: For each L in 587-600, run memetic tabu search with O(L) incremental
energy updates, starting from the Legendre seed and from random +-1 sequences. Use a tabu tenure
of L/4 with aspiration criterion. Multiple restarts (≥20 per length).

**Stage 3 — Continuation**: Also try extending the best L=585 and L=586 sequences from the
mdayan8 repo by ±1/±2 and applying tabu search to the result.

**Stage 4 — Broader search**: If time permits, run the same search on selected L in 121-449
where the best known may be from older searches.

## 3. Forecasts

- Stage 2 will beat Legendre (F ≈ 6.3) at every targeted length. I expect F ≥ 6.8 for most
  lengths, and F ≥ 7.0 for at least half.
- Stage 3 will also beat Legendre but may or may not beat Stage 2.
- The mdayan8 GitHub results (F ≈ 6.3-7.2 for nearby lengths) are the real frontier for L ≈ 587.
  I expect to match or slightly beat their continuation-only approach because I add tabu search.

## 4. Success criterion (from the target)

An explicit +-1 sequence of length L (67 ≤ L ≤ 600) whose exactly computed integer energy E is
STRICTLY SMALLER than the best published energy at verification time, comparing against
arXiv:2607.09688, arXiv:2504.00987, Boskovic et al. records, and any newer arXiv result.
**Compare integer energies, never rounded merit factors.**

## 5. Verification

Compute C_k exactly with integer arithmetic and E = sum C_k^2 as a Python int. Calibrate by
recomputing the energy of a published record sequence for a nearby L.

## 6. Null test

null_test: not needed because the verification is a direct integer computation with no statistical
component — the energy is either strictly less than the baseline or it is not.

## 7. Stopping rule

Stop when all 14 lengths in 587-600 have been searched with at least 20 restarts each, or when
I have records at 5 or more distinct lengths, whichever comes first.
