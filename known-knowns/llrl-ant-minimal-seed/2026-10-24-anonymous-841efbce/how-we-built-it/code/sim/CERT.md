# Exact translate certificate (used by ant.c, lcb.c, ccheck.py; hsearch.c uses the phase lists it justifies)

Setting. Rule w over colours 0..n-1, configuration s_t : Z^2 -> colours, finitely many non-zero cells, ant pose (x_t, h_t).
r_t = s_t(x_t) is the colour read at update t.

Claim. Fix t, P >= 1. Let A = {x_t, ..., x_{t+P-1}} (cells read in [t, t+P)), D = x_{t+P} - x_t != 0, and h_{t+P} = h_t.
Let U = union_{j>=0} (A + jD). If s_{t+P}(c + D) = s_t(c) for every c in U, then r_{u+P} = r_u for every u >= t
(the configuration is on a highway with period dividing P and drift D from time t).

Proof. Write X_j(c) = s_{t+jP}(c + jD) (the state seen from the ant's shifted frame after j periods). The ant's motion in
[t+jP, t+(j+1)P) depends only on X_j restricted to the cells it reads, and the pose relative to the frame is the same
for every j. Suppose X_1 = X_0 on U. Then during the next period the shifted ant starts at the same relative pose and
reads cells of A (relative), where X_1 = X_0, so it makes the same reads, the same moves, and the same writes as in
period 0; hence X_2 on U equals the image of X_1 under the same period-map that took X_0 to X_1 on U. Cells of U
outside A are untouched by one period, and U + D is a subset of U, so the update of X_1 on U uses only X_1 on U.
The period map F (on U-restricted states, read-set A, writes on A, plus shift by D) satisfies X_{j+1}|U = F(X_j|U),
and X_1|U = X_0|U gives X_j|U = X_0|U for all j by induction; reads are therefore P-periodic.  []

Finite check. Along each ray c, c+D, c+2D, ... (c in A) both s_t and s_{t+P} are zero once the projection <c, D>
exceeds the maximum projection of the support of s_t and of s_{t+P}; the condition then holds trivially. So the check
stops at that projection bound (implemented identically in all three codes; written independently).

Converse. If r is P-periodic from t with drift D, the first reads in period j+1 of shifted cells see the same colours
as period j, so the condition holds on the cells the ant ever reads; cells of U never read do not matter for the
conclusion, but can make the check fail. We therefore use the certificate only as a sufficient condition, and compute
the least onset by backward extension of the periodic read word (t* = least t with r_u = r_{u+P} for all u >= t),
which is exact once periodicity from some t is certified (periodicity from t implies the comparison r_u = r_{u+P}
for all u >= t; the least such t is the onset for period P, and any other period of the tail is a multiple of the
least period, which gives the same least t).  At t* - 1 the comparison fails, so no period gives an earlier onset
(verified as cert FAIL at onset-1 in every reported line).

Controls: Langton RL blank onset 9977 P 104 (known); RL k=4 seed onset 67 (f(T) run); LLRL blank 256241 P 384.
