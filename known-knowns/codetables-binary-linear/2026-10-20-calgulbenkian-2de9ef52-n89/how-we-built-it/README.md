# How it was built

The construction code is not included. Argon's snapshot of the contributor's laptop (folder qubit_lp) holds a results note, a campaign script and a verifier script for a different target (upper bounds for large qubit codes), but no program that builds these ten distance-5 codes, and no PREREG.md, command log or exact commands for them. We say so plainly rather than reconstruct them. The snapshot's campaign and verifier scripts are not shipped because they do not produce this object.

What the snapshot does contain about this object is the contributor's own results note (RESULTS.md, item 5), reproduced below from the snapshot with local paths replaced by the placeholder {WORKDIR} (the excerpt has none). It is the contributor's claim about method, unverified, and the panel did not check it.

The object file's own construction field for this entry reads: Hermitian-Plucker k=4 odd-parity defect quad in PG(7,F4) \ V_85 + 35-cap in V_85 (L_41) (the 16-generator code), and the analogous text with the 18-generator parameters for the other nine.

Nothing here is needed to check the claim: the object is explicit, and verify-it-yourself/ checks it from the definition.

## Excerpt of the contributor's results note

5. **Breakthrough Constructive Lower Bounds at $d = 5$: 10 New Odd-Length `[[n, k, 5]]_2` Qubit Stabilizer Codes (`results/new_stabilizer_codes_d5.json`)**:
   - Discovered the **Hermitian-Plücker $k=4$ Odd-Parity Defect Quad Method** for even redundancies $r = 2m$:
     - Under the block-diagonal $\mathbb{F}_4$-multiplication map $J : \mathbb{F}_2^r \to \mathbb{F}_2^r$ ($J^2 + J + I = 0$), every $\mathbb{F}_4$-line $L_j = \{0, u_j, J u_j, J^2 u_j\} \in \text{PG}(m-1, \mathbb{F}_4)$ maps via the Plücker bivector $\Psi(L_j) = u_j \wedge J u_j$ to a rank-1 Hermitian form in $\mathcal{H}_m(\mathbb{F}_4) \cong \mathbb{F}_2^{m^2}$.
     - Even-length $\mathbb{F}_4$-linear $d=5$ parent codes at $r = 16$ ($m = 8$, e.g. `[[70, 54, 5]]_2`) and $r = 18$ ($m = 9$, e.g. `[[74, 56, 5]]_2`) lie on special projective caps $\mathcal{V}_{85} \subset \text{PG}(7, \mathbb{F}_4)$ (spanning a $41$-dimensional subspace $\mathcal{L}_{41} \subset \mathbb{F}_2^{64}$ with zero internal weight-$\le 4$ conflicts across all 85 points) and $\mathcal{V}_{171} \subset \text{PG}(8, \mathbb{F}_4)$ (spanning a $55$-dimensional subspace $\mathcal{L}_{55} \subset \mathbb{F}_2^{81}$ with zero internal weight-$\le 4$ conflicts across all 171 points), on which a linear parity functional $\ell_0$ equals $1$ at every point.
     - By selecting a 4-tuple of $\mathbb{F}_4$-lines $E = \{L_1, L_2, L_3, L_4\} \subset \text{PG}(m-1, \mathbb{F}_4) \setminus \mathcal{V}$ whose quotient defect vectors sum to zero ($\sum_{a=1}^4 \Psi(L_a) \in \mathcal{L}$) with **odd $\ell_0$-parity** ($\ell_0(\sum_{a=1}^4 \Psi(L_a)) = 1$), any solution $S \subseteq \mathcal{V}$ to $\sum_{v \in S} \Psi(v) = \sum_{a=1}^4 \Psi(L_a)$ inside a conflict-free independent set $I \subseteq \mathcal{V}$ of the $(E, \mathcal{V})$ weight-$\le 4$ syndrome hypergraph automatically has **odd weight $|S|$** and yields an exact, commuting, pure distance-$5$ quantum stabilizer code of **odd length $n = |S| + 4$**.
     - Constructed and exhaustively verified **10 brand-new `[[n, k, 5]]_2` quantum stabilizer codes ($n \le 100$)** strictly beating Grassl's live `codetables.de/QECC` lower bounds (`[4, 6]` $\to$ **`[5, 6]`**):
       - **$r = 16$ ($1$ new code)**:
         $$\mathbf{[[39, 23, 5]]_2}$$
       - **$r = 18$ ($9$ new codes)**:
         $$\mathbf{[[75, 57, 5]]_2, \quad [[77, 59, 5]]_2, \quad [[79, 61, 5]]_2, \quad [[81, 63, 5]]_2, \quad [[83, 65, 5]]_2, \quad [[85, 67, 5]]_2, \quad [[87, 69, 5]]_2, \quad [[89, 71, 5]]_2, \quad [[91, 73, 5]]_2}$$
