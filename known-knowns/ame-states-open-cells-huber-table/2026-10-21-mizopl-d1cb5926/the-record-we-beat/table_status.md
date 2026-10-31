# Primary Status Table & Baselines (`ame-states-open-cells-huber-table`, Part II: `2026-10-21-mizopl-d1cb5926`)

- **Primary Status Table URL**: `https://tp.nt.uni-siegen.de/ame/table.html`
- **UTC Fetch Timestamp**: `2026-10-20T01:10:09Z` (`HTTP/2 200`, `230,252` bytes)
- **Page SHA-256**: `e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`
- **Secondary Status Table URL**: `https://www.codetables.de/QECC/`
- **Secondary UTC Fetch Timestamp**: `2026-10-20T01:10:24Z` (`HTTP/2 200`, `5,136` bytes)
- **Secondary Page SHA-256**: `f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`
- **Status of Newly Solved Open Cells & Pure Graph Upgrades on Live Tables & Literature (`arXiv:2608.05781`, `arXiv:2609.11796`)**:
  - **Live Huber–Wyderka Table (`D <= 10`)**: `(13, 5)`, `(15, 7)`, `(15, 8)`, `(15, 9)`, `(17, 7)`, `(17, 8)`, `(18, 7)`, and `(10, 10)` are all blank (`<td></td>`, absent from the Bokeh `ColumnDataSource` `existing` dictionary).
  - **Markus Grassl's `codetables.de`**:
    - `[[15, 0, 8]]_7` (`q=7, n=15, k=0`) is an **impure product state** ($w_{\text{pure}} = 1$, failing `3,003 / 6,435` seven-party cuts); our pure circulant graph state `AME(15, 7)` in `object/ame_15_7_pure_circulant_certificate.json` ($a = (1, 5, 4, 2, 1, 0, 0) \in \mathbb{F}_7^7$, `0 / 6,435` failed cuts) provides the first pure graph-state certificate.
    - `[[15, 0, 8]]_5` (`q=5, n=15, k=0`) is **impure** ($w_{\text{pure}} = 7$, failing `190 / 6,435` seven-party cuts, with parent `[[17, 1, 9]]_5` having $d_{\text{pure}} = 4 < 8$ as certified in `object/ame_15_5_impurity_and_circulant_nogo_certificate.json`).
    - `codetables.de` stops at $q \le 8$ (or $q = 9$ without $k=0$ graph matrices) and has no tables for $q \in \{10, 11, 13, 16, 17, 19, 289\}$.
  - **Extended $n \le 20, D \le 20$ Grid (`arXiv:2608.05781`, `arXiv:2609.11796`)**: `AME(16, 11)`, `AME(16, 13)`, `AME(18, 16)`, `AME(19, 13)`, `AME(20, 13)`, `AME(20, 16)`, `AME(20, 17)`, and `AME(20, 289)` were all open (`unknown (?)`) prior to our Theorems D21, D22, D25, D26, D27, D27B, D28, D29, and D30.
