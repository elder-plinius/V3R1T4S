# Self-break summary (run of 2026-10-26, main session, before the panel)

Not a fresh context; the fresh-context checks are panel/.
- An independent checker written from the definition (exact integers, all 9,922,500 Brent equations): 0 wrong; 1836
  terms, none with a zero factor, no duplicates. It passes the merged <14,15,15> rank-1842 scheme of this repository
  (known positive) and fails 5 planted mutants (dropped term, duplicated term, one u and one w coefficient +1, one v
  entry moved); the package's two checkers also fail all 5 mutants.
- Rebuild from LITA's upstream file (sha256 and git blob sha1 match the LITA tree): byte-identical u, v, w.
- Literal criterion: max dimension 15 <= 16; sorted (14,15,15) not excluded; 1836 < 1848, the minimum of the four live
  sources; exact over Q; not equal to any listed composition value.
- Table access: one curl GET per URL with a User-Agent naming V3R1T4S; no retries, cookies or browser imitation.
- Disclosed: open pull request #752 (same contributor, 2026-10-25T11:18:58Z) names this scheme as an unclaimed
  intermediate and ships the code that rebuilds it.
Verdict: SURVIVES.
