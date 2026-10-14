# Novelty verdict — hsp4 N = 54

context: subagent (Claude Code Agent tool, fresh context; one context panelled 14 separate claims with one fetch per URL)

Role: NOVELTY skeptic. Question: does the candidate in hsp4-54-candidate.txt (r* = 0.276798695687107..., from CLAIM.md) strictly beat everything known for 4D hsp4, N = 54? A tie is not a record. Table-access rule honoured: each URL below was requested exactly once for the whole panel (User-Agent "V3R1T4S skeptic", no retries), saved to the panel's shared _novelty_fetch folder, and grepped from the saved copy for every N.

## Fetch 1 — live table
- URL: https://packomania.com/hsp4/txt/radius.txt
- UTC: 2026-10-14T15:31:59Z, HTTP 200, saved as radius.txt (5575 bytes, 299 rows)
- Quoted row for N = 54: `0.276798004181`
- Snapshot in hsp4_radius_as_fetched.txt (claim folder), row N = 54: `54 0.276798004181` — live row EQUALS the snapshot; the full live file is byte-identical to the snapshot (cmp).
- Candidate minus live table value: +6.915e-7 (> 1e-10, strictly beats the posted value).

## Fetch 2 — status page
- URL: https://packomania.com/hsp4/hsp4.html
- UTC: 2026-10-14T15:32:00Z, HTTP 200, saved as hsp4.html (88618 bytes)
- "Last update: 06-Jul-2025". History of updates contains exactly three entries: 04-Jul-2025 (first presentation N=2–100, E. Specht), 05-Jul-2025 (extension to N=200), 06-Jul-2025 (extension to N=300). No entry newer than 06-Jul-2025; nothing covers (4, 54) beyond the original presentation.

## Fetch 3 — pending queue
- URL: https://packomania.com/pending-requests.html
- UTC: 2026-10-14T15:32:01Z, HTTP 200, saved as pending-requests.html (page dated 08-Oct-2026)
- Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv and one "*many*". No hsp4 (or any hsp) entry; no range in any listed category applies to the hsp4 table, so N = 54 is not in a declared hsp4 queue range.
- QUEUE CAVEAT (unresolvable): "26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total" is category-unspecified. It cannot be excluded that this bundle contains hsp4 candidates, possibly for N = 54. Per the bank's queue rule the verdict must carry this caveat, and N = 54 must be re-checked against the live table once that bundle leaves the pending list.

## Fetch 4 — TROPHY_CASE
- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
- UTC: 2026-10-14T15:32:02Z, HTTP 200, saved as TROPHY_CASE.md (100 lines)
- grep -i for hsp4 / hsp / hypersphere / 4-ball / packomania: zero matches. No prior hsp4 trophy for any N.

## Fetch 5 — open pull requests
- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
- UTC: 2026-10-14T15:32:03Z, HTTP 200, saved as open_prs.json (11 open PRs)
- Only PR #127 (same contributor) touches the hsp4 table; its title and body claim N = 66 only, which is not N = 54; its body does not mention N = 54. The other ten open PRs are Thomson-problem claims (#78, #124, #125, #126), constant-weight-code claims (#8, #28) and checker fixes (#1, #9, #30, #31). No open PR matches or beats the candidate for N = 54.

## Literature search (web, 2024–2026)
- Queries: "packing equal hyperspheres in a 4-dimensional ball best known radius 2025"; "\"hyperspheres in a hypersphere\" packomania hsp4 improved packings"; "arxiv 2025 2026 densest packing of N equal balls in a 4-ball spherical container numerical optimization table"; exact-number query "\"0.315990168743\" OR \"0.258522851648\" OR \"0.268830626376\" packing"; follow-ups on two unresolved hits.
- Result: no 2024–2026 source lists best-known radii for N equal balls in a 4-ball other than Packomania's own hsp4 table, which is a first presentation by E. Specht (Jul-2025) with no external contributors in its history. The exact posted values are not found anywhere else on the web.
- Hits checked and ruled out: arXiv 2506.11682 (fetched once, 2026-10-14T15:33:20Z, HTTP 200) is about saturated hyperball packings in hyperbolic n-space — not a container problem. preprints.org 202606.0856 (direct fetch once at 15:33:21Z returned HTTP 403 bot block; identified via a later search citation as "The sphere packing problem in dimension 4", v11, on the 24-cell conjecture) concerns infinite-space lattice packing density, not N balls in a 4-ball. Stoyan & Yaskov (J. Global Optim. 2012) and Stoyan et al. (MBE 2020) treat hyperspheres in a hypersphere but are older than 24 months and give no per-N 4D radius table competing with the candidate.
- Nothing in the literature matches or beats r* = 0.276798695687107... for (4, 54).

## Verdict
Live table row for N = 54 equals the claim's snapshot (0.276798004181); the candidate exceeds it by 6.915e-7 (> 1e-10). No newer history entry covers (4, 54). No hsp4 queue range includes N = 54. TROPHY_CASE, open PRs and the literature contain nothing at or above the candidate. The only unresolved item is the category-unspecified "Moki & Julio *many* 4666 candidates" bundle (caveat above). Isometry, feasibility and the 50-digit recomputation are outside this verdict's scope (other skeptics).

pass: true
