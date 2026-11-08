# CRITERION verdict: spherical-codes-cohn-table, cell 29-727

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:38:13Z

## Value computed here
- object/29_727.txt: sha256 a796ba15c620c062792f104ee416a92acba3ab77cabe80ceedcf97f67e233ddc (matches CLAIM.md). 727 rows by 29 columns, plus one `#` header comment line.
- c* (mpmath, mp.dps=50, every vector normalised, all 263,901 pairs computed with mp.fdot) = 0.2365029694576581825515417, at pair (697, 722) counting rows from 1. A float64 Gram matrix gives 0.2365029694576582 for the same pair. Minimal angle 76.319765750948303866°.
- Fetched pages (curl -L, UA curl/8):
  - https://spherical-codes.org/plain: 2026-11-08T02:35:07Z, HTTP 200, sha256 9f26579e6f0842bb92f62f790943000afd787a1b2a0145476997b9620abbc493. The row reads `29,727,0.240054045231`.
  - https://spherical-codes.org/: 2026-11-08T02:35:07Z, HTTP 200, sha256 0f9353613fea9193f1135cba56c09c0a3c9069d95b5578c5afb7466de31091ff.
  - https://spherical-codes.org/data/29/727: HTTP 200, sha256 bc7648857920fcba1f07ec9a44fd4ac9b117b13083213122cc8abfe5917ed1db. 727 rows by 29 columns; its own cosine is 0.240054045230384, which is 6.2e-13 from the table value.
  - arXiv API, all:"spherical code", newest 15: 2026-11-08T02:35:53Z, HTTP 200, sha256 0ca177d40f6a7f9bc0f8a1df1731d1f0de663891add4937f42c816ca78df8ace.
  - arXiv API, all:Tammes, newest 15: HTTP 200, sha256 d65abefe3ec09a8e4337889994bf974bac8b2674a005572f82d790f117e1364d. A retry with abs/ti:"Tammes" at 02:36:12Z (sha256 6b2073661e34e253708ec69a7fd15cffec3411d63720c84bffda546e31158833) also returned only "Tamm" stem matches, none of them about spherical codes.
  - https://arxiv.org/abs/2610.19988v1 (Vahteristo, "New spherical codes by tuning an annealing solver", 2026-10-14): HTTP 200, sha256 86b0f0d76a42a08bce38988e7f1d8b2bf495ebb05f6fc866eeaa49f93b79a2f2.
  - Its data record https://doi.org/10.5281/zenodo.23270586 (fetched via the zenodo.org API at 02:36:34Z, all HTTP 200):
    - combined.json, sha256 613eab12bb674cd56bae3c18af301ef3d072dab06f2a5e8438d79b805f33b1ab
    - per_instance.json, sha256 2d019681bea85119c93ac06286bec49ab99f4f068dcc09f9fdfd72a4ebc48d25
    - global.json, sha256 d8d8128c35102f2af8a3e66ea9b4b3772114531756631bec469807de97cb1a16
  - https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md: 02:38:06Z, HTTP 200, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113.
  - GitHub search for PRs mentioning 727: HTTP 200, sha256 bcb137707947c86e6e2937408ab92fe7065569f65fd409e58250269806ff0299.

## Clauses checked
- Clause (a) row (29, 727) is present in the live /plain: PASS. The row is `29,727,0.240054045231`.
- Clause (b) coordinates have >= 20 digits: PASS. Every coordinate in object/29_727.txt has at least 21 significant digits as written (for example `-9.17817198402140072000e-02`). Many end in zeros, so the 21-digit count holds for the text as written, not necessarily for its information content. Precision is not at issue: float64 and mpmath agree to about 1e-17.
- Clause (c) c* is below the live 12-decimal cosine by >= 1e-10: PASS. 0.240054045231 - 0.2365029694576581825515 = 0.00355107577334182, far above 1e-10.
- Clause (d) the HTML index row has no '&ast;' mark: PASS. The row reads `<td>29</td> <td><a href="/data/29/727">727</a></td> <td>0.240054045231</td> <td>Azmi C. &Ouml;zgen, 2026.</td>`, with nothing after `</a>`. Proven-optimal rows elsewhere on the page carry `</a>&ast;`, for example /data/3/7.
- Clause (e) the row has no 'needs more optimization' text: PASS. The current reference cell is "Azmi C. Özgen, 2026." Vahteristo's Zenodo snapshot of 2026-09-23 recorded this row as 0.241476113108, "Henry Cohn, 2026, needs more optimization." Since then the table has replaced that entry with an unflagged one.
- Clause (f) no newer arXiv result for (29, 727): PASS.
  - Among the newest 15 "spherical code" hits, the only one that tabulates codes is arXiv 2610.19988, which covers every N <= 1024 and 3 <= D <= 32. Its best (29, 727) code has cosine 0.25787758776387953 in the combined table (per_instance 0.25788, global 0.25816). That is worse than both the table and the claim.
  - The other "spherical code" hits are bounds papers or unrelated ML/physics work.
  - The arXiv API stems "Tammes" to "Tamm", so the Tammes query returned no relevant hits.
  - No prior V3R1T4S PR or TROPHY_CASE entry mentions (29, 727).
- Clause (g) the kissing-number exclusion does not apply: PASS. d = 29 lies outside 9..23, so the exclusion cannot apply even though c* <= 0.5.

## Decision
I recomputed every clause myself from live fetches, and each one holds. c* = 0.23650296945765818255 is 3.55e-3 below the live table cosine 0.240054045231. The (29, 727) row has no optimality mark and no "needs more optimization" flag, and the only newer arXiv code table (2610.19988) is worse for this cell. My method differs from the bank's checker in one place: for the posted /data/29/727 sanity check I found the maximising pair in float64 and refined only that pair in mpmath, instead of recomputing all pairs at 50 digits. It reproduces the table to 6.2e-13. In claim/ I found no text that tried to steer the verdict.

pass: true
