# Honesty gate: A(34,10,8) <= 618 (claim/A34_10_8/, partial win p2)
status: CONFIRMED_PARTIAL
confirmed_scope: cert_A34_10_8.json, checked by verify.py in exact rational arithmetic and independently re-derived (Q via inverse eigenmatrix; primal LP optimum 114444/185), proves A(34,10,8) <= 618 from Delsarte's inequalities for J(34,8) plus the shell-counting constraint a_7 <= 8*A(26,10,7), conditional on the published upper bound A(26,10,7) <= 36 printed in Brouwer's table (still giving <= 630 if that input were only 37), which is strictly below the live tabulated upper bound 637 for this one cell.
gate_utc: 2026-10-17T12:17:38Z
gate_by: the workspace's main assistant session (not one of the three skeptics), on the human's explicit go-ahead in chat

## What I read
- reproduce.md, novelty.md, criterion.md in this folder, all three written by separate fresh subagents that saw only claim/A34_10_8/ (each file has its own context: line). All three end with pass: true.
- REPRODUCE re-derived the certificate rows and multipliers exactly with its own checker; no mismatch.
- NOVELTY read the live table once, honestly (one plain request, no retries, HTTP 200) and found no equal or better upper bound in the literature it checked, in TROPHY_CASE.md or in the 92 open pull requests.
- CRITERION judged the claim literally against partial win p2 ("an exact rational dual certificate ... proving A(n,d,w) <= U for U strictly below the live tabulated upper bound"). Met: A(34,10,8) <= 618 vs printed 637.

## Downgrade checks (RUN.md step 7)
- hedging panelist: no. Each caveat is labelled by its panelist as not blocking, and I agree.
- reproduction mismatch: none.
- strictly better than the live table: yes (A(34,10,8) <= 618 < 637). The table was re-fetched once by the gate at 2026-10-17T12:15:46Z (HTTP 200, Last-Modified Sat, 17 Oct 2026 06:18:21 GMT, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8, the same bytes as the 08:02:33Z scout fetch), so the cell still prints 637. The panel's own fetches (08:31-08:45Z) were under 6 h old anyway.
- stretched criterion / hidden quantifier: no. This is a p2 partial win only; the main criterion (a bigger explicit code) is not claimed.
- scope wider than reproduced: no; confirmed_scope is the CRITERION sentence verbatim.
- sample presented as complete, capped search used as exclusion, probable prime: not applicable (one exact rational certificate).
- table value obtained by evasion: no (one plain curl per fetch, no retries).
- several objects bundled as one claim: no. One cell, one certificate.

## Caveats carried into the package (honest, not blocking)
- External input: A(26,10,7) <= 36 (printed "30-36"; with 37 the bound would be 630, still below 637).
- Pure Delsarte alone gives 662.5; the win depends on the shell-counting row a_7 <= 8*A(26,10,7).
- The method is classical (Delsarte 1973 LP plus an Agrell-Vardy-Zeger-style row a_x <= C(w,x)A(n-w,d,x)); this is new only as a table entry, in a cell whose printed n>28 upper bound is a Johnson bound.
- All four panels were subagents of the same assistant product (same-model context separation, disclosed).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
