# Low-autocorrelation binary sequence of length 328: energy 7148, below the best published 7444

## What
A binary sequence of length 328 with energy 7148 (merit factor 7.5255). The best published energy for this length
was 7444 (merit factor 7.2262).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 328 in sequence.txt has exactly recomputed integer energy E = 7148 (F = 7.525), which is strictly below 7444 (F = 7.22622246104), the only published L=328 value found in the ten sources actually read (arXiv:2206.12070 table row, whose printed hex sequence also recomputes to 7444; arXiv:2607.09688 and arXiv:2504.00987 were read and have no L=328 row, and 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222 and Knauer 2004 have none either), while the Boskovic records repository (git_labs tree and Merit_Factor_Records even/odd pages), newer arXiv results and journal-only versions were NOT readable, so "best published" is established only over the sources read.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 328: energy 7444, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 7148 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 327 (one-element edit (prepend '' and append '1' (0 = +1, 1 = -1)) of the published L=327 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
