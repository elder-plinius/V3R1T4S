/* Exhaustive max Hermitian hull over sign patterns for one code with n up to 40, split in 2^cb chunks:
   eps_0 = +1, bits n-cb..n-1 fixed by chunk id. Usage: epsbig cb chunk < code. Prints max hull, eps, histogram. */
#include "gf9.h"
int main(int argc, char **argv) {
  gf_init(); int cb = atoi(argv[1]); long long chunk = atoll(argv[2]);
  int K, n; if (scanf("%d %d", &K, &n) != 2) return 2;
  int G[MAXK * MAXN]; for (int i = 0; i < K * n; i++) if (scanf("%d", &G[i]) != 1) return 2;
  static int A[MAXN][MAXK * MAXK]; int M[MAXK * MAXK] = {0}; int eps[MAXN];
  for (int t = 0; t < n; t++) for (int i = 0; i < K; i++) for (int j = 0; j < K; j++) A[t][i * K + j] = MUL[G[i * n + t]][CONJ[G[j * n + t]]];
  int free_bits = n - 1 - cb;
  for (int t = 0; t < n; t++) eps[t] = 1;
  for (int b = 0; b < cb; b++) if (chunk >> b & 1) eps[1 + free_bits + b] = -1;
  for (int t = 0; t < n; t++) for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][eps[t] > 0 ? A[t][e] : NEG[A[t][e]]];
  long long hist[MAXK + 1] = {0}; int best = -1; char pat[MAXN + 1];
  long long N = 1LL << free_bits;
  for (long long g = 0; g < N; g++) {
    if (g) { int t = 1 + __builtin_ctzll(g);
      if (eps[t] == 1) { for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][A[t][e]]; eps[t] = -1; }
      else { for (int e = 0; e < K * K; e++) M[e] = ADD[M[e]][NEG[A[t][e]]]; eps[t] = 1; } }
    int T[MAXK * MAXK]; memcpy(T, M, sizeof(int) * K * K);
    int h = K - rank9(K, K, T); hist[h]++;
    if (h > best) { best = h; for (int t = 0; t < n; t++) pat[t] = eps[t] > 0 ? '+' : '-'; pat[n] = 0; }
  }
  printf("K=%d n=%d chunk=%lld/%d maxhull=%d eps=%s hist=", K, n, chunk, 1 << cb, best, pat);
  for (int h = 0; h <= K; h++) printf("%lld%c", hist[h], h < K ? ',' : '\n');
  return 0;
}
