# Honesty gate (qrac-qutrit-three-trits-smallest-open)

status: CONFIRMED_PARTIAL
confirmed_scope: The shipped rational dual certificate, verified exactly in Fraction arithmetic and independently confirmed numerically on random operators, proves ASP(3,3,3) <= 4368312591/6250000000 = 0.69893001456 <= 0.6990 for all states and all 3-outcome POVMs on C^3 via a Naimark-dilation relaxation that assumes no projectivity of the physical measurements, which meets enumerated partial win p1 only and does not meet criterion (b) (< 0.69853) or (a).

## Gate notes
- Object: object/qrac_333_naimark_dual_p1.json, sha256 d0e7e416ae05f09145419e9f54da3bf13d17408fdc3245a94c87ecdd40ab8b85.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p1 of the target: a rigorous POVM-valid upper bound, 4368312591/6250000000 = 0.69893001456, at most 0.6990. The full criterion (b) needs a bound below 0.69853 and is not claimed. The reproduce skeptic verified dual feasibility in exact rational arithmetic (78 LDL^T blocks and the assembled 203 x 203 matrix) and re-derived that the simultaneous Naimark dilation covers every POVM on C^3.
- The novelty skeptic read arXiv:2312.14142 on 2026-11-17: its lower numbers (down to 0.69853) assume projective measurements or are floating-point; the best published rigorous POVM-valid bound is 0.71823.
