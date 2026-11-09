# Least Primes with Least Quadratic Non-Residues 167..191: A000229(39..43)

## What

Exact determination of A000229(39) = 317398900373231 (least prime with least quadratic non-residue prime(39) = 167, full win) and A000229(41) = 1463971373078639 (least prime with least quadratic non-residue prime(41) = 179, full win), unblocking A000229(40) = 112434732901969, A000229(42) = 178936222537081, and A000229(43) = 501108392233679, together with independent exhaustive verification of A000229(30..38), A002223(30..38), and A002224(30..41) from 1 (partial wins p1 and p2).

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_qnr.py` and compiles `verify-it-yourself/verify_qnr_sieve.c` (~11 seconds total runtime), which:
1. Checks deterministic 64-bit Miller-Rabin primality, Euler criterion $p^{(q-1)/2} \bmod q$, and Quadratic Reciprocity Legendre symbols for all terms in `A000229(1..43)`, `A002223(30..38)`, `A002224(30..41)`, the 4 primes $q \equiv 1 \pmod 8$ in $[1, 317398900373231]$ having the first 38 primes as quadratic residues, and the 5 primes in $[1, 1463971373078639]$ having the first 40 primes as quadratic residues, and verifies byte-for-byte reproduction of `b000229.txt` (`n = 1..38`).
2. Runs **Stage 1** across $[1, 317398900373231]$ via two independent CRT modulus splits (`M1 = 892,371,480` with 20 sieve primes and `M2 = 25,878,772,920` with 28 sieve primes), reproducing `A000229(30..38)`, `A002223(30..38)`, and `A002224(30..41)` from 1 and establishing `A000229(39) = 317398900373231` and `A000229(40) = 112434732901969`.
3. Runs **Stage 2** across $[1, 1463971373078639]$ via two independent CRT modulus splits (`M2 = 25,878,772,920` with 30 sieve primes and `M3 = 802,241,960,520` with 29 sieve primes), independently finding the exact same 5 primes having the first 40 primes ($2 \dots 173$) as quadratic residues (`178936222537081`, `501108392233679`, `831583148698319`, `1152240096017111`, `1463971373078639`), proving `A000229(41) = 1463971373078639` and unblocking `A000229(42) = 178936222537081` and `A000229(43) = 501108392233679`.

## Compared To

- **Published Record (OEIS A000229, A002223, A002224)**: `b000229.txt` ends at $n = 38$ (`a(38) = 70864718555231`, least QNR $163$, from Tomas Oliveira e Silva exhaustive search up to $10^{14}$). Both `A000229(39)` (least QNR $167$) and `A000229(41)` (least QNR $179$) were open because the sibling records in `A002223` and `A002224` skip $167$ in the $1 \bmod 8$ branch (`A002224(38) = A002224(39) = 112434732901969`, least QNR $173$) and skip $179$ in both branches (`A002223(40) = A002223(41) = 501108392233679`, least QNR $191$; `A002224(40) = A002224(41) = 178936222537081`, least QNR $181$).
- **This Submission**: Extends `A000229` by five consecutive terms `a(39)..a(43)`:
  - `A000229(39) = 317398900373231` (least QNR $p_{39} = 167$, full win)
  - `A000229(40) = 112434732901969` (least QNR $p_{40} = 173$, unblocked by settling `a(39)`)
  - `A000229(41) = 1463971373078639` (least QNR $p_{41} = 179$, full win)
  - `A000229(42) = 178936222537081` (least QNR $p_{42} = 181$, unblocked by settling `a(41)`)
  - `A000229(43) = 501108392233679` (least QNR $p_{43} = 191$, unblocked by settling `a(41..42)`)

## Not Claimed

- No value is claimed for `A000229(44)` (least QNR $p_{44} = 193$) or `A002224(42)`.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - D. H. Lehmer, E. Lehmer, and D. Shanks, "Integer sequences having prescribed quadratic character," *Mathematics of Computation* 24 (1970), 433-451 (`https://doi.org/10.1090/S0025-5718-1970-0268109-0`).
  - Tomas Oliveira e Silva (`https://oeis.org/A000229` and `https://oeis.org/A000229/b000229.txt`).
  - Jinyuan Wang (`https://oeis.org/A002223` and `https://oeis.org/A002223/b002223.txt`).
  - Michael Hortmann and Mike Oakes (`https://oeis.org/A002224` and `https://oeis.org/A002224/b002224.txt`).
