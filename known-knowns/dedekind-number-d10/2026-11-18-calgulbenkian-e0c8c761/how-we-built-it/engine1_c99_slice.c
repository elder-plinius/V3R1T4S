/*
 * engine1_c99_slice.c
 *
 * Independent Implementation 1 for dedekind-number-d10 (partial win p1):
 *   - Language & Arithmetic: Standalone C99 using exact 128-bit unsigned/signed integers
 *     (__uint128_t / __int128). Zero floating-point or modular-CRT arithmetic.
 *   - Burnside Reduction: Un-grouped truncated subgroup-poset Mobius inversion over all
 *     50 subgroups of P_81 = C_3 wr C_3 <= S_9 (evaluates all 27 subgroups of order >= 9
 *     individually without assuming S_9-conjugacy).
 *   - Poset Decomposition:
 *     1. Reproduces exact D(0..7) (and D(8) with --with-d8) via Dedekind B^2 / B^3 interval
 *        lattice formulas, plus D(6..8) mod 9 via C_3^2 <= S_6 subgroup-poset Mobius inversion.
 *     2. Evaluates |Fix_{D_9}(K)| and |Fix_{D_10}(K)| via Dedekind B^k interval formulas on
 *        fixed coordinates combined with Bipartite Galois Downset-Interval Convolution on
 *        Q = Q_L cup Q_U.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

static void print_u128(u128 x) {
    if (x == 0) { putchar('0'); return; }
    char buf[64];
    int n = 0;
    while (x > 0) {
        buf[n++] = (char)('0' + (int)(x % 10));
        x /= 10;
    }
    while (n > 0) putchar(buf[--n]);
}

static void print_i128(i128 x) {
    if (x < 0) { putchar('-'); print_u128((u128)(-x)); }
    else print_u128((u128)x);
}

/* ---------- Part 1: Exact D(0..7) and optional D(8) from Boolean lattice definition ---------- */

static u128 compute_dedekind_small(int n) {
    if (n == 0) return 2;
    if (n == 1) return 3;
    if (n == 2) return 6;
    if (n == 3) return 20;
    if (n == 4) return 168;

    /* Enumerate D_4 (168 monotone functions B^4 -> B as 16-bit masks) */
    uint16_t D4[168];
    int n4 = 0;
    for (int m = 0; m < 65536; m++) {
        bool ok = true;
        for (int x = 0; x < 16 && ok; x++) {
            if ((m >> x) & 1) {
                for (int b = 0; b < 4; b++) {
                    int y = x | (1 << b);
                    if (!((m >> y) & 1)) { ok = false; break; }
                }
            }
        }
        if (ok) D4[n4++] = (uint16_t)m;
    }
    if (n4 != 168) { fprintf(stderr, "D4 count error\n"); exit(1); }

    /* Interval table re[i][j] = |{z in D4 : D4[i] <= z <= D4[j]}| (pointwise: z subseteq? D4 stores upsets, same lattice!) */
    int id4[65536];
    for (int i = 0; i < 65536; i++) id4[i] = -1;
    for (int i = 0; i < n4; i++) id4[D4[i]] = i;

    uint16_t re4[168][168];
    memset(re4, 0, sizeof(re4));
    for (int i = 0; i < n4; i++) {
        for (int j = 0; j < n4; j++) {
            if ((D4[i] & D4[j]) == D4[i]) {
                uint16_t cnt = 0;
                for (int k = 0; k < n4; k++) {
                    if ((D4[i] & D4[k]) == D4[i] && (D4[k] & D4[j]) == D4[k]) cnt++;
                }
                re4[i][j] = cnt;
            }
        }
    }

    if (n == 5) {
        u128 s = 0;
        for (int i = 0; i < n4; i++)
            for (int j = 0; j < n4; j++)
                if ((D4[i] & D4[j]) == D4[i]) s++;
        return s;
    }
    if (n == 6) {
        /* |D_4^{B^2}| = sum_{a <= d in D4} re4[a][d]^2 */
        u128 s = 0;
        for (int i = 0; i < n4; i++)
            for (int j = 0; j < n4; j++)
                if (re4[i][j]) s += (u128)re4[i][j] * (u128)re4[i][j];
        return s;
    }
    if (n == 7) {
        /* |D_4^{B^3}| = sum_{x,y,z in D4} re4[0][x&y&z] * sum_{u >= x|y|z} re4[x|y][u]*re4[x|z][u]*re4[y|z][u] */
        u128 total = 0;
        for (int x = 0; x < n4; x++) {
            for (int y = x; y < n4; y++) {
                int xy_and = id4[D4[x] & D4[y]];
                int xy_or  = id4[D4[x] | D4[y]];
                for (int z = y; z < n4; z++) {
                    u128 mult = (x == y && y == z) ? 1 : (x == y || y == z) ? 3 : 6;
                    int xyz_and = id4[D4[xy_and] & D4[z]];
                    int xyz_or  = id4[D4[xy_or]  | D4[z]];
                    int xz_or   = id4[D4[x] | D4[z]];
                    int yz_or   = id4[D4[y] | D4[z]];
                    u128 bot = re4[0][xyz_and];
                    u128 top_sum = 0;
                    for (int u = xyz_or; u < n4; u++) {
                        if (re4[xyz_or][u]) {
                            top_sum += (u128)re4[xy_or][u] * (u128)re4[xz_or][u] * (u128)re4[yz_or][u];
                        }
                    }
                    total += mult * bot * top_sum;
                }
            }
        }
        return total;
    }
    return 0;
}

/* Exact D(8) via R_6 x D_6 using 4 POSIX threads */
static int16_t id4_g[65536];
static int16_t id5_g[168][168];
static uint32_t *id6_g; /* 7581 * 7581 */
static uint64_t *D6_g;
static uint32_t *dn6_g, *up6_g;
static uint16_t *orb6_g;
static uint32_t R6_rep[17000];
static uint16_t R6_mult[17000];
static int nR6_g = 0;
static uint32_t n6_g = 0;

typedef struct {
    int tid, nthreads;
    u128 part;
} D8Arg;

static inline uint32_t lookup_d6(uint64_t m) {
    int a0 = id4_g[m & 0xFFFFU];
    int a1 = id4_g[(m >> 16) & 0xFFFFU];
    int a2 = id4_g[(m >> 32) & 0xFFFFU];
    int a3 = id4_g[(m >> 48) & 0xFFFFU];
    int lo = id5_g[a0][a1];
    int hi = id5_g[a2][a3];
    return id6_g[(size_t)lo * 7581 + hi];
}

static void *d8_worker(void *arg) {
    D8Arg *a = (D8Arg *)arg;
    u128 sum = 0;
    for (int r = a->tid; r < nR6_g; r += a->nthreads) {
        uint64_t mx = D6_g[R6_rep[r]];
        uint64_t mult_x = R6_mult[r];
        u128 row = 0;
        for (uint32_t j = 0; j < n6_g; j++) {
            uint16_t rj = orb6_g[j];
            if (rj < (uint16_t)r) continue;
            uint64_t my = D6_g[j];
            uint64_t p = (uint64_t)dn6_g[lookup_d6(mx & my)] * (uint64_t)up6_g[lookup_d6(mx | my)];
            row += (rj == (uint16_t)r) ? p : 2 * p;
        }
        sum += (u128)mult_x * row;
    }
    a->part = sum;
    return NULL;
}

static u128 compute_D8_exact(void) {
    uint16_t D4[168]; int n4 = 0;
    memset(id4_g, -1, sizeof(id4_g));
    for (int m = 0; m < 65536; m++) {
        bool ok = true;
        for (int x = 0; x < 16 && ok; x++) if ((m >> x) & 1)
            for (int b = 0; b < 4; b++) if (!((m >> (x | (1 << b))) & 1)) { ok = false; break; }
        if (ok) { id4_g[m] = (int16_t)n4; D4[n4++] = (uint16_t)m; }
    }
    uint32_t D5[7581]; int n5 = 0;
    memset(id5_g, -1, sizeof(id5_g));
    for (int i = 0; i < n4; i++)
        for (int j = 0; j < n4; j++)
            if ((D4[i] & D4[j]) == D4[i]) {
                id5_g[i][j] = (int16_t)n5;
                D5[n5++] = (uint32_t)D4[i] | ((uint32_t)D4[j] << 16);
            }
    id6_g = malloc((size_t)n5 * n5 * sizeof(uint32_t));
    D6_g  = malloc(7828354ULL * sizeof(uint64_t));
    n6_g = 0;
    for (int i = 0; i < n5; i++)
        for (int j = 0; j < n5; j++)
            if ((D5[i] & D5[j]) == D5[i]) {
                id6_g[(size_t)i * n5 + j] = n6_g;
                D6_g[n6_g++] = (uint64_t)D5[i] | ((uint64_t)D5[j] << 32);
            }
    /* Compute dn6_g = |{w in D6 : w subseteq z}| via 2D D5 decomposition:
     * Wait: D6 elements are upsets here (same lattice, bitwise subseteq)!
     * Even without Zeta, 1 Zeta sweep on B^6? Or for D(8) baseline, compute dn6 via 64-bit topological flip!
     * Wait: upsets closed upward -> pred6[x] = supersets of x in B^6!
     */
    uint64_t sup6[64] = {0};
    for (int x = 0; x < 64; x++)
        for (int b = 0; b < 6; b++) if (!((x >> b) & 1)) sup6[x] |= (1ULL << (x | (1 << b)));
    dn6_g = malloc((size_t)n6_g * sizeof(uint32_t));
    for (uint32_t i = 0; i < n6_g; i++) dn6_g[i] = 1;
    for (int x = 63; x >= 0; x--) {
        uint64_t bit = 1ULL << x, req = sup6[x];
        for (uint32_t i = 0; i < n6_g; i++) {
            uint64_t m = D6_g[i];
            if (!(m & bit) && (m & req) == req) dn6_g[lookup_d6(m | bit)] += dn6_g[i];
        }
    }
    up6_g = malloc((size_t)n6_g * sizeof(uint32_t));
    for (uint32_t i = 0; i < n6_g; i++) {
        uint64_t m = D6_g[i], dual = 0;
        for (int x = 0; x < 64; x++) if (!((m >> (63 - x)) & 1)) dual |= (1ULL << x);
        up6_g[i] = dn6_g[lookup_d6(dual)];
    }
    /* Partition D6 into S6-orbits via BFS under 5 adjacent transpositions (b, b+1) */
    orb6_g = malloc((size_t)n6_g * sizeof(uint16_t));
    for (uint32_t i = 0; i < n6_g; i++) orb6_g[i] = UINT16_MAX;
    uint8_t swap_map[5][64];
    for (int b = 0; b < 5; b++) {
        for (int x = 0; x < 64; x++) {
            int bit0 = (x >> b) & 1, bit1 = (x >> (b + 1)) & 1;
            int y = x & ~(3 << b);
            y |= (bit0 << (b + 1)) | (bit1 << b);
            swap_map[b][x] = (uint8_t)y;
        }
    }
    /* Fast byte-lookup table for applying swap_map[b] to 64-bit mask! */
    uint64_t byte_lut[5][8][256];
    for (int b = 0; b < 5; b++)
        for (int by = 0; by < 8; by++)
            for (int v = 0; v < 256; v++) {
                uint64_t out = 0;
                for (int bit = 0; bit < 8; bit++) if ((v >> bit) & 1) out |= (1ULL << swap_map[b][by * 8 + bit]);
                byte_lut[b][by][v] = out;
            }
    uint32_t q[720];
    nR6_g = 0;
    for (uint32_t i = 0; i < n6_g; i++) if (orb6_g[i] == UINT16_MAX) {
        uint16_t oid = (uint16_t)nR6_g;
        orb6_g[i] = oid;
        q[0] = i; int qh = 0, qt = 1;
        while (qh < qt) {
            uint64_t m = D6_g[q[qh++]];
            for (int b = 0; b < 5; b++) {
                uint64_t nm = byte_lut[b][0][m & 0xFF] | byte_lut[b][1][(m >> 8) & 0xFF] |
                              byte_lut[b][2][(m >> 16) & 0xFF] | byte_lut[b][3][(m >> 24) & 0xFF] |
                              byte_lut[b][4][(m >> 32) & 0xFF] | byte_lut[b][5][(m >> 40) & 0xFF] |
                              byte_lut[b][6][(m >> 48) & 0xFF] | byte_lut[b][7][(m >> 56) & 0xFF];
                uint32_t ni = lookup_d6(nm);
                if (orb6_g[ni] == UINT16_MAX) { orb6_g[ni] = oid; q[qt++] = ni; }
            }
        }
        R6_rep[nR6_g] = i;
        R6_mult[nR6_g] = (uint16_t)qt;
        nR6_g++;
    }
    printf("|D_6| = %u, |R_6| = %d\n", n6_g, nR6_g);

    pthread_t th[4];
    D8Arg args[4];
    for (int t = 0; t < 4; t++) { args[t].tid = t; args[t].nthreads = 4; args[t].part = 0; pthread_create(&th[t], NULL, d8_worker, &args[t]); }
    u128 tot = 0;
    for (int t = 0; t < 4; t++) { pthread_join(th[t], NULL); tot += args[t].part; }
    free(orb6_g); free(up6_g); free(dn6_g); free(D6_g); free(id6_g);
    return tot;
}


/* ---------- Part 2: Subgroup-Poset Mobius Inversion on P_81 <= S_9 ---------- */

typedef struct { uint8_t p[9]; } Perm9;

static Perm9 perm_compose(Perm9 a, Perm9 b) {
    Perm9 r;
    for (int i = 0; i < 9; i++) r.p[i] = a.p[b.p[i]];
    return r;
}

static bool perm_eq(Perm9 a, Perm9 b) {
    return memcmp(a.p, b.p, 9) == 0;
}

static int perm_cmp(const void *a, const void *b) {
    return memcmp(((const Perm9 *)a)->p, ((const Perm9 *)b)->p, 9);
}

static Perm9 G81[81];
static int mul81[81][81];
static int inv81[81];

static void build_P81(void) {
    Perm9 gens[4] = {
        {{1,2,0, 3,4,5, 6,7,8}},
        {{0,1,2, 4,5,3, 6,7,8}},
        {{0,1,2, 3,4,5, 7,8,6}},
        {{3,4,5, 6,7,8, 0,1,2}}
    };
    Perm9 id = {{0,1,2,3,4,5,6,7,8}};
    G81[0] = id;
    int cnt = 1, head = 0;
    while (head < cnt) {
        Perm9 cur = G81[head++];
        for (int g = 0; g < 4; g++) {
            Perm9 nxt = perm_compose(cur, gens[g]);
            bool seen = false;
            for (int i = 0; i < cnt; i++) if (perm_eq(G81[i], nxt)) { seen = true; break; }
            if (!seen) G81[cnt++] = nxt;
        }
    }
    if (cnt != 81) { fprintf(stderr, "|P_81| != 81\n"); exit(1); }
    qsort(G81, 81, sizeof(Perm9), perm_cmp);
    for (int i = 0; i < 81; i++) {
        for (int j = 0; j < 81; j++) {
            Perm9 prod = perm_compose(G81[i], G81[j]);
            for (int k = 0; k < 81; k++) {
                if (perm_eq(G81[k], prod)) { mul81[i][j] = k; break; }
            }
            if (mul81[i][j] == 0) inv81[i] = j;
        }
    }
}

typedef struct {
    u128 mask; /* bits 0..80 */
    int order;
} Subgroup;

static u128 close_subgroup(u128 mask) {
    mask |= (u128)1;
    while (1) {
        u128 next = mask;
        for (int i = 0; i < 81; i++) {
            if ((mask >> i) & 1) {
                for (int j = 0; j < 81; j++) {
                    if ((mask >> j) & 1) {
                        next |= ((u128)1 << mul81[i][j]);
                    }
                }
            }
        }
        if (next == mask) return mask;
        mask = next;
    }
}

static int popcount81(u128 m) {
    uint64_t lo = (uint64_t)m;
    uint64_t hi = (uint64_t)(m >> 64);
    return __builtin_popcountll(lo) + __builtin_popcountll(hi);
}

static int sub_cmp(const void *a, const void *b) {
    const Subgroup *sa = (const Subgroup *)a;
    const Subgroup *sb = (const Subgroup *)b;
    if (sa->order != sb->order) return sa->order - sb->order;
    if (sa->mask < sb->mask) return -1;
    if (sa->mask > sb->mask) return 1;
    return 0;
}

/* ---------- Part 3: Bipartite Galois Downset-Interval Evaluator ---------- */

/* Open-addressing hash map for u64 -> uint32_t */
typedef struct {
    uint64_t *keys;
    uint32_t *vals;
    uint32_t cap_mask;
} Hash64;

static void hash64_init(Hash64 *h, uint32_t min_cap) {
    uint32_t cap = 1024;
    while (cap < min_cap * 4) cap <<= 1;
    h->keys = (uint64_t *)malloc((size_t)cap * sizeof(uint64_t));
    h->vals = (uint32_t *)malloc((size_t)cap * sizeof(uint32_t));
    for (uint32_t i = 0; i < cap; i++) h->keys[i] = UINT64_MAX;
    h->cap_mask = cap - 1;
}

static void hash64_free(Hash64 *h) {
    free(h->keys);
    free(h->vals);
}

static inline uint32_t hash64_mix(uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return (uint32_t)x;
}

static inline void hash64_put(Hash64 *h, uint64_t k, uint32_t v) {
    uint32_t idx = hash64_mix(k) & h->cap_mask;
    while (h->keys[idx] != UINT64_MAX && h->keys[idx] != k) {
        idx = (idx + 1) & h->cap_mask;
    }
    h->keys[idx] = k;
    h->vals[idx] = v;
}

static inline uint32_t hash64_get(const Hash64 *h, uint64_t k) {
    uint32_t idx = hash64_mix(k) & h->cap_mask;
    while (h->keys[idx] != k) {
        idx = (idx + 1) & h->cap_mask;
    }
    return h->vals[idx];
}

/* Enumerate all downsets of a poset of size k <= 64 given pred_mask[0..k-1] (topologically sorted) */
typedef struct {
    uint64_t *arr;
    uint32_t count;
    uint32_t cap;
} Vec64;

static void vec64_push(Vec64 *v, uint64_t x) {
    if (v->count == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 1024;
        v->arr = (uint64_t *)realloc(v->arr, (size_t)v->cap * sizeof(uint64_t));
    }
    v->arr[v->count++] = x;
}

static void gen_downsets_rec(int idx, int k, const uint64_t *pred, uint64_t cur, Vec64 *out) {
    if (idx == k) {
        vec64_push(out, cur);
        return;
    }
    gen_downsets_rec(idx + 1, k, pred, cur, out);
    if ((cur & pred[idx]) == pred[idx]) {
        gen_downsets_rec(idx + 1, k, pred, cur | (1ULL << idx), out);
    }
}

/*
 * Given subgroup K (mask over G81), compute BOTH |Fix_{D_9}(K)| = |B^{B^9/K}|
 * and |Fix_{D_10}(K)| = |P_3^{B^9/K}|.
 */

typedef struct {
    int tid, nthreads, n1;
    const uint16_t (*join_id)[1764];
    const uint16_t (*meet_id)[1764];
    const uint16_t (*re)[1764];
    const uint16_t (*up_list)[1764];
    const uint16_t *up_len;
    u128 part;
} L1B3Arg;

static void *l1_b3_worker(void *arg_p) {
    L1B3Arg *a = (L1B3Arg *)arg_p;
    int n1 = a->n1;
    u128 total = 0;
    for (int x = a->tid; x < n1; x += a->nthreads) {
        for (int y = x; y < n1; y++) {
            int xy_and = a->meet_id[x][y];
            int xy_or  = a->join_id[x][y];
            const uint16_t *r_xy = a->re[xy_or];
            for (int z = y; z < n1; z++) {
                uint64_t mult = (x == y && y == z) ? 1ULL : (x == y || y == z) ? 3ULL : 6ULL;
                int xyz_and = a->meet_id[xy_and][z];
                uint64_t bot = a->re[0][xyz_and];
                int xyz_or  = a->join_id[xy_or][z];
                const uint16_t *r_xz = a->re[a->join_id[x][z]];
                const uint16_t *r_yz = a->re[a->join_id[y][z]];
                const uint16_t *ulist = a->up_list[xyz_or];
                int len = a->up_len[xyz_or];
                uint64_t top_s = 0;
                for (int k = 0; k < len; k++) {
                    int u = ulist[k];
                    top_s += (uint64_t)r_xy[u] * r_xz[u] * r_yz[u];
                }
                total += (u128)(mult * bot) * (u128)top_s;
            }
        }
    }
    a->part = total;
    return NULL;
}

static void compute_fix_d9_d10(u128 K_mask, u128 *out_d9, u128 *out_d10) {
    /* First check if K fixes a 3-variable block {0,1,2}, {3,4,5}, or {6,7,8}! */
    int fixed_vars[9], n_fixed = 0;
    int active_vars[9], n_active = 0;
    for (int v = 0; v < 9; v++) {
        bool fixed = true;
        for (int gi = 0; gi < 81; gi++) {
            if (((K_mask >> gi) & 1) && G81[gi].p[v] != v) { fixed = false; break; }
        }
        if (fixed) fixed_vars[n_fixed++] = v;
        else active_vars[n_active++] = v;
    }

    if (n_fixed > 0) {
        /*
         * K fixes 3 variables of {0..8} and acts on n_active == 6 variables.
         * Build Q_32 = (B^6 / K) x B^1 directly from K's action on {active_vars} x {fixed_var_0}!
         * Enumerate its downset lattice L_1 = D(Q_32) (|L_1| = 1,764), then evaluate:
         *   |Fix_{D_9}(K)|  = |L_1^{B^2}| = sum_{a <= d in L_1} |[a, d]_{L_1}|^2
         *   |Fix_{D_10}(K)| = |L_1^{B^3}| via Pawelski's B^3 interval-lattice identity (4 POSIX threads).
         * Zero Birkhoff Zeta sweeps used anywhere!
         */
        int oid7[128];
        memset(oid7, -1, sizeof(oid7));
        int rep7[64], m7 = 0;
        for (int x = 0; x < 128; x++) {
            if (oid7[x] == -1) {
                rep7[m7] = x;
                int b_extra = (x >> 6) & 1;
                for (int gi = 0; gi < 81; gi++) {
                    if ((K_mask >> gi) & 1) {
                        int y = b_extra << 6;
                        for (int t = 0; t < 6; t++) {
                            if ((x >> t) & 1) {
                                int iv = G81[gi].p[active_vars[t]];
                                for (int s = 0; s < 6; s++) if (active_vars[s] == iv) { y |= (1 << s); break; }
                            }
                        }
                        oid7[y] = m7;
                    }
                }
                m7++;
            }
        }
        int ord7[64];
        for (int i = 0; i < m7; i++) ord7[i] = i;
        for (int i = 0; i < m7; i++)
            for (int j = i + 1; j < m7; j++)
                if (__builtin_popcount(rep7[ord7[i]]) > __builtin_popcount(rep7[ord7[j]])) {
                    int t = ord7[i]; ord7[i] = ord7[j]; ord7[j] = t;
                }
        int inv7[64];
        for (int i = 0; i < m7; i++) inv7[ord7[i]] = i;
        uint64_t pred7[64] = {0};
        for (int a = 0; a < m7; a++) {
            int xa = rep7[ord7[a]];
            for (int y = 0; y < 128; y++) {
                if ((xa & y) == xa) {
                    int b = inv7[oid7[y]];
                    if (a < b) pred7[b] |= (1ULL << a);
                }
            }
        }
        Vec64 L1 = {NULL, 0, 0};
        gen_downsets_rec(0, m7, pred7, 0, &L1);
        int n1 = (int)L1.count;
        if (n1 != 1764) { fprintf(stderr, "Expected |L1|=1764, got %d\n", n1); exit(1); }

        Hash64 h1;
        hash64_init(&h1, (uint32_t)n1);
        for (int i = 0; i < n1; i++) hash64_put(&h1, L1.arr[i], (uint32_t)i);

        uint16_t (*join_id)[1764] = calloc((size_t)n1, sizeof(*join_id));
        uint16_t (*meet_id)[1764] = calloc((size_t)n1, sizeof(*meet_id));
        uint16_t (*re)[1764]      = calloc((size_t)n1, sizeof(*re));
        uint16_t (*up_list)[1764] = calloc((size_t)n1, sizeof(*up_list));
        uint16_t *up_len          = calloc((size_t)n1, sizeof(uint16_t));

        for (int i = 0; i < n1; i++) {
            for (int j = 0; j < n1; j++) {
                join_id[i][j] = (uint16_t)hash64_get(&h1, L1.arr[i] | L1.arr[j]);
                meet_id[i][j] = (uint16_t)hash64_get(&h1, L1.arr[i] & L1.arr[j]);
            }
        }
        u128 d9 = 0;
        for (int i = 0; i < n1; i++) {
            for (int j = 0; j < n1; j++) {
                if ((L1.arr[i] & L1.arr[j]) == L1.arr[i]) {
                    uint16_t c = 0;
                    for (int k = 0; k < n1; k++)
                        if ((L1.arr[i] & L1.arr[k]) == L1.arr[i] && (L1.arr[k] & L1.arr[j]) == L1.arr[k]) c++;
                    re[i][j] = c;
                    up_list[i][up_len[i]++] = (uint16_t)j;
                    d9 += (u128)c * (u128)c;
                }
            }
        }

        pthread_t th[4];
        L1B3Arg args[4];
        for (int t = 0; t < 4; t++) {
            args[t] = (L1B3Arg){t, 4, n1, join_id, meet_id, re, up_list, up_len, 0};
            pthread_create(&th[t], NULL, l1_b3_worker, &args[t]);
        }
        u128 d10 = 0;
        for (int t = 0; t < 4; t++) {
            pthread_join(th[t], NULL);
            d10 += args[t].part;
        }

        free(up_len); free(up_list); free(re); free(meet_id); free(join_id);
        hash64_free(&h1); free(L1.arr);
        *out_d9 = d9;
        *out_d10 = d10;
        return;
    }

    /*
     * Case n_fixed == 0: Build Q = B^9 / K (m <= 96 elements).
     * Choose a clean order ideal Q_L of size <= 48!
     * How? Check if any 3-variable block b in {0,1,2} is K-invariant (so wt(block b) in {0..3} is well-defined on orbits)!
     * If so, Q_L = {orbits with wt(block b) <= 1} (size <= 48, boundary <= 24)!
     * Otherwise, m <= 64 (actually m in {24, 28, 32, 60, 64}) and |D(Q)| <= 207,471, so Q_L = {rank <= 4} (size <= 32, |D(Q_L)| <= 2,000)!
     */
    int orb_id[512];
    memset(orb_id, -1, sizeof(orb_id));
    int orb_rep[128];
    int m = 0;
    for (int x = 0; x < 512; x++) {
        if (orb_id[x] == -1) {
            orb_rep[m] = x;
            for (int gi = 0; gi < 81; gi++) {
                if ((K_mask >> gi) & 1) {
                    int y = 0;
                    for (int b = 0; b < 9; b++) {
                        if ((x >> b) & 1) y |= (1 << G81[gi].p[b]);
                    }
                    orb_id[y] = m;
                }
            }
            m++;
        }
    }

    /* Check if any 3-block {3*blk, 3*blk+1, 3*blk+2} has invariant weight under K */
    int inv_blk = -1;
    for (int blk = 0; blk < 3; blk++) {
        bool ok = true;
        int mask3 = 7 << (3 * blk);
        for (int x = 0; x < 512 && ok; x++) {
            int w0 = __builtin_popcount(x & mask3);
            int w1 = __builtin_popcount(orb_rep[orb_id[x]] & mask3);
            if (w0 != w1) ok = false;
        }
        if (ok) { inv_blk = blk; break; }
    }

    int side[128]; /* 0 for Q_L, 1 for Q_U */
    for (int i = 0; i < m; i++) {
        int x = orb_rep[i];
        if (inv_blk >= 0) {
            int w = __builtin_popcount(x & (7 << (3 * inv_blk)));
            side[i] = (w <= 1) ? 0 : 1;
        } else {
            int r = __builtin_popcount(x);
            side[i] = (r <= 4) ? 0 : 1;
        }
    }

    /* Partial order le[a][b] on Q */
    bool le[128][128];
    memset(le, 0, sizeof(le));
    for (int a = 0; a < m; a++) {
        int xa = orb_rep[a];
        for (int y = 0; y < 512; y++) {
            if ((xa & y) == xa) le[a][orb_id[y]] = true;
        }
    }

    int QL[64], QU[64], mL = 0, mU = 0;
    /* Sort by total rank so topological order holds */
    for (int r = 0; r <= 9; r++) {
        for (int i = 0; i < m; i++) {
            if (__builtin_popcount(orb_rep[i]) == r) {
                if (side[i] == 0) QL[mL++] = i;
                else QU[mU++] = i;
            }
        }
    }
    if (mL > 60 || mU > 60) { fprintf(stderr, "mL=%d mU=%d > 60\n", mL, mU); exit(1); }

    uint64_t predL[64] = {0}, predU[64] = {0}, cross_req[64] = {0};
    for (int j = 0; j < mL; j++)
        for (int i = 0; i < j; i++)
            if (le[QL[i]][QL[j]]) predL[j] |= (1ULL << i);
    for (int j = 0; j < mU; j++) {
        for (int i = 0; i < j; i++)
            if (le[QU[i]][QU[j]]) predU[j] |= (1ULL << i);
        for (int i = 0; i < mL; i++)
            if (le[QL[i]][QU[j]]) cross_req[j] |= (1ULL << i);
    }

    Vec64 DL = {NULL, 0, 0}, DU = {NULL, 0, 0};
    gen_downsets_rec(0, mL, predL, 0, &DL);
    gen_downsets_rec(0, mU, predU, 0, &DU);

    uint32_t nL = DL.count, nU = DU.count;

    /* Identify boundary B_L = {i in 0..mL-1 : exists j in 0..mU-1 covering QL[i]}
     * Actually even simpler: B_L = union_{j=0..mU-1} direct_cross_req[j], or all bits appearing in minimal cross edges!
     * If x in QL and y in QU with x < y, pick maximal chain x = z_0 < ... < z_s < z_{s+1} <= y with z_s in QL, z_{s+1} in QU.
     * Then z_{s+1} covers z_s in Q, so no w in Q has z_s < w < z_{s+1}.
     */
    uint64_t BL_mask = 0;
    uint64_t cov_cross[64] = {0};
    for (int j = 0; j < mU; j++) {
        int y = QU[j];
        for (int i = 0; i < mL; i++) {
            int x = QL[i];
            if (!le[x][y]) continue;
            bool direct = true;
            for (int k = 0; k < m; k++) {
                if (k != x && k != y && le[x][k] && le[k][y]) { direct = false; break; }
            }
            if (direct) {
                cov_cross[j] |= (1ULL << i);
                BL_mask |= (1ULL << i);
            }
        }
    }

    /* Collect all distinct boundary traces T = { (I_L & BL_mask) : I_L in DL } U { (req(I_U) & BL_mask) : I_U in DU } */
    /* Wait: every req(I_U) & BL_mask is a subset of BL_mask; collect traces from DL first! */
    Vec64 T = {NULL, 0, 0};
    Hash64 hT;
    hash64_init(&hT, nL < 4096 ? nL : 4096);
    uint32_t *trL = (uint32_t *)malloc((size_t)nL * sizeof(uint32_t));
    for (uint32_t i = 0; i < nL; i++) {
        uint64_t tm = DL.arr[i] & BL_mask;
        uint32_t hidx = hash64_mix(tm) & hT.cap_mask;
        while (hT.keys[hidx] != UINT64_MAX && hT.keys[hidx] != tm) hidx = (hidx + 1) & hT.cap_mask;
        if (hT.keys[hidx] == UINT64_MAX) {
            uint32_t tid = T.count;
            hT.keys[hidx] = tm;
            hT.vals[hidx] = tid;
            vec64_push(&T, tm);
            trL[i] = tid;
        } else {
            trL[i] = hT.vals[hidx];
        }
    }

    int32_t *trU = (int32_t *)malloc((size_t)nU * sizeof(int32_t));
    /* Note: for each I_U in DU, its minimal downset in QL is downward-closure of union_{j in I_U} cov_cross[j] in QL!
     * Wait: be careful! Two elements of cov_cross[j] might force a common upper-or-lower element? Only LOWER elements in QL!
     * Since DL[i] is ALREADY downward-closed in QL:
     *   (all QL-predecessors of I_U) subseteq DL[i]  <==>  (union_{j in I_U} cov_cross[j]) subseteq (DL[i] & BL_mask)!!
     * And cov_req = union_{j in I_U} cov_cross[j] is ALWAYS a subset of BL_mask (though not necessarily in T itself)!
     * So collect distinct cov_req masks R_U across I_U in DU as well!
     */
    Vec64 RU = {NULL, 0, 0};
    Hash64 hRU;
    hash64_init(&hRU, nU < 4096 ? nU : 4096);
    for (uint32_t u = 0; u < nU; u++) {
        uint64_t um = DU.arr[u];
        uint64_t rq = 0;
        while (um) {
            int bit = __builtin_ctzll(um);
            rq |= cov_cross[bit];
            um &= um - 1;
        }
        uint32_t hidx = hash64_mix(rq) & hRU.cap_mask;
        while (hRU.keys[hidx] != UINT64_MAX && hRU.keys[hidx] != rq) hidx = (hidx + 1) & hRU.cap_mask;
        if (hRU.keys[hidx] == UINT64_MAX) {
            uint32_t rid = RU.count;
            hRU.keys[hidx] = rq;
            hRU.vals[hidx] = rid;
            vec64_push(&RU, rq);
            trU[u] = (int32_t)rid;
        } else {
            trU[u] = (int32_t)hRU.vals[hidx];
        }
    }

    uint32_t nT = T.count, nRU = RU.count;

    /* D_9 count: sum_{u in DU, i in DL : RU[trU[u]] subseteq T[trL[i]]} 1 */
    uint64_t *freqL = (uint64_t *)calloc(nT, sizeof(uint64_t));
    uint64_t *freqU = (uint64_t *)calloc(nRU, sizeof(uint64_t));
    for (uint32_t i = 0; i < nL; i++) freqL[trL[i]]++;
    for (uint32_t u = 0; u < nU; u++) freqU[trU[u]]++;

    u128 d9 = 0;
    for (uint32_t r = 0; r < nRU; r++) {
        uint64_t rq = RU.arr[r];
        u128 s = 0;
        for (uint32_t t = 0; t < nT; t++) {
            if ((rq & T.arr[t]) == rq) s += freqL[t];
        }
        d9 += (u128)freqU[r] * s;
    }

    /* D_10 count:
     *   cntL[t1 * nT + t2]   = |{(i1 <= i2 in DL) : trL[i1]=t1, trL[i2]=t2}|
     *   cntU[r1 * nRU + r2]  = |{(u1 <= u2 in DU) : trU[u1]=r1, trU[u2]=r2}|
     *   d10 = sum_{r1, r2, t1, t2 : RU[r1] <= T[t1] and RU[r2] <= T[t2]} cntU[r1, r2] * cntL[t1, t2]
     * Computed via 2-step separable matrix product:
     *   M[r1, t2] = sum_{t1 : RU[r1] <= T[t1]} cntL[t1, t2]
     *   d10       = sum_{r1, r2} cntU[r1, r2] * (sum_{t2 : RU[r2] <= T[t2]} M[r1, t2])
     */
    uint64_t *cntL = (uint64_t *)calloc((size_t)nT * nT, sizeof(uint64_t));
    for (uint32_t i1 = 0; i1 < nL; i1++) {
        uint64_t a = DL.arr[i1];
        uint64_t *row = cntL + (size_t)trL[i1] * nT;
        for (uint32_t i2 = i1; i2 < nL; i2++) {
            if ((a & DL.arr[i2]) == a) row[trL[i2]]++;
        }
    }

    uint64_t *cntU = (uint64_t *)calloc((size_t)nRU * nRU, sizeof(uint64_t));
    for (uint32_t u1 = 0; u1 < nU; u1++) {
        uint64_t a = DU.arr[u1];
        uint64_t *row = cntU + (size_t)trU[u1] * nRU;
        for (uint32_t u2 = u1; u2 < nU; u2++) {
            if ((a & DU.arr[u2]) == a) row[trU[u2]]++;
        }
    }

    /* Step A: M[r1, t2] = sum_{t1 : RU[r1] <= T[t1]} cntL[t1, t2] */
    u128 *M = (u128 *)calloc((size_t)nRU * nT, sizeof(u128));
    for (uint32_t r1 = 0; r1 < nRU; r1++) {
        uint64_t rq1 = RU.arr[r1];
        u128 *mrow = M + (size_t)r1 * nT;
        for (uint32_t t1 = 0; t1 < nT; t1++) {
            if ((rq1 & T.arr[t1]) == rq1) {
                const uint64_t *crow = cntL + (size_t)t1 * nT;
                for (uint32_t t2 = 0; t2 < nT; t2++) {
                    mrow[t2] += crow[t2];
                }
            }
        }
    }

    /* Step B: W[r1, r2] = sum_{t2 : RU[r2] <= T[t2]} M[r1, t2], contracted with cntU[r1, r2] */
    /* Precompute compatibility list for each r2 */
    u128 d10 = 0;
    uint32_t *good_t2 = (uint32_t *)malloc((size_t)nT * sizeof(uint32_t));
    for (uint32_t r2 = 0; r2 < nRU; r2++) {
        uint64_t rq2 = RU.arr[r2];
        uint32_t ng = 0;
        for (uint32_t t2 = 0; t2 < nT; t2++) {
            if ((rq2 & T.arr[t2]) == rq2) good_t2[ng++] = t2;
        }
        for (uint32_t r1 = 0; r1 < nRU; r1++) {
            uint64_t cu = cntU[(size_t)r1 * nRU + r2];
            if (!cu) continue;
            const u128 *mrow = M + (size_t)r1 * nT;
            u128 s = 0;
            for (uint32_t g = 0; g < ng; g++) s += mrow[good_t2[g]];
            d10 += (u128)cu * s;
        }
    }

    free(good_t2); free(M); free(cntU); free(cntL);
    free(freqU); free(freqL); free(trU); free(trL);
    hash64_free(&hRU); free(RU.arr); hash64_free(&hT); free(T.arr);
    free(DL.arr); free(DU.arr);
    *out_d9 = d9;
    *out_d10 = d10;
}

/* ---------- Part 4: C_3 x C_3 <= S_6 Check on D(6..8) mod 9 ---------- */

static void verify_c3x2_mod9(void) {
    /* Subgroups of C_3 x C_3 of order >= 3:
     *   1 subgroup of order 9: <(012), (345)> -> coeff -3
     *   4 subgroups of order 3: <(012)>, <(345)>, <(012)(345)>, <(012)(354)> -> coeff +1 each
     */
    /* Compute |Fix_{D_n}(K)| for n=6,7,8:
     *   K_9 = <(012),(345)>: B^6/K_9 = P_4^2 (16 els, 70 downsets)
     *   K_3a = <(012)> (2 conjugates): B^6/K = P_4 x B^3 (32 els, 3490 downsets)
     *   K_3b = <(012)(345)> (2 conjugates): B^6/K = Q_24 (24 els, 1300 downsets? let's compute exact!)
     */
    /* Just embed them in P_81? Wait: for n=6,7,8, build B^6 quotients directly! */
    uint8_t perms[4][6] = {
        {1,2,0, 3,4,5}, /* g1 */
        {0,1,2, 4,5,3}, /* g2 */
        {1,2,0, 4,5,3}, /* g1 g2 */
        {1,2,0, 5,3,4}  /* g1 g2^2 */
    };
    /* Build 3 quotient downset lattices on B^6: K_9, <g1>, <g1 g2> */
    u128 vals[3][3]; /* [sub_type][n - 6] */
    for (int st = 0; st < 3; st++) {
        int orb_id[64];
        memset(orb_id, -1, sizeof(orb_id));
        uint64_t orb_pts[64];
        int m = 0;
        for (int x = 0; x < 64; x++) {
            if (orb_id[x] == -1) {
                uint64_t pts = 0;
                for (int a = 0; a < 3; a++) {
                    for (int b = 0; b < (st == 0 ? 3 : 1); b++) {
                        int y = x;
                        for (int r = 0; r < a; r++) {
                            int ny = 0;
                            uint8_t *p = (st == 2) ? perms[2] : perms[0];
                            for (int v = 0; v < 6; v++) if ((y >> v) & 1) ny |= (1 << p[v]);
                            y = ny;
                        }
                        for (int r = 0; r < b; r++) {
                            int ny = 0;
                            for (int v = 0; v < 6; v++) if ((y >> v) & 1) ny |= (1 << perms[1][v]);
                            y = ny;
                        }
                        orb_id[y] = m;
                        pts |= (1ULL << y);
                    }
                }
                orb_pts[m++] = pts;
            }
        }
        int ord[64];
        for (int i = 0; i < m; i++) ord[i] = i;
        for (int i = 0; i < m; i++)
            for (int j = i + 1; j < m; j++)
                if (__builtin_popcountll(__builtin_ctzll(orb_pts[ord[i]])) > __builtin_popcountll(__builtin_ctzll(orb_pts[ord[j]]))) {
                    int t = ord[i]; ord[i] = ord[j]; ord[j] = t;
                }
        uint64_t spts[64], pred[64] = {0};
        for (int i = 0; i < m; i++) spts[i] = orb_pts[ord[i]];
        for (int j = 0; j < m; j++) {
            int xr = __builtin_ctzll(spts[j]);
            for (int i = 0; i < j; i++) {
                uint64_t pi = spts[i];
                while (pi) {
                    int x0 = __builtin_ctzll(pi);
                    if ((x0 & xr) == x0) { pred[j] |= (1ULL << i); break; }
                    pi &= pi - 1;
                }
            }
        }
        Vec64 L = {NULL, 0, 0};
        gen_downsets_rec(0, m, pred, 0, &L);
        uint32_t nL = L.count;
        vals[st][0] = nL; /* n = 6 */
        /* n = 7: comparable pairs; n = 8: sum |[a, d]|^2! Wait: nL <= 3490, compute |[a,d]| via bitwise! */
        u128 s7 = 0, s8 = 0;
        /* Precompute sub-elements or direct: for nL=3490, O(nL^2) for s7, and for s8 use G(x,y) = down(x&y)*up(x|y)! */
        Hash64 hL;
        hash64_init(&hL, nL);
        uint32_t *dn = (uint32_t *)calloc(nL, sizeof(uint32_t));
        uint32_t *up = (uint32_t *)calloc(nL, sizeof(uint32_t));
        for (uint32_t i = 0; i < nL; i++) hash64_put(&hL, L.arr[i], i);
        for (uint32_t i = 0; i < nL; i++) {
            for (uint32_t j = i; j < nL; j++) {
                if ((L.arr[i] & L.arr[j]) == L.arr[i]) {
                    s7++;
                    dn[j]++;
                    up[i]++;
                }
            }
        }
        for (uint32_t i = 0; i < nL; i++) {
            for (uint32_t j = i; j < nL; j++) {
                u128 p = (u128)dn[hash64_get(&hL, L.arr[i] & L.arr[j])] * (u128)up[hash64_get(&hL, L.arr[i] | L.arr[j])];
                s8 += (i == j) ? p : 2 * p;
            }
        }
        vals[st][1] = s7;
        vals[st][2] = s8;
        free(dn); free(up); hash64_free(&hL); free(L.arr);
    }
    int exp_mod9[3] = {1, 3, 1}; /* D(6)=7828354 (mod 9=1), D(7)=2414682040998 (mod 9=3), D(8)=...7788 (mod 9=1) */
    for (int k = 0; k < 3; k++) {
        i128 comb = 2 * (i128)vals[1][k] + 2 * (i128)vals[2][k] - 3 * (i128)vals[0][k];
        int r = (int)((comb % 9 + 9) % 9);
        if (r != exp_mod9[k]) {
            fprintf(stderr, "C3xC3 mod 9 mismatch at n=%d: got %d expected %d\n", 6 + k, r, exp_mod9[k]);
            exit(1);
        }
    }
    printf("OK [Engine1]: C_3^2 <= S_6 Mobius congruence reproduces D(6..8) mod 9 = (1, 3, 1)\n");
}

int main(int argc, char **argv) {
    bool with_d8 = (argc > 1 && strcmp(argv[1], "--with-d8") == 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    /* 1. Verify D(0..7) */
    const u128 exp_D[8] = {
        2ULL, 3ULL, 6ULL, 20ULL, 168ULL, 7581ULL, 7828354ULL, 2414682040998ULL
    };
    for (int n = 0; n <= 7; n++) {
        u128 got = compute_dedekind_small(n);
        if (got != exp_D[n]) {
            fprintf(stderr, "D(%d) mismatch!\n", n);
            return 1;
        }
    }
    printf("OK [Engine1]: Exact D(0..7) reproduced (2, 3, 6, 20, 168, 7581, 7828354, 2414682040998)\n");
    if (with_d8) {
        u128 got8 = compute_D8_exact();
        u128 exp8 = ((u128)56130437228687ULL * 1000000000ULL) + 557907788ULL;
        if (got8 != exp8) { fprintf(stderr, "D(8) mismatch!\n"); return 1; }
        printf("OK [Engine1]: Exact D(8) = 56130437228687557907788 reproduced via R_6 x D_6\n");
    }

    /* 2. Verify C_3^2 <= S_6 mod 9 on D(6..8) */
    verify_c3x2_mod9();

    /* 3. Build P_81 and all 50 subgroups */
    build_P81();
    Subgroup subs[64];
    int n_sub = 0;
    subs[n_sub++] = (Subgroup){(u128)1, 1};
    for (int head = 0; head < n_sub; head++) {
        u128 hm = subs[head].mask;
        for (int g = 0; g < 81; g++) {
            if (!((hm >> g) & 1)) {
                u128 km = close_subgroup(hm | ((u128)1 << g));
                bool seen = false;
                for (int i = 0; i < n_sub; i++) if (subs[i].mask == km) { seen = true; break; }
                if (!seen) subs[n_sub++] = (Subgroup){km, popcount81(km)};
            }
        }
    }
    qsort(subs, (size_t)n_sub, sizeof(Subgroup), sub_cmp);
    printf("OK [Engine1]: |P_81| = 81, subgroup lattice size = %d\n", n_sub);
    if (n_sub != 50) return 1;

    /* Mobius function on L(P_81) */
    int mu[50][50];
    memset(mu, 0, sizeof(mu));
    for (int i = 0; i < n_sub; i++) {
        mu[i][i] = 1;
        for (int j = i + 1; j < n_sub; j++) {
            if ((subs[i].mask & subs[j].mask) == subs[i].mask) {
                int s = 0;
                for (int k = i; k < j; k++) {
                    if ((subs[i].mask & subs[k].mask) == subs[i].mask &&
                        (subs[k].mask & subs[j].mask) == subs[k].mask) {
                        s += mu[i][k];
                    }
                }
                mu[i][j] = -s;
            }
        }
    }

    /* Compute c_1 (mod 3), c_2 (mod 9), c_3 (mod 27) and verify algebraically on all 50 transitive sets P_81/H0 */
    int c1[50] = {0}, c2[50] = {0}, c3[50] = {0};
    for (int j = 0; j < n_sub; j++) {
        for (int i = 0; i <= j; i++) {
            if ((subs[i].mask & subs[j].mask) == subs[i].mask) {
                if (subs[i].order >= 81 && subs[j].order >= 81) c1[j] += mu[i][j];
                if (subs[i].order >= 27 && subs[j].order >= 27) c2[j] += mu[i][j];
                if (subs[i].order >= 9  && subs[j].order >= 9)  c3[j] += mu[i][j];
            }
        }
    }

    for (int h0 = 0; h0 < n_sub; h0++) {
        int s1 = 0, s2 = 0, s3 = 0;
        for (int j = 0; j < n_sub; j++) {
            if (subs[j].order < 9) continue;
            int cnt_g = 0;
            for (int g = 0; g < 81; g++) {
                int gi = inv81[g];
                bool ok = true;
                for (int k = 0; k < 81; k++) {
                    if ((subs[j].mask >> k) & 1) {
                        int conj = mul81[gi][mul81[k][g]];
                        if (!((subs[h0].mask >> conj) & 1)) { ok = false; break; }
                    }
                }
                if (ok) cnt_g++;
            }
            int fix_cos = cnt_g / subs[h0].order;
            s1 += c1[j] * fix_cos;
            s2 += c2[j] * fix_cos;
            s3 += c3[j] * fix_cos;
        }
        int orb_sz = 81 / subs[h0].order;
        if (((s1 - orb_sz) % 3) != 0 || ((s2 - orb_sz) % 9) != 0 || ((s3 - orb_sz) % 27) != 0) {
            fprintf(stderr, "Algebraic Burnside check failed at h0=%d!\n", h0);
            return 1;
        }
    }
    printf("OK [Engine1]: Truncated Mobius identity verified over Z on all 50 transitive P_81-sets (mod 3, 9, 27)\n");

    /* 4. Evaluate ALL 27 subgroups of order >= 9 individually! */
    u128 fix9[50] = {0}, fix10[50] = {0};
    for (int j = 0; j < n_sub; j++) {
        if (subs[j].order < 9) continue;
        struct timespec s0, s1;
        clock_gettime(CLOCK_MONOTONIC, &s0);
        compute_fix_d9_d10(subs[j].mask, &fix9[j], &fix10[j]);
        clock_gettime(CLOCK_MONOTONIC, &s1);
        double dt = (s1.tv_sec - s0.tv_sec) + 1e-9 * (s1.tv_nsec - s0.tv_nsec);
        printf("  Subgroup %2d (|K|=%2d, c9=%2d, c27=%3d): Fix_D9=", j, subs[j].order, c2[j], c3[j]);
        print_u128(fix9[j]);
        printf("  Fix_D10=");
        print_u128(fix10[j]);
        printf("  (%.3fs)\n", dt);
    }

    i128 tot9_m3 = 0, tot9_m9 = 0, tot9_m27 = 0;
    i128 tot10_m3 = 0, tot10_m9 = 0, tot10_m27 = 0;
    for (int j = 0; j < n_sub; j++) {
        if (subs[j].order < 9) continue;
        tot9_m3   += (i128)c1[j] * (i128)fix9[j];
        tot9_m9   += (i128)c2[j] * (i128)fix9[j];
        tot9_m27  += (i128)c3[j] * (i128)fix9[j];
        tot10_m3  += (i128)c1[j] * (i128)fix10[j];
        tot10_m9  += (i128)c2[j] * (i128)fix10[j];
        tot10_m27 += (i128)c3[j] * (i128)fix10[j];
    }

    int d9_mod3  = (int)((tot9_m3  % 3  + 3)  % 3);
    int d9_mod9  = (int)((tot9_m9  % 9  + 9)  % 9);
    int d9_mod27 = (int)((tot9_m27 % 27 + 27) % 27);

    int d10_mod3  = (int)((tot10_m3  % 3  + 3)  % 3);
    int d10_mod9  = (int)((tot10_m9  % 9  + 9)  % 9);
    int d10_mod27 = (int)((tot10_m27 % 27 + 27) % 27);

    printf("\n=== ENGINE 1 SUMMARY ===\n");
    printf("D(9):  raw_m3="); print_i128(tot9_m3);
    printf(", raw_m9="); print_i128(tot9_m9);
    printf(", raw_m27="); print_i128(tot9_m27);
    printf("  =>  mod 3 = %d, mod 9 = %d, mod 27 = %d\n", d9_mod3, d9_mod9, d9_mod27);

    printf("D(10): raw_m3="); print_i128(tot10_m3);
    printf(", raw_m9="); print_i128(tot10_m9);
    printf(", raw_m27="); print_i128(tot10_m27);
    printf("  =>  mod 3 = %d, mod 9 = %d, mod 27 = %d\n", d10_mod3, d10_mod9, d10_mod27);

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("Total Engine 1 elapsed: %.3fs\n", elapsed);

    if (d9_mod3 != 0 || d9_mod9 != 6 || d9_mod27 != 24 || d10_mod3 != 1) {
        fprintf(stderr, "Calibration gate failed!\n");
        return 1;
    }
    return 0;
}
