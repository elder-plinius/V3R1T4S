# PREREG frozen at the time below (before any attack output of this run is scored)
frozen_utc: 2026-10-16T08:50:58Z
target: packomania-scu-spheres-in-cube (open).
criterion: verbatim in target.md.
statistic: r* = min(min_{i<j}|ci-cj|/2, 1/2 - max_i max|coord|) in mpmath at 50 digits, no tolerance (checker/scu_check.py, tested on scu100 positive/negative in checker/selftest_0845.txt).
threshold: r* - r_table(N) >= 1e-11 against data/radius.txt and a live re-fetch before any claim; not isometric to posted scu<N>.txt (checker/isometry.py, sorted distance multisets differ by > 1e-9); N not in a newer History line or the scu pending list; Moki&Julio dataset checked for the same N.
extra rules frozen now:
- Rows 795/794/793 derived from the unpanelled 796 candidate count as PROMISING only if, after deletion and re-relaxation, r* exceeds the 796 candidate's own r* (0.05735794878124123) by >= 1e-11. Otherwise they are a consequence of the 796 claim (subsumed), recorded and not claimed.
- Any candidate equal (to 1e-11) to a sub-configuration of a posted Packomania file (deletion only, no relaxation gain) is a table-consistency observation, not a claim.
- One cell per claim; if several plateau rows beat the table, each is its own claim, and the report says they share one method.
- Rows with an existing PR on the public repo are reported but marked "competing PR exists".
PROMISING (self-judged, unpanelled): all of the above pass at 50 dp on the saved file. This run has no fresh-context tool of its own, so any new claim stays single-context, unpanelled.
null_test: not needed because every claim would be an explicit configuration checked by a deterministic radius checker against a table value.
lenses: relaxer (795/794/793 + remaining blank-row sweep), evaluator-first (exact largest-hole evaluator: insertion screen over N<=1000 + 9 short rows), archivist (plateau vacancy patterns), swimmer (FIRE squeeze of insertion near-misses), contrarian (Moki&Julio dataset and PR landscape).
