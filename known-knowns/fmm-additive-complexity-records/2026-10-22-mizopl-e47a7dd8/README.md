# `fmm-additive-complexity-records` — 48 Certified Ternary Straight-Line Programs over $\mathbb{Z}$ with New Minimum Reduced Addition Counts Across 9 Exact-SOTA-Rank Formats, 2 $\mathbb{Z}_T$-Best Formats, & 21 Newly Addition-Reduced SOTA-Rank Formats (`2026-10-22-mizopl-e47a7dd8`)

## What

48 explicit ternary (ZT) straight-line programs in claim/schemes/ (indexed in claim/CERTIFICATE.json, sha256 e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de, and verified symbolically over Z[A, B] by claim/verify.py, sha256 d0a557971cd72c8c588d4a35e31b9f2135c5e421ef6caddb64a940a02f695c40) establishing strictly lower reduced addition counts cr = cu + cv + cw below the live minimum cr across all files in Perminov's addition_reduced_ZT repository, reduced_known.json, Lille catalogue, and matmulcatalog COVERAGE.md for 9 distinct exact-SOTA-rank formats with max(n, m, p) <= 8 (2x4x7 m=45: cr=157 and 164 vs 168, -11; 2x5x5 m=40: cr=145 vs 147, -2; 4x5x8 m=118: cr=447 vs 466, -19; 4x6x7 m=123: cr=464 vs 468, -4; 5x5x6 m=110: cr=406 vs 411, -5; 5x5x8 m=144: cr=548 vs 555, -7; 5x6x6 m=130: cr=492 vs 499, -7; 5x6x7 m=150: cr=573 and 576 vs 577, -4; 5x7x7 m=176: cr=680 vs 694, -14; satisfying both the full success criterion and partial win p3 >= 3 formats by 3x), plus 2 ZT-best formats (4x4x8 m=96: cr=338 vs 339/340; 3x3x6 m=43: cr=152 vs 153) and 21 newly addition-reduced exact-SOTA-rank ZT formats (6 of which also beat the older higher-rank cr: 2x6x6 m=56 cr=221, 3x5x6 m=68 cr=245, 3x6x8 m=108 cr=381, 4x7x8 m=161 cr=625, 4x8x8 m=180 cr=734, 5x7x8 m=204 cr=835).

### Summary Table of the 9 Exact-SOTA-Rank Wins & 2 $\mathbb{Z}_T$-Best Wins (`object/schemes/`)

| Format | Rank $m$ (`fmm_sota`) | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Live `addition_reduced_ZT` Min `cr` (All Files) | `matmulcatalog` `adds` | Delta vs Live Min `cr` | Scheme File in `object/schemes/` | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **`2x4x7`** | `45` (`45`) | **`157`** (`26, 58, 73`) | `345` | `168` (`cr168`, `cr174`) | `+308` | **`-11`** (`-6.55%`) | `2x4x7_m45_cr157_cn345_ZT_reduced.json` | `13925cb4e3fef5c3e0a79d18855b4a16ef3a0f361923e4f53fa835b9df231840` |
| **`2x4x7`** (var. 2) | `45` (`45`) | **`164`** (`27, 64, 73`) | `285` | `168` (`cr168`, `cr174`) | `+308` | **`-4`** (`-2.38%`) | `2x4x7_m45_cr164_cn285_ZT_reduced.json` | `2d85f22f397ead7f6895ecaf7645a83aacc429c857b3a9f4cebe2e42110c7730` |
| **`2x5x5`** | `40` (`40`) | **`145`** (`28, 58, 59`) | `273` | `147` (`cr147`, `cr153`; `rk`: `Z=313, Z2=218`) | `+256` | **`-2`** (`-1.36%`) | `2x5x5_m40_cr145_cn273_ZT_reduced.json` | `c7e30b3f2d2eb218e6015b88ad44e4e3631a41832237f48c5351514ac9eb9c3a` |
| **`4x5x8`** | `118` (`118`) | **`447`** (`96, 141, 210`) | `1463` | `466` (`cr466`, `cr513_fv249`) | `+1521` | **`-19`** (`-4.08%`) | `4x5x8_m118_cr447_cn1463_ZT_reduced.json` | `6a20a2b001f5255155c8a4da0d93bc8b2fd9562f03ddccea8ed0b4180287022d` |
| **`4x6x7`** | `123` (`123`) | **`464`** (`112, 138, 214`) | `1562` | `468` (`cr468`, `cr517`) | `+1586` | **`-4`** (`-0.85%`) | `4x6x7_m123_cr464_cn1562_ZT_reduced.json` | `2b78b41c57f3b26640504a2fbc2fbc555a85dc0b535f1b19e40b0aab56e2e082` |
| **`5x5x6`** | `110` (`110`) | **`406`** (`105, 110, 191`) | `1192` | `411` (`cr411`, `cr460_fv204`) | `+1215` | **`-5`** (`-1.22%`) | `5x5x6_m110_cr406_cn1192_ZT_reduced.json` | `4cbc3596ab458b161d627f90cf2969eac1f9926844eb2d1bcda0702cc7d20ffe` |
| **`5x5x8`** | `144` (`144`) | **`548`** (`130, 156, 262`) | `1872` | `555` (`cr555`, `cr620_fv281`) | `+1908` | **`-7`** (`-1.26%`) | `5x5x8_m144_cr548_cn1872_ZT_reduced.json` | `26e8fee0b3ca63a807b866972ea65448afba7d4188c09fd18b9f249e5c964244` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `499` (`cr499`, `cr562_fv250`) | `+1716` | **`-7`** (`-1.40%`) | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` |
| **`5x6x7`** | `150` (`150`) | **`573`** (`143, 165, 265`) | `1994` | `577` (`cr577`, `cr664_fv310`) | `+2039` | **`-4`** (`-0.69%`) | `5x6x7_m150_cr573_cn1994_ZT_reduced.json` | `e7b7f15ceb2237c93ba7ac363c3f70bf0bd520b669ff32d0595bd57a716059d4` |
| **`5x6x7`** (var. 2) | `150` (`150`) | **`576`** (`144, 168, 264`) | `2039` | `577` (`cr577`, `cr664_fv310`) | `+2039` | **`-1`** (`-0.17%`) | `5x6x7_m150_cr576_cn2039_ZT_reduced.json` | `e2e3d0b05e3e142fb07b104f45c2dbbcd6eb48b9c071ca1acbdaaf95766220b2` |
| **`5x7x7`** | `176` (`176`) | **`680`** (`170, 197, 313`) | `2535` | `694` (`cr694`, `cr788_fv371`) | `+2745` | **`-14`** (`-2.02%`) | `5x7x7_m176_cr680_cn2535_ZT_reduced.json` | `d8735ca9ebf4adf6a4bac9ab5af0906aafdc5247f80ec0a62f4507014e749d39` |
| **`4x4x8`** ($\mathbb{Z}_T$-best) | `96` (`95` over $\mathbb{Q}$) | **`338`** (`73, 101, 164`) | `962` | `339` (`cr_val = 340`, `cr377_fv171`) | `+1027` | **`-1` / `-2`** | `4x4x8_m96_cr338_cn962_ZT_reduced.json` | `eae682903920cd0ad9b3fda33f483b23cefaf1612e089e175367ba50249d1ae4` |
| **`3x3x6`** ($\mathbb{Z}_T$-best) | `43` (`40` over $\mathbb{Q}$) | **`152`** (`32, 46, 74`) | `286` | `153` (`cr153`, `cr160`) | `+367` ($r=42$) | **`-1`** (`-0.65%`) | `3x3x6_m43_cr152_cn286_ZT_reduced.json` | `1753cc9f70d6d518d22bd8612c21de2d35db0b05b9ecc42f5de9e4b8bdbec136` |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~2.0` seconds on CPU (`python3`, standard library only).

## Compared To

- **Target ID**: `fmm-additive-complexity-records` (`category: algorithms`)
- **Primary Status Tables**:
  - `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`2026-10-22T02:37:16Z`, `HTTP/2 200`, `343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`)
  - `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` (`2026-10-22T02:37:56Z`, `HTTP/2 200`, `431,121` bytes, `sha256: a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6`, `329` files) and `reduced_known.json` (`2026-10-22T02:38:44Z`, `1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`)
  - `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (`2026-10-22T02:37:58Z`, `HTTP/2 200`, `94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`)

## Not Claimed

- No multiplication rank $r$ is lowered beyond `fmm_sota.json`; all 48 schemes optimize the reduced addition complexity `cr = cu + cv + cw` over $\mathbb{Z}_T = \{-1, 0, +1\}$ for known ranks.
- Partial wins `p1` (`3x3x3` rank-23 below `55` additions; our `3x3x3_m23_cr55_cn122_ZT_reduced.json` matches the live record `55` and beats the secondary `56..60` files) and `p2` (`4x4x4` rank-48 over $\mathbb{Q}$) are not claimed here.

## Credits

- **Credit**: `mizopl`
