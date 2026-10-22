# Honesty gate (sorting-network-size-records)

status: CONFIRMED_PARTIAL
confirmed_scope: A standard-form network on 58 channels with 469 comparators and greedy depth 20 that sorts all 2^58 binary inputs (proved by exact reachable-set propagation), whose pair (469, 20) is non-dominated by the pairs [(465, 21), (471, 20)] on the Oct 13 2026 table and dominates the listed pair (471, 20), and is not obtained by the wire-deletion reductions I tried; this is the partial win p1 only, outside the 13..32 range of the main criterion.

## Gate notes
- Object: object/N58_S469_D20.txt, sha256 f9d89cde03cfc8905aecdd3fb1d2096f67c5490f666e2645791b86fdb524b350.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim package; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The propagation test (removing wires from listed networks) covered top and bottom wire fixings, any-wire fixings for up to two deletions, and removal of inactive comparators; deeper reductions were not tried.
