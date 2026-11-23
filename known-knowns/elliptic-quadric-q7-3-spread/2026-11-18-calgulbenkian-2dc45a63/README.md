# Spread of the Elliptic Quadric `Q^-(7,3)` (Partial Win `p1`): No Spread Admits an Automorphism of Order 3

## What

Rerunning the package (run_checks.sh PASS in 57 s, plus the SWAR engine with 0 solutions) confirms that no spread of Q^-(7,3) is invariant under any element of order 3 of the full collineation group PGO^-(8,3), covering all 430,408,160 such elements in 5 classes; order-2 automorphisms are excluded only inside PO^-(8,3), the similarity involutions (class Inv_0_sim) remain open.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` (3.8+, standard library only) and a C99 compiler (`cc`, `clang`, or `gcc`) with `-lpthread`.
- **Rough laptop time**: about 55 seconds.
- **Expected last line**: `PASS`

## Compared to

| Source | Cell / Scope | Prior status / bound | This result | URL | UTC fetch time |
|---|---|---|---|---|---|
| Kiermaier, Schmidt, Wassermann (*Designs, Codes and Cryptography* 2025; `arXiv:2403.11188v3`, Sec. 6) | Automorphisms of $1$-$(3,3,1)_{\Omega^-(3)}$ spreads of $Q^-(7,3) = \Omega^-(8,3)$ | Spread existence open; only prime powers $2$ or $3$ may divide the order of an automorphism | Partial win `p1`: **no spread of $Q^-(7,3)$ admits an automorphism of order $3$** (and $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3) = \{1\}$, so $\|\mathrm{Aut}(\mathcal{S})\| \in \{1, 2\}$) | https://arxiv.org/abs/2403.11188 | 2026-11-18T03:58:25Z |
| Kiermaier & Wassermann Zenodo dataset (`13353388`) | Released designs in $\Omega^-(8,3)$ | Strength-$2$ designs with $\lambda \in \{2, 5\}$ (`q3_Q-_r3_k3.txt`); zero spreads ($\lambda = 1$) | Rerunnable constructive certificate + dual-engine nonexistence proof for order-$3$ spread automorphisms | https://zenodo.org/api/records/13353388 | 2026-11-18T03:59:56Z |

Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- **Unconditional existence or nonexistence of a spread of $Q^-(7,3)$ remains open**: this package does not construct an $82$-plane spread of $Q^-(7,3)$ and does not rule out spreads with trivial automorphism group ($|\mathrm{Aut}(\mathcal{S})| = 1$) or spreads invariant solely under a fixed-point-free similarity involution in class `Inv_0_sim` ($Q(Hx) = 2Q(x)$, $H^2 = 2I_8$, $|\mathrm{Aut}(\mathcal{S})| = 2$, $533 \times 11{,}070$ exact cover).
- Not peer reviewed in a mathematical journal.

## Credits

- **Michael Kiermaier, Kai-Uwe Schmidt, and Alfred Wassermann**, *"Designs in finite classical polar spaces"*, *Designs, Codes and Cryptography* (2025), https://arxiv.org/abs/2403.11188 (and companion dataset https://doi.org/10.5281/zenodo.13353388) — formulation of $t$-$(r,k,\lambda)_Q$ polar-space designs, Kramer-Mesner framework, and prior restriction of prime-power automorphism divisors on $\Omega^-(8,3)$ to $\{2, 3\}$.
- **Beniamino Segre** (*Annali di Matematica Pura ed Applicata* 70, 1965) and **James W. P. Hirschfeld and Joseph A. Thas** (*General Galois Geometries*, Springer, 2016, Sec. 7.5) — foundational theory of spreads and regular systems in finite elliptic quadrics.
- **Earl S. Kramer and Dale M. Mesner** (*Discrete Mathematics* 15, 1976) and **Donald E. Knuth** (*Dancing Links*, `arXiv:cs/0011047`, 2000) — orbit incidence reduction and exact-cover backtracking.
- **Arthur Cayley** (*J. Reine Angew. Math.* 32, 1846) and **G. E. Wall** (*J. Austral. Math. Soc.* 3, 1963) — rational Cayley parameterization and conjugacy invariants in classical orthogonal groups.
- Contributor credit: `calgulbenkian`.
