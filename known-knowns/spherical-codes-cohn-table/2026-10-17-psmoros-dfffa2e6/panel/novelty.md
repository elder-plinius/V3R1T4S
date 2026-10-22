context: NOVELTY skeptic, subagent (Agent tool, fresh context), model opus; saved by the gate session from the returned text.

# NOVELTY skeptic: spherical-codes-cohn-table, (6,526), c* = 0.786427532330074 (panel-dfffa2e6)

Reviewed 2026-10-17, 21:50–22:00Z. Starting position: the result is not new until I fail to find a public value at or below 0.786427532330 for (6,526) that predates 2026-10-16T15:26:32Z.

**Verdict: I found no prior.** No public source I could reach lists a (6,526) code, or a code that dominates it, with cosine at or below 0.786427532330 before the claimant's upload. The only (6,526) value at or below c* anywhere is the claimant's own code, now on the live table. The pre-upload value 0.786636400242 is confirmed independently by Vahteristo's Zenodo data.

## Object
- object/d6_N526.txt: sha256 dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8 (matches the claim). 526 points in R^6.
- My own check (50-digit Decimal, normalised, float prefilter then exact max over 2,358 candidate pairs) gives c* = 0.786427532330074152872057367155… at points (202, 395). This matches the claim.

## (1) Live table, https://spherical-codes.org/ (one GET)
- robots.txt (fetched first) allows only `/`, `/robots.txt` and `/static/` for `*`. Only `/` was requested. /plain, /data and /upload-code were not requested.
- 2026-10-17T21:51:14Z: HTTP 200, 4,822,480 bytes, sha256 63f045d9fba53faccd0acd06645e9e2ddb08898642091148600a114c1cba95c8. This is byte-identical to the claimant's 21:47:47Z fetch.
- I parsed 16,648 rows (960 in d=6). There is exactly one (6,526) row: `0.786427532331 | Pavlos Moros, 2026.`, with no star and no "needs more optimization".
- The listed value is consistent with this code. The table rounds cosines up at 12 decimals: (3,9) and (7,56), whose cosines are exactly 1/3, are listed as 0.333333333334. So 0.786427532330074 rounds up to 0.786427532331.
- Nothing better is listed:
  - No (6,526) value is below 0.786427532330.
  - No row (6, N>=526) has cosine <= c*. Deleting points from such a code would give a 526-point code at least as good, and none exists. The nearest is (6,527) = 0.786484319899, also credited to Pavlos Moros, 2026.
  - No lower-dimensional row with N>=526 is anywhere close (best values: d=5 0.862094207579, d=4 0.934622453189, d=3 0.987016403921).
  - (6,525) is not listed.
- Limitation: I could not fetch /data/6/526 (disallowed), so I did not compare the posted file byte for byte. The match rests on the value (equal after rounding up to 12 decimals) and on the credit.
- Context: rows 520–534 in d=6 are all credited "Pavlos Moros, 2026". 338 rows table-wide carry this credit.

## (2) Public sources before 2026-10-16T15:26:32Z
**Vahteristo, Zenodo 10.5281/zenodo.23270586**
- The record page shows Version 1.0 (index 1, latest), published 2026-10-09. Its files were created 2026-10-14T20:13Z.
- I downloaded all three JSON summaries. Their MD5s match Zenodo's listing.
- (6,526) cosines:
  - combined (the best of all their runs): 0.7866364002418642. Rounded up, this is exactly the pre-upload table value 0.786636400242, which confirms the "record we beat" independently.
  - per_instance: 0.7866409885238883.
  - global: 0.7880757234615681.
- None of the three tables has an entry (6, N>=526) with cos <= c*. The closest is combined (6,527) = 0.7867115556.
- The JSON also records the older public table values for (6,526): 0.788562976701 on 2026-08-02, and 0.788513093183 on 2026-09-23 (credited to Antoine Jay, i.e. Jay et al.).
- The 2.6 GB coordinate zips were not downloaded. They are summarised by these JSON files.

**arXiv:2610.19988 (Vahteristo)**
- Abstract page: v1 only, submitted 2026-10-14 11:07:40 UTC. The abstract describes 60-second runs plus polishing. It reports no code beyond the Zenodo data.

**Jay et al. (SSRN 6427919)**
- I did not request SSRN: papers.ssrn.com returned 403 to this project on 2026-10-16.
- Their (6,526) values on the table were 0.788562976701 (2026-08-02) and 0.788513093183 (2026-09-23). Both are about 2.1e-3 above c*.
- The live table credits "Antoine Jay, 2026" on 1,313 rows, none of them (6,526).
- GitHub has no repository for their program (searches: "hypersphere equidistribution", "Poberznik").

**2025–2026 arXiv and other literature**
- arXiv's /search and /api paths and export.arxiv.org are disallowed by robots.txt, so I used three other routes:
  - **DataCite** (indexes arXiv and Zenodo DOIs). One query for "spherical code(s)" or "Tammes" in titles or abstracts, 2025–2026, returned 130 records. None reports a d=6 code near N=526. The relevant ones:
    - 2511.13391 (kissing numbers by reinforcement learning): table rows in d=13–22 only.
    - 2602.10233 (ImprovEvolve): its 90 benchmark codes span d ∈ [8,16] only (§4.4 of the arXiv HTML, v2 of 2026-06-26), so (6,526) was never in scope. Its table credits are in d=9, 14, 15, 24.
    - 2606.18984 (kissing arrangements in R^12): not relevant.
    - 2610.21263 (Delsarte bound): upper bounds, not codes.
    - Zenodo 18756225 (kissing configurations in R^6, N=72): withdrawn, and not N=526.
  - **arXiv "recent" listings** for math.MG and math.OC (2026-10-09 to 10-16, 83 + 312 entries): the only spherical-code paper is 2610.19988.
  - **WebSearch** (3 queries): no 2025–2026 paper with d=6 records found.
- Every arXiv ID the live table cites from 2025–2026 (2511.13391, 2602.10233, 2606.10402, 2610.19988) has no d=6 row near 526. Other 2026 contributors on the table (Özgen, Kevin Li, Farland, WolfFrogs, Granto, Borisov, Khrulkov, Kovačič, anonymous) have no d=6 row in 520–534. WolfFrogs has d=6 only at N=185 and 230; Kovačič only at N=86 and 98.

**GitHub** (gh, api.github.com)
- Repository searches for "spherical codes", "spherical code", "tammes" and "spherical-codes".
- Full file trees of eight repositories, with no (6,526) file in any:
  - ilmari99/Spherical-code-solver (certificates for other instances only)
  - matevz-kovacic/active-model (d=6 at N=86 and 98 only)
  - kantrarian/spherical-codes-vq
  - ChengJuiYeh/spherical-playground
  - spicylemonade/spherical-codes
  - MathieuDutSik/spherical_codes
  - maxime-fleury/open-problems-lab
  - JuanSembla/spherical_code_pmmh
- Code searches: `filename:526x6`, `filename:d6_N526`, `0.7864275`, `0.786427532`, `0.7866364` and a phrase query found nothing relevant. The `0.78642753` query returned HTTP 408 (timeout) and was not retried.

## (3) V3R1T4S pull requests
`gh pr list --repo elder-plinius/V3R1T4S --state all --search spherical` returned 10 PRs:
- **#231** (psmoros, CLOSED 2026-10-17T00:54:08Z, not merged): the claimant's earlier version of this claim, c* = 0.786430618545. That is worse than this code by 3.09e-6. It was closed by the maintainer as superseded by the live 0.786427532331 entry. Its body notes the upload; its README says nothing was uploaded. This package addresses that.
- **#70–#77** (calgulbenkian, CLOSED 2026-10-14): other spherical-codes-cohn-table cells in d=26–30 ((29,114), (30,74), (29,72), (28,70), (30,117), (29,145), (26,232), (27,68)). None is d=6.
- **#351** (rstevens70, OPEN): constant-weight codes, files under known-knowns/bigger-codes/. It matched the search text but does not touch this target.

Further searches over all 355 PRs ("cohn", "526", "d6_N526", "6,526", and a title scan for spher/cohn/526/kissing/packing) find no other PR touching (6,526). #311 (Packomania, N=507) is unrelated.

The main tree has no merged known-knowns/spherical-codes-cohn-table entry. Only the target description (known-unknowns/packings-physics/spherical-codes-cohn-table.md) exists. No PR by anyone else has a (6,526) value at or below c*.

## Notes for the panel (they do not change the novelty finding)
1. **Upload time.**
   - 15:26:32Z is the end of a 331-code batch, not the moment this file was sent. Per the claimant's own log (~/v3r1t4s/logs/cohn_upload.log, not independent evidence), the batch went out as 28 POSTs between 14:41:11Z and 15:26:01Z, with the summary line "uploaded 331 codes" at 15:26:33Z.
   - (6,526) is row 166 of 331, which in list order puts it in POST 14/28 at 15:03:33Z.
   - The same log shows that at 14:40:21Z the table's (6,526) value was 0.786430618545. That was the claimant's first upload, so no third-party value better than it was listed then.
   - Suggested wording: "uploaded in a 28-request batch on 2026-10-16 between 14:41Z and 15:26Z".
2. **Pre-upload fetch.** The pre-upload /plain fetch (05:12:04Z) is the claimant's, and I did not repeat it (robots). Its value is corroborated to the last digit by Vahteristo's Zenodo combined table.
3. **Not covered.**
   - SSRN full text of Jay et al.
   - Full texts of arXiv papers other than ImprovEvolve (titles and abstracts only).
   - Uploads pending at the table but not yet listed.
   - The 2.6 GB Zenodo coordinate zips (I used their JSON summaries).
   - Wayback Machine and DSpace snapshots. They are older than the live table, which keeps the best value.
4. **Robots conduct.** The claim discloses that /upload-code was used by scripted clients despite robots.txt. That is a conduct matter for CRITERION and the maintainer, not a novelty issue.

## Request log (every request; User-Agent "V3R1T4S novelty review (panel-dfffa2e6; one-off manual check)", one plain GET each, no retries)
I checked the stop logs in ~/v3r1t4s*/logs/stops-*.tsv beforehand. None of the hosts below had a stop in the last 24 h (api.openalex.org did, at 21:44Z, so it was not used). No new stops occurred, so ~/v3r1t4s/logs/stops-panel-dfffa2e6.tsv was not created. I honoured the crawl-delays (zenodo 10 s, arxiv 15 s).

| UTC | URL | status | bytes |
|---|---|---|---|
| 21:50:53 | https://spherical-codes.org/robots.txt | 200 | 130 |
| 21:50:54 | https://arxiv.org/robots.txt | 200 | 5,854 |
| 21:50:54 | https://export.arxiv.org/robots.txt | 200 (Disallow: /; host then unused) | 26 |
| 21:50:54 | https://zenodo.org/robots.txt | 200 | 272 |
| 21:50:55 | https://github.com/robots.txt | 200 (host then unused) | 14,489 |
| 21:50:55 | https://api.github.com/robots.txt | 404 (no rules) | 106 |
| 21:51:14 | https://spherical-codes.org/ | 200 | 4,822,480 |
| 21:52:14 | https://zenodo.org/records/23270586 | 200 | 95,461 |
| 21:52:26 | https://zenodo.org/api/records/23270586/files (explicitly allowed) | 200 | 5,145 |
| 21:52:56 | https://zenodo.org/api/records/23270586/files/README.md/content | 200 | 3,277 |
| 21:53:08 | …/files/combined.json/content | 200 | 6,707,750 |
| 21:53:53 | …/files/global.json/content | 200 | 6,648,142 |
| 21:54:38 | …/files/per_instance.json/content | 200 | 6,826,389 |
| 21:55:01 | https://arxiv.org/abs/2610.19988 | 200 | 42,306 |
| 21:57:55 | https://api.datacite.org/robots.txt | 404 (no rules) | 87 |
| 21:58:05 | https://api.datacite.org/dois?query=(spherical code(s)/Tammes in titles or descriptions) AND publicationYear:[2025 TO 2026]&page[size]=500 | 200 | 2,164,191 |
| 21:58:31 | https://arxiv.org/abs/2602.10233 | 200 | 42,480 |
| 21:58:47 | https://arxiv.org/html/2602.10233 | 200 | 1,379,051 |
| 21:59:24 | https://arxiv.org/list/math.MG/recent?skip=0&show=2000 | 200 | 119,767 |
| 21:59:40 | https://arxiv.org/list/math.OC/recent?skip=0&show=2000 | 200 | 447,830 |

**GitHub API calls** (gh CLI, api.github.com, authenticated):

| UTC | calls |
|---|---|
| 21:55:03 | pr list --search spherical |
| 21:55:14 | pr view 231 |
| 21:55:17 | pr view 351; pr list (all 355) |
| 21:55:27 | pr list --search cohn / 526 / d6_N526 / "6,526" |
| 21:55:29 | contents known-knowns/spherical-codes-cohn-table (404) |
| 21:55:33 | git/trees/HEAD (V3R1T4S) |
| 21:55:37 | contents known-unknowns/…/spherical-codes-cohn-table.md |
| 21:56:12 | 4 repo searches |
| 21:56:23–21:56:30 | 8 repo trees (+3 repeated listings) |
| 21:56:35–21:57:32 | 7 code searches (one HTTP 408, not retried) |
| 21:59:45–21:59:46 | 4 repo searches |

**WebSearch:** 3 queries ("arXiv 2026 spherical codes new records dimension 6 numerical optimization"; "\"spherical codes\" 2025 arXiv improved best known codes table Cohn"; "\"Equidistribution of points on the hypersphere including symmetries\" Jay").

**Files.** Downloads are in work/fetched/ (one directory per request, with headers). Scripts are in work/scripts/ (fetch.py, parse_index.py, zen_check.py, refs.py, refs2.py, rows_lookup.py, cstar.py). The machine-readable request log is work/requests.tsv.

pass: true
