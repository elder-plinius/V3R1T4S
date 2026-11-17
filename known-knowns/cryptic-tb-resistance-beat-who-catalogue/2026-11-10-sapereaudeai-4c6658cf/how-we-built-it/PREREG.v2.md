# PREREG.v2 (addendum; can only remove a claim, never add one)

written_at: Tue Nov 10 11:51:22 UTC 2026 (date -u). PREREG.md is unchanged.

What was seen before this file: the residual-model TEST results for all 13 drugs on split v2
(attempts/residual-model/model2_output.txt). Under PREREG.md's rule the main criterion is met for INH only (TEST model
993/64/17/1286 vs WHO-2023.5 987/70/20/1283). Inspection of the 11 TEST isolates where the two calls differ shows that
the 7 model-only true R calls carry filter-fail ('O') calls at katG S315 (6) or fabG1 c-15 / L203 (1), which the
look-up of PREREG.md lets match only '?' wildcards, and the 3 removed false R calls carry fabG1@t-8c.

Added robustness check, fixed now, before it is computed: a second, liberal reading of the comparator in which a
filter-fail call (alt O/o) at a gene position that carries any WHO-2023.5 R row for the drug (same gene and
position; amino-acid or nucleotide) counts as an R call. An INH claim (or any main-criterion claim) stands only if the
PREREG.md rule also holds against this liberal reading on TEST (same bootstraps, seed 20261110). If it does not, the
result is reported as reading-dependent and is not claimed.

BDQ meets PREREG.md's p1 point rule (TEST 5/13/14/2061 vs WHO 3/15/28/2047), but with two extra true R calls among 18
R isolates, a sensitivity-difference interval of -0.14 to 0.38 and a reversal on the never-held-out subset (model
1/12 vs WHO 2/11 true/false-negative R calls). It is reported and not claimed (a downgrade, not a new rule).
