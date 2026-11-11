# Honesty gate (kit RUN.md step 7), run folder 2026-10-18-0558

written by the run's main session (Opus 5.5, model claude-opus-5-5) at 2026-10-18T07:25:31Z, after reading all three panel files in full.

status: CONFIRMED_SOLUTION
confirmed_scope: For each n in {14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25}, this folder's row-n object (for n <= 22 the explicit list object/nN_orders.txt.xz, and for n = 23, 24, 25 the full domain D(A_n) of all linear orders on 1..n obeying object/nN_assignment.txt, of exactly counted size with a hash-pinned canonical enumeration) is a Condorcet domain on n alternatives of size 27040, 60956, 135072, 300388, 675512, 1497276, 3336208, 16571072, 36894088, 81912986 and 178950728 respectively, each strictly larger than the n entry of Table 4 of arXiv:2601.07336v1 (27026, 59430, 131536, 292015, 649079, 1432836, 3155366, 15037178, 33162136, 73279872 and 160316046), with the n = 14, 15, 18 and 19 domains being one-alternative restrictions of the n = 15, 16, 19 and 20 domains.

## Panel (three fresh contexts, Agent tool, model opus each)

- **REPRODUCE: pass: true, 11 of 11 rows PASS.**
  - It wrote its own list checker, subset DP and DFS enumerator before opening the claim's tools.
  - It tested them on Fishburn n = 7..25 (the whole Table 4 Fishburn column), brute force and 14 kinds of negatives.
  - It reproduced every size, every sha256 and list = D(A) for the type-L rows. For n = 23..25 it confirmed |D(A)| by an exact DP and by full streamed enumeration (DP = enumeration, stream hashes equal).
  - Every check was run twice with identical results.
- **NOVELTY: pass: true, 11 of 11 rows PASS.**
  - It made no request to arxiv.org or any mirror (the host is stopped).
  - It read the status source through the scout's honest HTTP 200 copy of v1 (2026-10-17T22:25:36Z) and the human's hand check of the abstract page (2026-10-18T00:58Z, v1 only).
  - It searched all 365 repo PRs (titles and bodies), the current TROPHY_CASE.md, GitHub at large, the authors' pages and data, the 2025-2026 Puppe-Slinko book draft, and about 30 web searches. Nothing at or above any of the eleven values exists.
- **CRITERION: pass: true, 11 of 11 rows PASS**, with the confirmed_scope above. It made four rulings:
  - **Never-condition test.** The test is necessary and sufficient in the paper's odd-profile sense: exhaustive on 3 alternatives, and a proof for all n.
  - **Comparison.** Comparing with Table 4's "≥" entries is the right comparison.
  - **Type-A rows.** For n = 23..25, D(A) with an exact count and a hash-pinned canonical enumeration is an explicit set. The paper itself names domains by never conditions, and its own ks bars are not printed lists.
  - **Restrictions.** Rows 14, 15, 18 and 19 are one-alternative restrictions of unpublished rows 15, 16, 19 and 20. They are still per-n wins against what is published, but must not be presented as independent discoveries: the eleven rows come from seven independent objects. Its scope sentence says so.

## Gate checks

- **Hedging.** No panelist hedged its verdict. NOVELTY states openly that a stricter reader could insist on a fresh fetch by the skeptic itself, but its own verdict is clear and reasoned.
  - The gate's judgment: the status source is a fixed arXiv version (v1). Its exact bytes come from one honest HTTP 200 GET made before the block.
  - The human checked by hand at 00:58Z that v1 is still the only version.
  - arXiv announces new submissions and replacements only Sunday to Thursday at 20:00 US Eastern (its help page "Availability of submissions", read through a web search summary; HEURISTIC support). The next possible announcement is 2026-10-19T00:00Z, after this gate.
  - This is the same footing on which the n = 21 gate of runs/2026-10-18-0238 confirmed.
- **Freshness of the table fetch.** The panel's status read (scout fetch 22:25:36Z, hand check 00:58Z) is more than 6 hours old. The kit says to fetch once more. That is impossible without breaking kit rule 5:
  - arxiv.org is stopped after its HTTP 429 at 2026-10-17T22:56:05Z.
  - The session's safety layer refused a one-URL exception for the abstract page, which the charter allowed.
  - No evasion was used, and no process of this run requested arxiv.org.
  - REPORT.md asks the human for a fresh hand check of https://arxiv.org/abs/2601.07336 before any of these packages is submitted.
- **Reproduction.** No mismatch anywhere. Every count and hash agrees across:
  - the three skeptics;
  - this folder's three lenses (strict-audit, count-audit, contrarian);
  - the main session's own tools (code/main_check: mcheck on the xz objects, mdom counts and canonical enumerations, mstream on every stream; code/main_check/verify/, summary in code/main_check/verify_summary.txt).
- **Values.** Every value is strictly better than its table entry. The smallest margin is n = 14 (+14 orders, +0.0518 %), exact.
- **Scope.** The scope is no wider than what was reproduced. CRITERION's sentence covers exactly the eleven rows that passed all three skeptics, and it names the four restriction rows.
- **No overreach.** No capped search is used as an exclusion. No sample is presented as complete: every list was checked in full, and every type-A domain was enumerated in full. No probable prime is involved, and no table value was obtained by evasion.
- **Bundling.** Several objects are bundled in one folder by the human's explicit order (charter Q5, 2026-10-17 21:36 PDT). Each row has its own object, bar and verdict, every row passed every skeptic, and none leans on another for its check. Packaging follows kit/SUBMIT.md, "one object or table cell per package": one package per row.
- **Gate rule.** A CONFIRMED status stands only if python3 repo/kit/check_run.py prints CHECK_RUN: PASS; see REPORT.md.
