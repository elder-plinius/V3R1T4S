# Honesty gate (gf2-polymult-8term-25-products)

status: CONFIRMED_PARTIAL
confirmed_scope: object/gf128_0x89_81gates.slp.txt is an 81-gate (32 AND, 49 XOR, no constants) straight-line circuit that multiplies correctly in the standard polynomial basis modulo x^7 + x^3 + 1 on all 16384 input pairs, which is at most the 84-gate p2 threshold and below the 85-gate NIST/CMT circuit and the 83-gate Jain circuit, and it settles neither the 25-product 8-term problem nor p1 or p3.

## Gate notes
- Object: object/gf128_0x89_81gates.slp.txt, sha256 36e8f04dbd4563949141fa5aa0b4179fcdb2a55a9742aeb517f69004a452053f.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p2 of the target (x^7 + x^3 + 1 branch). The novelty skeptic re-read the NIST list of circuits and Peralta's CMT page (85 gates) on 2026-11-16 and found Swapnil Jain's 83-gate circuit as the closest published object; the claim is 81.
