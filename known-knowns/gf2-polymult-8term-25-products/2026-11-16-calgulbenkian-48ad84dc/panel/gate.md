# Honesty gate (gf2-polymult-8term-25-products)

status: CONFIRMED_PARTIAL
confirmed_scope: The file object/gf128_0x91_82gates.slp.txt is a valid 82-gate (34 AND, 48 XOR) AND/XOR circuit that exhaustively matches standard polynomial-basis multiplication in GF(2^7) modulo x^7+x^4+1 on all 16384 input pairs, meeting partial win p2's 83-gate limit for that polynomial and beating the NIST/CMT 84 and Jain 87 figures, subject to the novelty skeptic's confirmation that no smaller published circuit exists.

## Gate notes
- Object: object/gf128_0x91_82gates.slp.txt, sha256 48ad84dc1afddd567bcccf6574447aa229e3371548afa57f386fe2779897f100.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p2 of the target (x^7 + x^4 + 1 branch). The novelty skeptic re-read the NIST list of circuits and Peralta's CMT page (84 gates) on 2026-11-16; Swapnil Jain's repository lists 87 gates for this modulus; the claim is 82.
- The criterion skeptic's sentence leaves the literature comparison to the novelty skeptic; that skeptic passed (panel/novelty.md), so the condition in the sentence is met.
