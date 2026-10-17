# Packomania cci, N = 4141: a certified better construction (partial win p2)

Submission id: 2026-10-16-nukewire-3dcf2cc2 · target: packomania-cci-equal-circles-in-circle ·
claim level: partial_win_claim (p2), one table cell.

## What

confirmed_scope: For the single Packomania cci table cell N = 4141 (live row fetched 2026-10-16,
value 0.014601755763187308074373236782), the 4141 container-centred centres in candidate_N4141.txt —
a non-isometric pure triangular-lattice construction with max|c| = 0.9853905285512 — give feasible
radius r* = 0.0146094714488139345759856245307 computed exactly from the submitted 18-decimal strings
(independently reproduced at Decimal 70 and mpmath dps 50), which exceeds that live table value by
7.7157e-6 (>= 1e-11), thereby satisfying partial win p2 for one listed gap value N > 2600 whose
record (reference "program cci", Specht) is a lattice-like seed rather than an optimized packing —
subject to the mandatory caveat that the category-unspecified 26-Sep-2026 "Moki & Julio *many*"
4666-candidate bundle remains on the pending list and N = 4141 must be re-checked against the live
table once it disappears.

## Check it yourself

One command, standard library only (Python 3.8+), about 2 minutes on a laptop:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (it verifies the object's sha256 and count, recomputes r* at 60
significant digits from the coordinate strings, and checks the margin over the recorded table
value; its real output is in verify-it-yourself/RECEIPTS.md).

## Compared to

Packomania, "The best known packings of equal circles in a circle" (cci), cell N = 4141:
https://packomania.com/cci/cci.html — machine-readable table
https://packomania.com/cci/txt/radius.txt fetched 2026-10-16T09:46:29Z (HTTP 200, sha256
6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead), row 4141 =
0.014601755763187308074373236782. The row cites the site's own construction program ("program
cci, 1999-2024"); the posted configuration for this cell reproduces its table value (integrity
clean) and is not isometric to ours (sorted distance multisets differ). Snapshot details in
the-record-we-beat/.

## Not claimed

- Not a record for any other N (a second candidate, N = 3307, margin +4.4e-6, was found in the
  same sweep but is NOT claimed here: one table cell per claim).
- Not proven optimal for N = 4141 (only N <= 13 and N = 19 have proofs in this table).
- Not a density or asymptotic result of any kind.
- No submission was made to Packomania (no email; the claim is the verified construction only).
- The queue-rule caveat above: the category-unspecified pending bundle is unresolved as of the
  fetch date; the cell must be re-checked when that bundle clears.

## Packaging note

The submission id retains the sha256-8 prefix (3dcf2cc2) of the object file as first assembled
on Windows (CRLF line endings). The repository stores LF-normalized bytes; every hash in this
package (SHA256SUMS, INDEX.csv, verify-it-yourself/check.py) refers to those committed LF bytes
(object sha256 b5cc9aef50c8aac1bdfa51107f030ca3f7e2ddf0f1483eb0c9336ee91095039e), so checks
pass on any fresh checkout. verify-it-yourself/check.py additionally accepts the CRLF-materialised
form of the object (a core.autocrlf=true checkout), so its integrity check passes on both.

## Credits

- Eckard Specht's Packomania (https://packomania.com) — the cci table, the radius data and the
  posted configuration this result improves on.
- The V3R1T4S open notebook (https://github.com/elder-plinius/V3R1T4S) — the bank entry that
  defines the success criterion, the run protocol, and the three-skeptic panel process.
- W. Sander, "LLM-Guided Program Evolution for Circle Packing" (arXiv:2609.05093, 2026) — checked
  for overlap; its 10 records are in the csqv category (variable radii, unit square), not cci.
- Construction method: plain triangular-lattice window with optimal orientation/offset/spacing
  (closed form s* = 2/(1 + 2 rho_N)); see how-we-built-it/.
