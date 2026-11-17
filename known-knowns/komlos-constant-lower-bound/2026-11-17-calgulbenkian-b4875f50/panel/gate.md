# Honesty gate (komlos-constant-lower-bound)

status: CONFIRMED_PARTIAL
confirmed_scope: The stored rational 15x15 matrix object/komlos_15x15_p2.txt (integers over 10^12, all 15 column squared norms <= 1 exactly) has exact discrepancy 205956508661/10^11 = 2.05956508661 over all sign vectors, strictly above 2.006 and above 2, so it meets partial win p2 (and p1) but not the full criterion.

## Gate notes
- Object: object/komlos_15x15_p2.txt, sha256 b4875f5077ae1c70895dcf38764ff27746fc573ffd284c10dd08723097de5113.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p2 (which also meets p1); the full criterion (discrepancy above 1 + sqrt 2) is not claimed. Two independent exact programs (exact fractions over all 2^15 sign vectors, and integer meet-in-the-middle) and a separate integer Gray-code checker all give d = 205956508661/100000000000; all 15 columns have squared norm at most 1, checked exactly on the stored integers over 10^12.
- The novelty skeptic read the status page (teorth.github.io/optimizationproblems, constant 24a) and Kunisky, arXiv:2111.02974, on 2026-11-17: the only reported example with at most 15 columns is D. Spielman's unpublished one, with discrepancy in [2.005, 2.006]; Kunisky's tree matrices first exceed 2 at 16 columns (2.0607).
