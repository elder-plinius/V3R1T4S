# Low-autocorrelation binary sequence of length 391: energy 10471, below the best published 10675

## What
A binary sequence of length 391 with energy 10471 (merit factor 7.3002). The best published energy for this length
was 10675 (merit factor 7.1607).

The exact scope, as signed off by the three reviewers:

> For L = 391 only, the explicit +-1 sequence in sequence.txt has exactly recomputed integer energy E = 10471 (F = 7.3002), strictly below 10675, the minimum over the baseline.tsv rows for L = 391 (the printed sequence of arXiv:2206.12070, E = 10675, F = 7.16070257611, plus its "previous best" figure 7.1553, E >= 10683 and no sequence printed), where the sources actually read were the ten TeX sources or tables in sources_checked.md (only 2206.12070 has a row for 391; 2607.09688 and 2504.00987 tabulate 450..573 and 92..120 and have none); it is a one-position cyclic rotation of that same published L = 391 sequence, not an independent search, and it is not established against the unread Boskovic records repository, journal-only papers, 2011.00068 v1, or any arXiv result newer than the sources read.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 391: energy 10675, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 10471 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 389 (two-element edit (prepend '' and append '01' (0 = +1, 1 = -1)) of the published L=389 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
