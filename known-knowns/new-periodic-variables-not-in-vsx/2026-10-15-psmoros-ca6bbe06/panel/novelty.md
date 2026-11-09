<!-- provenance: saved verbatim by the run's main session (Opus 5.5) from the NOVELTY skeptic subagent's returned final message (text between its BEGIN/END PANEL markers), 2026-10-15 ~19:49Z; subagents cannot write report-like files. -->
# panel/novelty.md: NOVELTY skeptic

context: subagent (Agent tool), model opus, fresh context seeing only claim/
inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/results/decide_output.txt, claim/results/far.txt,
claim/results/null_test.md, claim/results/variables.csv (columns only, plus counts), claim/prereg/PREREG_run1739.md
(wording only); the repo files bank/targets.json (entry new-periodic-variables-not-in-vsx), TROPHY_CASE.md and
kit/RULES.md. No other run folders were read.
review written: 2026-10-15T19:44:49Z (date -u)

## Claim under review
Bank target new-periodic-variables-not-in-vsx; claimed partial win `vsx-reproduce-known` (the bank calls this a
"calibration gate"). The claim (claim/CLAIM.md) says a frozen pipeline blindly recovered the VSX period of 77 of 80
randomly drawn VSX EW/EA/RRAB/DSCT stars with ZTF light curves, and reports a false-alarm rate of 0/400 at T = 54.0
(0/67 VSX CST stars, 0/333 Gaia DR3 non-variables). The full bank success criterion (new variables) is explicitly
NOT claimed.

## 1. Status source (one plain GET, honest User-Agent "V3R1T4S-run (research; honest client)", no retries)
- URL: https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json
- time: 2026-10-15T19:39:25Z (date -u, before and after the request)
- curl output: `http_code=200 size=4268 content_type=application/json`
- sha256 of the response: 686920557fcf33a7bbdef0642253c51bbc25f80e01c809e8b5adeaf6ef325594. This is identical to
  claim/data/vsx_status.json and to the hash quoted in claim/CLAIM.md (scout fetch 2026-10-15T17:42:18Z).
- What it shows: a JSON `VSXObjects.VSXObject` list of 17 VSX entries in the 0.1-degree cone, for example
  "V0816 Lyr", AUID 000-BQM-875, type EW, Period 0.346964, RA 291.09087, Dec 42.49928, and several "KIC ..."/"KID ..."
  ROT entries plus "Gaia DR3 ..." E/ROT/DSCT|GDOR|SXPHE entries. So the live VSX API answers. [KNOWN]
- Meaning for novelty: the target is a harvest with no "solved" state (bank entry: kind "harvest", status_checked
  2026-10-08). The status page is a liveness check of the reference catalogue. It neither records nor rules out
  any claim of this partial win, so it cannot make the claim "not new". It was read successfully, so this is not
  `PENDING STATUS CHECK`.

## 2. This repository: TROPHY_CASE.md and open pull requests
- Local TROPHY_CASE.md (repo HEAD 41ff532b74be742afa614fa057fd5c10cee0f3e6, sha256
  d78887f8bede24556974550b57a55d7fcbb0b8480dc88ec0d50cd97fccfa7ca6): `grep -i -E "vsx|variable|ZTF|periodic|
  calibration|vsx-reproduce"` returns no lines. Its families are degree-diameter graphs, Lehmer, matrix
  multiplication, VNN-COMP, RobustBench, constant-weight codes and cipher commitments. There is no variable-star
  entry. [KNOWN]
- GitHub main copy, one GET at 2026-10-15T19:43:45Z:
  https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md -> `http_code=200 size=30936`,
  sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. This differs from the local copy, but
  `grep -c -i -E "vsx|ztf|variable star|periodic variable"` gives 0 there too. [KNOWN]
- Open pull requests, one GET at 2026-10-15T19:39:33Z:
  https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 -> `http_code=200 size=168139`,
  sha256 c38af6f9d8c0c3617c4b166f376cc8e4b79dec7c3ded0c20bcb8f1eadb4af2fc. There are 9 open PRs: #194, #191 and #190
  (stable-marriage claims), #193 (qoblib portfolio), #192 (Angel-Holmes conjecture), #154 and #153 (bank entries),
  #30 and #9 (harness fixes). Searching titles and bodies for "vsx", "variable star", "ZTF", "periodic variable",
  "new-periodic-variables" and "vsx-reproduce-known" finds 0 hits in all 9. [KNOWN]
- Conclusion: neither the trophy case nor the open PRs hold an existing claim of `vsx-reproduce-known` or of this
  target. This claim would be the first. It is not a tie with an existing claim.
- Limit: closed or merged PRs were not queried separately. Anything merged would appear in TROPHY_CASE.md on main,
  which was checked.

## 3. Literature, last 24 months (2024-10 to 2026-10), plus the older baseline
Searches: arXiv API (export.arxiv.org, one GET each, all HTTP 200, 2026-10-15T19:41:06Z to 19:44:10Z) for abstract
queries "ZTF AND VSX" (4 papers in total), "ZTF AND periodic variable" (31 in total, 19 since 2024-10-01) and
"ZTF AND period AND (recovery OR recovered OR completeness)" (28 in total, 16 since 2024-10-01). I also ran six web
searches on ZTF/VSX period-recovery calibration, false-alarm rates on constant stars, SCoPe, and Rubin DP1.
- None of the 2024-10 to 2026-10 hits publishes a blind VSX-period recovery plus a constant-star false-alarm
  calibration of a ZTF period pipeline. The closest recent items, read from their arXiv abstracts:
  - arXiv:2605.02216 (ZTF ultracool dwarfs): 20 of its 32 robust periods have literature counterparts, "most of
    which are consistent".
  - arXiv:2512.13395 (ZTF DR17 CNN classifier): about 99% accuracy, but it measures classification, not
    period-recovery calibration.
  - arXiv:2509.15133 (Gaia DR3 white dwarfs with ZTF DR23 Lomb-Scargle).
  - arXiv:2504.08045 (ZTF IC 10 catalog), which verifies its classification against earlier catalogs.
  - arXiv:2605.00344 (Rubin DP1 RR Lyrae cross-matched with VSX; no period-recovery rate in the abstract).
  [KNOWN, from abstracts opened]
- Older than 24 months, and the real baseline: Chen et al. 2020 (arXiv:2005.08662, ApJS 249, 18; abstract opened)
  classify 781,602 ZTF DR2 periodic variables and report "typical misclassification rate and period accuracy ...
  on the order of 2% and 99%" against previously published catalogs. The ZTF Source Classification Project III
  (arXiv:2312.00143, 2023) runs Lomb-Scargle, conditional-entropy and AOV period finders over ZTF at scale. Recovering
  known periods of EW/EA/RRAB/DSCT stars from ZTF light curves is therefore established practice and is not new
  science. [KNOWN]
- Inside the claim itself, per claim/results/variables.csv (80 scored rows):
  - 73 of the 80 scored stars have a Chen+2020 match within 3".
  - For 71 of the 80, the VSX period agrees with the Chen+2020 ZTF period (column vsx_eq_chen).
  - Only 7 of the 77 recovered stars have a VSX period that does not agree with Chen+2020.
  - claim/results/decide_output.txt gives the provenance split: ZTF-named 62/63, other names 15/17.
  - 66 of the 77 recoveries are at P_rec/P_vsx = 0.5, which the bank criterion allows as a 2x alias.
  So most of the "known" periods were already derived from ZTF data by Chen+2020. [NUMERICAL, my tabulation of
  claim/results/variables.csv]

## 4. How I judged "novel" for a calibration-gate partial win
The kit's novelty test ("strictly beats everything known; a tie is not a record") is written for records. The bank
defines `vsx-reproduce-known` as a threshold gate, not a ranking: at least 50 blind VSX-period recoveries plus a
reported false-alarm rate on at least 50 constant/non-variable stars, saved as a table. By construction it
reproduces known periods, so its astrophysical content can never be new. Read literally against the literature,
it would fail every time, which would make the bank's own partial win impossible to award. I therefore judged
novelty on three tests:
1. **No duplicate claim in this repository.** The partial win must not already be claimed in TROPHY_CASE.md or an
   open PR; a second claim would be a tie, which is not a record. Result: no prior claim (section 2). PASS.
2. **No scope inflation.** The claim must not assert scientific novelty: no "new variable", "first", "record" or
   "discovery", and it must not present the full criterion as met. Result: claim/CLAIM.md calls itself the partial
   win, says the full criterion "is NOT claimed", and a grep of CLAIM.md, REPRODUCE.md, prereg/ and the
   results/*.md/*.txt files finds no first/novel/record/breakthrough/discover wording applied to the result. PASS.
3. **No published result makes the deliverable a duplicate.** Published calibrations (Chen+2020, SCoPe) belong to
   other pipelines. A calibration gate is specific to its pipeline, so they make the result unremarkable as science,
   not a duplicate of this deliverable. No last-24-month publication was found that calibrates this pipeline or
   publishes this table. PASS, with the explicit statement that the science is KNOWN.

The requirement to strictly beat everything known is met only in the bank sense: there is no existing claim of this
partial win in the repo. In the scientific sense it does not beat Chen+2020, and it must never be described as if it
did.

## Caveats (for the other skeptics and for any wording downstream)
- Any public wording must say "calibration gate reproduced known VSX periods". It must not say "new", "first" or
  "record". [HEURISTIC]
- Truth independence is weak: for 71 of 80 stars the VSX "truth" period agrees with Chen+2020's ZTF-derived period
  (vsx_eq_chen), and only about 7 of the 77 recovered periods are independent of Chen+2020. The gate largely shows
  that this pipeline reproduces Chen+2020-style ZTF periods from later ZTF data. Whether that satisfies "blind" and
  "VSX period" is for the CRITERION skeptic; it does not change the novelty verdict. [NUMERICAL]
- Limits of this check: the literature search used arXiv abstract queries and web search, not ADS full text, so a
  full-text-only calibration could be missed. Under test 3 that would not change the verdict. Only open PRs were
  queried (one GET), and merged work was checked through TROPHY_CASE.md on main. [HEURISTIC]

## Credit
Chen et al. 2020 (ZTF periodic variables, arXiv:2005.08662); ZTF Source Classification Project III
(arXiv:2312.00143); VSX/AAVSO (Watson, Henden & Price 2006); ZTF (Bellm et al. 2019; Masci et al. 2019) via SNAD
(Malanchev et al. 2023), as credited in claim/CLAIM.md.

novelty: PASS as a calibration-gate partial win (first claim of vsx-reproduce-known for this target in this
repository; status source live, HTTP 200 at 2026-10-15T19:39:25Z). The astrophysical content is KNOWN and is not
claimed as new.
pass: true
