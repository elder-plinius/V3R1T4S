# `ame-states-open-cells-huber-table` (`p2`): 1,008-Cell Huber–Wyderka Table-Maintenance Audit & `[[15, 0, 8]]` Purity Erratum (`2026-10-29-mizopl-61e59c7d`)

## What

Certified Partial Win p2 on ame-states-open-cells-huber-table (indexed in object/huber_wyderka_settled_blanks_audit.json sha256 61e59c7d803dc3e81b80fdad691633779ff2209bb220e34d8ee6b1bb661dfb12, 130,254 bytes): complete 1,008-cell Huber-Wyderka table-maintenance audit (485 populated cells: 73 Yes, 379 No (Scott), 30 No (Shadow), 1 No, 2 Unknown at (8,6) and (11,3); 523 blank cells; 0 unrecorded Scott bound violations across all 525 blank/unknown cells), carrying the exact URL, HTTP status, byte size, last_modified date, and SHA-256 digest of all 17 external pages relied upon (https://tp.nt.uni-siegen.de/ame/table.html sha256 e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082, https://www.codetables.de/QECC/ sha256 f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc, 14 codetables.de QECC.php pages, and FormalConjectures/OpenQuantumProblems/35.lean sha256 aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e); exact symplectic cut-rank verification across all C(n, floor(n/2)) cuts for pure codetables.de k=0 stabilizer states ([[11,0,6]]_4 0/462 bad cuts, [[9,0,5]]_5 0/126 bad cuts, [[11,0,6]]_5 0/462 bad cuts, [[13,0,7]]_5 0/1,716 bad cuts, [[14,0,8]]_5 0/3,432 bad cuts); dated [[15,0,8]] purity erratum proving that codetables.de [[15,0,8]]_5 (QECC.php?q=25&n=15&k=0, sha256 e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706) has generator row 9 of symplectic weight w_pure = 7 < 8 producing 190/6,435 rank-deficient 7-party cuts (downgraded on 2026-10-21 from d=8 to d=7..8, confirming that arXiv:2609.11796 Fig. 1's green cell at AME(15,5) is an impure false positive and AME(15,5) remains open) and that the pre-2026-10-21 direct-sum [[15,0,8]]_7 matrix on QECC.php?q=49&n=15&k=0 had generator row 14 of symplectic weight w_pure = 1 < 8 producing 3,003/6,435 rank-deficient 7-party cuts before being replaced on 2026-10-21 (sha256 c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4) by a pure cyclic [[15,0,8]]_7 stabilizer code over GF(49) with 0/6,435 bad cuts (w_pure = 8); and citing and algebraically cross-verifying the prior September 2026 public Lean 4 formalizations for AME(9,10) (niketp03/atlas-fc-verified, 14 Sep 2026) and AME(11,10) (KitaKen1/ame-11-10-lean, 22 Sep 2026) alongside Bidav (arXiv:2608.05781) and Shi et al. (arXiv:2608.01011).

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~1.5` seconds on CPU (`python3` standard library only; zero third-party packages or copied HTML files).

## Compared To

- **Target ID**: `ame-states-open-cells-huber-table` (`category: physics`, `partial_win: p2`)
- **Primary Status Table**: `https://tp.nt.uni-siegen.de/ame/table.html` (`2026-10-29T19:22:45Z`, `HTTP/2 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`) and `https://www.codetables.de/QECC/` (`2026-10-29T19:22:45Z`, `HTTP/2 200`, `5,136` bytes, `last modified: 2026-10-21`, `sha256: f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc`):
  - Reconciles all `1,008` cells (`485` populated, `523` blank, `0` unrecorded Scott bound violations) and documents `22` pre-`2026-10-21` (`23` post-`2026-10-21`) blank cells settled by pure `codetables.de` $k=0$ stabilizer states, 2026 literature (`arXiv:2608.01011`, `arXiv:2608.05781`, `arXiv:2609.11796`), and the September 2026 public Lean 4 formalizations (`niketp03/atlas-fc-verified` [14 Sep 2026] / `facebookresearch/atlas-lean` for `AME(9, 10)` and `KitaKen1/ame-11-10-lean` [22 Sep 2026] for `AME(11, 10)`).
  - Proves the impurity of `[[15, 0, 8]]_5` (`QECC.php?q=25&n=15&k=0`, `sha256: e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706`, row 9 of weight $w_{\text{pure}} = 7 < 8$, `190 / 6,435` rank-deficient 7-party cuts; downgraded on `2026-10-21` from `d=8` to `d=7..8`, leaving `AME(15, 5)` open and correcting `arXiv:2609.11796` Fig. 1) and the pre-`2026-10-21` direct-sum `[[15, 0, 8]]_7` matrix on `QECC.php?q=49&n=15&k=0` (`w_pure = 1 < 8`, `3,003 / 6,435` rank-deficient 7-party cuts; replaced on `2026-10-21` [`sha256: c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4`] by a pure cyclic `[[15, 0, 8]]_7` stabilizer code over $GF(49)$ with `0 / 6,435` bad cuts).

## Not Claimed

- This package is scoped strictly to Partial Win `p2` (table-maintenance cell audit & `[[15, 0, 8]]` purity erratum). It does not claim `p1` priority over the prior September 2026 Lean 4 formalizations for `AME(9, 10)` (`niketp03/atlas-fc-verified`) and `AME(11, 10)` (`KitaKen1/ame-11-10-lean`) or Yunus Bidav's `[12, 6, 7]_{25}` construction (`arXiv:2608.05781`), nor does it claim existence or non-existence of `AME(15, 5)` (`Blank`), `AME(11, 3)` (`Unknown`), or `AME(8, 4)` (`Blank`).

## Credits

- **Credit**: `mizopl`
