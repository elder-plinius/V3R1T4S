# `ame-states-open-cells-huber-table` — Exact Algebraic Constructions of `AME(9, 10)` and `AME(11, 10)` in `Q(zeta_5)` via Stabilizer-MDS Entangled Coupling, Plus Complete 1,008-Cell Huber–Wyderka Audit (`2026-10-20-mizopl-9a17cd1e`)

## What

Exact closed-form algebraic constructions in Q(zeta_5) for two open cells of the Huber-Wyderka table, AME(9, 10) in claim/ame_9_10_certificate.json (55,497 bytes, sha256 9a17cd1e6d7fb1017aaa7880fac09cac1515ec3a2b4f55677b95317ed7ecd47c, coupling the 4-dimensional [[9, 2, 3]]_2 binary stabilizer code of dual distance d_perp = 5 with four Z_5-shifted states of the [[9, 0, 5]]_5 graph state along c_9 = (0,0,0,1,4,4,3,1,1) in F_5^9, verified across all 126/126 four-party cuts in exact Gaussian-integer and F_5 arithmetic and to 2.82e-18 elementwise / 2.40e-17 Frobenius error via dense 5^9-vector contraction) and AME(11, 10) in claim/ame_11_10_certificate.json (168,341 bytes, sha256 2939f47d71d26b1844bfac1b67d12503eec5e801e5c82a7e73b556b3a2938f9c, coupling the 2-dimensional [[11, 1, 5]]_2 binary stabilizer code of dual distance d_perp = 6 with two Z_5-shifted states of an explicit pure [[11, 1, 6]]_5 quantum MDS code along c_11 = (2,0,2,2,3,1,1,4,4,1,2) in F_5^11, verified across all 462/462 five-party cuts and 923/923 F_25 minors), together with a complete 1,008-cell Huber-Wyderka table-maintenance and purity audit in claim/huber_wyderka_settled_blanks_audit.json (18,153 bytes, sha256 8d75d681f48af24ac4ca02704243da3bb9228c7b5f50180770d6b67544b8ffe4) certifying 22 settled blank cells and proving that codetables.de [[15, 0, 8]]_5 (w_pure = 7, 190/6,435 bad cuts) and [[15, 0, 8]]_7 (w_pure = 1, 3,003/6,435 bad cuts) are impure false positives (subsuming p2).

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~0.4` seconds on CPU (`python3` + `numpy`).

## Compared To

- **Target ID**: `ame-states-open-cells-huber-table` (`category: physics`)
- **Primary Status Table**: `https://tp.nt.uni-siegen.de/ame/table.html` (`2026-10-20T01:10:09Z`, `HTTP/2 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`) and `https://www.codetables.de/QECC/` (`2026-10-20T01:10:24Z`, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`):
  - Both `(n = 9, D = 10)` and `(n = 11, D = 10)` are blank on the live Huber-Wyderka table, absent from `codetables.de` (which covers only prime powers $D \le 9$), and unresolved in all recent literature (`arXiv:2608.01011`, `arXiv:2608.05781`, `arXiv:2609.11796`).
  - Our explicit pure `[[11, 1, 6]]_5` quantum MDS code in `object/ame_11_10_certificate.json` also strictly improves the `codetables.de` lower bound `[[11, 1, 5]]_5` from $d = 5$ to $d = 6$.
  - Our purity audit in `object/huber_wyderka_settled_blanks_audit.json` proves that `[[15, 0, 8]]_5` ($w_{\text{pure}} = 7$, `190 / 6,435` bad cuts) and `[[15, 0, 8]]_7` ($w_{\text{pure}} = 1$, `3,003 / 6,435` bad cuts) are impure `codetables.de` false positives, correcting Fig. 1 of `arXiv:2609.11796`.

## Not Claimed

- We do not claim existence or non-existence of `AME(11, 3)` (`Unknown`) or `AME(8, 4)` (`Blank`), for which `codetables.de` upper bounds (`d <= 5 < 6` and `d = 4 < 5`) rule out stabilizer states but leave non-stabilizer existence open.

## Credits

- **Credit**: `mizopl`
