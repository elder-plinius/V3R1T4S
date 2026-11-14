# The record we beat

Cell: MINLPLib instance `pricing050` (maximisation of objvar). Partial win p1 compares a rigorous dual upper bound against the recorded best primal plus a 1e-6 relative tolerance; the public dual columns are the published comparison points.

| source | URL | fetched (UTC) | HTTP | sha256 of the response | extracted |
|---|---|---|---|---|---|
| MINLPLib solu (status_source) | https://www.minlplib.org/minlplib.solu | 2026-11-05T19:50:42Z | 200 | df6732aac604d022f294a56b7597de52bd29da5b9db2b39087fed233ffbbac34 | =best= pricing050 -1813.8290780000 ; =bestdual= pricing050 -1153.0032810000 |
| instance page | https://www.minlplib.org/pricing050.html | 2026-11-05T19:50:45Z | 200 | f4e23f86d9237a6749c7801a87e28d86b3dbf22a381459e7ff1a64ce54d59fb3 | primal p1 -1813.829078 ; duals ANTIGONE -1153.003281, BARON -1036.050749, GUROBI -1438.459272, LINDO -1135.107611, SCIP -1534.3281 |

Selected headers were not retained for the 19:50Z panel fetches (User-Agent `V3R1T4S-research (curl)`, one try each, no retries). The same two files were also fetched earlier in the run:

| source | fetched (UTC) | HTTP | sha256 |
|---|---|---|---|
| minlplib.solu | 2026-11-03T19:44:01Z | 200 | df6732aac604d022f294a56b7597de52bd29da5b9db2b39087fed233ffbbac34 (byte-identical) |
| pricing050.html | 2026-11-03T19:44:04Z | 200 | f4e23f86d9237a6749c7801a87e28d86b3dbf22a381459e7ff1a64ce54d59fb3 (byte-identical) |
| minlplib.solu (re-fetch) | 2026-11-05T19:48:34Z | 200 | df6732aac604d022f294a56b7597de52bd29da5b9db2b39087fed233ffbbac34 (byte-identical) |

Partial-win bar used in the certificate: -1813.829078 + 1e-6 * 1813.829078 = -1813.827264170922. Claimed rigorous U = -1813.829075713452 (strictly below every listed solver dual and the solu bestdual, and within the bar of the best primal).
