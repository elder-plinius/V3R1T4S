# Self-break summary (before the panel)

Run 2026-10-28 (main session, not a fresh context); the fresh-context checks of record are panel/.
- Two independent checkers written from the definition (the package's check_scheme.py and an independently written
  integer checker): all 7,452,900 Brent equations, 0 wrong; 1644 terms, none with a zero factor, no duplicates, no two
  terms proportional, no pair sharing two factors up to scale. Both checkers pass the merged 1645 (known positive).
- Planted mutants (a dropped term, a duplicated term, coefficients +1 in u and w, a moved v entry) fail all three
  checkers (15 of 15 runs), the Brent checkers by violated equations, not by a parse error.
- Rebuild from LITA's upstream file (sha256 and git blob sha1 match the live LITA tree): byte-identical u, v, w.
- Literal criterion: max dimension 15 <= 16; sorted (13,14,15) not excluded; 1644 < 1681, the minimum of the four live
  sources, and < 1645, the merged value; exact over Q; equal to no listed value, so the composition clause does not
  apply.
- Table access: one curl GET per URL with a User-Agent naming V3R1T4S; no cookies, no browser imitation, no retries;
  no HTTP 401/403/429/503 in this run.
Verdict: SURVIVES.
