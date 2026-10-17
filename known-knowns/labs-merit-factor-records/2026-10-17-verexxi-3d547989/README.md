# Low-autocorrelation binary sequence of length 377: energy 9452, below the best published 9668

## What
A binary sequence of length 377 with energy 9452 (merit factor 7.5185). The best published energy for this length
was 9668 (merit factor 7.3505).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence in sequence.txt of length 377 (skew-symmetric, made by deleting the first and last element of the arXiv:2206.12070 length-379 record) has exactly recomputed integer energy E = 9452, which is strictly below 9668, the minimum over the baseline.tsv value for L = 377 (arXiv:2206.12070 table, E = 9668, F = 7.35048613984, printed hex sequence recomputed to 9668; its older-record column implies 9836) among the sources actually read (1406.5301, 1512.02475, 2011.00068, 2106.03377, 2206.12070, 2210.15962, 2409.07222, 2504.00987, 2607.09688, Knauer 2004), and it is not a verified win against the unread Boskovic et al. records repository, journal-only versions, or any arXiv result newer than the fetch time.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 377: energy 9668, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 9452 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 379 (two-element edit (remove 1 element(s) at the start and 1 at the end) of the published L=379 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
