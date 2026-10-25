# Primary Status Tables & Live Snapshots (`fmm-additive-complexity-records`)

## 1. Live Sources Fetched Before Claiming (`2026-10-22T02:37:16Z` – `2026-10-22T02:38:44Z`) & Post-Opening Upstream Check (`2026-10-25T07:29:51Z`)

*(All third-party reference tables and `.json` files are cited below by URL, byte size, and SHA-256 digest rather than vendored in the package.)*

1. **Lille FMM SOTA Catalogue (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`):**
   - **Fetched UTC:** `2026-10-22T02:37:16Z` (`HTTP/2 200`)
   - **Byte Size:** `343,774` bytes
   - **SHA-256:** `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`
2. **Perminov's Live `FastMatrixMultiplication` Repository (`https://github.com/dronperminov/FastMatrixMultiplication`):**
   - **Directory snapshot before PR opening (`https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT`):** `2026-10-22T02:37:56Z` (`HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` `.json` files in `addition_reduced_ZT` prior to PR #616 opening at `2026-10-22T02:57Z`).
   - **`reduced_known.json` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json`):** `2026-10-22T02:38:44Z` (`HTTP/2 200`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`).
   - **Upstream reference `.json` files in `schemes/results/addition_reduced_ZT/` at PR opening (`2026-10-22T02:57Z`):**
     - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x6_m70_cr252_cn561_ZT_reduced.json` (`17,967` bytes, `sha256: 61d9be14020b7c2e2a5193b4a4c616e3414e53840d3d2c5a6a876af6836bc0f0`)
     - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x6_m70_cr265_cn561_ZT_reduced.json` (`17,027` bytes, `sha256: 4b5148d2af0c2ce96e809274b01011568fedd33687082859c2012c994b4379f9`)
     - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x6x6_m130_cr499_cn1716_ZT_reduced.json` (`37,336` bytes, `sha256: f1f3b7a40fee69e36ebe57f82ba2b1ac983fbacc7f4299cad39a47080f7f9a0b`)
     - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (`35,833` bytes, `sha256: 8f899e560b2d2976b031272c59ebf6ea0472ae2d9616eaeb05d52027d818344f`)
   - **Credited unreduced/naive source schemes in `dronperminov/FastMatrixMultiplication` used as input tensors:**
     - `3x3x7_m49_ZT.json`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`)
     - `3x5x6_m68_ZT.json`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`)
     - `3x5x7_m79_ZT.json`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`)
     - `5x6x6_m130_c1697_ZT.json`: `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`)
   - **Live `docs/additions.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md`):** fetched `2026-10-25T07:29:51Z` (`HTTP/2 200`, `sha256: df12f44f9180f4923f299656539648b557406ff7d9eb6e1633e030b0c3dfdc25`). When PR #616 opened at `2026-10-22T02:57Z`, upstream had no rank-49 file for `3x3x7`, no rank-68 file for `3x5x6`, and no rank-79 file for `3x5x7`, and `5x6x6` ($m=130$) stood at `cr = 499` (and `502` in V3R1T4S). Upstream commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`) was published **independently** by Alexander Perminov (`@dronperminov`) later that day and added files with matching counts (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, `3x5x6_m68_cr245_cn494_ZT_reduced.json`, `3x5x7_m79_cr294_cn520_ZT_reduced.json`, `5x6x6_m130_cr492_cn1697_ZT_reduced.json`).
3. **`matmulcatalog` Live `COVERAGE.md` (`https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md`):**
   - **Initial Snapshot UTC:** `2026-10-22T02:37:58Z` (`HTTP/2 200`, `94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`); current `COVERAGE.md` values at ranks `49`, `68`, `79`, `130` are `+404`, `+482`, `+520`, and `+1716`.
4. **IACR ePrint 2026/849 (`https://eprint.iacr.org/2026/849`, checked `2026-10-25T07:30:12Z`):**
   - Erik Mårtensson & Paul Stankovski Wagner, *"On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms"* (approved `2026-05-05`): checked on `2026-10-25T07:30:12Z`; the full PDF (`https://eprint.iacr.org/2026/849.pdf`) is unread as of `2026-10-25T07:30:12Z` (Cloudflare managed JS challenge returning HTTP 403 on automated fetch; only the HTML abstract page `https://eprint.iacr.org/2026/849` was read on `2026-10-25T07:30:12Z`).

## 2. Live Reference Values & Independent Upstream Ties for the 4 Record Formats

| Format | Rank $m$ (`fmm_sota.json`) | Credited Source Scheme | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Independent Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24:59Z`, `docs/additions.md`) | `matmulcatalog` `adds` | Our Record `cr` (`cu, cv, cw`) | Naive `cn` |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **`3x3x7`** | `49` (`49`) | `3x3x7_m49_ZT.json` | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, published independently) | `+404` ($r=49$) | **`167`** (`33, 53, 81`) | `404` |
| **`3x5x6`** | `68` (`68`) | `3x5x6_m68_ZT.json` | No `m=68` file (`m=70, cr=252`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`, published independently) | `+482` ($r=68$) | **`245`** (`56, 78, 111`) | `494` |
| **`3x5x7`** | `79` (`79`) | `3x5x7_m79_ZT.json` | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`, published independently) | `+520` ($r=79$) | **`294`** (`66, 97, 131`) | `520` |
| **`5x6x6`** | `130` (`130`) | `5x6x6_m130_c1697_ZT.json` | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`, published independently) | `+1716` ($r=130$) | **`492`** (`128, 139, 225`) | `1697` |
