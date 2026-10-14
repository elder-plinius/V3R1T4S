# Primary table receipt

KNOWN: URL: https://aeb.win.tue.nl/codes/Andw.html

- Client: Python urllib default, one request, no retries, no separate web open.
- Fetch start UTC: `2026-10-14T02:50:17.281821+00:00`; completed UTC: `2026-10-14T02:50:22.728485+00:00`.
- HTTP: `200`; Content-Type: `text/html`.
- Last-Modified: `Sat, 10 Oct 2026 11:57:45 GMT`.
- Response bytes: `127021`.
- SHA256: `0f1b51bf71c0ca91aef82eef740cb0dd9f6be6c4014983213d0eefe0eb631cee`.
- Parsed target: n=27, d=6, w=10; lower `12987`, upper `43529`; printed annotation `g` means specified automorphism group.
- Claim `13026` exceeds lower by `39` and is below upper.

PROVED-HERE: Bitwise complementation preserves distances and exchanges weight 10 with weight 17 at length 27, so A(27,6,10)=A(27,6,17). The distance-6 table has weight columns 4 through 14 and the length-27 row stops at weight 13. There is no separate weight-17 cell to contradict the canonical representative. This is a mathematical symmetry check, not a claim to have fetched a nonexistent mirror cell.

Raw response and complete headers are retained locally as `evidence/Andw.html` and `evidence/table_meta.json`. Published receipt is this file. Reanalysis: `python3 analyze_table.py` with the recorded inputs available; do not rerun `fetch_once.py` for this review.
