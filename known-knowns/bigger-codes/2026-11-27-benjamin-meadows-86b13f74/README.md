# constant-weight-codes: A(25,10,12) >= 142

## What

The file object/A-25-10-12-142words.txt (sha256 86b13f74...) is a list of 142 distinct binary words of length 25, each of weight 12, with minimum Hamming distance 10 (so also A(25,10,13) at least 142 by complement), which exceeds the lower bound 141 and does not exceed the upper bound 433 of the A(25,10,12) cell as recorded in RECORD.md from the table fetched at 2026-11-27T18:39:11Z.

In numbers: 142 binary words of length 25 and weight 12 with minimum Hamming distance 10, against the table's lower bound 141 (upper bound 433), a margin of 1 word. This package contains one object only: object/A-25-10-12-142words.txt (one word per line as 25 characters 0/1, after a one-line description starting with `#`).

The construction, in words: one run of a seeded bit-swap tabu search, started from the 141-word code Brouwer hosts for this cell (https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H), credited in the table to William Echols. The run starts from the 141 seed words plus one word of least distance shortfall against them, and then repeatedly moves one 1 to a 0 position inside a word of a pair at distance below 10, minimizing the sum over such pairs of 10 minus their distance, with a tabu list, until no such pair is left. These moves change words, so the final code shares 117 of its 142 words with the seed code. The search is deterministic given its random seeds: how-we-built-it/rebuild.sh downloads the seed code, replays the run (81 CPU seconds in the original) and reproduces the object byte for byte. No symmetry group is claimed.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; seconds on a laptop. It checks the object's sha256, the word length, the alphabet, the weight of every word, distinctness and the Hamming distance of all 10011 pairs, and compares the size with the table's bounds; then it runs three planted-bug copies (a pair moved to distance 8, a word of the wrong weight, a duplicated word), each of which must be rejected. To rebuild the object from the published seed code: `sh how-we-built-it/rebuild.sh` (curl, a C++17 compiler and Python 3). Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | lower bound | upper bound | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Brouwer's table (Last-Modified Fri, 27 Nov 2026 00:32:42 GMT) | A(25,10,12) = A(25,10,13) | 141 | 433 | https://aeb.win.tue.nl/codes/Andw.html | 2026-11-27T18:39:11Z |

The table credits the lower bound 141 to William Echols, arXiv:2608.13906 (with 126 new codes). Echols (arXiv:2608.13906) lists 141 for this cell; Lysenstoen (arXiv:2607.19550) lists no value for it. Details, including the page's sha256 and the extracted cell: the-record-we-beat/RECORD.md.

## Not claimed

- Not an optimal code: only a code larger than the table's lower bound. The upper bound is 433.
- Only A(25,10,12) (and its complement cell A(25,10,13)). Each cell has its own package.
- Not a new construction method: the code is a local-search improvement of the code hosted for the cell (https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H), which is credited below.
- Maximality of the code was not checked.
- The code was not yet in Brouwer's table at the fetch above; it is to be sent to A. E. Brouwer after this claim is filed.

## Credits

- A. E. Brouwer, table of bounds on binary constant-weight codes: https://aeb.win.tue.nl/codes/Andw.html (the cell compared against, and the hosted 141-word seed code).
- William Echols: the 141-word code for this cell that the search started from (arXiv:2608.13906 (https://arxiv.org/abs/2608.13906)).
- Christopher D. Rosin, arXiv:2603.00174 and https://github.com/Constructive-Codes/CWBC (MIT licence): the bit-swap tabu search whose move scheme and parameters the search program follows.
- William Echols, arXiv:2608.13906: the seeded variant of the tabu search (starting from a known code).
- Christian Lysenstøen, arXiv:2607.19550: compared against for this cell.
- Benjamin Meadows (search, checking and packaging).
