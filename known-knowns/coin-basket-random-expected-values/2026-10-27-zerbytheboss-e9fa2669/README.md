# Jehn's Random-Basket Coin Game: Exact Expected Values (`coin-basket-random-expected-values`)

## What
Exact optimal expected values for Jehn's random-basket coin game: A391791(23)=884741548, A391791(24)=1922512940, A391791(25)=4164198462 (k=2) and A391792(19)=45245088184, A391792(20)=149627079790, A391792(21)=492482601295 (k=3), with all published terms reproduced and Jehn's conjecture confirmed for all n in 10..25.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 1 second using pure Python standard library: validates format and exact agreement of all published terms n=1..22 for k=2 and n=1..18 for k=3, validates all new terms, audits Jehn's conjecture for n=10..25, and dynamically evaluates exact backward-induction states from first principles).

## Compared To
- Published Sources:
  - OEIS A391791: `https://oeis.org/A391791` (revision #16, last edited 7 Jan 2026)
  - OEIS A391792: `https://oeis.org/A391792` (revision #6, last edited 7 Jan 2026)
- Fetched UTC: `2026-10-28T00:31:50Z`
- Page SHA-256:
  - A391791: `f4ca4c77d1c41c96dab40e5f51e2756147aba06cdbd83067bfd5e1d807f79b59`
  - A391792: `3143809d4ee29eb93fba6cc44747cff5fece2579df206bbda294c773bc26cb68`
- Literature Extents:
  - A391791 published terms ended at n = 22 (`405700861`).
  - A391792 published terms ended at n = 18 (`13615817865`).
  - Jehn's conjecture (optimal first move is coin $\lfloor (n+3)/2 \rfloor$ for $n > 9$) was stated as unproven for $n \ge 23$.
- This Work:
  - Computes exact integer values for A391791 at $n=23, 24, 25$.
  - Computes exact integer values for A391792 at $n=19, 20, 21$.
  - Unconditionally confirms Jehn's conjecture for all $n \in [10..25]$ with unique optimal first move $\lfloor (n+3)/2 \rfloor$.
  - Re-verifies all published terms with 100% agreement across two independent compiled implementations.

## Not Claimed
- We do not claim a closed-form analytic formula for $a(n)$ for arbitrary $n$; the results are established via certified finite-horizon Bellman backward induction.
- We do not claim proof of Jehn's conjecture for all infinite $n$; we prove it unconditionally for all $n \in [10..25]$.
- We do not submit directly to the OEIS; submitting to the OEIS is an action for the human only.

## Credits
- Ruediger Jehn, author of OEIS entries A391791 and A391792, and the Julia baseline `a391791_1.jl.txt`.
- The On-Line Encyclopedia of Integer Sequences (OEIS) Foundation.
- Contributor: zerbytheboss (V3R1T4S campaign).
