# Novelty verdict, hsp4 N = 79

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Claim under review (CLAIM.md): 79 equal balls in the unit 4-ball with feasible radius
r* = 0.256565783134456..., versus Packomania's posted hsp4 value for N = 79, 0.256468324828.
Candidate file: hsp4-79-candidate.txt. Snapshot of the table: hsp4_radius_as_fetched.txt.

Each live source below was requested exactly once, with User-Agent "V3R1T4S skeptic",
no retries. All six returned HTTP 200; no challenge page was served.

## Fetch 1: live table

- URL: https://packomania.com/hsp4/txt/radius.txt
- Time: 2026-10-16T17:48:37Z (date -u)
- HTTP: 200 (curl -w '%{http_code}')
- Row 79 quoted verbatim: `79 0.256468324828`
- 299 rows; the file is byte-identical (cmp) to hsp4_radius_as_fetched.txt in the claim folder.

## Fetch 2: status page

- URL: https://packomania.com/hsp4/hsp4.html
- Time: 2026-10-16T17:48:38Z
- HTTP: 200
- Quoted: `Last update: 06-Jul-2025`
- History of updates, complete list of entries: 04-Jul-2025 (first presentation N=2-100),
  05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300), all by E. Specht [31].
- No entry newer than 06-Jul-2025. No history entry mentions N=79. The only occurrence of "79"
  in the page is the table row for N=79 (value 0.256468324828, reference [31]) and a column
  value inside the N=84 row.

## Fetch 3: pending-requests queue

- URL: https://packomania.com/pending-requests.html
- Time: 2026-10-16T17:48:40Z
- HTTP: 200
- Page dated 08-Oct-2026. Zero occurrences of "hsp" anywhere on the page: no hsp4 range includes 79
  (no hsp4 entry exists at all).
- Visible but not applicable: `24-Sep-2026 01:29 Moki & Julio crt 3 candidates for 79, 271, 280`
  is category crt (not hsp4), so it does not trigger the queue rule.
- QUEUE CAVEAT (unresolvable): `26-Sep-2026 01:11 Moki & Julio *many* 4666 candidates total`
  carries no category. It could in principle contain an hsp4 candidate for N=79. This cannot be
  resolved from the page; per the bank entry, the N must be re-checked against the live table once
  that bundle leaves the pending list. This verdict is conditional on that re-check.

## Fetch 4: TROPHY_CASE.md

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
- Time: 2026-10-16T17:48:40Z
- HTTP: 200
- grep -iE 'hsp4|hypersphere|\b79\b|hsp[0-9]|packomania|packing|ball': zero matches.
  The file (dated 2026-10-10, families added 2026-10-12) lists six result families, none of
  them a Packomania hypersphere family. Nothing matches or beats the candidate.

## Fetch 5: open pull requests

- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
- Time: 2026-10-16T17:48:41Z
- HTTP: 200
- 52 open PRs. Searched title, body and branch name for hsp / hypersphere / packomania / 79.
  Packomania PRs present are all other targets: scu spheres-in-cube (#235-#238, N=882-886;
  #206, #207), cci circles-in-circle (#234, N=4141). #231 is spherical-codes-cohn-table (6, 526),
  a different target. #215 matches "79" only as "79/79 tests passed". No open PR targets
  packomania-hyperspheres-hsp4-hsp6, and none mentions N=79 in dimension 4.

## Fetch 6: merged family on upstream main

- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
- Time: 2026-10-16T17:48:42Z
- HTTP: 200
- Directory exists and holds 12 subdirectories, all named 2026-10-14-<author>-<hash>, consistent
  with the stated 12 merged N values (30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75). The directory
  names do not expose N, and I made no further fetches, so I take the N list from the panel
  instruction; 79 is not among them.

## Literature search (web, 2024-2026)

Three searches: "packing 79 equal hyperspheres in a 4-dimensional ball radius best known
2025 2026" (extended); "hsp4 packomania hyperspheres in a 4-ball improved packings";
"arXiv 2025 OR 2026 hyperspheres 4-dimensional ball packing N equal balls best known radii
table Specht". Results returned only: Packomania's 3-D ssp table (updated Jul-2026, a different
problem), the Stoyan-Yaskov 2012 hyperspheres-in-a-hypersphere paper (pre-window, counts not
radii), 4-D lattice/24-cell density work (arXiv 2609.25120, 1712.04099), OEIS 3-D counts,
and hyperbolic-space packings. No 2024-2026 source lists a packing of 79 equal balls in a
4-ball with radius at or above 0.256468324828, let alone above the candidate.
Packomania's own hsp4 page (fetch 2) cites only Specht [31] for N=79.

## Independent recomputation (local, no tolerance)

mpmath is not installed here, so I used Python's decimal module at 50 digits on the files in the
claim folder, directly from the submitted coordinates:
- N = 79 in both candidate and posted files.
- r*(candidate) = 0.25656578313445631327...
- r*(posted)    = 0.25646832482658934891... (matches the table's 0.256468324828 within 1e-11,
  so the parser is sane).
- gain = r*(candidate) - live table row = 9.745831e-05, which exceeds 1e-10 by about six orders
  of magnitude. Not a tie.
- max difference of sorted pairwise-distance multisets vs posted = 1.58e-02 (> 1e-8): not isometric.

## Conclusion

The live hsp4 table still posts 0.256468324828 for N = 79 (unchanged from the snapshot); the
candidate strictly beats it by 9.75e-05; no History-of-updates entry newer than 06-Jul-2025 exists;
no hsp4 range appears on the pending list; TROPHY_CASE.md, the merged
packomania-hyperspheres-hsp4-hsp6 family and the 52 open PRs contain nothing for (4, 79); and the
literature search found no competing value. The single unresolved item is the category-unspecified
26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle, which must be re-checked against the live
table once it disappears from the pending list.

pass: true
