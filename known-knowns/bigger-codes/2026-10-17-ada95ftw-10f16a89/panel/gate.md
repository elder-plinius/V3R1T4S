# Honesty gate: A(32,10,7) <= 131 (claim/A32_10_7/, partial win p2)
status: CONFIRMED_PARTIAL
confirmed_scope: An exact rational LP dual certificate in cert_A32_10_7.json combines the Delsarte inequalities D1 and D2 for J(32,7) with the standard distance-distribution constraint a_7 <= A(25,10,7) <= 32, whose input follows from A(24,10,6) <= 9 by Johnson; verify.py and an independent recomputation check it, and it proves A(32,10,7) <= 131, strictly below the upper bound 139 printed for that single cell in Brouwer's live Andw.html table as fetched on 2026-10-17.
gate_utc: 2026-10-17T12:17:38Z
gate_by: the workspace's main assistant session (not one of the three skeptics), on the human's explicit go-ahead in chat

## What I read
- reproduce.md, novelty.md, criterion.md in this folder, all three written by separate fresh subagents that saw only claim/A32_10_7/ (each file has its own context: line). All three end with pass: true.
- REPRODUCE re-derived the certificate rows and multipliers exactly with its own checker; no mismatch.
- NOVELTY read the live table once, honestly (one plain request, no retries, HTTP 200) and found no equal or better upper bound in the literature it checked, in TROPHY_CASE.md or in the 92 open pull requests.
- CRITERION judged the claim literally against partial win p2 ("an exact rational dual certificate ... proving A(n,d,w) <= U for U strictly below the live tabulated upper bound"). Met: A(32,10,7) <= 131 vs printed 139.

## Downgrade checks (RUN.md step 7)
- hedging panelist: no. Each caveat is labelled by its panelist as not blocking, and I agree.
- reproduction mismatch: none.
- strictly better than the live table: yes (A(32,10,7) <= 131 < 139). The table was re-fetched once by the gate at 2026-10-17T12:15:46Z (HTTP 200, Last-Modified Sat, 17 Oct 2026 06:18:21 GMT, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8, the same bytes as the 08:02:33Z scout fetch), so the cell still prints 139. The panel's own fetches (08:31-08:45Z) were under 6 h old anyway.
- stretched criterion / hidden quantifier: no. This is a p2 partial win only; the main criterion (a bigger explicit code) is not claimed.
- scope wider than reproduced: no; confirmed_scope is the CRITERION sentence verbatim.
- sample presented as complete, capped search used as exclusion, probable prime: not applicable (one exact rational certificate).
- table value obtained by evasion: no (one plain curl per fetch, no retries).
- several objects bundled as one claim: no. One cell, one certificate.

## Caveats carried into the package (honest, not blocking)
- External input: A(25,10,7) <= 32 (printed "28-32" in the table; the REPRODUCE skeptic also re-proved it from A(24,10,6) <= 9 by a counting argument plus Johnson).
- None beyond the input.
- The method is classical (Delsarte 1973 LP plus an Agrell-Vardy-Zeger-style row a_x <= C(w,x)A(n-w,d,x)); this is new only as a table entry, in a cell whose printed n>28 upper bound is a Johnson bound.
- All four panels were subagents of the same assistant product (same-model context separation, disclosed).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
