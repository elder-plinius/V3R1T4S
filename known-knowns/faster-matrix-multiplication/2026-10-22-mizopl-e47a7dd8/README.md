# `fmm-additive-complexity-records` — 4 Certified Ternary Straight-Line Programs over $\mathbb{Z}$ (`3x3x7` $m=49$ `cr=167`, `3x5x6` $m=68$ `cr=245`, `3x5x7` $m=79$ `cr=294`, `5x6x6` $m=130$ `cr=492`) (`2026-10-22-mizopl-e47a7dd8`)

## What

4 explicit ternary (`ZT`) straight-line programs in `object/schemes/` (indexed in `object/CERTIFICATE.json`, `3,699` bytes, `sha256: 4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6`, and verified symbolically over $\mathbb{Z}[A, B]$ by `verify-it-yourself/verify.py`) establishing winning reduced addition counts $\text{cr} = c_u + c_v + c_w$ across 4 exact-SOTA-rank formats with $\max(n, m, p) \le 8$:
- **`3x3x7` ($m = 49$, `sota_rank = 49`):** `cr = 167` (`cu = 33, cv = 53, cw = 81`, `cn = 404`), synthesized from Perminov's unreduced source tensor `schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-49 file in Perminov's `addition_reduced_ZT` directory (best was rank `51` at `cr = 146`); a file with the same count (`167`) was published independently by Alexander Perminov (`@dronperminov`) upstream later that day in commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`, now listed in live `docs/additions.md`).
- **`3x5x6` ($m = 68$, `sota_rank = 68`):** `cr = 245` (`cu = 56, cv = 78, cw = 111`, `cn = 494`), synthesized from Perminov's unreduced source tensor `schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-68 file in Perminov's `addition_reduced_ZT` directory (best was rank `70` at `cr = 252`); a file with the same count (`245`) was published independently by Alexander Perminov (`@dronperminov`) upstream later that day in commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`, now listed in live `docs/additions.md`).
- **`3x5x7` ($m = 79$, `sota_rank = 79`):** `cr = 294` (`cu = 66, cv = 97, cw = 131`, `cn = 520`), synthesized from Perminov's unreduced source tensor `schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-79 file in Perminov's `addition_reduced_ZT` directory (best was rank `83` at `cr = 291`); a file with the same count (`294`) was published independently by Alexander Perminov (`@dronperminov`) upstream later that day in commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`, now listed in live `docs/additions.md`).
- **`5x6x6` ($m = 130$, `sota_rank = 130`):** `cr = 492` (`cu = 128, cv = 139, cw = 225`, `cn = 1697`), synthesized from Perminov's naive-reduced source tensor `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`), strictly below the `499` in Perminov's repository when this PR opened (`-7` additions) and below the `502` merged in V3R1T4S (`-10` additions); a file with the same count (`492`) was published independently by Alexander Perminov (`@dronperminov`) upstream later that day in commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`, now listed in live `docs/additions.md`).

### Summary Table of the 4 Record Programs (`object/schemes/`)

| Format | Rank $m$ (`fmm_sota`) | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Credited Source Scheme in `dronperminov/FastMatrixMultiplication` | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Independent Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24:59Z`, `docs/additions.md`) | `matmulcatalog` `adds` | Scheme File in `object/schemes/` | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| **`3x3x7`** | `49` (`49`) | **`167`** (`33, 53, 81`) | `404` | `3x3x7_m49_ZT.json` | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, published independently) | `+404` ($r=49$) | `3x3x7_m49_cr167_cn404_ZT_reduced.json` | `2f10739cd6200745967118e413c1433a1781a8db374eb3343c3fe92c7a7fc280` |
| **`3x5x6`** | `68` (`68`) | **`245`** (`56, 78, 111`) | `494` | `3x5x6_m68_ZT.json` | No `m=68` file (`m=70, cr=252`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`, published independently) | `+482` ($r=68$) | `3x5x6_m68_cr245_cn494_ZT_reduced.json` | `4271edeb86e3c452ebaa6edec9647590162e7093a0b4468b5c5dbc866acc850f` |
| **`3x5x7`** | `79` (`79`) | **`294`** (`66, 97, 131`) | `520` | `3x5x7_m79_ZT.json` | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`, published independently) | `+520` ($r=79$) | `3x5x7_m79_cr294_cn520_ZT_reduced.json` | `7aaaceef49b6d190b1a50d3779209c6b216bedef03578144602a8d3808c4e977` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `5x6x6_m130_c1697_ZT.json` | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`, published independently) | `+1716` ($r=130$) | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `< 0.5` seconds on CPU (`python3`, standard library only).

## Compared To

- **Target ID**: `fmm-additive-complexity-records` (`category: algorithms`, package directory `known-knowns/faster-matrix-multiplication/2026-10-22-mizopl-e47a7dd8/`)
- **Primary Status Tables & Reference Files (by URL and SHA-256; third-party files are not vendored in this package)**:
  - `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`2026-10-22T02:37:16Z`, `HTTP/2 200`, `343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`)
  - `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` (`2026-10-22T02:37:56Z`, `HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` files before PR opening at `2026-10-22T02:57Z`), `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` (`2026-10-22T02:38:44Z`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`), and live `docs/additions.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md`, fetched `2026-10-25T07:29:51Z`, `HTTP/2 200`, `sha256: df12f44f9180f4923f299656539648b557406ff7d9eb6e1633e030b0c3dfdc25`), reflecting upstream commit `1781ca392cb26808f88e6f92a26894ab3727910f` (`2026-10-22T15:24:59Z`) in which Alexander Perminov (`@dronperminov`) independently published files matching these four counts (`167`, `245`, `294`, `492`) later that day after this PR opened (`2026-10-22T02:57Z`).
  - Upstream reference `.json` files in `dronperminov/FastMatrixMultiplication` at PR opening (`2026-10-22T02:57Z`):
    - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x6_m70_cr252_cn561_ZT_reduced.json` (`17,967` bytes, `sha256: 61d9be14020b7c2e2a5193b4a4c616e3414e53840d3d2c5a6a876af6836bc0f0`)
    - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x6_m70_cr265_cn561_ZT_reduced.json` (`17,027` bytes, `sha256: 4b5148d2af0c2ce96e809274b01011568fedd33687082859c2012c994b4379f9`)
    - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x6x6_m130_cr499_cn1716_ZT_reduced.json` (`37,336` bytes, `sha256: f1f3b7a40fee69e36ebe57f82ba2b1ac983fbacc7f4299cad39a47080f7f9a0b`)
    - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (`35,833` bytes, `sha256: 8f899e560b2d2976b031272c59ebf6ea0472ae2d9616eaeb05d52027d818344f`)
  - `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (initial snapshot `2026-10-22T02:37:58Z`, `94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`; current `COVERAGE.md` values at ranks `49`, `68`, `79`, `130`: `+404`, `+482`, `+520`, `+1716`)
  - **IACR ePrint 2026/849** (Mårtensson & Stankovski Wagner, *"On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms"*, `https://eprint.iacr.org/2026/849`, checked `2026-10-25T07:30:12Z`): the full PDF (`https://eprint.iacr.org/2026/849.pdf`) is unread as of `2026-10-25T07:30:12Z` (behind a Cloudflare managed JS challenge returning HTTP 403 on automated fetch; only the HTML abstract page `https://eprint.iacr.org/2026/849` was read on `2026-10-25T07:30:12Z`).

## Not Claimed

- No multiplication rank $r$ is lowered beyond `fmm_sota.json`; all 4 schemes optimize the reduced addition complexity `cr = cu + cv + cw` over $\mathbb{Z}_T = \{-1, 0, +1\}$ for known ranks (`49`, `68`, `79`, `130`).
- Partial wins `p1` (`3x3x3` rank-23 below `55` additions) and `p2` (`4x4x4` rank-48 over $\mathbb{Q}$) are not claimed here.

## Credits

- **Credit**: `mizopl`
- **Source Tensors Credited**: Unreduced/naive ternary schemes from Alexander Perminov's (`@dronperminov`) `FastMatrixMultiplication` repository: `3x3x7_m49_ZT.json` (`schemes/results/ZT/3x3x7_m49_ZT.json`), `3x5x6_m68_ZT.json` (`schemes/results/ZT/3x5x6_m68_ZT.json`), `3x5x7_m79_ZT.json` (`schemes/results/ZT/3x5x7_m79_ZT.json`), and `5x6x6_m130_c1697_ZT.json` (`schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json`).
