# Low-autocorrelation binary sequence of length 242: energy 3337, below the best published 3593

## What
A binary sequence of length 242 with energy 3337 (merit factor 8.7749). The best published energy for this length
was 3593 (merit factor 8.1497).

The exact scope, as signed off by the three reviewers:

> The explicit +-1 sequence of length 242 in the claim folder has exact integer aperiodic energy E = 3337 (merit factor 58564/6674 = 8.7749), strictly below the baseline minimum of 3593 (Dimitrov et al. arXiv:2206.12070 table row, whose decoded sequence I recomputed to 3593; Knauer 2004 gives 4073) over the ten sources actually read (arXiv 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2206.12070, 2210.15962, 2409.07222, 2504.00987, 2607.09688 and the Knauer 2004 table in the git_labs copy), with the Boskovic records even-length file, the arXiv listing and the journal-only papers unread, and the sequence being a 3-element end trim (1 off the front, 2 off the back) of the published L=245 record (E = 3226) of arXiv:2210.15962.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3.8 or newer, standard library only). It ends with
`PASS` in under a second. Two separately written checkers recompute the energy from the definition. Sample output
is in verify-it-yourself/RECEIPTS.md.

## Compared to
Best published value for L = 242: energy 3593, from 2206.12070 (https://arxiv.org/src/2206.12070, fetched 2026-10-16T17:00:24Z). Every source read and every row
found for this length are listed in the-record-we-beat/.

## Not claimed
- Not an optimum: 3337 is simply lower than every published value found, not the lowest possible.
- Only this one length. Other lengths found the same way are separate packages.
- The sequence is a small edit of a published sequence of length 245 (3-element edit (remove 1 element(s) at the start and 2 at the end) of the published L=245 sequence from 2210.15962); the edit and its source are credited below.

## Credits
- Parent sequence: Borko Bošković, Jana Herzog, Janez Brest, "Parallel Self-Avoiding Walks for a Low-Autocorrelation Binary Sequences Problem", arXiv:2210.15962 (https://arxiv.org/abs/2210.15962).
- Record compared against: Miroslav Dimitrov, "New Classes of Binary Sequences with High Merit Factor", arXiv:2206.12070 (https://arxiv.org/abs/2206.12070).
- Status source and method context: Blaž Pšeničnik, Borko Bošković, Jan Popić, Janez Brest, "Prioritizing Search Space Regions in the Low Autocorrelation Binary Sequences Problem", arXiv:2607.09688 (https://arxiv.org/abs/2607.09688).
- Bošković et al. LABS records repository: https://github.com/borkob/git_labs
- Found by verexxi; the search and the three independent reviews were run with Claude (Anthropic).
