# Primary Status Tables & Live Snapshots (`fmm-additive-complexity-records`)

## 1. Live Sources Fetched Before Claiming (`2026-10-22T02:37:16Z` – `2026-10-22T02:38:44Z`) & Post-Opening Upstream Check (`2026-10-25T07:29:51Z`)

1. **Lille FMM SOTA Catalogue (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`):**
   - **Fetched UTC:** `2026-10-22T02:37:16Z` (`HTTP/2 200`)
   - **Byte Size:** `343,774` bytes
   - **SHA-256:** `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`
   - **Saved Copy:** `the-record-we-beat/reference_live_champions/fmm_sota.json`
2. **Perminov's Live `FastMatrixMultiplication` Repository (`https://github.com/dronperminov/FastMatrixMultiplication`):**
   - **Directory snapshot before PR opening (`https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT`):** `2026-10-22T02:37:56Z` (`HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` `.json` files in `addition_reduced_ZT` prior to PR #616 opening at `2026-10-22T02:57Z`).
   - **`reduced_known.json` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json`):** `2026-10-22T02:38:44Z` (`HTTP/2 200`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`, saved at `the-record-we-beat/reference_live_champions/reduced_known.json`).
   - **Live `docs/additions.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md`):** fetched `2026-10-25T07:29:51Z` (`HTTP/2 200`, `sha256: df12f44f9180f4923f299656539648b557406ff7d9eb6e1633e030b0c3dfdc25`). When PR #616 opened at `2026-10-22T02:57Z`, upstream had no rank-49 file for `3x3x7`, no rank-68 file for `3x5x6`, and no rank-79 file for `3x5x7`, and `5x6x6` ($m=130$) stood at `cr = 499` (and `502` in V3R1T4S). Upstream commit `1781ca39` (`2026-10-22T15:24Z`) added files with matching counts (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, `3x5x6_m68_cr245_cn494_ZT_reduced.json`, `3x5x7_m79_cr294_cn520_ZT_reduced.json`, `5x6x6_m130_cr492_cn1697_ZT_reduced.json`) later that day.
3. **`matmulcatalog` Live `COVERAGE.md` (`https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md`):**
   - **Fetched UTC:** `2026-10-22T02:37:58Z` (`HTTP/2 200`, `94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`, saved at `the-record-we-beat/reference_live_champions/matmulcatalog_COVERAGE.md`).
4. **IACR ePrint 2026/849 (`https://eprint.iacr.org/2026/849`):**
   - Erik Mårtensson & Paul Stankovski Wagner, *"On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms"* (approved `2026-05-05`): the full PDF (`https://eprint.iacr.org/2026/849.pdf`) is unread (Cloudflare managed JS challenge on automated fetch; only the HTML abstract page was read).

## 2. Live Reference Values & Dated Upstream Ties for the 4 Record Formats

| Format | Rank $m$ (`fmm_sota.json`) | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Dated Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24Z`, `docs/additions.md`) | `matmulcatalog` `adds` | Our Record `cr` (`cu, cv, cw`) | Naive `cn` |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| **`3x3x7`** | `49` (`49`) | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`) | `+362` ($r=50$) | **`167`** (`33, 53, 81`) | `404` |
| **`3x5x6`** | `68` (`68`) | No `m=68` file (`m=70, cr=252`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`) | `+561` ($r=70$) | **`245`** (`56, 78, 111`) | `494` |
| **`3x5x7`** | `79` (`79`) | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`) | `+651` ($r=80$) | **`294`** (`66, 97, 131`) | `520` |
| **`5x6x6`** | `130` (`130`) | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`) | `+1716` | **`492`** (`128, 139, 225`) | `1697` |
