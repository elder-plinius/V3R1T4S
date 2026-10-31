# How We Found It

contributor text, unverified

The published transfer-matrix approach for OEIS A182275 tracks the state of a vertical cut across $n$ rows. Because each row cell along a vertical cut can be closed (`0`), open-start (`1`), or open-continuation (`2`, valid only after `1` or `2`), the vertical cut has $F(2n+1)$ states ($196,418$ states at $n=13$, $514,229$ at $n=14$, and $1,346,269$ at $n=15$).

Instead of cutting along vertical grid lines, we parametrized each column by its $n-1$ interior horizontal unit segments $h \in \{0, 1\}^{n-1}$, which has only $2^{n-1}$ states ($4,096$ states at $n=13$ — a $48\times$ state reduction at $n=13$ and an $(1.309)^n$ exponential asymptotic reduction).

Between two adjacent columns with horizontal segment masks $h_1, h_2 \in \{0, 1\}^{m-1}$, the vertical segments $v_0, \dots, v_{m-1} \in \{0, 1\}^m$ along the shared vertical grid line are governed by two equivalent, dual characterizations:
1. **Bottom-to-Top Vertex-Degree Continuity (`Method 1`)**: At interior grid vertex $i \in \{0, \dots, m-2\}$ with horizontal incident edges $(L_i, R_i) = (h_1[i], h_2[i])$ and vertical incident edges $(B_i, T_i) = (v_i, v_{i+1})$, forbidding degree-1 dead-ends and degree-2 L-corners requires $B_i = T_i$ when $(L_i, R_i) = (0, 0)$, $B_i = T_i = 1$ when $L_i \ne R_i$, and leaves $(B_i, T_i) \in \{0, 1\}^2$ unconstrained when $(L_i, R_i) = (1, 1)$.
2. **Recursive Kronecker-Block Divide-and-Conquer (`Method 2`)**: The $2^{m-1} \times 2^{m-1}$ column transfer operator $M_{m-1}$ satisfies the coupled Kronecker block recurrence $M_k = \begin{pmatrix} M_{k-1} + B_{k-1} & B_{k-1} \\ B_{k-1} & M_{k-1} \end{pmatrix}$, $B_k = \begin{pmatrix} 2 B_{k-1} & B_{k-1} \\ B_{k-1} & M_{k-1} \end{pmatrix}$ with $M_0 = (2), B_0 = (1)$, enabling fast divide-and-conquer matrix-vector multiplication without any vertex-by-vertex profile sweep.
3. **Vertical-Cut Fibonacci Transfer Matrix (`Method 3`)**: We also implemented the dual $F(2m+1)$-state vertical-cut transfer matrix over $v \in \{0, 1\}^m$ and shared horizontal bits at $(v_i, v_{i+1}) = (0, 0)$, verifying exact agreement across $0 \le m, n \le 6$.
