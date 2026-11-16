# Honesty gate (post-tag-busy-beaver-bbpt)

status: CONFIRMED_SOLUTION
confirmed_scope: Under the wiki convention (size |A|+sum|w_a|, start 00, halt below 2 symbols), all 19,693 size-8 2-tag systems either halt (maximum 19 steps, only 111_20_) or have a checkable cycle or DFA-invariant non-halting certificate (including all 7 wiki holdouts), meeting criterion (b)/p1 for S=8 only, subject to the novelty skeptic finding no prior or merged equal result.

## Gate notes
- Object: object/bbpt8_certificates.json, sha256 54c967d97feea6e5559cd65788e0e777a0193163fa40f7ec62e060348672b1cd.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- The novelty skeptic read the BusyBeaverWiki status page on 2026-11-16: it lists BB_PT(8) >= 19 with 7 holdouts, so the exact value was open.
