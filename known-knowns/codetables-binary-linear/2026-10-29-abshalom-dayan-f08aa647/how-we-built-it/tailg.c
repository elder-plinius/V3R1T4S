/* tailg: generalisation of constructor/code/tailc.c. Exhaustive search for L tail columns (a multiset of points of
   PG(r-1,9), r = 2..4) such that every hyperplane c^perp contains at most cap(c) = L - max(0, D - mu(c)) of them,
   where mu(c) is the minimum affine weight of the coset c of the zero-tail subcode (capped at D).  Then every
   codeword outside the zero-tail subcode has weight >= D.  Input blocks on stdin: "V <id> r L D" then NP = (9^r-1)/8
   integers mu in proj order (r-tuples over 0..8, first nonzero 1, lexicographic).  Node cap per block: MAXNODES.
   Output: "<id> nodes=<n> sols=<s> [first solution]" or "... CAPPED". GF(9) pair arithmetic, a + 3b, w^2 = w + 1. */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#define MAXNP 820
#define WD 13
#define ML 10
static int ADD[9][9], MUL[9][9], P[MAXNP][4], NP, R, L, D, cap[MAXNP];
static uint64_t inc[MAXNP][WD], forbid[ML + 2][WD];
static long long nodes, MAXNODES = 200000000LL; static int nsol, capped, chosen[ML], first[ML];
static void rec(int depth, int start, uint64_t lv[][WD]) {
    if (++nodes > MAXNODES) { capped = 1; return; }
    if (depth == L) { if (!nsol) memcpy(first, chosen, sizeof chosen); nsol++; return; }
    for (int i = start; i < NP && nsol == 0 && !capped; i++) {
        uint64_t nl[ML + 2][WD]; int ok = 1;
        for (int w = 0; w < WD; w++) { nl[1][w] = lv[1][w] | inc[i][w]; if (nl[1][w] & forbid[1][w]) ok = 0; }
        for (int t = 2; ok && t <= depth + 1; t++)
            for (int w = 0; w < WD; w++) { nl[t][w] = lv[t][w] | (lv[t - 1][w] & inc[i][w]); if (nl[t][w] & forbid[t][w]) { ok = 0; break; } }
        if (!ok) continue;
        for (int t = depth + 2; t <= L; t++) for (int w = 0; w < WD; w++) nl[t][w] = lv[t][w];
        chosen[depth] = i;
        rec(depth + 1, i, nl);
    }
}
int main(void) {
    for (int x = 0; x < 9; x++) for (int y = 0; y < 9; y++) {
        int a = x % 3, b = x / 3, c = y % 3, d = y / 3;
        ADD[x][y] = (a + c) % 3 + 3 * ((b + d) % 3);
        MUL[x][y] = (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3);
    }
    char tag[64], id[96];
    while (scanf("%63s %95s %d %d %d", tag, id, &R, &L, &D) == 5) {
        if (R < 2 || R > 4 || L < 1 || L > ML) return 2;
        NP = 0; int tot = 1; for (int j = 0; j < R; j++) tot *= 9;
        for (int v = 0; v < tot; v++) {
            int t[4] = {0}, x = v, f = -1;
            for (int j = R - 1; j >= 0; j--) { t[j] = x % 9; x /= 9; }
            for (int j = 0; j < R; j++) if (t[j]) { f = t[j]; break; }
            if (f != 1) continue;
            memcpy(P[NP++], t, sizeof t);
        }
        memset(inc, 0, sizeof inc);
        for (int p = 0; p < NP; p++) for (int c = 0; c < NP; c++) {
            int s = 0; for (int j = 0; j < R; j++) s = ADD[s][MUL[P[c][j]][P[p][j]]];
            if (!s) inc[p][c / 64] |= 1ULL << (c % 64);
        }
        int bad = 0;
        for (int c = 0; c < NP; c++) { int mu; if (scanf("%d", &mu) != 1) return 2; int need = D - mu; if (need < 0) need = 0; cap[c] = L - need; if (cap[c] < 0) bad = 1; }
        if (bad) { printf("%s impossible\n", id); fflush(stdout); continue; }
        memset(forbid, 0, sizeof forbid);
        for (int t = 0; t <= L + 1; t++) for (int c = 0; c < NP; c++) if (cap[c] < t) forbid[t][c / 64] |= 1ULL << (c % 64);
        uint64_t lv[ML + 2][WD]; memset(lv, 0, sizeof lv);
        nodes = 0; nsol = 0; capped = 0;
        rec(0, 0, lv);
        printf("%s nodes=%lld sols=%d%s", id, nodes, nsol, capped && !nsol ? " CAPPED" : "");
        if (nsol) for (int j = 0; j < L; j++) printf(" %d", first[j]);
        printf("\n"); fflush(stdout);
    }
    return 0;
}
