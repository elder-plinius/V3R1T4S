context: subagent

role: NOVELTY
claim: pricing050 partial win p1 — Lagrangian dual upper bound U on max objvar from object/lambda.txt + object/cert_arb_leaves.json

## Status source (live, one plain curl each, UA V3R1T4S-research (curl), no retries)

status_source URL: https://www.minlplib.org/minlplib.solu
instance page URL: https://www.minlplib.org/pricing050.html

Fetch times (UTC from command clock):
- minlplib.solu: start 2026-11-05T19:50:42Z, done 2026-11-05T19:50:45Z, HTTP=200
- pricing050.html: start 2026-11-05T19:50:45Z, done 2026-11-05T19:50:47Z, HTTP=200

sha256 (command output):
df6732aac604d022f294a56b7597de52bd29da5b9db2b39087fed233ffbbac34  minlplib.solu
f4e23f86d9237a6749c7801a87e28d86b3dbf22a381459e7ff1a64ce54d59fb3  pricing050.html
Identical to packaged status/ copies.

Decisive solu lines:
=best=     pricing050                                   -1813.8290780000
=bestdual= pricing050                                   -1153.0032810000

Decisive dual-bound numbers from pricing050.html (Dual Bounds block, last updated 31 Jul 2025):
-1153.003281 (ANTIGONE); -1036.050749 (BARON); -1438.459272 (GUROBI); -1135.107611 (LINDO); -1534.3281 (SCIP)
Primal: -1813.829078 (p1)

Best displayed solver dual for this maximisation cell: SCIP -1534.3281
solu =bestdual= (third-best rule): -1153.0032810000

## Claimed object (from claim package; numbers from command output)

object/lambda.txt:
e2 0
e3 0
e4 0
e5 3.04890112
e6 2.16775096

object/cert_arb_leaves.json fields:
nleaves 1958
LB_lower 1813.82907571345236477629709126
=> claimed rigorous upper bound U = -LB_lower = -1813.82907571345236477629709126
(CLAIM.md states the same U to the printed digits.)

mpmath comparison (dps 50) decisive lines:
claimed -1813.82907571345236477629709126
primal -1813.829078
claimed - primal 0.00000228654763522370290874
partial_win_bar -1813.827264170922
claimed<=bar True
claimed < scip True
claimed < bestdual True

## V3R1T4S repo (public web)

TROPHY_CASE.md (raw main, HTTP=200): no minlplib / pricing050 / finance-open rows (rg match count 0).
known-knowns/ directory listing (API, HTTP=200): no folder whose name contains minlp, pricing, finance, or saa.
Releases API: nreleases 0.
Open/closed pulls (API, 100 each) and issue search q=pricing050 repo:elder-plinius/V3R1T4S:
only #680 [bank] minlplib-finance-open-instances (closed, not merged) — bank proposal only; no solution/certificate PR.
Commit search q=pricing050 repo:elder-plinius/V3R1T4S: total_count 0.
bank/targets.json still lists minlplib-finance-open-instances as an open target; partial win p1 is exactly this certificate style. Bank text: "A solver status line is not a certificate."

## Literature / code (last ~24 months window; blocked endpoints not retried)

Recorded blocks (one try each):
- api.semanticscholar.org paper search: HTTP=429
- export.arxiv.org (several queries): HTTP=500, empty body
- api.github.com/search/code: HTTP=401
- link.springer.com Davarnia DOI landing: HTTP=301 (not followed)

Successful searches:
- OpenAlex works search "pricing050" / "pricing050 MINLPLib" / "Kiaghadi Davarnia pricing": count 0
- Crossref query=pricing050 MINLPLib: only Bussieck et al. 2003 MINLPLib paper
- Zenodo q=pricing050: total 0
- GitHub repo search pricing050 MINLPLib: total_count 0
- DuckDuckGo html q="pricing050": hits MINLPLib page; SECQUOIA agent-swarm-research experiment note; a fork known-unknowns page that still treats saa_2/pricing050 as open bank targets

Source papers (Davarnia / van Hoeve outer-approximation via decision diagrams, Math. Prog. 2021; instance credited on MINLPLib authors page) are the model origin, not a published dual closing this cell. No OpenAlex/Crossref hit in-window reporting a dual at the primal for pricing050.

## Neighbouring / other published duals for the same instance

Only pricing050 appears under "pricing" in live minlplib.solu (no sibling pricing0xx rows).
saa_2 is the other instance in the same bank target (minimise); different cell.

Nearest non-MINLPLib published dual number found: SECQUOIA/agent-swarm-research minlp-notes results JSONL (Date 2026-09-21; public raw files HTTP=200), SCIP hybrid envelopes run:
instance pricing050 mode hybrid status optimal nodes 1
dual -1813.8276337139228
primal -1813.8276337139228
(v3 jsonl time 17.090843439102173; same dual in v2)

mpmath decisive lines vs that published dual:
secquoia_hybrid -1813.8276337139228
claimed < sec (tighter)? True
sec - claimed 0.00144199952956477629709126

Native/split SECQUOIA duals are weaker (-1504.18 / -1626.21). MINLPLib page still shows SCIP -1534.3281.

Interpretation: for maximisation, a better dual upper bound is a strictly smaller number. Claimed U beats every MINLPLib dual and the SECQUOIA hybrid dual. SECQUOIA is a solver status/log dual (gap tol 1e-4 in their setup), not a machine-checkable independent certificate; even as a published dual value it is strictly weaker than claimed U. Claimed object (multipliers + arb leaf log) is not a trivial edit, restriction, relabelling, or local polish of that solver run or of the MINLPLib duals.

## Novelty conclusion

Cell = best dual on the MINLPLib instance page / =bestdual= in minlplib.solu, plus any published certificate or optimality dual for pricing050.
Claimed U = -1813.82907571345236477629709126 strictly improves on SCIP -1534.3281, on =bestdual= -1153.003281, and on the tightest other public dual found (SECQUOIA hybrid -1813.8276337139228). No TROPHY_CASE / known-knowns / PR / release prior art for this cell. Not a tie.

injection_suspected: none

pass: true
