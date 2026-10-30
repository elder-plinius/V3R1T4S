/* Exact upper bound on the Hermitian hull of every Construction X code from a pair C1 > C2, for a tail of dimension
   dt = K1 - K2 and length m (generalized from an earlier hullbound.c, not shipped here,
   which was fixed at dt = 3, m = 5). Input (stdin): "K1 K2 n" and K1 rows of n over GF(9) (codes a + 3b), the first K2
   rows spanning C2. An X code is C = {(c, tau(c)) : c in C1}, tau: C1 -> GF(9)^m linear with kernel C2 (a tail code A
   of dimension dt and an isomorphism M), with column scalings; a scaling enters the Hermitian Gram only through its
   norm, +-1. With the C1 basis "C2 rows, then complement rows", the Gram matrix under head signs e is
       [[P, Q], [Q^dagger, R + T]],  [P Q] = sum_t e_t g2_t g1_t^dagger (K2 x K1),  T = M (A E_tail A^dagger) M^dagger,
   so hull(C) = K1 - rank(Gram) <= K1 - 2 rho1 + rho0 (rho1 = rank[P Q], rho0 = rank P; minimal-rank completion).
   Exact value over all tails: with W = C1 ∩ C2^perp(e) and K = C2 ∩ C2^perp(e), rank = 2 rho1 - rho0 +
   rank((H + Pi)|W), Pi the pulled-back tail form (rank r = rank of the tail Gram), Pi|W any form on W/K (dimension
   u = dt - q, q = rho1 - rho0) of rank in [max(0, r - 2q), min(r, u)]; max hull = bound - mu, mu = min |s - rank|
   over achievable r and those ranks, s = rank(H|W). Hermitian forms over GF(9) are classified by rank, so only r
   matters. Two tail families: GRS (every m of the 10 points of the projective line, rows 1, x, ..., x^(dt-1), the
   point at infinity as e_(dt-1), all 2^m tail signs: the achievable r are enumerated), and ANY tail code of length m
   and dimension dt (its hull is at most min(dt, m - dt), so r ranges over [max(0, 2 dt - m), dt]): an upper bound
   for every tail, MDS or not.
   Only patterns with bound >= THR get the exact computation; rho0 is computed first and patterns with
   K1 - rho0 < THR are skipped (bound = K1 - 2 rho1 + rho0 <= K1 - rho0 since rho1 >= rho0).
   Modes:
     bound M THR           all 2^(n-1) head sign patterns (e_0 = +1), Gray code.
     test M SEED TRIES     random X codes with GRS tails: true hull <= exact (GRS) <= exact (any) <= bound.
     real M EPS SEED TRIES for head signs EPS, random GRS tails; best true hull found.  */
#include "gf9.h"
#define NN 40
static int K1, K2, n, dt, mt, C[MAXK * NN], RTG[MAXK + 1], RTA[MAXK + 1];
static void sumPQ(const int *eps, int *S) {
  for (int i = 0; i < K2; i++) for (int j = 0; j < K1; j++) { int s = 0;
    for (int t = 0; t < n; t++) { int v = MUL[C[i * n + t]][CONJ[C[j * n + t]]]; s = ADD[s][eps[t] > 0 ? v : NEG[v]]; }
    S[i * K1 + j] = s; }
}
static int rank_P(const int *S) { int U[MAXK * MAXK];
  for (int i = 0; i < K2; i++) for (int j = 0; j < K2; j++) U[i * K2 + j] = S[i * K1 + j];
  return rank9(K2, K2, U); }
static int rank_PQ(const int *S) { int T[MAXK * MAXK]; memcpy(T, S, sizeof(int) * K2 * K1); return rank9(K2, K1, T); }
static void tailrow(int x, int *col) { /* column of the GRS tail generator at point x (9 = infinity) */
  for (int l = 0; l < dt; l++) col[l] = 0;
  if (x == 9) { col[dt - 1] = 1; return; }
  int p = 1; for (int l = 0; l < dt; l++) { col[l] = p; p = MUL[p][x]; } }
static void tail_ranks(void) {
  memset(RTG, 0, sizeof RTG); memset(RTA, 0, sizeof RTA);
  for (int a = 0; a < 1024; a++) { if (__builtin_popcount(a) != mt) continue; int pts[10], c = 0;
    for (int b = 0; b < 10; b++) if (a >> b & 1) pts[c++] = b;
    int A[10][MAXK]; for (int c2 = 0; c2 < mt; c2++) tailrow(pts[c2], A[c2]);
    for (int sg = 0; sg < (1 << mt); sg++) { int D[MAXK * MAXK];
      for (int i = 0; i < dt; i++) for (int j = 0; j < dt; j++) { int t = 0;
        for (int c2 = 0; c2 < mt; c2++) { int v = MUL[A[c2][i]][CONJ[A[c2][j]]]; t = ADD[t][(sg >> c2 & 1) ? NEG[v] : v]; }
        D[i * dt + j] = t; }
      RTG[rank9(dt, dt, D)] = 1; } }
  int hmax = dt < mt - dt ? dt : mt - dt; for (int r = dt - hmax; r <= dt; r++) RTA[r] = 1;
}
static int s_of(const int *eps, const int *S) {   /* s = rank(H|W), W = {x : S conj(x) = 0} */
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
  return rank9(dw, dw, Gw);
}
static int exact_with(const int *RT, int s_, int r1, int r0) {
  int b = K1 - 2 * r1 + r0, q = r1 - r0, u = dt - q, mu = 99;
  for (int rr = 0; rr <= dt; rr++) if (RT[rr]) {
    int lo = rr - 2 * q; if (lo < 0) lo = 0; int hi = rr < u ? rr : u;
    for (int rho = lo; rho <= hi; rho++) { int m = s_ > rho ? s_ - rho : rho - s_; if (m < mu) mu = m; } }
  return b - mu;
}
static int true_hull(const int *eps, const int *pts, const int *teps, const int *M) {
  int A[10][MAXK], G[MAXK * NN], N = n + mt, H[MAXK * MAXK];
  for (int c = 0; c < mt; c++) tailrow(pts[c], A[c]);
  for (int i = 0; i < K1; i++) {
    for (int t = 0; t < n; t++) G[i * N + t] = C[i * n + t];
    for (int c = 0; c < mt; c++) { int s = 0;
      if (i >= K2) for (int l = 0; l < dt; l++) s = ADD[s][MUL[M[(i - K2) * dt + l]][A[c][l]]];
      G[i * N + n + c] = s; } }
  for (int i = 0; i < K1; i++) for (int j = 0; j < K1; j++) { int s = 0;
    for (int t = 0; t < N; t++) { int v = MUL[G[i * N + t]][CONJ[G[j * N + t]]];
      int e = t < n ? eps[t] : teps[t - n]; s = ADD[s][e > 0 ? v : NEG[v]]; }
    H[i * K1 + j] = s; }
  return K1 - rank9(K1, K1, H);
}
static void rand_tail(int *pts, int *teps, int *M) {
  int p[10] = {0,1,2,3,4,5,6,7,8,9};
  for (int i = 9; i > 0; i--) { int j = rand() % (i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; }
  for (int c = 0; c < mt; c++) { pts[c] = p[c]; teps[c] = rand() % 2 ? 1 : -1; }
  int T[MAXK * MAXK]; do { for (int e = 0; e < dt * dt; e++) M[e] = rand() % 9; memcpy(T, M, sizeof(int) * dt * dt); } while (rank9(dt, dt, T) < dt);
}
static void pe(const int *eps) { for (int t = 0; t < n; t++) putchar(eps[t] > 0 ? '+' : '-'); }
int main(int argc, char **argv) {
  gf_init();
  if (argc < 3 || scanf("%d %d %d", &K1, &K2, &n) != 3 || K1 > MAXK || n > NN) { fprintf(stderr, "usage: see header\n"); return 2; }
  for (int i = 0; i < K1 * n; i++) if (scanf("%d", &C[i]) != 1) return 2;
  dt = K1 - K2; mt = atoi(argv[2]); if (mt < dt || mt > 10) return 2;
  tail_ranks();
  int eps[NN], S[MAXK * MAXK], r1, r0;
  printf("K1 %d K2 %d n %d tail [%d,%d]; GRS tail ranks:", K1, K2, n, mt, dt);
  for (int r = 0; r <= dt; r++) if (RTG[r]) printf(" %d", r);
  printf("; any-tail ranks:"); for (int r = 0; r <= dt; r++) if (RTA[r]) printf(" %d", r); printf("\n");
  if (!strcmp(argv[1], "bound") && argc > 3) {
    int THR = atoi(argv[3]);
    for (int t = 0; t < n; t++) eps[t] = 1;
    sumPQ(eps, S);
    static int O[NN][MAXK * MAXK];
    for (int t = 0; t < n; t++) for (int i = 0; i < K2; i++) for (int j = 0; j < K1; j++)
      O[t][i * K1 + j] = MUL[C[i * n + t]][CONJ[C[j * n + t]]];
    long h0[MAXK + 1] = {0}, hb[MAXK + 1] = {0}, hxg[MAXK + 2] = {0}, hxa[MAXK + 2] = {0};
    int bestb = -99, bestg = -99, besta = -99, shown = 0;
    unsigned long total = 1UL << (n - 1), examined = 0;
    for (unsigned long g = 0; g < total; g++) {
      if (g) { int t = 1 + __builtin_ctzl(g);
        for (int x = 0; x < K2 * K1; x++) S[x] = ADD[S[x]][eps[t] > 0 ? O[t][x] : NEG[O[t][x]]];
        eps[t] = -eps[t]; }
      r0 = rank_P(S); h0[r0]++;
      if (K1 - r0 < THR) continue;
      examined++; r1 = rank_PQ(S); int b = K1 - 2 * r1 + r0; hb[b < 0 ? 0 : b]++; if (b > bestb) bestb = b;
      if (b < THR) continue;
      int s_ = s_of(eps, S), xg = exact_with(RTG, s_, r1, r0), xa = exact_with(RTA, s_, r1, r0);
      hxg[xg < 0 ? 0 : xg]++; hxa[xa < 0 ? 0 : xa]++;
      if (xg > bestg) bestg = xg; if (xa > besta) { besta = xa; shown = 0; }
      if (xa == besta && shown < 10) { shown++; printf("exact_any %d exact_grs %d bound %d rho1 %d rho0 %d s %d eps ", xa, xg, b, r1, r0, s_); pe(eps); putchar('\n'); fflush(stdout); }
    }
    printf("patterns %lu; rho0 histogram:", total); for (int r = 0; r <= K2; r++) if (h0[r]) printf(" %d:%ld", r, h0[r]);
    printf("\npatterns with K1 - rho0 >= %d: %lu; their bound histogram:", THR, examined);
    for (int r = 0; r <= MAXK; r++) if (hb[r]) printf(" %d:%ld", r, hb[r]);
    printf("\nmax bound among them: %d\n", examined ? bestb : -1);
    printf("exact max hull (GRS tails) histogram over patterns with bound >= %d:", THR); for (int r = 0; r <= MAXK; r++) if (hxg[r]) printf(" %d:%ld", r, hxg[r]);
    printf("\nexact max hull (any tail) histogram over patterns with bound >= %d:", THR); for (int r = 0; r <= MAXK; r++) if (hxa[r]) printf(" %d:%ld", r, hxa[r]);
    printf("\nRESULT max hull over all X codes of this pair: GRS tails %s%d, any tail %s%d\n",
           bestg >= THR ? "" : "<= ", bestg >= THR ? bestg : THR - 1, besta >= THR ? "" : "<= ", besta >= THR ? besta : THR - 1);
    return 0;
  }
  if (!strcmp(argv[1], "test") && argc > 4) {
    srand(atoi(argv[3])); long tries = atol(argv[4]), vb = 0, vg = 0, va = 0, tight = 0; int pts[10], teps[10], M[MAXK * MAXK], mx = -1;
    for (long r = 0; r < tries; r++) {
      eps[0] = 1; for (int t = 1; t < n; t++) eps[t] = rand() % 2 ? 1 : -1;
      rand_tail(pts, teps, M); sumPQ(eps, S); r0 = rank_P(S); r1 = rank_PQ(S); int b = K1 - 2 * r1 + r0;
      int h = true_hull(eps, pts, teps, M), s_ = s_of(eps, S), xg = exact_with(RTG, s_, r1, r0), xa = exact_with(RTA, s_, r1, r0);
      if (h > b) vb++; if (h > xg) vg++; if (xg > xa) va++; if (h == xg) tight++; if (h > mx) mx = h; }
    printf("test: %ld random X codes (GRS tails); true hull > bound: %ld; true hull > exact_grs: %ld; exact_grs > exact_any: %ld; true hull = exact_grs: %ld; max true hull %d\n",
           tries, vb, vg, va, tight, mx);
    return (vb || vg || va) ? 1 : 0;
  }
  if (!strcmp(argv[1], "real") && argc > 5) {
    for (int t = 0; t < n; t++) eps[t] = argv[3][t] == '-' ? -1 : 1;
    srand(atoi(argv[4])); long tries = atol(argv[5]); int pts[10], teps[10], M[MAXK * MAXK], best = -1;
    sumPQ(eps, S); r0 = rank_P(S); r1 = rank_PQ(S); int b = K1 - 2 * r1 + r0, s_ = s_of(eps, S), xg = exact_with(RTG, s_, r1, r0);
    printf("head: rho1 %d rho0 %d s %d bound %d exact_grs %d\n", r1, r0, s_, b, xg);
    for (long r = 0; r < tries; r++) { rand_tail(pts, teps, M); int h = true_hull(eps, pts, teps, M);
      if (h > best) { best = h; printf("try %ld: true hull %d pts", r, h);
        for (int c = 0; c < mt; c++) printf(" %d", pts[c]); printf(" teps "); for (int c = 0; c < mt; c++) putchar(teps[c] > 0 ? '+' : '-');
        printf(" M"); for (int e = 0; e < dt * dt; e++) printf(" %d", M[e]); printf("\n"); fflush(stdout); }
      if (best == xg) break; }
    printf("real: bound %d, exact_grs %d, best true hull %d\n", b, xg, best);
    return 0;
  }
  fprintf(stderr, "usage: see header\n"); return 2;
}
