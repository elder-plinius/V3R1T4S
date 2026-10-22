# Cage Upper Bounds & Mixed Cages of Girth 6 — Verified Results (`RESULTS.md`)

All 6 mixed-cage constructions below have been independently verified by two separate algorithms in [`verify_cages.py`]({WORKDIR}/results/verify_cages.py):
- **Algorithm A**: All-roots forward-backward non-backtracking path enumeration + explicit 6-cycle witness verification.
- **Algorithm B**: Exact integer transition-matrix algebra on $U$ (undirected) and $D$ (directed), $T = U + D$:
  - $\operatorname{tr}(T^3) = 0$ (zero 3-cycles),
  - $\forall u \neq v,\; (T^2)_{uv}(T^2)_{vu} - (U^2)_{uv} = 0$ (zero 4-cycles),
  - $\operatorname{tr}(T^5) = 0$ (zero 5-cycles).

## Summary of Strict Upper-Bound Improvements (`p2`) over `arXiv:2506.20003` (Table 1)

| Cell `[z, r; g]` | Lower Bound | Previous Best UB (`arXiv:2506.20003` / `2401.14768`) | **New Verified Order $N$** | Vertices Saved | Construction Method | Artifact File & SHA-256 |
|---|---:|---:|---:|---:|---|---|
| **`[1, 7; 6]`** | `72` (`118` AHM) | `192` | **`146`** | **`-46`** (`-24.0%`) | König 2-Factor Orientation of $PG(2, 8)$ | `mixed_z1_r7_g6_N146.json` (`c8864ff3769e4ba59f59c0c3fb40aef57b7ff164cf9ce31db78bdca9f121bd34`) |
| **`[2, 6; 6]`** | `72` | `140` | **`138`** | **`-2`** (`-1.4%`) | $\operatorname{BiCay}(\mathbb{Z}_{69}; S, A_0, A_1)$ Twin-Cluster Sidon | `mixed_z2_r6_g6_N138.json` (`cb985a480c9d476c66c82d20f2f09c70281a9614d170226434da0364fc2620ed`) |
| **`[2, 7; 6]`** | `90` (`123*`) | `196` | **`184`** | **`-12`** (`-6.1%`) | $\operatorname{BiCay}(\mathbb{Z}_{92}; S, A_0, A_1)$ Twin-Cluster Sidon | `mixed_z2_r7_g6_N184.json` (`fc561db7e3e7b50619bb4b6e8673994ad0192d582bab9c29a40ba7b2769cd00b`) |
| **`[2, 8; 6]`** | `110` (`155*`) | `252` | **`234`** | **`-18`** (`-7.1%`) | $\operatorname{BiCay}(\mathbb{Z}_{117}; S, A_0, A_1)$ Twin-Cluster Sidon | `mixed_z2_r8_g6_N234.json` (`64e5ed7fd2e7c94e5ac9c7273d7e2abaefaa4d63d4c7816e1ec26a1058b599d4`) |
| **`[2, 9; 6]`** | `132` (`191*`) | `320` | **`294`** | **`-26`** (`-8.1%`) | $\operatorname{BiCay}(\mathbb{Z}_{147}; S, A_0, A_1)$ Twin-Cluster Sidon | `mixed_z2_r9_g6_N294.json` (`db59df4a75389bb9ce7677d53d07768d30c91f41d31d855a232defead7aae912`) |
| **`[2, 11; 6]`** | `182` (`275*`) | `480` | **`450`** | **`-30`** (`-6.25%`) | $\operatorname{BiCay}(\mathbb{Z}_{225}; S, A_0, A_1)$ Twin-Cluster Sidon | `mixed_z2_r11_g6_N450.json` (`2c7b60282a1cf2cb4de947f8aa0554577cc57874f1d7c547ce6f1a90e05d8fb6`) |

## Explicit Generators for Bipartite Cayley Mixed Cages $\operatorname{BiCay}(\mathbb{Z}_M; S, A_0, A_1)$

- **`[2, 6; 6]`, $N = 138$ ($M = 69$)**:
  - `S = [0, 2, 10, 29, 36, 40]`, `A0 = [1, 37]`, `A1 = [5, 41]` (twin step difference $d = 36 \in S - S$)
- **`[2, 7; 6]`, $N = 184$ ($M = 92$)**:
  - `S = [0, 17, 20, 29, 50, 73, 74]`, `A0 = [7, 78]`, `A1 = [13, 84]` (twin step difference $d = 71 \in S - S$)
- **`[2, 8; 6]`, $N = 234$ ($M = 117$)**:
  - `S = [0, 21, 24, 28, 72, 91, 106, 108]`, `A0 = [16, 86]`, `A1 = [29, 92]`
- **`[2, 9; 6]`, $N = 294$ ($M = 147$)**:
  - `S = [0, 1, 47, 82, 86, 116, 124, 131, 134]`, `A0 = [6, 91]`, `A1 = [27, 80]`
- **`[2, 11; 6]`, $N = 450$ ($M = 225$)**:
  - `S = [0, 1, 6, 23, 38, 56, 63, 108, 138, 157, 217]`, `A0 = [27, 128]`, `A1 = [104, 205]` (twin step difference $d = 101 \in S - S$)

## Verification Command

```bash
python3 results/verify_cages.py results/mixed_*.json
```
