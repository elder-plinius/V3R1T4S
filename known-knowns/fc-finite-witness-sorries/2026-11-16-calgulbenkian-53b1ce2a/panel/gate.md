# Honesty gate (fc-finite-witness-sorries)

status: CONFIRMED_SOLUTION
confirmed_scope: A kernel-checked Lean 4 v4.33.1 proof, compiled standalone with `lake env lean` against a clean checkout of formal-conjectures at e028240a (whose RamseyNumbers.lean, lean-toolchain and lake-manifest.json are identical to live main f50ff7be), of the verbatim, research-solved, still-`sorry`, formal_proof-free theorem RamseyNumbers.ramsey_number_six_six_lower_bound with axioms exactly propext, Classical.choice and Quot.sound, with no open PR found proving or linking it (not a spliced in-tree `lake build`, and PR file lists not enumerated for all 798 open PRs).

## Gate notes
- Object: object/Solution.lean, sha256 53b1ce2a8a0e258b3fed499681bbb63ce796625b6bd2f38e093340f483a55275.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel is the referee. Re-checked on 2026-11-16: formal-conjectures live main (f50ff7be) has the same FormalConjectures/Wikipedia/RamseyNumbers.lean, lean-toolchain and lake-manifest.json as the pinned commit e028240a, and the theorem still ends in sorry there; the proof compiles in a clean checkout at e028240a, its pp.all type equals the upstream declaration's, and #print axioms lists only propext, Classical.choice and Quot.sound.
