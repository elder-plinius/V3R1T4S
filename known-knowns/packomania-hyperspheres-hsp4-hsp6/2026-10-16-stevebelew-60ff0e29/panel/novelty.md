# Novelty verdict, hsp4 N = 91

context: subagent (Claude Code Agent tool, fresh context for this one claim)
role: novelty skeptic (one of three). Scope: CLAIM.md and the four companion files in the claim folder, plus the public fetches listed below. Nothing else on the machine was read.

Candidate: hsp4-91-candidate.txt, 91 centres in the unit 4-ball. Recomputed here with Python Decimal at 50 digits directly from the file (no tolerance): feasible r* = 0.24699818287380882063..., which agrees with the value stated in CLAIM.md. Margin over the posted 12-decimal value is 3.728e-05, far above the 1e-10 threshold.

## Fetches (each URL requested exactly once, plain curl, User-Agent "V3R1T4S skeptic", no retries)

1. https://packomania.com/hsp4/txt/radius.txt
   time: Fri Oct 16 17:48:29 UTC 2026 (started), 17:48:30 UTC (done)
   HTTP 200, 299 rows
   row 91 (file line 90): "91 0.246960900415"
   cmp against hsp4_radius_as_fetched.txt in the claim folder: IDENTICAL (byte for byte). The live table still carries the snapshot value.

2. https://packomania.com/hsp4/hsp4.html
   time: Fri Oct 16 17:48:37 UTC 2026 (started), 17:48:38 UTC (done)
   HTTP 200
   "Last update: 06-Jul-2025" (page heading line 38; footer also dated 06-Jul-2025)
   History of updates, complete: 04-Jul-2025 first presentation N=2-100; 05-Jul-2025 extension to N=200; 06-Jul-2025 extension to N=300. No entry newer than 06-Jul-2025, so none mentions N=91.
   Table row for N=91 on the page: radius 0.246960900415, reference [31] (Specht's own program hsp4).

3. https://packomania.com/pending-requests.html
   time: Fri Oct 16 17:48:49 UTC 2026 (started), 17:48:50 UTC (done)
   HTTP 200, page dated 08-Oct-2026
   grep for "hsp" (case-insensitive): zero hits. No hsp4 (or hsp5/hsp6) entry exists, so no hsp4 range includes 91. Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv.
   Queue caveat: entry "26-Sep-2026 01:11  Moki & Julio *many* 4666 candidates total" names no category and no N range. It cannot be resolved from the page; it is possible (though nothing suggests it) that it contains hsp4 candidates including N=91. Per the bank entry, this N must be re-checked against the live radius.txt once that bundle disappears from the pending list.

4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   time: Fri Oct 16 17:48:56 UTC 2026
   HTTP 200, 100 lines (header says six result families, dated 2026-10-10/12)
   grep -i "hsp4|hsp[0-9]|hypersphere": zero hits. grep "packomania|ball|sphere": zero hits. grep for standalone "91": zero hits. The trophy case does not list this target at all.

5. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   time: Fri Oct 16 17:49:10 UTC 2026 (started), 17:49:11 UTC (done)
   HTTP 200, 52 open PRs returned (fewer than the page size, so the list is complete)
   No open PR targets packomania-hyperspheres-hsp4-hsp6, hsp4, or (4, 91). Packomania-related open PRs are scu spheres-in-cube (N=882, 883, 884, 886, and two p3 coordinate-mismatch claims for N=83, 507), cci N=4141, and spherical-codes-cohn-table (6, 526). None is the same target or N.

6. https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
   time: Fri Oct 16 17:49:21 UTC 2026
   HTTP 200, 12 subdirectories (all dated 2026-10-14)
   Because the directory names do not reveal N, one additional request was made:
   https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
   time: Fri Oct 16 17:49:34 UTC 2026 (started), 17:49:36 UTC (done), HTTP 200, truncated: false
   312 paths under the family; (d, N) pairs present in file names: (4,30), (4,35), (4,42), (4,48), (4,54), (4,62), (4,63), (4,64), (4,66), (4,69), (4,74), (4,75). Exactly the twelve values expected; no 91 anywhere in the family.

## Literature search (web, last 24 months)

Three searches: "packing 91 equal hyperspheres in a 4-dimensional ball best known radius 2025 2026"; "hsp4 packomania hyperspheres 4-ball improved packings arXiv"; "equal spheres in a 4-dimensional ball container packing new records 2025 arXiv dense packings hypersphere".
Returned: Packomania itself; OEIS A084826/A084828/A084829 (3-D sphere-in-sphere only); Zhou et al. arXiv:2305.10023 (equal spheres in a sphere, 3-D); Huang and Yu arXiv:1202.4149 (3-D, 2012); Stoyan/Yaskov hyperspheres-in-hypersphere papers (2012 and earlier, small N benchmark instances, not a public table of records); Mackay 1980 and Sloane's dim-4 spherical codes (cited on hsp4.html, they feed only N up to about 55 via the "N-1 on the surface plus one centre" construction); unrelated hyperbolic-space and infinite-lattice (D4 density) items. No 2024-2026 source publishes a best-known packing of 91 equal balls in a 4-ball, let alone one at or above 0.246960900415. Packomania's own hsp4 table, which cites only its own program for N=91, is the sole public record for this cell.

## Assessment

- Live table value for N=91 is unchanged from the snapshot (0.246960900415); the candidate's recomputed r* exceeds it by 3.73e-05, well over 1e-10.
- No History-of-updates entry newer than 06-Jul-2025 exists, so none covers (4, 91).
- No hsp4 range on the pending-requests page; the only unresolvable item is the category-unspecified Moki and Julio 4666-candidate bundle (26-Sep-2026), which must be re-checked when it leaves the queue.
- TROPHY_CASE.md, the merged known-knowns family (12 values, none 91), the 52 open PRs, and the literature contain nothing that matches or beats the candidate.
- Isometry versus the posted packing and the 50-digit certification are the other skeptics' remit; the margin alone (3.7e-05 against a table rounded at 1e-12) already rules out a tie.

Result strictly beats everything known, subject to the stated queue caveat.

pass: true
