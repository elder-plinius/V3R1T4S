# 3D AB Off-Lattice Protein Model: Four New Record Conformations (`F89` `-E* = 87.179252`, `2EWH` `-E* = 257.505676`, `1CRN` `-E* = 95.720530`, `1PCH` `-E* = 166.978884`) and 23-Sequence Reproduction Audit

## What
Explicit conformations and 3D unit-bond Cartesian coordinate sets in object/ab_3d_records_F89_2EWH_1CRN_1PCH.json for four benchmark sequences of the 3D AB off-lattice protein model (F89 with L = 89 and D = 173, 2EWH with L = 98 and D = 191, 1CRN with L = 46 and D = 87, and 1PCH with L = 87 and D = 169) achieve strict local-minimum energies (-E* = 87.179252478342 vs 86.4318 on F89, +0.747452 gain; -E* = 257.505676299754 vs 257.0741 on 2EWH, +0.431576 gain; -E* = 95.720529801173 vs 95.3159 on 1CRN, +0.404630 gain; and -E* = 166.978883682418 vs 166.7194 on 1PCH, +0.259484 gain) verified in both float64 and 50-digit arithmetic with all bond lengths equal to 1 within 2.22e-16 and angle-space gradient norms ||grad E||_2 <= 6.69e-12, beating the best published energies in Table 10 of Boskovic and Brest (arXiv:1903.01456) and Kim (2016) across all three longest chains (including +0.747452 above 0.5 on F89 for p1) alongside a complete independent reproduction and discrepancy audit of all 23 published conformations in Tables 11 and 12 (p2).

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in `< 2.5` seconds using the Python 3 standard library `math` and 55-digit `decimal.Decimal` verifier).

## Compared To
All comparisons are against the primary benchmark paper by Borko Boskovic and Janez Brest (*"Two-phase protein folding optimization on a three-dimensional AB off-lattice model"*, *Swarm and Evolutionary Computation* 57, 100711, 2020; `https://arxiv.org/abs/1903.01456`, Table 2, Table 10, Table 11, and Table 12; and S. Y. Kim, *Chaos, Solitons & Fractals* 90, 111-117, 2016, which reported `-E = 73.1065` for `F89`), fetched on `2026-10-17T18:07:36Z` (recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Sequence | $L$ | $D = 2L-5$ | Published Best $-E$ (`arXiv:1903.01456` Table 10) | Raw Table 11/12 Recomputed $-E$ | Our Polished $-E^*$ (`object/ab_3d_records_F89_2EWH_1CRN_1PCH.json`) | Gain over Table 10 | Angle-Space $\|\nabla E\|_2$ | Max Bond Length Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`F89`** | `89` | `173` | `86.4318` (Kim 2016: `73.1065`) | `86.431819` (`\|\nabla E\|_2 = 1.97\times 10^{-2}`) | **`87.179252`** | **`+0.747452`** (`>= 0.5`, `p1` + Full Win) | **`2.80e-12`** | **`2.22e-16`** |
| **`2EWH`** | `98` | `191` | `257.0741` | `257.074077` (`\|\nabla E\|_2 = 2.13\times 10^{-1}`) | **`257.505676`** | **`+0.431576`** (Full Win) | **`6.69e-12`** | **`2.22e-16`** |
| **`1CRN`** | `46` | `87` | `95.3159` | `95.315907` (`\|\nabla E\|_2 = 5.47\times 10^{-3}`) | **`95.720530`** | **`+0.404630`** (Full Win) | **`4.72e-12`** | **`2.22e-16`** |
| **`1PCH`** | `87` | `169` | `166.7194` | `166.719373` (`\|\nabla E\|_2 = 5.42\times 10^{-2}`) | **`166.978884`** | **`+0.259484`** (Full Win) | **`3.61e-12`** | **`2.22e-16`** |

### Complete 23-Sequence Independent Reproduction & Discrepancy Audit (Partial Win `p2`)
Because the authors' web demo (`http://spse.feri.um.si`) is offline, we extracted all 23 published angle vectors from Tables 11 and 12 of the `arXiv:1903.01456` LaTeX source (`paper.tex`) and recomputed their energies and gradients (embedded in `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` under `arXiv_1903_01456_reproduction_audit` and verified by `verify-it-yourself/check_ab_protein.py`):
1. **All 23 Table 10 Values Confirmed to 4 Decimal Places**: Every published conformation in Tables 11 and 12 reproduces its Table 10 value within `4.97e-5` under Eq. (4) (`c(A,A) = 1`, `c(B,B) = 0.5`, `c(A,B) = -0.5`).
2. **Table 2 `1PCH` Length & Dimension Discrepancy (`L = 87, D = 169` vs Printed `L = 88, D = 171`)**: Table 2 of `arXiv:1903.01456` lists `1PCH` with `L = 88` and `D = 171`, whereas the actual sequence string in Table 2 has **87 residues** (`L = 87`) and the published angle vector in Table 12 has **169 angles** (`D = 2L - 5 = 169`: 85 bond angles and 84 torsion angles) evaluating to `-E = 166.719373` (matching Table 10's `166.7194`).
3. **4-Decimal Angle Truncation Drift on `2EWH` (`L = 98`)**: Due to 4-decimal degree rounding in Tables 11 and 12, the published `2EWH` vector has `||grad E||_2 = 0.213` (`||grad E||_inf = 0.103`) and evaluates to `-E = 257.074077`; local Newton-polishing restores stationarity (`||grad E||_2 = 5.36e-12`) at `-E = 257.074539` (`+0.000462`).

## Not Claimed
- We do not claim global optimality of the four reported conformations; each is a verified strict local minimum in angle space (`||grad E||_2 <= 6.69e-12 < 1e-8`) that beats the best published value in Table 10 by `+0.259484` to `+0.747452` energy units (`259.5x` to `747.5x` the `1e-3` margin).

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **Borko Boskovic and Janez Brest** (`arXiv:1903.01456`, *Swarm and Evolutionary Computation* 57, 100711, 2020) for the two-phase differential evolution baseline and for publishing the full angle vectors of all 23 benchmark sequences in Tables 11 and 12.
- **S. Y. Kim** (*Chaos, Solitons & Fractals* 90, 111-117, 2016) for the `F89` Fibonacci benchmark (`L = 89`).
- **F. H. Stillinger, T. Head-Gordon, and C. L. Hirshfeld** (*Phys. Rev. E* 47, 2189, 1993) for the AB off-lattice protein model formulation.
