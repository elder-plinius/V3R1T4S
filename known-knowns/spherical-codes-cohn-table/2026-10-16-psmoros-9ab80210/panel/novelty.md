(saved by the main session from the subagent's returned text, 2026-10-16T05:09:04Z; the text between the skeptic's BEGIN/END PANEL markers, verbatim)

# Panel: NOVELTY skeptic, spherical-codes-cohn-table, (d, N) = (6, 526)

context: subagent (Agent tool), model opus, fresh context that saw only claim/

Inputs read: CLAIM.md, REPRODUCE.md, object/d6_N526.txt, object/SHA256SUMS, archives/vahteristo_combined_D6_N525-527.json,
table/index_row_6_526.html, prereg/PREREG_run2026-10-16-0024.md, verify/check_claim.py (read; I recomputed c* with my own
script). Nothing else in the run folder was read.

Access: every request went through the shared helper vfetch.py with --lens novelty-skeptic. I checked the session stop list
(export.arxiv.org 503, papers.ssrn.com 403) and the two other lanes' lists changed in the last 24 h (flore.unifi.it,
cris.unibo.it, www.sciencedirect.com, web.archive.org, buponline.com, ri.conicet.gov.ar) and requested none of those hosts.
No request was blocked and nothing was added to the stop list. I used 5 of 5 api.github.com requests and 4 of 4 arxiv.org
requests. One Zenodo search returned HTTP 400 (validation error: unauthenticated page size must be <= 25). That is not a
block code, so I sent a corrected, different query with size=25. No retries, no logins, no uploads, no contact.

## 1. Status source (live, fetched once each)
- status 200 fetched_at 2026-10-16T04:04:38Z sha256 5bc9a557e80c83b5dea824323b2b07abdf55a7b28f8e1840b5bbe3471917479f bytes 405465 url https://spherical-codes.org/plain
  Value: line `6,526,0.786636400242`. The sha256 is the same as table/plain_2026-10-16T03-59-07Z.csv.
- status 200 fetched_at 2026-10-16T04:04:40Z sha256 0693ae85b23218945abacc3a92a8eee805de3c82bfa622148034f1868eeb863f bytes 4837340 url https://spherical-codes.org/
  The (6,526) row has cosine 0.786636400242, no `&ast;` and no "needs more optimization". Reference: "Ilmari Vahteristo, New
  spherical codes by tuning an annealing solver, preprint, 2026, arXiv:2610.19988". The page has exactly one
  href="/data/6/526". The sha256 is the same as table/index_2026-10-16T03-59-09Z.html.
- Neighbouring live rows (/plain and HTML agree for every d = 6 row):
  - 524: 0.786347387957 (Vahteristo)
  - 525: 0.786474636176 (Vahteristo)
  - 526: 0.786636400242 (Vahteristo)
  - 527: 0.786675138796, 528: 0.786717061054, 529: 0.786740332532, 530: 0.786764253041 (all "Henry Cohn, 2026, needs
    more optimization")
  - 531 to 539: 0.786791954464 up to 0.786906193700
- **Smallest live cosine among (6, N >= 526): 0.786636400242, at N = 526 itself.** That is 459 rows, N = 526..1024. The
  d = 6 sequence is monotone. The only HTML-only d = 6 rows are N = 23, 24, 25, 26, 31, 35 and 990, none of them relevant.
  So no larger-N live code gives a 526-point code below c* by deleting points.
- Lower dimensions embed in R^6. Their smallest live cosines at N >= 526 (all at N = 526) are far above c*:
  - d = 5: 0.862094207579
  - d = 4: 0.934622453189
  - d = 3: 0.987016403921
- status 200 fetched_at 2026-10-16T04:13:55Z sha256 93dd533c9fe57d7330a5c3aa7346800db0479383fe2dfc19ac1f459fe8b5b259 bytes 63169 url https://spherical-codes.org/data/6/526
  The posted code has 526 points and max cosine 0.78663640024186403146 (float screen at 1e-7, then 2606 pairs recomputed in
  mpmath at 50 digits). This matches the table and Vahteristo's archive.

## 2. c* (own recompute: mpmath at 50 digits, all pairs, no screen)
- file sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a (matches object/SHA256SUMS); 526 points in
  6 dimensions; 138075 pairs.
- c* = 0.786430618544579725385299139732, attained at points (168, 416), 0-based.
- Gain over the live table: 0.000205781697420275.
- Gain over Vahteristo's combined.json value: 0.000205781697284475.
- Note for the other skeptics: c* is also below the live (6,525) value 0.786474636176 (but above (6,524)). This is not a
  novelty objection to (6,526).

## 3. Public archives
- Vahteristo, Zenodo 10.5281/zenodo.23270586 ("Three tables of spherical codes for 'New spherical codes by tuning an
  annealing solver'", version 1.0, published 2026-10-09, created 2026-10-14):
  - status 200 fetched_at 2026-10-16T04:05:29Z sha256 5fd9df8d65d00c86d3d2b63a58bb19b0c6a85da59966ded4052691ca7dcae7e1 bytes 6793 url https://zenodo.org/api/records/23270586
  - status 200 fetched_at 2026-10-16T04:06:34Z sha256 5fd9df8d65d00c86d3d2b63a58bb19b0c6a85da59966ded4052691ca7dcae7e1 bytes 6793 url https://zenodo.org/api/records/23270586/versions/latest
    This is the same record, so there is no newer version.
  - status 200 fetched_at 2026-10-16T04:06:39Z sha256 613eab12bb674cd56bae3c18af301ef3d072dab06f2a5e8438d79b805f33b1ab bytes 6707750 url https://zenodo.org/api/records/23270586/files/combined.json/content
    md5 a417aa84aad94965b411f0137875fc87, the same as in CLAIM.md. D=6 N=526: cos 0.7866364002418642.
  - status 200 fetched_at 2026-10-16T04:07:01Z sha256 2d019681bea85119c93ac06286bec49ab99f4f068dcc09f9fdfd72a4ebc48d25 bytes 6826389 url https://zenodo.org/api/records/23270586/files/per_instance.json/content
    D=6 N=526: cos 0.7866409885238883.
  - status 200 fetched_at 2026-10-16T04:07:17Z sha256 d8d8128c35102f2af8a3e66ea9b4b3772114531756631bec469807de97cb1a16 bytes 6648142 url https://zenodo.org/api/records/23270586/files/global.json/content
    D=6 N=526: cos 0.7880757234615681.
  - In all three tables the minimum over D = 6, N >= 526 is at N = 526. The best is 0.7866364002418642 (combined),
    matching archives/vahteristo_combined_D6_N525-527.json.
  - Public values the archive records for (6,526): 0.788562976701 (2026-08-02) and 0.788513093183 (2026-09-23,
    attributed to Antoine Jay using the program of Jay et al.).
- Vahteristo's solver repository README:
  - status 200 fetched_at 2026-10-16T04:11:24Z sha256 54d5e1a05324e6f55e40ddd134b473f5cbd6146659c7150e9712b23396d196df bytes 7848 url https://raw.githubusercontent.com/ilmari99/Spherical-code-solver/main/README.md
  - It holds the solver, parameters and 24 exact certificates. It mentions no codes newer than the Zenodo record.
- Numaro:
  - status 200 fetched_at 2026-10-16T04:10:16Z sha256 efd97cc796e0985c521049996adb6fd941c927db77a378f13eb5c18b7efb3b90 bytes 159612 url https://numaro.tech/
  - status 200 fetched_at 2026-10-16T04:10:30Z sha256 d5afb2767b8741eb7c5d99f799b3f9769377fb69eb19dca90edcd79d42238c5f bytes 134852 url https://numaro.tech/research/spherical-codes-2026/
  - status 200 fetched_at 2026-10-16T04:10:55Z sha256 087e08b39027f37224c96f66238609100a743f0023175d41d712cd40061ea463 bytes 99199 url https://numaro.tech/research/
  - NUMARO-2026-015 (July 11, 2026) claims 11,004 records against the July 2026 table. It publishes coordinates only for
    (9,614), (9,615), (10,929) and (26,55). It says "Forty-one explicit coordinate files are retained for a later bulk
    release, which is not linked from this page yet". Its uploads appear on the table as "Uploaded by anonymous internet
    user, 2026".
  - No d = 6 value is published, and this is the only spherical-code post in the research index. The live (6,526) row is
    Vahteristo's.
- Ganzhinov and Östergård, codes inside shells of integer lattices (Zenodo 12755054; arXiv:2403.04330; IEEE TIT Dec 2024):
  - status 200 fetched_at 2026-10-16T04:12:36Z sha256 4a9a73756b0ff0217bf05b29129245b434f2a5e74b8acb515f323f69343cdd20 bytes 63626 url https://zenodo.org/api/records/12755054/files/B.pdf/content
  - status 200 fetched_at 2026-10-16T04:12:57Z sha256 1149fdf953d9d984590e614efdf0f86f5d573aec1755acb0ee9c3d1d8c92f912 bytes 327142 url https://zenodo.org/api/records/12755054/files/A.pdf/content
  - The largest d = 6 codes are (6,568) with cos 4/5 and (6,10,8,504) with cos 0.8. Every d = 6 code with cos <= c* has
    at most 264 points, so none has N >= 526 and cos <= c*.
- Zenodo search ("spherical codes" OR "spherical code" OR tammes, most recent):
  - status 400 fetched_at 2026-10-16T04:11:56Z sha256 8105c5098c3b8051ed4e35cc510a7c4af8dcca8edb46986c9a37ba5469c6985c bytes 207 url https://zenodo.org/api/records?q=%22spherical%20codes%22%20OR%20%22spherical%20code%22%20OR%20tammes&sort=mostrecent&size=50
  - status 200 fetched_at 2026-10-16T04:12:09Z sha256 b3e635aab11b67dc6c1164444cd4fcdba559671f70233a7eecc9c3e6298e7592 bytes 831763 url https://zenodo.org/api/records?q=%22spherical%20codes%22%20OR%20%22spherical%20code%22%20OR%20tammes&sort=mostrecent&size=25
  - 53 hits; I read the 25 newest. Only Vahteristo's two records hold d = 6 codes. The others are Tammes 15 and 16 points,
    D4 packing, designs and unrelated items.
- Jay et al., "Equidistribution of points on the hypersphere including symmetries" (SSRN): papers.ssrn.com is stopped (403
  at 01:11:46Z, another skeptic) and I did not request it.
  - status 200 fetched_at 2026-10-16T04:13:21Z sha256 fcaa32ad6b0e2859cc083a68ccbf6c15936eea437c9f25cad8ab066ad9927021 bytes 9037 url https://api.crossref.org/works/10.2139/ssrn.6427919
    This is DOI metadata only: title, nine authors, year 2026. The abstract says the method "in some cases, even discovers
    improved ones" and gives no values.
  - status 200 fetched_at 2026-10-16T04:11:45Z sha256 52ca77ee006eafde4db51113092ef75caeef57a041873f94380e259175260c98 bytes 16510 url https://arxiv.org/search/?query=Equidistribution+points+hypersphere+symmetries&searchtype=all&abstracts=show&order=-announced_date_first&size=50
    No arXiv version.
  - Their (6,526) code was on the table on 2026-09-23 at 0.788513093183 (per the archive) and was later superseded by
    Vahteristo.
- GitHub repository search:
  - status 200 fetched_at 2026-10-16T04:11:04Z sha256 1ef73d5af9cfa49dca65b9300302aac87512b2de2c446073a391e52d51305f2c bytes 357535 url https://api.github.com/search/repositories?q=%22spherical+code%22+OR+%22spherical+codes%22+OR+tammes&sort=updated&order=desc&per_page=100
    48 repositories. I read the READMEs of the recent candidates:
  - status 200 fetched_at 2026-10-16T04:11:25Z sha256 91d87e6135bbb272cebbb262ac95aad8416c51c0f13c2a281eb3a195885e5088 bytes 33365 url https://raw.githubusercontent.com/maxime-fleury/open-problems-lab/main/README.md
    Tammes on S^2 for N = 15..23 and kissing attempts in d = 5, 6, 7; "no record beaten".
  - status 200 fetched_at 2026-10-16T04:11:26Z sha256 0276a1a5d32c7e287d1162bbb43173f7cf2676164c7c4f61d5df576393bd495a bytes 11582 url https://raw.githubusercontent.com/kantrarian/spherical-codes-vq/master/README.md
    Vector quantisation; no table codes.
  - status 404 fetched_at 2026-10-16T04:11:28Z sha256 d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed bytes 14 url https://raw.githubusercontent.com/spicylemonade/spherical-codes/main/README.md
  - No repository holds a (6,526) code.

## 4. Literature, last 24 months
- arXiv searches:
  - status 200 fetched_at 2026-10-16T04:08:46Z sha256 2bb502c4d2d991a59cc5554983c1e3d11c6202d5fbef8d8aae2aa233b727e94c bytes 447116 url https://arxiv.org/search/?query=%22spherical+codes%22&searchtype=all&abstracts=show&order=-announced_date_first&size=100
    154 results; the 100 newest go back to 2015.
  - status 200 fetched_at 2026-10-16T04:09:35Z sha256 c6ea7946539e1e302845f1112d792bbd8a27ca10b28715ee3422881ff943fd03 bytes 467170 url https://arxiv.org/search/?query=%22spherical+code%22+OR+Tammes&searchtype=all&abstracts=show&order=-announced_date_first&size=100
    623 results; the 100 newest go back to 2024-09-10, so both queries cover the whole 24-month window.
- Spherical-code papers in the window:
  - 2610.21263 (Salmon; rate of the Delsarte LP bound): upper bounds
  - 2610.19988 (Vahteristo): the table's current row
  - 2609.34845 (Bekker; SDP and completely-positive hierarchies): upper bounds
  - 2609.25288 (Rado covering)
  - 2606.18984 (kissing arrangements in R^12)
  - 2602.10233 (ImprovEvolve)
  - 2602.01638 (noncommutative spherical codes)
  - 2512.25037 (polar dual pairs in E8 and Leech)
  - 2512.23092 (T-avoiding codes in R^32)
  - 2511.13391 (PackingStar, kissing numbers)
  - 2501.13906 (T-avoiding universal optimality)
  - 2411.16038 (Tammes in R^n via LP): upper bounds
  - Only 2610.19988 gives a (6,526) code, and it is the live row. Nothing newer supersedes it.
- ImprovEvolve full text:
  - status 200 fetched_at 2026-10-16T04:09:47Z sha256 fb5b6706b1ce32ee346916bafec3b0a8b4eeafff41c23aebe172ea3546761094 bytes 1379051 url https://arxiv.org/html/2602.10233v2
  - Its benchmark is "90 catalogue codes spanning d in [8,16] and N in [26,1021]", so there is no d = 6.
- Crossref works query:
  - status 200 fetched_at 2026-10-16T04:13:22Z sha256 d45a1a7c685b2401ad7f3d65d2bd3d5e4f3e7ebe657364652b37d9501b5ed606 bytes 22120 url https://api.crossref.org/works?query.bibliographic=spherical+codes&filter=from-pub-date:2024-10-01&rows=100&select=DOI,title,published,container-title,type
  - I read the top 100 by relevance. They are journal versions of the papers above, plus "Spherical codes attached to
    complex weighing matrices" (Discrete Math. 2026, 10.1016/j.disc.2025.114860). I did not read that paper because
    www.sciencedirect.com is stopped in another lane's list.

## 5. This repository (https://github.com/elder-plinius/V3R1T4S)
- TROPHY_CASE.md:
  - status 200 fetched_at 2026-10-16T04:08:27Z sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 bytes 30936 url https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
  - It lists degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench and cipher
    commitments. It has no spherical-code entry.
- Pull requests, state=all:
  - status 200 fetched_at 2026-10-16T04:07:51Z sha256 4e79e7c20356e2ed2ccc9031b955c394d8180744833f2544eb94e2f56fb3666c bytes 1961432 url https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1
  - status 200 fetched_at 2026-10-16T04:08:00Z sha256 1566c860af97f73907eca9a2cf8d3b211c54b222de07cecc832dfaa9099a4c70 bytes 1828321 url https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=2
  - status 200 fetched_at 2026-10-16T04:08:11Z sha256 c63f639c673944bebcafc55c1ddc0d54d89ed99dcadc7dfb6a647b5e36866a55 bytes 336621 url https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=3
  - 218 PRs, numbers 1 to 220; #61 and #152 are issues, not PRs.
  - The spherical-codes-cohn-table PRs are #70 to #77, all closed and unmerged. They cover (29,114), (30,74), (29,72),
    (28,70), (30,117), (29,145), (26,232) and (27,68), so none is in d = 6.
  - No PR title or body mentions (6, 5xx), 526, or cosines 0.7864 / 0.7866.
- Issue and PR search:
  - status 200 fetched_at 2026-10-16T04:14:30Z sha256 7cf83b64232fb5b3eb10ef6e96e7a809dab2fb5bec8ff5adc815eb8e9714106c bytes 39541 url https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+spherical&per_page=100
  - 8 items, all of them PRs #70 to #77. None mentions d = 6.

## Not covered, and whether it leaves a genuine doubt
- The Jay et al. SSRN full text and any later Jay codes (host stopped). Their last public (6,526) value was 0.788513093183.
- Numaro's unpublished ledger and bulk release.
- Uploads to spherical-codes.org still awaiting maintainer review (not public).
- arXiv full text: the searches cover titles and abstracts only, and the export.arxiv.org API is stopped.
- The Discrete Mathematics 2026 weighing-matrix paper (ScienceDirect stopped).
- Google Scholar and GitHub code search (code search needs authentication).

Judgment: the margin is 2.06e-4. Cohn's table is the field's aggregator, and it already includes Vahteristo's codes of
2026-10-14 for this row. No public source I could reach comes within 2e-4 of c*. These gaps leave a small residual doubt
but not a genuine one.

## Verdict
c* = 0.786430618544579725 is strictly below every known public value for (6,526) by 2.0578e-4, far more than the 1e-10
margin. The known values are:
- the live table, 0.786636400242;
- Vahteristo's combined table, 0.7866364002418642;
- Vahteristo's per_instance table, 0.7866409885238883;
- Vahteristo's global table, 0.7880757234615681;
- Jay et al., 0.788513093183;
- the posted code, 0.78663640024186403;
- every live (6, N >= 526) row (minimum 0.786636400242).

It is not a tie, and nothing newer supersedes the row.
novelty: PASS
pass: true
