# Heptiamonds M and X: no common figure with k = 2..20 tiles inside the stated boards (bounded UNSAT, DRAT-checked), bank target polyform-compatibility-open-pairs, partial win p3

> Partial win p3 only ("a computer-certified impossibility ... up to a stated figure size for a '?' pair,
> clearly labelled as bounded"). This is NOT a proof that M and X are incompatible: a common figure that does not
> fit inside the stated board for its k, or that needs more than 20 tiles of each kind, is not ruled out.
> The main criterion and partial wins p1 and p2 are not claimed.

## What
Status: CONFIRMED_PARTIAL (partial win p3) per panel/gate.md; panel passed 3/3 (panel/reproduce.md,
panel/novelty.md, panel/criterion.md). Zenodo record 10.5281/zenodo.24518087 was published 2026-11-25T00:44:38Z and
verified (archive size, sha256 and all 38 members; the-record-we-beat/ARCHIVE.md).

For heptiamonds M and X (Ishino names as on George Sicherman's Heptiamond Compatibility page, where the unrestricted M-X cell is '?'), for each k = 2..20 the joint cover CNF on the triangular-lattice board of board_rows = max(6, ceil(2*sqrt(7k))) + 2 rows by board_rows + 2 triangles listed per k in object/mx_k2_20_bounded_unsat.json (10x12 at k=2 up to 26x28 at k=19 and 20) is unsatisfiable, with CaDiCaL 3.0.1 reporting UNSAT and drat-trim reporting s VERIFIED on its DRAT proof (archived as heptiamond-MX-k2-20-proofs.tar.xz, 175028808 bytes, sha256 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be, at https://doi.org/10.5281/zenodo.24518087), so no figure of area 7k inside that board (connected or not, with or without holes) can be tiled both by k copies of M and by k copies of X; for k = 2..5 an independent board-free exhaustive search also finds no common figure; nothing is claimed for figures outside the stated boards, for k > 20, or about incompatibility of M and X.

In plain words: two heptiamonds (shapes made of 7 equilateral triangles) are "compatible" if one figure can be
tiled by copies of either. For the pair M and X nobody has found such a figure, and Sicherman's table shows `?`.
For each tile count k from 2 to 20, a SAT encoding asks: is there a set F of 7k triangles inside a fixed board,
together with an exact tiling of F by k copies of M and an exact tiling of F by k copies of X (any rotation or
reflection)? The SAT solver CaDiCaL 3.0.1 answered "unsatisfiable" for all 19 values of k and wrote a DRAT proof of
each answer, and the independent proof checker drat-trim accepted every proof. The per-k labels (copied from the
run's summary.json) are, for example, `bounded UNSAT: no figure with k=20 tiles (area 140) inside a 26x28 board
(disconnected figures also forbidden by model coverage); table=unrestricted`. The board grows with k: it is
`max(6, ceil(2*sqrt(7k))) + 2` rows of that number plus 2 triangles each, so a k=20 figure must fit in 26 rows of
28 triangles (about 14 by 22.5 triangle edges). The proofs (about 1 GB of DRAT files, plus the 19 CNF files) are
too large for git; they are archived as one file:

| file | bytes | sha256 | public archive |
|---|---|---|---|
| heptiamond-MX-k2-20-proofs.tar.xz | 175028808 | 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be | https://doi.org/10.5281/zenodo.24518087 |

The archive holds the 38 files listed, each with its sha256, in object/SHA256SUMS-files.txt (problem.cnf and
proof.drat for each k). Zenodo record status: published 2026-11-25T00:44:38Z (open access, CC BY 4.0). A full download at
2026-11-25T00:45:17Z gave 175028808 bytes and the sha256 above, and all 38 archive members matched
object/SHA256SUMS-files.txt (the-record-we-beat/ARCHIVE.md).

Box reproduction (packaging machine, not the contributor's PC): the run's own CNF generator, re-run from
how-we-built-it/code/, rebuilt all 19 problem.cnf files byte for byte (sha256 equal to the PC list), and
CaDiCaL 3.0.1 built from the same sources re-solved k = 2..20, producing proof.drat files whose sha256 equal the PC
list, each accepted by drat-trim (how-we-built-it/box-reproduction/).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh and python3 3.8+, standard library only, no
network). Expected last line: `PASS`. About 5 to 10 seconds on a laptop. It checks the object's internal
consistency (k = 2..20, board formula, labels, the 38 sha256 lines, the archive hash), rebuilds M and X from their
definition in its own coordinates (and checks there are exactly 24 free heptiamonds and X is the only one with 3-fold
rotational symmetry and no mirror), recounts the placements of M and X inside every board, runs a positive and a
negative control (M-B, listed 2 on the page, has a common 2-tile figure; M-C, listed 6, has none), and then
searches with no board at all for a common figure with k = 2..4 tiles (none). It does not re-run the SAT solver or
drat-trim; RUN_IT_YOURSELF.md says how to download the archive and check every proof (about 1 GB unpacked DRAT,
a few minutes per k).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Sicherman, Heptiamond Compatibility, Minimal Solutions (unrestricted) | M-X | `?` | https://sicherman.net/7mond/7compat.html | 2026-11-25T00:18:18Z, re-fetched 2026-11-25T00:46:46Z |
| Sicherman, Heptiamond Compatibility, Holeless Variants | M-X | `?` | https://sicherman.net/7mond/7compat.html | 2026-11-25T00:18:18Z, re-fetched 2026-11-25T00:46:46Z |
| Friedman, Math Magic, September 2004 | (no heptiamond pairs) | n/a | https://erich-friedman.github.io/mathmagic/0904.html | 2026-11-25T00:18:20Z |

The page says "Last revised 2012-01-04" and its sha256 is unchanged from the copy the run used (2026-11-03). No
`×` appears anywhere on it. Details, headers and the other pages read: the-record-we-beat/RECORD.md.

## Not claimed
- That M and X are incompatible. A common figure may exist with more than 20 tiles of each kind, or with k <= 20
  but not fitting inside the stated board for that k. Only k = 2..5 are ruled out without a board limit (independent search, not SAT).
- Partial win p1 (a figure for a '?' cell), p2 (a smaller figure for a listed minimum of 10 or more), or the main
  criterion. No figure was found.
- Anything about the holeless table beyond what follows from the unrestricted result.
- Any other pair. The contributor's run covered all 21 unrestricted '?' pairs; each would be its own package.
- Any edit to Sicherman's page.

## Credits
- George Sicherman, Polyform Curiosities, Heptiamond Compatibility (the table and the pair names): https://sicherman.net/7mond/7compat.html and https://sicherman.net/pairwise.html
- K. Ishino, the heptiamond letter names (K. Ishino's Heptiamonds Page) Sicherman adopts (archived via https://web.archive.org/web/20110807154834/http://www.puzzlewillbeplayed.com/000/Ishino/).
- Erich Friedman, Math Magic, September 2004: https://erich-friedman.github.io/mathmagic/0904.html
- Giovanni Resta, Polypolyominoes (checked as the bank asks; covers polyominoes).
- Armin Biere and the CaDiCaL authors, CaDiCaL 3.0.1: https://github.com/arminbiere/cadical
- Marijn Heule, Nathan Wetzler and Warren Hunt, drat-trim: https://github.com/marijnheule/drat-trim
- Zenodo (CERN) for the proof archive: https://doi.org/10.5281/zenodo.24518087
- Contributor: whosedreams (V3R1T4S kit). Search run on the contributor's PC (AMD Ryzen 9 9900X, WSL2).
