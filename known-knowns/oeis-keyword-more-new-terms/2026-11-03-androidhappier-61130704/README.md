# A361864(12) = 2092816: set partitions of {1..12} whose block-medians have integer median

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A361864(12) equals 2092816, the first term beyond the live DATA and b-file of OEIS A361864 (keyword more), computed by two independent programs that reproduce a(1..11) and not found in the entry, its history, or an OEIS value search as of 2026-11-03T17:41Z.

OEIS A361864 (Gus Wiseman, Apr 2023) counts the set partitions of {1..n} for which the median of the block medians
is an integer. A median of an even number of values is the mean of the two middle values (entry comment), and the
outer median is taken over the multiset of block medians, with repetition. The entry gives a(1..11) =
1, 0, 3, 6, 30, 96, 461, 2000, 10727, 57092, 342348 (offset 1, keyword nonn,more). This folder adds the next term:

    A361864(12) = 2092816

The object is object/VALUE.txt (sha256 61130704e05eb2819cbd23604b090802da6409ae924ed4239a2658f992ec1a55).
It was found by an exhaustive count over all Bell(12) = 4,213,597 set partitions of {1..12}, done by two separately
written programs (how-we-built-it/): a C program over restricted growth strings with doubled integer medians, and a
Go program that builds each partition from the block holding the lowest unused element and uses exact rationals.
Both reproduce a(1..11) and agree on a(12). A Python Fraction brute force reproduces a(1..10).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: about 30 seconds to a few minutes (pure-Python exhaustive count
over all 4,213,597 partitions of {1..12}, Python 3 standard library only; the C cross-check is skipped without a
compiler). Real output: verify-it-yourself/RECEIPTS.md. Full commands for both search programs: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A361864 (revision #5, Apr 04 2023), DATA, b-file, history, value search | a(12) | absent (DATA and synthesized b-file end at a(11) = 342348; no pending draft; search for 2092816: "No results.") | 2092816 | 2026-11-03T16:17:38Z (scout); 2026-11-03T17:21:44Z (novelty panel); 2026-11-03T17:41:23Z (criterion panel) |

URL: https://oeis.org/A361864 (b-file https://oeis.org/A361864/b361864.txt, history
https://oeis.org/history?seq=A361864). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A361864(12). By-product values of a(13), a(14) and a(15) printed during the run are not claimed
  and were not checked by the panel.
- This is an exact computer enumeration, not a proof by hand.
- Nothing has been submitted to the OEIS.
- panel/ holds the panel files as written, except two leak-scan replacements in novelty.md recorded in
  panel/REDACTIONS.md.

## Credits

- Gus Wiseman: the sequence A361864 and its terms a(1..11), https://oeis.org/A361864.
- The OEIS Foundation, https://oeis.org.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub @CharanRayudu (https://github.com/CharanRayudu), credited through the account that submits this folder.
