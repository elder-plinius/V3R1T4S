# Novelty verdict, hsp4 N = 74

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Candidate (hsp4-74-candidate.txt, 74 points, recomputed here with 60-digit decimal arithmetic, no tolerance):
r* = 0.258529650660235193... (CLAIM.md states 0.258529650660235..., agrees).

## Fetches (each exactly once, User-Agent "V3R1T4S skeptic", no retries, times from date -u)

1. https://packomania.com/hsp4/txt/radius.txt
   2026-10-16 17:55:17 UTC, HTTP 200, 5575 bytes.
   Row 74: `74 0.258522851648`. File is byte-identical (cmp) to hsp4_radius_as_fetched.txt in the claim folder.
2. https://packomania.com/hsp4/hsp4.html
   2026-10-16 17:55:18 UTC, HTTP 200, 88618 bytes.
   `Last update: 06-Jul-2025`. History of updates contains only 04-Jul-2025 (N=2-100), 05-Jul-2025 (to N=200),
   06-Jul-2025 (to N=300). No entry newer than 06-Jul-2025; nothing mentions N=74. Table row in the page:
   `74 0.258522851648 ...`, consistent with radius.txt.
3. https://packomania.com/pending-requests.html
   2026-10-16 17:55:19 UTC, HTTP 200, 4954 bytes, page dated 08-Oct-2026.
   Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv. No hsp4 (or hsp5/hsp6) line at all, so no
   hsp4 range includes 74.
   Caveat: the entry `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` names no category. It
   cannot be resolved from the page; it could in principle contain an hsp4 N=74 candidate. The N must be
   re-checked against the live table once that bundle disappears from the pending list.
4. https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   2026-10-16 17:55:20 UTC, HTTP 200, 30936 bytes, 100 lines.
   grep -i for hsp4 / hypersphere / sphere / ball / packomania / "74": zero hits. The file lists six families
   (graphs, codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and does not mention the hypersphere
   family at all, so it contains no competing N=74 value.
5. INDEX.csv of the merged earlier N=74 package (family packomania-hyperspheres-hsp4-hsp6 on branch main,
   package hash 1d6ec66c, PR #132, merged 2026-10-15), fetched from raw.githubusercontent.com
   2026-10-16 17:55:20 UTC, HTTP 200, 260 bytes. Quoted row:
   `packomania-hyperspheres-hsp4-hsp6,hsp4 N=74,0.25852872389914219568,0.258522851648,2026-10-14T15:29:10Z,object/hsp4-74-candidate.txt,1d6ec66c...`
   Merged earlier value: r* = 0.25852872389914219568.
6. https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
   2026-10-16 17:55:21 UTC, HTTP 200, 53 open PRs.
   Titles and bodies grepped for hsp4/hsp5/hsp6/hypersphere/packomania/"74"/4-ball: the only Packomania PRs are
   spheres-in-cube (scu) and circles-in-circle (cci) claims; no open PR claims any hsp4 value, and none for N=74.

## Comparison

- candidate - live table = 0.258529650660235 - 0.258522851648 = 6.799e-06, which exceeds 1e-10: strictly beats the table.
- candidate - merged earlier object = 0.258529650660235 - 0.258528723899142 = 9.268e-07, positive: strictly beats
  the earlier merged N=74 object (same cell, same contributor; the present object is a different, better packing).
- No tie anywhere.

## Literature / web search (2024-2026)

Three searches (hyperspheres in a 4-ball N=74 radius 0.2585; hsp4 Packomania improved packings 2025-2026;
densest packings of equal spheres in a 4-ball N up to 300). Results: Stoyan & Yaskov 2012 (hyperspheres in a
hypersphere, no N=74 table), Stoyan et al. 2020 (MBE, general method), arXiv 2305.10023 (3D spheres in a
sphere), 24-cell conjecture / D4 lattice papers (unbounded packings), hyperbolic-space packings, random
jammed packings. No 2024-2026 source lists a packing of 74 equal balls in a 4-ball with radius above
0.258522851648. Packomania's own hsp4 page (July 2025) remains the only public table.

## Conditions

- live table value for N=74 still the snapshot value: yes (byte-identical file)
- candidate beats the table by more than 1e-10: yes (6.80e-06)
- candidate strictly beats the merged earlier object: yes (9.27e-07)
- no newer History-of-updates entry covers (4,74): confirmed
- no hsp4 queue range includes 74: confirmed (no hsp4 entry); category-unspecified 4666-candidate bundle
  of 26-Sep-2026 is an unresolvable caveat and must be re-checked when it clears
- nothing else known matches or beats it: nothing found (trophy case, open PRs, web)

pass: true
