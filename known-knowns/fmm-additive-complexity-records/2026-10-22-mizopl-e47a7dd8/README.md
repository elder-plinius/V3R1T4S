# `fmm-additive-complexity-records` — 4 Certified Ternary Straight-Line Programs over $\mathbb{Z}$ (`3x3x7` $m=49$ `cr=167`, `3x5x6` $m=68$ `cr=245`, `3x5x7` $m=79$ `cr=294`, `5x6x6` $m=130$ `cr=492`) (`2026-10-22-mizopl-e47a7dd8`)

## What

4 explicit ternary (`ZT`) straight-line programs in `object/schemes/` (indexed in `object/CERTIFICATE.json`, `sha256: ede93f9030024c813dfb7ce8d1bdd3e3180fd2cdfab0691e552f30e81180b834`, and verified symbolically over $\mathbb{Z}[A, B]$ by `verify-it-yourself/verify.py`) establishing winning reduced addition counts $\text{cr} = c_u + c_v + c_w$ across 4 exact-SOTA-rank formats with $\max(n, m, p) \le 8$:
- **`3x3x7` ($m = 49$, `sota_rank = 49`):** `cr = 167` (`cu = 33, cv = 53, cw = 81`, `cn = 404`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-49 file in Perminov's repository (best was rank `51` at `cr = 146`); a file with the same count (`167`) appeared upstream later that day in commit `1781ca39` (`2026-10-22T15:24Z`, now listed in live `docs/additions.md`).
- **`3x5x6` ($m = 68$, `sota_rank = 68`):** `cr = 245` (`cu = 56, cv = 78, cw = 111`, `cn = 494`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-68 file in Perminov's repository (best was rank `70` at `cr = 252`); a file with the same count (`245`) appeared upstream later that day in commit `1781ca39` (`2026-10-22T15:24Z`, now listed in live `docs/additions.md`).
- **`3x5x7` ($m = 79$, `sota_rank = 79`):** `cr = 294` (`cu = 66, cv = 97, cw = 131`, `cn = 520`). When this PR opened (`2026-10-22T02:57Z`), there was no rank-79 file in Perminov's repository (best was rank `83` at `cr = 291`); a file with the same count (`294`) appeared upstream later that day in commit `1781ca39` (`2026-10-22T15:24Z`, now listed in live `docs/additions.md`).
- **`5x6x6` ($m = 130$, `sota_rank = 130`):** `cr = 492` (`cu = 128, cv = 139, cw = 225`, `cn = 1697`), strictly below the `499` in Perminov's repository when this PR opened (`-7` additions) and below the `502` merged in V3R1T4S (`-10` additions); a file with the same count (`492`) appeared upstream later that day in commit `1781ca39` (`2026-10-22T15:24Z`, now listed in live `docs/additions.md`).

### Summary Table of the 4 Record Programs (`object/schemes/`)

| Format | Rank $m$ (`fmm_sota`) | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Dated Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24Z`, `docs/additions.md`) | `matmulcatalog` `adds` | Scheme File in `object/schemes/` | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- | :--- | :---: | :--- | :--- |
| **`3x3x7`** | `49` (`49`) | **`167`** (`33, 53, 81`) | `404` | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`) | `+362` ($r=50$) | `3x3x7_m49_cr167_cn404_ZT_reduced.json` | `2f10739cd6200745967118e413c1433a1781a8db374eb3343c3fe92c7a7fc280` |
| **`3x5x6`** | `68` (`68`) | **`245`** (`56, 78, 111`) | `494` | No `m=68` file (`m=70, cr=252`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`) | `+561` ($r=70$) | `3x5x6_m68_cr245_cn494_ZT_reduced.json` | `4271edeb86e3c452ebaa6edec9647590162e7093a0b4468b5c5dbc866acc850f` |
| **`3x5x7`** | `79` (`79`) | **`294`** (`66, 97, 131`) | `520` | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`) | `+651` ($r=80$) | `3x5x7_m79_cr294_cn520_ZT_reduced.json` | `7aaaceef49b6d190b1a50d3779209c6b216bedef03578144602a8d3808c4e977` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`) | `+1716` | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `< 0.5` seconds on CPU (`python3`, standard library only).

## Compared To

- **Target ID**: `fmm-additive-complexity-records` (`category: algorithms`)
- **Primary Status Tables**:
  - `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`2026-10-22T02:37:16Z`, `HTTP/2 200`, `343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`)
  - `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` (`2026-10-22T02:37:56Z`, `HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` files before PR opening at `2026-10-22T02:57Z`), `reduced_known.json` (`2026-10-22T02:38:44Z`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`), and live `docs/additions.md` (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md`, fetched `2026-10-25T07:29:51Z`, `HTTP/2 200`, `sha256: df12f44f9180f4923f299656539648b557406ff7d9eb6e1633e030b0c3dfdc25`), reflecting upstream commit `1781ca39` (`2026-10-22T15:24Z`) which added ties for these four counts (`167`, `245`, `294`, `492`) later that day after this PR opened (`2026-10-22T02:57Z`).
  - `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (`2026-10-22T02:37:58Z`, `HTTP/2 200`, `94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`)
  - **IACR ePrint 2026/849** (Mårtensson & Stankovski Wagner, *"On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms"*, `https://eprint.iacr.org/2026/849`): the full PDF (`https://eprint.iacr.org/2026/849.pdf`) is unread (behind a Cloudflare managed JS challenge on automated fetch; only the HTML abstract page was read).

## Not Claimed

- No multiplication rank $r$ is lowered beyond `fmm_sota.json`; all 4 schemes optimize the reduced addition complexity `cr = cu + cv + cw` over $\mathbb{Z}_T = \{-1, 0, +1\}$ for known ranks (`49`, `68`, `79`, `130`).
- Partial wins `p1` (`3x3x3` rank-23 below `55` additions) and `p2` (`4x4x4` rank-48 over $\mathbb{Q}$) are not claimed here.

## Credits

- **Credit**: `mizopl`
