# Site percolation on the cubic lattice Z^3: an explicit certified upper bound on p_c below Campanino-Russo's 1/2 (1985)

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-hours (exhaustive checks over all states of a finite block, a few GB) · open as of 2026-11-06

## The problem

In site percolation on the simple cubic lattice Z^3, each site is open independently with probability p, and p_c^site(Z^3) is the threshold above which an infinite open cluster exists. Monte Carlo puts it near 0.3116, which is an estimate, not a bound. The best published rigorous upper bound is Massimo Campanino and Lucio Russo's theorem p_c^site(Z^3) < 1/2 (Ann. Probab. 13 (1985) 478-491). Its published abstract states only the strict inequality, with no explicit constant below 1/2. Geoffrey Grimmett (arXiv:1604.04849, Section 6, Theorem 6.2) writes that it may still be the best rigorous upper bound known, and that a small explicit epsilon could be calculated from its proof; none has been published. Table 1 of Pablo A. Gomes, Alan Pereira and Remy Sanchis (J. Appl. Probab., arXiv:2106.10388v2, 13 March 2026) lists 0,5000 for site percolation in d = 3 with that reference. They feed it into their Theorem 2.3 to get explicit upper bounds in dimensions 4 to 9. Comparison with a plane inside Z^3 gives only p_c^site(Z^3) <= p_c^site(Z^2) <= 0.666894 (John C. Wierman and Samuel P. Oberly, 2024), which is weaker. Searches on 2026-10-26, 2026-11-03 and 2026-11-06 (arXiv) found no published explicit bound below 1/2. A submission in V3R1T4S PR #481 uses this target id; it is under review and not established.

## What counts as a win

Success means a rigorous upper bound p_c^site(Z^3) <= p0 with an explicit rational p0 at least 1e-4 below the best published explicit rigorous upper bound. That bound is the one found by a search of arXiv, Google Scholar and the works citing Campanino-Russo (1985) and arXiv:2106.10388, re-run immediately before claiming. It is currently 1/2, so p0 <= 0.4999. The claim is decided by a machine-checkable certificate with three parts. (a) A finite condition at p0, verified by a program in exact integer or rational arithmetic, or in outward-rounded interval arithmetic with an exact final comparison. An example is a stochastic-domination or block-renormalisation inequality over all states of a finite block. (b) The program that generates every number the condition uses, exhaustively over the finite state space, from the stated definitions. A stranger must be able to rerun it from scratch, and its runtime and memory must be stated. A second implementation that shares no code must reproduce its counts, at least on a smaller block. (c) The step from the finite condition to p_c^site(Z^3) <= p0 must be either an exact citation of a published theorem (by number), every hypothesis of which is verified by (a) or is itself a cited published theorem (inputs such as Campanino-Russo's theorem must be cited theorems, not estimates), or a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry or extra axioms). A new written derivation, such as a new coupling argument, does not count, however carefully argued; it needs peer review first. Floating-point evidence and Monte Carlo estimates do not count.

## Partial wins

- **p1:** A certified explicit upper bound on p_c^site(Z^d), for some 4 <= d <= 9, at least 1e-4 below the value for that d in Table 1 of Gomes-Pereira-Sanchis (arXiv:2106.10388v2), or below a better published bound the claimant finds. The certificate rules are the same. A bound obtained only by feeding a new Z^3 bound into their Theorem 2.3 is part of the main win, not this partial win.

## How a win is checked

Skeptic: (1) Rerun the claimant's checker over the whole finite state space (minutes to hours, a few GB). (2) Rebuild the state space and its counts independently from the written definitions and compare. (3) Recheck the final comparisons in exact arithmetic with your own code. (4) Check that the cited theorem's statement and hypotheses match exactly what the program verifies, including the direction of every inequality; for a formal proof, build it in a clean pinned environment and inspect the theorem statement and its axioms. If the proof is a chain of certificates, check that every link starts from a value proved by a cited theorem or by an earlier link.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2106.10388>

## Sources

- <https://doi.org/10.1214/aop/1176993004>
- <https://arxiv.org/abs/2106.10388>
- <https://doi.org/10.1017/jpr.2025.10041>
- <https://arxiv.org/abs/1604.04849>
- <https://doi.org/10.1007/978-3-031-62166-6_9>
- <https://arxiv.org/abs/1312.0961>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Block growth processes with Strassen's coupling theorem, as in van den Berg-Ermakov (1996) for Z^2, carry over to 3D blocks. The domination check is finite and can be made exhaustive.
- Planes inside Z^3 give only Z^2 bounds. Combining several planes, or using slabs, needs a certified coupling.
- Gomes-Pereira-Sanchis's Theorem 2.3 turns any Z^3 bound into bounds in dimensions 4 to 9.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Estimates (about 0.3116) and rigorous confidence intervals (Ball 2013) are not bounds. An 'upper bound' below 0.3116 indicates a bug.
- Campanino and Russo's p_c < 1/2 is strict but not explicit. A claim must beat 1/2 itself by the margin, not 'Campanino-Russo minus epsilon'.
- Bond percolation is a different model: the cubic-lattice bond bounds (for example 0.347297, Yu and Wierman 2021) say nothing about site percolation.
- Checking marginals is not enough for Strassen's theorem: stochastic domination must hold for every increasing set.
- Floating-point evidence is not a certificate. Use exact arithmetic, or outward rounding with an exact final comparison.
- A new block-renormalisation or Strassen-coupling argument in 3D is a new proof, not a citation; it counts here only as a kernel-checked formal proof.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/z3-site-percolation-rigorous-upper-bound.md
```

Already set up? Say `run V3R1T4S on z3-site-percolation-rigorous-upper-bound`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `z3-site-percolation-rigorous-upper-bound`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
