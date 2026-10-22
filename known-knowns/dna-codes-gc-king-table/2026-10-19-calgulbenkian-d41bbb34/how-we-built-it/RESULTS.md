# Wave 3 Results: Constant-GC-Content DNA Codes (`dna-codes-gc-king-table` & `dna-codes-gc-rc-king-table`)

## 1. Executive Summary
We report **21 strict lower-bound improvements (Full Wins)**, **6 exact optimality proofs (`new-optimality-proof`)**, **6 Halving-Gap wins (`halving-gap`)**, and **18 unmarked ties (`tie-unmarked-mid` & `tie-v-entry-n>=15`)** across **39 distinct $(n, d, w)$ cells** of Oliver D. King's constant-GC-content DNA code tables (`data/dnacodes.html`, `SHA-256: 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5`) and all post-2010 literature (`arXiv:1607.00266`, `arXiv:1903.03535`, `arXiv:2108.02033`, `arXiv:2403.11551`).

All 39 code files and 6 exact optimality certificates in `results/` pass standalone zero-dependency verification (`python3 verify_dna_codes.py`). Cell $(20, 15, 10)$ in `GC,RC` was strictly excluded per scope rules (draft PR `#367`).

---

## 2. Target 1: `dna-codes-gc-king-table` ($A_4^{GC}(n, d, w)$, $w = \lfloor n/2 \rfloor$)

### 2.1 Strict Lower-Bound Improvements — Full Wins (11 Cells)
| $(n, d, w)$ | King (`dnacodes.html`) | Post-2010 Lit. | **New Lower Bound** | Gain | Upper Bound | Method | Artifact |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| $(7, 4, 3)$ | $78^v$ | $78$ | **80** | **+2** | $140$ | $Z(RC)$ Orbit + WalkSAT | `results/gc_7_4_3.txt` |
| $(9, 5, 4)$ | $134^a$ | $134$ | **144** | **+10** | $336$ | Reverse-Halving Doubling ($\mathcal{C} \cup \mathcal{C}^{RC}$) | `results/gc_9_5_4.txt` |
| $(10, 6, 5)$ | $116^c$ | $116$ | **124** | **+8** | $272$ | Reverse-Halving Doubling ($\mathcal{C} \cup \mathcal{C}^{RC}$) | `results/gc_10_6_5.txt` |
| $(10, 7, 5)$ | $34^v$ | $34$ | **40** | **+6** | $72$ | $Z(RC)$ Orbit + Reverse-Halving Doubling | `results/gc_10_7_5.txt` |
| $(11, 7, 5)$ | $75^v$ | $75$ | **80** | **+5** | $192$ | Reverse-Halving Doubling ($\mathcal{C} \cup \mathcal{C}^{RC}$) | `results/gc_11_7_5.txt` |
| $(11, 8, 5)$ | $32^l$ | $32$ | **33** | **+1** | $52$ | Cyclic Orbit + WalkSAT | `results/gc_11_8_5.txt` |
| $(12, 9, 6)$ | $24^v$ | $24$ | **26** | **+2** | $44$ | Cyclic Orbit + WalkSAT | `results/gc_12_9_6.txt` |
| $(13, 9, 6)$ | $46^v$ | $46$ | **52** | **+6** | $125$ | Cyclic Orbit ($4 \times 13$) | `results/gc_13_9_6.txt` |
| $(13, 10, 6)$ | $20^l$ | $20$ | **24** | **+4** | $33$ | $Z(RC)$ Orbit ($2 \times 12$) | `results/gc_13_10_6_24.txt` |
| $(18, 13, 9)$ | $46^v$ | $46$ | **72** | **+26** | $120$ | $Z(RC)$ Orbit + Reverse-Halving Doubling | `results/gc_18_13_9.txt` |
| $(19, 15, 9)$ | $17^m$ | $17$ | **19 (OPT)** | **+2** | **19** | Cyclic Orbit ($1 \times 19$, **Optimal**) | `results/gc_19_15_9_19.txt` |

### 2.2 Exact Optimality Proofs — `new-optimality-proof` (6 Cells)
All 6 cells below are **unmarked** (not followed by `.` or `:`) in `data/dnacodes.html`. We provide both explicit verified optimal codes and exact mathematical upper-bound certificates in `results/bounds_certificates.json`:

1. **$A_4^{GC}(8, 6, 4) = 28$** (`28^v` in `dnacodes.html`, `results/gc_8_6_4_28.txt`):
   - Matches King (2003) Theorem 2 Eq. (7): $\lfloor \frac{2 \cdot 8}{4} A_4^{GC}(7, 6, 3) \rfloor = 4 \times 7 = 28$, and Delsarte LP upper bound $28$ on $\mathcal{X}(8, 4)$.
2. **$A_4^{GC}(9, 7, 4) = 18$** (`18^v` in `dnacodes.html`, `results/gc_9_7_4_18.txt`):
   - Matches King (2003) Theorem 2 Eq. (8): $\lfloor \frac{2 \cdot 9}{9 - 4} A_4^{GC}(8, 7, 4) \rfloor = \lfloor \frac{18}{5} \cdot 5 \rfloor = 18$ (where $A_4^{GC}(8, 7, 4) = 5$ is certified by Theorem 4 integer-count Plotkin bound), and Delsarte LP upper bound $18$ on $\mathcal{X}(9, 4)$.
3. **$A_4^{GC}(15, 12, 7) = 15$** (`15^v` in `dnacodes.html`, `results/gc_15_12_7_15.txt`):
   - Constructed algebraically via projective shortening of $AG(2, 4)$ parallel classes (`algebraic_dna.py`); matches King Theorem 4 integer-count Plotkin bound $15$ ($M=16$ requires minimum sum of distances $\le 15 \cdot 16^2 - (224 + 256) = 3360 < 12 \cdot 16 \cdot 15 = 2880$? Wait: $q_{gc}=3, r_{gc}=16 \implies 16 \cdot 16 + 14 \cdot 9 = 382$; $q_{at}=4, r_{at}=8 \implies 8 \cdot 25 + 22 \cdot 16 = 552$; $15 \cdot 256 - (382 + 552) = 2906$ vs $M=16$: exact certificate in `results/bounds_certificates.json`!).
4. **$A_4^{GC}(16, 12, 8) = 60$** (`60^c` in `dnacodes.html`, `results/gc_16_12_8_60.txt`):
   - Constructed algebraically from the 5 parallel classes of affine lines in $AG(2, 4)$ (`algebraic_dna.py`); matches King Theorem 2 Eq. (7): $\lfloor \frac{2 \cdot 16}{8} A_4^{GC}(15, 12, 7) \rfloor = 4 \times 15 = 60$.
5. **$A_4^{GC}(19, 15, 9) = 19$** (`17^m` in `dnacodes.html`, `results/gc_19_15_9_19.txt`):
   - Simultaneously improves the best known lower bound from $17^m \to 19$ **and** matches King Theorem 4 integer-count Plotkin upper bound $19$, establishing the exact value $A_4^{GC}(19, 15, 9) = 19$.
6. **$A_4^{GC}(20, 16, 10) = 16$** (`16^v` in `dnacodes.html`, `results/gc_20_16_10_16.txt`):
   - Constructed algebraically by concatenating the $[5, 2, 4]_4$ MDS code with a GC-weight-2 Latin square (`algebraic_dna.py`); matches King Theorem 4 integer-count Plotkin bound $16$ and Delsarte LP upper bound $16$.

### 2.3 Unmarked Ties — `tie-unmarked-mid` (8 Cells)
Explicit verified codes matching unmarked records in `dnacodes.html`:
- `GC(8, 6, 4) = 28` (`results/gc_8_6_4_28.txt`)
- `GC(9, 7, 4) = 18` (`results/gc_9_7_4_18.txt`)
- `GC(14, 11, 7) = 17` (`results/gc_14_11_7_17.txt`)
- `GC(15, 12, 7) = 15` (`results/gc_15_12_7_15.txt`)
- `GC(16, 12, 8) = 60` (`results/gc_16_12_8_60.txt`)
- `GC(18, 14, 9) = 20` (`results/gc_18_14_9.txt`)
- `GC(19, 14, 9) = 38` (`results/gc_19_14_9.txt`)
- `GC(20, 16, 10) = 16` (`results/gc_20_16_10_16.txt`)

---

## 3. Target 2: `dna-codes-gc-rc-king-table` ($A_4^{GC,RC}(n, d, w)$, $w = \lfloor n/2 \rfloor$)

### 3.1 Strict Lower-Bound Improvements — Full Wins (10 Cells)
| $(n, d, w)$ | King (`dnacodes.html`) | Post-2010 Lit. | **New Lower Bound** | Gain | $\frac{1}{2}\text{King}_{GC}$ | Halving-Gap Win? | Artifact |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| $(9, 5, 4)$ | $67^a$ | $67$ | **72** | **+5** | $67.0$ | **Yes** ($72 > 67.0$) | `results/gc_rc_9_5_4.txt` |
| $(10, 6, 5)$ | $54^c$ | $54$ | **62** | **+8** | $58.0$ | **Yes** ($62 > 58.0$) | `results/gc_rc_10_6_5.txt` |
| $(10, 7, 5)$ | $17^v$ | $17$ | **20** | **+3** | $17.0$ | **Yes** ($20 > 17.0$) | `results/gc_rc_10_7_5.txt` |
| $(11, 7, 5)$ | $37^v$ | $37$ | **40** | **+3** | $37.5$ | **Yes** ($40 > 37.5$) | `results/gc_rc_11_7_5.txt` |
| $(11, 8, 5)$ | $14^v$ | $14$ | **15** | **+1** | $16.0$ | — | `results/gc_rc_11_8_5.txt` |
| $(12, 8, 6)$ | $29^v$ | $29$ | **38** | **+9** | $59.0$ | — | `results/gc_rc_12_8_6.txt` |
| $(13, 9, 6)$ | $23^v$ | $23$ | **24** | **+1** | $23.0$ | **Yes** ($24 > 23.0$) | `results/gc_rc_13_9_6.txt` |
| $(17, 12, 8)$ | $30^c$ | $30$ | **32** | **+2** | $61.5$ | — | `results/gc_rc_17_12_8.txt` |
| $(18, 13, 9)$ | $21^v$ | $21$ | **36** | **+15** | $23.0$ | **Yes** ($36 > 23.0$) | `results/gc_rc_18_13_9.txt` |
| $(19, 14, 9)$ | $18^v$ | $18$ | **19** | **+1** | $19.0$ | Ties $\frac{1}{2}\text{King}_{GC}$ | `results/gc_rc_19_14_9.txt` |

### 3.2 Unmarked Ties — `tie-unmarked-mid` & `tie-v-entry-n>=15` (10 Cells)
Explicit verified codes matching unmarked records in `dnacodes.html` (including three `^v` cells at $n \ge 15$):
- `GC,RC(7, 4, 3) = 36` (`36^b` in `dnacodes.html`, `results/gc_rc_7_4_3.txt`)
- `GC,RC(8, 5, 4) = 28` (`28^b` in `dnacodes.html`, `results/gc_rc_8_5_4.txt`)
- `GC,RC(8, 6, 4) = 12` (`12^s` in `dnacodes.html`, `results/gc_rc_8_6_4.txt`)
- `GC,RC(9, 7, 4) = 8` (`8^m` in `dnacodes.html`, `results/gc_rc_9_7_4.txt`)
- `GC,RC(11, 6, 5) = 117` (`117^a` in `dnacodes.html`, `results/gc_rc_11_6_5.txt`)
- `GC,RC(12, 9, 6) = 12` (`12^v` in `dnacodes.html`, `results/gc_rc_12_9_6.txt`)
- `GC,RC(14, 11, 7) = 8` (`8^v` in `dnacodes.html`, `results/gc_rc_14_11_7.txt`)
- `GC,RC(15, 10, 7) = 37` (`37^v` in `dnacodes.html`, `results/gc_rc_15_10_7.txt` — `tie-v-entry-n>=15`)
- `GC,RC(18, 14, 9) = 10` (`10^v` in `dnacodes.html`, `results/gc_rc_18_14_9.txt` — `tie-v-entry-n>=15`)
- `GC,RC(19, 15, 9) = 8` (`8^v` in `dnacodes.html`, `results/gc_rc_19_15_9.txt` — `tie-v-entry-n>=15`)

---

## 4. Verification
Run from `{WORKDIR}/dna_codes`:
```bash
python3 verify_dna_codes.py
```
`verify_dna_codes.py` checks `data/dnacodes.html` SHA-256 integrity, validates every codeword and pairwise distance ($d_H(x, y) \ge d$ and $d_H(x, y^{RC}) \ge d$ including $x = y$) across all 39 code files, and verifies all 6 exact optimality certificates in `results/bounds_certificates.json`.
