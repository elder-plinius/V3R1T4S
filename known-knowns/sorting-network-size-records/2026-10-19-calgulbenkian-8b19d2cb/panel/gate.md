# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 51 channels with 387 comparators and greedy depth 21 that sorts all 2^51 binary inputs (proved by exact reachable-set propagation), whose pair (387, 21) is non-dominated by the pairs [(387, 22), (389, 20), (396, 19)] on the Oct 13 2026 table and dominates the listed pair (387, 22), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N51_S387_D21.txt, sha256 8b19d2cb06fb21333ee3b2e392b131340ec4899b2e659250b51e637c5c41cfc3.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
