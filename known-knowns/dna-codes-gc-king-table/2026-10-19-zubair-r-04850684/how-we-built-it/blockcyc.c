/* Lens block-cyclic: A_4^GC(n,d,w) codes invariant under G = Z_m acting on n = b*m coordinates by rotating every
 * block of m consecutive coordinates by the same amount. Word = (g,l) as in cyc_pairs.c; distance =
 * popcount((g1^g2)|(l1^l2)). Phase 1: visit EVERY word (all g of popcount w, all l), keep the canonical (minimal
 * key g<<n|l) representative of each G-orbit whose orbit is self-compatible (distinct orbit words pairwise >= d);
 * orbit size p = the least k>0 fixing the word (p divides m). Phase 2: compatibility graph on orbits (all G-rotations
 * of j against i). Phase 3: exact maximum-weight clique (weight = orbit size) by branch and bound, stopping early
 * only if a clique of weight >= stop is found (stop = the GC-Plotkin upper bound). Writes the best code found.
 * Usage: blockcyc n m d stop outfile [maxN] [seconds]: skip the cell if more than maxN orbits; stop branch and
 * bound after `seconds` (then the clique is a lower bound only, labelled as such). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
static double t_end = 1e300; static int timed_out = 0;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
typedef uint32_t u32; typedef uint64_t u64;
static int n, m, b, d, w, stopw; static u32 FULL, BM;
static inline u32 brot(u32 x, int k) {            /* rotate each m-bit block of x by k */
    u32 r = 0;
    for (int t = 0; t < b; t++) { u32 blk = (x >> (t * m)) & BM; blk = ((blk << k) | (blk >> (m - k))) & BM; r |= blk << (t * m); }
    return r;
}
static inline int dist(u32 g1, u32 l1, u32 g2, u32 l2) { return __builtin_popcount((g1 ^ g2) | (l1 ^ l2)); }
typedef struct { u32 g, l; int p; } Orb;
static Orb *O; static long N = 0, cap = 0;
static long *adjstart; static int *adj; static long nedges = 0;
static int best_w = 0; static int *best_set, best_k = 0; static int *cur; static long nodes = 0;
static int compat(long i, long j) {
    for (int k = 0; k < O[j].p; k++) if (dist(O[i].g, O[i].l, brot(O[j].g, k), brot(O[j].l, k)) < d) return 0;
    return 1;
}
/* branch and bound over candidate list (sorted, all > last chosen, all adjacent to every chosen vertex) */
static void bb(int *cand, int nc, int curw, int depth) {
    nodes++;
    if ((nodes & 0xffff) == 0 && now() > t_end) timed_out = 1;
    if (timed_out) return;
    if (curw > best_w) { best_w = curw; best_k = depth; memcpy(best_set, cur, depth * sizeof(int)); }
    if (best_w >= stopw) return;
    int rem = 0; for (int i = 0; i < nc; i++) rem += O[cand[i]].p;
    if (curw + rem <= best_w) return;
    int *nxt = malloc(sizeof(int) * (nc > 0 ? nc : 1));
    for (int i = 0; i < nc; i++) {
        rem -= (i ? O[cand[i - 1]].p : 0);
        if (curw + rem <= best_w) break;
        int v = cand[i], nn = 0; long a = adjstart[v], e = adjstart[v + 1];
        for (int j = i + 1; j < nc; j++) {                 /* intersect cand[i+1..] with adj(v) (both sorted) */
            int u = cand[j];
            while (a < e && adj[a] < u) a++;
            if (a < e && adj[a] == u) nxt[nn++] = u;
        }
        cur[depth] = v; bb(nxt, nn, curw + O[v].p, depth + 1);
        if (best_w >= stopw || timed_out) break;
    }
    free(nxt);
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); m = atoi(argv[2]); d = atoi(argv[3]); stopw = atoi(argv[4]); b = n / m; w = n / 2;
    FULL = (1u << n) - 1; BM = (1u << m) - 1;
    long words = 0;
    for (u32 g = 0; g <= FULL; g++) {
        if (__builtin_popcount(g) != w) continue;
        int gmin = 1; for (int k = 1; k < m; k++) if (brot(g, k) < g) { gmin = 0; break; }
        if (!gmin) { words += (1L << n); continue; }        /* not the minimal g in its orbit: its orbit is counted elsewhere */
        for (u32 l = 0; l <= FULL; l++) {
            words++;
            int p = m; for (int k = 1; k < m; k++) if (brot(g, k) == g && brot(l, k) == l) { p = k; break; }
            u64 key = ((u64)g << n) | l; int canon = 1;
            for (int k = 1; k < p; k++) { u32 gk = brot(g, k); if (gk == g && ((((u64)g << n) | brot(l, k)) < key)) { canon = 0; break; } }
            if (!canon) continue;
            int ok = 1;
            for (int k = 1; k < p && ok; k++) if (dist(g, l, brot(g, k), brot(l, k)) < d) ok = 0;
            if (!ok) continue;
            if (N == cap) { cap = cap ? cap * 2 : 1024; O = realloc(O, cap * sizeof(Orb)); }
            O[N].g = g; O[N].l = l; O[N].p = p; N++;
        }
    }
    long maxN = argc > 6 ? atol(argv[6]) : 1L << 40; double secs = argc > 7 ? atof(argv[7]) : 1e300;
    long psz[33] = {0}; for (long i = 0; i < N; i++) psz[O[i].p]++;
    printf("n=%d m=%d b=%d d=%d w=%d words_visited=%ld self_compatible_orbits=%ld", n, m, b, d, w, words, N);
    for (int p = 1; p <= m; p++) if (psz[p]) printf(" size%d:%ld", p, psz[p]);
    printf("\n"); fflush(stdout);
    if (N > maxN) { printf("SKIPPED: %ld orbits > maxN %ld\n", N, maxN); return 0; }
    /* adjacency, two passes (count then fill), parallel */
    long *deg = calloc(N + 1, sizeof(long));
    #pragma omp parallel for schedule(dynamic, 64)
    for (long i = 0; i < N; i++) { long c = 0; for (long j = i + 1; j < N; j++) if (compat(i, j)) c++; deg[i] = c; }
    adjstart = malloc((N + 1) * sizeof(long)); adjstart[0] = 0;
    for (long i = 0; i < N; i++) adjstart[i + 1] = adjstart[i] + deg[i];
    nedges = adjstart[N];
    printf("compatible_pairs=%ld\n", nedges); fflush(stdout);
    adj = malloc((nedges ? nedges : 1) * sizeof(int));
    #pragma omp parallel for schedule(dynamic, 64)
    for (long i = 0; i < N; i++) { long c = adjstart[i]; for (long j = i + 1; j < N; j++) if (compat(i, j)) adj[c++] = (int)j; }
    best_set = malloc(64 * sizeof(int)); cur = malloc(64 * sizeof(int));
    int *all = malloc(N * sizeof(int)); for (long i = 0; i < N; i++) all[i] = (int)i;
    t_end = now() + secs;
    bb(all, (int)N, 0, 0);
    printf("max_weight_clique=%d orbits=%d bb_nodes=%ld %s\n", best_w, best_k, nodes,
           best_w >= stopw ? "(stopped: reached the upper bound)" : timed_out ? "(TIMEOUT: lower bound only, not exhaustive)" : "(exact: search completed)");
    FILE *f = fopen(argv[5], "w");
    for (int t = 0; t < best_k; t++) { Orb *o = &O[best_set[t]];
        for (int k = 0; k < o->p; k++) { u32 g = brot(o->g, k), l = brot(o->l, k);
            for (int i = 0; i < n; i++) { int G = (g >> i) & 1, L = (l >> i) & 1; fputc(G ? (L ? 'G' : 'C') : (L ? 'T' : 'A'), f); }
            fputc('\n', f); } }
    fclose(f);
    return 0;
}
