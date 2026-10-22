# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 54 channels with 434 comparators and greedy depth 19 that sorts all 2^54 binary inputs (proved by exact reachable-set propagation), whose pair (434, 19) is non-dominated by the pairs [(421, 20), (435, 19)] on the Oct 13 2026 table and dominates the listed pair (435, 19), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N54_S434_D19.txt, sha256 a06aa15e8bce7af1bc7b6c18dd33b4230b8cad01d8be921c32b8180aa0a84fa0.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
