# How we found it (contributor text, unverified)

The brief: reproduce the Hospitalization Nowcast Hub's published evaluation (bank partial win p3) from the hub's own
files, and say exactly which rules are needed. The paper's evaluation code is in R; there is no R on the machine.
So the rules were read from the released R code and re-implemented in Python, one at a time, as a ladder:
- S0: no rules.
- S1: the exclusion list.
- S2: the four repairs, then the exclusion, in the released code's order.

What we saw:
- S0 already lands within 1% for 25 of 31 cells. Every cell sits 0.1-0.3% off, because 547 targets missing for some
  models are excluded for all models.
- The big misses each map to one rule:
  - LMU states (+11%): missing state rows filled from the hub's updated-models folder.
  - Epiforecasts (+2-3%): missing 0.1 quantiles interpolated.
  - RKI (undefined): NA and implausible 0-day values repaired.
- With all rules in place, 28 cells match to machine precision. The three Epiforecasts cells stay off by at most
  1.04e-4. That fits a closed-form two-point normal fit versus the R package's numerical fit: only the spread and
  overprediction components move. This is a hypothesis; we could not run R to confirm it.

Provenance checks:
- The evaluation's assembled submissions file matches, row for row, all 1,590 hub files the released loader reads.
- The FrozenBaseline equals the hub's raw triangle truncated as of each forecast date.
- The exclusion lists are re-derivable from the nowcast files.

Mismatches with the paper's text, raised by the NOVELTY skeptic: the RKI threshold and the number of excluded
targets in the S1 Appendix differ from the released code. Both are documented in
object/rules_and_discrepancies_addendum.md. The published tables follow the released code.

What failed or was not done:
- The same run also built a nowcaster for partial win p1. It beat the ensemble on the youngest and oldest age strata
  pooled, but the paper's own retrospective KIT 80-day rerun and ILM beat it on the same rows. It is not part of
  this package.
- This is a retrospective methods benchmark on an archived series, not public-health guidance.
