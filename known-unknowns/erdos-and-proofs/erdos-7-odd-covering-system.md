# MOONSHOT - Erdos #7 / Selfridge: a covering system with distinct odd moduli

✏️ **Erdős problems and proofs** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: needs cluster (for search); pure thought for impossibility · open as of 2026-11-19

## The problem

Is there a finite set of congruences a_i mod n_i, with distinct odd moduli n_i > 1, covering every integer? Erdos offered $25; Selfridge later offered $2000 for an explicit example. Known: impossible with odd squarefree moduli (BBMST 2022). Some modulus must be divisible by 3 (Hough-Nielsen 2019). The lcm L is divisible by 9 or 15. Forum (2026, needs re-verification): L is abundant (>= 945), L >= 11,486,475, L has >= 9 distinct prime factors, and some modulus has >= 4 distinct prime factors. Later public bounds on L: L > 1,527,701,174 (a Lean 4 proof, github.com/rw762-sketch/Open-Math-problem, Nov 2026) and L >= 9,704,539,845 with omega(L) >= 9 (Schroeder, Zenodo 10.5281/zenodo.22759614, Sep 2026, unrefereed; its finite computation has since been reproduced exactly by two independent re-implementations).

## What counts as a win

An explicit finite list of (a_i, n_i) with distinct odd n_i > 1 that covers Z, verified by two independent exact checkers. Alternatively, a complete axiom-free proof of impossibility.

## Partial wins

- **p1:** A rigorous proof, checked line by line or in Lean without extra axioms, that L = lcm(n_i) of any odd distinct-moduli covering has at least 10 distinct prime factors (the forum claims >= 9, unrefereed).
- **p2:** A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code.
- **p3:** An axiom-free Lean formalisation of one of the forum's unrefereed necessary conditions (e.g. Schroeder's >= 9 distinct primes in L, or a modulus with >= 4 distinct primes), checked with #print axioms.

## How a win is checked

Let L = lcm(n_i). If L <= ~2e9, sieve a bitset of residues mod L. Otherwise use a recursive CRT check: process the prime-power factors of L layer by layer, tracking uncovered residue classes, as in Nielsen/Krukenberg-style verifiers. Use two independent implementations, and also check distinctness and oddness.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.erdosproblems.com/7>

## Sources

- <https://www.erdosproblems.com/7>
- <https://www.erdosproblems.com/forum/thread/7>
- <https://www.erdosproblems.com/586>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Run the BBMST distortion/sieve LP numerically to map which prime-exponent profiles of L are not excluded, then search only there.
- Nielsen-style tree search (the method that found a covering with minimum modulus 40) adapted to odd moduli: residue trees over primes 3, 5, 7, 11, ... with exact-cover/ILP at each level.
- Prove the strongest rigorous necessary conditions (e.g., >= 10 distinct primes in L) as a publishable partial result.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The forum already has a retracted Lean 'proof' that relied on an impossible axiom.
- Moduli must be distinct.
- Odd squarefree moduli are already impossible.
- Covering 'almost all' integers is not covering all of them.
- Schroeder's prime-count papers are forum postings, not refereed; re-verify before building on them.
- Large exponents alone cannot give a contradiction. If a_0 mod n_0 has v_p(n_0) = v_p(L) and n_0 is the largest such modulus, replacing it by {a_0 + n_0 a_i mod n_0 n_i} over the whole system gives another odd distinct covering on the same primes with v_p(L) doubled. So 'v_3(L) >= E implies no covering' is as hard as the whole problem.
- Clipping the conditional loss at 1 inside a nested convex comparison is invalid (first-order dominance fails once 9 | L), and the cap at 1 is invisible to any convex-order argument. At nine primes with free exponents the best valid functional is about 7.5-8.3% short of the reserve (Schroeder's own rank-ten diagnostic). Treating the prime 7 exactly on the 135-cell anchor does not close it either: an explicit family of seven classes at 7 keeps the refined functional about 2 cells (of 33.75) above the reserve.
- For ten or more prime factors the open case is narrow: after prime replacement, an odd covering with omega(L) = 9 must have 3^4 5^3 7^2 | L and also 3^5, 5^4 or 7^3 | L. A proof of p1 has to defeat exactly these families.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/erdos-and-proofs/erdos-7-odd-covering-system.md
```

Already set up? Say `run V3R1T4S on erdos-7-odd-covering-system`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `erdos-7-odd-covering-system`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
