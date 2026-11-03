# PREREG (frozen at the time in the next line, before any program computed A131449 beyond its DATA)
frozen: 2026-11-03T21:54:14Z

Disclosure: no labeling-count program exists in this workspace; no value of A131449 beyond index 65 has been computed here (the hook formula makes T(6,2) = 360 predictable by hand; nothing was run).
target: oeis-keyword-more-new-terms, cell A131449 flattened index 66 (= row 6, m = 2), object = row 6 m = 2..132.
criterion (verbatim): see target.md (copied verbatim from bank/targets.json).
statistic: row 6 = increasing-labeling counts of the 132 ordered trees with 6 non-root vertices, non-increasing order (target.md).
programs: (A) Python hook formula on Dyck words; (B) C brute force over permutations / leaf-removal DP (BRIEF.md angles 1, 2).
thresholds: claim only if A and B both reproduce every DATA term (indices 0..65) exactly, row 6 has 132 entries summing to 10395 = A001147(6) in both, and A and B agree on the full sorted row 6;
  the negative fixture differs from DATA; OEIS search of the DATA tail + row-6 head (e.g. 2,1,720,360,...) shows no hit holding it as this triangle;
  entry/b-file/history re-fetched before claim show DATA unchanged and no pending draft. The ordering convention is disclosed as a risk; CRITERION judges it.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
