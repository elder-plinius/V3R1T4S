/* Exact information-set test over GF(9) (written from the definition).
   Input (stdin): "kappa n" then kappa rows of n entries in 0..8 (a + 3b for a + b w, w^2 = w + 1).
   For subset size m: enumerate every m-subset U of the n columns (depth-first, incremental echelon form) and count
   those with rank(G_U) < kappa. d(C) >= n - m + 1 holds iff that count is 0 (a nonzero codeword of weight <= n - m
   vanishes on some m-subset, and a rank-deficient m-subset gives such a codeword). Pruning is exact: once the rank
   is kappa every completion is full rank; once rank + (columns still to pick) < kappa every completion is deficient;
   both are counted by binomials, never skipped.
   Usage: infoset m part nparts [list L] ; the subsets are split by their first column index (mod nparts).
   Prints: m, total subsets visited in this part (counted), deficient count, and with "list L" up to L deficient
   m-subsets (positions 0-based) found by full descent. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, N, M;
static uint8_t G[32][64];          /* G[row][col] */
static uint8_t MUL[9][9], ADD[9][9], NEG[9], INV[9];
static uint8_t basis[33][32];      /* reduced vectors, length K */
static int bpiv[33];
static unsigned long long total = 0, deficient = 0;
static long listmax = 0, listed = 0;
static int chosen[64];
static double BIN[70][70];
static unsigned long long BINU[70][70];

static int f9(int a, int b) { a = ((a % 3) + 3) % 3; b = ((b % 3) + 3) % 3; return a + 3 * b; }

static void tables(void) {
  for (int u = 0; u < 9; u++) for (int v = 0; v < 9; v++) {
    int a = u % 3, b = u / 3, c = v % 3, d = v / 3;
    MUL[u][v] = f9(a * c + b * d, a * d + b * c + b * d);
    ADD[u][v] = f9(a + c, b + d);
  }
  for (int u = 0; u < 9; u++) { NEG[u] = f9(-(u % 3), -(u / 3)); INV[u] = 0;
    for (int v = 1; v < 9; v++) if (MUL[u][v] == 1) INV[u] = v; }
  for (int i = 0; i < 70; i++) { BINU[i][0] = 1; for (int j = 1; j <= i; j++) BINU[i][j] = BINU[i-1][j-1] + (j <= i-1 ? BINU[i-1][j] : 0); }
}

static unsigned long long binom(int a, int b) { if (b < 0 || a < 0 || b > a) return 0; return BINU[a][b]; }

/* reduce column j against basis[0..r-1]; if independent, store as basis[r] and return 1 */
static int addcol(int j, int r) {
  uint8_t v[32];
  for (int i = 0; i < K; i++) v[i] = G[i][j];
  for (int t = 0; t < r; t++) {
    int p = bpiv[t];
    if (v[p]) {
      uint8_t f = NEG[MUL[v[p]][INV[basis[t][p]]]];
      for (int i = 0; i < K; i++) if (basis[t][i]) v[i] = ADD[v[i]][MUL[f][basis[t][i]]];
    }
  }
  for (int i = 0; i < K; i++) if (v[i]) { memcpy(basis[r], v, K); bpiv[r] = i; return 1; }
  return 0;
}

/* depth = number chosen so far, next = smallest allowed column, r = current rank */
static void dfs(int depth, int next, int r) {
  int need = M - depth;
  if (need == 0) { total++; if (r < K) { deficient++;
      if (listed < listmax) { listed++; printf("deficient:"); for (int t = 0; t < M; t++) printf(" %d", chosen[t]); printf("\n"); } }
    return; }
  int avail = N - next;
  if (avail < need) return;
  unsigned long long cnt = binom(avail, need);
  if (r == K) { total += cnt; return; }                       /* every completion full rank */
  if (r + need < K && listed >= listmax) { total += cnt; deficient += cnt; return; }   /* every completion deficient */
  for (int j = next; j <= N - need; j++) {
    chosen[depth] = j;
    int nr = r + addcol(j, r);
    dfs(depth + 1, j + 1, nr);
  }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: infoset m part nparts [list L]\n"); return 1; }
  M = atoi(argv[1]); int part = atoi(argv[2]), np = atoi(argv[3]);
  if (argc >= 6 && !strcmp(argv[4], "list")) listmax = atol(argv[5]);
  tables();
  if (scanf("%d %d", &K, &N) != 2 || K > 32 || N > 64) { fprintf(stderr, "bad header\n"); return 1; }
  for (int i = 0; i < K; i++) for (int j = 0; j < N; j++) { int x; if (scanf("%d", &x) != 1 || x < 0 || x > 8) { fprintf(stderr, "bad entry\n"); return 1; } G[i][j] = x; }
  for (int j0 = 0; j0 <= N - M; j0++) {
    if (j0 % np != part) continue;
    chosen[0] = j0;
    int r = addcol(j0, 0);
    dfs(1, j0 + 1, r);
  }
  printf("kappa=%d n=%d m=%d part=%d/%d subsets=%llu deficient=%llu (expected subsets in all parts C(n,m)=%llu)\n",
         K, N, M, part, np, total, deficient, binom(N, M));
  return 0;
}
