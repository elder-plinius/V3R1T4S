Reviewer: NOVELTY skeptic (Claude Opus 5.5, general-purpose subagent)
context: subagent (fresh context, given only claim/)

# NOVELTY review, Claim B: f(3,6) = 13 (partial win p1)

## Status-source fetch (one plain request with curl, no retries)
- URL: https://arxiv.org/abs/2604.08790
- Time: 2026-10-30T04:09:53Z (UTC)
- HTTP status: 200, 39,949 bytes, sha256 0b2c17af0cb7342b68eecf9951a3f011cbf28e31fdb41b3c086f9b58cfd9e3c0
  (the same hash the claimant recorded on 2026-10-27)
- Value: title "Schuttes property for sets of tournaments and an application to dice games". Submission history lists
  **[v1] only** (Thu, 9 Apr 2026 21:58:15 UTC, 143 KB). There is no newer version, so the Figure 7 status recorded in the
  target (f(3,6) <= 13, unstarred) is unchanged. I did not open the PDF myself; the unstarred status comes from the bank
  record and TABLE_RECORD.md.

## Searches run and results
1. Web search "Schütte property sets of tournaments dice games Jeffries f(m,k)": returned the arXiv paper, the Iowa State
   dissertation record (Jeffries 2024), an FAU conference abstract, and older dice/Paley work. None states an exact value
   for f(3,6).
2. Web search "\"2604.08790\"": no relevant results. I found no citing work.
3. Web search "\"Schütte\" tournaments \"every k-subset\" dominated multiple tournaments SAT exact value 2026": only the
   arXiv paper and unrelated older work. No SAT exact value for f(3,6).
4. Web search for f(2,5)/f(3,6), SAT certificate and Jeffries dice: nothing on these cells.
5. Web search for citations of Jeffries' Schütte property with dice: no work citing it.
6. Semantic Scholar citations API for arXiv:2604.08790 (2026-10-30T04:11:00Z): HTTP 429, not read.
   arXiv API search: HTTP 429, not read.
7. OEIS search "Schütte tournament": a single hit, A362137 (single-tournament Paley sizes). It has nothing on sets of
   tournaments.
8. Jeffries' dissertation page (dr.lib.iastate.edu): HTTP 403, not read by me. The claimant reports reading it on
   2026-10-27 and finding the same unstarred values with no certificate. I have not confirmed that.
9. Bank repo TROPHY_CASE.md (GitHub API, current main): no match for schutte, tournament, dice, Jeffries or 2604.08790.
10. Bank repo PRs, `gh pr list --state all --search schutte` (also searched "tournament", "dice" and "f(3,6)"):
    - #694 [bank] (closed, unmerged): the bank entry, no claim on any cell.
    - #816 [claim], OPEN, created 2026-10-29 by another contributor (DmitrL-dev): it claims f(2,5) = 14 only. Under
      "Not claimed" it says, in summary, "Nothing about f(3,6)". It also reports that its encoding for three tournaments
      on 12 vertices was UNSAT according to CaDiCaL, but cake_lpr ran out of memory, so it has no verified certificate
      and no panel review. That is a disclosed, unverified solver outcome that the PR explicitly does not claim. It is a
      sign of independent parallel work, but it is not a claim of f(3,6) = 13 being exact.
    - No other PR or issue mentions f(3,6).

## Judgement
In the sources I could reach, nobody claims f(3,6) = 13 as an exact value, with or without a certificate:
- the status page lists v1 only, and the target records the cell as unstarred;
- I found no citing literature;
- TROPHY_CASE.md has no entry;
- the only related PR (#816) explicitly disclaims f(3,6).
A verified-certificate exact value would therefore strictly improve on the known state (an upper bound only).

Why the answer is still pass: false: two sources I was told to check could not be read here. Jeffries' dissertation
returned 403, and the citation databases (Semantic Scholar, arXiv API) returned 429. I also did not open the paper PDF to
confirm the unstarred mark myself. My instructions say to default to fail unless I can genuinely confirm, so I cannot
confirm novelty in full.

Unlike A, I found no competing claim. Note also that #816 discloses an unverified UNSAT run for the same instance, so
priority on f(3,6) may become contested if #816 later adds a certificate.

novelty: NOT CONFIRMED. No prior or competing claim of f(3,6) = 13 found, but the dissertation (403) and the citation
indexes (429) could not be read, so strict novelty is unconfirmed.

pass: false
