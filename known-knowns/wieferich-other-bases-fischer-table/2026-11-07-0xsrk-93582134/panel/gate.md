# Honesty gate: run 2026-11-07-2319, claim (b, p) = (36260, 1026120862861), partial win p1

status: CONFIRMED_PARTIAL
confirmed_scope: The pair in object/pair.json (b = 36260, not a perfect power, strictly between 10125 and 65537; p = 1026120862861, proven prime and above 1e12) satisfies 36260^(p-1) == 1 mod p^2 in exact integer arithmetic, and neither p nor a row for base 36260 appears in the Fischer files or the OEIS search recorded in the-record-we-beat/RECORD.md, which meets partial win p1 only (not the full win, and not a beyond-searched-limit result, since those tables give no row or limit for base 36260).

partial_win: p1
panel: reproduce.md pass: true · novelty.md pass: true · criterion.md pass: true. Three isolated headless Claude Code
sessions (`claude -p --safe-mode`), each started in its own copy of claim/ outside the workspace, launched in
parallel at 2026-11-07T23:25:48Z-23:25:54Z.

## Order and isolation
- PREREG.md was frozen at 23:20:27Z.
- PREREG.v2.md (23:24:21Z) changed only the frontier-archivist lens: no sweep on battery power. That change came
  before claim/ existed and before any sweep.
- claim/ was built at 23:25Z, and no claim/ file is older than the freeze
  (attempts/skeptic-settled/output/claim_order_and_quote_check.txt).
- Every skeptic's init event shows 7 tools, 0 MCP servers, permission mode dontAsk and Opus 5.5. The session ids are
  in attempts/skeptic-settled/output/panel_run_*.txt.
- `collect` found each claim/ copy unchanged and no path outside a skeptic's own folder.
- Refused calls: REPRODUCE 0, CRITERION 0, NOVELTY 5. NOVELTY's five were one `gh issue list` and four `mv`
  renames of its own scratch files. The workspace denials block both, and neither made a network request
  (attempts/skeptic-settled/output/panel_refusals_novelty.txt).
- Run times and costs: REPRODUCE 270 s, $1.03; CRITERION 373 s, $1.30; NOVELTY 680 s, $3.19.

## Gate reading (main session, RUN.md step 7; the status may only go down)
- **No downgrade trigger found.**
  - No skeptic hedged its verdict, and there is no reproduction mismatch.
  - REPRODUCE disclosed that its own checker's first run printed FAIL. The cause was its coverage assertion:
    isqrt(p) = 1012976 is even, so the last needed divisor is 1012975, and no factor had been found. It fixed the
    assertion, added an independent divide-by-every-integer route, and all later runs pass. This was a fault in its
    tool, not in the claim.
  - REPRODUCE leaves OEIS to the skeptics who fetch, by role.
  - p is proven prime by full trial division (REPRODUCE, CRITERION). Lucas certificates on
    p - 1 = 2^2·3·5·17102014381, with witness 6, come from CRITERION and from NOVELTY's sanity check.
  - The congruence holds by several exact routes, plus the additivity identity
    2q(2) + q(5) + 2q(7) + q(37) ≡ 0 (mod p). claim/verify.py agrees.
  - The claim is one object; primality is proven, not probable; no capped search is used as an exclusion; and no
    benchmark baseline applies.
- **CRITERION's scope note, read and accepted:** for a base above 10125, the clause "absent from both Fischer
  tables" is vacuous for the base row, since no table has a row or limit there. Its content is that p appears in no
  Fischer file and in no OEIS search. The scope sentence therefore claims p1 only, and not a beyond-limit result.
  CRITERION also notes that 3 is a smaller Wieferich prime to base 36260.
- **Table access was honest.** Every fetch used the User-Agent naming V3R1T4S, with one request per source, no
  retries, and no blocked or challenge page.
- **The panel's fetches are under 6 hours old and byte-identical to the scout's of 23:19:19Z-21Z.**
  - NOVELTY: FermQ_Sorg.txt at 23:26:16Z, FermQ_Sort.txt at 23:26:24Z, and the first-bases files at 23:26:32Z and
    23:26:39Z.
  - CRITERION: FermQ_Sorg.txt at 23:29:42Z, FermQ_Sort.txt at 23:29:44Z, and OEIS at 23:29:46Z.
- **The quoted criterion texts match the pinned bank verbatim** (main-session check in
  attempts/skeptic-settled/output/claim_order_and_quote_check.txt).
- **confirmed_scope** above is the CRITERION panelist's sentence, exactly. It names the package's own files
  (object/pair.json, the-record-we-beat/RECORD.md).
- **Priority: no earlier public mention.**
  - NOVELTY fetched the full file patches of the four Wieferich pull requests. Their only "unclaimed" mentions
    concern a different pair, (28860, 1017279755641).
  - Its PR, issue and code searches found nothing.
  - No submitted or packaged file names this pair (main-session check of outbox/).
- The panel files are copied into the package exactly as written.
