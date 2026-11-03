# PREREG (frozen 2026-11-03T20:05:19Z, before any program for A331783 was written or run; no value beyond DATA computed)

target: oeis-keyword-more-new-terms, cell A331783(21)
criterion (verbatim): see target.md (copied verbatim from bank/targets.json).
statistic: the exact count of locally disjoint rooted semi-identity trees with 21 vertices as defined by the entry name, comments
  and Mathematica code (BRIEF.md).
programs: (A) C id-multiset backtracking with mark counts; (B) Go literal partition x tuple transcription; (C) Python
  Matula-Goebel / A331682 rule for small n. Written separately for this run.
thresholds: claim only if A and B both reproduce every DATA term a(1..20) exactly and agree on a(21); negative fixture (no
  disjointness) differs from DATA; OEIS value search of a(21) shows no hit holding it as this count; entry/b-file/history
  re-fetched before claim show DATA still ending at a(20) and no pending draft.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
by-products beyond a(21) are not part of the claim.
