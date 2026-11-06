# A390087(8), A390087(9), and A390085(31) through A390085(48)

## What

A390087(8) = 39 and A390087(9) = 48, so A390085(31) through A390085(38) = 7, A390085(39) through A390085(47) = 8, and A390085(48) = 9, from explicit irreducible odd zero-sum witnesses of lengths 16 and 18 and from saved exhaustive searches that found no shorter index, past the OEIS b-files ending at A390087(7) = 30 and A390085(30) = 7.

A390085(k) is half the length of a longest irreducible zero-sum subset of
the odd integers from -(2k-1) through 2k-1. Irreducible means no nonempty
proper subset sums to 0. A390087(n) is the smallest k with A390085(k) = n.
The sequence is non-decreasing in k, because a set that fits in a smaller
odd interval still fits in a larger one.

## Check it yourself

From this folder, with Python 3 (standard library only):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. A few seconds. The script enumerates every
nonempty proper subset of both witnesses and checks the odd-zero-sum
conditions, and it checks that the object still carries the attested
A390085 row. It does not repeat the exhaustive NONE searches. Those are
the saved logs cited in `panel/reproduce.md` (minutes to a few hours).

## Compared to

| sequence | cell | our value | published value we extended | source | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A390087 | a(8), a(9) | 39, 48 | a(7) = 30, no later index | https://oeis.org/A390087/b390087.txt | 2026-10-25T07:43:25Z |
| OEIS A390085 | a(31)..a(48) | eight 7s, nine 8s, then 9 | a(30) = 7, no later index | https://oeis.org/A390085/b390085.txt | 2026-10-25T07:43:25Z |

Both b-file sha256 values are in `the-record-we-beat/snapshot.md`.

## Not claimed

- Nothing past A390087(9) or A390085(48).
- The published upper bound A390085(k) <= sqrt(2k+4) - 1 was not used. The research record does not contain a proof of it.
- The one-command checker re-proves the two witnesses (so a(8) <= 39 and a(9) <= 48, and A390085(39) >= 8 and A390085(48) >= 9). Equality, and the values in between, stand on the saved exhaustive NONE logs.
- Not yet an OEIS edit. Not a V3R1T4S bank target. A390085 is included here because it is the same computation, not as a second package.

## Credits

- Joao Tarira. Witnesses and the exhaustive searches are from the nocturno research record.
- Hu Junhua, OEIS A390087 and A390085, 2025-11-13. https://oeis.org/A390087 and https://oeis.org/A390085
- Christian Sievers, A390087(4) and the A390085 b-file through k = 30, 2025-11-12.
- The OEIS Foundation.

Checker code in this package is offered under AGPL-3.0-or-later.
The term lists and witnesses are offered under CC BY 4.0.
Both match the inbound-equals-outbound terms of github.com/elder-plinius/V3R1T4S.
