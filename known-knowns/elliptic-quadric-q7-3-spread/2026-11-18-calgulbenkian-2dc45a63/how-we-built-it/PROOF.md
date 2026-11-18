# Complete Mathematical & Computational Proof (`elliptic-quadric-q7-3-spread`, Partial Win `p1`)

## Main Theorem (`PROVED-HERE`)

Let $Q^-(7,3) = \Omega^-(8,3)$ be the elliptic quadric in $\mathrm{PG}(7,3)$ defined over $\mathbb{F}_3^8$ by the quadratic form
$$Q(x) = x_1 x_2 + x_3 x_4 + x_5 x_6 + x_7^2 + x_8^2 \pmod 3,$$
with polar symmetric bilinear form $B(x, y) = Q(x + y) - Q(x) - Q(y) \pmod 3$ and symmetric invertible Gram matrix $G = \operatorname{diag}\!\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}, \begin{smallmatrix}0&1\\1&0\end{smallmatrix}, \begin{smallmatrix}0&1\\1&0\end{smallmatrix}, 2, 2\right)$ satisfying $Q(x) \equiv 2 x^T G x \pmod 3$. A **spread** $\mathcal{S}$ of $Q^-(7,3)$ is a set of $82$ pairwise-disjoint totally singular planes ($3$-dimensional vector subspaces of $\mathbb{F}_3^8$) partitioning the $1{,}066$ singular projective points of $Q^-(7,3)$.

1. **(`PROVED-HERE`, Target Partial Win `p1`)** **No spread of $Q^-(7,3)$ admits an automorphism of order $3$.**
2. **(`PROVED-HERE`, Self-Contained Structural Corollary)** Moreover, no spread of $Q^-(7,3)$ admits any automorphism of prime order $p \in \{5, 7, 13, 41\}$ or any involution in the projective orthogonal isometry group $\mathrm{PO}^-(8,3)$. Consequently, for every spread $\mathcal{S}$ of $Q^-(7,3)$, $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3) = \{1\}$ and $|\mathrm{Aut}(\mathcal{S})| \in \{1, 2\}$ (any nontrivial automorphism is a fixed-point-free similarity involution in the field-reduction class `Inv_0_sim` with $Q(Hx) = 2Q(x)$ and $H^2 = 2I_8$).

Prior status (`KNOWN`, Kiermaier, Schmidt, and Wassermann, *Designs, Codes and Cryptography* 2025; `arXiv:2403.11188v3`, Sec. 6): existence of a spread of $\Omega^-(8,3)$ is open, and prior computer search restricted the prime-power divisors of the order of an automorphism to $\{2, 3\}$.

---

## Step 1. Polar Space Parameters & Positive Control on $Q^-(5,3)$ (`PROVED-HERE`)

- **Lemma 1.1 (`KNOWN` / `PROVED-HERE` by RREF enumeration):** Over $\mathbb{F}_3$, the quadratic form $x_7^2 + x_8^2$ is anisotropic ($x_7^2 + x_8^2 \equiv 0 \pmod 3 \iff x_7 = x_8 = 0$), so $Q$ has Witt index $3$ (elliptic type). Direct RREF enumeration in both independent engines confirms:
  - $\frac{(3^4 + 1)(3^3 - 1)}{3 - 1} = 82 \cdot 13 = 1{,}066$ singular projective points;
  - $\frac{(3^4 + 1)(3^3 + 1)(3^3 - 1)(3^2 - 1)}{(3^2 - 1)(3 - 1)} / 2 = 29{,}848$ totally singular projective lines ($4$ points per line);
  - $(3^2 + 1)(3^3 + 1)(3^4 + 1) = 10 \cdot 28 \cdot 82 = 22{,}960$ totally singular planes ($13$ points per plane), and zero totally singular $4$-dimensional vector subspaces.
- **Lemma 1.2 (`PROVED-HERE`, Positive Control on $Q^-(5,3)$):** Running the identical Cayley classification and Kramer-Mesner exact-cover pipeline on $Q^-(5,3)$ ($Q_6(x) = x_1 x_2 + x_3 x_4 + x_5^2 + x_6^2$, $112$ singular points, $280$ totally singular lines) constructs an explicit $28$-line spread invariant under an order-$3$ isometry $A_6 \in \mathrm{O}^-(6,3)$ (recorded as $28$ explicit $2 \times 6$ basis matrices in `object/q7_3_ord3_certificate.json` and checked in both verifiers).

---

## Step 2. Identification of the Full Automorphism Group $\mathrm{Aut}(Q^-(7,3)) = \mathrm{PGO}^-(8,3)$ (`PROVED-HERE`)

An automorphism of a spread $\mathcal{S}$ of $Q^-(7,3)$ is an automorphism $\sigma$ of the point-plane incidence geometry of $Q^-(7,3)$ preserving $\mathcal{S}$ (`KNOWN` definition, Kiermaier-Schmidt-Wassermann Sec. 5). Rather than relying solely on the Tits/Chow/Dieudonné theorem for polar spaces of rank $3 \ge 3$ (noting $\mathrm{Aut}(\mathbb{F}_3) = \{1\}$ so $\mathrm{P}\Gamma\mathrm{O}^-(8,3) = \mathrm{PGO}^-(8,3)$), we verify $\mathrm{Aut}(Q^-(7,3)) = \mathrm{PGO}^-(8,3)$ directly by elementary finite computation (`verify_engine2_dlx.c`, Step 2):

- **Lemma 2.1 (`PROVED-HERE`):** Let $\Gamma$ be the collinearity graph on the $1{,}066$ singular points ($u \sim v \iff u \ne v$ and $B(u, v) = 0$). Direct inspection over all $\binom{1066}{2} = 567{,}645$ point pairs confirms $u \sim v$ if and only if $u$ and $v$ lie in at least one common totally singular plane. Conversely, every clique $C$ of size $13$ in $\Gamma$ spans a totally singular subspace of dimension $\ge 3$ (a $2$-space has at most $4$ points) and $\le 3$ (Witt index is $3$), hence equals one of the $22{,}960$ planes. Thus $\mathrm{Aut}(Q^-(7,3)) = \mathrm{Aut}(\Gamma)$.
- **Lemma 2.2 (`PROVED-HERE`):** Define an ordered standard hyperbolic frame $(p_0, q_0, p_1, q_1, p_2, q_2)$ in $\Gamma$ by: $p_0 \in V(\Gamma)$ ($1{,}066$ choices); $q_0 \notin \{p_0\} \cup N_\Gamma(p_0)$ ($729$ choices); $p_1 \in N_\Gamma(p_0) \cap N_\Gamma(q_0)$ ($112$ choices); $q_1 \in (N_\Gamma(p_0) \cap N_\Gamma(q_0)) \setminus (\{p_1\} \cup N_\Gamma(p_1))$ ($81$ choices); and distinct $p_2 \ne q_2$ in $\bigcap_{i=0}^1 (N_\Gamma(p_i) \cap N_\Gamma(q_i)) \cong Q^-(3,3)$ ($10 \times 9 = 90$ choices, pairwise non-adjacent since $Q^-(3,3)$ has Witt index $1$). Thus there are at most
  $$1{,}066 \cdot 729 \cdot 112 \cdot 81 \cdot 10 \cdot 9 = 634{,}498{,}038{,}720$$
  ordered standard frames in $\Gamma$. Exact backtracking on $\Gamma$ (`count_gamma_aut_dfs`) proves that the pointwise stabilizer in $\mathrm{Aut}(\Gamma)$ of the canonical frame $F_0 = ([e_1], [e_2], [e_3], [e_4], [e_5], [e_6])$ has order **exactly $64$**. Hence
  $$|\mathrm{Aut}(Q^-(7,3))| = |\mathrm{Aut}(\Gamma)| \le 634{,}498{,}038{,}720 \times 64 = 40{,}607{,}874{,}478{,}080.$$
  Conversely, counting similarity bases $(c_1, \dots, c_8) \in (\mathbb{F}_3^8)^8$ with $c_i^T G c_j = \lambda G_{ij}$ ($\lambda \in \{1, 2\}$) gives $|\mathrm{GO}^-(8,3)| = 2 \cdot 2{,}132 \cdot 1{,}458 \cdot 224 \cdot 162 \cdot 20 \cdot 18 \cdot 4 \cdot 2 = 81{,}215{,}748{,}956{,}160$, with scalar kernel $\{\pm I_8\}$ of order $2$ on $Q^-(7,3)$, so $|\mathrm{PGO}^-(8,3)| = 40{,}607{,}874{,}478{,}080 = 2^{12} \cdot 3^{12} \cdot 5 \cdot 7 \cdot 13 \cdot 41$. Since $\mathrm{PGO}^-(8,3) \le \mathrm{Aut}(\Gamma)$, equality holds: $\mathrm{Aut}(Q^-(7,3)) = \mathrm{PGO}^-(8,3)$.

---

## Step 3. Constructive Classification of All Order-$3$ Conjugacy Classes in $\mathrm{PGO}^-(8,3)$ (`PROVED-HERE`)

- **Lemma 3.1 (`PROVED-HERE`, Unique Matrix Lift & Cayley Bijection):** Let $[M] \in \mathrm{PGO}^-(8,3)$ have order $3$, so $M \in \mathrm{GO}^-(8,3) \setminus \{\pm I_8\}$ satisfies $M^3 = s I_8$ with $s \in \{1, 2\}$. Replacing $M$ by $s M$ yields $(s M)^3 = s^3 M^3 = s^2 I_8 = I_8$ while $(-s M)^3 = -I_8 \ne I_8$; thus $[M]$ has a **unique** lift $A \in \mathrm{GO}^-(8,3)$ satisfying $A^3 = I_8, A \ne I_8$. If $Q(Ax) = \lambda Q(x)$ ($\lambda \in \{1, 2\}$), choosing $x$ with $Q(x) \ne 0$ gives $Q(x) = Q(A^3 x) = \lambda^3 Q(x) = \lambda Q(x)$, forcing $\lambda = 1$, i.e., $A \in \mathrm{O}^-(8,3)$.
  In characteristic $3$, $A^3 = I_8 \iff D^3 = 0$ for $D = A - I_8$. Hence $A + I_8 = -(I_8 - D)$ is invertible with inverse $-(I_8 + D + D^2)$. Cayley's map
  $$X := (A - I_8)(A + I_8)^{-1} = -(D + D^2), \qquad S := G X, \qquad A = (I_8 + X)(I_8 - X)^{-1} = I_8 + 2X + 2X^2$$
  is an **exact bijection** between $\{A \in \mathrm{O}^-(8,3) : A^3 = I_8, A \ne I_8\}$ and $\{S \in \mathfrak{so}_8(\mathbb{F}_3) \setminus \{0\} : (G^{-1} S)^3 = 0\}$. Under conjugation $A \mapsto M^{-1} A M$ by $M \in \mathrm{GO}^-(8,3)$ ($M^T G M = \lambda G$), $S$ transforms by scaled congruence $S \mapsto \lambda^{-1} M^T S M$.

- **Lemma 3.2 (`PROVED-HERE`, Exact Total Count $= 430{,}408{,}160$):** Every nonzero skew-symmetric $8 \times 8$ matrix $S$ has even rank $d \in \{2, 4, 6, 8\}$. Since $X = G^{-1} S$ satisfies $X^3 = 0$, Jordan blocks of $X$ have size $\le 3$, so $8 \le 3 \dim \ker(X) = 3(8 - d) \implies d \le 5$, forcing $d \in \{2, 4\}$. Let $U = \operatorname{im}(X)$ ($\dim U = d$); because $B(u, Xv) = u^T S v = -B(Xu, v)$, $\ker(X) = U^{\perp_B}$. Therefore
  $$X^3 = 0 \iff X(U) \subseteq U \cap \ker(X) = U \cap U^{\perp_B} = \operatorname{rad}_B(U).$$
  Since $\ker(X|_U) = U \cap \ker(X) = \operatorname{rad}_B(U)$ has dimension $r_0 \le 3$ (Witt index $3$), $\dim X(U) = d - r_0 \le r_0 \implies r_0 \ge d/2$. Exhaustive RREF enumeration in `verify_engine2_dlx.c` (Step 3) verifies all four strata:
  1. $d = 2, r_0 = 2$: $U$ is one of the $29{,}848$ totally singular lines, with $2$ nonzero skew forms each $\implies 59{,}696$ elements.
  2. $d = 2, r_0 = 1$: $U$ is one of the $268{,}632$ rank-$1$ degenerate $2$-spaces (verified across all $896{,}260$ $2$-spaces of $\mathbb{F}_3^8$), with $2$ skew forms each $\implies 537{,}264$ elements.
  3. $d = 4, r_0 = 3$: $\operatorname{rad}_B(U)$ is one of the $22{,}960$ totally singular planes $\Pi$, $U/\Pi$ is one of the $4$ projective points of $\Pi^\perp/\Pi$, and all $468$ invertible $4 \times 4$ skew forms satisfy $X^3 = 0$ $\implies 22{,}960 \cdot 4 \cdot 468 = 42{,}981{,}120$ elements.
  4. $d = 4, r_0 = 2$: $\operatorname{rad}_B(U)$ is one of the $29{,}848$ totally singular lines $L$, $U/L$ is one of the $90$ nondegenerate $2$-spaces of $L^\perp/L \cong Q^-(3,3)$ ($45$ hyperbolic secants + $45$ elliptic passants), and exactly $144$ of the $468$ invertible $4 \times 4$ skew forms make $U/L$ Lagrangian (`X(U) <= L`) $\implies 29{,}848 \cdot 90 \cdot 144 = 386{,}830{,}080$ elements.
  Total elements of order $3$ in $\mathrm{PGO}^-(8,3)$:
  $$59{,}696 + 537{,}264 + 42{,}981{,}120 + 386{,}830{,}080 = 430{,}408{,}160.$$

- **Lemma 3.3 (`PROVED-HERE`, 100% Constructive Conjugacy-Class Completeness):** The five certified matrices `C3_94`, `C3_121`, `C3_13`, `C3_4`, `C3_22` have pairwise distinct fixed-point counts $(94, 121, 13, 4, 22)$ on $Q^-(7,3)$, hence lie in **five pairwise disjoint conjugacy classes** of $\mathrm{PGO}^-(8,3)$. In `verify_engine2_dlx.c` (Step 3):
  - Direct BFS closure under $10$ explicit generators of $\mathrm{GO}^-(8,3)$ over the $596{,}960$ rank-$2$ forms visits **exactly $59{,}696$** conjugates of `C3_94` and **exactly $537{,}264$** conjugates of `C3_121`.
  - Exhaustive Jordan-chain enumeration in $\mathrm{GO}^-(8,3)/\langle -I_8 \rangle$ computes $|\mathrm{C}_{\mathrm{PGO}}(\text{C3\_13})| = 944{,}784$, $|\mathrm{C}_{\mathrm{PGO}}(\text{C3\_4})| = 209{,}952$, and $|\mathrm{C}_{\mathrm{PGO}}(\text{C3\_22})| = 209{,}952$, yielding class sizes $42{,}981{,}120$, $193{,}415{,}040$, and $193{,}415{,}040$.
  Summing the five disjoint classes gives $59{,}696 + 537{,}264 + 42{,}981{,}120 + 193{,}415{,}040 + 193{,}415{,}040 = 430{,}408{,}160$, proving **100% conjugacy-class completeness with zero random sampling**.

---

## Step 4. Exclusion of All Five Order-$3$ Conjugacy Classes (`PROVED-HERE`)

For $g \in \mathrm{PGO}^-(8,3)$ of order $3$ preserving a spread $\mathcal{S}$, every $g$-orbit of planes in $\mathcal{S}$ is either a $g$-fixed plane or a triple $\{\Pi, g(\Pi), g^2(\Pi)\}$ of pairwise-disjoint planes. Every $g$-fixed point $P \in Q^-(7,3)$ must lie in a $g$-fixed plane of $\mathcal{S}$ (otherwise $P \in \Pi \cap g(\Pi) \ne \emptyset$).

1. **`C3_121` (`fix_pts = 121`, `436 x 280`):** Because $\dim \ker(A - I) = 6$, every plane $\Pi$ satisfies $\dim(\Pi \cap \ker(A - I)) \ge 3 + 6 - 8 = 1$, so zero disjoint plane $3$-orbits exist (`disjoint_3_orbits = 0`), leaving $243$ point $3$-orbits covered by $0$ options (`UNSAT` in $0$ branches).
2. **`C3_94` (`fix_pts = 94`, `418 x 1090`):** Again $\dim \ker(A - I) = 6 \implies$ `disjoint_3_orbits = 0`, and every $A$-fixed plane intersects the $4$-point totally singular line $L = \operatorname{im}(X)$, so at most $4 < 82$ pairwise-disjoint fixed planes exist (`UNSAT` in $\le 11$ branches in both engines).
3. **`C3_22` (`fix_pts = 22`, `370 x 5842`):** The $18$ fixed points outside $L = \operatorname{rad}_B(U)$ lie on two planes $\langle L, Q_1 \rangle$ and $\langle L, Q_2 \rangle$ with degree $1$, forcing both planes into $\mathcal{S}$, where they intersect along $L$ (`UNSAT` in $\le 2$ branches).
4. **`C3_4` (`fix_pts = 4`, `358 x 5896`):** Exact cover proves `UNSAT` in $\le 11$ branches (`< 0.001s` in both engines).
5. **`C3_13` (`fix_pts = 13`, `364 x 6598`):**
   - **Fixed-plane dichotomy (`PROVED-HERE`):** The $13$ fixed points form a single totally singular plane $\Pi_* = \operatorname{rad}_B(U)$. Direct check of all $37$ $A$-fixed planes shows $\Pi_*$ covers all $13$ fixed points while every one of the other $36$ fixed planes intersects $\Pi_* \cong \mathrm{PG}(2,3)$ in a $4$-point line. Since any two lines in $\mathrm{PG}(2,3)$ intersect (and $4 < 13$), $\Pi_* \notin \mathcal{S}$ (`Case B`) is impossible; hence **every $A$-invariant spread must contain $\Pi_*$ (`Case A`)**, reducing `C3_13` to choosing $27$ plane $3$-orbits from `6,561` options partitioning the $351$ non-fixed point $3$-orbits.
   - **Exact Normalizer Symmetry Breaking (`PROVED-HERE`):** Enumerating $N = N_{\mathrm{PGO}^-(8,3)}(\langle A \rangle)$ constructs all $|N| = 1{,}889{,}568$ projective normalizer elements (`2 x 944,784`). Direct orbit evaluation verifies that **$N$ acts transitively on all $6{,}561$ plane $3$-orbits** (`1` single orbit, $|\mathrm{Stab}_N(O_0)| = 288$). Thus WLOG $O_0 \in \mathcal{S}$. Under $\mathrm{Stab}_N(O_0)$, there is an uncovered point $3$-orbit $r_1$ of orbit size $2$ (`|\mathrm{Stab}_N(O_0, r_1)| = 144`), splitting the $144$ options compatible with $O_0$ that cover $r_1$ into **exactly $4$ canonical Depth-$1$ branches** $j_1 \in \{b_0, b_1, b_2, b_3\}$.
   - **Staged Pair-Orbit Elimination & Dual-Engine `UNSAT` (`PROVED-HERE`):** Processing $b_0, b_1, b_2, b_3$ in decreasing order of $|\mathrm{Stab}_N(\{O_0, b_s\})| \in \{12, 6, 3, 3\}$, for each $b_s$ we pick an uncovered item $r_2$ minimizing $\mathrm{Stab}_N(\{O_0, b_s\}, r_2)$-orbits of compatible Depth-$2$ options $j_2$. Once Stage $s$ is proved exhaustively `UNSAT`, no $A$-invariant spread can contain `{O_0, b_s}`, hence by $N$-invariance **no $A$-invariant spread can contain any pair $\{u, v\} \in \mathrm{Orb}_N(\{O_0, b_s\})$**, eliminating those pairs in Stages $> s$:
     - **Engine 1 (`how-we-built-it/solve_ord3_staged_swar.c`, 64-bit SWAR bitsets `uint64_t[103]`):** `0` solutions across `144` canonical Depth-$2$ tasks (`8,796,560` branching nodes, `15.6s` on 4 threads; also verified without cross-stage pair deletion across all `243` Depth-$2$ tasks in `43,626,688` nodes, `64.3s`).
     - **Engine 2 (`verify-it-yourself/verify_engine2_dlx.c`, zero-shared-code RREF builder + Row-Elimination Dancing Links):** `0` solutions across `143` canonical Depth-$2$ tasks (`8,776,899` deterministic branching nodes, `52.3s`).

---

## Step 5. Self-Contained Exclusion of Primes $\{5, 7, 13, 41\}$ and All $\mathrm{PO}^-(8,3)$ Involutions (`PROVED-HERE`)

- **Lemma 5.1 (`PROVED-HERE`, Odd Primes $\{5, 7, 13, 41\}$):** Because $|\mathrm{PGO}^-(8,3)| = 2^{12} \cdot 3^{12} \cdot 5^1 \cdot 7^1 \cdot 13^1 \cdot 41^1$, for each $p \in \{5, 7, 13, 41\}$ the Sylow $p$-subgroups of $\mathrm{PGO}^-(8,3)$ are cyclic of prime order $p$ and form a **single conjugacy class** by Sylow's Second Theorem. Direct inspection of one explicit matrix $G_p \in \mathrm{O}^-(8,3)$ of order $p$ excludes all four immediately:
  - $p = 5$: $16$ fixed points, $0$ fixed planes $\implies$ impossible;
  - $p = 7$: $2$ fixed points, $0$ fixed planes $\implies$ impossible;
  - $p = 13$: $82 \equiv 4 \pmod{13}$ forces $\ge 4$ fixed planes, whereas only $2$ fixed planes exist $\implies$ impossible;
  - $p = 41$: $0$ fixed planes and $0$ disjoint plane $41$-orbits $\implies$ impossible.
- **Lemma 5.2 (`PROVED-HERE`, All Involutions in $\mathrm{PO}^-(8,3)$):** Let $[H] \in \mathrm{PO}^-(8,3) = \mathrm{O}^-(8,3)/\{\pm I_8\}$ have order $2$, so $H^2 = s I_8$ ($s \in \{1, 2\}$).
  - First, $s = 2$ ($H^2 = -I_8$) is impossible in $\mathrm{O}^-(8,3)$: if $H^T G H = G$ and $H^2 = -I_8$, then $h(u, v) = B(u, v) + i B(u, Hv)$ defines a nondegenerate Hermitian form on $\mathbb{F}_9^4$ ($\mathbb{F}_9 = \mathbb{F}_3[i], i^2 = -1$). Because the norm $\mathbb{F}_9^\times \to \mathbb{F}_3^\times$ is surjective, $(\mathbb{F}_9^4, h)$ admits an orthonormal basis $e_1, \dots, e_4$ ($h(e_k, e_k) = 1$), giving an $\mathbb{F}_3$-basis $\{e_1, He_1, \dots, e_4, He_4\}$ in which $B$ has Gram matrix $I_8$ ($\det = 1$), contradicting $\det(G) = (-1)^3 \cdot 2 \cdot 2 \equiv 2 \pmod 3$ (not a square in $\mathbb{F}_3^\times$).
  - Second, for $s = 1$ ($H^2 = I_8, H \ne \pm I_8$), $H$ is uniquely determined up to sign by the orthogonal decomposition $\mathbb{F}_3^8 = V_+ \perp V_-$ with $1 \le \dim V_- \le 4$. Exact orthogonal group order formulas confirm the five classes `Inv_364` ($2{,}214$), `Inv_130` ($209{,}223$), `Inv_114` ($388{,}557$), `Inv_44` ($16{,}319{,}394$), and `Inv_26` ($24{,}479{,}091$) sum to all $41{,}398{,}479$ involutions in $\mathrm{PO}^-(8,3)$. All five are `UNSAT` in $\le 1{,}313$ DLX branches (and by elementary fixed-point counting: `Inv_364, Inv_130, Inv_114` have zero disjoint $2$-orbits and uncoverable point orbits; in `Inv_44` at most $4$ fixed planes cover $\le 16 < 40$ points of $V_+$; in `Inv_26` covering $10$ points of $V_+ \cong Q^-(3,3)$ requires $10$ fixed planes covering $40 > 16$ points of $V_- \cong Q^+(3,3)$).
- **Corollary 5.3 (`PROVED-HERE`):** By Steps 4 and 5, $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3)$ contains no element of prime order $p \in \{2, 3, 5, 7, 13, 41\}$, hence $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3) = \{1\}$. Since $[\mathrm{PGO}^-(8,3) : \mathrm{PO}^-(8,3)] = 2$, $|\mathrm{Aut}(\mathcal{S})| \in \{1, 2\}$.
