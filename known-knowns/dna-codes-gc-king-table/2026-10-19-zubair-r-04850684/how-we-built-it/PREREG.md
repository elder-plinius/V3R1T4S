# PREREG: dna-codes-gc-king-table, run 2026-10-19-1601
frozen_utc: 2026-10-19T16:14:30Z

## Criterion (verbatim from bank/targets.json)
A plain-text list of codewords for some (n,d) whose table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':' such that a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming, AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature (e.g. Limbachiya-Gupta-Rao altruistic-algorithm papers, Montemanni-Smith, arXiv 1903.03535, 2108.02033).

## Statistic and checker
checker/check_gc_code.py CODEFILE n d TABLE. Statistic: the size m of a VALID code for (n,d), w = floor(n/2).

## Thresholds
- record: m > the King-page value (data/dnacodes.html, sha256 25d6e9f8...) at (17,13)=24, (18,14)=20 or (14,11)=17.
  Even then the claim is at most PROMISING until Montemanni-Smith-Koul 2014 is checked by hand and a 3-skeptic panel passes it.
- exhaustive negative: "no Z_17-invariant code of size 34 exists at (17,13)" may be stated only if the enumeration of
  self-compatible Z_17 orbits is complete (every word of length 17 with GC count 8, up to shift, visited), with the count
  of orbits printed and cross-checked by a second independent counting method on a smaller case (n=13, d=10),
  and the pair search over all orbit pairs is complete. Otherwise the result is stated as sampled.

null_test: not needed because any claim is an explicit code checked by a deterministic checker against a table value, and negatives are exhaustive enumerations, not statistics
