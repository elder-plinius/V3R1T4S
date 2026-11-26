The size-43 list was returned by a CP-SAT model: one binary variable per length-16 word, and one constraint per length-13 subsequence that at most one selected word contains it. The objective was the number of selected words. A locally constructed 42-word code was given as a hint. Time limit 2400 seconds, four workers. The solver reported feasible, objective 43, not optimal.

Requirements, not in the standard library: ortools (the run used the package available as ortools on 2026-11-06).

The pre-registration is PREREG.md in this folder. No null test was required: the claim is an explicit codebook checked by a deterministic pairwise LCS checker against the table value 43.
