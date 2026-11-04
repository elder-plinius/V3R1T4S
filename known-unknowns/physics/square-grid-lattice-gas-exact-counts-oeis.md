# Exact partition functions of lattice gases on n x n boards: the next term of OEIS A028420 (monomer-dimer), A006506 (hard squares), A063443 (kings/1x1-2x2 tilings), A054759 (square ice on the torus) or A027683 (hard squares on the torus)

⚛️ **Physics** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

Exact unit-activity partition functions of classic lattice models on n x n boards are tabulated in OEIS and extended by a few people: A028420 (monomer-dimer coverings = all matchings of the n x n grid) b-file to n = 27 (Liang Kai; n <= 21 Jennifer Henry); A006506 (hard squares = independent sets of the n x n grid) b-file to n = 39 (Jin-Guo Liu; earlier terms Robert Gerbicz, Paolo Butera and Marco Pernici, Casey Mills Davis); A063443 (tilings by 1x1 and 2x2 squares = non-attacking kings) to n = 40 (Andrew Woods, Vaclav Kotesovec, Johan Nilsson); A054759 (Eulerian orientations of the n x n torus = square ice, six-vertex model at the ice point) to n = 14 (Brendan McKay, 2024-04-18); A027683 (independent sets of the n x n torus) to n = 32 (Rintaro Matsuo). All checked live 2026-10-15. Column-by-column transfer matrices with modular arithmetic (several 62-bit primes and Chinese remaindering) make the next term of A028420 (2^28 frontier states, about 226-digit answer) and A006506 (Fibonacci-many frontier states, F(42) = 2.7e8 at width 40) and A063443 (comparable) laptop-hours to laptop-days computations; A054759 is much easier and is listed as a partial win.

## What counts as a win

Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N is one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before claiming, computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a different decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer run), with the same code reproducing every published term for n <= N-1 exactly, and the result consistent with the known growth constant: a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant, or, when the entropy constant's finite-size correction is larger than 1e-3 at that N (measured as n^2*(ln a(n)/n^2 - ln W) on the PUBLISHED terms nearest N), consistency with the finite-size model ln a(n) = W2*n^2 + A + B/n with W2 fixed at ln(entropy constant), requiring |ln(a(N)/predicted a(N))| < 2e-3 and reporting both the literal deviation and the model residual. This keeps the clause checkable at small N, where the literal tolerance can exceed any correct value's deviation (observed on A054759: the published a(14) deviates 5.5e-3 from Lieb's constant and n^2*(ln a/n^2 - ln W) = 1.08 is stable over every published term n = 4..14, so the literal 1e-3 clause first becomes attainable only around N >= 33 for that sequence).

## Partial wins

- **p1:** The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard squares on the n x n torus), same two-run and reproduction rules; A054759 is expected to be easy (row transfer matrix with 2^n states plus one tracked boundary edge) and is a partial only.
- **p2:** A new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n) extending the largest published m by one for all n up to the published range, same rules.

## How a win is checked

Skeptic (< 1 hour): rerun the claimant's program modulo one fresh 62-bit prime not used in the claim and check the residue of a(N); rerun for all n <= 20 and compare with the b-file; check digit count against the entropy-constant growth estimate. Full recomputation (hours) can follow the panel.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A028420>

## Sources

- <https://oeis.org/A028420>
- <https://oeis.org/A006506>
- <https://oeis.org/A063443>
- <https://oeis.org/A054759>
- <https://oeis.org/A027683>
- <https://arxiv.org/abs/2505.12776>
- <https://arxiv.org/abs/2507.04007>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Broken-profile dynamic programming with one 32/64-bit counter per frontier state, run once per prime modulus (about 13 primes for a 226-digit A028420 term), parallel over primes across cores; memory is about 8 bytes x 2^28 per array for A028420(28).
- From signal processing / FFT practice: exploit the left-right reflection symmetry of the frontier to halve states, as Liang and Liu did with tensor-network contractions.
- From tensor networks (Jin-Guo Liu's GenericTensorNetworks approach): an exact contraction with an optimised order and big-integer or modular tensors is a genuinely independent second method.
- From number theory: random-prime residue checks (Freivalds-style) let a skeptic validate a 300-digit claim in minutes without redoing all primes.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Offsets differ (A028420 starts at n = 0, A054759 at n = 1); a 'new' term at the wrong index is an existing one.
- Torus conventions for tiny n (multi-edges and loops at n = 1, 2) change the small terms; reproduce the published small terms before trusting the code.
- CRT with too few primes silently returns the value modulo the product; check the bound on a(N) (from the entropy constant) is below the modulus product with a wide margin.
- These sequences also fall under the bank's generic OEIS 'more' target; claims belong here only under this entry's two-run and reproduction rules. Some terms may sit in a pending OEIS edit; check the sequence's history page.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/physics/square-grid-lattice-gas-exact-counts-oeis.md
```

Already set up? Say `run V3R1T4S on square-grid-lattice-gas-exact-counts-oeis`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `square-grid-lattice-gas-exact-counts-oeis`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
