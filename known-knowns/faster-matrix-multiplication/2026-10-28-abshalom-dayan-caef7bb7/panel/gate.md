# Honesty gate (run 2026-10-28-2200, main session)

claim: the scheme in claim/object/ is an exact rank-1644 bilinear scheme over Q for <14,15,13>, a permutation of the
sorted format <13,14,15> (main success criterion).

status: CONFIRMED_SOLUTION
confirmed_scope: The files object/u.txt (sha256 caef7bb7...), object/v.txt (b31e5e77...) and object/w.txt (79b90daf...) define a bilinear scheme over Q with exactly 1644 rank-one terms and no zero factors that satisfies all 7452900 Brent equations for <14,15,13> in exact arithmetic (and, after the cyclic relabelling, for <13,14,15>), which is strictly below the rank 1681 that fmm_sota.json, the Lille page 13x14x15.html and the minimum of Perminov's ZT/Z/Q columns in docs/ranks.md each list for (13,14,15) as re-fetched at 2026-10-28T22:33Z, strictly below the rank 1645 merged in this repository, and in a cell where MerlijnW70/fmm-schemes lists no scheme.

Gate written 2026-10-28T22:26:06Z. Updated 2026-10-28T22:38:34Z for the CRITERION re-run.

How the panel was run: claim/ frozen at 22:10Z (panel/claim.sha256, 17 files) and re-checked unchanged after each
skeptic. Three fresh subagents, one after another, each given only its own copy of claim/: REPRODUCE (Claude Sonnet
5.5, about 22:11-22:15Z), NOVELTY (Claude Opus 5.5, about 22:15-22:21Z), CRITERION (Claude Opus 5.5, about
22:21-22:25Z, then re-run by a fresh Opus 5.5 subagent about 22:33-22:38Z on an unchanged copy, see below). All end
with pass: true. The NOVELTY and CRITERION table fetches are minutes old (22:16-22:19Z, 22:23Z, 22:33Z), so no gate re-fetch was needed (the packaging step re-fetches anyway, per NEXT_RUN.md).

What the gate read and decided:
- REPRODUCE: own exact checker written from the definition before reading the author's code; all 7,452,900 Brent
  equations, 0 wrong; 1644 terms, no empty factors, no duplicate, proportional or two-factor-sharing terms; lcm of the
  denominators 5440 as claimed; the merged 1645 decoded independently passes; 4 planted negatives fail; author's checks
  PASS twice, byte-identical output; rebuild from LITA 15^3 r1977 byte-identical. Its only discrepancy is cosmetic:
  REPRODUCE.md's expected rebuild output shows the npz path as ../../data/lita/... and a different "wrote ... to"
  path; the hash is the same. Not a downgrade; fixed in the package text.
- NOVELTY: status source and the four criterion sources fetched once each (HTTP 200, sha256 equal to TABLE_RECORD.md);
  bar 1681 in all catalogues, matmulcatalog 1681; merged 1645 (#166); all 781 PRs (pulls list API, 8 pages, numbers
  1-811) have nothing at or below 1644 for any ordering; literature (Perminov 2603.02398, 2606.02480, Kauers-Wood
  2510.19787, 2511.20317, LITA tree): nothing at or below 1644 (abstracts and snippets only, stated). No hedge.
- CRITERION re-run (why): the first CRITERION verdict (pass: true, kept as panel_ws/criterion/criterion.v1.md, not
  shipped) quoted the criterion's Lille URL template with angle brackets, which the package check rejects as an
  unfilled placeholder; panel files may not be edited after the gate, so a fresh CRITERION subagent was run on an
  unchanged copy of claim/ with one added formatting rule (no single word inside angle brackets). Its verdict and
  scope are the ones of record; both runs agree (pass, same clauses, same values, both built and checked the rotated
  <13,14,15> scheme).
- CRITERION: criterion text equal to the bank string (compared by script); clause by clause met; permutation argument
  checked by building the rotated <13,14,15> scheme and checking it exactly; no null model applies (explicit object,
  deterministic exact check); Merlijn bar met vacuously (no entry). Scope above copied exactly.
- Downgrade checks: no reproduction mismatch; 1644 strictly below the live minimum 1681 (margin 37) and the merged 1645
  (margin 1; strict, so not a tie); no PR at or below; no stretched clause; scope no wider than what was reproduced; no
  sample presented as complete; no capped search used as an exclusion; no probable primes; table access by one honest
  GET each (no evasion found, 0 lines in attempts/contrarian/evasion_grep.txt); one object per claim (the cut-30
  sibling is cited only).
