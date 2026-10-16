/* covsearch3 (v2 plus two switches: pnoise, maxcand): weighted tabu local search for (v,k,t) covering designs with a fixed number of blocks b.
 * State: b blocks (k-subsets of 0..v-1). Exact coverage counts per t-subset (colex rank).
 * Step: pick a random uncovered t-set T; for every block B with the largest |B cap T| and every point q in B\T,
 * evaluate the weighted delta of replacing q by p (p = a random point of T\B); apply the best non-tabu move
 * (aspiration if it reaches a new best). If the best weighted delta is >= 0, raise w[T] by 1.
 * Delta per block uses one pass over the t-subsets and (t-1)-subsets of B, so all q are scored at once.
 *
 * If the best weighted delta is >= 0 the move is applied only with probability pnoise (v2 = pnoise 1).
 * maxcand > 0 scores at most that many random candidate blocks per step (v2 = all).
 * usage: covsearch3 v k t b seconds seed outfile [init|-] [tenure] [maxw] [pnoise] [maxcand]
 * Exit 0 iff a full covering was found (written to outfile, 1-based, one block per line).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MAXV 100
#define MAXK 26
#define MAXT 9
#define MAXB 50000

static uint64_t binom[MAXV + 1][MAXT + 1];
static int V, K, T, B;
static uint16_t *cnt;
static uint32_t *w;
static uint32_t *unc_list, *unc_pos;
static uint64_t n_unc, NT;
static int pts[MAXB][MAXK];
static uint64_t msk[MAXB][2];
static int best_pts[MAXB][MAXK];
static uint64_t best_cost;
static int64_t tabu_until[MAXB][MAXV];
static int cand[MAXB];
/* enumeration tables of index subsets of 0..k-1 */
static int nsubT, nsubT1;
static uint8_t (*subT)[MAXT], (*subT1)[MAXT];

static uint64_t s0, s1;
static inline uint64_t rnd(void) {
    uint64_t a = s0, b = s1;
    s0 = b; a ^= a << 23; a ^= a >> 17; a ^= b ^ (b >> 26); s1 = a;
    return a + b;
}
static inline uint32_t rndn(uint32_t n) { return (uint32_t)(((rnd() >> 32) * (uint64_t)n) >> 32); }
static double now(void) { struct timespec ts; timespec_get(&ts, TIME_UTC); return ts.tv_sec + ts.tv_nsec * 1e-9; }

static inline void unc_add(uint32_t r) { unc_pos[r] = (uint32_t)n_unc; unc_list[n_unc++] = r; }
static inline void unc_del(uint32_t r) {
    uint32_t p = unc_pos[r]; uint32_t last = unc_list[--n_unc];
    unc_list[p] = last; unc_pos[last] = p;
}
static void unrank(uint64_t r, int *out, int t) {
    int x = V - 1;
    for (int i = t; i >= 1; i--) { while (binom[x][i] > r) x--; out[i - 1] = x; r -= binom[x][i]; x--; }
}
static int gen_subsets(int n, int r, uint8_t (**out)[MAXT]) {
    int total = (int)binom[n][r]; *out = malloc(sizeof(**out) * (total ? total : 1));
    if (r == 0) return 1;
    int idx[MAXT], c = 0; for (int i = 0; i < r; i++) idx[i] = i;
    for (;;) {
        for (int i = 0; i < r; i++) (*out)[c][i] = (uint8_t)idx[i];
        c++;
        int i = r - 1; while (i >= 0 && idx[i] == n - r + i) i--;
        if (i < 0) break;
        idx[i]++; for (int j = i + 1; j < r; j++) idx[j] = idx[j - 1] + 1;
    }
    return c;
}
static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
static void set_mask(int bi) {
    msk[bi][0] = msk[bi][1] = 0;
    for (int i = 0; i < K; i++) msk[bi][pts[bi][i] >> 6] |= 1ULL << (pts[bi][i] & 63);
}
/* rank of t-subset of sorted block given index tuple */
static inline uint64_t rank_idx(const int *blk, const uint8_t *ix, int t) {
    uint64_t r = 0; for (int i = 0; i < t; i++) r += binom[blk[ix[i]]][i + 1]; return r;
}
/* rank of (t-1)-subset of sorted block (index tuple) with x (not in block) inserted */
static inline uint64_t rank_idx_ins(const int *blk, const uint8_t *ix, int m, int x) {
    uint64_t r = 0; int i = 0;
    for (; i < m && blk[ix[i]] < x; i++) r += binom[blk[ix[i]]][i + 1];
    r += binom[x][i + 1];
    for (int j = i; j < m; j++) r += binom[blk[ix[j]]][j + 2];
    return r;
}
/* score all q in block bi for adding p: dq[i] = weighted delta for removing pts[bi][i] (i over block indices) */
static void score_block(int bi, int p, int64_t *dq) {
    const int *blk = pts[bi];
    int64_t loss[MAXK] = {0}, gcont[MAXK] = {0}, gtot = 0;
    for (int s = 0; s < nsubT; s++) {
        uint64_t r = rank_idx(blk, subT[s], T);
        if (cnt[r] == 1) { uint32_t ww = w[r]; for (int i = 0; i < T; i++) loss[subT[s][i]] += ww; }
    }
    for (int s = 0; s < nsubT1; s++) {
        uint64_t r = rank_idx_ins(blk, subT1[s], T - 1, p);
        if (cnt[r] == 0) { uint32_t ww = w[r]; gtot += ww; for (int i = 0; i < T - 1; i++) gcont[subT1[s][i]] += ww; }
    }
    for (int i = 0; i < K; i++) dq[i] = loss[i] - (gtot - gcont[i]);
}
static void apply_move(int bi, int qi, int p) {
    int *blk = pts[bi]; int q = blk[qi];
    /* remove q: t-subsets of block containing index qi */
    for (int s = 0; s < nsubT; s++) {
        int has = 0; for (int i = 0; i < T; i++) if (subT[s][i] == qi) has = 1;
        if (!has) continue;
        uint64_t r = rank_idx(blk, subT[s], T);
        if (--cnt[r] == 0) unc_add((uint32_t)r);
    }
    int nb[MAXK], j = 0, placed = 0;
    for (int i = 0; i < K; i++) { if (i == qi) continue; if (!placed && p < blk[i]) { nb[j++] = p; placed = 1; } nb[j++] = blk[i]; }
    if (!placed) nb[j++] = p;
    memcpy(blk, nb, sizeof(int) * K); set_mask(bi);
    int pi = 0; while (blk[pi] != p) pi++;
    for (int s = 0; s < nsubT; s++) {
        int has = 0; for (int i = 0; i < T; i++) if (subT[s][i] == pi) has = 1;
        if (!has) continue;
        uint64_t r = rank_idx(blk, subT[s], T);
        if (cnt[r]++ == 0) unc_del((uint32_t)r);
    }
    (void)q;
}
static void write_blocks(const char *path, int (*P)[MAXK]) {
    FILE *f = fopen(path, "wb"); if (!f) { perror(path); return; }
    for (int b = 0; b < B; b++) for (int i = 0; i < K; i++) fprintf(f, "%d%c", P[b][i] + 1, i == K - 1 ? '\n' : ' ');
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: covsearch2 v k t b seconds seed outfile [init|-] [tenure] [maxw]\n"); return 2; }
    V = atoi(argv[1]); K = atoi(argv[2]); T = atoi(argv[3]); B = atoi(argv[4]);
    double secs = atof(argv[5]); uint64_t seed = strtoull(argv[6], 0, 10); const char *out = argv[7];
    const char *init = argc > 8 ? argv[8] : "-";
    int tenure = argc > 9 ? atoi(argv[9]) : 10;
    uint32_t maxw = argc > 10 ? (uint32_t)atoi(argv[10]) : 1000000;
    double pnoise = argc > 11 ? atof(argv[11]) : 1.0;
    int maxcand = argc > 12 ? atoi(argv[12]) : 0;
    if (V > MAXV || K >= MAXK || T >= MAXT || T < 2 || B > MAXB || K > V || T > K) { fprintf(stderr, "bad params\n"); return 2; }
    for (int n = 0; n <= MAXV; n++) { binom[n][0] = 1; for (int r = 1; r <= MAXT; r++) binom[n][r] = n ? binom[n - 1][r - 1] + binom[n - 1][r] : 0; }
    NT = binom[V][T];
    if (NT > 200000000ULL) { fprintf(stderr, "too many t-sets\n"); return 2; }
    s0 = seed * 0x9E3779B97F4A7C15ULL + 1; s1 = (seed + 7) * 0xBF58476D1CE4E5B9ULL + 3;
    for (int i = 0; i < 20; i++) rnd();
    nsubT = gen_subsets(K, T, &subT); nsubT1 = gen_subsets(K, T - 1, &subT1);
    cnt = calloc(NT, sizeof(uint16_t)); w = malloc(NT * 4); unc_list = malloc(NT * 4); unc_pos = malloc(NT * 4);
    if (!cnt || !w || !unc_list || !unc_pos) { fprintf(stderr, "oom\n"); return 2; }
    for (uint64_t r = 0; r < NT; r++) w[r] = 1;
    int nb = 0;
    if (strcmp(init, "-") != 0) {
        FILE *f = fopen(init, "rb"); if (!f) { perror(init); return 2; }
        while (nb < B) {
            int ok = 1;
            for (int i = 0; i < K; i++) { int x; if (fscanf(f, "%d", &x) != 1) { ok = 0; break; } pts[nb][i] = x - 1; }
            if (!ok) break; nb++;
        }
        fclose(f);
    }
    int ninit = nb;
    for (; nb < B; nb++) {
        int perm[MAXV]; for (int i = 0; i < V; i++) perm[i] = i;
        for (int i = 0; i < K; i++) { int j = i + rndn(V - i); int tmp = perm[i]; perm[i] = perm[j]; perm[j] = tmp; pts[nb][i] = perm[i]; }
    }
    for (int b = 0; b < B; b++) {
        qsort(pts[b], K, sizeof(int), cmpint); set_mask(b);
        for (int s = 0; s < nsubT; s++) cnt[rank_idx(pts[b], subT[s], T)]++;
    }
    n_unc = 0;
    for (uint64_t r = 0; r < NT; r++) if (cnt[r] == 0) unc_add((uint32_t)r);
    best_cost = n_unc; memcpy(best_pts, pts, sizeof(int) * MAXK * B);
    printf("start v=%d k=%d t=%d b=%d NT=%llu init_blocks=%d uncovered=%llu tenure=%d seed=%llu\n", V, K, T, B,
           (unsigned long long)NT, ninit, (unsigned long long)n_unc, tenure, (unsigned long long)seed);
    fflush(stdout);
    double t_start = now(), t_last = t_start, t_ck = t_start;
    int64_t step = 0; uint64_t wbumps = 0;
    char bestpath[4096]; snprintf(bestpath, sizeof bestpath, "%s.best", out);
    int64_t dq[MAXK];
    while (n_unc > 0) {
        step++;
        uint64_t r = unc_list[rndn((uint32_t)n_unc)];
        int Tp[MAXT]; unrank(r, Tp, T);
        uint64_t tm0 = 0, tm1 = 0;
        for (int i = 0; i < T; i++) { if (Tp[i] < 64) tm0 |= 1ULL << Tp[i]; else tm1 |= 1ULL << (Tp[i] - 64); }
        int best_in = -1, nc = 0;
        for (int b = 0; b < B; b++) {
            int in = __builtin_popcountll(msk[b][0] & tm0) + __builtin_popcountll(msk[b][1] & tm1);
            if (in > best_in) { best_in = in; nc = 0; }
            if (in == best_in) cand[nc++] = b;
        }
        int64_t bestd = INT64_MAX; int bb = -1, bq = -1, bp = -1, nties = 0;
        if (maxcand > 0 && nc > maxcand) { /* partial shuffle: keep maxcand random candidates */
            for (int c = 0; c < maxcand; c++) { int j = c + rndn(nc - c); int tmp = cand[c]; cand[c] = cand[j]; cand[j] = tmp; }
            nc = maxcand;
        }
        for (int c = 0; c < nc; c++) {
            int bi = cand[c];
            int outs[MAXT], no = 0;
            for (int i = 0; i < T; i++) if (!((msk[bi][Tp[i] >> 6] >> (Tp[i] & 63)) & 1)) outs[no++] = Tp[i];
            int p = outs[rndn(no)];
            score_block(bi, p, dq);
            for (int i = 0; i < K; i++) {
                int x = pts[bi][i];
                if (x < 64 ? ((tm0 >> x) & 1) : ((tm1 >> (x - 64)) & 1)) continue;
                int is_tabu = tabu_until[bi][x] > step;
                int64_t d = dq[i];
                if (is_tabu) continue;
                if (d < bestd) { bestd = d; bb = bi; bq = i; bp = p; nties = 1; }
                else if (d == bestd) { nties++; if (rndn(nties) == 0) { bb = bi; bq = i; bp = p; } }
            }
        }
        if (bb < 0) continue;
        if (bestd >= 0) {
            if (w[r] < maxw) { w[r]++; wbumps++; }
            if (pnoise < 1.0 && (rnd() >> 11) * (1.0 / 9007199254740992.0) >= pnoise) continue;
        }
        int qpt = pts[bb][bq];
        apply_move(bb, bq, bp);
        tabu_until[bb][bp] = step + tenure + rndn(tenure + 1); /* do not remove the new point p from bb soon */
        (void)qpt;
        if (n_unc < best_cost) { best_cost = n_unc; memcpy(best_pts, pts, sizeof(int) * MAXK * B); }
        if ((step & 0x3FF) == 0) {
            double tn = now();
            if (tn - t_last > 10) {
                printf("t=%.0fs steps=%lld rate=%.0f/s wbumps=%llu cur=%llu best=%llu\n", tn - t_start, (long long)step,
                       step / (tn - t_start), (unsigned long long)wbumps, (unsigned long long)n_unc, (unsigned long long)best_cost);
                fflush(stdout); t_last = tn;
            }
            if (tn - t_ck > 60) { write_blocks(bestpath, best_pts); t_ck = tn; }
            if (tn - t_start > secs) break;
        }
    }
    double tn = now();
    printf("end t=%.1fs steps=%lld rate=%.0f/s best=%llu\n", tn - t_start, (long long)step, step / (tn - t_start + 1e-9),
           (unsigned long long)best_cost);
    write_blocks(bestpath, best_pts);
    if (n_unc == 0) { write_blocks(out, pts); printf("FOUND covering with %d blocks -> %s\n", B, out); return 0; }
    return 1;
}
