# Constructive Derivation of `[binom(d, e-3)] D_e(q)` (`PROVED-HERE`, Theorem 7)

## 1. Statement of Theorem 7 (Extending Mertens & Moore 2018 Theorems 4–6)
Let $D_e(q) = \sum_{k=1}^e \binom{d}{k} \sum_{t,v} G_{e,t,v}^{(k)}\, q^{t + 2(d-k)v}$ be the bond perimeter polynomial on $\mathbb{Z}^d$, where $G_{e,t,v}^{(k)}$ counts fixed connected bond animals of size $e$ bonds proper in $k$ dimensions with $v$ vertices and subspace perimeter $t$.

**Theorem 7 (`PROVED-HERE`).** *For all integers $d \ge 3$ and $e \ge 3$, the coefficient of $\binom{d}{e-3}$ in $D_e(q)$ is*
$$[\tbinom{d}{e-3}]\, D_e(q) = q^{2(e+1)d - 2e}\left(\gamma_0 + \gamma_1 q^{-1} + \gamma_2 q^{-2} + \gamma_3 q^{-3} + \gamma_{2d} q^{-2d} + \gamma_{2d+1} q^{-2d-1}\right),$$
*where*
$$\begin{aligned}
\gamma_0 &= \frac{1}{3}\, 2^{e-7}(e-3)\left(8e^8 - 76e^7 + 254e^6 - 345e^5 + 446e^4 - 2240e^3 + 16024e^2 - 76155e + 126212\right)(e+1)^{e-8},\\
\gamma_1 &= \frac{1}{3}\, 2^{e-5}(e-3)(e-4)\left(12e^6 - 56e^5 - 49e^4 + 771e^3 - 245e^2 - 7243e + 15930\right)(e+1)^{e-8},\\
\gamma_2 &= 2^{e-5}(e-3)(e-4)\left(8e^5 - 2e^4 - 325e^3 + 376e^2 + 5541e - 16990\right)(e+1)^{e-8},\\
\gamma_3 &= \frac{1}{3}\, 2^{e-3}(e-3)(e-4)(e-5)\left(4e^3 + 51e^2 + 120e - 2195\right)(e+1)^{e-8},\\
\gamma_{2d} &= 2^{e-5}(e-3)(e-4)\left(2e^3 - 9e^2 + 5e + 50\right) e^{e-7},\\
\gamma_{2d+1} &= 2^{e-4}(e-3)(e-4)(e-5)(2e + 9)\, e^{e-7}.
\end{aligned}$$

## 2. Proof Outline (`PROVED-HERE`)

1. **Perimeter-Chord Identity.** For any proper bond animal $A \subset \mathbb{Z}^k$ with $e$ bonds and $v$ vertices, let $s(A) = |E(\mathbb{Z}^k[V(A)]) \setminus E(A)|$ be the number of non-animal grid chords induced by $V(A)$. Counting vertex-edge incidences in $\mathbb{Z}^k$ gives $2kv = 2e + 2s(A) + (t - s(A))$, so $t = 2kv - 2e - s(A)$ and
   $$t + 2(d - k)v = 2dv - 2e - s(A) = \bigl(2(e+1)d - 2e\bigr) - 2(e + 1 - v)d - s(A).$$
2. **Cyclomatic Bound ($v \in \{e, e+1\}$ for $k = e - 3$).** Partition the $k = e - 3$ spanned axes into repeated axes $R$ ($\operatorname{mult}_A(a) \ge 2$, $|R| = r$) and singleton axes $S$ ($\operatorname{mult}_A(a) = 1$, $|S| = k - r$). Then $e_R := \sum_{a \in R} \operatorname{mult}_A(a) = r + 3$, and since $e_R \ge 2r$, we have $1 \le r \le 3$ and $e_R \le 6$. Every cycle in $\mathbb{Z}^k$ uses every axis on it at least twice, so all cycles lie inside $E_R$. Since $\mathbb{Z}^r$ is bipartite and $K_{2,3}$-free, any subgraph with cyclomatic number $\ge 2$ has $e_H \ge 7 > 6 \ge e_R$. Hence every animal proper in $e - 3$ dimensions has $e + 1 - v \in \{0, 1\}$, i.e., $v = e + 1$ (trees) or $v = e$ (unicyclic).
3. **Singleton-Bridge Separation and Additivity.** Let $H_0 = (V_0, E_R)$ have $c_0$ connected components $K_1, \dots, K_{c_0}$ in $\mathbb{Z}^r$ ($v_0 = \sum_{i=1}^{c_0} |V(K_i)|$). Any zero-displacement path or repeated-axis chord path in $A$ must have net displacement $0$ along every singleton axis $a \in S$, hence uses zero edges of $S$ and lies wholly inside a single component $K_i$. Conversely, a chord along a singleton axis $a \in S$ corresponds to a path $u \xrightarrow{P_1 \subseteq E_R} x \xrightarrow{e_a} y \xrightarrow{P_2 \subseteq E_R} w$ with $\Delta(P_1) + \Delta(P_2) = 0$ and $(u, w) \neq (x, y)$, forcing both $P_1$ and $P_2$ to be non-empty. Thus $e_a$ must be a direct length-$1$ bridge joining $u_i \in K_i$ and $u_j \in K_j$ ($i \neq j$), contributing $\Delta s(i, u_i; j, u_j) = |(V(K_i) - u_i) \cap (V(K_j) - u_j)| - 1$ chords additively across all length-$1$ singleton bridges.
4. **Finite Core-Forest Summation.** Each connected fixed animal $K_i \subset \mathbb{Z}^r$ normalized by $\min V(K_i) = 0^r$ has trivial translation-preserving automorphism group; permuting identical components divides by $\prod_X m_X!$. Contracting $K_1, \dots, K_{c_0}$ and adding $N = v - v_0$ unlabeled external vertices yields a spanning tree $T$ on $c_0 + N$ vertices with $e - e_R = c_0 + N - 1$ distinctly axis-labeled, oriented singleton edges ($2^{e-e_R} (c_0 + N - 1)! / N!$ label-orientation factor). Writing each direct-bridge $z$-polynomial ($z = q^{-1}$) as $W_{i,j}(z) = |V(K_i)||V(K_j)| + \widetilde{W}_{i,j}(z)$ and expanding over forests $F \subseteq \binom{\{1..c_0\}}{2}$ with merged component sizes $S_1, \dots, S_{c'}$ ($c' = c_0 - |F|$), Prüfer's weighted tree theorem gives $\bigl(\prod_{q=1}^{c'} S_q\bigr) v^{c' + N - 2}$. Summing symbolically over all $16{,}314$ canonical core multisets ($r \in \{1, 2, 3\}$) in exact rational arithmetic (`how-we-built-it/prove_bond_perimeter_e_minus_3.py`) produces the six closed formulas above with zero free parameters.
