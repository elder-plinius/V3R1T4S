// Orbit-method search for codes over mixed alphabets (coordinate i has alphabet size qs[i] <= 8), length n <= 16.
// usage: osg alph d elements_file target time_limit_s max_vertices out_file
// alph: comma list of SIZExCOUNT blocks in coordinate order, e.g. "3x15" or "2x5,3x9".
// elements_file: one group element per line: n ints (coordinate permutation pi), then for each coordinate i, Q ints
//   (Q = max alphabet size) giving the symbol map sigma_i used at coordinate i. Action: (g w)[pi[i]] = sigma_i[w[i]].
//   The list must be the whole group (closure is done by the caller); pi must preserve alphabet sizes.
// Vertices = orbits whose words are pairwise at distance >= d. Edge = two orbits mutually at distance >= d.
// Finds a maximum-weight clique (weight = orbit size) among cliques of weight >= target. Exhaustive unless the time
// limit hits. Output line: G=.. orbits=.. selfcompat=.. alive=.. nodes=.. COMPLETE|TIMEOUT best=..
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef uint64_t u64;

static int n, d, Q;
static int qs[16];
static long N, rad[17];
static int G;
static unsigned char (*perm)[16];
static unsigned char (*sym)[16][8];

static inline int dist(u64 a, u64 b) {
    u64 z = a ^ b;
    z = (z | (z >> 1) | (z >> 2) | (z >> 3)) & 0x1111111111111111ULL;
    return __builtin_popcountll(z);
}
static u64 idx2w(long x) { u64 w = 0; for (int i = 0; i < n; i++) { w |= (u64)(x % qs[i]) << (4 * i); x /= qs[i]; } return w; }
static long w2idx(u64 w) { long x = 0; for (int i = 0; i < n; i++) x += (long)((w >> (4 * i)) & 15) * rad[i]; return x; }
static inline u64 apply(int g, u64 w) {
    u64 v = 0;
    for (int i = 0; i < n; i++) v |= (u64)sym[g][i][(w >> (4 * i)) & 15] << (4 * perm[g][i]);
    return v;
}

static int V, Wd;
static u64 *adj;
static int *wt;
static int best, bestlen, *bestset, *cur;
static long nodes;
static time_t t0; static double tlim; static int timed_out;
static long *gkey;
static int cmpkey(const void *a, const void *b) { long x = gkey[*(int *)a], y = gkey[*(int *)b]; return x > y ? -1 : x < y; }
static int cmpu64(const void *a, const void *b) { u64 x = *(u64 *)a, y = *(u64 *)b; return x < y ? -1 : x > y; }

static void expand(u64 *P, int curw, int depth) {
    if (timed_out) return;
    if ((++nodes & 0x3fff) == 0 && difftime(time(NULL), t0) > tlim) { timed_out = 1; return; }
    int cnt = 0;
    for (int k = 0; k < Wd; k++) cnt += __builtin_popcountll(P[k]);
    int *ord = malloc(sizeof(int) * (cnt + 1)), *ub = malloc(sizeof(int) * (cnt + 1));
    u64 *Qm = malloc(8 * Wd), *R = malloc(8 * Wd), *NP = malloc(8 * Wd);
    memcpy(Qm, P, 8 * Wd);
    int m = 0, cum = 0;
    for (;;) {
        int any = 0; for (int k = 0; k < Wd; k++) if (Qm[k]) { any = 1; break; }
        if (!any) break;
        memcpy(R, Qm, 8 * Wd);
        int start = m, mx = 0;
        for (int k = 0; k < Wd; k++) {
            while (R[k]) {
                int b = __builtin_ctzll(R[k]); int v = k * 64 + b;
                R[k] &= R[k] - 1; Qm[k] &= ~(1ULL << b);
                u64 *a = adj + (size_t)v * Wd;
                for (int j = k; j < Wd; j++) R[j] &= ~a[j];
                ord[m++] = v; if (wt[v] > mx) mx = wt[v];
            }
        }
        cum += mx;
        for (int i = start; i < m; i++) ub[i] = cum;
    }
    for (int i = m - 1; i >= 0; i--) {
        if (curw + ub[i] <= best) break;
        int v = ord[i];
        cur[depth] = v;
        u64 *a = adj + (size_t)v * Wd; int any = 0;
        for (int k = 0; k < Wd; k++) { NP[k] = P[k] & a[k]; any |= NP[k] != 0; }
        if (curw + wt[v] > best) { best = curw + wt[v]; bestlen = depth + 1; memcpy(bestset, cur, sizeof(int) * (depth + 1)); }
        if (any) expand(NP, curw + wt[v], depth + 1);
        if (timed_out) break;
        P[v / 64] &= ~(1ULL << (v % 64));
    }
    free(ord); free(ub); free(Qm); free(R); free(NP);
}

// weighted neighbour sum of v restricted to mask, using per-weight-class masks
static int nwc, wcval[64]; static u64 *wcmask;
static long wsum(u64 *row, u64 *mask) {
    long s = 0;
    for (int c = 0; c < nwc; c++) {
        u64 *mc = wcmask + (size_t)c * Wd; long p = 0;
        for (int k = 0; k < Wd; k++) p += __builtin_popcountll(row[k] & mask[k] & mc[k]);
        s += p * wcval[c];
    }
    return s;
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: osg alph d elements target tlim maxV out\n"); return 2; }
    n = 0; Q = 0;
    { char *s = strdup(argv[1]); for (char *t = strtok(s, ","); t; t = strtok(NULL, ",")) { int a, c; if (sscanf(t, "%dx%d", &a, &c) != 2) { fprintf(stderr, "bad alph\n"); return 2; } for (int i = 0; i < c; i++) qs[n++] = a; if (a > Q) Q = a; } }
    if (n > 16 || Q > 8) { fprintf(stderr, "n<=16, q<=8\n"); return 2; }
    d = atoi(argv[2]);
    int target = atoi(argv[4]); tlim = atof(argv[5]); int maxV = atoi(argv[6]);
    rad[0] = 1; for (int i = 0; i < n; i++) rad[i + 1] = rad[i] * qs[i];
    N = rad[n];
    FILE *f = fopen(argv[3], "r"); if (!f) { fprintf(stderr, "no elements file\n"); return 2; }
    int cap = 1024; G = 0; perm = malloc(sizeof(*perm) * cap); sym = malloc(sizeof(*sym) * cap);
    for (;;) {
        int ok = 1, x;
        if (G == cap) { cap *= 2; perm = realloc(perm, sizeof(*perm) * cap); sym = realloc(sym, sizeof(*sym) * cap); }
        for (int i = 0; i < n && ok; i++) { ok = fscanf(f, "%d", &x) == 1; perm[G][i] = x; }
        for (int i = 0; i < n && ok; i++) for (int s = 0; s < Q && ok; s++) { ok = fscanf(f, "%d", &x) == 1; sym[G][i][s] = x; }
        if (!ok) break;
        G++;
    }
    fclose(f);
    for (int g = 0; g < G; g++) for (int i = 0; i < n; i++) {
        if (qs[perm[g][i]] != qs[i]) { fprintf(stderr, "element %d maps coordinate %d to a different alphabet\n", g, i); return 2; }
        for (int s = 0; s < qs[i]; s++) if (sym[g][i][s] >= qs[i]) { fprintf(stderr, "bad symbol map\n"); return 2; }
    }
    unsigned char *vis = calloc(N, 1);
    long norb = 0; long ocap = 1 << 16, mcap = 1 << 20, nm = 0;
    long *ooff = malloc(sizeof(long) * (ocap + 1)); u64 *mem = malloc(8 * mcap);
    u64 *buf = malloc(8 * G);
    int nsc = 0;
    ooff[0] = 0;
    for (long x = 0; x < N; x++) {
        if (vis[x]) continue;
        norb++;
        u64 u = idx2w(x); int good = 1, nb = 0;
        for (int g = 0; g < G; g++) {
            u64 v = apply(g, u); vis[w2idx(v)] = 1;
            if (good) { if (v != u && dist(u, v) < d) good = 0; else buf[nb++] = v; }
        }
        if (!good) continue;
        if (nsc >= maxV) { nsc++; continue; }
        qsort(buf, nb, 8, cmpu64);
        int k = 0; for (int i = 0; i < nb; i++) if (i == 0 || buf[i] != buf[i - 1]) buf[k++] = buf[i];
        if (nsc + 1 >= ocap) { ocap *= 2; ooff = realloc(ooff, sizeof(long) * (ocap + 1)); }
        if (nm + k > mcap) { while (nm + k > mcap) mcap *= 2; mem = realloc(mem, 8 * mcap); }
        ooff[nsc] = nm; memcpy(mem + nm, buf, 8 * k); nm += k; nsc++; ooff[nsc] = nm;
    }
    free(vis);
    printf("G=%d orbits=%ld selfcompat=%d", G, norb, nsc);
    if (nsc > maxV) { printf(" TOO_MANY_VERTICES\n"); return 3; }
    V = nsc; Wd = (V + 63) / 64; if (Wd == 0) Wd = 1;
    adj = calloc((size_t)V * Wd, 8); wt = malloc(sizeof(int) * (V + 1));
    for (int a = 0; a < V; a++) wt[a] = (int)(ooff[a + 1] - ooff[a]);
    // orbit a and orbit b are compatible iff the representative of a is far from every word of b (G-invariance)
    for (int a = 0; a < V; a++) {
        u64 ra = mem[ooff[a]];
        for (int b = a + 1; b < V; b++) {
            int ok = 1;
            for (long t = ooff[b]; t < ooff[b + 1]; t++) if (dist(ra, mem[t]) < d) { ok = 0; break; }
            if (ok) { adj[(size_t)a * Wd + b / 64] |= 1ULL << (b % 64); adj[(size_t)b * Wd + a / 64] |= 1ULL << (a % 64); }
        }
    }
    // weight classes
    nwc = 0;
    for (int v = 0; v < V; v++) { int c; for (c = 0; c < nwc; c++) if (wcval[c] == wt[v]) break; if (c == nwc && nwc < 64) wcval[nwc++] = wt[v]; }
    wcmask = calloc((size_t)nwc * Wd, 8);
    for (int v = 0; v < V; v++) for (int c = 0; c < nwc; c++) if (wcval[c] == wt[v]) wcmask[(size_t)c * Wd + v / 64] |= 1ULL << (v % 64);
    u64 *alive = calloc(Wd, 8); for (int v = 0; v < V; v++) alive[v / 64] |= 1ULL << (v % 64);
    int changed = 1, nalive = V;
    while (changed) {
        changed = 0;
        for (int v = 0; v < V; v++) {
            if (!(alive[v / 64] >> (v % 64) & 1)) continue;
            long s = wt[v] + wsum(adj + (size_t)v * Wd, alive);
            if (s < target) { alive[v / 64] &= ~(1ULL << (v % 64)); changed = 1; nalive--; }
        }
    }
    printf(" alive=%d", nalive);
    fflush(stdout);
    int *ids = malloc(sizeof(int) * (nalive + 1)); long *key = malloc(sizeof(long) * (V + 1)); int m = 0;
    for (int v = 0; v < V; v++) if (alive[v / 64] >> (v % 64) & 1) { key[v] = wsum(adj + (size_t)v * Wd, alive); ids[m++] = v; }
    gkey = key; qsort(ids, m, sizeof(int), cmpkey);
    int W2 = (m + 63) / 64; if (W2 == 0) W2 = 1;
    u64 *adj2 = calloc((size_t)m * W2, 8); int *wt2 = malloc(sizeof(int) * (m + 1));
    for (int i = 0; i < m; i++) {
        wt2[i] = wt[ids[i]];
        u64 *row = adj + (size_t)ids[i] * Wd;
        for (int j = 0; j < m; j++) if (row[ids[j] / 64] >> (ids[j] % 64) & 1) adj2[(size_t)i * W2 + j / 64] |= 1ULL << (j % 64);
    }
    free(adj); adj = adj2; wt = wt2; Wd = W2; V = m;
    best = target - 1; bestlen = 0; bestset = malloc(sizeof(int) * (V + 2)); cur = malloc(sizeof(int) * (V + 2));
    u64 *P = calloc(Wd, 8); for (int i = 0; i < V; i++) P[i / 64] |= 1ULL << (i % 64);
    t0 = time(NULL); nodes = 0; timed_out = 0;
    if (V > 0) expand(P, 0, 0);
    printf(" nodes=%ld %s best=%d\n", nodes, timed_out ? "TIMEOUT" : "COMPLETE", bestlen ? best : -1);
    if (bestlen) {
        FILE *o = fopen(argv[7], "w");
        fprintf(o, "# size %d, %d orbits, G=%d, alph %s, d=%d\n", best, bestlen, G, argv[1], d);
        for (int i = 0; i < bestlen; i++) {
            int v = ids[bestset[i]];
            for (long t = ooff[v]; t < ooff[v + 1]; t++) {
                for (int c = 0; c < n; c++) fputc('0' + (int)((mem[t] >> (4 * c)) & 15), o);
                fputc('\n', o);
            }
        }
        fclose(o);
    }
    return 0;
}
