# Pre-registration

target_id: fmm-additive-complexity-records
frozen_utc: 2026-10-15T03:18:13Z
null_test: not needed because the claim is an explicit straight-line program checked by a deterministic exact checker (tensor identity over Z, ternary condition, addition count) against a table value

**Timing note.** The success rule below was copied verbatim from the bank into the search team's brief at
2026-10-15T03:18Z, before the search started; the 5x5x5 program was found later that morning. The rule was not chosen by us.

## Success rule (bank criterion, verbatim)

Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms
producing the outputs) for a format <n,m,p> with max(n,m,p) <= 8 and rank r equal to the best rank listed for that
format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is
verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions
STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live
repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched
live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between
already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not
allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format
page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the
format is attained only with non-ternary coefficients, the comparison is against the best count in the same
coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and
rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the
rank is a rank target, not this one.

## Statistic and threshold

- Statistic: the reduced addition count of the program (sum over all fresh and final forms of the number of terms minus
  one; negation free), after an exact check that every form is a ternary combination of already-computed quantities
  and that the 93 products and 25 outputs satisfy the full tensor identity for 5x5 times 5x5 over Z.
- Threshold: strictly less than the minimum reduced count over Perminov's live addition_reduced_ZT files for 5x5x5 at
  rank 93 (383 at the time of the brief), with rank 93 equal to the live best known rank, and below any
  comparable count on the Lille page or in matmulcatalog's COVERAGE.md.
