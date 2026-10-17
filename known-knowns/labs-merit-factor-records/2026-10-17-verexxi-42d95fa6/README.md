# Low-autocorrelation binary sequence of length 252: energy 3534, below the best published 3738

## What
A binary sequence of length 252 with energy 3534 (merit factor 8.9847). The best published energy for this length
was 3738 (merit factor 8.4944).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 252 in sequence.txt has exactly recomputed integer energy E = 3534 (F = 8.98), strictly below the baseline 3738 (the minimum over the rows for L = 252 in arXiv:2206.12070 [3738, also recomputed from its printed hex sequence] and the Knauer 2004 table as stored in the Boskovic git_labs repository [4386]), after reading ten sources (1406.5301, 1512.02475, 2011.00068, 2106.03377, 2206.12070, 2210.15962, 2409.07222, 2504.00987, 2607.09688, Knauer 2004), none of which has a lower value for L = 252; it is NOT established against the unread current Boskovic records pages or any arXiv result newer than the sources read, and it is a one-end trim of a published L = 253 record sequence.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 252: energy 3738, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 3534 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 253 (one-element edit (remove 0 element(s) at the start and 1 at the end) of the published L=253 sequence from 2011.00068); the edit and its source are credited below.

## Credits
- Parent sequence: Janez Brest, Borko Bošković, "Computational Searching of Long Skew-symmetric Binary Sequences with High Merit Factors", arXiv:2011.00068 (https://arxiv.org/abs/2011.00068).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
