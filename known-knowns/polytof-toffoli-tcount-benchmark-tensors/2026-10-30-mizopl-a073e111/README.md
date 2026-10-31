# `polytof` (`p2`): Certified `CP = 3` and `Waring = 17` Optimality for Row `0725` ($\mathrm{GF}(2^2)$ Multiplication)

## What

Confirmed partial win p2 on polytof-toffoli-tcount-benchmark-tensors for single table row 0725 (GF(2^2) multiplication, n=6, nnz=5, indexed in object/p2_0725_optimality_certificate.json sha256 a073e111c38831bfba3839a47b5bb9a0f2cc2abde8aa9572ee7a528e241dbc8a and recomputed from scratch in 0.21s by verify-it-yourself/verify.py against ZIB-IOL/polytof pinned commit 0dcac107d15adc34dc646242d222f21ae7d32699): (1) certified CP = 3 optimality (CP <= 2 impossible) via exterior-wedge reduction Sym_6(u x v x w) = u ^ v ^ w mod 2 and exhaustive Grassmannian Gr(3, F_2^6) enumeration over all 1,395 3-dimensional subspaces (0/1,395 at R=1, 0/972,315 unordered pairs at R=2, and 120 canonical unordered subspace triples at R=3 including posted 0725-00003.npy) plus exhaustive bilinear check on 0525-00003.npy (0/9 at R=1, 0/36 at R=2, 3/84 at R=3); and (2) certified Waring = 17 optimality (Waring <= 16 impossible) via punctured Reed-Muller RM(3,6)* / RM(2,6)* coset reduction (41 signature equations over 63 nonzero linear forms, rank(H) = 41, dim ker(H) = 22) and exhaustive evaluation of all 2^22 = 4,194,304 valid Waring decompositions in the affine coset e_0 + ker(H) (0/4,194,304 at weight <= 16, and 1,008 optimal weight-17 decompositions including posted 0725-00017.npy).

### Summary of Row `0725` ($\mathrm{GF}(2^2)$ Multiplication) Optimality Certificates

Row `0725` ($\mathrm{GF}(2^2)$ mult) in `docs/tensors.md` (`| GF($2^2$) mult | - | - | - | - | - | - | 6 | 5 | 3 | 17 |`) has cubic phase polynomial
$$\mathcal{T}_{0725}(x) = x_0 x_2 x_4 \oplus x_0 x_3 x_5 \oplus x_1 x_2 x_5 \oplus x_1 x_3 x_4 \oplus x_1 x_3 x_5 \pmod 2$$
on $n = 6$ qubits. Unlike the `Tof_3` rows whose `CP = 2` lower bound follows directly from their mode-1 flattening rank ($\lceil 6/3 \rceil = 2$), `0725` has mode-1 flattening rank $6$ over $\mathbb{F}_2$, which only gives the trivial lower bound $\text{CP} \ge 2$. `verify-it-yourself/verify.py` recomputes two exact, exhaustive algebraic obstruction checks proving that **both** table values (`CP = 3` and `Waring = 17`) are strictly optimal across all $\mathrm{GL}_6(\mathbb{F}_2)$ basis changes:

| Metric (`docs/tensors.md` Row `0725`) | Table Value | Trivial Flattening Lower Bound | Exhaustive Search Space Checked | Decompositions at $\le \text{Table} - 1$ | Optimal Decompositions at Table Value | Re-Verification Time |
|---|---:|---:|---|---:|---:|---:|
| **Toffoli / Symmetric `CP` (`0725-00003.npy`)** | **`3`** | `2` ($\lceil 6/3 \rceil$) | All $\left[\begin{matrix} 6 \\ 3 \end{matrix}\right]_2 = 1,395$ 3-subspaces ($R=1$) and $\binom{1395}{2} = 972,315$ pairs ($R=2$) in $\operatorname{Gr}(3, \mathbb{F}_2^6)$ | **`0`** (`0/1,395` at $R=1$; `0/972,315` at $R=2$) | **`120`** canonical subspace triples | `0.10 s` |
| **Bilinear `CP` (`0525-00003.npy`)** | **`3`** | `2` | All $9$ rank-1 bilinear forms ($R=1$), $\binom{9}{2}=36$ pairs ($R=2$), $\binom{9}{3}=84$ triples ($R=3$) | **`0`** (`0/9` at $R=1$; `0/36` at $R=2$) | **`3`** rank-1 bilinear triples | `< 0.01 s` |
| **T-Count / `Waring` (`0725-00017.npy`)** | **`17`** | `6` | All $2^{63-41} = 2^{22} = 4,194,304$ valid Waring decompositions in $e_0 + \mathrm{RM}(2,6)^* \subset \mathbb{F}_2^{63}$ | **`0`** (`0/4,194,304` at $r \le 16$) | **`1,008`** weight-17 schemes | `0.08 s` |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **What it does**: Recomputes from scratch all $1,395$ RREF 3D subspaces of $\mathbb{F}_2^6$ ($0 / 1,395$ at $R=1$, $0 / 972,315$ at $R=2$, $120$ optimal triples at $R=3$), all $9$ rank-1 bilinear forms on $\mathbb{F}_2^2 \times \mathbb{F}_2^2$ ($0 / 9$ at $R=1$, $0 / 36$ at $R=2$, $3$ optimal triples at $R=3$), and all $2^{22} = 4,194,304$ valid Waring decompositions in the punctured Reed-Muller coset $e_0 + \mathrm{RM}(2,6)^*$ ($0$ at $r \le 16$, $1,008$ optimal weight-17 schemes at $r = 17$), and verifies `object/p2_0725_optimality_certificate.json` (`~0.21 s` single-thread CPU time).

## Compared To

- **Target ID**: `polytof-toffoli-tcount-benchmark-tensors` (`category: physics`)
- **Primary Status Table**:
  - `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md` (upstream commit `0dcac107d15adc34dc646242d222f21ae7d32699`, fetched `2026-10-30T07:50:00Z`, `HTTP 200`, `8,777` bytes, `sha256: f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`).
- **Literature Checked**:
  - Khoruzhii, Gelß, Pokutta (`arXiv:2602.15285`, Feb 2026, `https://arxiv.org/abs/2602.15285`, `https://github.com/ZIB-IOL/polytof`).
  - Ruiz et al., AlphaTensor-Quantum (`arXiv:2402.14396`, `https://github.com/google-deepmind/alphatensor_quantum`).
  - Mazumder (`arXiv:2610.01024`).

## Not Claimed

- This package claims only partial win **`p2`** for single table row **`0725` ($\mathrm{GF}(2^2)$ mult)** (`CP = 3` and `Waring = 17` certified strictly optimal), split out from PR #761 per maintainer review (`2026-10-29T23:11:07Z`).
- Partial win `p3` (the `data/paper/` audit and `4` repaired Waring schemes) is tracked separately in PR #761.

## Credits

- **Credit**: `mizopl` (`https://github.com/mizopl/we-star` — `we*` multi-agent autoresearch engine)
- **Built on / Compared against**:
  - Kirill Khoruzhii, Patrick Gelß, and Sebastian Pokutta, `ZIB-IOL/polytof` (`https://github.com/ZIB-IOL/polytof`, `arXiv:2602.15285`)
  - Francisco J. R. Ruiz et al., AlphaTensor-Quantum (`https://github.com/google-deepmind/alphatensor_quantum`, `arXiv:2402.14396`)
