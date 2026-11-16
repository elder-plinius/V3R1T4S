# Honesty gate (bivariate-bicycle-exact-distance-360-756)

status: CONFIRMED_PARTIAL
confirmed_scope: An explicit weight-28 nontrivial logical operator (index-negated labeling of the standard convention, equivalent by relabeling) exists for the [[504,12]] covering BB code with l=42, m=6, A=x^27+y+y^2, B=y^3+x^37+x^38, verified exactly over GF(2), so its minimum distance is at most 28, below the published bound of 30; no lower bound, no exact distance, and no claim on the 360, 432 or 756 codes.

## Gate notes
- Object: object/bb504_logical_wt28.txt, sha256 2894986d2179d2db637805691c36033eae41721b9d29267c58d044d85da0f878.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p1 of the target for the [[504,12,<=30]] covering code: an upper bound of 28, not an exact distance. The witness satisfies the checks in the package's shift convention, which is the code of the stated l, m, A and B up to the qubit relabelling (i,j) -> (-i,-j) in both blocks; the reproduce and criterion skeptics both proved that this relabelling preserves the code and all weights.
