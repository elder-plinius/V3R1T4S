# Primary Status Tables & Live Snapshots (`fmm-additive-complexity-records`)

## 1. Live Sources Fetched Before Claiming (`2026-10-22T02:37:16Z` – `2026-10-22T02:38:44Z`)

1. **Lille FMM SOTA Catalogue (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`):**
   - **Fetched UTC:** `2026-10-22T02:37:16Z` (`HTTP/2 200`)
   - **Byte Size:** `343,774` bytes
   - **SHA-256:** `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`
   - **Saved Copy:** `the-record-we-beat/reference_live_champions/fmm_sota.json`
2. **Perminov's Live `FastMatrixMultiplication` Repository (`https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT`):**
   - **Fetched UTC:** `2026-10-22T02:37:56Z` (`HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` `.json` files in `addition_reduced_ZT`)
   - **`reduced_known.json` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json`):** `2026-10-22T02:38:44Z` (`HTTP/2 200`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`, saved at `the-record-we-beat/reference_live_champions/reduced_known.json`)
   - **`README.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`):** `2026-10-22T02:37:57Z` (`HTTP/2 200`, `112,906` bytes, `sha256: 5f8eb46827fd667f0200990f0e91d2f439db13f6555f63eeecbb39bc7b9fc17e`)
   - **`CHANGELOG.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md`):** `2026-10-22T02:37:57Z` (`HTTP/2 200`, `85,475` bytes, `sha256: 1ce6b0fa4aba0f86814dde157bee140014e894ac3956ed00efe022783d6224a8`)
3. **`matmulcatalog` Live `COVERAGE.md` (`https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md`):**
   - **Fetched UTC:** `2026-10-22T02:37:58Z` (`HTTP/2 200`)
   - **Byte Size:** `94,842` bytes
   - **SHA-256:** `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`
   - **Saved Copy:** `the-record-we-beat/reference_live_champions/matmulcatalog_COVERAGE.md`

## 2. Live Reference Values Beaten (9 Exact-SOTA Formats & 2 $\mathbb{Z}_T$-Best Formats)

| Format | Rank $m$ (`fmm_sota.json`) | Live `addition_reduced_ZT` Min `cr` (All Files) | `reduced_known.json` | `matmulcatalog` `adds` | Our New `cr` (`cu, cv, cw`) | Delta |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **`2x4x7`** | `45` (`45`) | `168` (`cr168`, `cr174`) | — | `+308` | **`157`** (`26, 58, 73`) & **`164`** (`27, 64, 73`) | **`-11` & `-4`** |
| **`2x5x5`** | `40` (`40`) | `147` (`cr147`, `cr153`) | `Z: 313, Z2: 218` | `+256` | **`145`** (`28, 58, 59`) | **`-2`** |
| **`4x5x8`** | `118` (`118`) | `466` (`cr466`, `cr513_fv249`) | — | `+1521` | **`447`** (`96, 141, 210`) | **`-19`** |
| **`4x6x7`** | `123` (`123`) | `468` (`cr468`, `cr517`) | — | `+1586` | **`464`** (`112, 138, 214`) | **`-4`** |
| **`5x5x6`** | `110` (`110`) | `411` (`cr411`, `cr460_fv204`) | — | `+1215` | **`406`** (`105, 110, 191`) | **`-5`** |
| **`5x5x8`** | `144` (`144`) | `555` (`cr555`, `cr620_fv281`) | — | `+1908` | **`548`** (`130, 156, 262`) | **`-7`** |
| **`5x6x6`** | `130` (`130`) | `499` (`cr499`, `cr562_fv250`) | — | `+1716` | **`492`** (`128, 139, 225`) | **`-7`** |
| **`5x6x7`** | `150` (`150`) | `577` (`cr577`, `cr664_fv310`) | — | `+2039` | **`573`** (`143, 165, 265`) & **`576`** (`144, 168, 264`) | **`-4` & `-1`** |
| **`5x7x7`** | `176` (`176`) | `694` (`cr694`, `cr788_fv371`) | — | `+2745` | **`680`** (`170, 197, 313`) | **`-14`** |
| **`4x4x8`** ($\mathbb{Z}_T$-best) | `96` (`95` over $\mathbb{Q}$) | `339` (`cr_val = 340`, `cr377_fv171`) | — | `+1027` | **`338`** (`73, 101, 164`) | **`-1` / `-2`** |
| **`3x3x6`** ($\mathbb{Z}_T$-best) | `43` (`40` over $\mathbb{Q}$) | `153` (`cr153`, `cr160`) | — | `+367` ($r=42$) | **`152`** (`32, 46, 74`) | **`-1`** |
