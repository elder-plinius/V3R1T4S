# constant-weight-codes: A(30,12,9) >= 45

## What

The file object/A-30-12-9-45words.txt (sha256 806649f7...) is a list of 45 distinct binary words of length 30, each of weight 9, with minimum Hamming distance 12 (so also A(30,12,21) at least 45 by complement), which exceeds the lower bound 44 and does not exceed the upper bound 74 of the A(30,12,9) cell as recorded in RECORD.md from the table fetched at 2026-11-26T20:13:38Z.

In numbers: 45 binary words of length 30 and weight 9 with minimum Hamming distance 12, against the table's lower bound 44 (upper bound 74), a margin of one word. This package contains one object only: object/A-30-12-9-45words.txt (one word per line as 30 characters 0/1, after a one-line description starting with `#`).

The construction, in words: a seeded bit-swap tabu search (the method of Echols, arXiv:2608.13906), started from the 44-word code Brouwer hosts for this cell (https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44) plus the one weight-9 word with the smallest total distance shortfall against it. Each step moves one 1 to a 0 position inside one word of a pair at distance below 12, minimizing the sum over such pairs of 12 minus their distance, with a short tabu list; it stops when no such pair is left. Every word was moved: the result shares no word with the seed code, and no 44-word subset of it is equivalent to the seed. The seed code is maximal (no 45th word can be added to it), so the result is not the seed plus a word. No symmetry group is claimed. The search is deterministic given its random seed (1008): how-we-built-it/rebuild.sh downloads the seed code, reruns the search and reproduces the object byte for byte.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the word length, the alphabet, the weight of every word, distinctness and the Hamming distance of all 990 pairs, and compares the size with the table's bounds; then it runs three planted-bug copies (a pair moved to distance 10, a word of weight 10, a duplicated word), each of which must be rejected. To rebuild the object from the published seed code: `sh how-we-built-it/rebuild.sh` (curl and a C++17 compiler; 10 s to about 1.5 minutes on one core). Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | lower bound | upper bound | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Brouwer's table (Last-Modified Thu, 26 Nov 2026 15:24:18 GMT) | A(30,12,9) = A(30,12,21) | 44 | 74 | https://aeb.win.tue.nl/codes/Andw.html | 2026-11-26T20:13:38Z |
| Brouwer's table, re-fetched before filing (Last-Modified Thu, 26 Nov 2026 20:15:27 GMT) | A(30,12,9) = A(30,12,21) | 44 | 74 | https://aeb.win.tue.nl/codes/Andw.html | 2026-11-26T20:27:26Z |

The only note under the table that names the cell says that 44 was obtained by polishing the 43-word code of Rosin (arXiv:2603.00174). Echols (arXiv:2608.13906) and Lysenstoen (arXiv:2607.19550) list no value for this cell. Bounds implied by the hosted codes of neighbouring cells reach at most 42 (the-record-we-beat/RECORD.md). Details, including the page's sha256 and the extracted row: the-record-we-beat/RECORD.md.

## Not claimed

- Not an optimal code: only a code larger than the table's lower bound. The upper bound is 74.
- Only A(30,12,9) (and its complement cell A(30,12,21)). Each cell has its own package.
- One derivation route was not tested: the table's A(32,12,11) >= 215 code file returned 404, so the best two-coordinate shortening of that code to (30,12,9) was not computed (on average a coordinate pair keeps about 24 words).
- Maximality of the 45-word code was not checked.
- The code was not yet in Brouwer's table at the fetch above; it is to be sent to A. E. Brouwer after this claim is filed.
- The review files in panel/ refer to the folder the reviewers saw: its CLAIM.md held the claim, the construction and the criterion quoted from the bank (the same content as this README and how-we-built-it/COMMANDS.md), its RECORD.md is the-record-we-beat/RECORD.md, and its search/bststate.cpp is how-we-built-it/bststate.cpp.

## Credits

- A. E. Brouwer, table of bounds on binary constant-weight codes: https://aeb.win.tue.nl/codes/Andw.html (the cell compared against, and the hosted 44-word seed code).
- Christopher D. Rosin, arXiv:2603.00174: the 43-word code from which the table's 44-word code was polished.
- William Echols, arXiv:2608.13906: the seeded bit-swap tabu search method used here.
- Christian Lysenstøen, arXiv:2607.19550: compared against for this cell (no value listed).
- Benjamin Meadows (search, checking and packaging).
