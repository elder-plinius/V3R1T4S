# Low-autocorrelation binary sequence of length 384: energy 10192, below the best published 10400

## What
A binary sequence of length 384 with energy 10192 (merit factor 7.2339). The best published energy for this length
was 10400 (merit factor 7.0892).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 384 in sequence.txt has exactly recomputed integer energy E = 10192, which is strictly below the only published energy found for L = 384, 10400 (arXiv:2206.12070 table row "B_383 o eta1 o eta2 o eta3", F = 7.08923076923, printed hex sequence recomputed to 10400), with arXiv:2607.09688, arXiv:2504.00987, 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222 and Knauer 2004 read and carrying no L = 384 row, and the Boskovic repository, the arXiv listing for newer results and the journal-only papers NOT read, so the claim is a strict win over the read-source baseline only, not a verified minimum over the full criterion set.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 384: energy 10400, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 10192 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 387 (3-element edit (remove 1 element(s) at the start and 2 at the end) of the published L=387 sequence from 2206.12070); the edit and its source are credited below.

## Credits
- Parent sequence: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
