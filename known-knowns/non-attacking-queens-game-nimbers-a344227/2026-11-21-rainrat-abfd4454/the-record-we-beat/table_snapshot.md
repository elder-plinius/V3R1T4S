# Status and Table Snapshot (`the-record-we-beat/table_snapshot.md`)

## 1. OEIS A344227 Status Snapshot

- **URL (HTML)**: `https://oeis.org/A344227`
  - **UTC fetch time**: `2026-11-21T16:54:05Z`
  - **HTTP status**: `200`
  - **Selected headers**: `content-type: text/html; charset=utf-8`
  - **SHA-256 of raw page**: `d9877453e873ffcc6ddec087efe808ad0015029abed52cb6bfa4616b0589e124`
- **URL (JSON)**: `https://oeis.org/search?q=id:A344227&fmt=json`
  - **UTC fetch time**: `2026-11-21T16:54:04Z`
  - **HTTP status**: `200`
  - **Selected headers**: `content-type: application/json; charset=utf-8`
  - **SHA-256 of raw page**: `169b3ba6ae35fc2ec36f8ae818d7cd5d4df7f64c5d388c2d4bf283fbc42451d5`
- **Extracted cell / content compared against**:
  - Sequence data `a(0)..a(17)`: `0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0, 2` (revision 72, dated August 23, 2026).
  - Notes that on a vertex-transitive board (such as the toroidal queens graph $TQ_n$), the nimber is $0$ or $1$, without listing any values of $G(TQ_n)$ or central-strike refutation margins $R_n$.

## 2. Primary Paper & Repository Snapshot (Rudd 2026)

- **URL (Paper)**: `https://raw.githubusercontent.com/rudd-work/queens-nimbers/main/paper/queens-n18-paper.md`
  - **UTC fetch time**: `2026-11-21T16:54:23Z`
  - **HTTP status**: `200`
  - **Selected headers**: `content-type: text/plain; charset=utf-8`
  - **SHA-256 of raw page**: `d2f189d1136e7b23e32a61d02e7f30ca6bb90ac8d676e06b55e381658fecc9a2`
- **URL (Conjecture Theory)**: `https://raw.githubusercontent.com/rudd-work/queens-nimbers/main/docs/conjecture-theory.md`
  - **UTC fetch time**: `2026-11-21T16:54:44Z`
  - **HTTP status**: `200`
  - **SHA-256 of raw page**: `e24efb2b64f4ccd5fa2b41c0341f381c5dee6580e2171b5a6dceb918bdc90ffe`
- **URL (Verification Results)**: `https://raw.githubusercontent.com/rudd-work/queens-nimbers/main/verification/RESULTS.md`
  - **UTC fetch time**: `2026-11-21T16:54:45Z`
  - **HTTP status**: `200`
  - **SHA-256 of raw page**: `a0e5b15875b6a1ddf14e547a357919feb542f1a1b8f40526bf71e653058f2bd1`
- **URL (Winning Geometry / Refutation Margins)**: `https://raw.githubusercontent.com/rudd-work/othello-solved/main/docs/cgt-winning-geometry-n20.md`
  - **UTC fetch time**: `2026-11-21T16:55:20Z`
  - **HTTP status**: `200`
  - **SHA-256 of raw page**: `13fab18457896bdc772c0dad9557308d52e12a3df80b2f697062085afcbcb7a4`
- **Extracted cells compared against**:
  1. **Section 6.7 (Toroidal Queens $G(TQ_n)$ and Conjecture T1)**: Reports $G(TQ_n)$ only for $n = 1 \dots 10$: `(1, 1, 1, 0, 1, 0, 1, 0, 1, 0)`, and states Conjecture T1 ($G(TQ_n) = n \bmod 2$ for $n \ge 4$). All values $n \ge 11$ were uncomputed.
  2. **Section 6.6 (Central-Strike Refutation Margins on $R_n = Q_n \setminus N[c^*]$)**: Reports margins for $n = 8$ (`0/36`), $n = 10$ (`8/64`), $n = 12$ (`100/100`), and $n = 18$ (`0/256`). It explicitly leaves $n = 14$ and $n = 16$ open.
