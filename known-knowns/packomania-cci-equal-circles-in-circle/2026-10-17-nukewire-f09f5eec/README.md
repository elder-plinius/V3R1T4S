# Packomania cci, N = 3307: a certified better construction (partial win p2)

Submission id: 2026-10-17-nukewire-f09f5eec · target: packomania-cci-equal-circles-in-circle ·
claim level: partial_win_claim (p2), one table cell. Sibling claim: cell N=4141 (PR #234) —
a different cell, found by the same sweep.

## What

confirmed_scope: For the single cell N = 3307 of the Packomania circles-in-a-circle equal-circles table (row "3307 0.016314899796158766989004378524" of the live radius.txt fetched 2026-10-17T09:45:15Z and re-fetched unchanged by this skeptic on 2026-10-17), the submitted 3307-centre container-centred configuration (sha256 f09f5eecbb7b14f10607e97c3a74829129931cc0e0285e4372a5b4c4f61b0194) has feasible radius r* = 0.0163193001009681407709767792724368962804100804902253419885095 computed at 60 decimal digits directly from the coordinate strings, exceeding that live table value by 4.4003048093738e-6 (>= 1e-11) and non-isometric to the posted lattice-like configuration — a certified improvement meeting partial win p2 for a listed gap row N > 2600, for this one cell only, subject to the mandatory caveat that the category-unspecified 26-Sep-2026 "Moki & Julio *many*" 4666-candidate bundle is still on the pending-requests page and N = 3307 must be re-checked against the live table once that bundle disappears.

## Check it yourself

One command, standard library only (Python 3.8+), about 2 minutes on a laptop:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (verifies the object's sha256 — LF or CRLF-materialised form — and
count, recomputes r* at 60 significant digits from the coordinate strings, checks the margin;
its real output is in verify-it-yourself/RECEIPTS.md).

## Compared to

Packomania, "The best known packings of equal circles in a circle" (cci), cell N = 3307:
https://packomania.com/cci/cci.html — machine-readable table
https://packomania.com/cci/txt/radius.txt fetched 2026-10-17T09:45:15Z (HTTP 200, sha256
6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead), row 3307 =
0.016314899796158766989004378524. The posted configuration reproduces its table value to
-8.15e-31 (integrity clean) and is structurally lattice-like (3292 of 3307 nearest-neighbour
distances at the exact minimum; neighbour directions at multiples of 60 degrees) — an unoptimized
seed of the kind partial win p2 names. Snapshot details in the-record-we-beat/.

## Not claimed

- Not a record for any other N (the sibling cell N = 4141 is a separate claim, PR #234).
- Not proven optimal for N = 3307 (only N <= 13 and N = 19 have proofs in this table).
- No submission was made to Packomania (no email; the claim is the verified construction only).
- The queue-rule caveat above: the category-unspecified pending bundle is unresolved as of the
  fetch date; the cell must be re-checked when that bundle clears.

## Credits

- Eckard Specht's Packomania (https://packomania.com) — the cci table, the radius data and the
  posted configuration this result improves on.
- The V3R1T4S open notebook (https://github.com/elder-plinius/V3R1T4S) — the bank entry that
  defines the success criterion, the run protocol, and the three-skeptic panel process.
- W. Sander, "LLM-Guided Program Evolution for Circle Packing" (arXiv:2609.05093, 2026) — checked
  for overlap; its 10 records are in the csqv category, not cci.
- Construction method: plain triangular-lattice window with optimal orientation/offset/spacing
  (closed form s* = 2/(1 + 2 rho_N)); see how-we-built-it/.

## Packaging note

All package files are LF; every hash (SHA256SUMS, INDEX.csv, verify-it-yourself/check.py) refers
to these LF bytes (object sha256
f09f5eecbb7b14f10607e97c3a74829129931cc0e0285e4372a5b4c4f61b0194, which also keys the
submission id). verify-it-yourself/check.py additionally accepts the CRLF-materialised form of
the object (a core.autocrlf=true checkout), so its integrity check passes on both.
