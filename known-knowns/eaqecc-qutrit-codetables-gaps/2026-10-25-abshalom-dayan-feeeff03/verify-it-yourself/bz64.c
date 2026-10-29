/* bz64 (bz9 with 64-bit masks, n <= 64; made by sed from bz9.c (not shipped), otherwise identical). bz9: exact minimum Hamming distance of a linear code over GF(9) by the Brouwer-Zimmermann method with
   Zimmermann's bound for partial information sets. Written independently of analyze.c (not shipped).
   GF(9) = GF(3)[w]/(w^2 - w - 1), element a + b*w stored as a + 3b. A vector of length n <= 64 is stored bit-sliced:
   masks a1, a2 (positions where a = 1, a = 2) and b1, b2 (same for b). Hamming weight = popcount(a1|a2|b1|b2).
   Input (stdin): "K n" then K rows of n integers 0..8 (a generator matrix of full rank K).
   Output: one line "K=.. n=.. d=.. sets=r1,r2,.. maxw=.. words=.. witness=c_0 c_1 ... c_{n-1}"
   Correctness argument: for information set j (pivot columns P_j, of which r_j are not pivots of earlier sets),
   the systematic generator R_j gives every codeword as m R_j with m = codeword restricted to P_j. Enumerating all m
   of Hamming weight <= w (first nonzero = 1, weights are scale invariant) finds every codeword whose restriction to
   P_j has weight <= w. Any codeword not found has > w nonzeros on each P_j, hence >= w + 1 - (K - r_j) on the r_j
   fresh columns of P_j, and the fresh column sets are disjoint. So its weight is >= sum_j max(0, w + 1 - (K - r_j)).
   Stop when that bound reaches the best weight found. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef struct { uint64_t a1, a2, b1, b2; } V;
static int ADD9[9][9], MUL9[9][9], INV9[9], NEG9[9];
static void gf(void) {
  for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) {
    int a = x % 3, b = x / 3, c = y % 3, d = y / 3;
    ADD9[x][y] = (a + c) % 3 + 3 * ((b + d) % 3);
    MUL9[x][y] = (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3);   /* w^2 = w + 1 */
  }
  for (int x = 1; x < 9; x++) for (int y = 1; y < 9; y++) if (MUL9[x][y] == 1) INV9[x] = y;
  for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) if (ADD9[x][y] == 0) NEG9[x] = y;
}
static inline void add3(uint64_t p1, uint64_t p2, uint64_t q1, uint64_t q2, uint64_t *r1, uint64_t *r2) {
  /* GF(3) add, one-hot masks: value 1 at p1, value 2 at p2 */
  uint64_t p0 = ~(p1 | p2), q0 = ~(q1 | q2);
  *r1 = (p0 & q1) | (p1 & q0) | (p2 & q2);
  *r2 = (p0 & q2) | (p2 & q0) | (p1 & q1);
}
static inline V vadd(V x, V y) { V r; add3(x.a1, x.a2, y.a1, y.a2, &r.a1, &r.a2); add3(x.b1, x.b2, y.b1, y.b2, &r.b1, &r.b2); return r; }
static inline int vwt(V x) { return __builtin_popcountll(x.a1 | x.a2 | x.b1 | x.b2); }
static V pack(const int *v, int n) {
  V r = {0, 0, 0, 0};
  for (int t = 0; t < n; t++) { int a = v[t] % 3, b = v[t] / 3; uint64_t m = 1ULL << t;
    if (a == 1) r.a1 |= m; if (a == 2) r.a2 |= m; if (b == 1) r.b1 |= m; if (b == 2) r.b2 |= m; }
  return r;
}
static void unpack(V x, int n, int *v) {
  for (int t = 0; t < n; t++) { uint64_t m = 1ULL << t;
    int a = (x.a1 & m) ? 1 : (x.a2 & m) ? 2 : 0, b = (x.b1 & m) ? 1 : (x.b2 & m) ? 2 : 0; v[t] = a + 3 * b; }
}
#define MK 32
#define MS 16
static int K, n, nsets, r_fresh[MS];
static V MULT[MS][MK][9];          /* MULT[j][i][l] = l * (row i of systematic generator of set j) */
static int best = 1 << 20; static V bestv; static long long words = 0;
static void rec(int j, int start, int left, V acc) {
  if (left == 0) { words++; int w = vwt(acc); if (w < best) { best = w; bestv = acc; } return; }
  for (int i = start; i <= K - left; i++)
    for (int l = 1; l < 9; l++) rec(j, i + 1, left - 1, vadd(acc, MULT[j][i][l]));
}
static void rec_first(int j, int w) {      /* first chosen row gets coefficient 1 */
  for (int i = 0; i <= K - w; i++) { V z = {0, 0, 0, 0}; rec(j, i + 1, w - 1, vadd(z, MULT[j][i][1])); }
}
int main(void) {
  gf();
  if (scanf("%d %d", &K, &n) != 2 || K < 1 || K > MK || n > 64 || n < K) { printf("bad input\n"); return 2; }
  static int G[MK][64];
  for (int i = 0; i < K; i++) for (int t = 0; t < n; t++) if (scanf("%d", &G[i][t]) != 1 || G[i][t] < 0 || G[i][t] > 8) { printf("bad input\n"); return 2; }
  int used[64] = {0};
  nsets = 0;
  while (nsets < MS) {
    int M[MK][64]; memcpy(M, G, sizeof(M));
    int piv[MK], np = 0, fresh = 0;
    /* pivot on unused columns first (left to right), then on used columns */
    for (int pass = 0; pass < 2 && np < K; pass++)
      for (int t = 0; t < n && np < K; t++) {
        if ((pass == 0) == (used[t] != 0)) continue;
        int p = -1; for (int i = np; i < K; i++) if (M[i][t]) { p = i; break; }
        if (p < 0) continue;
        for (int u = 0; u < n; u++) { int tmp = M[np][u]; M[np][u] = M[p][u]; M[p][u] = tmp; }
        int iv = INV9[M[np][t]]; for (int u = 0; u < n; u++) M[np][u] = MUL9[M[np][u]][iv];
        for (int i = 0; i < K; i++) if (i != np && M[i][t]) { int f = M[i][t];
          for (int u = 0; u < n; u++) M[i][u] = ADD9[M[i][u]][NEG9[MUL9[f][M[np][u]]]]; }
        piv[np++] = t; if (pass == 0) fresh++;
      }
    if (np < K) { printf("generator matrix is not of full rank\n"); return 2; }
    if (fresh == 0) break;
    for (int i = 0; i < K; i++) used[piv[i]] = 1;
    r_fresh[nsets] = fresh;
    for (int i = 0; i < K; i++) for (int l = 0; l < 9; l++) { int v[64];
      for (int u = 0; u < n; u++) v[u] = MUL9[l][M[i][u]]; MULT[nsets][i][l] = pack(v, n); }
    /* sanity: systematic on its pivots */
    for (int i = 0; i < K; i++) for (int i2 = 0; i2 < K; i2++) if (M[i][piv[i2]] != (i == i2)) { printf("elimination error\n"); return 3; }
    nsets++;
  }
  int w;
  for (w = 1; w <= K; w++) {
    for (int j = 0; j < nsets; j++) rec_first(j, w);
    int lb = 0; for (int j = 0; j < nsets; j++) { int c = w + 1 - (K - r_fresh[j]); if (c > 0) lb += c; }
    if (lb >= best) break;
  }
  int cw[64]; unpack(bestv, n, cw);
  printf("K=%d n=%d d=%d sets=", K, n, best);
  for (int j = 0; j < nsets; j++) printf("%d%s", r_fresh[j], j + 1 < nsets ? "," : "");
  printf(" maxw=%d words=%lld witness=", w > K ? K : w, words);
  for (int t = 0; t < n; t++) printf("%d%s", cw[t], t + 1 < n ? " " : "\n");
  return 0;
}
