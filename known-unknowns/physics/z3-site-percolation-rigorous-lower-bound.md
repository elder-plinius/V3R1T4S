# Site percolation on the cubic lattice Z^3: a certified lower bound on p_c above Georgakopoulos-Panagiotis's 0.2522 (2023)

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-hours to laptop-days (exhaustive enumeration of walks or animals, a few GB at the largest sizes) · open as of 2026-11-03

## The problem

In site percolation on the simple cubic lattice Z^3, each site is open independently with probability p, and p_c^site(Z^3) is the threshold above which an infinite open cluster exists. Monte Carlo puts it near 0.3116; N. Ball (arXiv:1312.0961) gives the 99.9999% confidence interval [0.3110, 0.3118], which is not a bound. Rigorous lower bounds are much lower. The classical bound p_c >= 1/mu, with Andre Poenitz and Peter Tittmann's connective-constant bound mu(Z^3) <= 4.7387 (Electron. J. Combin. 7 (2000) R21), gives 0.21102; Georgakopoulos and Panagiotis cite about 0.21225 (the inverse of the connective-constant bound of MacDonald et al., J. Phys. A 33 (2000)) as the previous best. Alexander Georgakopoulos and Christoforos Panagiotis (Combin. Probab. Comput. 32 (2023) 912-955, Theorem 7.1; arXiv:2107.06272, eq. (16)) proved p_c^site(Z^3) > 0.2522, calling it the best rigorous lower bound known. Their inequality a(Z^3) >= (1+r)^(1+r)/r^r at r = (1-p_c)/p_c, together with Gill Barequet and Mira Shalah's bound a(Z^3) < 9.3835 on the site-animal growth constant (arXiv:1906.11447), gives exactly 0.252265.... Salvatore Torquato and Yang Jiao (Phys. Rev. E 87 (2013) 032149, arXiv:1302.0332) state 5/19 = 0.263158 for this threshold without proof; they prove 1/6. By the same inequality, an upper bound on a(Z^3) below about 9.3792 gives p_c >= 0.252366, so this target overlaps lattice-animal-growth-constant-certified-bounds. arXiv searches on 2026-10-26 and 2026-11-03 found no published improvement on 0.2522; arXiv:2107.06272 has only version v1. A submission in V3R1T4S PR #571 uses this target id; it is under review and not established.

## What counts as a win

Success means a rigorous lower bound p_c^site(Z^3) >= p0 with p0 at least 1e-4 above the best published rigorous lower bound. That bound is the one found by a search of arXiv, Google Scholar and the works citing arXiv:2107.06272, re-run immediately before claiming. It is currently 0.2522 (exactly 0.252265... from Georgakopoulos-Panagiotis's inequality), so p0 >= 0.252366. The claim is decided by a machine-checkable certificate with three parts. (a) A finite condition at p0, verified by a program in exact integer or rational arithmetic, or in outward-rounded interval arithmetic with an exact final comparison. Examples: an inequality between exact integer counts and p0, or a spectral-radius test with an explicit vector. (b) The program that generates every number the condition uses by exhaustive enumeration from the stated definitions. A stranger must be able to rerun it from scratch, and its runtime and memory must be stated. Its output must match an external anchor where one exists (for example OEIS walk or polycube counts), and a second implementation that shares no code must reproduce it at small sizes. (c) The step from the finite condition to p_c^site(Z^3) >= p0 must be either an exact citation of a published theorem (by number), every hypothesis of which is verified by (a) or is itself a cited published theorem (for example Georgakopoulos-Panagiotis Theorem 7.1's inequality a(Z^3) >= (1+r)^(1+r)/r^r applied to a certified upper bound on a(Z^3) obtained by a published method), or a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry or extra axioms). A new written derivation does not count, however carefully argued; it needs peer review first. Every constant must come from the computation. Floating-point evidence, series or Monte Carlo estimates, and values stated without proof (such as 5/19) do not count.

## Partial wins

- **p1:** A certified improvement, by at least 1e-4, of the best published rigorous lower bound on p_c^site(Z^d) for d = 4, 5 or 6 that the claimant can cite (DOI or arXiv, with page). An example is 1/mu with a published connective-constant bound. The certificate rules are the same. Without a citable comparator it does not count.

## How a win is checked

Skeptic: (1) Run the claimant's exact checker on the archived data at p0 (minutes). (2) Write an independent enumerator from the written definitions. Reproduce the data byte for byte at every size it reaches in an hour, and check the totals against OEIS where they apply. (3) Recheck the final inequality in exact arithmetic with your own code. (4) Check that the cited theorem's statement and hypotheses match exactly what the program verifies, and that the counted objects are exactly the ones the theorem needs; for a formal proof, build it in a clean pinned environment and inspect the theorem statement and its axioms. (5) Optionally, regenerate the largest table (hours).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2107.06272>

## Sources

- <https://arxiv.org/abs/2107.06272>
- <https://doi.org/10.1017/S0963548323000214>
- <https://arxiv.org/abs/1906.11447>
- <https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r21>
- <https://arxiv.org/abs/1302.0332>
- <https://arxiv.org/abs/1312.0961>
- <https://oeis.org/A174319>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Lattice animals: Georgakopoulos-Panagiotis's inequality turns any better certified upper bound on the site-animal growth constant a(Z^3) (currently Barequet-Shalah's 9.3835; about 9.3792 is needed) into a better bound on p_c. Extend Barequet-Shalah's iterative Klarner-Rivest-type process with more computation.
- Exploration processes that force extra closed sites next to the explored path (the spirit of Menshikov-Pelikh and van den Berg-Ermakov in 2D) count only through a published theorem that covers Z^3 or through a kernel-checked proof.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Estimates (about 0.3116) and rigorous confidence intervals (Ball 2013) are not bounds. A 'lower bound' above 0.3116 indicates a bug.
- Torquato and Jiao state 5/19 and 1/5 without proof; only their 1/6 is proved. None of these is the comparator.
- Bond percolation on Z^3 (p_c about 0.2488) is a different model.
- In an exploration process, independence holds only for sites not yet examined. A derivation that reuses examined sites, or that applies the Harris-FKG inequality to events that are not both increasing or both decreasing, gives an invalid bound.
- Floating-point ratios are not certificates. Use exact arithmetic, or outward rounding with an exact final comparison.
- The route p_c >= 1/mu cannot reach the bar: mu(Z^3) is about 4.684, so it tops out near 0.2135.
- A new upper bound on a(Z^3) also wins lattice-animal-growth-constant-certified-bounds; file it once, under one target, and name the other.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/z3-site-percolation-rigorous-lower-bound.md
```

Already set up? Say `run V3R1T4S on z3-site-percolation-rigorous-lower-bound`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `z3-site-percolation-rigorous-lower-bound`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
