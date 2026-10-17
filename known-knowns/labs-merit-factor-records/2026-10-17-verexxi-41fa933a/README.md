# Low-autocorrelation binary sequence of length 338: energy 7609, below the best published 7865

## What
A binary sequence of length 338 with energy 7609 (merit factor 7.5072). The best published energy for this length
was 7865 (merit factor 7.2628).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 338 in the claim folder has exactly recomputed integer energy E = 7609 (F = 338^2/(2*7609) = 7.508), which is strictly below 7865, the only published row for L = 338 found in the ten sources read (the 2206.12070 table row, printed F = 7.26280991736, whose decoded sequence I recomputed to E = 7865), as a one-element truncation of that same paper's L = 339 record (E = 7393); the minimum over the criterion's other named sources (the Boskovic et al. repository, any arXiv result newer than 2607.09688) is not established because they could not be read.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 338: energy 7865, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 7609 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 339 (one-element edit (remove 0 element(s) at the start and 1 at the end) of the published L=339 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
