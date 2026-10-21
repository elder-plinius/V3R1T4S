# PREREG v2: focused stage on A(26,6,9), review cadence for incremental gains (PREREG.md unchanged)

frozen_utc: 2026-10-16T20:58:57Z
Observed: 4 minutes into batch 1 (started 20:54:30Z) one walk reached 5992 (b1_plateau_s22_s104), one word above the
already confirmed and delivered 5991. Frozen at once (candidates/A26_6_9_5992_b1_s104.txt, sha256 9e48231b...0530),
both workspace checkers valid (20:58:44Z-20:58:45Z).
Decision (prospective, technical): within an active batch every improvement is frozen and checked by both checkers
immediately; the three-skeptic panel, the honesty gate and the package are run on the BEST code of each batch as soon
as the batch ends (at most 60 min after the first improvement), not on each +1. Reason: the cell already has a
confirmed, delivered record (5991), so waiting at most one batch does not risk priority, and one panel per batch keeps
the review complete without a panel per word. If a batch produces a jump of 5 or more words over the last confirmed
value, the panel starts immediately instead. Earlier claims (5988, 5991) are never rewritten; each new one is linked.
