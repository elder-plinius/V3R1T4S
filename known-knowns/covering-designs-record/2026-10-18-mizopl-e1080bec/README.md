# covering-designs-record — Explicit `(94, 13, 5)` Covering Design with `125,184` Blocks

- **Claim:** The explicit `(94, 13, 5)` covering design stored in `object/design_94_13_5_part1.txt .. object/design_94_13_5_part5.txt` (reassembled `sha256: e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`, `4,704,754` bytes) has `125,184` distinct 13-element blocks over `{0, ..., 93}` and covers all $\binom{94}{5} = 54,891,018$ 5-subsets of a 94-set (`0` uncovered 5-subsets).
- **Compared to:**
  - **$47 + 47$ LJCR ingredient combining baseline (`how-we-built-it/build.py`):** `C(94, 13, 5) <= 125,236` blocks, constructed by partitioning $94 = 47 + 47$ across $j = 0, \dots, 5$ using the La Jolla Covering Repository (LJCR v1.2, Zenodo record `19735294`, published `2026-04-24`, fetched `2026-10-18T09:40:54Z`) ingredient designs credited to **Jan de Heer & Steve Muir** ($C(47, 13, 5) \le 2,849$, `2026-02-28`; $C(47, 11, 4) \le 866$, `2026-02-28`; $C(47, 8, 3) \le 345$, `2009-07-02`) and **Michael Dambmann** ($C(47, 5, 2) \le 113$, `2008-11-22`) plus trivial $(47, 2, 1) = 24$ and $(47, 0, 0) = 1$ (`2,849 + 20,784 + 38,985 + 38,985 + 20,784 + 2,849 = 125,236`, `sha256: 4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb`).
  - **Covering Repository (`coveringrepository.com` plain `(v,k,t)` table, `m = t = 5`):** `C(94, 13, 5) <= 129,203` (fetched `2026-10-18T09:40:05Z`, `sha256: 78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3`, line `3648`).
  - **La Jolla Covering Repository (`dmgordon.org/covering-designs/` & Zenodo `dmgordo/LJCR` v1.1 `19472830` / v1.2 `19735294`):** `C(94, 13, 5) <= 129,337` (status page fetched `2026-10-18T09:40:05Z`, `sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`; Zenodo v1.2 `coverdata.json` updated `2026-04-24`, fetched `2026-10-18T09:40:54Z`, `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`).
  - **Schönheim lower bound:** $L(94, 13, 5) = 42,705$.
- **Margin:**
  - **`52` blocks (`-0.0415%`)** below the `125,236`-block $47+47$ LJCR combining construction (`how-we-built-it/merge.c` pair-merge post-pass),
  - **`4,019` blocks (`-3.1106%`)** below the live Covering Repository record (`129,203`, fetched `2026-10-18T09:40:05Z`), and
  - **`4,153` blocks (`-3.2110%`)** below the live La Jolla Covering Repository record (`129,337`, fetched `2026-10-18T09:40:05Z` / `2026-10-18T09:40:54Z`).
- **One-liner to verify:** `sh verify-it-yourself/run_checks.sh`
- **Status:** `SELF-CONTAINED CONFIRMED`
