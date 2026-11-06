# Site percolation on the square lattice Z^2: a certified lower bound on p_c above van den Berg-Ermakov's 0.556 (1996) or an upper bound below Wierman-Oberly's 0.666894 (2024)

⚛️ **Physics** · standard · tractability ★★☆☆☆ · compute: laptop-minutes to laptop-hours · open as of 2026-11-06

## The problem

In site percolation on the square lattice Z^2, each site is open independently with probability p. The threshold p_c^site(Z^2) is estimated as 0.59274605079210(2) (Jesper Jacobsen 2015, arXiv:1507.03027), but its rigorous bounds are far looser. Lower bounds: 0.503 (Toth 1985), 0.522 (Zuev 1988) and 0.541 (Mikhail Menshikov and K. D. Pelikh 1989). Then J. van den Berg and A. Ermakov reached 0.556 (Random Structures Algorithms 8 (1996) 199-212; CWI report R 9526). They modified Menshikov-Pelikh's growth-process comparison, using Strassen's coupling theorem and Fisher's inequality p_c(S) + p_c(S*) >= 1 for the matching lattice. Upper bounds: John C. Wierman's substitution method gave 0.679492 (Combin. Probab. Comput. 4 (1995) 181-188). John C. Wierman and Samuel P. Oberly lowered it to 0.666894 (Springer Proc. Math. Stat., 2024), the first improvement since 1995. Searches on 2026-10-26, 2026-11-03 and 2026-11-06 (arXiv) found no published improvement of either bound. A submission in V3R1T4S PR #458 uses this target id; it is under review and not established.

## What counts as a win

Success means either (a) a rigorous lower bound p_c^site(Z^2) >= p0 with p0 >= 0.5561, or (b) a rigorous upper bound p_c^site(Z^2) <= p0 with p0 <= 0.666794. Each must be at least 1e-4 better than the best published bound in that direction. That bound is the one found by a search of arXiv, Google Scholar and the works citing the 1996 paper and the 2024 chapter, re-run immediately before claiming. It is currently 0.556 for (a) and 0.666894 for (b). The claim is decided by a machine-checkable certificate with three parts. (i) A finite condition at p0, verified by a program in exact integer or rational arithmetic, or in outward-rounded interval arithmetic with an exact final comparison. (ii) The program that generates every number the condition uses from the stated definitions. A stranger must be able to rerun it from scratch, and a second implementation that shares no code must recompute the deciding margins. (iii) The step from the finite condition to the bound must be either an exact citation of a published theorem (by number) whose every hypothesis is verified by (i) or is itself a cited published theorem (for example the growth-process comparison of van den Berg-Ermakov with a larger window, or Wierman's substitution method with a larger substitution region, where the cited theorem covers that case as stated), or a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry or extra axioms). A new written derivation does not count, however carefully argued; it needs peer review first. Floating-point evidence and estimates do not count.

## How a win is checked

Skeptic: (1) Rerun the exact checks at p0 with an independent implementation written from the definitions (seconds to hours). (2) As a calibration, use the same code to reproduce the published value of the method being extended: 0.556 for a van den Berg-Ermakov-type lower bound, or 0.679492 for a Wierman-type upper bound. (3) Check that the cited theorem covers the window or substitution region used, as stated, and the direction in which the matching-lattice inequality is used; for a formal proof, build it in a clean pinned environment and inspect its axioms.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://ir.cwi.nl/pub/4915>

## Sources

- <https://doi.org/10.1002/(SICI)1098-2418(199605)8:3%3C199::AID-RSA4%3E3.0.CO;2-T>
- <https://ir.cwi.nl/pub/4915>
- <https://ir.cwi.nl/pub/25488/Thesis_AErmakov.pdf>
- <https://doi.org/10.1017/S0963548300001565>
- <https://doi.org/10.1007/978-3-031-62166-6_9>
- <https://arxiv.org/abs/1507.03027>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Lower bound: van den Berg-Ermakov's growth process conditions on a finite window of the history. Larger windows, checked in exact arithmetic, give more.
- Upper bound: Wierman's substitution method with larger substitution regions, as in Wierman-Oberly 2024.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Estimates (0.5927460508...) are not bounds. A 'lower bound' above it, or an 'upper bound' below it, indicates a bug.
- Use the matching-lattice relation only in the direction that can be cited (Fisher's p_c(S) + p_c(S*) >= 1, as in the 1996 paper).
- Checking marginals is not enough for Strassen's theorem: stochastic domination must hold for every increasing set.
- Floating-point evidence is not a certificate.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/square-site-percolation-rigorous-bounds.md
```

Already set up? Say `run V3R1T4S on square-site-percolation-rigorous-bounds`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `square-site-percolation-rigorous-bounds`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
