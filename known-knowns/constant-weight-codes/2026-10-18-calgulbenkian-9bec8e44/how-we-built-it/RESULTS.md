# Constant-Weight Codes (`Andw.html`) Attack — Verified Results, trimmed to A(28, 8, 11)

> Note added 2026-11-06, not contributor text: this is the contributor's working record. Paths such as `results/...` name files in the contributor's own workspace and are not shipped. The shipped object is `object/A28_8_11_3802.txt`, and the shipped checkers are in `verify-it-yourself/`. Trimmed on maintainer review (#440) to the one cell this package claims: the run's other cells, its upper-bound certificates and its p1 codes are left out, and nothing is claimed for them here. The Echols value for this cell was corrected from 3716 to "not listed": arXiv:2608.13906v1 has no row for A(28, 8, 11). The live table value has moved since the run (3791, label Ol, fetched 2026-11-06T20:26:09Z); see README.md.

## Summary

Against the contributor's frozen copy of https://aeb.win.tue.nl/codes/Andw.html (not shipped; `SHA-256: bc8822714c5d0f6414f158e6f0dad6529b9253aaf33b6b4a4c620105ee7e3653`), the run found an explicit constant-weight code showing A(28, 8, 11) >= 3802, above that snapshot's lower bound 3785 (label Pl). The search started from the merged 3785 code and used degree-sorted coordinate relabelling with large-neighbourhood search. The code was checked by the contributor's own verifier (not shipped; the shipped checkers are in `verify-it-yourself/`).

| Cell $(n, d, w)$ | `Andw.html` (contributor's snapshot) | Echols `2608.13906` | Lysenstoen `2607.19550` | **New Verified $M$** | **Gain vs snapshot** | File | SHA-256 (prefix) |
|---|---:|---:|---:|---:|---:|---|---|
| `A(28, 8, 11)` | `3785Pl-16354` | not listed | — | **`3802`** | **`+17`** | `A28_8_11_3802.txt` (shipped as `object/A28_8_11_3802.txt`) | `9bec8e442ef7b35e` |
