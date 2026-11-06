# Honesty gate (constant-weight-codes)

status: CONFIRMED_SOLUTION
confirmed_scope: A word list of 2218 distinct binary words of length 35, weight exactly 6 and minimum pairwise distance 6 (>= 6, d even) was verified exactly, so A(35,6,6) >= 2218, strictly above the lower bound 2217 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 3249; the page has no mirror cell A(35,6,29); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.

## Gate notes
- Object: object/A35_6_6_2218.txt, sha256 dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell; not a partial win. One cell per claim.
- Reproduce: own exhaustive check of count, distinctness, weight and every pairwise distance. Novelty: live Andw.html re-fetched 2026-10-18T17:54Z (sha256 15b15c8d, unchanged), Echols arXiv:2608.13906 table read in full, Lysenstoen and Yang et al. abstracts, V3R1T4S pull requests pages 1 to 5, TROPHY_CASE and the merged bigger-codes family.
- The live lower bound for this cell is a code from the merged V3R1T4S bigger-codes family (label Pl in the table); this claim beats it.
- Refile: the author filed the same value as pull request #59, closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect.
- No downgrade triggers found.
