# Novelty verdict: hsp4, N = 80

context: subagent (Claude Code Agent tool, fresh context for this one claim)
role: novelty skeptic (one of three). Scope: is the candidate strictly better than everything known, and is (4,80) free of any pending/queued/merged/open-PR claim.

Claim under test (claim/CLAIM.md): r* = 0.255469606984850... for 80 equal balls in the unit 4-ball, vs Packomania hsp4 row "80 0.255463163131".

## Live fetches (each exactly once, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: Fri Oct 16 17:55:18 UTC 2026 (date -u), HTTP 200, 299 rows
   row 80 quoted verbatim: `80 0.255463163131`
   The file is byte-identical (MD5 deb4cbcd0a0131989fbf6d1adf1e85f9) to the snapshot hsp4_radius_as_fetched.txt in the claim folder.

2. https://packomania.com/hsp4/hsp4.html
   time: Fri Oct 16 17:55:18 UTC 2026, HTTP 200
   quoted: `Last update: 06-Jul-2025`
   History of updates (complete, all entries): 04-Jul-2025 first presentation N=2-100; 05-Jul-2025 extension to N=200; 06-Jul-2025 extension to N=300. The only date tokens anywhere on the page are 04/05/06-Jul-2025. No entry newer than 06-Jul-2025; nothing mentions N=80.

3. https://packomania.com/pending-requests.html
   time: Fri Oct 16 17:55:20 UTC 2026, HTTP 200, page dated 08-Oct-2026
   No row with category hsp4 (nor hsp5/hsp6). Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one row with category "*many*". So no hsp4 range includes 80.
   QUEUE CAVEAT (cannot be resolved): row `26-Sep-2026 01:11 Moki & Julio *many* 4666 candidates total` names no category. It could in principle contain an hsp4 N=80 candidate. Per the bank rule, N=80 must be re-checked against the live table once that bundle leaves the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: Fri Oct 16 17:55:20 UTC 2026, HTTP 200, 100 lines
   grep -i for hsp4 / hypersphere / word "80": no matches. The fetched file's git blob sha (61bbe687...) equals the TROPHY_CASE.md blob in the main tree fetched below, so this is the current main copy. Note: TROPHY_CASE.md does not yet list the packomania-hyperspheres family at all (it lists six other families); the family exists only as folders in the tree.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: Fri Oct 16 17:55:21 UTC 2026, HTTP 200, 53 open PRs
   PRs mentioning packomania/hsp/hypersphere/ball: 8, all other targets (packomania-scu-spheres-in-cube N=882/883/884/886 and N=83/507, packomania-cci N=4141, spherical-codes (6,526)). None targets packomania-hyperspheres-hsp4-hsp6, none mentions hsp4 or N=80 in that category. (The only "80" hit among open PRs is "77/80 VSX periods" in an unrelated astronomy claim.)

6. https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
   time: Fri Oct 16 17:55:22 UTC 2026, HTTP 200, tree not truncated, root sha ab114dcb...
   known-knowns/packomania-hyperspheres-hsp4-hsp6/ holds twelve 2026-10-14 claim folders. hsp4 N values present in file names: 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75. No path in the repo contains N=80 for this family. Confirms the merged family does not cover (4,80).

## Literature search (last 24 months)

Three web searches (16 Oct 2026): "packing 80 equal hyperspheres in a 4-dimensional ball best known radius 2025 2026"; "hyperspheres packing in a 4-ball Packomania hsp4 improved packings arXiv 2025 2026"; "equal spheres / hyperspheres in a sphere four-dimensional packing records N=80 table radius 0.2554".
Returned: Packomania itself (hsp4 category, last update 06-Jul-2025); Zhou et al. arXiv 2305.10023 (3-D spheres in a sphere, 2023); Stoyan & Yaskov (JOGO 2012; MBE 2020) on hyperspheres in a hypersphere (methods, pre-2024); Pfoertner / OEIS A084824-A084829 and Wikipedia "Sphere packing in a sphere" (all 3-D); hyperbolic hyperball packings (Yahya & Szirmai 2025, irrelevant); Boroczky four-ball note (3-D). No 2024-2026 source lists a radius for 80 equal balls in a 4-ball at all, let alone one at or above 0.255463163131. The only known value for (4,80) is Packomania's 0.255463163131.

## Comparison

Independent recompute from hsp4-80-candidate.txt (exact rationals for squared distances, 50-digit decimal square roots; mpmath not available in this shell): 80 points, r* = 0.25546960698484976114... (boundary term is the binding one; half-min-distance is 0.25546960699912). Posted file hsp4-80-posted.txt recomputes to 0.25546316313059780..., matching the table row within 4.1e-13 (parser sanity). Gain over the live row = 6.4438e-06, which exceeds the 1e-10 margin by more than four orders of magnitude. Strict improvement, not a tie. Isometry vs the posted packing is the other skeptics' domain; not checked here.

## Verdict

All conditions required for a novelty pass hold at fetch time: live table row for N=80 unchanged (0.255463163131), candidate strictly beats it by 6.44e-06 > 1e-10; no History-of-updates entry newer than 06-Jul-2025; no hsp4 range on the pending list; nothing in the literature, TROPHY_CASE.md, the merged known-knowns family (N = 30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75) or the 53 open PRs matches or beats the candidate for (4,80).
Standing caveat: the category-unspecified 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle cannot be resolved; re-check (4,80) against the live table once it disappears from the pending list.

pass: true
