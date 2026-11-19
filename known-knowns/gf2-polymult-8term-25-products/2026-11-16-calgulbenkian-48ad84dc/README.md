# 82-Gate Depth-6 Multiplier for `GF(2^7)` Modulo `x^7 + x^4 + 1` (`p2`)

## What

The file object/gf128_0x91_82gates.slp.txt is a valid 82-gate (34 AND, 48 XOR) AND/XOR circuit that exhaustively matches standard polynomial-basis multiplication in GF(2^7) modulo x^7+x^4+1 on all 16384 input pairs, meeting partial win p2's 83-gate limit for that polynomial and beating the NIST/CMT 84 and Jain 87 figures, subject to the novelty skeptic's confirmation that no smaller published circuit exists.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in `< 0.2 s`, Python 3 standard library only; verifies all `2^14 = 16,384` input pairs).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| NIST List of Circuits (`gf128-740-mult.slp`) | `GF(2^7)` mod `x^7 + x^4 + 1` | `84` gates (`40 AND + 44 XOR`, depth `5`) | https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits | 2026-11-15T16:29:25Z |
| Peralta CMT (`slp_740.txt`, July 2010) | `GF(2^7)` mod `x^7 + x^4 + 1` | `84` gates (depth `5`) | https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html | 2026-11-15T16:29:26Z |
| Swapnil Jain (`gf2m-circuits`, Oct 2026, `final_f7.slp`) | `GF(2^7)` mod `x^7 + x^4 + 1` | `87` gates (`32 AND + 55 XOR`, depth `11`) | https://github.com/Swapnil-jain/gf2m-circuits | 2026-11-15T16:29:26Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Satisfies enumerated partial win `p2` for `GF(2^7)` modulo `x^7 + x^4 + 1`; does not claim a `25`-AND circuit for 8-term binary polynomial multiplication or improvements on `GF(2^8)` / `GF(2^6)`.

## Credits

- **Joan Boyar, René Peralta, Magnus Gausdal Find, Çağdaş Çalık, Meltem Sönmez Turan, and Luís T. A. N. Brandão** (NIST Circuit Complexity Project & Yale CMT): problem formulation, SLP convention, and 2010 `84`-gate record.
- **Swapnil Jain** (<https://github.com/Swapnil-jain/gf2m-circuits>, Oct 2026): highlighted `x^7 + x^4 + 1` as an open barrier for symmetric split-family constructions.
