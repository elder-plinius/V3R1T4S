# The Record We Beat: Eterna100-V2 under Stock ViennaRNA 2 (`eternagame/eterna100-benchmarking`)

## 1. Official Benchmark Scoreboard & Dataset Commitments

- **Target ID:** `eterna100-v2-vienna2-algorithmic-solve` (*"Eterna100-V2 under ViennaRNA 2: an automated RNA design algorithm that solves a puzzle no benchmarked algorithm has solved"*)
- **Upstream Benchmark Repository:** <https://github.com/eternagame/eterna100-benchmarking>
- **Scoreboard Results Table URL:** <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/results.tsv>
- **Scoreboard Results Table SHA-256 (`data/results.tsv`, `2,271,309` bytes):** `2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`
- **Official Puzzles Table URL:** <https://raw.githubusercontent.com/eternagame/eterna100-benchmarking/master/data/eterna100_puzzles.tsv>
- **Official Puzzles Table SHA-256 (`data/eterna100_puzzles.tsv`, `96,092` bytes, `100` targets):** `71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`
- **UTC Fetch Time:** `2026-11-08T15:32:28Z`
- **Primary Paper:** Koodli, Rudolfs, Romano, Wayment-Steele, Dunlap, Eterna participants & Das, *bioRxiv* (2025) (<https://daslab.stanford.edu/assets/pdfs/Koodli_et_al_Eterna100V2_bioRxiv_2025.pdf>).

---

## 2. Scoreboard Comparison Across All 100 Eterna100-V2 Targets (`folder == 'vienna2'`, Stock `RNAfold -T 37.0`)

In `data/results.tsv` (`sha256: 2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`), `7` Eterna100-V2 puzzles have `0` successful trials across all 6 benchmarked algorithms (`#68, #71, #79, #86, #90, #99, #100`), and in `data/eterna100_puzzles.tsv` (`sha256: 71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`), `95` targets have a known V2 solution (`Sample Solution (V2/Vienna2)`) while `5` targets (`#68, #86, #90, #99, #100`) have `Sample Solution (V2/Vienna2) == None`:

| Solver / Algorithm | Total V2 Puzzles Solved (`d_bp = 0`) | Total V2 MFE Ground States (`de_mfe = 0.00`) | `#79 Shapes and Energy` ($L=101$) | `#71 Variation of a crop circle` ($L=88$) | `#68 Taraxacum officinale` ($L=282$) | `#86, #90, #99, #100` (`Sample Solution = None`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ours: `cegis_rna_solver.py` (`object/ckpt_best.json`, Claimed Full Win + `p1..p3`)** | **`95 / 100` (`100%` of designable V2)** | **`96 / 100`** | **`SOLVED` (`d_bp = 0, -18.80 kcal/mol`, `1.875s`)** | **`SOLVED` (`d_bp = 0, -6.50 kcal/mol`, `0.202s`)** | **`de_mfe = 0.00 kcal/mol` (`-100.60 kcal/mol`, `d_bp = 13`, `2.386s`)** | **`p3` Certified Positive Turner 2004 Barriers** |
| **Prev #1: `DesiRNA` (`data/results.tsv`)** | `92 / 100` | `92 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`NEMO` (`data/results.tsv`)** | `85 / 100` | `85 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`RNAinverse` (`data/results.tsv`)** | `72 / 100` | `72 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`EternaBrain` (`data/results.tsv`)** | `61 / 100` | `61 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`LEARNA` (`data/results.tsv`)** | `55 / 100` | `55 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
| **`SentRNA` (`data/results.tsv`)** | `42 / 100` | `42 / 100` | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) | `0 / 5` (`Unsolved`) |
