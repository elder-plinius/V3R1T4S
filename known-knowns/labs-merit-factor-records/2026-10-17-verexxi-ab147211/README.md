# Low-autocorrelation binary sequence of length 380: energy 10058, below the best published 10286

## What
A binary sequence of length 380 with energy 10058 (merit factor 7.1784). The best published energy for this length
was 10286 (merit factor 7.0192).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence in sequence.txt (length 380) has exactly recomputed integer energy E = 10058, strictly below 10286, which is the only published L = 380 value found in the ten sources actually read (arXiv:2206.12070 row for 380, merit factor 7.01924946529, decoded sequence energy 10286; arXiv:2607.09688, 2504.00987 and 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222 and Knauer's 2004 table have no L = 380 row), so it beats the baseline as read but not a baseline that is proven complete, because the Boskovic et al. records repository pages, the journal-only versions and any arXiv result newer than 2607.09688 could not be read.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 380: energy 10286, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 10058 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 383 (3-element edit (remove 1 element(s) at the start and 2 at the end) of the published L=383 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
