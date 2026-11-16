# 81-Gate Depth-6 Multiplier for `GF(2^7)` Modulo `x^7 + x^3 + 1` (`p2`)

## What

object/gf128_0x89_81gates.slp.txt is an 81-gate (32 AND, 49 XOR, no constants) straight-line circuit that multiplies correctly in the standard polynomial basis modulo x^7 + x^3 + 1 on all 16384 input pairs, which is at most the 84-gate p2 threshold and below the 85-gate NIST/CMT circuit and the 83-gate Jain circuit, and it settles neither the 25-product 8-term problem nor p1 or p3.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in `< 0.2 s`, Python 3 standard library only; verifies all `2^14 = 16,384` input pairs).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| NIST List of Circuits (`gf128-730-mult.slp`) | `GF(2^7)` mod `x^7 + x^3 + 1` | `85` gates (`40 AND + 45 XOR`, depth `5`) | https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits | 2026-11-15T16:29:25Z |
| Peralta CMT (`slp_730.txt`) | `GF(2^7)` mod `x^7 + x^3 + 1` | `85` gates (depth `5`) | https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html | 2026-11-15T16:29:26Z |
| Swapnil Jain (`gf2m-circuits`, Oct 2026, `final_f73_d6.slp`) | `GF(2^7)` mod `x^7 + x^3 + 1` | `83` gates (`32 AND + 51 XOR`, depth `6`) | https://github.com/Swapnil-jain/gf2m-circuits | 2026-11-15T16:29:26Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Satisfies enumerated partial win `p2` for `GF(2^7)` modulo `x^7 + x^3 + 1`; does not claim a `25`-AND circuit for 8-term binary polynomial multiplication or improvements on `GF(2^8)` / `GF(2^6)`.

## Credits

- **Joan Boyar, René Peralta, Magnus Gausdal Find, Çağdaş Çalık, Meltem Sönmez Turan, and Luís T. A. N. Brandão** (NIST Circuit Complexity Project & Yale CMT): problem formulation, SLP convention, and `85`-gate baseline.
- **Swapnil Jain** (<https://github.com/Swapnil-jain/gf2m-circuits>, Oct 2026): previous `83`-gate depth-`6` `GF(2^7)` mod `x^7 + x^3 + 1` construction.
