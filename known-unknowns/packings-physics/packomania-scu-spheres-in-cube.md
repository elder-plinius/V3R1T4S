# Packomania: equal spheres in a cube (scu), beat a per-N record radius

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Packomania's 'spheres in a cube' table (scu) lists the best known radius r(N) of N equal spheres in the unit cube, complete for N = 1..1000 plus lattice rows up to N = 1024192 (1134 rows; since the 17-Oct-2026 reorganisation txt/radius.txt gives 12 decimals for 1058 rows and 30 for 76; per-N coordinates scu/txt/scu<N>.txt). Proven only for N <= 10 and a few more. The table is being revised right now: 04-Oct-2026 Specht posted 2022 Lai-Hao-Xiao-Glover candidates for ~60 values of N and wrote 'This table needs a revision!'; 05-Oct-2026 Yuan Gao (Harvard) set ~80 records in 202..576; 06-Oct and 08-Oct-2026 Lu Peng set ~185 records across 102..946; 17-Oct-2026 Lu Peng continued (N in 95..883), Vidit Patankar set records for 40 values of N from 101 to 1596, and the table was reorganized. Author file (2026-10-20): Lu Peng 321 rows, Goldberg (1971) 262, Cantrell 231, Specht 173, Vidit Patankar 40, Lai-Hao-Xiao-Glover 39, so hundreds of rows are still 1970s-2012 constructions. scu is NOT in the pending-requests list of 17-Oct-2026, and the 'many: 4666 candidates' bundle from Moki & Julio of 26-Sep-2026 matches their public release v2.2, which has no scu table (see pitfalls).

## What counts as a win

Success means N centers in R^3 for one N listed in https://packomania.com/scu/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ) for the cube [-1/2, 1/2]^3, computed in mpmath at 50 digits with no tolerance, is STRICTLY GREATER (direction: max) than the live txt/radius.txt value (12 or 30 decimals depending on the row since 17-Oct-2026) for that N re-fetched immediately before claiming, by at least 1e-11, AND the configuration is not isometric to the posted scu<N>.txt configuration (sorted distance multisets differ), AND N does not appear in a History-of-updates line on the live scu.html newer than the one the scout fetched (the table was rewritten on 04, 05, 06, 08 and 17 Oct 2026 from private communications outside the public queue, so a same-day re-fetch is mandatory). QUEUE RULE (Packomania, checked 2026-10-20): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. Packomania coordinate files are CENTERED (container centre at the origin: circle/sphere radius 1, square side 1 in [-1/2,1/2]^2, cube edge 1 in [-1/2,1/2]^3). No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- **p1:** A certified improvement (same rule) for an N whose live author (txt/author.txt) is 'Michael Goldberg' or 'Hugo Pfoertner' or 'Dave Boll' (pre-2000 hand constructions), i.e. a row nobody has optimized by computer; counted as a record if it passes the criterion, else as a near-miss with r* within 1e-6.
- **p2:** A certified improvement to the sibling 'spheres in a sphere' table (ssp, last update 26-Sep-2024, 1156 rows, 12-decimal txt/radius.txt) using the same mpmath feasible-radius rule against https://packomania.com/ssp/txt/radius.txt (container radius 1), margin 1e-10 because that file has only 12 decimals, same queue rule for category ssp.
- **p3:** Reproduction milestone: re-derive from scu<N>.txt the table radius (12 or 30 decimals) for all N <= 1000 and report any N where the posted coordinates do NOT achieve the posted radius (a data-integrity finding, which Deeter-style audits have found in other tables).

## How a win is checked

Checker (< 2 minutes): curl https://packomania.com/scu/txt/radius.txt live; load the claimed N centers; mpmath mp.dps=50; r* = min(half minimum pairwise distance, 1/2 - max_i max(|x_i|,|y_i|,|z_i|)); assert r* - r_table >= 1e-11. Download scu/txt/scu<N>.txt, recompute its r (must reproduce the table to 1e-20; parser sanity) and compare sorted distance multisets. Re-fetch scu.html History of updates and pending-requests.html and apply the queue rule. Report r* to 25 digits and the contact graph.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://packomania.com/scu/scu.html>

## Sources

- <https://packomania.com/scu/scu.html>
- <https://packomania.com/scu/txt/radius.txt>
- <https://packomania.com/scu/txt/author.txt>
- <https://packomania.com/scu/txt/scu100.txt>
- <https://packomania.com/scu/txt/scu_coords.tar.gz>
- <https://packomania.com/pending-requests.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Read txt/author.txt live and attack only rows still attributed to Goldberg/Pfoertner/Boll/Schaer (hundreds of N in 100..1000): these are decades-old constructions and the Oct-2026 waves by Gao and Peng show large gains are still routine there.
- Lattice-cut plus relax: cut fcc/hcp/bcc and 'layered square' lattices by the cube at many orientations and offsets, pick the best N-subsets, then inflate with an event-driven (Lubachevsky-Stillinger) compression and polish the active contacts with mpmath Newton.
- Peng/Gao ran N = 102..946; try the complementary N they did not touch (check the History of updates lists) and the rows between record clusters.
- Monotonic basin-hopping with a smooth overlap penalty; perturbation = remove the 3-5 'loosest' spheres (txt/loose.txt gives rattler counts) and re-insert at the largest cavities found by a Delaunay-based hole search.
- Rows N = 385..395 (and other runs) share one identical radius with ref [24]: they are a larger packing with spheres removed, so any genuine optimization of the smaller N beats them.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The table is being rewritten daily (04-08 Oct 2026). A value fetched by the scout at 04:20 can be beaten by Packomania's own update before the verifier runs; re-fetch radius.txt immediately before claiming.
- Cube convention: coordinates are centered (edge length 1, [-1/2, 1/2]^3); testing against [0,1]^3 produces false protrusion or false feasibility.
- Noise in the 30th decimal is not a record; the 1e-11 margin on the mpmath feasible radius is mandatory.
- The 'many' bundle (4666 candidates, Moki & Julio, 26-Sep-2026) matches their public release v2.2 (github.com/Hashirama1337s/moki-julio-circle-packing, commit 855d8f6838e9, 2026-09-25T22:41Z, '4,666 records in 15 tables', all 2-D: crt, ccq, cpd, cpt, crc_100 to crc_800, csc, csq, cxd); spheres in a cube enter that repo only at v2.3 (commit ea2a2e66d21c, 2026-09-26T01:29Z). The count and the timing agree, but the queued zip is not public, so the novelty skeptic must still check pending-requests.html and the per-N page, and compare a claim with their later public scu records (455 N at commit fd6316dd, 2026-10-18; none of them in v2.2) (checked 2026-10-19).
- Email submission requires explicit permission from the human and is asked to pause in October 2026.
- Count the centre rows before trusting a coordinate file. The 17-Oct-2026 exports listed N-1 centres: scu_coords.tar.gz 6c15d5db... (N-1 rows in all 1000 files with N <= 1000, per the maintainer's note on PR #311) and ed1760a3...57c7 (Last-Modified 17 Oct 2026 19:37 GMT), in which every scu<N>.txt for N <= 1000 and 58 of the 134 lattice files leave the row for index N empty while rows 1..N-1 hold the centres that the next export lists as 2..N. The export of 18 Oct 2026 09:05 GMT (sha256 909f98ca...a4d0, radius.txt unchanged 2e2af491...1791, seen 2026-10-18 21:53Z) lists all N centres in all 1000 files with N <= 1000 and in those 58 lattice files; the 76 largest lattice files (N >= 70304) hold only the radius. An N-1 subset still reaches the table radius (998 of 998 files in ed1760a3 within 1e-9; the complete files within 1.5e-12), so a radius match does not show that a file is complete, and the non-isometry clause needs all N centres. Per-N files can change bytes under an unchanged Last-Modified (txt/scu100.txt was fd927c05... at 07:21Z and 4b7ff475... at 21:53Z on 18 Oct, both dated 15 Oct 2026 18:41 GMT), so compare sha256, not dates.
- Free cells (2026-10-20): 26 rows, N in 209..807, lie below the row of a larger N by at least 1e-11, among them N = 727..733 below the 17-Oct-2026 N = 734 row (by up to 4.13e-4), N = 738 and 739 below 741, N = 743..746 below 747 and N = 806 and 807 below 808; no scu range is queued. Deleting balls from the posted N' file gives such an N the N' radius with no search (N = 733 from scu734.txt: r* = 0.0589436758646 against the row 0.058531064607), which meets the numeric part of this criterion. Compare a claim with B(N) = max over listed N' >= N of r(N') (kit/propagated_bar.py, PR #573) and report the margin over B(N): #526 and #527 beat B(N) by 7.7e-8 and 5.1e-7. In ssp (partial win p2) 25 rows, N in 917..100000, are free in the same sense (margin 1e-10, largest gap 7.86e-4 at N = 30000 below 30093), all inside the 15-Oct-2026 Vidit Patankar ssp range on pending-requests.html.
- Public packings outside the table (checked 2026-10-21): Vidit Patankar's release v1.1 of github.com/vidigoat/optimization-records (published 2026-10-18T05:54:31Z, asset packings-round2.zip, sha256 4d5f70542d8ce68f016c2bf3eed13127f7a6feec1141d90a125c6b33b564f091) holds scu packings for N = 209, 340, 458, 508, 512, 516, 517, 519-521, 727-733, 738, 739, 743-746, 796, 806 and 807, i.e. 25 of the 26 free cells. Each lies above the live row and the deletion bar (floating-point check for all 26; exact for N = 516, 521, 733, 739, 745 and 806, e.g. 733: 0.058947755877729602, 739: 0.058630658894405385). The repository tree's packomania/SUMMARY.tsv covers only release v1.0, so the release asset has to be read separately. Closed PR #264 holds an 806-centre packing with exact r* = 0.057020808306465647: the posted scu805 plus one sphere, closed by the maintainer as a trivial derivation, but public. A novelty check for any of these N must include both sources.
- Rows set in October 2026 carry 12 decimals, while the margin is 1e-11. A local polish of a posted 12-decimal file can clear the margin with no new structure: 120 s of sequential-LP polishing of the posted scu734.txt gives exact r* = 0.05894367596473648607, 9.9e-11 above its row. Compare a claim with the posted file after the same kind of local polish (or use a 1e-10 margin for 12-decimal rows), not only with the printed row.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/packomania-scu-spheres-in-cube.md
```

Already set up? Say `run V3R1T4S on packomania-scu-spheres-in-cube`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `packomania-scu-spheres-in-cube`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
