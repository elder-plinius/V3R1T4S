# Honesty gate — run 2026-11-07-1158, claim (b, p) = (24766, 1000747824697), partial win p1

status: CONFIRMED_PARTIAL
confirmed_scope: Against the p1 text as quoted in claim.md, the pair (b, p) = (24766, 1000747824697) has 10125 < b < 65537, b = 2*7*29*61 not a perfect power, p > 10^12 proven prime (full trial division and a Lucas certificate) and not dividing b, and 24766^(p-1) == 1 (mod p^2) by exact integer arithmetic, while neither claim/inputs copy of FermQ_Sorg.txt or FermQ_Sort.txt (hashes as recorded, not re-fetched) has a row for 24766 or contains p, and one OEIS search at 2026-11-07T12:24:27Z returned HTTP 200 with no match, so the object meets partial win p1 and not the full win (b > 10125); novelty against any other source, a live re-fetch of the tables and whether the quoted criterion matches the bank file are not established.

partial_win: p1
panel: reproduce.md pass: true · novelty.md pass: true · criterion.md pass: true (three delegate_task subagents, each
given only claim/)

## Gate reading (main session, RUN.md step 7; the status may only go down)
- No downgrade trigger found. No panelist hedged its verdict. No reproduction mismatch: three independent primality
  proofs and six exact congruence computations agree with verify.py. The claim is one object. Primality is proven,
  not probable. No capped search is used as an exclusion. No benchmark baseline applies.
- Table access was honest: every fetch in the run and in panel/work-* used a User-Agent naming V3R1T4S, with no
  retries. The only grep hits for "cookie" or "retry" are inside fetched GitHub PR bodies (other people's text), not in
  any request. The panel's table fetch (NOVELTY, 2026-11-07T12:18:47Z) is under 6 hours old, so no extra fetch was
  needed.
- The confirmed_scope above is the CRITERION panelist's sentence, exactly. Two of the items it leaves open are closed
  elsewhere, without widening the scope. The live re-fetch was done by NOVELTY (2026-11-07T12:18:47Z, HTTP 200,
  byte-identical to the scout's copies). The quoted p1 text matches bank/targets.json verbatim (main-session string
  comparison).
- Disclosures: the REPRODUCE context reports that it loaded the general procedure notes of the Hermes v3r1t4s skill
  (no run notes, reports or quarry state). novelty.md shows one search URL partly masked (`100****4697`) by a
  redaction filter; the masking is cosmetic and its finding (total_count 0) is unaffected. Panel files are kept
  exactly as written.
