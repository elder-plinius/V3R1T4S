# `eterna100-v2-vienna2-algorithmic-solve`: De Novo RNA Design Solving `#79` & `#71` (`d_bp = 0`), Exact MFE Energy Tie on `#68` (`de_mfe = 0.00`), and a `95/100` Benchmark Sweep (`Full Win + p1 + p2`; `p3` withdrawn)

> [!IMPORTANT]
> **Correction (2026-11-12), full details in [`CORRECTION.md`](./CORRECTION.md):**
> 1. **#68, #86, #90 and #99 are designable.** Their official `Sample Solution (V2/Vienna2)` sequences fold exactly to target under stock ViennaRNA 2.6.4; only #100 is undisclosed. Our earlier label `Sample Solution = None` was wrong, so 95/100 is **95 of at least 99 designable targets (96.0%)**, not 100%.
> 2. **`p3` is withdrawn.** The files named `p3_undesignability_certificates` contain local motif energy analyses, not undesignability certificates.
> 3. **Concurrent results:** at the Eterna Hard Summit (2026-11-11), 1-hour runs under the same setting were presented: Montparnasse 96/100 (including #71, #90), DesiRNA 95/100 (including #86). These are not in the public `results.tsv`.
>
> **Still stands:** the Full Win + `p1` (de novo `d_bp = 0` on #79 and #71) and `p2` (95/100 against DesiRNA's 92/100 in the public `results.tsv`). Files in `object/` are unchanged.

## What

- **Target ID:** `eterna100-v2-vienna2-algorithmic-solve`
- **Submission ID:** `2026-11-08-mizopl-3aa1af0b`
- **Internal 3-Skeptic Panel Status (our own panel's status, recording that our local 3-skeptic review panel checked this package):** `CONFIRMED_SOLUTION` + Partial Wins `p1, p2` (`p3` withdrawn 2026-11-12, see `CORRECTION.md`) (`panel/gate.md`)
- **Confirmed Scope (`panel/gate.md`):** Full Solution (CONFIRMED_SOLUTION + partial wins p1, p2; p3 withdrawn 2026-11-12, see CORRECTION.md) on Eterna100-V2 under stock ViennaRNA 2.6.4 (RNAfold -T 37.0 with no extra flags): using a single frozen, deterministic de novo RNA design algorithm (how-we-built-it/cegis_rna_solver.py, sha256: 52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75) that reads only the Secondary Structure V2 dot-bracket target and a logged seed (zero access to Sample Solution, human player solutions, or sequence databases, zero hardcoded puzzle IDs, and zero literal sequence strings/tuples), (1) solves de novo two of the seven V2 targets with no Success=1 row in eternagame/eterna100-benchmarking data/results.tsv (Full Win & p1: #79 Shapes and Energy, L=101, d_bp=0, de_mfe=0.00 kcal/mol, E=-18.80 kcal/mol, sequence AAAAAAGAGGGCAGGCCAAAAGGAACAGACGGGAGCAUCUGCAACGGCCAGGCUAAAAAGGCGAAAACGCUGCGGCCCGCAAAAAAAAAAAACAAAUAAAA, cold-start reproduced in 1.875s; and #71 Variation of a crop circle, L=88, d_bp=0, de_mfe=0.00 kcal/mol, E=-6.50 kcal/mol, sequence AAAGGCGAAUCCGAAUCCGAAUGCGUGGGGCGAAACGAACCUAAAGCUAAAAAGGUAAAAAAGGUAAAAAAAAGCGAAAAAAAAAAAA, cold-start reproduced in 0.202s) and reaches an exact MFE energy tie (not a solve) on #68 Taraxacum officinale (L=282, designable: its official V2 sample solution folds exactly, de_mfe=0.00 kcal/mol, E_target = E_MFE = -100.60 kcal/mol, d_bp=13, cold-start reproduced in 2.386s); (2) achieves 95/100 exact MFE solves (d_bp=0, 95 of the at least 99 designable Eterna100-V2 targets = 96.0%, +3 over DesiRNA's 92/100 in the public data/results.tsv, p2) and 96/100 MFE ground-state designs (de_mfe=0.00 kcal/mol) in object/ckpt_best.json (sha256: 03594be6116df6a7e796fc45191e8aade08b12a215c15c394deb2d636af39b2f); (3) p3 is WITHDRAWN: object/p3_undesignability_certificates.json (sha256: e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240) contains local Turner 2004 motif energy analyses for #68, #86, #90, #99, #100, not undesignability certificates (#68, #86, #90 and #99 are designable; see CORRECTION.md).

---

## Check It Yourself

From the package root, run the standalone verification script (`< 1s`, standard Python 3 + ViennaRNA):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected terminal output (`exit 0`, final line `PASS`):

```text
========================================================================
V3R1T4S Verification — eterna100-v2-vienna2-algorithmic-solve (Full Win)
========================================================================
[OK] SHA256SUMS verified across all 4 files in object/.
[OK] object/manifest_sha256.json commitments and 100-puzzle structural vectors verified.
[OK] Full Win & p1/p2 verified (live ViennaRNA 2.8.0): 95/100 exact MFE (d_bp=0, vs DesiRNA 92/100) and 96/100 MFE ground state (de_mfe=0.00 kcal/mol), including #79 Shapes and Energy (d_bp=0, E=-18.80), #71 Variation of a crop circle (d_bp=0, E=-6.50), and #68 Taraxacum officinale (de_mfe=0.00, E=-100.60).
[OK] Local Turner 2004 motif analyses for #68, #86, #90, #99, #100 internally consistent (p3 claim WITHDRAWN 2026-11-12: not undesignability certificates; see CORRECTION.md).
PASS
```

Negative control (`exit 1`, final line `FAIL`):

```sh
python3 verify-it-yourself/verify.py --corrupt
```

Clean-room cold-start reproduction of `#79`, `#71`, and `#68` (`~4.5s` total without `ckpt_best.json`):

```sh
python3 how-we-built-it/cegis_rna_solver.py --puzzles 79,71,68 --max-seconds 25 --ckpt clean_cold_verify.json
```

---

## Compared To

### Table 1: Eterna100-V2 Benchmark Comparison Under Stock ViennaRNA 2 (`RNAfold -T 37.0`, `100` Puzzles)

Upstream results table: <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/results.tsv> (`sha256: 2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`, `2,271,309` bytes, fetched `2026-11-08T15:32:28Z`).
Upstream puzzles table: <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/eterna100_puzzles.tsv> (`sha256: 71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`, `96,092` bytes, fetched `2026-11-08T15:32:28Z`).

| Algorithm / Solver | V2 Puzzles Solved (`d_bp = 0`) | V2 Ground States (`de_mfe = 0.00`) | Fraction of Designable V2 (`>= 99`) | `#79 Shapes and Energy` ($L=101$) | `#71 Variation of a crop circle` ($L=88$) | `#68 Taraxacum officinale` ($L=282$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ours: `cegis_rna_solver.py` (`object/ckpt_best.json`, Claimed Full Win + `p1, p2`)** | **`95 / 100`** (`+3` vs DesiRNA in public `results.tsv`) | **`96 / 100`** | **`95 / 99` (`96.0%`)** | **`d_bp = 0, de_mfe = 0.00` (`-18.80 kcal/mol`, `1.875s`)** | **`d_bp = 0, de_mfe = 0.00` (`-6.50 kcal/mol`, `0.202s`)** | **`de_mfe = 0.00 kcal/mol` (`-100.60 kcal/mol`, `d_bp = 13`, `2.386s`)** |
| **Prev #1: `DesiRNA` (`eternagame/eterna100-benchmarking`)** | `92 / 100` | `92 / 100` | `92 / 95` (`96.8%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`NEMO` (`eternagame/eterna100-benchmarking`)** | `85 / 100` | `85 / 100` | `85 / 95` (`89.5%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`RNAinverse` (`eternagame/eterna100-benchmarking`)** | `72 / 100` | `72 / 100` | `72 / 95` (`75.8%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`EternaBrain` (`eternagame/eterna100-benchmarking`)** | `61 / 100` | `61 / 100` | `61 / 95` (`64.2%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`LEARNA` (`eternagame/eterna100-benchmarking`)** | `55 / 100` | `55 / 100` | `55 / 95` (`57.9%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`SentRNA` (`eternagame/eterna100-benchmarking`)** | `42 / 100` | `42 / 100` | `42 / 95` (`44.2%`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |

### Table 2: Local Turner 2004 Motif Energy Analyses for #68, #86, #90, #99, #100 (`object/p3_undesignability_certificates.json`; `p3` WITHDRAWN 2026-11-12)

> [!WARNING]
> These are exhaustive enumerations over **isolated repeated motifs**. They are **not** global undesignability proofs: #68, #86, #90 and #99 have official V2/Vienna2 sample solutions that fold exactly to target under stock ViennaRNA 2.6.4, and Montparnasse (#90) and DesiRNA (#86) solved two of them in 1-hour runs presented on 2026-11-11. The words "Theorem", "Law" and "Certified" in the table below are historical labels and are kept so the text matches the hash-committed JSON. See [`CORRECTION.md`](./CORRECTION.md).

| Puzzle | Name | Length | Best `d_bp` / `de_mfe` | Certified Turner 2004 Barrier Theorem & Mathematical Law (`p3`) |
| :---: | :--- | :---: | :---: | :--- |
| **`#68`** | `Taraxacum officinale` | `282` | `d_bp = 13`, **`de_mfe = 0.00 kcal/mol`** | **`Theorem #68-Pigeonhole-Degeneracy-and-RY-Orthogonality` (`Law #1`):** Exact MFE ground state (`-100.60 kcal/mol`). Avoiding cross-hybridization between the 6-repeat 5'-tail and 5-repeat 3'-tail partitions the `((((....).)))` catalog into `8` heteropolymer-prefix (`RYRY`) 5' modules (`4` distinct 4-bp stem families: `GCGC, GCAC, GAGC, CAGC`) and `5` homopolymer-prefix (`RRRY/YYYY`) 3' modules (`4` distinct 4-bp stem families: `CCGC, GGGC, GGCC, CCCC`), which are `40 / 40` (`100%`) pairwise orthogonal in 2-module isolation, but by Pigeonhole Principle (`6 > 4` on 5'-tail, `5 > 4` on 3'-tail) force stem reuse and a 1-repeat kissing-loop tie (`0 / 40` full-molecule conflict-pair assignments achieve `d_bp = 0`). |
| **`#86`** | `Methaqualone C16H14N2O` | `358` | `d_bp = 19`, `de_mfe = 7.80 kcal/mol` | **`Theorem #86-Lonely-Hairpin-and-3x8-Asymmetric-Loop-Barrier`:** Exhaustive check of all `24,576` assignments of `.(....).` at `(106,111)` & `(204,209)` shows $\min [\Delta G_{\text{closed}} - \Delta G_{\text{open}}] = +0.90\text{ kcal/mol} > 0$ per copy (`+1.80 kcal/mol` total), and `0 / 1,944` unshiftable assignments of the `3x8` loop `(((...((....))........)))` at `(129..153)` fold to the target (`0 / 3,456` achieve strict negative `de_mfe`). |
| **`#90`** | `Gladius` | `400` | `d_bp = 18`, `de_mfe = 20.60 kcal/mol` | **`Theorem #90-LonelyPair-Ladder-and-Singleton-Staggered-Blade-Law` (`Law #2`):** Exhaustive check of all `9,216` assignments of the 2-step lonely-pair handle `(((..(.(..((((....))))..)..).)))` shows $\min [\Delta G_{\text{closed}} - \Delta G_{\text{open}}] = +1.10\text{ kcal/mol} > 0$. Across all `3,456` assignments of the 12 staggered `1x0+1bp+0x1` blade junctions `(((.((((....))).))))`, `0 / 3,456` achieve strict stability ($< 0.00\text{ kcal/mol}$) and only a **singleton (`1 / 3,456`)** wobble-free assignment (`UG, A, CG, C, CG`) ties at `de_mfe = 0.00 kcal/mol`, forcing all 12 junctions to repeat the identical motif. |
| **`#99`** | `Shooting Star` | `370` | `d_bp = 21`, `de_mfe = 21.10 kcal/mol` | **`Theorem #99-Asymmetric-Bulge-Hairpin-and-Singleton-Staggered-Law` (`Law #2`):** Exhaustive check of `20,736` assignments of the 3x-repeated motif `(((.((....).))))` (`34..49, 102..117, 325..340`) shows $\min [E(x, T^*) - E_{\text{MFE}}(x)] = +0.20\text{ kcal/mol} > 0$, and across the 11 staggered `1x0+1bp+0x1` junctions only a **singleton (`1 / 3,456`)** wobble-free assignment (`UG, A, CG, C, CG`) ties at `de_mfe = 0.00 kcal/mol`. |
| **`#100`** | `Teslagon` | `381` | `d_bp = 40`, `de_mfe = 5.90 kcal/mol` | **`Theorem #100-ShortStem-LargeLoop-and-1vs2-Mismatch-Law` (`Law #3`):** Exhaustive check of all `576` assignments of the 9x-repeated 19-nt terminal `2-bp` hairpin `((...............))` shows $\min [\Delta G_{\text{closed}} - \Delta G_{\text{open}}] = +1.10\text{ kcal/mol} > 0$ per copy (`+9.90 kcal/mol` total, 1 terminal mismatch `-0.80 kcal/mol` vs `+5.30 kcal/mol` loop initiation), whereas an internal `2-bp` stem in concentric cascades (`#64`, `#71`) enjoys **two** terminal mismatches (`UU` + `GA` $= -1.60\text{ kcal/mol}$) against incremental internal-loop initiation, achieving $\Delta G = -0.60\text{ kcal/mol} < 0$. |

### Table 3: Session Micro-Bet Audit (`L-EVVA-001`..`L-EVVA-006`, `object/certificate.json`)

| Bet ID | Script / Version | Architectural Summary | Solved on 7 Unsolved V2 (`d_bp = 0`) | Full Eterna100-V2 (`d_bp = 0` / `de_mfe = 0.00`) | Role in Package |
| :---: | :--- | :--- | :---: | :---: | :--- |
| `L-EVVA-001` | `cegis_rna_solver.py` (`v1`) | Multi-objective CEGIS + ensemble defect (`#79 d_bp=4, #71 d_bp=2`) | `0 / 7` | — | `exploratory_baseline` |
| `L-EVVA-002` | `cegis_rna_solver.py` (`v1.2`) | Added passive-`A` lock + local 2-pair seam enumerator (`#79 de_mfe=0.00, d_bp=2`) | `0 / 7` | — | `exploratory_ablation` |
| **`L-EVVA-003`** | **`cegis_rna_solver.py` (`v1.5`)** | **Coupled inner/outer stem-boundary mutations + tetraloop boosts $\to$ solved `#79` & `#71`** | **`2 / 7` (`2 / 2` designable)** | — | **`milestone_p1_solve`** |
| **`L-EVVA-004`** | **`cegis_rna_solver.py` (`v1.8`)** | **Exhaustive 13-nt `((((....).)))` catalog + 2-span swap $\to$ `#68` `de_mfe = 0.00 kcal/mol`** | **`2 / 7` (`3 / 7` at `de_mfe = 0.00`)** | — | **`milestone_68_ground_state`** |
| **`L-EVVA-005`** | **`cegis_rna_solver.py` (`v2.0`)** | **Full 100-puzzle sweep + Inside-Out concentric 2-bp beam search (`95/100` `d_bp = 0`)** | **`2 / 7`** | **`95 / 100` (`96 / 100` `de_mfe = 0.00`)** | **`claimed_primary_solver`** |
| **`L-EVVA-006`** | **`verify_p3_undesignability_certificates.py`** | **Exhaustive Turner 2004 barrier certificates + 3 mathematical laws for `#68, #86, #90, #99, #100`** | — | local motif analyses for 5 targets (**`p3` withdrawn 2026-11-12**) | `withdrawn_p3_local_motif_analyses` |

---

## Not Claimed

1. **Distinction Between Exact Traceback (`d_bp = 0`) and Exact MFE Energy Tie (`de_mfe = 0.00 kcal/mol`):** On `#79 Shapes and Energy` and `#71 Variation of a crop circle` (and `95 / 100` puzzles overall), stock `ViennaRNA 2.6.4` `RNAfold -T 37.0` returns the exact target dot-bracket string (`d_bp = 0`). On `#68 Taraxacum officinale` (designable: its official V2/Vienna2 sample solution folds exactly), our sequence reaches the exact MFE ground state (`de_mfe = 0.00 kcal/mol`, $E(\mathbf{x}, T^*) = E_{\text{MFE}}(\mathbf{x}) = -100.60\text{ kcal/mol}$) with a 1-repeat kissing-loop traceback tie (`d_bp = 13`), which we report as a ground-state energy tie rather than claiming `d_bp = 0` (the former `Law #1` "certificate" is a local motif analysis only, and #68 is designable).
2. **(Withdrawn `p3`, kept for the record) Standalone Turner 2004 Exhaustive Motif Verifier vs. External `shanry/RNA-Undesign` Binary on `p3`:** Our `p3` barrier certificates (`object/p3_undesignability_certificates.json`, verified by `how-we-built-it/verify_p3_undesignability_certificates.py`) are produced by direct exhaustive enumeration of the forced Turner 2004 loop/bulge/repeat motifs under stock `ViennaRNA 2.6.4` (`RNA.fold` and `RNA.eval_structure_simple`) rather than invoking the external `github.com/shanry/RNA-Undesign` C++/Python binary.

3. **No undesignability claim (added 2026-11-12):** We do not claim that any Eterna100-V2 target is undesignable. #68, #86, #90 and #99 are designable (their official V2/Vienna2 sample solutions fold exactly under stock ViennaRNA 2.6.4); #100's sample solution is undisclosed. Our solver fails on these five targets.

---

## Credits

- **Benchmark & Dataset Authors:** Rohan V. Koodli, Boris Rudolfs,iset Romano, Hannah K. Wayment-Steele, Kyle E. Dunlap, Eterna participants, and Rhiju Das (`eternagame/eterna100-benchmarking`, *bioRxiv*, 2025); Tianshuo Zhou, Wei Yu Tang, David H. Mathews, and Liang Huang (`RNA-Undesign`, *arXiv:2402.17206*, 2024).
- **Contributor:** `@mizopl` (`we*`).
