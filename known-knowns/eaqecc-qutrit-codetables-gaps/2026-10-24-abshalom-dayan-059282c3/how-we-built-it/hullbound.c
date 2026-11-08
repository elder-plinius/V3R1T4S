/* Exact upper bound on the Hermitian hull of every Construction X code from a pair C1 > C2.
   Input (stdin): "K1 K2 n" and K1 rows of n over GF(9) (codes a + 3b), the first K2 rows spanning C2.
   An X code is C = {(c, tau(c)) : c in C1} with tau: C1 -> GF(9)^m linear, kernel C2 (any tail code A of dimension
   K1 - K2 and any isomorphism M), with column scalings; a scaling enters the Hermitian Gram only through its norm,
   +-1. With the C1 basis "C2 rows, then complement rows", the Gram matrix of C under head signs e is
       [[P, Q], [Q^dagger, R + T]],  [P Q] = sum_t e_t g2_t g1_t^dagger (K2 x K1),  T = M (A E_tail A^dagger) M^dagger,
   so for every tail and every M: rank(Gram) >= rank[P Q] + rank[P; Q^dagger] - rank P = 2 rank[P Q] - rank P
   (the standard minimal-rank-completion bound; [P; Q^dagger] is the conjugate transpose of [P Q]), hence
       hull(C) = K1 - rank(Gram) <= K1 - 2 rho1 + rho0,   rho1 = rank[P Q],  rho0 = rank P.
   Exact value (all tails): with W = C1 ∩ C2^perp(e) (dimension K1 - rho1, containing K = C2 ∩ C2^perp(e)), the Gram
   reduces to rank = 2 rho1 - rho0 + rank((H + Pi)|W), Pi the tail form pulled back to C1 (zero on C2, rank r = rank of
   the tail Gram A E_tail A^dagger); Pi|W is any form on W/K (dimension u = K1 - K2 - q, q = rho1 - rho0) whose rank is
   in [max(0, r - 2q), min(r, u)], so max hull = bound - mu, mu = min over tail ranks r and those ranks of |s - rank|,
   s = rank(H|W). Tail ranks r: enumerated over every [5,3,3] GRS tail (5 of the 10 points, all tail signs).
   Modes:
     bound            all 2^(n-1) head sign patterns (e_0 = +1; a global sign does not change ranks), Gray code;
                      prints the histogram of (rho1, rho0), the maximal bound and up to 20 patterns attaining it.
     test SEED TRIES  random X codes (head signs, m = 5 GRS tail points, tail signs, invertible M): their true hull
                      (direct Gram rank) must never exceed the bound for their head signs.
     real EPS SEED TRIES   for head signs EPS (n chars of + and -): random tails, report the best true hull found.
   Usage: hullbound bound < pair.xin;  hullbound test 1 100000 < pair.xin;  hullbound real +-+... 1 200000 < pair.xin */
#include "gf9.h"
#define NN 40
static int K1, K2, n, C[MAXK * NN];
static void sumPQ(const int *eps, int *S) {               /* S = [P Q], K2 x K1 */
  for (int i = 0; i < K2; i++) for (int j = 0; j < K1; j++) { int s = 0;
    for (int t = 0; t < n; t++) { int v = MUL[C[i * n + t]][CONJ[C[j * n + t]]]; s = ADD[s][eps[t] > 0 ? v : NEG[v]]; }
    S[i * K1 + j] = s; }
}
static int bound_of(const int *S, int *r1, int *r0) {
  int T[MAXK * MAXK], U[MAXK * MAXK];
  memcpy(T, S, sizeof(int) * K2 * K1); *r1 = rank9(K2, K1, T);
  for (int i = 0; i < K2; i++) for (int j = 0; j < K2; j++) U[i * K2 + j] = S[i * K1 + j];
  *r0 = rank9(K2, K2, U);
  return K1 - 2 * *r1 + *r0;
}
static int RT[4];                                           /* achievable tail ranks */
static void tail_ranks(void) {
  for (int a = 0; a < 1024; a++) { if (__builtin_popcount(a) != 5) continue; int pts[5], c = 0;
    for (int b = 0; b < 10; b++) if (a >> b & 1) pts[c++] = b;
    for (int sg = 0; sg < 32; sg++) { int A[3][5], D[9];
      for (int c2 = 0; c2 < 5; c2++) { int x = pts[c2];
        if (x == 9) { A[0][c2] = 0; A[1][c2] = 0; A[2][c2] = 1; } else { A[0][c2] = 1; A[1][c2] = x; A[2][c2] = MUL[x][x]; } }
      for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) { int t = 0;
        for (int c2 = 0; c2 < 5; c2++) { int v = MUL[A[i][c2]][CONJ[A[j][c2]]]; t = ADD[t][(sg >> c2 & 1) ? NEG[v] : v]; }
        D[i * 3 + j] = t; }
      RT[rank9(3, 3, D)] = 1; } }
}
static int exact_of(const int *eps, const int *S, int r1, int r0, int b, int *sout) {
  /* basis of W: x with S conj(x) = 0 */
  int R[MAXK * MAXK]; memcpy(R, S, sizeof(int) * K2 * K1);
  int piv[MAXK], r = 0;
  for (int c = 0; c < K1 && r < K2; c++) {
    int p = -1; for (int i = r; i < K2; i++) if (R[i * K1 + c]) { p = i; break; }
    if (p < 0) continue;
    for (int j = 0; j < K1; j++) { int t = R[r * K1 + j]; R[r * K1 + j] = R[p * K1 + j]; R[p * K1 + j] = t; }
    int iv = INV[R[r * K1 + c]]; for (int j = 0; j < K1; j++) R[r * K1 + j] = MUL[R[r * K1 + j]][iv];
    for (int i = 0; i < K2; i++) if (i != r && R[i * K1 + c]) { int f = NEG[R[i * K1 + c]];
      for (int j = 0; j < K1; j++) R[i * K1 + j] = ADD[R[i * K1 + j]][MUL[f][R[r * K1 + j]]]; }
    piv[r++] = c; }
  int isp[MAXK] = {0}; for (int i = 0; i < r; i++) isp[piv[i]] = 1;
  int X[MAXK][MAXK], dw = 0;
  for (int f = 0; f < K1; f++) if (!isp[f]) { int y[MAXK] = {0}; y[f] = 1;
    for (int i = 0; i < r; i++) y[piv[i]] = NEG[R[i * K1 + f]];
    for (int j = 0; j < K1; j++) X[dw][j] = CONJ[y[j]]; dw++; }
  int Hf[MAXK][MAXK];
  for (int i = 0; i < K1; i++) for (int j = 0; j < K1; j++) { int t = 0;
    for (int c = 0; c < n; c++) { int v = MUL[C[i * n + c]][CONJ[C[j * n + c]]]; t = ADD[t][eps[c] > 0 ? v : NEG[v]]; }
    Hf[i][j] = t; }
  int Gw[MAXK * MAXK];
  for (int a = 0; a < dw; a++) for (int c = 0; c < dw; c++) { int t = 0;
    for (int i = 0; i < K1; i++) if (X[a][i]) for (int j = 0; j < K1; j++) if (X[c][j])
      t = ADD[t][MUL[MUL[X[a][i]][CONJ[X[c][j]]]][Hf[i][j]]];
    Gw[a * dw + c] = t; }
  int s_ = rank9(dw, dw, Gw); *sout = s_;
  int q = r1 - r0, u = K1 - K2 - q, mu = 99;
  for (int rr = 0; rr <= 3; rr++) if (RT[rr]) {
    int lo = rr - 2 * q; if (lo < 0) lo = 0; int hi = rr < u ? rr : u;
    for (int rho = lo; rho <= hi; rho++) { int m = s_ > rho ? s_ - rho : rho - s_; if (m < mu) mu = m; } }
  return b - mu;
}
static int true_hull(const int *eps, const int *pts, const int *teps, const int *M, int m) {
  int A[3][10], G[MAXK * NN], N = n + m, H[MAXK * MAXK], d = K1 - K2;
  for (int c = 0; c < m; c++) { int a = pts[c];
    if (a == 9) { A[0][c] = 0; A[1][c] = 0; A[2][c] = 1; } else { A[0][c] = 1; A[1][c] = a; A[2][c] = MUL[a][a]; } }
  for (int i = 0; i < K1; i++) {
    for (int t = 0; t < n; t++) G[i * N + t] = C[i * n + t];
    for (int c = 0; c < m; c++) { int s = 0;
      if (i >= K2) for (int l = 0; l < d; l++) s = ADD[s][MUL[M[(i - K2) * d + l]][A[l][c]]];
      G[i * N + n + c] = s; } }
  for (int i = 0; i < K1; i++) for (int j = 0; j < K1; j++) { int s = 0;
    for (int t = 0; t < N; t++) { int v = MUL[G[i * N + t]][CONJ[G[j * N + t]]];
      int e = t < n ? eps[t] : teps[t - n]; s = ADD[s][e > 0 ? v : NEG[v]]; }
    H[i * K1 + j] = s; }
  return K1 - rank9(K1, K1, H);
}
static void rand_tail(int *pts, int *teps, int *M, int m) {
  int p[10] = {0,1,2,3,4,5,6,7,8,9};
  for (int i = 9; i > 0; i--) { int j = rand() % (i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; }
  for (int c = 0; c < m; c++) { pts[c] = p[c]; teps[c] = rand() % 2 ? 1 : -1; }
  int T[9]; do { for (int e = 0; e < 9; e++) M[e] = rand() % 9; memcpy(T, M, sizeof T); } while (rank9(3, 3, T) < 3);
}
int main(int argc, char **argv) {
  gf_init();
  if (scanf("%d %d %d", &K1, &K2, &n) != 3 || K1 > MAXK || n > NN) return 2;
  for (int i = 0; i < K1 * n; i++) if (scanf("%d", &C[i]) != 1) return 2;
  int eps[NN], S[MAXK * MAXK], r1, r0;
  if (argc > 1 && !strcmp(argv[1], "bound")) {
    for (int t = 0; t < n; t++) eps[t] = 1;
    sumPQ(eps, S);
    int O[NN][MAXK * MAXK];                                    /* O_t = g2_t g1_t^dagger */
    for (int t = 0; t < n; t++) for (int i = 0; i < K2; i++) for (int j = 0; j < K1; j++)
      O[t][i * K1 + j] = MUL[C[i * n + t]][CONJ[C[j * n + t]]];
    long hist[MAXK + 1][MAXK + 1]; memset(hist, 0, sizeof hist); int best = -99, shown = 0, bestx = -99, shownx = 0;
    long exhist[MAXK + 1] = {0}; tail_ranks(); printf("tail ranks achievable:"); for (int rr = 0; rr <= 3; rr++) if (RT[rr]) printf(" %d", rr); printf("\n");
    unsigned long total = 1UL << (n - 1);
    for (unsigned long g = 0; g < total; g++) {
      if (g) { int t = 1 + __builtin_ctzl(g);                  /* Gray code: flip coordinate t (1..n-1) */
        /* e_t -> -e_t changes S by -2 e_t O_t = e_t O_t (mod 3) */
        for (int x = 0; x < K2 * K1; x++) S[x] = ADD[S[x]][eps[t] > 0 ? O[t][x] : NEG[O[t][x]]];
        eps[t] = -eps[t]; }
      int b = bound_of(S, &r1, &r0); hist[r1][r0]++;
      if (b >= 5) { int sw, x = exact_of(eps, S, r1, r0, b, &sw); exhist[x < 0 ? 0 : x]++;
        if (x > bestx) { bestx = x; shownx = 0; }
        if (x == bestx && shownx < 20) { shownx++; printf("exact %d bound %d rho1 %d rho0 %d s %d eps ", x, b, r1, r0, sw);
          for (int t = 0; t < n; t++) putchar(eps[t] > 0 ? '+' : '-'); putchar('\n'); fflush(stdout); } }
      if (b > best) { best = b; shown = 0; }
      if (b == best && shown < 20) { shown++; printf("bound %d rho1 %d rho0 %d eps ", b, r1, r0);
        for (int t = 0; t < n; t++) putchar(eps[t] > 0 ? '+' : '-'); putchar('\n'); }
    }
    printf("patterns %lu\nhistogram (rho1 rho0 count bound):\n", total);
    for (int a = 0; a <= K2; a++) for (int c = 0; c <= K2; c++) if (hist[a][c])
      printf("  %d %d %ld %d\n", a, c, hist[a][c], K1 - 2 * a + c);
    printf("max bound over all head sign patterns: %d\n", best);
    printf("exact max hull (over all tails) among patterns with bound >= 5, histogram:");
    for (int x = 0; x <= MAXK; x++) if (exhist[x]) printf(" %d:%ld", x, exhist[x]);
    printf("\nexact max hull over all X codes of this pair: %d (patterns with bound <= 4 have hull <= 4)\n", bestx > 4 ? bestx : 4);
    return 0;
  }
  if (argc > 3 && !strcmp(argv[1], "test")) {
    srand(atoi(argv[2])); tail_ranks(); long tries = atol(argv[3]), viol = 0, tight = 0, violx = 0; int pts[10], teps[10], M[9], mx = -1;
    for (long r = 0; r < tries; r++) {
      eps[0] = 1; for (int t = 1; t < n; t++) eps[t] = rand() % 2 ? 1 : -1;
      rand_tail(pts, teps, M, 5); sumPQ(eps, S); int b = bound_of(S, &r1, &r0), h = true_hull(eps, pts, teps, M, 5);
      int sw, x = exact_of(eps, S, r1, r0, b, &sw); if (h > x) violx++;
      if (h > b) viol++; if (h == b) tight++; if (h > mx) mx = h; }
    printf("test: %ld random X codes, true hull <= bound in all but %ld, <= exact in all but %ld, equal to bound in %ld, max true hull %d\n", tries, viol, violx, tight, mx);
    return (viol || violx) ? 1 : 0;
  }
  if (argc > 4 && !strcmp(argv[1], "real")) {
    for (int t = 0; t < n; t++) eps[t] = argv[2][t] == '-' ? -1 : 1;
    srand(atoi(argv[3])); long tries = atol(argv[4]); int pts[10], teps[10], M[9], best = -1;
    sumPQ(eps, S); int b = bound_of(S, &r1, &r0); tail_ranks(); int sw, x = exact_of(eps, S, r1, r0, b, &sw);
    printf("head: rho1 %d rho0 %d s %d bound %d exact %d\n", r1, r0, sw, b, x);
    for (long r = 0; r < tries; r++) { rand_tail(pts, teps, M, 5); int h = true_hull(eps, pts, teps, M, 5);
      if (h > best) { best = h; printf("try %ld: true hull %d (bound %d) pts", r, h, b);
        for (int c = 0; c < 5; c++) printf(" %d", pts[c]); printf(" teps "); for (int c = 0; c < 5; c++) putchar(teps[c] > 0 ? '+' : '-');
        printf(" M"); for (int e = 0; e < 9; e++) printf(" %d", M[e]); printf("\n"); fflush(stdout); }
      if (best == x) break; }
    printf("real: bound %d, exact %d, best true hull %d\n", b, x, best);
    return 0;
  }
  fprintf(stderr, "usage: see header\n"); return 2;
}
