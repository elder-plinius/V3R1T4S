# Pre-Registration — `polytof-toffoli-tcount-benchmark-tensors` (`p2`: Row `0725` / $\mathrm{GF}(2^2)$ mult)

- **Target Problem**: `known-unknowns/physics/polytof-toffoli-tcount-benchmark-tensors.md`
- **Target Partial Win**: `p2` — Certified optimality proof for single table row `0725` ($\mathrm{GF}(2^2)$ multiplication, $n=6$, $5$ cubic monomials) showing that neither $\text{CP} \le 2$ nor $\text{Waring} \le 16$ exists across all $\mathrm{GL}_6(\mathbb{F}_2)$ basis changes.
- **Verification Protocol**: Exact Grassmannian $\operatorname{Gr}(3, \mathbb{F}_2^6)$ enumeration ($1,395$ singletons + $972,315$ pairs) for `CP = 3` and exact punctured Reed-Muller coset enumeration ($2^{22} = 4,194,304$ valid Waring decompositions in $e_0 + \mathrm{RM}(2,6)^*$) for `Waring = 17`, recomputed from scratch in `< 1s` by `verify-it-yourself/verify.py`.
