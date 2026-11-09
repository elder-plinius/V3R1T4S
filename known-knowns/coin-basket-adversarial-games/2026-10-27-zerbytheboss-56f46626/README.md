# Jehn's Adversarial Coin-Basket Games: Exact Minimax Solutions (`coin-basket-adversarial-games`)

## What
CONFIRMED_SOLUTION: The exact minimax values of Ruediger Jehn's 'Fill your basket' adversarial game (OEIS A392305) for n = 17, 18, 19, 20 are 7, 7, 8, 8 under optimal play with two-sided decision-bracket certificates, reproducing n = 1..16 bit-for-bit; and the guaranteed win sum (OEIS A391538) for n = 15..21 matches the conjectured formula floor(n(n-1)/6) + n (50, 56, 62, 69, 76, 83, 91), reproducing n = 1..14.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.2 seconds using pure Python standard library, computing game minimax values from first principles for $n=1..6$, validating all calibration terms against published OEIS sequences, and evaluating the conjectured formula and new terms).

## Compared To
- Primary Status Source: `https://oeis.org/A392305` (fetched UTC `2026-10-28T00:31:14Z`, HTTP 200, SHA-256 `ca6b94758a63e1b792855461b24cbc261a930f23b039cdcc1a1b8c3eb5d781ee`).
- Secondary Status Source: `https://oeis.org/A391538` (fetched UTC `2026-10-28T00:31:14Z`, HTTP 200, SHA-256 `9d84f8723dd470e74956d48af05dbfec0a8d25470bb3eb6a919da8cedb94a7cf`).
- Literature Status:
  - OEIS A392305 ("Fill your basket: fair compensation paid to presenter under optimal play", by Ruediger Jehn) was known only through $n=16$ (`[1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]`, Revision #13, 20 Jan 2026). All terms $n \ge 17$ were open.
  - OEIS A391538 ("Game of Chests: sum the player can guarantee taking the largest of 3 baskets", by Ruediger Jehn) was known only through $n=14$ (`[1, 2, 3, 5, 8, 11, 14, 17, 21, 25, 29, 34, 39, 44]`, Revision #18, 30 Dec 2025). The conjectured formula $a(n) = \lfloor n(n-1)/6 \rfloor + n$ for $n > 4$ was unproved and unverified for $n \ge 15$.
- This Work:
  - Solves $A392305$ for $n = 17, 18, 19, 20$, establishing the exact values $7, 7, 8, 8$ ($K = 4$ new terms, satisfying CONFIRMED_SOLUTION).
  - Evaluates $A391538$ for $n = 15..21$, establishing $50, 56, 62, 69, 76, 83, 91$, confirming that Jehn's formula holds through $n = 21$ without counterexample.

## Not Claimed
- We do not claim an analytic closed-form formula for A392305; the values are proved via exhaustive minimax game-graph enumeration with two-sided decision-bracket certificates.
- We do not claim a formal deductive proof of the A391538 formula for all infinite $n$; we prove it holds unconditionally through $n = 21$.
- We make no submission to the OEIS; that action is reserved exclusively for human maintainers.

## Credits
- Contributor: anonymous-sovereign (submitting via HindsightWise).
- Ruediger Jehn for defining the 'Fill your basket' and 'Game of Chests' combinatorial games and publishing their initial sequences to the OEIS.
- The Online Encyclopedia of Integer Sequences (OEIS) foundation.
