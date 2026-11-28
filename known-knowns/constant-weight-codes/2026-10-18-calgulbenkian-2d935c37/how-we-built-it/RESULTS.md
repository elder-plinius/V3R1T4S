# Constant-Weight Codes (`Andw.html`) Attack — Verified Results (`p2` + `p1` + Full Win)

## Executive Summary

Against the frozen baseline snapshot [`data/Andw.html`]({WORKDIR}/data/Andw.html) (`SHA-256: bc8822714c5d0f6414f158e6f0dad6529b9253aaf33b6b4a4c620105ee7e3653`), we achieved **all three goals (`p2` + `p1` + Full Win)** with 100% standalone exact verification via [`verify_cwc.py`]({WORKDIR}/verify_cwc.py):

1. **Goal A — Partial Win `p2` (21 Cells / 22 Certificates in `results/certificates/`)**:
   - **Family A1 (11 cells / 12 certificates)**: Exact rational Delsarte + support-split ($R_x$) + shortening ($M_{1,s}$) LP upper-bound certificates strictly beating explicitly printed `lo-hi` upper bounds in `data/Andw.html` (excluding `(31,10,7)` and the 5 already-merged `L` cells).
   - **Family A2 (10 cells / 10 certificates)**: Pure Delsarte LP certificates ($D_1, \dots, D_w$ **only**, zero table inputs) strictly beating the iterated Johnson upper bound on unmarked $n > 28$ cells in `data/Andw.html`.
2. **Goal B — Partial Win `p1` (8 Explicit Codes in `results/codes_p1/`)**:
   - First explicit binary constant-weight code files matching $M = L_{\text{table}}$ for **8 cells** in `data/Andw.html` whose lower bounds are unlinked 1990 `[BSSS]` citations (neither $(n, d, w)$ nor $(n, d, n-w)$ has an `href="cwc/..."` link in `data/Andw.html`, and none appear in `arXiv:2607.19550` or `arXiv:2608.13906`).
3. **Goal C — Full Win (13 Explicit Record-Breaking Codes in `results/codes_full_win/`)**:
   - **13 explicit constant-weight codes** strictly beating today's live `data/Andw.html` lower bounds ($M > \max(L_{\text{table}}(n,d,w), L_{\text{table}}(n,d,n-w))$), also strictly beating `arXiv:2608.13906` (Echols) and `arXiv:2607.19550` (Lysenstoen).
   - Includes **4 brand-new record cells** discovered via degree-sorted coordinate relabeling + LNS (`A(28,8,11) >= 3802` [+17], `A(51,6,6) >= 11187` [+3], `A(25,6,11) >= 8720` [+2], `A(27,8,11) >= 2422` [+1]) that were untouched in `cg_repo.git`, plus **3 further improvements** strictly above prior unmerged LNS records (`A(54,8,7) >= 4205` [+12], `A(45,8,7) >= 1913` [+6], `A(55,8,7) >= 4432` [+6]).

---

## Goal C — Full Win: 13 Explicit Constant-Weight Codes Strictly Beating Live `Andw.html` Lower Bounds

All 13 codes are stored in `results/codes_full_win/` (and mirrored in `results/`) and verified by `python3 verify_cwc.py results/codes_full_win/*.txt`:

| # | Cell $(n, d, w)$ | Live `Andw.html` | Echols `2608.13906` | Lysenstoen `2607.19550` | **New Verified $M$** | **Gain vs `Andw.html`** | File (`results/codes_full_win/`) | SHA-256 (prefix) |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | `A(28, 8, 11)` | `3785Pl-16354` | `3716` | — | **`3802`** | **`+17`** (New cell!) | `A28_8_11_3802.txt` | `9bec8e442ef7b35e` |
| 2 | `A(54, 8, 7)` | `4193Pl-8447` | — | `4176` | **`4205`** | **`+12`** (+1 over LNS) | `A54_8_7_4205.txt` | `765069602e766f6c` |
| 3 | `A(26, 6, 9)` | `5986Pl-16122` | `5909` | — | **`5997`** | **`+11`** | `A26_6_9_5997.txt` | `6be5a215f0b66249` |
| 4 | `A(45, 8, 7)` | `1907Pl-4050` | — | `1901` | **`1913`** | **`+6`** (+3 over LNS) | `A45_8_7_1913.txt` | `7da959051e830cb6` |
| 5 | `A(55, 8, 7)` | `4426Pl-9617` | — | `4410` | **`4432`** | **`+6`** (+1 over LNS) | `A55_8_7_4432.txt` | `50a6e273e744067f` |
| 6 | `A(56, 8, 7)` | `4685Pl-10264` | — | `4669` | **`4691`** | **`+6`** | `A56_8_7_4691.txt` | `e12d11fa604fd790` |
| 7 | `A(53, 8, 7)` | `3987Pl-8003` | — | `3973` | **`3992`** | **`+5`** | `A53_8_7_3992.txt` | `7be7a08730ebb932` |
| 8 | `A(51, 6, 6)` | `11184Pl-19937` | — | `11157` | **`11187`** | **`+3`** (New cell!) | `A51_6_6_11187.txt` | `3684474037a4c998` |
| 9 | `A(52, 8, 7)` | `3799Pl-7577` | — | `3787` | **`3802`** | **`+3`** | `A52_8_7_3802.txt` | `4743db7cec4929d0` |
| 10 | `A(27, 8, 10)` | `1737Pl-4986` | `1719` | — | **`1740`** | **`+3`** | `A27_8_10_1740.txt` | `bdbf1cf2b34d5a27` |
| 11 | `A(25, 6, 11)` | `8718Pl-22575` | `8665` | — | **`8720`** | **`+2`** (New cell!) | `A25_6_11_8720.txt` | `46ae5613f60a668e` |
| 12 | `A(27, 8, 11)` | `2421Pl-12266` | `2386` | — | **`2422`** | **`+1`** (New cell!) | `A27_8_11_2422.txt` | `1ce741658d4881c2` |
| 13 | `A(35, 6, 6)` | `2217Pl-3249` | — | `2204` | **`2218`** | **`+1`** | `A35_6_6_2218.txt` | `dd2eb057e40bc19b` |

---

## Goal A — Partial Win `p2`: 21 Cells (22 Certificates) Beating `Andw.html` Upper Bounds in Exact Rational Arithmetic

All 22 certificates in `results/certificates/` are verified in 100% exact `fractions.Fraction` arithmetic (`python3 verify_cwc.py --delsarte results/certificates/*.json`), including $P Q = \binom{n}{w} I$ orthogonality and primal==dual LP optimality.

### Family A1 — 11 Cells (12 Certificates) Beating Explicitly Printed `lo-hi` Upper Bounds in `Andw.html`

| # | Cell $(n, d, w)$ | Printed in `Andw.html` | Table $U_{\text{table}}$ | **Certified $U$** | **Improvement** | Exact Rational Optimum | Active Constraints & Table Inputs | Certificate File | SHA-256 (prefix) |
|---|---|---|---:|---:|---:|---|---|---|---|
| 1 | `A(32, 10, 7)` | `64c-139` | `139` | **`131`** | **`-8`** | `46624/355` (`131.3352`) | `D1, D2, R7` (`A(25,10,7)<=32`, printed `28-32` & unconditional via `floor(25/7 * A(24,10,6))=32`) | `cert_A32_10_7.json` | `c616b821f22eee5a` |
| 2 | `A(33, 10, 7)` | `72g-150` | `150` | **`145`** | **`-5`** | `26928/185` (`145.5568`) | `D1, D2, R7` (`A(26,10,7)<=36`, printed `30-36`) | `cert_A33_10_7.json` | `63f2e39ea6a9e76c` |
| 3 | `A(33, 10, 8)` | `165-573` | `573` | **`530`** | **`-43`** | `13266/25` (`530.6400`) | `D1, M1_0` (`A(32,10,8)<=402`, printed `145-402Po`) | `cert_A33_10_8.json` | `6765c783c92aabfe` |
| 4 | `A(34, 10, 7)` | `85E-160` | `160` | **`155`** | **`-5`** | `1088/7` (`155.4286`) | `D1, M1_1` (`A(33,10,6)<=32`, printed `31-32`) | `cert_A34_10_7.json` | `2c448c74db74ca1d` |
| 5a | `A(34, 10, 8)` | `181g-637` | `637` | **`618`** | **`-19`** | `114444/185` (`618.6162`) | `D1, D2, D3, R7` (`A(26,10,7)<=36`, printed `30-36`, standalone) | `cert_A34_10_8.json` | `f8d221d5346407a0` |
| 5b | `A(34, 10, 8)` | `181g-637` | `637` | **`616`** | **`-21`** | `2465/4` (`616.2500`) | `D1, M1_1` (`A(33,10,7)<=145`, cascaded from `cert_A33_10_7.json`) | `cert_A34_10_8_cascaded.json` | `7627d23cd79a1620` |
| 6 | `A(35, 10, 8)` | `210c-700` | `700` | **`678`** | **`-22`** | `5425/8` (`678.1250`) | `D1, M1_1` (`A(34,10,7)<=155`, cascaded from `cert_A34_10_7.json`) | `cert_A35_10_8.json` | `a0d7da5fc326b41a` |
| 7 | `A(42, 12, 8)` | `105g-157` | `157` | **`152`** | **`-5`** | `609/4` (`152.2500`) | `D1, M1_1` (`A(41,12,7)<=29`, printed `26-29`) | `cert_A42_12_8.json` | `557f303663298c46` |
| 8 | `A(43, 12, 8)` | `111sb-192` | `192` | **`182`** | **`-10`** | `731/4` (`182.7500`) | `D1, M1_1` (`A(42,12,7)<=34`, printed `30-34`) | `cert_A43_12_8.json` | `6c9d8c696ef08ad4` |
| 9 | `A(44, 12, 8)` | `124sb-234` | `234` | **`209`** | **`-25`** | `209` (`209.0000`) | `D1, M1_1` (`A(43,12,7)<=38`, printed `32-38`) | `cert_A44_12_8.json` | `1245d2003d6ae4a0` |
| 10 | `A(47, 10, 7)` | `333Bo-462` | `462` | **`449`** | **`-13`** | `3149/7` (`449.8571`) | `D1, M1_1` (`A(46,10,6)<=67`, printed `60-67`) | `cert_A47_10_7.json` | `5bca96f0b37f3707` |
| 11 | `A(48, 10, 8)` | `905Bo-2772` | `2772` | **`2694`** | **`-78`** | `2694` (`2694.0000`) | `D1, M1_1` (`A(47,10,7)<=449`, cascaded from `cert_A47_10_7.json`) | `cert_A48_10_8.json` | `87462bcff1c308b6` |

### Family A2 — 10 Pure Delsarte LP Certificates (`D1..Dw` Only, Zero Table Inputs) Beating Iterated Johnson Upper Bounds on Unmarked `n > 28` Cells

| # | Cell $(n, d, w)$ | Printed in `Andw.html` | Iterated Johnson UB | **Certified Pure Delsarte $U$** | **Improvement vs Johnson** | Exact Rational Optimum | Active Constraints | Certificate File | SHA-256 (prefix) |
|---|---|---|---:|---:|---:|---|---|---|---|
| 12 | `A(29, 6, 11)` | `41219Pl-...` | `167926` | **`164749`** | **`-3,177`** | `164749` (`164749.0000`) | `D1..D8, D11` | `cert_A29_6_11.json` | `18f3c75f26d7a11d` |
| 13 | `A(29, 6, 12)` | `61823Pl-...` | `242434` | **`228441`** | **`-13,993`** | `12564279/55` (`228441.4364`) | `D1..D9, D12` | `cert_A29_6_12.json` | `870c67a9911cf7f5` |
| 14 | `A(29, 6, 13)` | `80837gs-...` | `297646` | **`289604`** | **`-8,042`** | `10715355/37` (`289604.1892`) | `D1..D9, D13` | `cert_A29_6_13.json` | `2d935c37e2b197f8` |
| 15 | `A(29, 6, 14)` | `92366gs-...` | `328162` | **`322266`** | **`-5,896`** | `6123060/19` (`322266.3158`) | `D1..D9, D13, D14` | `cert_A29_6_14.json` | `476121c35ae79408` |
| 16 | `A(32, 14, 14)` | `62` (unmarked UB) | `294` | **`233`** | **`-61`** | `12400/53` (`233.9623`) | `D1, D2, D3` | `cert_A32_14_14.json` | `49f5dd3e003afee1` |
| 17 | `A(33, 14, 14)` | `64` (unmarked UB) | `431` | **`348`** | **`-83`** | `16368/47` (`348.2553`) | `D1, D2, D3` | `cert_A33_14_14.json` | `0189cfa6f025a7f0` |
| 18 | `A(34, 14, 14)` | `68` (unmarked UB) | `726` | **`591`** | **`-135`** | `208692/353` (`591.1955`) | `D1, D2, D3, D4` | `cert_A34_14_14.json` | `55b19855bbe54648` |
| 19 | `A(35, 12, 12)` | `267` (unmarked UB) | `3161` | **`2777`** | **`-384`** | `48694800/17531` (`2777.6396`) | `D1..D5` | `cert_A35_12_12.json` | `6b189cf6925d08bb` |
| 20 | `A(35, 14, 14)` | `70` (unmarked UB) | `1207` | **`837`** | **`-370`** | `56100/67` (`837.3134`) | `D1..D4` | `cert_A35_14_14.json` | `5782329f280871cd` |
| 21 | `A(36, 12, 12)` | `322` (unmarked UB) | `4275` | **`3613`** | **`-662`** | `589050/163` (`3613.8037`) | `D1..D5` | `cert_A36_12_12.json` | `f6f8d503de8169cf` |

---

## Goal B — Partial Win `p1`: 8 Explicit Constant-Weight Codes for Unlinked 1990 `[BSSS]` Citations

All 8 codes in `results/codes_p1/` match $M = L_{\text{table}}$ on cells where neither $(n, d, w)$ nor $(n, d, n-w)$ has an `href="cwc/..."` link in `data/Andw.html` (and none are in `arXiv:2607.19550` or `arXiv:2608.13906`):

| # | Cell $(n, d, w)$ | Printed in `Andw.html` | **Verified $M$** | Actual $\min d_H$ | Algebraic / Combinatorial Construction | File (`results/codes_p1/`) | SHA-256 (prefix) |
|---|---|---|---:|---:|---|---|---|
| 1 | `A(21, 10, 10)` | `38-42` (unlinked `[BSSS]`) | **`38`** | `10` | Paley Hadamard $H_{20}$ ($q=19 \equiv 3 \pmod 4$) rows & complements embedded into $n=21$ | `A21_10_10_38.txt` | `d1e0ca790e503119` |
| 2 | `A(23, 8, 6)` | `77-80` (unlinked `[BSSS]`) | **`77`** | `8` | 77 hexads of derived Witt design $S(3, 6, 22)$ from $[23,12,7]$ Golay code embedded into $n=23$ | `A23_8_6_77.txt` | `f670127c543f509f` |
| 3 | `A(24, 12, 12)` | `46^H` (unlinked `[BSSS]`) | **`46`** | `12` | Paley Hadamard $H_{24}$ ($q=23 \equiv 3 \pmod 4$) non-constant rows & complements | `A24_12_12_46.txt` | `ec2f873a0b1ecdad` |
| 4 | `A(24, 8, 7)` | `253-274` (unlinked `[BSSS]`) | **`253`** | `8` | 253 heptads of Witt design $S(4, 7, 23)$ (weight-7 words of $[23,12,7]$ Golay code) in $n=24$ | `A24_8_7_253.txt` | `98324034d84ca5a9` |
| 5 | `A(25, 8, 8)` | `759-850Po` (unlinked `[BSSS]`) | **`759`** | `8` | 759 octads of extended binary Golay Steiner system $S(5, 8, 24)$ embedded into $n=25$ | `A25_8_8_759.txt` | `e1f62ccd348e9e4e` |
| 6 | `A(28, 12, 9)` | `39-45` (unlinked `[BSSS]`) | **`39`** | `12` | 39 affine planes (size 9, max intersection 3) of $AG(3, 3) = \mathbb{F}_3^3$ on 27 points in $n=28$ | `A28_12_9_39.txt` | `ef63c0c1fc7aac61` |
| 7 | `A(28, 14, 14)` | `54^H` (unlinked `[BSSS]`) | **`54`** | `14` | Paley Type-I Hadamard matrix $H_{28}$ over $\mathbb{F}_{27} = \mathbb{F}_3[x]/(x^3-x+1)$ | `A28_14_14_54.txt` | `952f3ca643762adc` |
| 8 | `A(30, 14, 14)` | `58-95Po` (unlinked `[BSSS]`) | **`58`** | `14` | 29 cyclic shifts of QR + 29 cyclic shifts of QNR mod $29$ ($q=29 \equiv 1 \pmod 4$) in $n=30$ | `A30_14_14_58.txt` | `e38245e64026afec` |
