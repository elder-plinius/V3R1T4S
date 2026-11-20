// Orbit-method search for q-ary codes of length n <= 16, minimum distance d.
// usage: orbsearch q n d elements_file target time_limit_s max_vertices out_file [fixed_code_file]
// elements_file: one group element per line: n ints (coordinate permutation pi) then q ints (symbol permutation sigma);
//   action: (g w)[pi[i]] = sigma[w[i]]. Must list the whole group (closure done by the caller).
// Vertices are orbits whose words are pairwise at distance >= d (and, if a fixed code is given, at distance >= d from
// every fixed word). Edge = the two orbits are mutually at distance >= d. Finds a max-weight clique (weight = orbit
// size) among cliques of weight >= target; prints result line. Exhaustive unless the time limit hits.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef uint64_t u64;

static int q, n, d;
static long N;
static int G;
static int (*perm)[16];
static int (*sym)[8];

static inline int dist(u64 a, u64 b) {
    u64 z = a ^ b;
    z = (z | (z >> 1) | (z >> 2) | (z >> 3)) & 0x1111111111111111ULL;
    return __builtin_popcountll(z);
}

static long powq[17];

static u64 idx2w(long x) { u64 w = 0; for (int i = 0; i < n; i++) { w |= (u64)(x % q) << (4 * i); x /= q; } return w; }
static long w2idx(u64 w) { long x = 0; for (int i = 0; i < n; i++) x += (long)((w >> (4 * i)) & 15) * powq[i]; return x; }
static u64 apply(int g, u64 w) {
    u64 v = 0;
    for (int i = 0; i < n; i++) v |= (u64)sym[g][(w >> (4 * i)) & 15] << (4 * perm[g][i]);
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
    int *ord = malloc(sizeof(int) * cnt), *ub = malloc(sizeof(int) * cnt);
    u64 *Q = malloc(8 * Wd), *R = malloc(8 * Wd), *NP = malloc(8 * Wd);
    memcpy(Q, P, 8 * Wd);
    int m = 0, cum = 0;
    for (;;) {
        int any = 0; for (int k = 0; k < Wd; k++) if (Q[k]) { any = 1; break; }
        if (!any) break;
        memcpy(R, Q, 8 * Wd);
        int start = m, mx = 0;
        for (int k = 0; k < Wd; k++) {
            while (R[k]) {
                int b = __builtin_ctzll(R[k]); int v = k * 64 + b;
                R[k] &= R[k] - 1; Q[k] &= ~(1ULL << b);
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
    free(ord); free(ub); free(Q); free(R); free(NP);
}

int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage\n"); return 2; }
    q = atoi(argv[1]); n = atoi(argv[2]); d = atoi(argv[3]);
    int target = atoi(argv[5]); tlim = atof(argv[6]); int maxV = atoi(argv[7]);
    powq[0] = 1; for (int i = 1; i <= n; i++) powq[i] = powq[i - 1] * q;
    N = powq[n];
    FILE *f = fopen(argv[4], "r");
    int cap = 1024; G = 0; perm = malloc(sizeof(*perm) * cap); sym = malloc(sizeof(*sym) * cap);
    for (;;) {
        int ok = 1;
        if (G == cap) { cap *= 2; perm = realloc(perm, sizeof(*perm) * cap); sym = realloc(sym, sizeof(*sym) * cap); }
        for (int i = 0; i < n && ok; i++) ok = fscanf(f, "%d", &perm[G][i]) == 1;
        for (int i = 0; i < q && ok; i++) ok = fscanf(f, "%d", &sym[G][i]) == 1;
        if (!ok) break;
        G++;
    }
    fclose(f);
    int nfix = 0; u64 fixed[4096];
    if (argc > 9) {
        FILE *g = fopen(argv[9], "r"); char line[256];
        while (fgets(line, sizeof line, g)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            u64 w = 0; for (int i = 0; i < n; i++) w |= (u64)(line[i] - '0') << (4 * i);
            fixed[nfix++] = w;
        }
        fclose(g);
    }
    unsigned char *vis = calloc(N, 1);
    long norb = 0; long ocap = 1 << 16, mcap = 1 << 20, nm = 0;
    long *ooff = malloc(sizeof(long) * (ocap + 1)); u64 *mem = malloc(8 * mcap);
    u64 *buf = malloc(8 * G);
    int nsc = 0;
    for (long x = 0; x < N; x++) {
        if (vis[x]) continue;
        norb++;
        u64 u = idx2w(x); int good = 1;
        for (int j = 0; j < nfix && good; j++) if (dist(u, fixed[j]) < d) good = 0;
        int nb = 0;
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
    printf("G=%d orbits=%ld selfcompat=%d", G, norb, nsc);
    if (nsc > maxV) { printf(" TOO_MANY_VERTICES\n"); return 3; }
    V = nsc; Wd = (V + 63) / 64; if (Wd == 0) Wd = 1;
    adj = calloc((size_t)V * Wd, 8); wt = malloc(sizeof(int) * V);
    for (int a = 0; a < V; a++) wt[a] = (int)(ooff[a + 1] - ooff[a]);
    #pragma omp parallel for schedule(dynamic, 16)
    for (int a = 0; a < V; a++) {
        u64 ra = mem[ooff[a]];
        for (int b = 0; b < V; b++) {
            if (b == a) continue;
            int ok = 1;
            for (long t = ooff[b]; t < ooff[b + 1]; t++) if (dist(ra, mem[t]) < d) { ok = 0; break; }
            if (ok) adj[(size_t)a * Wd + b / 64] |= 1ULL << (b % 64);
        }
    }
    // prune: a vertex needs w(v) + sum of neighbour weights >= target
    unsigned char *alive = malloc(V); memset(alive, 1, V);
    int changed = V <= 40000, nalive = V;
    while (changed) {
        changed = 0;
        for (int v = 0; v < V; v++) {
            if (!alive[v]) continue;
            long s = wt[v];
            for (int u = 0; u < V; u++) if (alive[u] && (adj[(size_t)v * Wd + u / 64] >> (u % 64) & 1)) s += wt[u];
            if (s < target) { alive[v] = 0; changed = 1; nalive--; }
        }
    }
    printf(" alive=%d", nalive);
    // relabel alive vertices by decreasing weighted degree
    int *ids = malloc(sizeof(int) * nalive); long *key = malloc(sizeof(long) * V); int m = 0;
    for (int v = 0; v < V; v++) if (alive[v]) {
        long s = 0; for (int u = 0; u < V; u++) if (alive[u] && (adj[(size_t)v * Wd + u / 64] >> (u % 64) & 1)) s += wt[u];
        key[v] = s; ids[m++] = v;
    }
    gkey = key; qsort(ids, m, sizeof(int), cmpkey);
    int W2 = (m + 63) / 64; if (W2 == 0) W2 = 1;
    u64 *adj2 = calloc((size_t)m * W2, 8); int *wt2 = malloc(sizeof(int) * (m + 1));
    for (int i = 0; i < m; i++) {
        wt2[i] = wt[ids[i]];
        for (int j = 0; j < m; j++) if (adj[(size_t)ids[i] * Wd + ids[j] / 64] >> (ids[j] % 64) & 1) adj2[(size_t)i * W2 + j / 64] |= 1ULL << (j % 64);
    }
    // MCQ colouring takes vertices in index order; put heavy-degree vertices last so they are branched first
    free(adj); adj = adj2; wt = wt2; Wd = W2; V = m;
    best = target - 1; bestlen = 0; bestset = malloc(sizeof(int) * 256); cur = malloc(sizeof(int) * 256);
    u64 *P = calloc(Wd, 8); for (int i = 0; i < V; i++) P[i / 64] |= 1ULL << (i % 64);
    t0 = time(NULL); nodes = 0; timed_out = 0;
    if (V > 0) expand(P, 0, 0);
    printf(" nodes=%ld %s best=%d\n", nodes, timed_out ? "TIMEOUT" : "COMPLETE", bestlen ? best : -1);
    if (bestlen) {
        FILE *o = fopen(argv[8], "w");
        fprintf(o, "# size %d, %d orbits, G=%d\n", best, bestlen, G);
        for (int i = 0; i < bestlen; i++) {
            int v = ids[bestset[i]];
            for (long t = ooff[v]; t < ooff[v + 1]; t++) {
                for (int c = 0; c < n; c++) fputc('0' + (int)((mem[t] >> (4 * c)) & 15), o);
                fputc('\n', o);
            }
        }
        for (int j = 0; j < nfix; j++) { for (int c = 0; c < n; c++) fputc('0' + (int)((fixed[j] >> (4 * c)) & 15), o); fputs("  # fixed\n", o); }
        fclose(o);
    }
    return 0;
}
