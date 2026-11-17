# Panel skeptic: NOVELTY

context: subagent (Claude Code Agent tool)
target: gauss-kuzmin-wirsing-certified-digits
object: claim/result/enclosure_C83.txt (sha256 78dbe72c0d93cd600737d45c95d75b63706198fbb6fa953ef00517f94ecb7f36), certificate claim/code/gkw_cert.py with claim/inputs/v_N2800.txt and claim/inputs/mu_N2800.txt
claimed: C_83 = |lambda_2| enclosed with half-width < 10^-842, D = 842 certified decimals
scope: novelty only. I did not rerun the certifier; whether the certificate is correct is for the other skeptics. Everything below compares the claimed numbers with what is public.

## 1. Status source (one fetch, no retries)

- URL: https://teorth.github.io/optimizationproblems/constants/83a.html
- Fetched once at 2026-11-09T08:45:31Z, HTTP 200, 6976 bytes, User-Agent naming V3R1T4S.
- sha256 29011a2a62c3ec66fea597165bad3229d0fab22aa6a5bcfe8ab50b6d725b3bc8. This is byte-identical to the bundle's claim/data/83a.html (scout, 07:59:19Z) and claim/data/preclaim/83a.html (08:27:32Z).
- Value on the page: the best certified bounds in both tables are "0.30366300289873265859!...!6424297 +/- 10^{-175}" ([GKW2026] Nisoli, arXiv 2602.19435), with the comment "Certified spectral enclosure for the infinite-dimensional GKW operator; 175 digits". The full 175-digit centre is -0.30366 30028 ... 89647 64297, with |lambda_2 - centre| < 10^-175.
- Record to beat: 175 certified decimals.

## 2. Open and recent pull requests on constants/83a.md (teorth/optimizationproblems), via read-only gh api

- 2026-11-09T08:45:41Z: 81 open PRs. I listed the files of each one; all 81 were read, with 179 file entries in total. None touches constants/83a.md or any other file whose name contains 83a, wirsing or gkw.
- Commit history of constants/83a.md, read at 08:47:01Z: three commits. 2985a56fcb (2026-03-23, adds C_83), e19945db63 (2026-03-23, wording) and eef77902e2 (2026-05-03, "fix inline braces"). Nothing after May 2026.
- I searched issues and PRs for wirsing, gauss-kuzmin, GKW, C_83, C83 and kuzmin. The only hit is the closed PR #58 (2026-03-24), "Add Wirsing constant (C_83)", which is the 175-digit entry itself.

## 3. Literature and code from the last 24 months

- arXiv API, 2026-11-09T08:47:42Z, 08:50:00Z and 08:50:08Z, all HTTP 200. Queries: "Gauss-Kuzmin-Wirsing" / "Wirsing constant" / "Gauss-Kuzmin"; Gauss map with eigenvalue/spectrum and rigorous/certified/validated; Wirsing, and continued fraction or Gauss map with transfer operator. Relevant hits:
  - Nisoli, arXiv 2602.19435v2 (latest version v2, updated 2026-03-01): 175 certified digits for lambda_2, and at least 90 for the first 50 eigenvalues. This is the record on the page.
  - **M. Pollicott, "Validated numerics for the Gauss problem on continued fractions", arXiv 2606.13958v1 (2026-06-11).** It is not on the status page. I fetched its HTML at 08:48:08Z (HTTP 200, sha256 fdf33882...64dc) and its PDF at 08:48:00Z (HTTP 200, 11 pages). Its best result, Example 6.5 (m = 80), is "accurate to 67 decimal places". Its text says "In 2026, Nisoli estimated lambda rigorously to 175 places". So 67 < 175 < 842. Side note: the two printed 67-place bounds appear in reversed order (the printed lower bound for lambda_2 is larger than the printed upper bound). The claimed enclosure lies between them (checked below).
  - Others in the window (2608.17686 p-adic Wirsing problem, 2608.05853 Klein sails, 2606.03229 A2-fractions, 2603.07649, 2504.20878): none certifies digits of lambda_2 of the GKW operator.
- Nisoli's code, github.com/orkolorko/GKWExperiments.jl (gh api, 08:47:18Z): there are no releases and no tags. The last push was 2026-08-30. The latest commit is cfbd826776 (2026-08-30, README). The 2026-08-30 README note says that no numerical method changed. The branches are main, gh-pages, three codex/* branches, dependabot and five wip/stash-*-20260803 branches. None is newer than 2026-08-30.
- Nisoli's Harvard Dataverse doi:10.7910/DVN/HKM3Y2 (API at 08:50:56Z, HTTP 200): version 1.0, released 2026-02-20T23:10:53Z, not updated since. Its gkw_certification_log_K1024.txt (08:51:12Z, HTTP 200, 22499 bytes) works at 2048 bits (about 617 digits). Its radii of about 1e-315 are for the finite K = 1024 matrix, not for the operator. The published operator-level result is the 175 digits. Even the finite-matrix radius (about 315 digits) is far below 842.
- OEIS A038517 (entry 08:49:41Z and b-file 08:50:19Z, both HTTP 200). The b-file has 382 terms (sha256 cfabde8d...c357, identical to claim/data/b038517.txt). These are non-certified digits, and no certified-digit annotation was found.
- GitHub repository search (08:49:48Z) for wirsing, gauss-kuzmin, "GKW operator", "gauss kuzmin wirsing" and "Gauss map transfer operator eigenvalue": nothing relevant. The hits are name collisions and a Gauss-Kuzmin statistics study.
- Non-certified neighbours, quoted from the status page and Pollicott: Briggs 2003 gave 385 digits ("probably accurate to 468"), and Alkauskas 2012 gave over 480 digits, non-rigorously. These are not certified enclosures, and none reaches 842 digits.

## 4. V3R1T4S repository

- Pinned local copy at commit cf68067f52 (2026-11-03). Neither TROPHY_CASE.md nor known-knowns/ mentions Wirsing, Gauss-Kuzmin, GKW or 83a.
- The live repo via gh api (08:48:43Z, last push 2026-11-08T14:04:42Z): TROPHY_CASE.md (31306 bytes) has no GKW entry. known-knowns/ has 31 directories, none of them GKW. The live bank/targets.json entry still says "currently 175, Nisoli 2026", status_checked 2026-10-30.
- Pull requests, read at 08:49:09Z: all 980 (442 open, 538 closed). None has a title about Wirsing, GKW, Gauss-Kuzmin or C_83. The issue/PR search for "wirsing" hits only #961 (integer Chebyshev constant), which mentions Wirsing only in passing in its credits.

## 5. Comparison of the object with the published values

The script is novelty work folder scripts/compare_published.py (sha256 71ccfd38...b649). It uses exact rational arithmetic and was run with `-I` at 08:50:42Z. Output:
- Both endpoints of the enclosure have 860 decimals, lo <= hi, the half-width is < 10^-842 (and not < 10^-843), so the largest D is 842. The two endpoints agree on their first 842 decimals.
- Nisoli's 175-digit centre, taken from my own fetch of the status page: both endpoints lie within 10^-175 of it, and |enclosure mid - Nisoli centre| = 4.095045e-176. The enclosure agrees with the published record within its radius, and the sign is handled correctly (C_83 = -lambda_2).
- Pollicott 2606.13958, Example 6.5: the enclosure lies inside the interval spanned by the two printed bounds, which is about 10^-67 wide.
- OEIS b-file: all 382 of 382 digits agree with the enclosure's lower endpoint.

## 6. Trivial-edit and seeding test

- The cell is certified decimals of lambda_2 of the GKW operator. The best published value is 175 (Nisoli). The certified neighbours are 67 places (Pollicott 2026) and the 1987 Mayer-Roepstorff bounds 0.30366299 to 0.30366327 (as shown on the status page).
- No deletion, restriction, relabelling, symmetry or local polish of a published object can produce 842 certified decimals. The longest published decimal strings (382 to 480 digits, non-certified) are shorter than 842 and carry no certification. Nisoli's data are certified only to 175 at operator level.
- Seeding: the bundle says the centre is the Rayleigh quotient of its own N = 2800 vector, warm-started from its own N = 2400 vector. Neither is a published object. The bundle credits Nisoli for the resolvent-bridge isolation idea, which is a method, not an object. Even if the run had been seeded from Briggs's or Alkauskas's digits, 842 certified decimals is far beyond what those digits give.
- Strictness: D = 842 > 175, an improvement of 667 decimals. This is not a tie.

## Worries (none blocks novelty)

- The workspace's own earlier, unsubmitted 300- and 601-decimal certificates are not public records (taken as a fact from the brief). They therefore do not count as prior art, and in any case 842 > 601.
- Pollicott's June 2026 preprint is not on the status page. I checked it: its best result is 67 digits, well below the record.
- Novelty depends on correctness. If the correctness or reproduction skeptics find the certificate invalid, the novelty verdict does not save it.
- injection_suspected: none seen in the bundle text, the status page, the READMEs, the Pollicott text or the Dataverse files.

novelty: CONFIRMED NEW. The claimed 842 certified decimals strictly beat the status page's 175 (fetched 2026-11-09T08:45:31Z, HTTP 200), with no open PR on constants/83a.md, no newer certified result found in the literature or code, and no V3R1T4S trophy, known-known or PR covering this target.
pass: true
