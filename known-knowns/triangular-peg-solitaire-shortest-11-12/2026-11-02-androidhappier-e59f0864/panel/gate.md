# Honesty gate — runs/2026-11-02-1731

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
No hedging panelist. Reproduce: independent checker confirms legal 22-move T11 solution a2→j11 (64 jumps); Bell fixtures calibrate; author's pegcheck.py and pegsim2.c agree. Novelty: live OEIS A127500 and Bell LargeTriangular page re-fetched 2026-11-02T18:17:50Z / 18:17:51Z still show upper bound 28; no PR/trophy/literature below 28. Criterion: full success (first alternative), first improvement past published 28, not p1.
Panel table fetch is under 6 hours old; no extra re-fetch required for the gate.
No downgrade triggers from kit/RUN.md step 7.

status: CONFIRMED_SOLUTION
confirmed_scope: The 22-move sequence in result/T11_22moves.txt is a legal Triangle(11) peg solitaire solution from the single vacancy a2 to the single peg j11 (64 jumps), checked by two included simulators and an independent re-check, so a(11) <= 22, strictly below the upper bound 28 in the OEIS A127500 and Bell page snapshots in data/; this is an upper bound only, not an exact value of a(11).
