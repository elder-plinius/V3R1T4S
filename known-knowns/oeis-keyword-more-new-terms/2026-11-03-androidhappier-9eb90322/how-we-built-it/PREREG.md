# PREREG (frozen at the time in the next line, before any program computed A155520 beyond its DATA)
frozen: 2026-11-03T21:47:04Z

Disclosure: no drawing-count program exists in this workspace; no value of A155520 beyond row 5 has been computed here.
target: oeis-keyword-more-new-terms, cell A155520 row 6 (first missing flattened index 22 = A(6,1)).
criterion (verbatim): see target.md (copied verbatim from bank/targets.json).
statistic: for every ordered tree with 6 edges, its number of drawings; row 6 = histogram k -> #trees for k = 1..max (zeros kept inside the row).
programs: (A) Python backward leaf-deletion DP; (B) C forward leaf-insertion chain DP (BRIEF.md angles 1, 2).
thresholds: claim only if A and B both reproduce rows 1..5 exactly (flattened DATA indices 1..21), both satisfy row sum = Catalan(6) = 132 and sum k*A(6,k) = A014307(6) = 1787, and agree on the full row 6;
  the negative fixture differs from DATA; OEIS search of the row-6 prefix (first 4+ values, and DATA tail + row-6 head) shows no hit holding it as this triangle;
  entry/b-file/history re-fetched before claim show DATA unchanged and no pending draft. If row 6 contains zeros, the tabf convention (zeros inside the row) is disclosed.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
