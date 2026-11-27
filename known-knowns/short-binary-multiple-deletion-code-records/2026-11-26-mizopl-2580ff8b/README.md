# Three Pure-Scratch Binary Multiple-Deletion Codes Beating Table 2: (15,2)=137, (15,3)=31, and (16,3)=44

## What

Three pure-scratch binary multiple-deletion codes strictly improve the best-known sizes in Table 2 of arXiv:2504.00613v2 across three cells: (15,2) has 137 distinct words (vs 136, |D_2|=3396, max LCS=12<13), (15,3) has 31 distinct words (vs 30, |D_3|=1397, max LCS=11<12), and (16,3) has 44 Klein-4-invariant distinct words (vs 42 and unmerged PR #997=43, |D_3|=2344, max LCS=12<13), with zero composition of published codebooks and standalone Lean 4.36.0 kernel certificates.

- `(15, 2)`: **137** distinct 15-bit words (`|D_2| = 3,396`, `max LCS = 12 < 13`, sorted-list `SHA-256` `2b226e2f0f7ab7fd...`), strictly above Table 2 `136` (`OnlineMIS`) and `CPro1` `132`.
- `(15, 3)`: **31** distinct 15-bit words (`|D_3| = 1,397`, `max LCS = 11 < 12`, sorted-list `SHA-256` `427002b54632ecc1...`), strictly above Table 2 `30` (`OnlineMIS`) and `CPro1` `29`.
- `(16, 3)`: **44** distinct 16-bit words (`|D_3| = 2,344`, `max LCS = 12 < 13`, Klein-4 `<c, r>`-invariant, sorted-list `SHA-256` `2580ff8bef1160cd...`), strictly above Table 2 `42` (`OnlineMIS`), `CPro1` `42`, and unmerged `V3R1T4S PR #997` (`43`). Three additional non-isomorphic `<rc>`, `<r>`, and `<c>` size-44 codes (`|D_3| = 2304, 2410, 2468`) are included under `object/companions/`.

None of these codes is a composition of published codebooks; all were constructed from scratch (word overlap with `CPro1` is `1` on `(15,2)`, `3` on `(15,3)`, and `10` on `(16,3)`; overlap with unmerged `PR #997` is `7`).

A standalone zero-dependency Lean 4.36.0 certification suite (`lean4_certs/`, `108` `.lean` files, `0` Mathlib, `0 sorryAx`, `0 native_decide`, `lake env leanchecker DeletionCode` exit `0`) certifies the general `D_s <-> LCS` equivalence, validity and full `2^n` 1-word inclusion-maximality of all codes, Klein-4 invariance of `(16,3)=44`, and exact global optimality on small benchmarks `M_2(7) = 5` and `M_3(9) = 5`.

## Check it yourself

From this folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (under 1 second on a standard laptop; runs exact `D_s` disjointness, full pairwise DP `LCS`, Klein-4 invariance, `SHA256SUMS`, and `--corrupt` negative control).

Optional Lean 4.36.0 kernel audit from `lean4_certs/`:

```sh
lake build DeletionCode && lake env lean AuditAxioms.lean && lake env leanchecker DeletionCode
```

## Compared to

Table 2 of Franziska Weindel and Reinhard Heckel, *LLM-Guided Search for Deletion-Correcting Codes*, TMLR 2026 (`arXiv:2504.00613v2`, fetched `2026-11-26T07:13:18Z`, HTTP 200, `sha256 = 4542bd58bc16be9bf47f6fc12f14fe86464c078c5a9c747058ee5698fbc7499a`):
- `(15, 2)`: `OnlineMIS = 136` (bold), `ReduMIS = 135`, `CPro1 = 132`, LP upper bound `277`.
- `(15, 3)`: `OnlineMIS = 30` (bold), `ReduMIS = t/o`, `CPro1 = 29`, LP upper bound `61`.
- `(16, 3)`: `OnlineMIS = 42` (bold), `ReduMIS = t/o`, `CPro1 = 42`, LP upper bound `99`.

## Not claimed

- **No `(16, 2)` frontier record claimed:** Although `object/companions/code_16_2_219_companion.json` (`219` words, pure scratch, Lean-certified) exceeds Table 2 (`215`), live EinsteinArena `#34` (`two-deletion-code-16`) already has public codes up to `226` (`kgrey #2778`). Our `(16,2)=219` is included strictly as a Lean-certified companion artifact, not as a record claim.
- **No global optimality proof for `n in (15, 16)`:** Lean `inclusion_maximal` proves 1-word non-extendability over all `2^n` binary words, not `M_s(n) <= |C|`. The LP upper bounds remain `277`, `61`, and `99`.
- **No decoder efficiency or linearity claim.**

## Credits

Franziska Weindel and Reinhard Heckel (`arXiv:2504.00613v2`, TMLR 2026) for Table 2; Christopher D. Rosin (`arXiv:2505.23881`, `Constructive-Codes/CPro1`) for the public baseline codebooks; Landjev and Haralambiev (Serdica J. Comput. 2007) and the `OnlineMIS`/`ReduMIS` authors cited in Table 2; and the EinsteinArena `#34` contributors for public `(16,2)` structural benchmarks.
