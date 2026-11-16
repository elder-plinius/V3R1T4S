# How We Built It

1. Audited live `google-deepmind/formal-conjectures` `main` (`e028240a61822d970c933f4656f51da025cf200b`) and open PRs; noted `ramsey_number_five_five_lower_bound` received a `formal_proof` link in commit `e028240a`, and selected `RamseyNumbers.ramsey_number_six_six_lower_bound` (`R(6,6) >= 102`).
2. Verified quadratic residues modulo `101` and the 24-vertex common neighborhood of `0` and `1` in the 101-vertex Paley graph `P(101)` via the helper script in this folder.
3. Formalized `paley101`, its multiplication-by-2 self-complementarity, its `AGL_1(ZMod 101)` two-point edge-transitivity, and a total structural-recursion clique-freeness checker proved sound in Lean 4 (`leanprover/lean4:v4.33.1`) inside `object/Solution.lean`.
