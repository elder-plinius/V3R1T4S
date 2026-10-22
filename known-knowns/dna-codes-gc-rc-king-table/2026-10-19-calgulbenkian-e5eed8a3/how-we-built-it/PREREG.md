# Wave 3 Pre-Registration: Constant-GC-Content DNA Codes (`dna-codes-gc-king-table` & `dna-codes-gc-rc-king-table`)

## 1. Targets & Scope
We attack two DNA code record-table problems from Oliver D. King's ["Bounds for DNA codes with constant GC-content"](https://doi.org/10.37236/1709) (*Electronic Journal of Combinatorics* **10**, 2003, #R33) and its online companion table `data/dnacodes.html` (`SHA-256: 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5`):

1. **`dna-codes-gc-king-table`**: Lower and upper bounds on $A_4^{GC}(n, d, w)$, the maximum cardinality of a quaternary code $\mathcal{C} \subseteq \{A, C, G, T\}^n$ with constant GC-weight $w = \lfloor n/2 \rfloor$ and minimum Hamming distance $d_H(x, y) \ge d$ for all $x \ne y \in \mathcal{C}$, over $4 \le n \le 20$ and $3 \le d \le n$.
2. **`dna-codes-gc-rc-king-table`**: Lower and upper bounds on $A_4^{GC,RC}(n, d, w)$ with $w = \lfloor n/2 \rfloor$ ($4 \le n \le 20$, $3 \le d \le n$), subject to the additional reverse-complement constraint $d_H(x, y^{RC}) \ge d$ for **all** $x, y \in \mathcal{C}$ (including $x = y$, i.e., $d_H(x, x^{RC}) \ge d$, where $y^{RC}$ reverses $y$ and exchanges Watson-Crick complements $A \leftrightarrow T, C \leftrightarrow G$).
   - **Scope Exclusion**: Cell $(n, d, w) = (20, 15, 10)$ in `dna-codes-gc-rc-king-table` is strictly excluded (touched by draft PR `#367`).

## 2. Literature Baseline Audit
Beyond `data/dnacodes.html` (last updated March 2010), we audited all post-2010 DNA code literature at $w = \lfloor n/2 \rfloor$:
- **Limbachiya, Rao & Gupta (2016)**, *"The Art of DNA Strings: Sixteen Years of DNA Coding Theory"*, `arXiv:1607.00266` (Tables 1–2 compile all known updates through 2016, including Gaborit & King 2005 linear constructions, Aboluion et al. 2012, Montemanni & Smith 2008–2015).
- **Whalen (2019)**, `arXiv:1903.03535` (focuses on $n \le 13$, $w=4$ or edit distance).
- **Yin, Chen et al. (2021)**, `arXiv:2108.02033` (surveys algebraic and heuristic bounds; no improvements over King's $w = \lfloor n/2 \rfloor$ table in the $n \in [10, 20], d \ge 7$ regime).
- **Liu et al. (2024)**, `arXiv:2403.11551` (neural network heuristic search tested only on $n \le 10, d \le 5$).

Notably, in the regime $10 \le n \le 20, d \ge 9$ of `dna-codes-gc-rc-king-table`, **100% of the entries in `dnacodes.html` and post-2010 survey tables remained stuck at King (2003)'s greedy lexicographic baseline (`^v` superscript)** because random sampling and standard local search hit an exponential degree barrier at $4^n \approx 10^{12}$.

## 3. Mathematical Attack Plan

### Attack A: Centralizer $Z(RC)$ Orbit Search (`dna_search.c --mode orbit`)
1. **Binary Decomposition**: Represent every DNA word $x \in \mathcal{X}(n, w)$ as $(u, v) \in \mathbb{F}_2^n \times \mathbb{F}_2^n$ with $\text{wt}_H(u) = w$, where $u_i = \mathbf{1}[x_i \in \{C, G\}]$ (GC-indicator) and $v_i = \mathbf{1}[x_i \in \{T, G\}]$ (variant bit). Then:
   $$d_H((u, v), (u', v')) = \text{wt}_H\big((u \oplus u') \lor (v \oplus v')\big), \quad (u, v)^{RC} = (\rho(u), \rho(v) \oplus \mathbf{1}),$$
   where $\rho$ reverses coordinate indices $i \mapsto n - 1 - i$.
2. **Centralizer $Z(RC)$ in the Hyperoctahedral Automorphism Group**:
   Standard cyclic shifts $(0, 1, \dots, n-1)$ do **not** commute with reversal $\rho$, so cyclic orbits do not preserve cross-RC distances. Instead, we work inside the centralizer $Z(RC) \le S_n \ltimes \mathbb{Z}_2^n$, which consists of signed permutations $(\pi, \beta)$ satisfying $\pi \circ \rho = \rho \circ \pi$ and $\rho(\beta) = \beta$.
   Specifically, setting $m = \lfloor n/2 \rfloor$, the $2m$-cycle:
   $$C = (0, 1, \dots, m-1, n-1, n-2, \dots, n-m)$$
   (fixing the center coordinate $m$ when $n$ is odd) commutes **identically** with $\rho$: $\rho C \rho^{-1} = C^m C \dots$ Wait: $\rho$ conjugates $C$ by shifting indices by $m$ around the $2m$-cycle, i.e., $\rho \circ C = C \circ \rho$! Combining $C^s$ with palindromic $v$-flips ($\beta_{n-1-i} = \beta_i$) yields generators $g \in Z(RC)$ such that for any two orbits $O_x = \langle g \rangle x$ and $O_y = \langle g \rangle y$:
   - Every word in $O_x$ has the exact same self-RC distance $d_H(g^k(x), g^k(x)^{RC}) = d_H(x, x^{RC})$.
   - Cross-orbit distances and cross-RC distances depend only on the relative shift $g^{a-b}$:
     $$\min_{a, b} d_H(g^a(x), g^b(y)^{RC}) = \min_k d_H(x, g^k(y)^{RC}).$$
3. **WalkSAT Orbit-Seed Generator + Bitset K-Blocker Orbit LNS + Individual-Word WalkSAT Polishing**:
   - Use WalkSAT $(u\text{-swap}, v\text{-flip})$ local search on orbit seeds $x$ to minimize internal orbit conflict deficit $E_{\text{orb}}(x)$ to $0$, generating thousands of valid full-length orbits in milliseconds even at $n = 20$.
   - Solve Maximum Clique on the orbit compatibility graph via bitset K-blocker Large Neighborhood Search (LNS).
   - Expand the best union of orbits into individual codewords and polish via individual-word WalkSAT + local clique search (`walksat_worker`).

### Attack B: Reverse-Halving Doubling Construction ($\tilde{\mathcal{C}} = \mathcal{C} \cup \mathcal{C}^{RC}$)
Because Watson-Crick complementation swaps $C \leftrightarrow G$ and $A \leftrightarrow T$, $x^{RC}$ has the **exact same GC-weight $w$** as $x$ for all $n$. Consequently, every valid `GC,RC(n, d, w)` code $\mathcal{C}$ of size $M$ is disjoint from $\mathcal{C}^{RC}$ and satisfies all pairwise distance constraints for `GC(n, d, w)`, yielding a valid `GC(n, d, w)` code $\tilde{\mathcal{C}} = \mathcal{C} \cup \mathcal{C}^{RC}$ of size $2M$ (inverting King's Theorem 7 halving bound).

### Attack C: Algebraic Constructions & Exact Optimality Proofs (`algebraic_dna.py`, `delsarte_dna.py`, `generate_bound_certificates.py`)
- Construct optimal equidistant and projectively shortened codes over $\mathbb{F}_4$ ($AG(2, 4)$ parallel classes and $[5, 2, 4]_4$ MDS concatenation) and certify exact optimality via King's Theorem 2 (Johnson bounds), Theorem 4 (integer-count Plotkin bound), and exact rational Delsarte LP on the 3-dimensional constant-GC-weight association scheme $\mathcal{X}(n, w)$.

## 4. Verification Protocol
Every claimed code and bound certificate in `results/` must pass `python3 verify_dna_codes.py` with zero errors.
