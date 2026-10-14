# Honesty gate (main session) — B_3552 only
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (B_3552 round, fresh executors).
Table fetch age: novelty live fetch 2026-10-14T14:53:45Z (HTTP 200, page sha256 eeac3235…, unchanged); criterion re-fetched ~14:55Z; gate at 2026-10-14T15:33Z, under 6 h, no re-fetch needed.
Downgrade checks (never upgrade): no hedging; reproduction matches to all digits; gap 1.4955e-5 > 1e-6; same basin, no new configuration claimed; one object; scope limited to p1 table integrity. Criterion noted points_3552_1.dat missing from the claim folder at panel time; it is now present with the matching sha256 837f6c84…. Not a scope issue.
status: CONFIRMED_PARTIAL
confirmed_scope: For N = 3552, polishing the live CCD Riesz s=1 table's own posted coordinates (points_3552_1.dat) to a stationary point gives energy 6191355.68664355, which is 1.4955e-5 below the posted cell value 6191355.6866585, so the posted energy is not reproduced to within 1e-6 (table-integrity partial win p1 only, same basin, no new configuration).
