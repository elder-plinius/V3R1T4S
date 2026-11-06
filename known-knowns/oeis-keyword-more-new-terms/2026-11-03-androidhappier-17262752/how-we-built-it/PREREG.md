# PREREG (frozen 2026-11-03T16:25:52Z, before any attack program for A326335 was written or run)

target: oeis-keyword-more-new-terms, cell A326335(11)
criterion (verbatim): see target.md.
statistic: the count defined in target.md (entry comment + Mathematica code), over all set partitions of {1..n}.
programs: (A) C, restricted-growth strings, explicit element-quadruple tests per block pair, union-find connectivity;
  (B) Go, lowest-element bitmask generator, bitmask/popcount characterisations of capturing/nesting, BFS connectivity;
  written separately, no shared code. Both also print A326245/A326246/A326249/A326335/A326336 as cross-checks.
thresholds: claim only if A and B reproduce every DATA term of A326335 exactly and agree on a(11); OEIS value search
  for the new term shows no hit holding it as this count; history shows no pending draft.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
by-products beyond a(11) are not part of the claim.
