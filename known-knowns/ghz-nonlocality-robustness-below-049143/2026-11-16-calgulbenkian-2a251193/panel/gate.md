# Honesty gate (ghz-nonlocality-robustness-below-049143)

status: CONFIRMED_SOLUTION
confirmed_scope: The 18x24x72 integer full-correlation Bell functional in object/bell_ghz3_18x24x72.json with planar projective qubit settings has exact local bound L = 130692616 (confirmed by two independent orbit-enumeration programs that agree) and Q_GHZ = 265961302.90703046706895787151..., so the white-noise-mixed three-qubit GHZ state is nonlocal for every v > 0.4913971114274656713239022, which beats the 0.49143 Table III value by more than 1e-5 and meets the stated full criterion for N = 3, subject to the NOVELTY skeptic's search finding no equal or better prior result.

## Gate notes
- Object: object/bell_ghz3_18x24x72.json, sha256 2a251193be2909afcb89ec74c13e10ef52aadf6b4cad148b6f82f7e4221a4b68.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- The bar is the best certified value, 0.49143 (arXiv:2310.20677 Table III), as the target's success criterion states; the target's pitfalls say the uncertified Table VI values (large m) are not the record to beat. The novelty skeptic's caveat about Table VI is therefore not a competing record under the criterion.
- The novelty skeptic found the status page unchanged from the package's snapshot (same sha256) on 2026-11-16 and no published certified value at or below the claim; the best published rigorous lower bound (0.49129) covers planar strategies only.
- The criterion skeptic's sentence leaves the literature comparison to the novelty skeptic; that skeptic passed (panel/novelty.md), so the condition in the sentence is met.
