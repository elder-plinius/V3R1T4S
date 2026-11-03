# PREREG (frozen 2026-11-03T20:01:18Z, before any program for A316471 was written or run; no value beyond DATA computed)

target: oeis-keyword-more-new-terms, cell A316471(21)
criterion (verbatim): see target.md (copied verbatim from bank/targets.json).
statistic: the exact count of locally disjoint rooted identity trees with 21 nodes as defined by the entry name + Mathematica
  code (BRIEF.md).
programs: (A) C canonical-id backtracking enumeration with bitset disjointness; (B) Go literal partition x tuple generation
  then filter; (C) Python Matula-Goebel characterization for small n. Written separately, no shared code.
thresholds: claim only if A and B both reproduce every DATA term a(1..20) exactly and agree on a(21); negative fixture (no
  disjointness test) reproduces A004111 terms in DATA range in both A and B; OEIS value search of a(21) shows no hit holding it
  as this count; entry/b-file/history re-fetched before claim show DATA still ending at a(20) and no pending draft.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
by-products beyond a(21) are not part of the claim.
