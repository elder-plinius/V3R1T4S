role: NOVELTY skeptic (panel v3)
context: fresh subagent, started by the parent session with PANEL_BRIEFS_v3.md (header + NOVELTY section) and kit/RULES.md only; worked on a copy of claim_v3 in sandbox/panel-0728v3-novelty/claim_v3; did not open claim/, claim_v2/, panel/, panel_v2/, attempts/, notes/ or other panel sandboxes
claim: runs/2026-11-24-0728/claim_v3 (partial win p1 of mertens-smallest-counterexample-upper-bound: certified re-evaluation of all 19 rows of Kim-Nguyen arXiv:2502.21021v1 Tables 1-2, to 3 decimals plus full balls)
date_utc: 2026-11-24T12:17:50Z

## Method
Every fetch was one plain curl request with User-Agent "V3R1T4S-panel-novelty/1.0 (verification research bot;
single request)". No retries of any URL. Fetched content was treated as data; no injection was seen.
Full log (UTC time, HTTP status, bytes, sha256 prefix, URL): sandbox/panel-0728v3-novelty/fetch_log.tsv
(38 requests). Non-200 results: arXiv export API 500 (server error; covered instead by the arXiv
HTML search, a different query page, not a retry of the same URL); Zenodo search 400 (my own request had size=50
above the anonymous limit of 25; the corrected query is a different request, not a block); GitHub REST
pulls list 403 "API rate limit exceeded" (not retried, see Gaps); Zenodo file URL 404 (wrong path built by
me; the file link taken from the record JSON then returned 200).

## Status source (claim_v3/status_source.md)
- URL https://en.wikipedia.org/wiki/Mertens_conjecture, HTTP 200, fetched 2026-11-24T12:13:59Z.
- sha256 of the page 6f5b7e5234e1e9f6283599b0d800c6ed393e98851e7538b6b5c2122b15f54b26, the same as the hash recorded
  in status_source.md. Page last edited 15 March 2026, at 17:25.
- Value quoted from the page: "In 2024, Seungki Kim and Phong Nguyen lowered the bound to e1.96×1019 ... but no
  explicit counterexample is known." (KNOWN)

## Searches (last 24 months) and what they found
- arXiv (HTML search "Mertens conjecture", 63 hits, newest first): 2025-2026 entries are 2502.21021 (Kim-Nguyen
  itself), 2505.08160 (Mertens' theorem, not relevant), 2608.24878 (Pintz, about the average order of |M(x)|; the
  abstract has no Kim-Nguyen tables) and unrelated stable-roommates/arctan papers. Kim-Nguyen abs page shows the
  record exists. No re-evaluation or correction found. (KNOWN)
- OpenAlex works citing the journal version (DOI 10.1007/s40993-024-00603-9): 4. They are Rozmarynowycz-Kim,
  Exp. Math. 2025 (an earlier bound); Ng, arXiv:2505.11295 (a survey); Johnston-Trudgian, Anal. Math. 2026
  (open access; Kim-Nguyen appears only in the references and acknowledgements); and Gaur, Zenodo 23403117
  (number fields). None of them re-evaluates the tables. (KNOWN)
- Crossref (bibliographic queries): only the journal article and Rozmarynowycz-Kim are relevant; no erratum or
  correction notice. The Springer article page shows no "Correction to" link. (KNOWN)
- HAL API ("Mertens conjecture", 7 hits): Bi-Hou hal-05838582 (2026-10-26), Yarman et al. hal-05675375
  (2026-06-30, about replicating the 1985 Odlyzko-te Riele disproof; its PDF never mentions Kim or Nguyen), and
  Kim-Nguyen hal-05016898 (2025-04-02). The rest are older or unrelated. (KNOWN)
- Zenodo: "Mertens" sorted by newest (2552 hits, top 25) has nothing relevant. "Kim AND Nguyen AND Mertens" finds
  Nguyen's own data record 11550925 (2024-06, the authors' own code and data, not independent; its Test-ST.txt
  and Test-Pinch.txt are byte-identical, ignoring CR, to claim_v3/inputs) and Gallego 23700212 (the version of
  concept DOI 10.5281/zenodo.23700211). (KNOWN)
- Gallego, Zenodo 10.5281/zenodo.23700211 (2026-10-27), EN PDF: "Control. The same program, with k = 3·10^-9,
  T = 74 000 and the point y of [KN25, Table 2], gives -1.00745 ... which agrees with the value -1.007 printed in
  [KN25, Table 2]." So only the record row is re-evaluated. (KNOWN)
- GitHub: repository search ("mertens conjecture", 7 repos; "mertens counterexample", 1 repo) turns up only
  bzyzz/mertens_bound and repos unrelated to these tables. bzyzz/mertens_bound has no releases (releases API
  returned []). I fetched the main-branch archive once and grepped it for all 19 published y values:
  - path1_report.txt: "Kim-Nguyen Record | -1.0074515576 | -1.0074515722 ..." (256-bit MPFR, the record row
    only) and "Peak1 (1.3860e19) | -0.9958957660 | -0.9958957567 ...", at
    y0 = 13859539710197847064.0623176514. That is 6.06e-5 from Table 2 row 2's y = ...064.062257. It is a
    polished different point, and the README says only Peak2 has been certified.
  - The Table 1 y values appear nowhere. Table 2 rows 4-14 appear only in kim_nguyen_ref/Test-ST.txt (the
    authors' file).
  - Table 2 rows 1 and 2 are also used as lattice-search seeds (legacy/focus_search.py). legacy/path4_verify_and_export.py
    computes 68-zero phase residuals and coset distances for "KN_00..KN_13", not h_StR, and no output from it
    is published.
  - Search logs list float cluster hits near row 1 (y=8895437864289867776.000000 plus dy, h=-0.97498624). These
    are floating-point search hits at a nearby double-rounded point, not a value at the published y and not a
    correction.
  None of this is a certified re-evaluation of the 18 non-record rows. None of it corrects Table 2 rows 1, 4,
  12 or 14. (KNOWN)
- This repo: TROPHY_CASE.md (local checkout, commit 25c9968 of 2026-11-15, and a fresh fetch of main on
  raw.githubusercontent.com, HTTP 200, identical to the local file) has no Mertens entry. known-knowns/ has no
  Mertens entry. Local git history (all refs) has no Mertens commit. (KNOWN)

## Journal version
Res. Number Theory 11 (2025), DOI 10.1007/s40993-024-00603-9. The Springer page returned HTTP 200 but is
paywalled ("Access this article" / "Buy article PDF"), so its tables were not visible. This is a stated gap, not a
fail. The HAL copy hal-05016898 links that DOI. I extracted the PDF with pdftotext and compared all 19 (y, h)
pairs from its Tables 1-2 with claim_v3/inputs/kn_arxiv_v1_tables_excerpt.txt: 19 vs 19, identical. (NUMERICAL,
string comparison)

## Credit check
- Zhenyu Bi and Enze Hou, HAL hal-05838582 (submitted 2026-10-26), together with github.com/bzyzz/mertens_bound:
  correct. The HAL PDF says "All code and certificates are available at https://github.com/bzyzz/mertens_bound".
  The repo value -1.0074515722 is quoted correctly.
- Peak1 is described correctly as a different polished point near Table 2 row 2 (about 6e-5 away in y, about
  -0.99590, uncertified) and is not treated as a re-evaluation of that row.
- The HAL copy of Kim-Nguyen (hal-05016898) is cited as printing identical digits. Confirmed above.
- Gallego (Zenodo 10.5281/zenodo.23700211, 2026-10-27, section 4 "The zeros, Table 1 and the sum", Control
  -1.00745) is still credited, correctly.
- Kim-Nguyen (arXiv:2502.21021, Zenodo 10775723) is credited. Note: Zenodo 11550925 is an earlier deposit by
  Nguyen of the same code and data. Citing it is optional.
- Minor, not required: the claim could also say that the bzyzz search logs hold uncertified floating-point
  hits near Table 2 row 1 (about -0.97499 at a nearby point). They do not change novelty.

## Gaps (stated, not fails)
- I could not list this repo's open and closed pull requests: the GitHub REST API returned 403 (rate limit).
  Under RULES 5 I did not retry and did not use an authenticated route. PR check: PENDING, for a human to look at
  github.com/elder-plinius/V3R1T4S/pulls?q=mertens. Mitigation: TROPHY_CASE on main and the local history (merged
  PRs up to 2026-11-15) show nothing on Mertens.
- The journal's typeset tables are paywalled, so I did not compare them directly. The HAL post-referee copy
  matches arXiv v1.
- The arXiv export API returned 500. The arXiv HTML search was used instead.
- GitHub code search needs authentication and was not used. The repository search and the full archive of the
  one relevant repo were used.

## Verdict
After searching arXiv, HAL, Zenodo, Crossref/OpenAlex (citing works), GitHub (including the bzyzz repo archive
and releases), TROPHY_CASE.md and known-knowns/, I found no existing independent certified re-evaluation of the
18 non-record rows of Kim-Nguyen Tables 1-2 and no published correction of their printed values, in particular
of Table 2 rows 1, 4, 12 and 14. The only independent re-evaluations found cover the record row (Table 2 row 3),
by Gallego and by Bi-Hou, and the claim credits them correctly. Novelty of the 18-row re-evaluation and the four
convention-free corrections: confirmed, with the PR-list gap above. (KNOWN for the search results; the
non-existence finding is bounded by the searched sources.)
pass: true
