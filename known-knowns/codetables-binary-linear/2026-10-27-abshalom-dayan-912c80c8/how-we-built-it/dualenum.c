/* dualenum: weight distribution of the dual code C^perp of a linear code over GF(9) by enumerating ALL its 9^m
   codewords (m = n - k), then (in macwilliams.py) the weight distribution of C by the MacWilliams identities.
   Written for the run's self-break, independently of m3_mindist, hdep and bz9t (not shipped).
   GF(9) = GF(3)[w]/(w^2 - w - 1), a + b*w encoded a + 3b. As an additive group GF(9)^m = GF(3)^(2m) with basis
   {h_i, w*h_i} (h_i the rows of a parity-check matrix H); a ternary modular Gray code over 2m digits visits every
   element once, each step adding one basis vector. Vectors are bit-sliced: for the a-part and the b-part, masks of the
   positions equal to 1 and to 2. Input: "k n" then G (k rows). H is computed here from G by Gaussian elimination
   (systematic form on the pivot columns, H = [-A^T | I]), with a check G H^T = 0. Output: "B_w <w> <count>" lines. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
typedef struct { uint64_t a1, a2, b1, b2; } V;
static int ADD[9][9], MUL[9][9], NEG[9], INV[9];
static inline void add3(uint64_t x1, uint64_t x2, uint64_t y1, uint64_t y2, uint64_t *s1, uint64_t *s2) {
    uint64_t zx = ~(x1 | x2), zy = ~(y1 | y2);
    *s1 = (x1 & zy) | (y1 & zx) | (x2 & y2);
    *s2 = (x2 & zy) | (y2 & zx) | (x1 & y1);
}
static V vadd(V x, V y) { V r; add3(x.a1, x.a2, y.a1, y.a2, &r.a1, &r.a2); add3(x.b1, x.b2, y.b1, y.b2, &r.b1, &r.b2); return r; }
static V pack(const int *v, int n) {
    V r = {0, 0, 0, 0};
    for (int j = 0; j < n; j++) { int a = v[j] % 3, b = v[j] / 3; if (a == 1) r.a1 |= 1ULL << j; if (a == 2) r.a2 |= 1ULL << j; if (b == 1) r.b1 |= 1ULL << j; if (b == 2) r.b2 |= 1ULL << j; }
    return r;
}
int main(void) {
    for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) {
        int a = x % 3, b = x / 3, c = y % 3, d = y / 3;
        ADD[x][y] = (a + c) % 3 + 3 * ((b + d) % 3);
        MUL[x][y] = (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3);
    }
    for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) { if (ADD[x][y] == 0) NEG[x] = y; if (MUL[x][y] == 1) INV[x] = y; }
    int k, n, G[40][64];
    if (scanf("%d %d", &k, &n) != 2 || n > 64 || k > 40) return 2;
    for (int i = 0; i < k; i++) for (int j = 0; j < n; j++) if (scanf("%d", &G[i][j]) != 1) return 2;
    int piv[64], isp[64] = {0}, r = 0;
    for (int c = 0; c < n && r < k; c++) {
        int p = -1; for (int i = r; i < k; i++) if (G[i][c]) { p = i; break; }
        if (p < 0) continue;
        for (int j = 0; j < n; j++) { int t = G[p][j]; G[p][j] = G[r][j]; G[r][j] = t; }
        int iv = INV[G[r][c]]; for (int j = 0; j < n; j++) G[r][j] = MUL[G[r][j]][iv];
        for (int i = 0; i < k; i++) if (i != r && G[i][c]) { int f = NEG[G[i][c]]; for (int j = 0; j < n; j++) G[i][j] = ADD[G[i][j]][MUL[f][G[r][j]]]; }
        piv[r] = c; isp[c] = 1; r++;
    }
    if (r < k) { printf("RANK_DEFICIENT rank=%d\n", r); return 1; }
    int m = n - k, H[40][64], np[64], q = 0;
    for (int c = 0; c < n; c++) if (!isp[c]) np[q++] = c;
    for (int t = 0; t < m; t++) { for (int c = 0; c < n; c++) H[t][c] = 0; H[t][np[t]] = 1; for (int i = 0; i < k; i++) H[t][piv[i]] = NEG[G[i][np[t]]]; }
    for (int i = 0; i < k; i++) for (int t = 0; t < m; t++) { int s = 0; for (int c = 0; c < n; c++) s = ADD[s][MUL[G[i][c]][H[t][c]]]; if (s) { printf("INTERNAL_ERROR\n"); return 3; } }
    V basis[80]; int wv[64];
    for (int t = 0; t < m; t++) {
        basis[2 * t] = pack(H[t], n);
        for (int c = 0; c < n; c++) wv[c] = MUL[3][H[t][c]];    /* 3 encodes w */
        basis[2 * t + 1] = pack(wv, n);
    }
    int D = 2 * m; unsigned long long total = 1; for (int i = 0; i < D; i++) total *= 3;
    unsigned long long cnt[65] = {0};
    V v = {0, 0, 0, 0};
    cnt[0]++;
    for (unsigned long long t = 1; t < total; t++) {
        unsigned long long u = t; int j = 0; while (u % 3 == 0) { u /= 3; j++; }
        v = vadd(v, basis[j]);
        cnt[__builtin_popcountll(v.a1 | v.a2 | v.b1 | v.b2)]++;
    }
    printf("k=%d n=%d m=%d dual_words=%llu\n", k, n, m, total);
    for (int w = 0; w <= n; w++) if (cnt[w]) printf("B_w %d %llu\n", w, cnt[w]);
    return 0;
}
