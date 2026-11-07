# Pre-registration

frozen_at: 2026-11-06T07:12:45Z
id: short-binary-multiple-deletion-code-records
cell: (16,3)

Criterion, copied verbatim from bank/targets.json:

Provide an explicit set of distinct binary words with respectively at least 137, 216, 31 or 43 codewords for any one of the four specified (n,s) cells, with pairwise disjoint s-deletion subsequence sets. No linearity, constant-weight or decoder-efficiency assumption is imposed. The complete codebook is the certificate. Also strictly improve the best comparable published result at claim time, including compatible compositions of published objects. State whether the candidate is a composition and identify its components. Values in unmerged pull requests do not set the bar.

Statistic: the number of distinct length-16 binary words in the saved file, accepted only if an independent pairwise longest-common-subsequence checker, written from the definition and not sharing code with the searcher, prints ACCEPT. ACCEPT means every pair has LCS at most 12, which is LCS < 16-3. A C ball-intersection test is a search device, not the judge.

Threshold: size >= 43. A tie at 42 is not a win. The live table maximum copied from the fetched HTML is 42, from the OnlineMIS row of Table 2, which is printed in bold. If a later source read in this run states a larger comparable size, that larger size plus one is the threshold, and this file is not edited; a new PREREG.v2.md would say so before that comparison is scored.

null_test: not needed because an explicit codebook is checked by a deterministic checker against a table value

baseline: not a score on a dataset. No published-baseline reproduction step. The comparison is the integer size against Table 2.

Families frozen before their output is scored:

- F1, heuristic, excludes nothing: iterated deletion of 1 to 8 codewords from a greedy seed, greedy refill, then exact 1-drop and periodic 2-drop, on all 65536 words. A timeout or a best size below 43 excludes no code.
- F2, exact only if the program prints complete=1: each constant Hamming weight 0 through 16, branch-and-bound on that slice alone. A slice that hits its time cap excludes nothing.
- F3, exact only if the program prints complete=1: unions of internally independent rotation orbits of Z/16Z. The orbit list is every necklace, ties broken by minimum representative.
- F4, exact only if the program prints complete=1: the 256 words of least deletion-ball size, ties broken by the integer whose least bit is the leftmost symbol. The list is written and hashed before the solve. A larger pool is a different family and is not searched unless named in a later prereg before it runs.

No threshold changes after a size is seen. A composition must be named as a composition. The (15,3) codes from the previous run are seeds only, not a claim.
