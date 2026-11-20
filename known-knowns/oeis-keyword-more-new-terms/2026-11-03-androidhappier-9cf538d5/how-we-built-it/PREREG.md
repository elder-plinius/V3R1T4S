# PREREG (frozen 2026-11-03T16:42:32Z, before any program computed A325786 beyond its DATA)

Disclosure: for A336131 a scratch Program A/B (scratch/split) was written and run only for n = 0..17 (the DATA range) to
check the definition before this file; no value at n >= 18 had been computed. A325786: no program written yet.
target: oeis-keyword-more-new-terms, cell A325786(21)
criterion (verbatim): see target.md.
statistic: the exhaustive count defined in target.md (entry name + Mathematica code).
programs: (A) C exhaustive enumeration; (B) Go with a different generator and a different test algorithm; (C) Python
  literal transcription for small n. Written separately, no shared code.
thresholds: claim only if A and B reproduce every DATA term exactly and agree on a(21); OEIS value/context search shows
  no hit holding it as this count; history shows no pending draft.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
by-products beyond a(21) are not part of the claim.
