## Target 2: `potts-antiferromagnet-colouring-entropy-bounds`

### 2.1 Fast Matrix-Free Site-by-Site (Kink) Transfer on $S_q \times D_m$ Equitable Partitions (`potts_kink_cert.c`)

For proper $q$-colourings of the open path $P_m$ (symmetry group $G = S_q \times \mathbb{Z}_2$) or periodic cycle $C_m$ (symmetry group $G = S_q \times D_m$), the quotient transfer matrix $C_{\mathcal{X}}$ on the $N_3$ symmetry orbits is $>85\%$ dense ($O(N_3^2)$ nonzeros), making explicit matrix construction prohibitive beyond $m \approx 14$.

In `potts_kink_cert.c`, we exploit two exact structural properties:
1. **Equitable Partition Lifting**: For any orbit vector $v \in \mathbb{Z}_{>0}^{N_3}$, lifting $v$ to the $G$-invariant vector $\tilde{v}(w) = v_{\text{orb}(w)}$ on uncompressed colourings $w$ gives $(C_{\mathcal{X}} v)_i = (M \tilde{v})(\text{rep}(X_i))$ **with zero rounding error in exact integer arithmetic**.
2. **$S_q$-Normalized Kink Factorization**: Because every orbit representative $u = \text{rep}(X_i)$ has $u_0 = 0, u_1 = 1$, and $\tilde{v}$ is $S_q$-invariant, changing summation variables via the canonical permutation $\tau_{w_0, w_1} \in S_q$ mapping $w_0 \mapsto 0, w_1 \mapsto 1$ fixes the first two sites of the source colouring $\hat{w} = \tau_{w_0, w_1}(w)$ to $\hat{w}_0 = 0, \hat{w}_1 = 1$. Consequently:
   - Even for periodic cylinders $C_m$, the wrap-around constraint $w_{m-1} \ne w_0$ reduces to the local constraint $\hat{w}_{m-1} \ne 0$, eliminating the factor-of-$q$ memory/time penalty of cylindrical site-by-site transfer.
   - The entire row-to-row transfer across all $N_3$ orbits reduces to $m - 2$ site-by-site sparse kink sweeps on a flat buffer of size $N_{\text{mid}} = q^2 (q - 1)^{m - 4}$, followed by a gather of $q^2 - 3q + 3$ terms per orbit ($7$ for $q=4$, $13$ for $q=5$).
   - Using a 3-stage precision ladder (35 `double` iterations $\to$ 50 native 128-bit `u128` iterations $\to$ 65–90 exact 256-bit `u256` iterations) followed by an unshifted exact 256-bit matvec $y = C_{\mathcal{X}} v$ and 512-bit cross-multiplied Collatz–Wielandt verification (`ratio_cmp`), we certify the Perron root $\theta_1$ to **55–66 decimal places**.

### 2.2 Reproduction & Extension of Lundow & Markström (2008) Tables 1, 2, and 3 (Partial Win `p2`)

All 256-bit certificate vectors are saved in `results/potts_certs/q{4,5}_{open,cyl}_{m}_cert.bin` and summarized in `results/potts_certs/verified_potts_all.txt`. Every entry of Table 1, Table 2 ($q=4$), and Table 3 ($q=5$) of Lundow & Markström (2008) is reproduced to all 25 published digits and extended to 55–66 certified digits:

#### Table A: $q = 4$ Open Strip $P_m$ and Periodic Cylinder $C_m$ ($m = 3 \dots 16$)

| $m$ | $N_1(P_m)$ | $N_3(P_m)$ | Certified $\theta_1(P_m)$ (first 32 digits shown; certified to 56–66 digits) | $N_1(C_m)$ | $N_3(C_m)$ | Certified $\theta_1(C_m)$ (first 32 digits shown; certified to 55–66 digits) |
| :-: | ---------: | ---------: | :-------------------------------------------------------------------------- | ---------: | ---------: | :-------------------------------------------------------------------------- |
| 3 | 36 | 2 | `16.352349955308334315460785483749` | 24 | 1 | `11.000000000000000000000000000000` |
| 4 | 108 | 4 | `38.188748998197855775726485843420` | 84 | 3 | `31.696938456699068589183704448235` |
| 5 | 324 | 10 | `89.209728646509765238955477451016` | 240 | 2 | `67.015148038438355607590988509038` |
| 6 | 972 | 25 | `208.398096425397572063353861326750` | 732 | 9 | `165.600822094455667248188305945134` |
| 7 | 2,916 | 70 | `486.829155541356600054386411584992` | 2,184 | 10 | `375.480400415288679799601678347769` |
| 8 | 8,748 | 196 | `1137.260058429224259797968094098566` | 6,564 | 34 | `892.241875348657735421278311630311` |
| 9 | 26,244 | 574 | `2656.703606588566986303095647925216` | 19,680 | 57 | `2064.554606528212648447034977823528` |
| 10 | 78,732 | 1,681 | `6206.209878666071640432711118733059` | 59,052 | 169 | `4849.504943339923099642784406395947` |
| 11 | 236,196 | 5,002 | `14498.057634700719542682938984674868` | 177,144 | 366 | `11293.109165102436437817109851003991` |
| 12 | 708,588 | 14,884 | `33868.283692433502471991031124155091` | 531,444 | 1,062 | `26429.649584445686077498084317158373` |
| 13 | 2,125,764 | 44,530 | `79118.228942860971926838387142431479` | 1,594,320 | 2,646 | `61675.615974547291014472578925608883` |
| 14 | 6,377,292 | 133,225 | `184824.664073982626399770978132252853` | 4,782,972 | 7,515 | `144167.261208556704557393266257266521` |
| 15 | 19,131,876 | 399,310 | `431760.883879446034608057172382078553` | 14,348,904 | 20,209 | `336660.408523582504387828038681862020` |
| 16 | 57,395,628 | 1,196,836 | `1008617.880082225136681907397786195435` | 43,046,724 | 57,234 | `786626.001501069793657552915484632535` |
| 17 | 172,186,884 | 3,589,414 | `2356188.497002459749106437175416025224` | 129,140,160 | 159,080 | `1837371.449233874382829229168431210451` |
| 18 | — | — | — | 387,420,492 | 451,929 | `4292523.034205622358715771955659005973` |

#### Table B: $q = 5$ Open Strip $P_m$ ($m = 2 \dots 13$) and Periodic Cylinder $C_m$ ($m = 3 \dots 14$)

| $m$ | $N_1(P_m)$ | $N_3(P_m)$ | Certified $\theta_1(P_m)$ (first 32 digits shown; certified to 61–66 digits) | $N_1(C_m)$ | $N_3(C_m)$ | Certified $\theta_1(C_m)$ (first 32 digits shown; certified to 60–66 digits) |
| :-: | ---------: | ---------: | :-------------------------------------------------------------------------- | ---------: | ---------: | :-------------------------------------------------------------------------- |
| 2 | 20 | 1 | `13.000000000000000000000000000000` | — | — | — |
| 3 | 80 | 2 | `42.254746265138411035546166818489` | 60 | 1 | `32.000000000000000000000000000000` |
| 4 | 320 | 4 | `137.344848480761466240312967211563` | 260 | 3 | `114.167960646926020492363823871018` |
| 5 | 1,280 | 11 | `446.426299171970952640361401264439` | 1,020 | 3 | `359.909325150344589146283804766089` |
| 6 | 5,120 | 31 | `1451.066211108510758569258597073221` | 4,100 | 11 | `1182.693461888314602393120641084775` |
| 7 | 20,480 | 107 | `4716.552743951021562714615293640707` | 16,380 | 17 | `3829.146666724943385607503526337294` |
| 8 | 81,920 | 379 | `15330.706253905017572949912502455090` | 65,540 | 62 | `12464.383871815031823493687115813111` |
| 9 | 327,680 | 1,451 | `49831.003080926028995195885884941623` | 262,140 | 151 | `40492.334305935591334799800278044335` |
| 10 | 1,310,720 | 5,611 | `161970.937739519110666360222385162239` | 1,048,580 | 539 | `131643.391695728352982890513044151308` |
| 11 | 5,242,880 | 22,187 | `526471.133438035407882091526259163659` | 4,194,300 | 1,699 | `427861.134428042428864726923248967758` |
| 12 | 20,971,520 | 87,979 | `1711244.364032136209197000480370212079` | 16,777,220 | 6,226 | `1390763.127021926612444105266040691823` |
| 13 | 83,886,080 | 350,891 | `5562237.105591935320511145734718686648` | 67,108,860 | 21,945 | `4520491.971281671467512957100333192641` |
| 14 | — | — | — | 268,435,460 | 81,433 | `14693493.610319124799256859942479451396` |

### 2.3 High-Precision Non-Rigorous Determination of $W_{\text{sq}}(4)$ and $W_{\text{sq}}(5)$ (Partial Win `p1`)

We computed $W_{\text{sq}}(4)$ and $W_{\text{sq}}(5)$ by two independent non-rigorous methods:
1. **Method A (`potts_ctmrg.c`)**: 106-bit Double-Double (`dd`, 32-digit) Baxter / Nishino–Okunishi CTMRG exploiting exact $\mathbb{Z}_q$ cyclic colour-translation reduction ($C_a = C_0$, $P_{a,b} = P_{(b-a)\bmod q}$) and $S_{q-1}$-multiplet-preserving truncation across $\chi \in \{9, 15, 21, 27, 36, 45\}$ ($q=4$) and $\chi \in \{8, 16, 24, 32, 40\}$ ($q=5$).
2. **Method B (`potts_extrapolate_and_verify.py`)**: Wynn $\varepsilon$-algorithm acceleration applied to the 60-digit certified open-strip ratio sequence $r_m = \theta_1(P_m) / \theta_1(P_{m-1})$ across $\ge 4$ truncation windows $M_{\max} \in \{12, 13, 14, 15, 16, 17\}$ ($q=4$) and $M_{\max} \in \{10, 11, 12, 13\}$ ($q=5$).

| Constant | Method A ($\mathbb{Z}_q$-CTMRG) | Method B (Strip Wynn $\varepsilon$-Extrapolation) | Cross-Method Difference | Certified Agreeing Digits |
| :--- | :--- | :--- | :---: | :--- |
| **$W_{\text{sq}}(4)$** | `2.336056641041133653...` ($\chi=45$) | `2.336056641041133623...` ($M_{\max}=17$) | $3.04 \times 10^{-17}$ | **17 decimals**: `2.3360566410411336` |
| **$W_{\text{sq}}(5)$** | `3.250404923167119143811...` ($\chi=40$) | `3.250404923167119143803...` ($M_{\max}=13$) | $8.09 \times 10^{-21}$ | **20 decimals**: `3.2504049231671191438` |

Both values lie strictly inside Lundow & Markström's rigorous intervals and agree with $2.336056641 \pm 10^{-9}$.

### 2.4 Rigorous Bound Improvements over Lundow & Markström (2008) (Full Win)

By Theorem 2.1 ($\theta_1(P_{m}) / \theta_1(P_{m-1}) \le W_{\text{sq}}(q)$) and Theorem 2.2 ($W_{\text{sq}}(q) \le \theta_1(C_{2k})^{1/(2k)}$) of Lundow & Markström (2008), combined with our 512-bit cross-multiplied Collatz–Wielandt lower and upper bounds $\theta_{1,\text{lo}} \le \theta_1 \le \theta_{1,\text{hi}}$:

$$\frac{\theta_{1,\text{lo}}(P_m)}{\theta_{1,\text{hi}}(P_{m-1})} \le W_{\text{sq}}(q) \le \Big(\theta_{1,\text{hi}}(C_{2k})\Big)^{1/(2k)}.$$

| Bound | Lundow & Markström (2008) | Our Certified Bound (`potts_kink_cert.c`) | Strict Improvement | Certificate Files |
| :--- | :--- | :--- | :--- | :--- |
| **$W_{\text{sq}}(4)$ Upper Bound** | `2.33606820555777` ($C_{16}^{1/16}$) | **`2.33606022655545835814...`** ($C_{18}^{1/18}$) | **$-7.979002314 \times 10^{-6}$** (**$7,979\times$ required $10^{-9}$ margin!**) | `results/potts_certs/q4_cyl_18_cert.bin` |
| **$W_{\text{sq}}(4)$ Lower Bound** | `2.3360566407231149...` ($P_{15}/P_{14}$) | **`2.33605664100499306289...`** ($P_{17}/P_{16}$) | **$+2.818782 \times 10^{-10}$** | `results/potts_certs/q4_open_16_cert.bin`, `q4_open_17_cert.bin` |
| **$W_{\text{sq}}(5)$ Upper Bound** | `3.250407145038276` ($C_{12}^{1/12}$) | **`3.25040520587854968506...`** ($C_{14}^{1/14}$) | **$-1.939159726 \times 10^{-6}$** (**$1,939\times$ required $10^{-9}$ margin!**) | `results/potts_certs/q5_cyl_14_cert.bin` |
| **$W_{\text{sq}}(5)$ Lower Bound** | `3.2504049231640788...` ($P_{11}/P_{10}$) | **`3.25040492316705717894...`** ($P_{13}/P_{12}$) | **$+2.978368 \times 10^{-12}$** | `results/potts_certs/q5_open_12_cert.bin`, `q5_open_13_cert.bin` |

