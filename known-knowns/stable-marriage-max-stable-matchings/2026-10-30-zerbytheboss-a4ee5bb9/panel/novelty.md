context: subagent

Novelty evaluation against live status sources, literature, and merged repository records:

1. Live Status Source:
   - URL: `https://oeis.org/A357271`
   - Fetched: 2026-10-30T06:23:50Z
   - HTTP status: 200 OK
   - SHA-256: `fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143`
   - Data line for n = 17: lists lower bound `a(17) = 200,832`.

2. Ong et al. (IFoRE 2024 / OEIS 2025) linked file `a357271_1.txt`:
   - Contains improved instances only for odd n up to 15 (n=7: 81, n=9: 365, n=11: 1690, n=13: 7123, n=15: 27059).
   - Contains no entry for n = 17.

3. Repository Merged Records (`known-knowns/stable-marriage-max-stable-matchings/`):
   - `2026-10-14-r-nikhil-ec9b2daf`: n = 13 (7,698)
   - `2026-10-14-r-nikhil-3a7359d3`: n = 15 (30,362)
   - No package or merged record exists for n = 17.

4. Composition Closure Bar:
   - Since 17 is a prime integer, no non-trivial factors n1, n2 > 1 exist such that n1 * n2 = 17.
   - Therefore, no lexicographic composition of smaller known instances (e.g. products with K2, K3, K4, etc.) can be formed for n = 17.
   - The composition closure record at verification time is strictly 200,832.

5. Comparison:
   - Candidate instance stable matching count: 206,728.
   - Previous record: 200,832.
   - Margin: +5,896 stable matchings (+2.93% improvement).
   - The result strictly exceeds all prior published and composed records.

pass: true
