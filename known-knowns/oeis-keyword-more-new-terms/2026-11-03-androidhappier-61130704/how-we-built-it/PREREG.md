# PREREG (frozen 2026-11-03T16:18:26Z, before any attack program was written or run)

target: oeis-keyword-more-new-terms, cell A361864(12)
criterion (verbatim): see target.md "Success criterion".
statistic: the count of set partitions P of {1..n} such that median({median(B) : B in P}) is an integer, where
  median of a multiset of numbers = middle element (odd size) or mean of the two middle elements (even size),
  exactly as the A361864 comment states; block medians are taken over the block's elements, the outer median is
  over the multiset of block medians (with repetition).
programs: (A) C, restricted-growth-string enumeration with doubled/quadrupled integer arithmetic;
  (B) independent program in another language (Go) generating partitions by "block containing the smallest
  remaining element" over bitmasks with exact rational comparisons (num/den), no shared code;
  (C) Python brute force with fractions.Fraction for n <= 10 as a definition check.
thresholds: claim only if A and B both reproduce DATA a(1..11) exactly and agree on a(12); any mismatch = no claim.
  value search on OEIS for the a(12) value must return no entry containing it as A361864's term; history no pending draft.
null_test: not needed because the claim is an exact deterministic count checked by two independent programs against a table; no search/statistical inference.
extra terms a(13), a(14) may be computed as by-products; they are not part of the claim.
