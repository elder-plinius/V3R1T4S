/* hdep: exact minimum distance of a linear code over GF(9) from the dual side, written this run independently of
   m3_mindist.  d = the smallest number of columns of a parity-check matrix H that are linearly dependent.
   H is derived from the generator G (k x n) by bringing G to systematic form [I | A] on its pivot columns and taking
   H = [-A^T | I] on the same column order.  Then a depth-first search over column subsets in increasing index order
   keeps an echelon basis of the chosen columns; a column that reduces to zero closes a dependent set of size s and
   so certifies a nonzero codeword of weight <= s.  Subsets are only extended while independent, so the search visits
   every independent subset of size < Wmax exactly once: exhaustive up to Wmax.
   GF(9) = GF(3)[w]/(w^2 - w - 1); a + b*w encoded a + 3b; arithmetic by discrete log tables with generator w
   (w is primitive: its order is 8).  Input on stdin: "k n" then k rows.  Usage: hdep Wmax
   Output: "dependent_min=<s>" (d = s) or "no dependent set of size <= Wmax" (d > Wmax). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MX 64
static int LOG[9], EXP[16];
static int add9(int x, int y) { return (x % 3 + y % 3) % 3 + 3 * ((x / 3 + y / 3) % 3); }
static int mul9(int x, int y) { if (!x || !y) return 0; return EXP[(LOG[x] + LOG[y]) % 8]; }
static int neg9(int x) { return ((3 - x % 3) % 3) + 3 * ((3 - x / 3) % 3); }
static int inv9(int x) { return EXP[(8 - LOG[x]) % 8]; }
static void tables(void) {
    /* powers of w by the rule w^2 = w + 1 on pairs (a,b) = a + b w */
    int a = 1, b = 0;
    for (int e = 0; e < 8; e++) {
        int x = a + 3 * b; EXP[e] = x; EXP[e + 8] = x; LOG[x] = e;
        int na = b % 3, nb = (a + b) % 3;   /* (a + b w) w = a w + b (w + 1) = b + (a + b) w */
        a = na; b = nb;
    }
}
static int k, n, m, G[MX][MX], H[MX][MX], Hc[MX][MX];  /* Hc[j] = column j of H, length m = n - k */
static int Wmax, best;
static long long nodes;
/* basis: B[s] vector (length m) with pivot P[s], normalized pivot = 1, fully reduced is not needed */
static int B[MX][MX], P[MX];
static void dfs(int start, int s) {
    for (int j = start; j < n; j++) {
        int v[MX];
        memcpy(v, Hc[j], sizeof(int) * m);
        for (int t = 0; t < s; t++)
            if (v[P[t]]) { int f = neg9(v[P[t]]); for (int i = 0; i < m; i++) v[i] = add9(v[i], mul9(f, B[t][i])); }
        int p = -1;
        for (int i = 0; i < m; i++) if (v[i]) { p = i; break; }
        nodes++;
        if (p < 0) { if (s + 1 < best) best = s + 1; continue; }
        if (s + 1 >= Wmax || s + 1 >= best - 1) continue;   /* a dependent set needs one more column */
        int iv = inv9(v[p]);
        for (int i = 0; i < m; i++) B[s][i] = mul9(v[i], iv);
        P[s] = p;
        dfs(j + 1, s + 1);
    }
}
int main(int argc, char **argv) {
    tables();
    Wmax = argc > 1 ? atoi(argv[1]) : 10;
    if (scanf("%d %d", &k, &n) != 2 || k > MX || n > MX) return 2;
    for (int i = 0; i < k; i++) for (int j = 0; j < n; j++) if (scanf("%d", &G[i][j]) != 1 || G[i][j] < 0 || G[i][j] > 8) return 2;
    /* systematic form */
    int piv[MX], isp[MX] = {0}, r = 0;
    for (int c = 0; c < n && r < k; c++) {
        int p = -1;
        for (int i = r; i < k; i++) if (G[i][c]) { p = i; break; }
        if (p < 0) continue;
        for (int j = 0; j < n; j++) { int t = G[p][j]; G[p][j] = G[r][j]; G[r][j] = t; }
        int iv = inv9(G[r][c]);
        for (int j = 0; j < n; j++) G[r][j] = mul9(G[r][j], iv);
        for (int i = 0; i < k; i++) if (i != r && G[i][c]) { int f = neg9(G[i][c]); for (int j = 0; j < n; j++) G[i][j] = add9(G[i][j], mul9(f, G[r][j])); }
        piv[r] = c; isp[c] = 1; r++;
    }
    printf("rank=%d (k=%d n=%d)\n", r, k, n);
    if (r < k) { printf("RANK_DEFICIENT\n"); return 1; }
    m = n - k;
    int nonp[MX], q = 0;
    for (int c = 0; c < n; c++) if (!isp[c]) nonp[q++] = c;
    /* H rows indexed by nonpivot t: H[t][nonp[t]] = 1, H[t][piv[i]] = -G[i][nonp[t]] */
    for (int t = 0; t < m; t++) {
        for (int c = 0; c < n; c++) H[t][c] = 0;
        H[t][nonp[t]] = 1;
        for (int i = 0; i < k; i++) H[t][piv[i]] = neg9(G[i][nonp[t]]);
    }
    /* self-test: G H^T = 0 */
    for (int i = 0; i < k; i++) for (int t = 0; t < m; t++) {
        int s = 0; for (int c = 0; c < n; c++) s = add9(s, mul9(G[i][c], H[t][c]));
        if (s) { printf("INTERNAL_ERROR GH^T != 0\n"); return 3; }
    }
    for (int j = 0; j < n; j++) for (int t = 0; t < m; t++) Hc[j][t] = H[t][j];
    best = Wmax + 1;
    dfs(0, 0);
    printf("nodes=%lld\n", nodes);
    if (best <= Wmax) printf("dependent_min=%d d=%d\n", best, best);
    else printf("no dependent set of size <= %d: d >= %d\n", Wmax, Wmax + 1);
    return 0;
}
