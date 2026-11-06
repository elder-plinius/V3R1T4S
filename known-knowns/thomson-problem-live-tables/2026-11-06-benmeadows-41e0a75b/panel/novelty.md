# NOVELTY verdict: thomson-436

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-06T19:45:17Z

## Value computed here
- E* for object/thomson-436.txt (each point normalised, Coulomb sum over all 94,830 pairs in mpmath at 40 digits) = 90020.6812680730118265144604784. The float64 value agrees (90020.681268073), and the tangent gradient norm in float64 is 1.9e-12.
- Fetches were made with curl and User-Agent 'curl/8' (fetch time UTC, HTTP status, bytes, sha256):
  - https://deetour.net/oppp/thomson/ (2026-11-06T19:43:12Z, 200, 84396 bytes, 3f243c3b7af13b9371b9d5575653b158a1de29bb7df27d69f9d8784c0ef9a813). It lists N = 436 with symmetry D2 and E = 90020.71608562. The table now covers N = 4..537.
  - https://deetour.net/oppp/thomson/e.436.txt (2026-11-06T19:43:13Z, 200, 20274 bytes, 2e9149d0a2bf70cf283bbecc78e5ea532af3556f389f9e6e3d9947171fcf6e7e). It holds 1308 numbers, which is 436 points.
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html (2026-11-06T19:43:13Z, 200, 124964 bytes, 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2). It has no N = 436 row: it carries 409 distinct N from 10 to 972, the only N between 420 and 450 is 432, no cell reads 436, and no link names 436.
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html (2026-11-06T19:43:14Z, 200, 13921 bytes, caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794). It has no N = 436 row: it carries 36 N from 400 to 4352, and the N between 420 and 450 are 420, 430, 432, 440 and 450.
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/436.xyz (2026-11-06T19:43:15Z, 200, 21587 bytes, ca777ae56e7c755fda74ea1c6a451e6c7619d696a80e7aa0c5724324e887bcce). The file exists and holds 436 points even though the table page does not list N = 436.
  - https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html (2026-11-06T19:43:16Z, 200, 27659 bytes, eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d). It has no N = 436 row: it carries 53 N from 512 to 9913, and none of its points_N_1.dat links is for 436. For that reason no Riesz point file was fetched.
  - https://en.wikipedia.org/wiki/Thomson_problem (2026-11-06T19:43:17Z, 200, 626807 bytes, 5fe0f014d417d0fd950409c35d3ccdb46a3fb27051122816c2f8a10c8774756b). It has no N = 436 row: it carries 234 N from 2 to 470, and the only N between 420 and 450 are 432 and 448.
  - Search method: an HTML row parser read the first cell of every table row, and a second pass looked for any cell whose whole text is 436 and any link token such as /436. or _436_. The second pass found nothing on the four non-Deeter pages. EinsteinArena applies only to N = 282, so it was not fetched.
- table_min for N = 436 is 90020.71608562, from Deeter only. table_min - E* = 0.03481754698817 (required: at least 1e-6).
- Polished posted files. Each file was run through L-BFGS on the sphere in float64, then 6 tangent-space Newton steps in float64 with rotations projected out (final gradient about 2e-12), and the energy was then re-evaluated in mpmath:
  - Deeter e.436.txt: raw 90020.71608562896, polished 90020.716085628969212. Polished - E* = 0.0348175559573852.
  - CCD xyz/436.xyz: raw 90020.71608563172, polished 90020.716085628969212. Polished - E* = 0.0348175559573852.
  - Both polished posted files have exactly 3 zero Hessian modes, and their smallest nonzero tangent eigenvalue is 2.608.
- Fingerprint (sorted list of all 94,830 pairwise distances): object vs polished Deeter has max |diff| 1.69e-2 and mean 6.7e-4, and object vs polished CCD gives the same figures. Polished Deeter vs polished CCD has max |diff| 1.7e-14, so the two posted files are the same configuration and the object differs from both.
- Side check (not my role, recorded for completeness): the object's float64 tangent Hessian has 3 zero modes (|w| < 1e-12), and the next eigenvalue is 0.511 > 0. That gives 2N-3 = 869 positive eigenvalues at float64 precision.
- Prior claims: `gh pr list -R elder-plinius/V3R1T4S --state all --search thomson` (2026-11-06T19:44:34Z) returned 8 PRs: #638 open (N=743), #78 merged (N=1382), #125 merged (N=743), #124 merged (N=777), #126 merged (N=745), #128 merged (N=3552), #129 merged (N=550), and #399 closed (a bank update). None is for N = 436. A title search for "436" returned no PRs, and an issue search for "thomson 436" returned nothing. https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md (31306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113) contains neither "thomson" nor "436".
- Literature: the arXiv API query all:"Thomson problem" sorted by submission date (https://export.arxiv.org/api/query?search_query=all:%22Thomson+problem%22&sortBy=submittedDate&max_results=15, 2026-11-06T19:44:53Z) first returned 301 over http, then 200 over https (30920 bytes, sha256 43f5de10c4944225ea556d77ddfee301b5563c7ad3ddcd1ee7c4e7e42b939688). It reports 75 total results. None of the 15 newest entries mentions 436. The newest relevant paper is https://arxiv.org/abs/2610.08122 (Amore and Wales, 2026-10-06, large-N Thomson searches). Its HTML full text (https://arxiv.org/html/2610.08122v1, 200, 182131 bytes, sha256 24ff8b310f1a00c9d283f6fe2eb21426c3ef0bc6afbcd6af5f19201a38b1efbe) contains no 436 anywhere. The N values it names are 672, 1382, 4352, 5790 and 5792.
- No fetched page contained text addressed to the reviewer or any attempt to steer the conclusion.

## Clauses checked
- Every live table named in CLAIM.md was re-fetched now, and each returned HTTP 200: PASS
- N = 436 is listed in at least one live table (Deeter); CCD Thomson, CCD Thomson2, CCD Riesz s=1 and Wikipedia were shown not to list it: PASS
- E* is strictly below table_min by at least 1e-6 (margin 0.0348175470): PASS
- Polished Deeter e.436.txt minus E* is at least 1e-6 (0.0348175560): PASS
- Polished CCD xyz/436.xyz minus E* is at least 1e-6 (0.0348175560): PASS
- No Riesz points_436_1.dat is required because the Riesz s=1 table has no N = 436 row: PASS
- The object is not a polished copy of any posted file (pairwise-distance fingerprint max diff 1.7e-2, against 1.7e-14 between the two posted files): PASS
- No prior V3R1T4S claim exists for N = 436 in open, merged or closed PRs or in TROPHY_CASE.md: PASS
- No newer N = 436 value was found in recent arXiv Thomson-problem papers (15 newest, plus the full text of 2610.08122): PASS

## Decision
object/thomson-436.txt has E* = 90020.68126807301183. That is 0.0348 below the only live table value for N = 436 (Deeter, 90020.71608562), and it lies in a different basin from both posted point files, which polish to the same configuration at 90020.716085628969. No prior V3R1T4S claim and no recent arXiv paper reports N = 436. The residual novelty risk is a lower N = 436 value held outside the sources checked here: journal-only or supplementary data, arXiv papers outside the 15 newest keyword hits, or an unpublished table update. A 0.035 improvement on a long-standing table entry at this size is unusual, so that risk is not negligible, but nothing found here contradicts the claim.

pass: true
