# Criterion review: z(16,19;3,3) >= 142
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
confirmed_scope: The saved 16 x 19 0/1 matrix matrix/z_16x19_142.txt (sha256 47ef934e...) has 142 ones and no all-ones 3 x 3 submatrix, which is strictly above the best explicit lower bound 136 recorded in status_source/ for z(16,19;3,3) and above 141, the best that 192000 saved trivial-surgery runs on 12 public witness matrices reached, with the limits that the status pages were not re-fetched here and the surgery baseline is a bounded sample.

## Reasoning
- Validity: check/check_matrix.py re-run on the matrix prints PASS (142 ones, 16x19, both methods agree); sha256 matches CLAIM.md.
- Baseline 136: status_source/df_new_bounds.json (dfield repo copy) lists 16,19 lower = 136; status_source/scout_record.md attributes 136 to Saurabh's zero-column padding of 16x18/136, and 132 to Bhan et al. Nothing saved states a higher value. Caveat: scout_record.md is the author's own record; the live sources were not re-fetched (no web allowed), so "best stated 136" rests on the saved files only.
- Subsumption: I checked the saved table for larger shapes. 16x20 = 146 gives at most 139 by min-column deletion; 16x21 = 148, 16x23 = 158, 15x20 = 138 give less. status_source/lb_closure_output.txt gives a closure of 139 even with all rules (monotone, +2 line, min-line deletion). Nothing implies 142 by line deletion, so not subsumed.
- Trivial-derivation policy: the surgery baseline (baseline/output/surgery_16x19_seed1..4.txt, 48000 runs per seed shown in seed1 tail, 192000 total) tops out at 141 with 0 runs at 142; derivability_output.txt shows 0 exact sub-matrix copies of the 10 fitting public bases. The matrix was found by an independent local search, and six reruns (search/output) all reached 142 within 16 s to 3 min, one isomorphic to the claim, none reached 143. So 142 is a searched object, not an end-trim, append or padding. The residual risk is that the baseline is a sample of one family, which the claim states openly; this is evidence, not proof, and it does not defeat a literal reading of the criterion (strictly exceeding every explicitly stated bound, and not an end-trim or padding of a published matrix).
- Null model concerns: 142 is easy for a plain local search, so priority risk exists (unpublished holders), but the criterion is about published values. The +1 over the 141 surgery plateau is thin but supported by 66663 hits at 141 and zero at 142 versus six of six searches reaching 142.
- No hidden quantifier found: the claim is one cell, no wider scope claimed. Upper bound 147 does not contradict.
- Limits: OEIS, Guy and live arXiv not checked by the author or by me.

pass: true
