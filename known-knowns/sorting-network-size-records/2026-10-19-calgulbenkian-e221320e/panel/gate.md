# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 57 channels with 458 comparators and greedy depth 20 that sorts all 2^57 binary inputs (proved by exact reachable-set propagation), whose pair (458, 20) is non-dominated by the pairs [(454, 21), (461, 20)] on the Oct 13 2026 table and dominates the listed pair (461, 20), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N57_S458_D20.txt, sha256 e221320e3d190b87782aee7c6753917b43c49196cc567add0ed233c89dbffb4a.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
