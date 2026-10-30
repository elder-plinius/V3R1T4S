/* For each code (format "K n" + rows): exact d (Brouwer-Zimmermann), Hermitian hull, and (if n <= 24) the
   maximum hull over column-norm sign patterns with its histogram. Usage: analyze [noeps] < codes */
#include "gf9.h"
static int maxhull_eps(int K, int n, const int *G, long long *hist, char *bestpat) {
  static int A[MAXN][MAXK * MAXK]; int M[MAXK * MAXK] = {0}; int eps[MAXN];
  for (int t = 0; t < n; t++) { eps[t] = 1; for (int i = 0; i < K; i++) for (int j = 0; j < K; j++)
    A[t][i * K + j] = MUL[G[i * n + t]][CONJ[G[j * n + t]]]; }
  for (int t = 0; t < n; t++) for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][A[t][e]];
  int best = -1; long long N = 1LL << (n - 1);
  for (long long g = 0; g < N; g++) {
    if (g) { int t = 1 + __builtin_ctzll(g);
      if (eps[t] == 1) { for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][A[t][e]]; eps[t] = -1; }
      else { for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][NEG[A[t][e]]]; eps[t] = 1; } }
    int T[MAXK * MAXK]; memcpy(T, M, sizeof(int) * K * K);
    int h = K - rank9(K, K, T); hist[h]++;
    if (h > best) { best = h; for (int t = 0; t < n; t++) bestpat[t] = eps[t] > 0 ? '+' : '-'; bestpat[n] = 0; }
  }
  return best;
}
int main(int argc, char **argv) {
  gf_init(); int noeps = argc > 1;
  int K, n, idx = 0;
  while (scanf("%d %d", &K, &n) == 2) {
    int G[MAXK * MAXN]; for (int i = 0; i < K * n; i++) if (scanf("%d", &G[i]) != 1) return 2;
    int T[MAXK * MAXN]; memcpy(T, G, sizeof(int) * K * n); int rk = rank9(K, n, T);
    int d = dist_exact(K, n, G), h = hull_dim(K, n, G);
    printf("code %d K=%d n=%d rank=%d d=%d hull=%d", idx, K, n, rk, d, h);
    if (!noeps && n <= 24) { long long hist[MAXK + 1] = {0}; char pat[MAXN + 1];
      int mh = maxhull_eps(K, n, G, hist, pat); printf(" maxhull_eps=%d eps=%s hist=", mh, pat);
      for (int i = 0; i <= K; i++) printf("%lld%c", hist[i], i < K ? ',' : ' '); }
    printf("\n"); fflush(stdout); idx++;
  }
  return 0;
}
