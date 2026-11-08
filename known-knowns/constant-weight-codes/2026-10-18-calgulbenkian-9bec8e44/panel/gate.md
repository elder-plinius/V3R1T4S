# Honesty gate (constant-weight-codes)

status: CONFIRMED_SOLUTION
confirmed_scope: A word list of 3802 distinct binary words of length 28, weight exactly 11 and minimum pairwise distance 8 (>= 8, d even) was verified exactly, so A(28,8,11) >= 3802, strictly above the lower bound 3791 (label Ol) printed in that cell of Andw.html as fetched 2026-11-06T20:26:09Z (page sha256 91479623612b85a1782b729dc88563c3a944c65f7181b7965964a08de1a52e82) and below the printed upper bound 11896; the page has no mirror cell A(28,8,17); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.

## Gate notes
- Object: object/A28_8_11_3802.txt, sha256 9bec8e442ef7b35ee427a3dd311c77ae66677b1a0e38cd95d03756e1ea4ae335.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word, with the bar updated on 2026-11-06 (see below and the note in panel/criterion.md).
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell; not a partial win. One cell per claim.
- Reproduce: own exhaustive check of count, distinctness, weight and every pairwise distance. Novelty: live Andw.html re-fetched 2026-10-18T17:54Z (sha256 15b15c8d, unchanged), Echols arXiv:2608.13906 table read in full, Lysenstoen and Yang et al. abstracts, V3R1T4S pull requests pages 1 to 5, TROPHY_CASE and the merged bigger-codes family.
- On 2026-10-18 the live lower bound for this cell was a code from the merged V3R1T4S bigger-codes family (3785, label Pl). Updated 2026-11-06 on maintainer review (#440): the live cell, fetched 2026-11-06T20:26:09Z (sha256 91479623), now reads 3791 (label Ol, Antoine Olivier). This claim beats it by 11. The panel reports were run against the 2026-10-18 page.
- No earlier filing of this cell by the author.
- No downgrade triggers found.
