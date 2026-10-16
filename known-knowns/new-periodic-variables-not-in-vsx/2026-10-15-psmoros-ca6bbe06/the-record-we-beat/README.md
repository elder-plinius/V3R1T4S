# Status source snapshot (not the page itself)

This partial win is a calibration gate: there is no record table and no cell to beat. The bank's status source for
the target is the live VSX API.

- URL: https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json
- scout fetch: 2026-10-15T17:42:18Z, HTTP 200, content-type application/json, sha256
  686920557fcf33a7bbdef0642253c51bbc25f80e01c809e8b5adeaf6ef325594 (identical to fetches at 14:08Z and 16:45Z)
- NOVELTY skeptic fetch: 2026-10-15T19:39:25Z, HTTP 200, 4268 bytes, the same sha256
- extracted content: a VSXObjects list of 17 entries in the 0.1-degree test cone (first entry KID 7030792, ROT).
  The API answers; it records no claim of this partial win.
- VSX periods used for the comparison: CDS B/vsx version 2026-10-05 via VizieR (pools saved in how-we-built-it/data).
