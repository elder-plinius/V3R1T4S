# Live MinT Status Snapshot — `(b, T, m, s) = (3, 2, 8, 8)`

## 1. Exact Cell Query Page

- **URL**: `http://mint.sbg.ac.at/query.php?i=x&b=3&s=8&m=8&p=smt&de=2`
- **Fetched (UTC)**: `2026-11-10T18:30:43Z`
- **HTTP Status**: `200 OK`
- **Response Size**: `8336` bytes
- **Page SHA-256**: `5aed6c5b2410094646d736a48515f8241cf76491caeafc8be5a0719482cb9dcf`
- **Database Footer**: `Last update to this application module: 2024-09-05` / `Last update to the database: 2024-09-05`
- **Extracted Constructive & Linear Entry**:
  - Heading: `OOA(3^8, 8, F_3, 2, 8-2) over F_3 — Constructive and linear` (`t = 2`, so constructive linear strength `k = 8 - 2 = 6`)
  - Method text: `Linear OOA(3^8, 8, F_3, 2, 6) (dual of [(8, 2), 8, 7]-NRT-code), using extended algebraic-geometric NRT-code AG_e(2;F,9P) [id=880683] based on function field F/F_3 with g(F) = 2 and N(F) >= 8`
- **Extracted Lower Bound on `t`**:
  - Heading: `OOA(3^8, 8, S_3, 2, 8-1) in Base 3 — Lower bound on t` (`t >= 1`, so maximum possible strength `k <= 8 - 1 = 7`)
  - Bound text: `There is no OOA(3^8, 8, S_3, 2, 8), because the generalized Rao or (dual) Hamming bound shows that M >= 7457 > 3^8 [id=73393]`

## 2. Base-3 Depth-2 Overview Table

- **URL**: `http://mint.sbg.ac.at/table.php?i=x&b=3&col=1&mode=cd&opt=bd&de=2&p=smt&minx=1&maxx=20&miny=0&maxy=15`
- **Fetched (UTC)**: `2026-11-10T18:30:44Z`
- **HTTP Status**: `200 OK`
- **Response Size**: `41568` bytes
- **Page SHA-256**: `f9ed86586695a5a120ca499a43d5bd53e99de174806290b493b3739c05473ef8`
- **Extracted Cell `(m = 8, s = 8)`**: `1 — 2` (lower bound `t = 1`, constructive linear `t = 2`, i.e., `k = 6` vs upper bound `k = 7`).
