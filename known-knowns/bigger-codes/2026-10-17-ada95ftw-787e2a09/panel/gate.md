# Honesty gate: A(31,10,7) <= 106 (claim/A31_10_7/, partial win p2)
status: CONFIRMED_PARTIAL
confirmed_scope: An exact rational Delsarte-LP dual certificate (Delsarte inequalities k=1,2 for J(31,7) plus the elementary constraint a_7 <= A(24,10,7) <= 24, using the published bound A(24,10,7) <= 24 (Agrell–Vardy–Zeger 2000, printed as 24 in Brouwer's table)) proves A(31,10,7) <= 106, strictly below the upper bound 109 printed for this cell in Brouwer's Andw.html as fetched 2026-10-17 08:44 UTC.
gate_utc: 2026-10-17T12:17:38Z
gate_by: the workspace's main assistant session (not one of the three skeptics), on the human's explicit go-ahead in chat

## What I read
- reproduce.md, novelty.md, criterion.md in this folder, all three written by separate fresh subagents that saw only claim/A31_10_7/ (each file has its own context: line). All three end with pass: true.
- REPRODUCE re-derived the certificate rows and multipliers exactly with its own checker; no mismatch.
- NOVELTY read the live table once, honestly (one plain request, no retries, HTTP 200) and found no equal or better upper bound in the literature it checked, in TROPHY_CASE.md or in the 92 open pull requests.
- CRITERION judged the claim literally against partial win p2 ("an exact rational dual certificate ... proving A(n,d,w) <= U for U strictly below the live tabulated upper bound"). Met: A(31,10,7) <= 106 vs printed 109.

## Downgrade checks (RUN.md step 7)
- hedging panelist: no. Each caveat is labelled by its panelist as not blocking, and I agree.
- reproduction mismatch: none.
- strictly better than the live table: yes (A(31,10,7) <= 106 < 109). The table was re-fetched once by the gate at 2026-10-17T12:15:46Z (HTTP 200, Last-Modified Sat, 17 Oct 2026 06:18:21 GMT, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8, the same bytes as the 08:02:33Z scout fetch), so the cell still prints 109. The panel's own fetches (08:31-08:45Z) were under 6 h old anyway.
- stretched criterion / hidden quantifier: no. This is a p2 partial win only; the main criterion (a bigger explicit code) is not claimed.
- scope wider than reproduced: no; confirmed_scope is the CRITERION sentence verbatim, except that the input-bound clause now cites the published bound A(24,10,7) <= 24 instead of an independent proof (wording only, per maintainer review 2026-10-25; verdict unchanged).
- sample presented as complete, capped search used as exclusion, probable prime: not applicable (one exact rational certificate).
- table value obtained by evasion: no (one plain curl per fetch, no retries).
- several objects bundled as one claim: no. One cell, one certificate.

## Caveats carried into the package (honest, not blocking)
- External input: A(24,10,7) <= 24 (printed as the single value "24"; NOVELTY found it stated as an upper bound in Agrell-Vardy-Zeger 2000, Example 2). The REPRODUCE skeptic could not re-derive it from first principles (got 27); with 25 the bound would still be 108 < 109, with 26 it would fail.
- Conditional on a published input that the panel could not re-prove.
- The method is classical (Delsarte 1973 LP plus an Agrell-Vardy-Zeger-style row a_x <= C(w,x)A(n-w,d,x)); this is new only as a table entry, in a cell whose printed n>28 upper bound is a Johnson bound.
- All four panels were subagents of the same assistant product (same-model context separation, disclosed).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
