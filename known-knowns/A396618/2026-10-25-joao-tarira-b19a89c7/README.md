# A396618(22) through A396618(25)

## What

A396618(22) = 6338072189, A396618(23) = 20042521382, A396618(24) = 63380064097, and A396618(25) = 200424655855, each the number of n-digit squares whose proper decimal suffixes are not squares (0 counting as a square), with the saved outputs of two different counters adding to the same total, past the OEIS b-file ending at a(21) = 2004269529.

A396618(n) counts n-digit terms of A192689: squares N such that N modulo 10^d
is not a square for every d with 1 <= d < n. Zero counts as a square, as in
the OEIS Mathematica program. a(1) = 4 is the given start.

## Check it yourself

From this folder, with Python 3 and a C compiler:

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About one minute on a laptop. The script
recomputes a(2) through a(19) from the definition and checks that
`object/terms.json` carries the attested a(1) through a(25). It does not
re-enumerate a(22) through a(25); those full counts are the saved research
outputs cited in `panel/reproduce.md`. Re-running them is a separate, longer
job (about 20 minutes for a(22), about an hour for a(23), about 45 minutes
for a(24), about 2.5 hours for a(25), on two cores). See `RUN_IT_YOURSELF.md`.

## Compared to

| sequence | cell | our value | published value we extended | source | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A396618 | a(22)..a(25) | 6338072189, 20042521382, 63380064097, 200424655855 | a(21) = 2004269529, and no later index | https://oeis.org/A396618/b396618.txt | 2026-10-25T07:43:25Z |

The b-file sha256 is in `the-record-we-beat/snapshot.md`.

## Not claimed

- Nothing past a(25).
- The one-minute checker does not by itself re-prove a(22) through a(25). Those
  totals stand on the saved full counts.
- These terms are not yet an OEIS edit. They are not a V3R1T4S bank target.
- No claim about the growth ratio beyond the observed a(n)/a(n-1) near the square root of 10.

## Credits

- Joao Tarira. The counters were written in the nocturno research record and checked against the published prefix before the new terms were kept.
- Michael S. Branicky, OEIS A396618 a(18) through a(21), 2026-06-10. https://oeis.org/A396618
- The OEIS Foundation, and the authors of A396618 and of A192689. https://oeis.org/A192689

Checker code in this package is offered under AGPL-3.0-or-later.
The term lists and witnesses are offered under CC BY 4.0.
Both match the inbound-equals-outbound terms of github.com/elder-plinius/V3R1T4S.
