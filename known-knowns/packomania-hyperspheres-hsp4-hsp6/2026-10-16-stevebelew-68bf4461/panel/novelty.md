# Novelty verdict: hsp4, N = 81

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Claim under review (CLAIM.md): 81 equal balls in the unit 4-ball with feasible radius r* = 0.254080381791775..., said to beat Packomania's posted hsp4 value 0.254058669351 by about 2.17e-05 and to be non-isometric to the posted packing. Object: hsp4-81-candidate.txt. Snapshot: hsp4_radius_as_fetched.txt.

Sanity recomputation (not my gate, but needed for "strictly beats"): 50-digit Decimal evaluation of hsp4-81-candidate.txt gives 81 points, r* = 0.254080381791774903..., gain over the live table value = 2.1712e-05, which is far above the 1e-10 margin.

## Live fetches (one plain request each, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: 2026-10-16T17:48:36Z, HTTP 200
   row 81: `81 0.254058669351`
   The fetched file is byte-identical (cmp) to hsp4_radius_as_fetched.txt. The snapshot value is still the live value, so the candidate strictly beats it by more than 1e-10.

2. https://packomania.com/hsp4/hsp4.html
   time: 2026-10-16T17:48:37Z, HTTP 200
   quoted: `Last update: 06-Jul-2025`
   History of updates contains only three entries: 04-Jul-2025 (first presentation N = 2-100), 05-Jul-2025 (extension to N = 200), 06-Jul-2025 (extension to N = 300). No entry newer than 06-Jul-2025, so none covers (4, 81). The table row in the page reads `81 0.254058669351 0.681176009191 3.9360987073 0.337459062243 309 3 76 5 [31]`, consistent with radius.txt.

3. https://packomania.com/pending-requests.html
   time: 2026-10-16T17:48:38Z, HTTP 200
   page dated 08-Oct-2026. Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one "*many*". No hsp4 (or hsp5/hsp6) line at all, so no hsp4 range includes 81.
   QUEUE CAVEAT (cannot be resolved): the entry `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` is category-unspecified. It may or may not contain hsp4 candidates, including N = 81. Per the bank's queue rule, N = 81 must be re-checked against the live radius.txt once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: 2026-10-16T17:48:39Z, HTTP 200
   grep -i for "hsp4", "hypersphere", and whole-word "81": no hsp4 or hypersphere entry. The only "81" hit is in an unrelated degree-diameter row ("exceeds table entry 1 539 ... by +81"). No trophy for (4, 81).

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: 2026-10-16T17:48:40Z, HTTP 200
   52 open PRs. None has target packomania-hyperspheres-hsp4-hsp6. Title/body grep for "hsp4", "hypersphere", whole-word "81": PR 231 (spherical-codes-cohn-table, (6, 526)) mentions "hypersphere" only in a cited paper title; PR 218 (fmm-additive-complexity) has "U 81" as an unrelated count. Open Packomania PRs are scu (spheres in a cube, N = 882-886, 83, 507) and cci (N = 4141) only. No open PR matches or beats this (4, 81) candidate.

6. https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
   time: 2026-10-16T17:48:41Z, HTTP 200
   12 subdirectories (hash-named, dated 2026-10-14). To confirm which N they hold without further per-directory requests I fetched the repo tree once:
   https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 (time: 2026-10-16T17:49:15Z, HTTP 200, truncated: false). File names under that family resolve to exactly (4, N) for N in {30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75}. N = 81 is not among them. No other hsp4/hypersphere path exists in the repo besides the bank entry known-unknowns/packings-physics/packomania-hyperspheres-hsp4-hsp6.md.

## Literature search (web, 2024-2026)

- "packing 81 equal spheres in a 4-dimensional ball hypersphere packing radius best known 2025 2026": only 3D spheres-in-sphere material (arXiv 2305.10023, OEIS A084828/A084829), unreviewed 2026 preprints about the D4 lattice density (infinite-space, not finite-N), nothing on N = 81 in a 4-ball.
- "packomania hsp4 hyperspheres in a 4-ball improved packings arXiv": hyperbolic-space hyperball packings (arXiv 2506.11682, 1401.6084), the 2020 MBE paper on hypersphere packing heuristics citing Packomania as benchmark, the Packomania index itself (hsp4 page last updated July 2025). No source reports a (4, 81) radius.
- Exact-value search for "0.254058669351" or "0.25408038": no page anywhere carries either number.
Nothing in the literature found lists a packing of 81 equal balls in a 4-ball with radius at or above the candidate value. The posted Packomania value (E. Specht, program hsp4, 2010-2025) remains the only known reference point and the candidate strictly exceeds it.

## Conclusion

- Live table value for N = 81 unchanged at 0.254058669351 (byte-identical radius.txt); candidate r* exceeds it by 2.17e-05 (well over 1e-10). Not a tie.
- No History-of-updates entry newer than 06-Jul-2025; none covers (4, 81).
- No hsp4 range on the pending-requests page; the category-unspecified "Moki & Julio *many* 4666 candidates" bundle (26-Sep-2026) is an unresolvable caveat and the value must be re-checked once that bundle clears.
- TROPHY_CASE.md, the merged hsp family (N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75) and the 52 open PRs contain nothing for (4, 81).
- Web literature search found nothing matching or beating the candidate.

pass: true
