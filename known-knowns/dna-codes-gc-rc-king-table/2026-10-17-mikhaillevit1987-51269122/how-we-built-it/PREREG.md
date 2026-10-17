frozen: 2026-10-17T13:37:08Z

A codeword list for some (n,d) whose A_4^GC,RC entry on https://rambutan.umassmed.edu/king/dnacodes.html is not followed by '.' or ':', checked to satisfy: length n, alphabet ACGT, GC count = floor(n/2), pairwise Hamming >= d, Hamming(x, rc(y)) >= d for all x,y including x=y, distinct; size strictly greater than the live table entry re-fetched immediately before claiming and than any post-2010 published value for the same parameters (novelty search, e.g. arXiv 1903.03535 lists GC,RC improvements).

statistic: exact cardinality of an explicit codeword list, conditioned on every fixed-GC, Hamming and reverse-complement constraint passing check_dna.py. Compare against the saved eligible table cell and all later published values found before any claim.
threshold: strictly greater than both comparison values; a tie is not a win. Enumerated partial wins judged literally from target.md.
null_test: not needed because an explicit object is checked by a deterministic checker against a table value; no statistical or beats-chance claim will be made.

Lenses: structured constructions and direct penalty optimization, independently implemented. Parameter candidates are all unmarked cells in data/table.json with code size at most 40; larger cells may be exploratory but require the same exact criterion. Bounded heuristic failures are not exhaustive exclusions.
