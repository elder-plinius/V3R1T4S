# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 38 channels with 253 comparators and greedy depth 16 that sorts all 2^38 binary inputs (proved by exact reachable-set propagation), whose pair (253, 16) is non-dominated by the pairs [(250, 17), (254, 16)] on the Oct 13 2026 table and dominates the listed pair (254, 16), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N38_S253_D16.txt, sha256 e4ef45f9dda97a64c70c380dc0508ecb86e21b0654d8fa4248d58e30b3628f09.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
