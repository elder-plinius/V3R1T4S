# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 53 channels with 422 comparators and greedy depth 19 that sorts all 2^53 binary inputs (proved by exact reachable-set propagation), whose pair (422, 19) is non-dominated by the pairs [(411, 22), (412, 21), (414, 20), (423, 19)] on the Oct 13 2026 table and dominates the listed pair (423, 19), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N53_S422_D19.txt, sha256 4ed72ca5cb966a3d915e0769777a0750e0a2b98aa5109f5efe81db821e374a12.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
