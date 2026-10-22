/* nzwrap2.c -- cache-friendly rewrite of nzwrap.c (run 2026-10-16-0447), same computation, same outputs.
 *
 * Same model, command line, RNG stream (xoshiro256** seeded by splitmix64, Lemire bounded draws in the same order),
 * Fisher-Yates order, histogram, .hist/.state/log formats as nzwrap.c. Only the memory layout changes:
 *   - one 16-byte record per vertex (parent, unwrapped displacement to parent, root data) instead of seven arrays;
 *     an unoccupied site is marked by par = -1;
 *   - union by rank (5 bits) instead of union by size; rank, winding rank and primitive direction packed in one word;
 *   - neighbours (site mode) computed from precomputed offsets and a per-vertex flag byte (column at the seam,
 *     cell vertex), and bond endpoints (bond mode) from the bond id (bond id = (c2 L1 + c1) E + k, as in nzwrap.c),
 *     instead of stored adjacency and bond arrays.
 * n1 and n2 depend only on the random order and the topology of the occupied set (the winding lattice of a
 * cluster does not depend on the union-find tree or on the order of joins within one step), so the .hist files
 * must be byte-identical to nzwrap's for the same arguments: that is the regression test (test_nzwrap2.py).
 *
 * usage: nzwrap2 <lattice file> <site|bond> L1 L2 <samples per block> <blocks> <seed> <outdir> [tag]
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
static inline uint32_t bounded(uint32_t n) {  /* Lemire, unbiased; identical to nzwrap.c */
    uint64_t m = (uint64_t)(uint32_t)next64() * n;
    uint32_t l = (uint32_t)m;
    if (l < n) {
        uint32_t t = -n % n;
        while (l < t) { m = (uint64_t)(uint32_t)next64() * n; l = (uint32_t)m; }
    }
    return (uint32_t)(m >> 32);
}

typedef struct { int32_t par, dx, dy; uint32_t aux; } vrec;   /* aux at roots: rank | wr << 5 | va << 8 | vb << 16 */
#define AUX(rank, wr, a, b) ((uint32_t)(rank) | ((uint32_t)(wr) << 5) | ((uint32_t)(uint8_t)(int8_t)(a) << 8) | ((uint32_t)(uint8_t)(int8_t)(b) << 16))
#define RANK(x) ((x) & 31u)
#define WR(x) (((x) >> 5) & 3u)
#define VA(x) ((int)(int8_t)(uint8_t)(((x) >> 8) & 255u))
#define VB(x) ((int)(int8_t)(uint8_t)(((x) >> 16) & 255u))

static int K, E, L1, L2, N, NB, bond_mode;
static int *ei, *ej, *ed1, *ed2;
static int nadj[64], adj_j[64][32], adj_d1[64][32], adj_d2[64][32];   /* per cell vertex, in nzwrap.c's order */
static int adj_off[64][32];      /* id(neighbour) - id(x) before wraparound: (d2 L1 + d1) K + j - v */
static int bond_off[16];         /* the same for bond k: (ed2 L1 + ed1) K + ej - ei */
static uint8_t *fl;              /* per vertex: bit 0 = cell column c1 is 0, bit 1 = c1 is L1 - 1, bits 2-7 = v */
static vrec *V;
static int32_t *order;
static int any1, any2;

/* id of the neighbour of x at offset off with column step d1 (-1, 0, +1), without divisions */
static inline int nbr(int x, int off, int d1) {
    int y = x + off;
    if (d1 > 0 && (fl[x] & 2)) y -= L1 * K;
    else if (d1 < 0 && (fl[x] & 1)) y += L1 * K;
    if (y >= N) y -= N; else if (y < 0) y += N;
    return y;
}

static inline int vid(int c1, int c2, int v) {
    if (c1 >= L1) c1 -= L1; else if (c1 < 0) c1 += L1;
    if (c2 >= L2) c2 -= L2; else if (c2 < 0) c2 += L2;
    return (c2 * L1 + c1) * K + v;
}

static inline int find(int x, int *ox, int *oy) {
    int r = x, ax = 0, ay = 0;
    while (V[r].par != r) { ax += V[r].dx; ay += V[r].dy; r = V[r].par; }
    int y = x, cx = ax, cy = ay;
    while (V[y].par != y) {
        int p = V[y].par, tx = V[y].dx, ty = V[y].dy;
        V[y].par = r; V[y].dx = cx; V[y].dy = cy;
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
static void add_cycle(int r, int cx, int cy) {
    if (cx % L1 != 0 || cy % L2 != 0) { fprintf(stderr, "error: cycle displacement not a period multiple\n"); exit(3); }
    int a = cx / L1, b = cy / L2;
    if (a == 0 && b == 0) return;
    prim(&a, &b);
    if (a > 127 || a < -127 || b > 127 || b < -127) { fprintf(stderr, "error: winding direction out of int8 range\n"); exit(5); }
    uint32_t x = V[r].aux;
    if (WR(x) == 0) { V[r].aux = AUX(RANK(x), 1, a, b); any1 = 1; }
    else if (WR(x) == 1) { if (VA(x) * b - VB(x) * a != 0) { V[r].aux = AUX(RANK(x), 2, VA(x), VB(x)); any2 = 1; } }
}
static void join(int u, int w, int ex, int ey) {
    int ux, uy, wx, wy;
    int ru = find(u, &ux, &uy), rw = find(w, &wx, &wy);
    if (ru == rw) { add_cycle(ru, ux + ex - wx, uy + ey - wy); return; }
    int dx = ux + ex - wx, dy = uy + ey - wy;     /* pos(rw) - pos(ru) */
    uint32_t xu = V[ru].aux, xw = V[rw].aux;
    if (RANK(xu) < RANK(xw)) { int t = ru; ru = rw; rw = t; dx = -dx; dy = -dy; uint32_t tt = xu; xu = xw; xw = tt; }
    V[rw].par = ru; V[rw].dx = dx; V[rw].dy = dy;
    int rank = RANK(xu) + (RANK(xu) == RANK(xw));
    int wr = WR(xu), a = VA(xu), b = VB(xu);
    if (WR(xw) == 2) wr = 2;
    else if (WR(xw) == 1) {
        if (wr == 0) { wr = 1; a = VA(xw); b = VB(xw); }
        else if (wr == 1 && a * VB(xw) - b * VA(xw) != 0) wr = 2;
    }
    V[ru].aux = AUX(rank, wr, a, b);
    if (wr == 2) any2 = 1;
}

int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage: nzwrap2 latfile site|bond L1 L2 samples blocks seed outdir [tag]\n"); return 1; }
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
    if (K > 63) { fprintf(stderr, "too many vertices per cell\n"); return 1; }
    ei = malloc(sizeof(int) * E); ej = malloc(sizeof(int) * E); ed1 = malloc(sizeof(int) * E); ed2 = malloc(sizeof(int) * E);
    for (int k = 0; k < E; k++) if (fscanf(f, " %d %d %d %d", &ei[k], &ej[k], &ed1[k], &ed2[k]) != 4) { fprintf(stderr, "bad edge\n"); return 1; }
    fclose(f);
    for (int k = 0; k < E; k++) {
        if (ed1[k] > 1 || ed1[k] < -1 || ed2[k] > 1 || ed2[k] < -1) { fprintf(stderr, "edge offsets beyond one cell are not supported\n"); return 1; }
    }
    if (L1 < 3 || L2 < 3) { fprintf(stderr, "L1, L2 >= 3 required (single-step wraparound)\n"); return 1; }
    for (int v = 0; v < K; v++) {          /* same order as nzwrap.c's adjacency build */
        nadj[v] = 0;
        for (int k = 0; k < E; k++) {
            if (ei[k] == v) { adj_j[v][nadj[v]] = ej[k]; adj_d1[v][nadj[v]] = ed1[k]; adj_d2[v][nadj[v]] = ed2[k]; nadj[v]++; }
            if (ej[k] == v) { adj_j[v][nadj[v]] = ei[k]; adj_d1[v][nadj[v]] = -ed1[k]; adj_d2[v][nadj[v]] = -ed2[k]; nadj[v]++; }
            if (nadj[v] > 30) { fprintf(stderr, "degree too large\n"); return 1; }
        }
    }
    N = L1 * L2 * K; NB = L1 * L2 * E;
    if (E > 16 || N >= (1 << 28)) { fprintf(stderr, "E <= 16 and N < 2^28 required\n"); return 1; }
    int M = bond_mode ? NB : N;
    for (int v = 0; v < K; v++)
        for (int q = 0; q < nadj[v]; q++) adj_off[v][q] = (adj_d2[v][q] * L1 + adj_d1[v][q]) * K + adj_j[v][q] - v;
    for (int k = 0; k < E; k++) bond_off[k] = (ed2[k] * L1 + ed1[k]) * K + ej[k] - ei[k];
    fl = malloc((size_t)N);
    for (int c2 = 0; c2 < L2; c2++) for (int c1 = 0; c1 < L1; c1++) for (int v = 0; v < K; v++)
        fl[(c2 * L1 + c1) * K + v] = (uint8_t)((c1 == 0 ? 1 : 0) | (c1 == L1 - 1 ? 2 : 0) | (v << 2));
    V = malloc(sizeof(vrec) * (size_t)N);
    order = malloc(sizeof(int32_t) * (size_t)M);
    long long *h1 = calloc(M + 1, sizeof(long long)), *h2 = calloc(M + 1, sizeof(long long));
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
                for (int i = 0; i < N; i++) V[i].par = -1;
            } else {
                for (int i = 0; i < N; i++) { V[i].par = i; V[i].dx = 0; V[i].dy = 0; V[i].aux = 0; }
            }
            for (int n = 0; n < M; n++) {
                int j = n + (int)bounded((uint32_t)(M - n));
                int e = order[j]; order[j] = order[n]; order[n] = e;
                if (!bond_mode) {
                    int x = e, v = fl[x] >> 2;
                    V[x].par = x; V[x].dx = 0; V[x].dy = 0; V[x].aux = 0;
                    for (int q = 0; q < nadj[v]; q++) {
                        int y = nbr(x, adj_off[v][q], adj_d1[v][q]);
                        if (V[y].par >= 0) join(x, y, adj_d1[v][q], adj_d2[v][q]);
                    }
                } else {
                    int cell = e / E, k = e - cell * E, u = cell * K + ei[k], w = u + bond_off[k];
                    if (ed1[k] > 0 && cell % L1 == L1 - 1) w -= L1 * K;
                    else if (ed1[k] < 0 && cell % L1 == 0) w += L1 * K;
                    if (w >= N) w -= N; else if (w < 0) w += N;
                    join(u, w, ed1[k], ed2[k]);
                }
                if (n1 < 0 && any1) n1 = n + 1;
                if (any2) { n2 = n + 1; if (n1 < 0) n1 = n + 1; break; }
            }
            if (n1 < 0 || n2 < 0) { fprintf(stderr, "error: no rank-2 cluster at full occupation\n"); return 4; }
            h1[n1]++; h2[n2]++;
        }
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
