# PREREG: packaging 13 cells (hsp4 x 12, spherical codes x 1)

This file has two versions. Version 2 (below, binding for the second panel) was written on 2026-11-01 at 14:36Z UTC.
Version 1 (kept unchanged at the end of this file and in git history, commit d15a6d1) was written on 2026-11-01 at
13:47Z UTC and judged the first panel.

## Version 2

written_utc: 2026-11-01T14:36Z

### Timing, stated plainly

Version 2 was written after the searches (2026-11-01, about 05:04 to 08:50 UTC) and after the first panel
(13:47Z to about 14:00Z), which dropped all 13 cells. The objects are unchanged since the first panel (same files,
same sha256). It is not a pre-registration in the strict sense: it freezes the judging, not the search. What changed
from version 1: the criteria are now quoted from the CURRENT public bank, `bank/targets.json` in a clone of
https://github.com/elder-plinius/V3R1T4S made 2026-11-01 at 14:30Z UTC (HEAD f3b19b475065f35d0a7f93e8a6078c9b2f12566e,
committed 2026-10-30T03:12:11-07:00), instead of the 2026-10-31 staged snapshot. The hsp4 criterion in the current
bank is stricter than the snapshot (it adds the posted-file non-isometry condition, the polish floor, and the
not-a-relaxed-copy clause). The spherical-codes criterion is identical in both. No threshold or margin was chosen by
us; every number below is the bank's.

### Criterion: packomania-hyperspheres-hsp4-hsp6 (12 cells)

Quoted verbatim from the current bank:

> Success means N centers in R^d (d in {4,5,6}) for one N listed in the live https://packomania.com/hsp<d>/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 (the table carries 12 decimals; 1e-10 is 200x its rounding), AND, wherever the posted hsp<d>-<N>.txt reproduces its own header radius to 1e-11, the configuration is not isometric to that posted configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere) and r* exceeds by at least 1e-9 the highest radius that the verifier's own local polishes of that posted file reach, each run until it stops improving, under several trust-region schedules, AND the configuration is not a relaxed copy of a posted packing, which is a trivial derivation however much it gains (a polish gain is an errata note for the table keeper, as in packomania-scu-spheres-in-cube since #605; the claim names any posted packing it started from), AND (d, N) does not appear in a History-of-updates entry on the live hsp<d>.html newer than the one the scout fetched. COORDINATES UNAVAILABLE (checked 2026-10-28): every hsp4 file reproduces its header radius, but the hsp5 and hsp6 rows carry 4 coordinates and hsp6 N = 251-259 have no file, so among hsp5 and hsp6 only hsp5 N = 7 and 8 can be compared or polished (see pitfalls); for every other hsp5 or hsp6 N the verdict must say 'posted coordinates unavailable', and the N must be re-checked against the posted file once Packomania posts complete coordinates. QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. No submission (email) is ever made; the claim is for the verified construction only.

Cells: hsp4 N = 136, 141, 152, 156, 160, 163, 188, 213, 214, 215, 216, 217.

### Criterion: spherical-codes-cohn-table (1 cell)

Quoted verbatim from the current bank:

> Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Cell: (d, N) = (31, 64).

### Evidence available to the second panel

Fetched by the repository owner from an unrestricted machine on 2026-11-01 at 14:32Z (this sandbox still cannot reach
these hosts), listed with sha256 in `cloud/1101/novelty/FETCHED.md`: live hsp4 radius.txt, hsp4.html,
pending-requests.html, the Moki & Julio MANIFEST.csv, the spherical-codes.org /plain and the index row for (31, 64),
and two arXiv API searches (newest 15 for "spherical code" and for Tammes). Posted hsp4 coordinates:
`cloud/1101/data/hsp4_coords.tar.gz` (sha256 b929acc815b5b4e12e4b7654af23a58483d8cb0d44af804b231203ca935163df).

### Statistic, thresholds, null design

- hsp4: r* as defined in the criterion; pass iff r* - table >= 1e-10, the configuration is not isometric to the posted
  hsp4-N.txt (sorted pairwise-distance multisets differ by more than 1e-8 somewhere), and r* exceeds by at least 1e-9
  the highest radius reached by the skeptic's own local polishes of the posted file under at least three trust-region
  schedules (largest step 1e-2, 1e-3, 1e-4), each run until it stops improving. Additionally r* must exceed the Moki &
  Julio MANIFEST value for N (prior public claim) and N must not be in a queued hsp4 range.
- spherical code: c* as defined; pass iff table - c* >= 1e-10, coordinates >= 20 digits, no star, no 'needs more
  optimization' text, no newer arXiv result for (31, 64), not in the kissing range.
- Null test: not applicable. These are deterministic constructions checked against a definition, not search or
  statistical claims.

### Starting points (for the not-a-relaxed-copy clause)

Lanes hsp4-a (N = 136..188) and hsp4-b (N = 213..217) started from random configurations, lattice cuts and shell
seeds, and (hsp4-b) from their own earlier results for N - 1 plus one inserted ball. Neither lane had Packomania's
posted coordinates; no search started from a posted file. Lane code is in `inputs/`.

### Panel

Three fresh skeptics per cell (REPRODUCE, NOVELTY, CRITERION), new subagents, none sees the search code or our
checkers. NOVELTY and CRITERION receive `cloud/1101/novelty/` and the posted coordinates and run the hsp4 clauses
themselves. A cell whose three skeptics do not all write `pass: true` is dropped.

---

## Version 1 (superseded 2026-11-01T14:36Z; kept unchanged)

written_utc: 2026-11-01T13:47Z

## Timing, stated plainly

This file was written on 2026-11-01, AFTER the searches had run (lanes hsp4-a, hsp4-b and sph-d25-32, 2026-11-01
about 05:04 to 08:50 UTC). It is not a pre-registration in the strict sense: the objects already existed when it was
written. What it freezes is the judging, not the search: each success criterion below is copied unchanged from the
bank snapshot `cloud/1031/data/targets.json` (staged 2026-10-31), and no criterion, threshold or margin was chosen or
adjusted after seeing the results.

## Criterion: packomania-hyperspheres-hsp4-hsp6 (12 cells)

Quoted verbatim from `cloud/1031/data/targets.json`:

> Success means N centers in R^d (d in {4,5,6}) for one N listed in the live https://packomania.com/hsp<d>/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 (the table carries 12 decimals; 1e-10 is 200x its rounding), AND the configuration is not isometric to the posted hsp<d>-<N>.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere), AND (d, N) does not appear in a History-of-updates entry on the live hsp<d>.html newer than the one the scout fetched. QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. No submission (email) is ever made; the claim is for the verified construction only.

Cells: hsp4 N = 136, 141, 152, 156, 160, 163, 188, 213, 214, 215, 216, 217.
Table: `cloud/1031/data/packomania.com_hsp4_txt_radius.txt`, a copy of https://packomania.com/hsp4/txt/radius.txt
fetched 2026-10-31, sha256 f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f; re-checked unchanged on
2026-11-01 by the repository owner (this session cannot reach packomania.com).

## Criterion: spherical-codes-cohn-table (1 cell)

Quoted verbatim from `cloud/1031/data/targets.json`:

> Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Cell: (d, N) = (31, 64).
Table: `cloud/1031/data/spherical-codes.org_plain`, a copy of https://spherical-codes.org/plain fetched 2026-10-31,
sha256 a2256fc2c4d7003f089adbd6e221f1ecbda048be67cc5630374686a607e4109b.

## Statistic, thresholds, null design

- hsp4: r* as defined above, exact decimal input, 50-digit square roots; pass iff r* - table >= 1e-10.
- spherical code: c* as defined above, exact inner products, 50-digit normalisation; pass iff table - c* >= 1e-10,
  coordinates >= 20 digits, not in the kissing range.
- Null test: not applicable. These are deterministic constructions checked against a definition, not search or
  statistical claims; the criterion has no statistic that a shuffled control could reproduce.

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), each seeing only the claim folder (object file, criterion,
table value and URL; NOVELTY also the claims lists and TROPHY_CASE.md). None sees the search code or the packaging
checker. A cell whose three skeptics do not all write `pass: true` is dropped.

## Known limits at freeze time (from command output in this session)

- packomania.com, spherical-codes.org and export.arxiv.org are unreachable from this sandbox (curl: CONNECT tunnel
  403; web tool: host not resolvable). The live re-fetch, the hsp4 History-of-updates and pending-requests clauses,
  the hsp4 posted-coordinate non-isometry comparison, the spherical-codes HTML index star/label clause and the arXiv
  supersession clause cannot be checked here.
- The bank in the public V3R1T4S repository (clone of 2026-10-30, commit f3b19b475065) carries a stricter hsp4
  criterion than the 2026-10-31 snapshot quoted above (posted-file polish floor; not a relaxed copy of a posted
  packing) and records a public Moki & Julio collection claiming radii above the live hsp4 table at 216 N.
  These are recorded here so the judging cannot quietly ignore them.
