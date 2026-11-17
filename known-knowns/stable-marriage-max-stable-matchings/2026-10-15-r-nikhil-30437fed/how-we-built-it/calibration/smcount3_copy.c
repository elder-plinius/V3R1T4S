/* smcount3.c (v3 evaluator): counts stable matchings as ideals of the rotation poset.
   1. Man-optimal M0 and woman-optimal Mz by Gale-Shapley.
   2. All rotations by eliminating every exposed rotation along one chain M0 -> Mz (Gusfield & Irving ch. 2-3: the
      cycles of next_M are the rotations exposed in M; exposed rotations are disjoint and stay exposed after
      eliminating another; every rotation is eliminated exactly once along a maximal chain).  Discovery order is a
      linear extension of the rotation poset.
   3. Explicit predecessors (Gusfield & Irving, Section 3.2): rho precedes rho' if (a) rho' contains a pair (m, w) and rho
      moves m to w, or (b) rho' moves m from w_i to w_{i+1} and some woman w strictly between them on m's list is moved
      by rho from a man she likes less than m to a man she likes more than m.  Closed subsets of the transitive closure
      = subsets closed under explicit predecessors.
   4. Number of ideals by a memoised DP over the linear extension: state = (k, I restricted to the bits that later
      rotations' predecessor sets look at).
   Modes: count FILE [cross]   (cross=1 also runs the lattice walk with per-matching stability re-check, n <= 25, and reports agreement)
          climb N SEEDFILE|random RNGSEED SECONDS OUTPREFIX [KICKEVALS] [KMAX]   (iterated local search on the v3 count;
          every new best is cross-checked by the lattice walk when n <= 16)
   n <= 32, rotations <= 496. Written for V3R1T4S lane A, 2026-10-14. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
#define MAXN 32
#define MAXR 496
#define MW 8            /* 8 x 64 = 512 bits >= MAXR */
typedef struct { int n; int mpref[MAXN][MAXN], wpref[MAXN][MAXN], mrank[MAXN][MAXN], wrank[MAXN][MAXN]; } Inst;
typedef struct { uint64_t w[MW]; } Bits;
static inline void bset(Bits *b, int i) { b->w[i >> 6] |= (uint64_t)1 << (i & 63); }
static inline int bsubset(const Bits *a, const Bits *b) { for (int i = 0; i < MW; i++) if (a->w[i] & ~b->w[i]) return 0; return 1; }
static inline void band(Bits *r, const Bits *a, const Bits *b) { for (int i = 0; i < MW; i++) r->w[i] = a->w[i] & b->w[i]; }
static inline void bor(Bits *r, const Bits *a) { for (int i = 0; i < MW; i++) r->w[i] |= a->w[i]; }

static void build_ranks(Inst *I) {
    for (int m = 0; m < I->n; m++) for (int p = 0; p < I->n; p++) I->mrank[m][I->mpref[m][p]] = p;
    for (int w = 0; w < I->n; w++) for (int p = 0; p < I->n; p++) I->wrank[w][I->wpref[w][p]] = p;
}
static int check_perms(const Inst *I) {
    for (int s = 0; s < 2; s++) for (int i = 0; i < I->n; i++) {
        int seen[MAXN] = {0};
        for (int p = 0; p < I->n; p++) { int x = s ? I->wpref[i][p] : I->mpref[i][p]; if (x < 0 || x >= I->n || seen[x]) return 0; seen[x] = 1; }
    }
    return 1;
}
static int read_prefs(const char *path, Inst *I) {
    FILE *f = fopen(path, "r"); if (!f) { perror(path); return 0; }
    char line[8192]; int rows = 0, n = -1; static int grid[2 * MAXN][MAXN];
    while (fgets(line, sizeof line, f)) {
        char *s = line; while (*s == ' ' || *s == '\t') s++;
        if (*s == '#' || *s == '\n' || *s == '\r' || *s == 0) continue;
        int cnt = 0; char *tok = strtok(s, " \t\r\n");
        while (tok) { if (cnt >= MAXN) { fprintf(stderr, "too many entries\n"); fclose(f); return 0; } grid[rows][cnt++] = atoi(tok) - 1; tok = strtok(NULL, " \t\r\n"); }
        if (n < 0) n = cnt; else if (cnt != n) { fprintf(stderr, "ragged row %d\n", rows + 1); fclose(f); return 0; }
        rows++; if (rows > 2 * MAXN) { fprintf(stderr, "too many rows\n"); fclose(f); return 0; }
    }
    fclose(f);
    if (n <= 0 || n > MAXN || rows != 2 * n) { fprintf(stderr, "need 2n rows of n entries, n<=%d (got rows=%d n=%d)\n", MAXN, rows, n); return 0; }
    I->n = n;
    for (int i = 0; i < n; i++) for (int p = 0; p < n; p++) { I->mpref[i][p] = grid[i][p]; I->wpref[i][p] = grid[n + i][p]; }
    if (!check_perms(I)) { fprintf(stderr, "lists must be complete strict permutations\n"); return 0; }
    build_ranks(I); return 1;
}
static void write_prefs(const char *path, const Inst *I, const char *comment) {
    FILE *f = fopen(path, "w"); if (!f) { perror(path); return; }
    if (comment) fprintf(f, "# %s\n", comment);
    for (int i = 0; i < I->n; i++) { for (int p = 0; p < I->n; p++) fprintf(f, "%d%c", I->mpref[i][p] + 1, p + 1 < I->n ? ' ' : '\n'); }
    for (int i = 0; i < I->n; i++) { for (int p = 0; p < I->n; p++) fprintf(f, "%d%c", I->wpref[i][p] + 1, p + 1 < I->n ? ' ' : '\n'); }
    fclose(f);
}
static void gale_shapley(int n, const int pref[MAXN][MAXN], const int rrank[MAXN][MAXN], int *match) {
    int nxt[MAXN] = {0}, held[MAXN], freeq[MAXN], nf = 0;
    for (int i = 0; i < n; i++) { held[i] = -1; match[i] = -1; freeq[nf++] = i; }
    while (nf) {
        int p = freeq[--nf]; int r = pref[p][nxt[p]++]; int h = held[r];
        if (h == -1) { held[r] = p; match[p] = r; }
        else if (rrank[r][p] < rrank[r][h]) { held[r] = p; match[p] = r; match[h] = -1; freeq[nf++] = h; }
        else freeq[nf++] = p;
    }
}
static int is_stable(const Inst *I, const int *M) {
    int n = I->n, Mw[MAXN];
    for (int m = 0; m < n; m++) Mw[M[m]] = m;
    for (int m = 0; m < n; m++) for (int w = 0; w < n; w++)
        if (I->mrank[m][w] < I->mrank[m][M[m]] && I->wrank[w][m] < I->wrank[w][Mw[w]]) return 0;
    return 1;
}
/* ---------- v3: rotation poset + memoised ideal count ---------- */
typedef struct { int r; int men[MAXN]; int wold[MAXN]; int wnew[MAXN]; } Rot;
static Rot rots[MAXR]; static int nrot;
static Bits pred[MAXR], relevant[MAXR + 1];
static int movesto[MAXN][MAXN];        /* movesto[m][w] = rotation moving m to w, or -1 */
static int wmoves[MAXN][MAXR], nwm[MAXN];  /* rotations that move woman w (in chain order) */
/* memo: open addressing on (k, masked I) */
typedef struct { int k; Bits key; uint64_t val; int used; } Memo;
static Memo *memo; static size_t mcap, mcnt;
static uint64_t hash_state(int k, const Bits *b) { uint64_t h = 0x9E3779B97F4A7C15ULL * (uint64_t)(k + 1); for (int i = 0; i < MW; i++) { h ^= b->w[i] + 0x9E3779B97F4A7C15ULL + (h << 6) + (h >> 2); h *= 0xBF58476D1CE4E5B9ULL; } return h ^ (h >> 29); }
static void memo_init(size_t cap) { mcap = cap; mcnt = 0; memo = calloc(cap, sizeof(Memo)); }
static void memo_grow(void);
static Memo *memo_find(int k, const Bits *key, int *found) {
    if (mcnt * 2 >= mcap) memo_grow();
    size_t i = hash_state(k, key) & (mcap - 1);
    while (memo[i].used) { if (memo[i].k == k && memcmp(&memo[i].key, key, sizeof(Bits)) == 0) { *found = 1; return &memo[i]; } i = (i + 1) & (mcap - 1); }
    *found = 0; return &memo[i];
}
static size_t memo_max = 0;   /* MEMO_MAX_STATES env: abort instead of exceeding this many states (memory guard) */
static void memo_grow(void) {
    if (memo_max && mcap >= memo_max) { fprintf(stderr, "memo cap of %zu states reached; aborting (set MEMO_MAX_STATES)\n", memo_max); exit(6); }
    Memo *old = memo; size_t oc = mcap; memo_init(oc * 2);
    for (size_t i = 0; i < oc; i++) if (old[i].used) { int f; Memo *e = memo_find(old[i].k, &old[i].key, &f); *e = old[i]; mcnt++; }
    free(old);
}
static uint64_t count_rec(int k, Bits I) {
    if (k == nrot) return 1;
    Bits key; band(&key, &I, &relevant[k]);
    int found; Memo *e = memo_find(k, &key, &found);
    if (found) return e->val;
    uint64_t res = count_rec(k + 1, I);
    if (bsubset(&pred[k], &I)) { Bits J = I; bset(&J, k); res += count_rec(k + 1, J); }
    e = memo_find(k, &key, &found);          /* table may have grown */
    if (!found) { e->k = k; e->key = key; e->used = 1; mcnt++; }
    e->val = res;
    return res;
}
static long g_states; static int g_verify_chain = 0;
static uint64_t count_poset(const Inst *I) {
    int n = I->n, M[MAXN], Mzw[MAXN], Mz[MAXN], Mw[MAXN], nxt[MAXN], state[MAXN], path[MAXN];
    gale_shapley(n, I->mpref, I->wrank, M);
    gale_shapley(n, I->wpref, I->mrank, Mzw);
    for (int w = 0; w < n; w++) Mz[Mzw[w]] = w;
    nrot = 0;
    for (int m = 0; m < n; m++) { nwm[m] = 0; for (int w = 0; w < n; w++) movesto[m][w] = -1; }
    /* find all rotations along one chain, eliminating all exposed rotations of each matching at once */
    while (1) {
        if (g_verify_chain && !is_stable(I, M)) { fprintf(stderr, "chain matching unstable\n"); exit(4); }
        for (int m = 0; m < n; m++) Mw[M[m]] = m;
        int any = 0;
        for (int m = 0; m < n; m++) {
            nxt[m] = -1;
            int lo = I->mrank[m][M[m]] + 1, hi = I->mrank[m][Mz[m]];
            for (int p = lo; p <= hi; p++) { int w = I->mpref[m][p]; if (I->wrank[w][m] < I->wrank[w][Mw[w]]) { nxt[m] = Mw[w]; break; } }
        }
        for (int m = 0; m < n; m++) state[m] = 0;
        int Mn[MAXN]; memcpy(Mn, M, sizeof(int) * n);
        for (int s = 0; s < n; s++) {
            if (state[s] || nxt[s] == -1) continue;
            int pl = 0, u = s;
            while (u != -1 && state[u] == 0) { state[u] = 1; path[pl++] = u; u = nxt[u]; }
            if (u != -1 && state[u] == 1) {
                int st = 0; while (path[st] != u) st++;
                int len = pl - st;
                if (nrot >= MAXR) { fprintf(stderr, "too many rotations\n"); exit(4); }
                Rot *R = &rots[nrot]; R->r = len;
                for (int i = 0; i < len; i++) {
                    int mi = path[st + i], mn = path[st + (i + 1) % len];
                    R->men[i] = mi; R->wold[i] = M[mi]; R->wnew[i] = M[mn];
                    Mn[mi] = M[mn];
                    movesto[mi][M[mn]] = nrot;
                    int w = M[mn]; wmoves[w][nwm[w]++] = nrot;   /* woman w moves from mn to mi */
                }
                nrot++; any = 1;
            }
            for (int i = 0; i < pl; i++) state[path[i]] = 2;
        }
        if (!any) break;
        memcpy(M, Mn, sizeof(int) * n);
    }
    for (int m = 0; m < n; m++) if (M[m] != Mz[m]) { fprintf(stderr, "chain did not end at the woman-optimal matching\n"); exit(4); }
    /* explicit predecessors */
    for (int r = 0; r < nrot; r++) {
        memset(&pred[r], 0, sizeof(Bits));
        Rot *R = &rots[r];
        for (int i = 0; i < R->r; i++) {
            int m = R->men[i], wi = R->wold[i], wn = R->wnew[i];
            int a = movesto[m][wi]; if (a >= 0 && a != r) bset(&pred[r], a);              /* rule (a): m was moved to wi by a */
            for (int p = I->mrank[m][wi] + 1; p < I->mrank[m][wn]; p++) {                /* rule (b) */
                int w = I->mpref[m][p];
                for (int q = 0; q < nwm[w]; q++) {
                    int s = wmoves[w][q]; Rot *S = &rots[s]; int j; for (j = 0; j < S->r; j++) if (S->wnew[j] == w) break;
                    int mold = S->men[(j + 1) % S->r], mnew = S->men[j];   /* w moves from mold to mnew */
                    if (I->wrank[w][mold] > I->wrank[w][m] && I->wrank[w][mnew] < I->wrank[w][m]) { if (s != r) bset(&pred[r], s); break; }
                }
            }
        }
        for (int b = r; b < MAXR; b++) if (pred[r].w[b >> 6] & ((uint64_t)1 << (b & 63))) { fprintf(stderr, "predecessor %d of rotation %d is not earlier in the chain\n", b, r); exit(4); }
    }
    /* relevant masks: suffix union of pred, restricted to bits < k (pred bits are always < their rotation) */
    memset(&relevant[nrot], 0, sizeof(Bits));
    for (int k = nrot - 1; k >= 0; k--) { relevant[k] = relevant[k + 1]; bor(&relevant[k], &pred[k]); }
    for (int k = 0; k <= nrot; k++) for (int b = k; b < MAXR; b++) relevant[k].w[b >> 6] &= ~((uint64_t)1 << (b & 63));
    if (!memo) { memo_init(1 << 14); const char *e = getenv("MEMO_MAX_STATES"); if (e) memo_max = (size_t)atol(e); }
    memset(memo, 0, mcap * sizeof(Memo)); mcnt = 0;
    Bits I0; memset(&I0, 0, sizeof I0);
    uint64_t c = count_rec(0, I0);
    g_states = (long)mcnt;
    return c;
}
/* ---------- lattice walk (n <= 16) for cross-checks ---------- */
typedef struct { uint64_t *k; size_t cap, cnt; } HSet;
static const uint64_t EMPTY = ~(uint64_t)0;
static uint64_t mix(uint64_t x) { x += 0x9E3779B97F4A7C15ULL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL; x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL; return x ^ (x >> 31); }
static void hs_init(HSet *h, size_t cap) { h->cap = cap; h->cnt = 0; h->k = malloc(cap * 8); for (size_t i = 0; i < cap; i++) h->k[i] = EMPTY; }
static int hs_insert(HSet *h, uint64_t key);
static void hs_grow(HSet *h) { HSet g; hs_init(&g, h->cap * 2); for (size_t i = 0; i < h->cap; i++) if (h->k[i] != EMPTY) hs_insert(&g, h->k[i]); free(h->k); *h = g; }
static int hs_insert(HSet *h, uint64_t key) {
    if (h->cnt * 2 >= h->cap) hs_grow(h);
    size_t i = mix(key) & (h->cap - 1);
    while (h->k[i] != EMPTY) { if (h->k[i] == key) return 0; i = (i + 1) & (h->cap - 1); }
    h->k[i] = key; h->cnt++; return 1;
}
static long count_lattice(const Inst *I, int verify) {
    int n = I->n; if (n > 16) return -1;
    int M0[MAXN], Mzw[MAXN], Mz[MAXN];
    gale_shapley(n, I->mpref, I->wrank, M0); gale_shapley(n, I->wpref, I->mrank, Mzw);
    for (int w = 0; w < n; w++) Mz[Mzw[w]] = w;
    HSet hs; hs_init(&hs, 1 << 12);
    size_t scap = 1 << 12, sn = 0; uint64_t *stack = malloc(scap * 8);
    uint64_t k0 = 0; for (int m = 0; m < n; m++) k0 |= (uint64_t)M0[m] << (4 * m);
    hs_insert(&hs, k0); stack[sn++] = k0;
    int M[MAXN], Mw[MAXN], nxt[MAXN], state[MAXN], path[MAXN], M2[MAXN];
    while (sn) {
        uint64_t key = stack[--sn]; for (int m = 0; m < n; m++) M[m] = (int)((key >> (4 * m)) & 15);
        if (verify && !is_stable(I, M)) { fprintf(stderr, "lattice walk produced an unstable matching\n"); exit(3); }
        for (int m = 0; m < n; m++) Mw[M[m]] = m;
        for (int m = 0; m < n; m++) {
            nxt[m] = -1; int lo = I->mrank[m][M[m]] + 1, hi = I->mrank[m][Mz[m]];
            for (int p = lo; p <= hi; p++) { int w = I->mpref[m][p]; if (I->wrank[w][m] < I->wrank[w][Mw[w]]) { nxt[m] = Mw[w]; break; } }
        }
        for (int m = 0; m < n; m++) state[m] = 0;
        for (int s = 0; s < n; s++) {
            if (state[s] || nxt[s] == -1) continue;
            int pl = 0, u = s;
            while (u != -1 && state[u] == 0) { state[u] = 1; path[pl++] = u; u = nxt[u]; }
            if (u != -1 && state[u] == 1) {
                int st = 0; while (path[st] != u) st++;
                int len = pl - st; memcpy(M2, M, sizeof(int) * n);
                for (int i = 0; i < len; i++) M2[path[st + i]] = M[path[st + (i + 1) % len]];
                uint64_t k2 = 0; for (int m = 0; m < n; m++) k2 |= (uint64_t)M2[m] << (4 * m);
                if (hs_insert(&hs, k2)) { if (sn == scap) { scap *= 2; stack = realloc(stack, scap * 8); } stack[sn++] = k2; }
            }
            for (int i = 0; i < pl; i++) state[path[i]] = 2;
        }
    }
    long c = (long)hs.cnt; free(hs.k); free(stack); return c;
}

/* ---------- lattice walk with 128-bit keys (n <= 25, 5 bits per man) ---------- */
typedef unsigned __int128 u128;
typedef struct { u128 *k; unsigned char *used; size_t cap, cnt; } HSet2;
static uint64_t mix2(u128 x) { uint64_t a = (uint64_t)x, b = (uint64_t)(x >> 64); return mix(a ^ (b * 0x9E3779B97F4A7C15ULL)) ^ mix(b + 0x632BE59BD9B4E019ULL); }
static void hs2_init(HSet2 *h, size_t cap) { h->cap = cap; h->cnt = 0; h->k = malloc(cap * sizeof(u128)); h->used = calloc(cap, 1); }
static int hs2_insert(HSet2 *h, u128 key);
static void hs2_grow(HSet2 *h) { HSet2 g; hs2_init(&g, h->cap * 2); for (size_t i = 0; i < h->cap; i++) if (h->used[i]) hs2_insert(&g, h->k[i]); free(h->k); free(h->used); *h = g; }
static int hs2_insert(HSet2 *h, u128 key) {
    if (h->cnt * 2 >= h->cap) hs2_grow(h);
    size_t i = mix2(key) & (h->cap - 1);
    while (h->used[i]) { if (h->k[i] == key) return 0; i = (i + 1) & (h->cap - 1); }
    h->k[i] = key; h->used[i] = 1; h->cnt++; return 1;
}
static long count_lattice25(const Inst *I, int verify) {
    int n = I->n; if (n > 25) return -1;
    int M0[MAXN], Mzw[MAXN], Mz[MAXN];
    gale_shapley(n, I->mpref, I->wrank, M0); gale_shapley(n, I->wpref, I->mrank, Mzw);
    for (int w = 0; w < n; w++) Mz[Mzw[w]] = w;
    HSet2 hs; hs2_init(&hs, 1 << 16);
    size_t scap = 1 << 16, sn = 0; u128 *stack = malloc(scap * sizeof(u128));
    u128 k0 = 0; for (int m = 0; m < n; m++) k0 |= (u128)M0[m] << (5 * m);
    hs2_insert(&hs, k0); stack[sn++] = k0;
    int M[MAXN], Mw[MAXN], nxt[MAXN], state[MAXN], path[MAXN], M2[MAXN];
    while (sn) {
        u128 key = stack[--sn]; for (int m = 0; m < n; m++) M[m] = (int)((key >> (5 * m)) & 31);
        if (verify && !is_stable(I, M)) { fprintf(stderr, "lattice walk produced an unstable matching\n"); exit(3); }
        for (int m = 0; m < n; m++) Mw[M[m]] = m;
        for (int m = 0; m < n; m++) {
            nxt[m] = -1; int lo = I->mrank[m][M[m]] + 1, hi = I->mrank[m][Mz[m]];
            for (int p = lo; p <= hi; p++) { int w = I->mpref[m][p]; if (I->wrank[w][m] < I->wrank[w][Mw[w]]) { nxt[m] = Mw[w]; break; } }
        }
        for (int m = 0; m < n; m++) state[m] = 0;
        for (int s = 0; s < n; s++) {
            if (state[s] || nxt[s] == -1) continue;
            int pl = 0, u = s;
            while (u != -1 && state[u] == 0) { state[u] = 1; path[pl++] = u; u = nxt[u]; }
            if (u != -1 && state[u] == 1) {
                int st = 0; while (path[st] != u) st++;
                int len = pl - st; memcpy(M2, M, sizeof(int) * n);
                for (int i = 0; i < len; i++) M2[path[st + i]] = M[path[st + (i + 1) % len]];
                u128 k2 = 0; for (int m = 0; m < n; m++) k2 |= (u128)M2[m] << (5 * m);
                if (hs2_insert(&hs, k2)) { if (sn == scap) { scap *= 2; stack = realloc(stack, scap * sizeof(u128)); } stack[sn++] = k2; }
            }
            for (int i = 0; i < pl; i++) state[path[i]] = 2;
        }
    }
    long c = (long)hs.cnt; free(hs.k); free(hs.used); free(stack); return c;
}

/* ---------- reverse search over ideals (no visited set): parent(I) = I minus its max-index element ---------- */
static uint64_t rs_count, rs_unstable; static int rs_n; static const Inst *rs_I; static int rs_M[MAXN];
static void rs_dfs(Bits *J, int maxidx) {
    rs_count++;
    if (!is_stable(rs_I, rs_M)) rs_unstable++;
    for (int r = maxidx + 1; r < nrot; r++) {
        if (!bsubset(&pred[r], J)) continue;
        Rot *R = &rots[r];
        for (int i = 0; i < R->r; i++) rs_M[R->men[i]] = R->wnew[i];
        bset(J, r);
        rs_dfs(J, r);
        J->w[r >> 6] &= ~((uint64_t)1 << (r & 63));
        for (int i = 0; i < R->r; i++) rs_M[R->men[i]] = R->wold[i];
    }
}
static uint64_t enumerate_verified(const Inst *I) {
    g_verify_chain = 1; uint64_t dp = count_poset(I); g_verify_chain = 0;
    rs_I = I; rs_n = I->n; rs_count = 0; rs_unstable = 0;
    gale_shapley(rs_n, I->mpref, I->wrank, rs_M);
    Bits J; memset(&J, 0, sizeof J);
    rs_dfs(&J, -1);
    printf("count_poset: %llu\nenumerated_ideals: %llu\nunstable_matchings_found: %llu\n", (unsigned long long)dp, (unsigned long long)rs_count, (unsigned long long)rs_unstable);
    return rs_count;
}
/* ---------- search ---------- */
static uint64_t rs;
static uint64_t rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 0x2545F4914F6CDD1DULL; }
static int rndint(int k) { return (int)(rnd() % (uint64_t)k); }
static void random_inst(Inst *I, int n) {
    I->n = n;
    for (int s = 0; s < 2; s++) for (int i = 0; i < n; i++) {
        int *L = s ? I->wpref[i] : I->mpref[i];
        for (int p = 0; p < n; p++) L[p] = p;
        for (int p = n - 1; p > 0; p--) { int j = rndint(p + 1); int t = L[p]; L[p] = L[j]; L[j] = t; }
    }
    build_ranks(I);
}
static double now_s(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
static void random_move(Inst *I) {
    int n = I->n, side = rndint(2), i = rndint(n);
    int *L = side ? I->wpref[i] : I->mpref[i];
    int a, b;
    if (rndint(10) < 7) { a = rndint(n - 1); b = a + 1; } else { a = rndint(n); do { b = rndint(n); } while (b == a); }
    int t = L[a]; L[a] = L[b]; L[b] = t;
    build_ranks(I);
}
int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "count")) {
        Inst I; if (!read_prefs(argv[2], &I)) return 2;
        int cross = argc >= 4 ? atoi(argv[3]) : 0;
        double t0 = now_s(); uint64_t c = count_poset(&I); double t1 = now_s();
        printf("file: %s\nn: %d\nrotations: %d\nmemo_states: %ld\ncount_poset: %llu\nseconds_poset: %.4f\n", argv[2], I.n, nrot, g_states, (unsigned long long)c, t1 - t0);
        if (cross && I.n <= 25) { double t2 = now_s(); long L = I.n <= 16 ? count_lattice(&I, 1) : count_lattice25(&I, 1); double t3 = now_s(); printf("count_lattice_verified: %ld\nseconds_lattice: %.4f\nagree: %s\n", L, t3 - t2, (uint64_t)L == c ? "yes" : "NO"); if ((uint64_t)L != c) return 5; }
        return 0;
    }
    if (argc >= 7 && !strcmp(argv[1], "climb")) {
        int n = atoi(argv[2]); const char *seedfile = argv[3]; uint64_t seed = strtoull(argv[4], 0, 10);
        double secs = atof(argv[5]); const char *out = argv[6]; long kick = argc >= 8 ? atol(argv[7]) : 3000; int kmax = argc >= 9 ? atoi(argv[8]) : 1;
        rs = seed * 0x9E3779B97F4A7C15ULL + 12345; for (int i = 0; i < 10; i++) rnd();
        Inst cur, best, cand;
        if (!strcmp(seedfile, "random")) random_inst(&cur, n); else { if (!read_prefs(seedfile, &cur)) return 2; if (cur.n != n) { fprintf(stderr, "seed file order %d != %d\n", cur.n, n); return 2; } }
        uint64_t curc = count_poset(&cur), bestc = curc; best = cur;
        char bpath[1024], lpath[1024]; snprintf(bpath, sizeof bpath, "%s.best.prefs", out); snprintf(lpath, sizeof lpath, "%s.log", out);
        FILE *lf = fopen(lpath, "a"); if (!lf) { perror(lpath); return 2; }
        char cm[256]; snprintf(cm, sizeof cm, "best so far: n=%d count=%llu seed=%llu start=%s", n, (unsigned long long)bestc, (unsigned long long)seed, seedfile);
        write_prefs(bpath, &best, cm);
        double t0 = now_s(), tlast = t0; long evals = 0, since_best = 0, kicks = 0, accepted = 0;
        fprintf(lf, "start v3 n=%d seed=%llu start=%s secs=%.0f initial_count=%llu kick=%ld kmax=%d\n", n, (unsigned long long)seed, seedfile, secs, (unsigned long long)curc, kick, kmax); fflush(lf);
        printf("start v3 n=%d seed=%llu start=%s initial_count=%llu\n", n, (unsigned long long)seed, seedfile, (unsigned long long)curc); fflush(stdout);
        while (1) {
            double t = now_s(); if (t - t0 >= secs) break;
            if (t - tlast >= 10.0) { tlast = t; fprintf(lf, "t=%.0f evals=%ld accepted=%ld kicks=%ld cur=%llu best=%llu rate=%.1f/s\n", t - t0, evals, accepted, kicks, (unsigned long long)curc, (unsigned long long)bestc, evals / (t - t0)); fflush(lf); }
            cand = cur; random_move(&cand); uint64_t c = count_poset(&cand); evals++;
            if (c >= curc) {
                if (c > curc) since_best = 0; else since_best++;
                cur = cand; curc = c; accepted++;
                if (c > bestc) {
                    long L = count_lattice(&cur, 0);
                    if (L >= 0 && (uint64_t)L != c) { fprintf(lf, "MISMATCH poset=%llu lattice=%ld at evals=%ld; keeping lattice value\n", (unsigned long long)c, L, evals); fflush(lf); c = (uint64_t)L; curc = c; if (c <= bestc) continue; }
                    bestc = c; best = cur; snprintf(cm, sizeof cm, "best so far: n=%d count=%llu seed=%llu start=%s evals=%ld t=%.0f", n, (unsigned long long)bestc, (unsigned long long)seed, seedfile, evals, now_s() - t0); write_prefs(bpath, &best, cm); fprintf(lf, "NEWBEST t=%.0f evals=%ld best=%llu (lattice cross-check %s)\n", now_s() - t0, evals, (unsigned long long)bestc, L >= 0 ? "ok" : "n/a"); fflush(lf);
                }
            } else since_best++;
            if (since_best >= kick) { cur = best; int k = 1 + rndint(kmax); for (int i = 0; i < k; i++) random_move(&cur); curc = count_poset(&cur); evals++; since_best = 0; kicks++; }
        }
        double el = now_s() - t0;
        fprintf(lf, "end t=%.0f evals=%ld accepted=%ld kicks=%ld cur=%llu best=%llu rate=%.1f/s\n", el, evals, accepted, kicks, (unsigned long long)curc, (unsigned long long)bestc, evals / el); fclose(lf);
        printf("end n=%d seed=%llu evals=%ld best=%llu rate=%.1f/s best_file=%s\n", n, (unsigned long long)seed, evals, (unsigned long long)bestc, evals / el, bpath);
        return 0;
    }


    if (argc >= 3 && !strcmp(argv[1], "enumerate")) {
        /* enumerate FILE: reverse-search enumeration of every ideal, converting each to its matching incrementally and
           re-checking it against the stability definition; prints the DP count, the enumerated count and the number of
           unstable matchings met (must be 0). Memory O(rotations); time O(ideals x rotations). */
        Inst I; if (!read_prefs(argv[2], &I)) return 2;
        double t0 = now_s(); uint64_t e = enumerate_verified(&I); double t1 = now_s();
        printf("n: %d\nrotations: %d\nseconds_enumerate: %.2f\nagree: %s\n", I.n, nrot, t1 - t0, (e == count_poset(&I) && rs_unstable == 0) ? "yes" : "NO");
        return (e == count_poset(&I) && rs_unstable == 0) ? 0 : 5;
    }
    if (argc >= 9 && !strcmp(argv[1], "anneal")) {
        /* anneal N SEEDFILE|random RNGSEED SECONDS OUTPREFIX T0 TEND [NCYCLES]: Metropolis on ln(count), geometric
           cooling T0 -> TEND inside each cycle, each cycle restarts from the best; new bests cross-checked (n <= 16). */
        int n = atoi(argv[2]); const char *seedfile = argv[3]; uint64_t seed = strtoull(argv[4], 0, 10);
        double secs = atof(argv[5]); const char *out = argv[6]; double T0 = atof(argv[7]), TEND = atof(argv[8]); int ncyc = argc >= 10 ? atoi(argv[9]) : 6;
        rs = seed * 0x9E3779B97F4A7C15ULL + 777; for (int i = 0; i < 10; i++) rnd();
        Inst cur, best, cand;
        if (!strcmp(seedfile, "random")) random_inst(&cur, n); else { if (!read_prefs(seedfile, &cur)) return 2; if (cur.n != n) { fprintf(stderr, "seed file order %d != %d\n", cur.n, n); return 2; } }
        uint64_t curc = count_poset(&cur), bestc = curc; best = cur;
        char bpath[1024], lpath[1024]; snprintf(bpath, sizeof bpath, "%s.best.prefs", out); snprintf(lpath, sizeof lpath, "%s.log", out);
        FILE *lf = fopen(lpath, "a"); if (!lf) { perror(lpath); return 2; }
        char cm[256]; snprintf(cm, sizeof cm, "best so far: n=%d count=%llu seed=%llu start=%s (anneal)", n, (unsigned long long)bestc, (unsigned long long)seed, seedfile);
        write_prefs(bpath, &best, cm);
        double t0 = now_s(), tlast = t0, cyc = secs / ncyc; long evals = 0, accepted = 0, worse = 0; int cycle = 0;
        fprintf(lf, "start anneal n=%d seed=%llu start=%s secs=%.0f initial_count=%llu T0=%g TEND=%g ncycles=%d\n", n, (unsigned long long)seed, seedfile, secs, (unsigned long long)curc, T0, TEND, ncyc); fflush(lf);
        printf("start anneal n=%d seed=%llu start=%s initial_count=%llu\n", n, (unsigned long long)seed, seedfile, (unsigned long long)curc); fflush(stdout);
        while (1) {
            double t = now_s(), el = t - t0; if (el >= secs) break;
            int c_now = (int)(el / cyc); if (c_now != cycle) { cycle = c_now; cur = best; curc = bestc; fprintf(lf, "cycle %d restart from best=%llu\n", cycle, (unsigned long long)bestc); }
            double frac = (el - cycle * cyc) / cyc; double T = T0 * pow(TEND / T0, frac);
            if (t - tlast >= 10.0) { tlast = t; fprintf(lf, "t=%.0f evals=%ld accepted=%ld worse_accepted=%ld T=%.4f cur=%llu best=%llu rate=%.1f/s\n", el, evals, accepted, worse, T, (unsigned long long)curc, (unsigned long long)bestc, evals / el); fflush(lf); }
            cand = cur; random_move(&cand); uint64_t c = count_poset(&cand); evals++;
            int acc = 0;
            if (c >= curc) acc = 1;
            else { double d = (log((double)c) - log((double)curc)) / T; if (d > -40 && (double)(rnd() >> 11) / 9007199254740992.0 < exp(d)) { acc = 1; worse++; } }
            if (acc) {
                cur = cand; curc = c; accepted++;
                if (c > bestc) {
                    long L = count_lattice(&cur, 0);
                    if (L >= 0 && (uint64_t)L != c) { fprintf(lf, "MISMATCH poset=%llu lattice=%ld at evals=%ld; keeping lattice value\n", (unsigned long long)c, L, evals); fflush(lf); c = (uint64_t)L; curc = c; if (c <= bestc) continue; }
                    bestc = c; best = cur; snprintf(cm, sizeof cm, "best so far: n=%d count=%llu seed=%llu start=%s evals=%ld t=%.0f (anneal)", n, (unsigned long long)bestc, (unsigned long long)seed, seedfile, evals, now_s() - t0); write_prefs(bpath, &best, cm); fprintf(lf, "NEWBEST t=%.0f evals=%ld best=%llu (lattice cross-check %s)\n", now_s() - t0, evals, (unsigned long long)bestc, L >= 0 ? "ok" : "n/a"); fflush(lf);
                }
            }
        }
        double el = now_s() - t0;
        fprintf(lf, "end t=%.0f evals=%ld accepted=%ld worse_accepted=%ld cur=%llu best=%llu rate=%.1f/s\n", el, evals, accepted, worse, (unsigned long long)curc, (unsigned long long)bestc, evals / el); fclose(lf);
        printf("end anneal n=%d seed=%llu evals=%ld best=%llu rate=%.1f/s best_file=%s\n", n, (unsigned long long)seed, evals, (unsigned long long)bestc, evals / el, bpath);
        return 0;
    }
    fprintf(stderr, "usage: smcount3 count FILE [cross] | smcount3 enumerate FILE | smcount3 anneal N SEEDFILE|random RNGSEED SECONDS OUTPREFIX T0 TEND [NCYCLES] | smcount3 climb N SEEDFILE|random RNGSEED SECONDS OUTPREFIX [KICKEVALS] [KMAX]\n");
    return 1;
}
