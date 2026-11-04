# A395265(20) and A395265(21)

## What

A395265(20) = 56 and A395265(21) = 62, the minimum diameters of a 20-mark and a 21-mark 5-Golomb ruler, with explicit witnesses of those diameters and saved independent exhaustive searches reporting none of diameter 51 through 55 or 57 through 61, past the OEIS b-file ending at a(19) = 50.

A 5-Golomb ruler on n marks is an n-element set of integers in which every
positive difference occurs at most 5 times. A395265(n) is the minimum
possible largest element when the smallest element is 0.

## Check it yourself

From this folder, with Python 3 (standard library only):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a second. The script checks both witnesses
in `object/rulers.json`: 20 and 21 distinct marks, starting at 0, ending at
56 and 62, no positive difference more than 5 times. It does not repeat the
exhaustive proof that no smaller diameter exists. That is the saved
`verify_run.txt` for each term (about 45 minutes for a(20), about 3.5 hours
for a(21)).

## Compared to

| sequence | cell | our value | published value we extended | source | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A395265 | a(20), a(21) | 56, 62 | a(19) = 50, no later index | https://oeis.org/A395265/b395265.txt | 2026-10-25T07:43:25Z |

The b-file sha256 is in `the-record-we-beat/snapshot.md`.

arXiv:2605.14229, Table 1, row g = 5, was read the same day from the HTML full text. That row lists G(5, n) through n = 19 (value 50) and leaves n = 20 blank. The raw HTML fetch did not return bytes, so that page has no sha256 here. The hashed record is the OEIS b-file.

## Not claimed

- Nothing past a(21).
- The one-command checker proves only that these two rulers exist. Minimality is the saved exhaustive search.
- The left-to-right and right-to-left programs share the same two pruning rules (span at least a(j-i+1), and a capacity bound on the unplaced segment). Agreement of node counts is expected for mirror-image trees. The rules are argued in the research notes; this package does not add a separate formal derivation.
- Not yet an OEIS edit. Not a V3R1T4S bank target. No claim about other cells of the Gupta-O'Bryant table.

## Credits

- Joao Tarira. The witnesses and the exhaustive searches are from the nocturno research record.
- Aditya A. Gupta, OEIS A395265, 2026-04-17. https://oeis.org/A395265
- Sean A. Irvine, A395265(19), 2026-04-23.
- Aditya Gupta and Kevin O'Bryant, Optimal Diameters of High Multiplicity g-Golomb Rulers, arXiv:2605.14229, 2026. Their Table 1 stops at G(5, 19) = 50.
- The OEIS Foundation.

Checker code in this package is offered under AGPL-3.0-or-later.
The term lists and witnesses are offered under CC BY 4.0.
Both match the inbound-equals-outbound terms of github.com/elder-plinius/V3R1T4S.
