# Optional: Lean 4 check

`DnaCode20_15.lean` restates the object and proves `lower_bound` (16 words, GC 10, distance >= 15,
reverse-complement distance >= 15 including self-pairs) by `decide` (kernel evaluation, no `native_decide`).
Checked with Lean 4.34.0-rc2 and Mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`;
`#print axioms DnaCode20_15.lower_bound` gives `[propext, Classical.choice, Quot.sound]`. About 70 s.
Not run by `run_checks.sh` (needs a Lean + Mathlib install).
