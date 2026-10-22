# Pre-Registration: `snake-coil-in-the-box` (Wave 3)

## 1. Target & Baseline Specification
- **Target ID**: `snake-coil-in-the-box`
- **Graph**: $n$-dimensional hypercube $Q_n = \{0, \dots, 2^n - 1\}$ where edges connect vertices with $\operatorname{popcount}(u \oplus v) = 1$.
- **Definitions**:
  - **Snake** of length $L$: sequence of $L+1$ distinct vertices $(v_0, \dots, v_L)$ with $\operatorname{popcount}(v_i \oplus v_{i+1}) = 1$ and $\operatorname{popcount}(v_i \oplus v_j) \ge 2$ for $|i - j| > 1$.
  - **Coil** of length $L$: cyclic sequence of $L$ distinct vertices $(v_0, \dots, v_{L-1})$ with $\operatorname{popcount}(v_i \oplus v_{(i+1)\bmod L}) = 1$ and $\operatorname{popcount}(v_i \oplus v_j) \ge 2$ for $(i - j) \bmod L \notin \{0, 1, L-1\}$.
  - **Symmetric Coil (`minortriad` convention)**: coil of even length $L = 2h$ whose transition sequence satisfies exact half-period invariance $\text{steps}[i] = \text{steps}[i + h]$ for all $0 \le i < h$.

### Published Baselines
| Dimension $n$ | Snake (`minortriad` / `Caltech` / `Toner`) | Coil (`minortriad` / `Caltech` / `Taylor`) | Symmetric Coil (`minortriad` / `Caltech`) | Prior Unmerged `#79..#89` |
| :---: | :---: | :---: | :---: | :---: |
| $Q_9$ | `191` | `192` | `186` | — |
| $Q_{10}$ | `379` | `374` | `370` | `co10=374` (`p3`, `#83`) |
| $Q_{11}$ | `750` (`746` Caltech) | `740` (`734` Caltech) | `730` (`734` Caltech) | `co11=740` (`p3`, `#84`), `sn11=750` (`p3`, `#87`) |
| $Q_{12}$ | `1480` (`1476` Caltech) | `1468` (`1466` Caltech) | `1434` | `sc12=1450` (`p1`, `#79`), `co12=1468` (`p3`, `#85`), `sn12=1480` (`p3`, `#88`) |
| $Q_{13}$ | `2946` (`2924` Caltech) | `2930` (`2916` Caltech) | `2830` | `sc13=2870` (`p1`, `#80`), `co13=2930` (`p3`, `#86`), `sn13=2946` (`p3`, `#89`) |
| $Q_{14}$ | `5850` (Toner) / `5844` (Taylor) | `5750` (Taylor) | — | `co14=5854` (`p2`, `#81`), `sn14=5854` (`p2`, `#82`) |

## 2. Attack Plan
1. **Audit, Calibrate, and Re-verify `#79..#89`**:
   - Calibrate standalone verifier against all 37 `minortriad_records.json` sequences, all full `Math-AI-Caltech/Snake-in-the-Box` CSV banks (`record_snakes.csv`, `record_coils.csv`, `record_symmetric_coils.csv`), and the `toner`/`taylor` $Q_{13}/Q_{14}$ records.
   - Verify all `#79..#89` objects and check canonical transition-sequence inequivalence and step-gap spectrum invariants against the full reference banks.
2. **Push `p1` (Symmetric Coils in $Q_{11}, Q_{12}, Q_{13}$) and `p2` ($Q_{14}$ Coil & Snake) Higher**:
   - Upgrade `lift_all_dims.c` and `snake_coil_opt.c` to explore multiple Step-1 detour candidates, wider Step-2 junction windows, symmetric iterated local perturbations (ILS + `+2/+4` half-period window sweeps), and subcube automorphism splices to beat `1450` in $Q_{12}$ (`sc12`), `2870` in $Q_{13}$ (`sc13`), and `5854` in $Q_{14}$ (`co14` and `sn14`).
3. **Expand `p3` and Search for $Q_9..Q_{13}$ Improvements**:
   - Check if any record in $Q_9..Q_{13}$ can be lengthened or if new strictly inequivalent equal-record witnesses can be constructed for $Q_9$ (`sn9=191`, `co9=192`) and $Q_{10}$ (`sn10=379`) beyond the full Caltech banks (`131` classes for `sn9=191`, `12` classes for `sn10=379`).
