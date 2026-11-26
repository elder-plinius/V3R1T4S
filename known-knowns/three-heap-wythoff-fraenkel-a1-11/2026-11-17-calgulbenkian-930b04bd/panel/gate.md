# Honesty gate (three-heap-wythoff-fraenkel-a1-11)

status: CONFIRMED_SOLUTION
confirmed_scope: For N = 3 and smallest heap A1 = 11, under Sun and Zeilberger's convention, with n2 = 1216, n1 = 3249 and N3^i and B^i_{N3^i} recomputed for every i <= 10, the constants T^11, S^11, alpha = -61, N1 = N2 = 1214, N3 = 1381 and S1(3249) satisfy every hypothesis of their Claims 3.4 and 3.5, so both of Fraenkel's conjectures follow by their published Claim 3.5 and not by any independent formal proof; I reproduced this with separate code, and found no evidence it was already published.

## Gate notes
- Object: object/wythoff_a1_11_certificate.json, sha256 930b04bd94e8ab8f9624c92df6de6bd51224d79798f54c985560d2831d86755e.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- The first reproduce run failed for a missing input: the claim folder did not quote Sun and Zeilberger's Claims 3.4 and 3.5, so the skeptic could not check their conditions. The paper (Annals of Combinatorics 8 (2004), the copy on Zeilberger's site, sha256 e09b6d0e...) was added to the claim folder for the panel, and a fresh reproduce skeptic then passed, checking every condition with its own solver. The paper is not shipped in this package.
- The novelty skeptic read the GONC Unsolved Problems column on 2026-11-17 (it lists A1 <= 10 only); four further arXiv searches on 2026-11-17 found nothing on A1 = 11. The result relies on Sun and Zeilberger's Claim 3.5 as published.
