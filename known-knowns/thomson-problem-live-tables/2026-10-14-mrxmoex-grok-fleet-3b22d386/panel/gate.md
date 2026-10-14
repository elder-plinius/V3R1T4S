# Honesty gate (main session) — C_550 only
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (C_550 round, fresh executors).
Table fetch age: the criterion skeptic used the 07:28Z snapshot, but the novelty skeptic re-fetched live at 2026-10-14T14:56:23Z (HTTP 200) and the N = 550 row was unchanged (144126.0927100). Gate at 2026-10-14T15:33Z, under 6 h after the live fetch, no further re-fetch needed.
Downgrade checks (never upgrade): no hedging; reproduction matches; gap 9.0e-5 > 1e-6. Direction caveat: the posted cell is LOWER than its own coordinates reproduce (likely a transcription slip; the xyz header gives 144126.0927999970). p1 is met literally. This is not an energy improvement. One object; scope limited to p1.
status: CONFIRMED_PARTIAL
confirmed_scope: For N = 550 only, the CCD Thomson2 table's posted energy (144126.092710000) is not reproduced by its own posted coordinates (data/t2_550.xyz), whose mpmath-polished energy is 144126.092800000 (12 digits; difference +8.9999e-5 > 1e-6), satisfying partial win p1 and nothing more.
