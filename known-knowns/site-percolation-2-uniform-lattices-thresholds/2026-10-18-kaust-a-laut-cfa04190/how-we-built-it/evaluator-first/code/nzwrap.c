/* nzwrap.c -- Newman-Ziff sweeps with cluster winding on an L1 x L2 torus of unit cells.
 *
 * Sites (site mode) or bonds (bond mode) are added in a uniformly random order. Union-find keeps, for every
 * vertex, its unwrapped cell displacement to its parent, so a bond closing a cycle reveals the cycle's winding
 * vector (a, b) in units of the torus periods. Each cluster root keeps the rank (0, 1, 2) of the lattice of
 * winding vectors of its cycles and, at rank 1, its primitive direction.
 * Per sample two numbers are recorded:
 *   n1 = number of added elements when the first cluster with a non-contractible cycle appears
 *        (so the "0D" event, no winding cluster, holds exactly for n < n1),
 *   n2 = number of added elements when the first cluster with rank-2 winding appears ("2D" holds for n >= n2).
 * Histograms of n1 and n2 are written block by block (independent batches for error bars).
 *
 * usage: nzwrap <lattice file> <site|bond> L1 L2 <samples per block> <blocks> <seed> <outdir> [tag]
 * Resumable: an existing outdir/<tag>.state file continues the run with its RNG state and block counter.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t next64(void) {   /* xoshiro256** */
    const uint64_t r = rotl(s[1] * 5, 7) * 9;
    const uint64_t t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45);
    return r;
}
static uint64_t splitmix(uint64_t *x) {
    uint64_t z = (*x += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static inline uint32_t bounded(uint32_t n) {  /* Lemire, unbiased */
    uint64_t m = (uint64_t)(uint32_t)next64() * n;
    uint32_t l = (uint32_t)m;
    if (l < n) {
        uint32_t t = -n % n;
        while (l < t) { m = (uint64_t)(uint32_t)next64() * n; l = (uint32_t)m; }
    }
    return (uint32_t)(m >> 32);
}

static int K, E;               /* vertices and edges per cell */
static int *ei, *ej, *ed1, *ed2;
static int L1, L2, N, NB;
static int bond_mode;
/* adjacency (site mode): for vertex x, list of (neighbour, dx, dy) */
static int *adj_start, *adj_nb, *adj_dx, *adj_dy;
/* bonds (bond mode) */
static int *bu, *bw, *bdx, *bdy;

static int32_t *par, *dxp, *dyp, *sz;
static int8_t *rk; static int8_t *va, *vb;   /* rank and primitive direction at roots (in torus periods) */
static int *occ;
static int *order;

static int vid(int c1, int c2, int v) {
    c1 %= L1; if (c1 < 0) c1 += L1;
    c2 %= L2; if (c2 < 0) c2 += L2;
    return (c2 * L1 + c1) * K + v;
}

static inline int find(int x, int *ox, int *oy) {
    /* returns root; ox, oy = displacement from root to x (pos(x) - pos(root)), with full path compression */
    int r = x, ax = 0, ay = 0;
    while (par[r] != r) { ax += dxp[r]; ay += dyp[r]; r = par[r]; }
    /* compress: second pass */
    int y = x, cx = ax, cy = ay;
    while (par[y] != y) {
        int p = par[y], tx = dxp[y], ty = dyp[y];
        par[y] = r; dxp[y] = cx; dyp[y] = cy;
        cx -= tx; cy -= ty; y = p;
    }
    *ox = ax; *oy = ay;
    return r;
}

static int gcd(int a, int b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { int t = a % b; a = b; b = t; } return a; }
static void prim(int *a, int *b) {
    int g = gcd(*a, *b); *a /= g; *b /= g;
    if (*a < 0 || (*a == 0 && *b < 0)) { *a = -*a; *b = -*b; }
}
static int any1, any2;
static void add_cycle(int r, int cx, int cy) {
    /* cycle displacement (cx, cy) in cells; winding in periods */
    if (cx % L1 != 0 || cy % L2 != 0) { fprintf(stderr, "error: cycle displacement not a period multiple\n"); exit(3); }
    int a = cx / L1, b = cy / L2;
    if (a == 0 && b == 0) return;
    prim(&a, &b);
    if (rk[r] == 0) { rk[r] = 1; va[r] = (int8_t)a; vb[r] = (int8_t)b; any1 = 1; }
    else if (rk[r] == 1) { if (va[r] * b - vb[r] * a != 0) { rk[r] = 2; any2 = 1; } }
}
static void join(int u, int w, int ex, int ey) {
    /* bond from u to w with displacement e = pos(w) - pos(u) */
    int ux, uy, wx, wy;
    int ru = find(u, &ux, &uy), rw = find(w, &wx, &wy);
    if (ru == rw) { add_cycle(ru, ux + ex - wx, uy + ey - wy); return; }
    /* pos(rw) - pos(ru) = ux + ex - wx */
    int dx = ux + ex - wx, dy = uy + ey - wy;
    if (sz[ru] < sz[rw]) { int t = ru; ru = rw; rw = t; dx = -dx; dy = -dy; }
    par[rw] = ru; dxp[rw] = dx; dyp[rw] = dy; sz[ru] += sz[rw];
    /* merge winding information */
    if (rk[rw] == 2) rk[ru] = 2;
    else if (rk[rw] == 1) {
        if (rk[ru] == 0) { rk[ru] = 1; va[ru] = va[rw]; vb[ru] = vb[rw]; }
        else if (rk[ru] == 1 && va[ru] * vb[rw] - vb[ru] * va[rw] != 0) rk[ru] = 2;
    }
    if (rk[ru] == 2) any2 = 1;
}

int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage: nzwrap latfile site|bond L1 L2 samples blocks seed outdir [tag]\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
    bond_mode = strcmp(argv[2], "bond") == 0;
    L1 = atoi(argv[3]); L2 = atoi(argv[4]);
    long long spb = atoll(argv[5]); int nblocks = atoi(argv[6]);
    uint64_t seed = strtoull(argv[7], NULL, 10);
    const char *outdir = argv[8];
    char tag[256];
    if (argc > 9) snprintf(tag, sizeof tag, "%s", argv[9]);
    else snprintf(tag, sizeof tag, "%s_L%dx%d_s%llu", bond_mode ? "bond" : "site", L1, L2, (unsigned long long)seed);
    if (fscanf(f, " K %d E %d", &K, &E) != 2) { fprintf(stderr, "bad lattice header\n"); return 1; }
    ei = malloc(sizeof(int) * E); ej = malloc(sizeof(int) * E); ed1 = malloc(sizeof(int) * E); ed2 = malloc(sizeof(int) * E);
    for (int k = 0; k < E; k++) if (fscanf(f, " %d %d %d %d", &ei[k], &ej[k], &ed1[k], &ed2[k]) != 4) { fprintf(stderr, "bad edge\n"); return 1; }
    fclose(f);
    N = L1 * L2 * K; NB = L1 * L2 * E;
    /* adjacency */
    int *deg = calloc(K, sizeof(int));
    for (int k = 0; k < E; k++) { deg[ei[k]]++; deg[ej[k]]++; }
    int maxdeg = 0; for (int v = 0; v < K; v++) if (deg[v] > maxdeg) maxdeg = deg[v];
    adj_start = malloc(sizeof(int) * (N + 1));
    adj_nb = malloc(sizeof(int) * (size_t)N * maxdeg); adj_dx = malloc(sizeof(int) * (size_t)N * maxdeg); adj_dy = malloc(sizeof(int) * (size_t)N * maxdeg);
    bu = malloc(sizeof(int) * NB); bw = malloc(sizeof(int) * NB); bdx = malloc(sizeof(int) * NB); bdy = malloc(sizeof(int) * NB);
    {
        int q = 0, b = 0;
        for (int x = 0; x < N; x++) {     /* vertex ids in increasing order: x = (c2 * L1 + c1) * K + v */
            adj_start[x] = q;
            int c2 = (x / K) / L1, c1 = (x / K) % L1, v = x % K;
            for (int k = 0; k < E; k++) {
                if (ei[k] == v) { adj_nb[q] = vid(c1 + ed1[k], c2 + ed2[k], ej[k]); adj_dx[q] = ed1[k]; adj_dy[q] = ed2[k]; q++; }
                if (ej[k] == v) { adj_nb[q] = vid(c1 - ed1[k], c2 - ed2[k], ei[k]); adj_dx[q] = -ed1[k]; adj_dy[q] = -ed2[k]; q++; }
            }
        }
        adj_start[N] = q;
        for (int c2 = 0; c2 < L2; c2++) for (int c1 = 0; c1 < L1; c1++) for (int k = 0; k < E; k++) {
            bu[b] = vid(c1, c2, ei[k]); bw[b] = vid(c1 + ed1[k], c2 + ed2[k], ej[k]); bdx[b] = ed1[k]; bdy[b] = ed2[k]; b++;
        }
    }
    int M = bond_mode ? NB : N;
    par = malloc(sizeof(int32_t) * N); dxp = malloc(sizeof(int32_t) * N); dyp = malloc(sizeof(int32_t) * N);
    sz = malloc(sizeof(int32_t) * N); rk = malloc(N); va = malloc(N); vb = malloc(N);
    occ = malloc(sizeof(int) * N); order = malloc(sizeof(int) * M);
    long long *h1 = calloc(M + 1, sizeof(long long)), *h2 = calloc(M + 1, sizeof(long long));
    /* state */
    char path[1024];
    snprintf(path, sizeof path, "%s/%s.state", outdir, tag);
    int block0 = 0;
    FILE *sf = fopen(path, "r");
    if (sf) {
        unsigned long long a, b2, c, d; int blk;
        if (fscanf(sf, " block %d rng %llu %llu %llu %llu", &blk, &a, &b2, &c, &d) == 5) {
            block0 = blk; s[0] = a; s[1] = b2; s[2] = c; s[3] = d;
            fprintf(stderr, "resuming %s at block %d\n", tag, block0);
        }
        fclose(sf);
    } else {
        uint64_t x = seed;
        for (int i = 0; i < 4; i++) s[i] = splitmix(&x);
    }
    for (int blk = block0; blk < nblocks; blk++) {
        time_t tb = time(NULL);
        memset(h1, 0, sizeof(long long) * (M + 1)); memset(h2, 0, sizeof(long long) * (M + 1));
        for (long long smp = 0; smp < spb; smp++) {
            for (int i = 0; i < M; i++) order[i] = i;
            any1 = 0; any2 = 0;
            int n1 = -1, n2 = -1;
            if (!bond_mode) {
                for (int i = 0; i < N; i++) occ[i] = 0;
            } else {
                for (int i = 0; i < N; i++) { par[i] = i; dxp[i] = 0; dyp[i] = 0; sz[i] = 1; rk[i] = 0; }
            }
            for (int n = 0; n < M; n++) {
                int j = n + (int)bounded((uint32_t)(M - n));
                int e = order[j]; order[j] = order[n]; order[n] = e;
                if (!bond_mode) {
                    int x = e;
                    occ[x] = 1; par[x] = x; dxp[x] = 0; dyp[x] = 0; sz[x] = 1; rk[x] = 0;
                    for (int q = adj_start[x]; q < adj_start[x + 1]; q++) {
                        int y = adj_nb[q];
                        if (occ[y]) join(x, y, adj_dx[q], adj_dy[q]);
                    }
                } else {
                    join(bu[e], bw[e], bdx[e], bdy[e]);
                }
                /* after adding n+1 elements */
                if (n1 < 0 && any1) n1 = n + 1;
                if (any2) { n2 = n + 1; if (n1 < 0) n1 = n + 1; break; }
            }
            if (n1 < 0 || n2 < 0) { fprintf(stderr, "error: no rank-2 cluster at full occupation\n"); return 4; }
            h1[n1]++; h2[n2]++;
        }
        /* write block */
        snprintf(path, sizeof path, "%s/%s_b%04d.hist", outdir, tag, blk);
        FILE *of = fopen(path, "w");
        fprintf(of, "mode %s L1 %d L2 %d K %d E %d M %d samples %lld seed %llu block %d\n",
                bond_mode ? "bond" : "site", L1, L2, K, E, M, spb, (unsigned long long)seed, blk);
        for (int n = 0; n <= M; n++) if (h1[n] || h2[n]) fprintf(of, "%d %lld %lld\n", n, h1[n], h2[n]);
        fclose(of);
        snprintf(path, sizeof path, "%s/%s.state", outdir, tag);
        char tmpp[1100]; snprintf(tmpp, sizeof tmpp, "%s.tmp", path);
        FILE *st = fopen(tmpp, "w");
        fprintf(st, "block %d rng %llu %llu %llu %llu\n", blk + 1, (unsigned long long)s[0], (unsigned long long)s[1],
                (unsigned long long)s[2], (unsigned long long)s[3]);
        fclose(st);
        remove(path); rename(tmpp, path);
        fprintf(stderr, "%s block %d done, %lld samples, %ld s\n", tag, blk, spb, (long)(time(NULL) - tb));
    }
    return 0;
}
