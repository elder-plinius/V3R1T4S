/* GF(9) = GF(3)[w]/(w^2 - w - 1), element a + b*w encoded as a + 3b. w (=3) is primitive (order 8). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int ADD[9][9], MUL[9][9], NEG[9], CONJ[9], INV[9], NORM[9];
static void gf_init(void) {
  for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) {
    int a = x % 3, b = x / 3, c = y % 3, d = y / 3;
    ADD[x][y] = (a + c) % 3 + 3 * ((b + d) % 3);
    MUL[x][y] = (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3);
  }
  for (int x = 0; x < 9; x++) {
    for (int y = 0; y < 9; y++) { if (ADD[x][y] == 0) NEG[x] = y; if (MUL[x][y] == 1) INV[x] = y; }
    CONJ[x] = MUL[MUL[x][x]][x]; NORM[x] = MUL[x][CONJ[x]];
  }
}
static int gpow(int x, int e) { int r = 1; e = ((e % 8) + 8) % 8; while (e--) r = MUL[r][x]; return r; }
static int rank9(int rows, int cols, int *M) {
  int r = 0;
  for (int c = 0; c < cols && r < rows; c++) {
    int p = -1; for (int i = r; i < rows; i++) if (M[i * cols + c]) { p = i; break; }
    if (p < 0) continue;
    for (int j = 0; j < cols; j++) { int t = M[r * cols + j]; M[r * cols + j] = M[p * cols + j]; M[p * cols + j] = t; }
    int iv = INV[M[r * cols + c]];
    for (int j = 0; j < cols; j++) M[r * cols + j] = MUL[M[r * cols + j]][iv];
    for (int i = 0; i < rows; i++) if (i != r && M[i * cols + c]) {
      int f = NEG[M[i * cols + c]];
      for (int j = 0; j < cols; j++) M[i * cols + j] = ADD[M[i * cols + j]][MUL[f][M[r * cols + j]]];
    }
    r++;
  }
  return r;
}
static int hull_dim(int K, int n, const int *G) {
  int H[64 * 64];
  for (int i = 0; i < K; i++) for (int j = 0; j < K; j++) { int s = 0;
    for (int t = 0; t < n; t++) s = ADD[s][MUL[G[i * n + t]][CONJ[G[j * n + t]]]]; H[i * K + j] = s; }
  return K - rank9(K, K, H);
}
/* ---- minimum distance: Brouwer-Zimmermann with disjoint information sets ----
   Returns exact d if d >= target is undecided... semantics: if mode_exact, returns exact d.
   Otherwise returns a value < target as soon as a codeword of weight < target is found, or >= target when the
   lower bound reaches target (value returned is then max(lower bound, target)). */
#define MAXN 40
#define MAXK 20
typedef struct { int K, n, r; int perm[8][MAXN]; int A[8][MAXK][MAXN]; } ISets;
static int build_isets(int K, int n, const int *G, ISets *S) {
  int used[MAXN] = {0}; S->K = K; S->n = n; S->r = 0;
  for (int round = 0; round < 8; round++) {
    int M[MAXK * MAXN]; memcpy(M, G, sizeof(int) * K * n);
    int piv[MAXK]; int r = 0;
    /* pivot preferring unused columns */
    for (int pass = 0; pass < 2 && r < K; pass++)
    for (int c = 0; c < n && r < K; c++) {
      if (pass == 0 && used[c]) continue;
      if (pass == 1) break;
      int p = -1; for (int i = r; i < K; i++) if (M[i * n + c]) { p = i; break; }
      if (p < 0) continue;
      for (int j = 0; j < n; j++) { int t = M[r * n + j]; M[r * n + j] = M[p * n + j]; M[p * n + j] = t; }
      int iv = INV[M[r * n + c]];
      for (int j = 0; j < n; j++) M[r * n + j] = MUL[M[r * n + j]][iv];
      for (int i = 0; i < K; i++) if (i != r && M[i * n + c]) { int f = NEG[M[i * n + c]];
        for (int j = 0; j < n; j++) M[i * n + j] = ADD[M[i * n + j]][MUL[f][M[r * n + j]]]; }
      piv[r++] = c;
    }
    if (r < K) break; /* unused columns do not contain an information set */
    int isp[MAXN] = {0}; for (int i = 0; i < K; i++) { isp[piv[i]] = 1; used[piv[i]] = 1; }
    int idx = 0; for (int i = 0; i < K; i++) S->perm[S->r][idx++] = piv[i];
    for (int c = 0; c < n; c++) if (!isp[c]) S->perm[S->r][idx++] = c;
    for (int i = 0; i < K; i++) for (int c = 0; c < n; c++) S->A[S->r][i][c] = M[i * n + S->perm[S->r][c]];
    S->r++;
  }
  return S->r;
}
/* enumerate projective messages of weight exactly w in info set s; return min codeword weight (or big) */
static int min_weight_w(const ISets *S, int s, int w, int stop_below) {
  int K = S->K, n = S->n, best = 1 << 20;
  int comb[MAXK]; for (int i = 0; i < w; i++) comb[i] = i;
  int cw[MAXN];
  while (1) {
    /* coefficients: first = 1, others over 8 nonzero values */
    int coef[MAXK]; for (int i = 0; i < w; i++) coef[i] = 1;
    long long tot = 1; for (int i = 1; i < w; i++) tot *= 8;
    for (long long it = 0; it < tot; it++) {
      long long x = it; for (int i = 1; i < w; i++) { coef[i] = gpow(3, (int)(x % 8)); x /= 8; }
      int wt = w;
      for (int c = K; c < n; c++) { int v = 0; for (int i = 0; i < w; i++) v = ADD[v][MUL[coef[i]][S->A[s][comb[i]][c]]];
        if (v) wt++; }
      if (wt < best) { best = wt; if (best < stop_below) return best; }
    }
    int i = w - 1; while (i >= 0 && comb[i] == K - w + i) i--;
    if (i < 0) break;
    comb[i]++; for (int j = i + 1; j < w; j++) comb[j] = comb[j - 1] + 1;
  }
  (void)cw; return best;
}
/* returns: if found weight < target -> that weight (<target). Else returns >= target meaning d >= target. */
static int dist_at_least(int K, int n, const int *G, int target) {
  ISets S; build_isets(K, n, G, &S);
  if (S.r == 0) return 0;
  int best = 1 << 20;
  for (int w = 1; w <= K; w++) {
    for (int s = 0; s < S.r; s++) {
      int m = min_weight_w(&S, s, w, target);
      if (m < best) best = m;
      if (best < target) return best;
    }
    int lb = S.r * (w + 1);
    if (lb >= target || lb >= best) return best < target ? best : (best < lb ? best : lb) ;
  }
  return best;
}
/* exact minimum distance by BZ */
static int dist_exact(int K, int n, const int *G) {
  ISets S; build_isets(K, n, G, &S);
  int best = 1 << 20;
  for (int w = 1; w <= K; w++) {
    for (int s = 0; s < S.r; s++) { int m = min_weight_w(&S, s, w, 0); if (m < best) best = m; }
    if (S.r * (w + 1) >= best) return best;
  }
  return best;
}
