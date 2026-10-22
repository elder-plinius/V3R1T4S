# Primary Status Table & Baselines (`ame-states-open-cells-huber-table`)

- **Primary Status Table URL**: `https://tp.nt.uni-siegen.de/ame/table.html`
- **UTC Fetch Timestamp**: `2026-10-20T01:10:09Z` (`HTTP/2 200`, `230,252` bytes)
- **Page SHA-256**: `e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`
- **Status of `(n=9, D=10)` and `(n=11, D=10)` on Live Table**: Both cells are blank (`<td></td>`, absent from the Bokeh `ColumnDataSource` `existing` dictionary).
- **Status on Markus Grassl's `codetables.de`**:
  - `https://www.codetables.de/QECC/` (`2026-10-20T01:10:24Z`, `HTTP/2 200`, `5,136` bytes, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`): covers only prime-power local dimensions $q \in \{2, 3, 4, 5, 7, 8, 9\}$, with no tables for composite dimension $D = 10$.
  - `https://www.codetables.de/QECC.php?q=25&n=11&k=1` (`2026-10-20T01:10:55Z`, `HTTP/2 200`, `2,169` bytes, `sha256: d5ac9540c97cf840b131f9f225d8ff1f946bb510410faf818f40ca7ff68b0aed`): lists only lower bound $d = 5$ (`5 - 6`) for `[[11, 1, d]]_5`, which our explicit pure `[[11, 1, 6]]_5` quantum MDS code strictly improves to $d = 6$.
