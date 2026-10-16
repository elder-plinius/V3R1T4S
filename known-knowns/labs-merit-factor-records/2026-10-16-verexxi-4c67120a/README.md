# Low-autocorrelation binary sequence of length 232: energy 3032, below the best published 3340

## What
A binary sequence of length 232 with energy 3032 (merit factor 8.8760). The best published energy for this length
was 3340 (merit factor 8.0575).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 232 in the claim folder has exactly recomputed integer energy E = 3032 (F = 8.876), strictly below 3340 (F = 8.0575, Dimitrov et al. arXiv:2206.12070), which is the minimum over the rows for L = 232 in the ten sources actually read (Knauer 2004 copy in the Boskovic git_labs repository, 3752; 2206.12070, 3340; the other eight read sources, 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222, 2504.00987 and 2607.09688, have no row for 232), and it is not established against the unread repository pages, Mertens' table, journal-only versions or arXiv posts newer than 2607.09688.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 232: energy 3340, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 3032 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 229 (3-element edit (prepend '' and append '000' (0 = +1, 1 = -1)) of the published L=229 sequence from 2210.15962); the edit and its source are credited below.

## Credits
- Parent sequence: Borko Bošković, Jana Herzog, Janez Brest, "Parallel Self-Avoiding Walks for a Low-Autocorrelation Binary Sequences Problem", arXiv:2210.15962 (https://arxiv.org/abs/2210.15962).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
