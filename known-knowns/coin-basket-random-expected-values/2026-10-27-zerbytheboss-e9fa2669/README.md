# Jehn's Random-Basket Coin Game: Exact Expected Values (`coin-basket-random-expected-values`)

## What
Exact optimal expected values for Jehn's random-basket coin game: A391791(23)=884741548, A391791(24)=1922512940, A391791(25)=4164198462 (k=2) and A391792(19)=45245088184, A391792(20)=149627079790, A391792(21)=492482601295 (k=3), with all published terms reproduced and Jehn's conjecture confirmed by exact computation for n = 10..25.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (runs in < 1 second using pure Python standard library). Note on scope: the bundled check (`verify-it-yourself/check_coin_basket.py`) compares the `object/` files with values stored in the script (`n = 1..25` for `k = 2`, `n = 1..21` for `k = 3`, and the `n = 10..25` first-move table) and recomputes from the game definition only `n = 1..6` (`k = 2`) and `n = 1..4` (`k = 3`), so it does not validate the new terms (`A391791(23..25)` and `A391792(19..21)`); to recompute the new terms from scratch, compile and run the two independent solvers in `how-we-built-it/` as shown in `RUN_IT_YOURSELF.md`.

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
  - Jehn's conjecture states that the optimal first move is coin $\lfloor (n+3)/2 \rfloor$ for $n > 9$.
- This Work:
  - Computes exact integer values for A391791 at $n=23, 24, 25$.
  - Computes exact integer values for A391792 at $n=19, 20, 21$.
  - Jehn's conjecture is confirmed by exact computation for n = 10..25 with unique optimal first move $\lfloor (n+3)/2 \rfloor$.
  - Re-verifies all published terms with 100% agreement across two independent compiled implementations.

## Not Claimed
- We do not claim a closed-form analytic formula for $a(n)$ for arbitrary $n$; the results are established via certified finite-horizon Bellman backward induction.
- We do not claim a general proof of Jehn's conjecture for all $n > 9$; it is confirmed by exact computation for n = 10..25.
- We do not submit directly to the OEIS; submitting to the OEIS is an action for the human only.

## Credits
- Ruediger Jehn, author of OEIS entries A391791 and A391792, and the Julia baseline `a391791_1.jl.txt`.
- The On-Line Encyclopedia of Integer Sequences (OEIS) Foundation.
- Contributor: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
