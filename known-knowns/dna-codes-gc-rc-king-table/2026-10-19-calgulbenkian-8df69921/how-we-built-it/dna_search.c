// High-Performance Multi-Threaded Solver for DNA Codes:
//   Target 1: A_4^{GC}(n, d, w)    (constant GC-content w = floor(n/2))
//   Target 2: A_4^{GC,RC}(n, d, w) (constant GC-content + reverse-complement constraint)
//
// Supports three modes:
//   --mode lns     : Full-universe / RC-orbit-universe K-blocker LNS + exact bit-parallel Max-Clique
//   --mode walksat : WalkSAT conflict-minimization generator + dynamic candidate pool Max-Clique LNS (for n=13..20)
//   --mode exact   : Exact branch-and-bound Max-Clique with symmetry breaking (for optimality proofs)

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>

typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t  u8;

static int G_N = 8;
static int G_D = 4;
static int G_DMAX = 999;
static int G_W = 4;
static int G_RC = 0;
static int G_TIME_LIMIT = 15;
static int G_THREADS = 8;
static int G_TARGET = 99999999;
static char G_OUT_PATH[512] = "";
static char G_SEED_PATH[512] = "";

// Packed word format: ((u64)u << 32) | (u64)v
// where u in {0,1}^n has popcount(u) == w (1 iff C or G)
//       v in {0,1}^n (1 iff G or T)
// Base mapping: A=(0,0), C=(1,0), T=(0,1), G=(1,1)

static inline u32 bitrev_n(u32 x, int n) {
    u32 r = 0;
    for (int i = 0; i < n; i++) {
        if ((x >> i) & 1U) r |= (1U << (n - 1 - i));
    }
    return r;
}

static inline u64 word_rc(u64 w, int n) {
    u32 u = (u32)(w >> 32);
    u32 v = (u32)w;
    u32 mask = (1U << n) - 1U;
    u32 u_rc = bitrev_n(u, n);
    u32 v_rc = bitrev_n((~v) & mask, n);
    return ((u64)u_rc << 32) | (u64)v_rc;
}

static inline int dna_dist(u64 x, u64 y) {
    u64 diff = x ^ y;
    u32 d = ((u32)(diff >> 32)) | ((u32)diff);
    return __builtin_popcount(d);
}

static inline bool dna_compat(u64 x, u64 y, u64 y_rc, int d, int rc_flag) {
    int d1 = dna_dist(x, y);
    if (d1 < d || d1 > G_DMAX) return false;
    if (rc_flag && dna_dist(x, y_rc) < d) return false;
    return true;
}

static void word_to_str(u64 w, int n, char *buf) {
    u32 u = (u32)(w >> 32);
    u32 v = (u32)w;
    for (int i = 0; i < n; i++) {
        int ui = (u >> i) & 1;
        int vi = (v >> i) & 1;
        if (!ui && !vi) buf[i] = 'A';
        else if (ui && !vi) buf[i] = 'C';
        else if (!ui && vi) buf[i] = 'T';
        else buf[i] = 'G';
    }
    buf[n] = '\0';
}

static bool str_to_word(const char *s, int n, int expected_w, u64 *out) {
    u32 u = 0, v = 0;
    int gc = 0;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (c == 'A' || c == 'a') { /* 0,0 */ }
        else if (c == 'C' || c == 'c') { u |= (1U << i); gc++; }
        else if (c == 'T' || c == 't') { v |= (1U << i); }
        else if (c == 'G' || c == 'g') { u |= (1U << i); v |= (1U << i); gc++; }
        else return false;
    }
    if (gc != expected_w) return false;
    *out = ((u64)u << 32) | (u64)v;
    return true;
}

// Global best tracking
static pthread_mutex_t G_LOCK = PTHREAD_MUTEX_INITIALIZER;
static u64 *G_BEST_CODE = NULL;
static int G_BEST_SIZE = 0;
static volatile int G_STOP = 0;
static struct timespec G_START_TS;

static double elapsed_sec(void) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (now.tv_sec - G_START_TS.tv_sec) + 1e-9 * (now.tv_nsec - G_START_TS.tv_nsec);
}

static bool verify_code_exact(const u64 *code, int sz, int n, int d, int w, int rc) {
    for (int i = 0; i < sz; i++) {
        u32 u = (u32)(code[i] >> 32);
        if (__builtin_popcount(u) != w) return false;
        if (rc) {
            u64 irc = word_rc(code[i], n);
            if (dna_dist(code[i], irc) < d) return false;
        }
        for (int j = i + 1; j < sz; j++) {
            if (dna_dist(code[i], code[j]) < d) return false;
            if (rc) {
                u64 jrc = word_rc(code[j], n);
                if (dna_dist(code[i], jrc) < d) return false;
            }
        }
    }
    return true;
}

static void update_global_best(const u64 *code, int sz, int tid) {
    if (sz <= G_BEST_SIZE) return;
    pthread_mutex_lock(&G_LOCK);
    if (sz > G_BEST_SIZE) {
        if (!verify_code_exact(code, sz, G_N, G_D, G_W, G_RC)) {
            fprintf(stderr, "[ERROR] Thread %d produced invalid code of size %d!\n", tid, sz);
            pthread_mutex_unlock(&G_LOCK);
            return;
        }
        G_BEST_SIZE = sz;
        G_BEST_CODE = (u64 *)realloc(G_BEST_CODE, sizeof(u64) * sz);
        memcpy(G_BEST_CODE, code, sizeof(u64) * sz);
        printf("[%.2fs] [T%d] NEW BEST %s(%d, %d, %d) = %d\n",
               elapsed_sec(), tid, G_RC ? "GC,RC" : "GC", G_N, G_D, G_W, sz);
        fflush(stdout);
        if (G_OUT_PATH[0] != '\0') {
            FILE *f = fopen(G_OUT_PATH, "w");
            if (f) {
                char buf[32];
                for (int i = 0; i < sz; i++) {
                    word_to_str(code[i], G_N, buf);
                    fprintf(f, "%s\n", buf);
                }
                fclose(f);
            }
        }
        if (sz >= G_TARGET) {
            G_STOP = 1;
        }
    }
    pthread_mutex_unlock(&G_LOCK);
}

// Fast PRNG (xoshiro256**)
typedef struct { u64 s[4]; } rng_t;
static inline u64 rng_next(rng_t *r) {
    const u64 result = ((r->s[1] * 5) << 7 | (r->s[1] * 5) >> 57) * 9;
    const u64 t = r->s[1] << 17;
    r->s[2] ^= r->s[0];
    r->s[3] ^= r->s[1];
    r->s[1] ^= r->s[2];
    r->s[0] ^= r->s[3];
    r->s[2] ^= t;
    r->s[3] = (r->s[3] << 45) | (r->s[3] >> 19);
    return result;
}
static void rng_seed(rng_t *r, u64 seed) {
    for (int i = 0; i < 4; i++) {
        seed += 0x9e3779b97f4a7c15ULL;
        u64 z = seed;
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
        z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        r->s[i] = z ^ (z >> 31);
    }
}

// ============================================================================
// Exact Bit-Parallel Max-Clique on a Subgraph (up to MAX_SUB = 512 vertices)
// ============================================================================
#define MAX_SUB 512
#define SUB_WORDS (MAX_SUB / 64)

typedef struct {
    int n;
    u64 adj[MAX_SUB][SUB_WORDS];
    int best_sz;
    int best_sol[MAX_SUB];
    int cur_sol[MAX_SUB];
    int max_steps;
    int steps;
} sub_clique_t;

static void sub_expand(sub_clique_t *sc, const u64 *P, int d) {
    if (sc->steps >= sc->max_steps) return;
    sc->steps++;

    // Greedy coloring of P to get upper bound and vertex ordering
    int verts[MAX_SUB];
    int colors[MAX_SUB];
    int nv = 0;

    u64 rem[SUB_WORDS];
    memcpy(rem, P, sizeof(rem));
    int c_num = 0;
    while (1) {
        int first = -1;
        for (int w = 0; w < SUB_WORDS; w++) {
            if (rem[w]) { first = w * 64 + __builtin_ctzll(rem[w]); break; }
        }
        if (first < 0) break;
        c_num++;
        u64 avail[SUB_WORDS];
        memcpy(avail, rem, sizeof(avail));
        while (1) {
            int v = -1;
            for (int w = 0; w < SUB_WORDS; w++) {
                if (avail[w]) { v = w * 64 + __builtin_ctzll(avail[w]); break; }
            }
            if (v < 0) break;
            verts[nv] = v;
            colors[nv] = c_num;
            nv++;
            rem[v >> 6] &= ~(1ULL << (v & 63));
            avail[v >> 6] &= ~(1ULL << (v & 63));
            // Exclude neighbors of v from same color class
            for (int w = 0; w < SUB_WORDS; w++) {
                avail[w] &= ~sc->adj[v][w];
            }
        }
    }

    for (int i = nv - 1; i >= 0; i--) {
        if (d + colors[i] <= sc->best_sz) return;
        int v = verts[i];
        sc->cur_sol[d] = v;

        u64 newP[SUB_WORDS];
        int any = 0;
        for (int w = 0; w < SUB_WORDS; w++) {
            newP[w] = P[w] & sc->adj[v][w];
            if (newP[w]) any = 1;
        }
        if (!any) {
            if (d + 1 > sc->best_sz) {
                sc->best_sz = d + 1;
                memcpy(sc->best_sol, sc->cur_sol, sizeof(int) * (d + 1));
            }
        } else {
            sub_expand(sc, newP, d + 1);
        }
        // Remove v from P
        ((u64 *)P)[v >> 6] &= ~(1ULL << (v & 63));
        if (sc->steps >= sc->max_steps) return;
    }
}

static int solve_subgraph_clique(const u64 *sub_words, const u64 *sub_rc, int sub_n,
                                 int d_min, int rc_flag, int max_steps, int *out_idx) {
    if (sub_n <= 0) return 0;
    if (sub_n > MAX_SUB) sub_n = MAX_SUB;
    sub_clique_t sc;
    memset(&sc, 0, sizeof(sc));
    sc.n = sub_n;
    sc.max_steps = max_steps;

    for (int i = 0; i < sub_n; i++) {
        for (int j = i + 1; j < sub_n; j++) {
            if (dna_compat(sub_words[i], sub_words[j], sub_rc[j], d_min, rc_flag)) {
                sc.adj[i][j >> 6] |= (1ULL << (j & 63));
                sc.adj[j][i >> 6] |= (1ULL << (i & 63));
            }
        }
    }
    u64 P[SUB_WORDS];
    memset(P, 0, sizeof(P));
    for (int i = 0; i < sub_n; i++) P[i >> 6] |= (1ULL << (i & 63));
    sub_expand(&sc, P, 0);
    for (int i = 0; i < sc.best_sz; i++) out_idx[i] = sc.best_sol[i];
    return sc.best_sz;
}

// ============================================================================
// MODE 0: Full-Universe / RC-Orbit Universe K-Blocker LNS
// ============================================================================
static u64 *G_UNIV = NULL;
static u64 *G_UNIV_RC = NULL;
static int G_UNIV_N = 0;

static void build_universe(int n, int d, int w, int rc) {
    // Generate all u in {0,1}^n with popcount(u) == w
    u32 max_mask = 1U << n;
    size_t cap = 1024 * 1024;
    G_UNIV = (u64 *)malloc(sizeof(u64) * cap);
    G_UNIV_RC = (u64 *)malloc(sizeof(u64) * cap);
    G_UNIV_N = 0;

    for (u32 u = 0; u < max_mask; u++) {
        if (__builtin_popcount(u) != w) continue;
        for (u32 v = 0; v < max_mask; v++) {
            u64 word = ((u64)u << 32) | (u64)v;
            u64 wrc = word_rc(word, n);
            if (rc) {
                // Keep only canonical orbit representative word < wrc with dist(word, wrc) >= d
                if (word >= wrc) continue;
                if (dna_dist(word, wrc) < d) continue;
            }
            if ((size_t)G_UNIV_N >= cap) {
                cap *= 2;
                G_UNIV = (u64 *)realloc(G_UNIV, sizeof(u64) * cap);
                G_UNIV_RC = (u64 *)realloc(G_UNIV_RC, sizeof(u64) * cap);
            }
            G_UNIV[G_UNIV_N] = word;
            G_UNIV_RC[G_UNIV_N] = wrc;
            G_UNIV_N++;
        }
    }
    printf("[INIT] Built universe for %s(%d, %d, %d): %d vertices\n",
           rc ? "GC,RC" : "GC", n, d, w, G_UNIV_N);
    fflush(stdout);
}

typedef struct {
    int tid;
    u64 *seed_words;
    int seed_n;
} worker_arg_t;

static void *lns_worker(void *arg) {
    worker_arg_t *wa = (worker_arg_t *)arg;
    int tid = wa->tid;
    int N = G_UNIV_N;
    if (N == 0) return NULL;

    rng_t rng;
    rng_seed(&rng, 0x123456789ABCDEF0ULL ^ ((u64)tid * 0x9E3779B97F4A7C15ULL) ^ (u64)time(NULL));

    u16 *blk_cnt = (u16 *)calloc(N, sizeof(u16));
    u32 *blk_who = (u32 *)calloc(N, sizeof(u32));
    int *code_idx = (int *)malloc(sizeof(int) * (N + 1));
    u64 *code_words = (u64 *)malloc(sizeof(u64) * (N + 1));
    int *in_code = (int *)malloc(sizeof(int) * N);
    memset(in_code, -1, sizeof(int) * N);
    int code_sz = 0;

    // Helper lambdas via macros (bind macro argument once!)
    #define ADD_WORD(u_idx_expr) do { \
        int _u = (u_idx_expr); \
        int pos = code_sz++; \
        code_idx[pos] = _u; \
        in_code[_u] = pos; \
        u64 w_x = G_UNIV[_u]; \
        for (int i = 0; i < N; i++) { \
            if (!dna_compat(w_x, G_UNIV[i], G_UNIV_RC[i], G_D, G_RC)) { \
                blk_cnt[i]++; \
                blk_who[i] ^= (u32)pos; \
            } \
        } \
    } while (0)

    #define REM_POS(pos_expr) do { \
        int _p = (pos_expr); \
        int u_idx = code_idx[_p]; \
        in_code[u_idx] = -1; \
        u64 w_x = G_UNIV[u_idx]; \
        for (int i = 0; i < N; i++) { \
            if (!dna_compat(w_x, G_UNIV[i], G_UNIV_RC[i], G_D, G_RC)) { \
                blk_cnt[i]--; \
                blk_who[i] ^= (u32)_p; \
            } \
        } \
        int last = --code_sz; \
        if (_p != last) { \
            int moved_u = code_idx[last]; \
            code_idx[_p] = moved_u; \
            in_code[moved_u] = _p; \
            u64 w_m = G_UNIV[moved_u]; \
            u32 mask_diff = (u32)(last ^ _p); \
            for (int i = 0; i < N; i++) { \
                if (!dna_compat(w_m, G_UNIV[i], G_UNIV_RC[i], G_D, G_RC)) { \
                    blk_who[i] ^= mask_diff; \
                } \
            } \
        } \
    } while (0)

    int *free_list = (int *)malloc(sizeof(int) * N);
    int *tabu_until = (int *)calloc(N, sizeof(int));
    int *one_blk_cnt = (int *)calloc(N + 1, sizeof(int));
    u64 sub_w[MAX_SUB], sub_rc[MAX_SUB];
    int sub_u[MAX_SUB], clique_out[MAX_SUB];

    int restart_iter = 0;
    while (!G_STOP && elapsed_sec() < G_TIME_LIMIT) {
        restart_iter++;
        // Reset state
        memset(blk_cnt, 0, sizeof(u16) * N);
        memset(blk_who, 0, sizeof(u32) * N);
        memset(in_code, -1, sizeof(int) * N);
        memset(tabu_until, 0, sizeof(int) * N);
        code_sz = 0;

        // If thread 0 on first iteration and seed provided, load seed
        if (restart_iter == 1 && wa->seed_n > 0) {
            for (int s = 0; s < wa->seed_n; s++) {
                u64 sw = wa->seed_words[s];
                u64 sw_rc = word_rc(sw, G_N);
                u64 canon = (G_RC && sw_rc < sw) ? sw_rc : sw;
                for (int i = 0; i < N; i++) {
                    if (G_UNIV[i] == canon && in_code[i] < 0 && blk_cnt[i] == 0) {
                        ADD_WORD(i);
                        break;
                    }
                }
            }
        } else if (G_BEST_SIZE > 0 && (rng_next(&rng) % 2 == 0)) {
            // Warm-start from global best minus 10..20%
            pthread_mutex_lock(&G_LOCK);
            int bsz = G_BEST_SIZE;
            u64 *bcopy = (u64 *)malloc(sizeof(u64) * bsz);
            memcpy(bcopy, G_BEST_CODE, sizeof(u64) * bsz);
            pthread_mutex_unlock(&G_LOCK);
            int drop_mod = 5 + (int)(rng_next(&rng) % 8);
            for (int s = 0; s < bsz; s++) {
                if ((rng_next(&rng) % drop_mod) == 0) continue;
                u64 sw = bcopy[s];
                u64 sw_rc = word_rc(sw, G_N);
                u64 canon = (G_RC && sw_rc < sw) ? sw_rc : sw;
                int lo = 0, hi = N - 1;
                while (lo <= hi) {
                    int mid = (lo + hi) >> 1;
                    if (G_UNIV[mid] == canon) {
                        if (in_code[mid] < 0 && blk_cnt[mid] == 0) ADD_WORD(mid);
                        break;
                    } else if (G_UNIV[mid] < canon) lo = mid + 1;
                    else hi = mid - 1;
                }
            }
            free(bcopy);
        }

        // Greedy completion
        while (1) {
            int nf = 0;
            for (int i = 0; i < N; i++) {
                if (in_code[i] < 0 && blk_cnt[i] == 0) free_list[nf++] = i;
            }
            if (nf == 0) break;
            int pick = free_list[rng_next(&rng) % nf];
            ADD_WORD(pick);
        }

        if (code_sz > G_BEST_SIZE) {
            for (int i = 0; i < code_sz; i++) code_words[i] = G_UNIV[code_idx[i]];
            update_global_best(code_words, code_sz, tid);
        }

        int plateau_limit = (N <= 10000) ? 12000 : ((N <= 80000) ? 3500 : ((N <= 400000) ? 900 : 250));
        int local_best = code_sz;
        int since_imp = 0;

        for (int iter = 1; iter <= plateau_limit && !G_STOP && elapsed_sec() < G_TIME_LIMIT; iter++) {
            if (code_sz < 2) break;

            // Strategy A (35% of steps): fast 1-for-1 or 1-for-2 Tabu swap using blk_cnt[i] == 1!
            if ((rng_next(&rng) % 100) < 35) {
                memset(one_blk_cnt, 0, sizeof(int) * code_sz);
                int n1 = 0;
                for (int i = 0; i < N; i++) {
                    if (in_code[i] < 0 && blk_cnt[i] == 1 && iter >= tabu_until[i]) {
                        u32 who = blk_who[i];
                        if (who < (u32)code_sz) {
                            one_blk_cnt[who]++;
                            free_list[n1++] = i;
                        }
                    }
                }
                if (n1 > 0) {
                    // Pick a random 1-blocked vertex u_new, remove its unique blocker r0, add u_new + any other freed!
                    int pick_u = free_list[rng_next(&rng) % n1];
                    int r0 = (int)blk_who[pick_u];
                    if (r0 >= 0 && r0 < code_sz) {
                        int old_u = code_idx[r0];
                        REM_POS(r0);
                        tabu_until[old_u] = iter + 7 + (int)(rng_next(&rng) % 10);
                        ADD_WORD(pick_u);
                        // Greedily add any additional now-free vertices!
                        while (1) {
                            int nf2 = 0;
                            for (int i = 0; i < N; i++) {
                                if (in_code[i] < 0 && blk_cnt[i] == 0) free_list[nf2++] = i;
                            }
                            if (nf2 == 0) break;
                            ADD_WORD(free_list[rng_next(&rng) % nf2]);
                        }
                        if (code_sz > local_best) {
                            local_best = code_sz;
                            since_imp = 0;
                            if (code_sz > G_BEST_SIZE) {
                                for (int i = 0; i < code_sz; i++) code_words[i] = G_UNIV[code_idx[i]];
                                update_global_best(code_words, code_sz, tid);
                            }
                        } else {
                            since_imp++;
                        }
                        continue;
                    }
                }
            }

            // Strategy B: Blocker-driven K-removal + exact Max-Clique on freed neighborhood!
            // Pick a vertex x with 1 <= blk_cnt[x] <= 3 (not tabu), and remove all its blockers in C,
            // plus blockers of a second low-blocked vertex y that shares at least one blocker with x!
            int K_max = (since_imp > 100 && code_sz >= 5) ? 5 : (2 + (int)(rng_next(&rng) % 3));
            if (K_max > code_sz) K_max = code_sz;

            int n_low = 0;
            for (int i = 0; i < N; i++) {
                if (in_code[i] < 0 && blk_cnt[i] >= 1 && blk_cnt[i] <= 3 && iter >= tabu_until[i]) {
                    free_list[n_low++] = i;
                }
            }
            if (n_low == 0) {
                for (int i = 0; i < N; i++) {
                    if (in_code[i] < 0 && blk_cnt[i] >= 1 && blk_cnt[i] <= 4) {
                        free_list[n_low++] = i;
                    }
                }
            }
            if (n_low == 0) break;

            int rem_pos[6];
            int picked = 0;
            int seed_x = free_list[rng_next(&rng) % n_low];
            u64 wx = G_UNIV[seed_x];
            for (int p = 0; p < code_sz && picked < K_max; p++) {
                int cu = code_idx[p];
                if (!dna_compat(wx, G_UNIV[cu], G_UNIV_RC[cu], G_D, G_RC)) {
                    rem_pos[picked++] = p;
                }
            }

            // Try to augment rem_pos up to K_max by finding another low-blocked vertex y
            // that is blocked by at least one codeword already in rem_pos!
            if (picked > 0 && picked < K_max) {
                int anchor_pos = rem_pos[rng_next(&rng) % picked];
                u64 w_anc = G_UNIV[code_idx[anchor_pos]];
                u64 w_anc_rc = G_UNIV_RC[code_idx[anchor_pos]];
                for (int tries = 0; tries < 60 && picked < K_max; tries++) {
                    int cand_y = free_list[rng_next(&rng) % n_low];
                    if (cand_y == seed_x) continue;
                    u64 wy = G_UNIV[cand_y];
                    if (!dna_compat(wy, w_anc, w_anc_rc, G_D, G_RC)) {
                        // Add all blockers of cand_y to rem_pos if they fit in K_max
                        int add_p[4], n_add = 0;
                        bool fits = true;
                        for (int p = 0; p < code_sz; p++) {
                            int cu = code_idx[p];
                            if (!dna_compat(wy, G_UNIV[cu], G_UNIV_RC[cu], G_D, G_RC)) {
                                bool already = false;
                                for (int j = 0; j < picked; j++) if (rem_pos[j] == p) { already = true; break; }
                                if (!already) {
                                    if (picked + n_add + 1 > K_max) { fits = false; break; }
                                    add_p[n_add++] = p;
                                }
                            }
                        }
                        if (fits && n_add > 0) {
                            for (int j = 0; j < n_add; j++) rem_pos[picked++] = add_p[j];
                        }
                    }
                }
            }
            int K = picked;
            if (K == 0) continue;

            // Sort rem_pos descending so REM_POS doesn't invalidate earlier indices
            for (int a = 0; a < K; a++) {
                for (int b = a + 1; b < K; b++) {
                    if (rem_pos[a] < rem_pos[b]) {
                        int tmp = rem_pos[a]; rem_pos[a] = rem_pos[b]; rem_pos[b] = tmp;
                    }
                }
            }
            int saved_u[6];
            for (int a = 0; a < K; a++) {
                saved_u[a] = code_idx[rem_pos[a]];
                REM_POS(rem_pos[a]);
            }

            // Collect all now-free vertices EXCLUDING saved_u[0..K-1] first!
            int nf = 0;
            for (int i = 0; i < N; i++) {
                if (in_code[i] < 0 && blk_cnt[i] == 0) {
                    bool is_saved = false;
                    for (int a = 0; a < K; a++) if (i == saved_u[a]) { is_saved = true; break; }
                    if (!is_saved && iter >= tabu_until[i]) {
                        free_list[nf++] = i;
                    }
                }
            }

            if (nf >= 1) {
                int sub_n = 0;
                int max_new = MAX_SUB - (K - 1);
                for (int i = 0; i < nf && sub_n < max_new; i++) {
                    if (nf > max_new) {
                        int r = i + (int)(rng_next(&rng) % (nf - i));
                        int tmp = free_list[i]; free_list[i] = free_list[r]; free_list[r] = tmp;
                    }
                    int u_i = free_list[i];
                    sub_u[sub_n] = u_i;
                    sub_w[sub_n] = G_UNIV[u_i];
                    sub_rc[sub_n] = G_UNIV_RC[u_i];
                    sub_n++;
                }
                // Include at most K-1 of saved_u (NEVER saved_u[0]!), so any K-clique MUST use >= 1 new vertex!
                for (int a = 1; a < K && sub_n < MAX_SUB; a++) {
                    int u_i = saved_u[a];
                    sub_u[sub_n] = u_i;
                    sub_w[sub_n] = G_UNIV[u_i];
                    sub_rc[sub_n] = G_UNIV_RC[u_i];
                    sub_n++;
                }

                int clq_sz = solve_subgraph_clique(sub_w, sub_rc, sub_n, G_D, G_RC, 3000, clique_out);
                if (clq_sz >= K) {
                    for (int a = 0; a < K; a++) {
                        tabu_until[saved_u[a]] = iter + 6 + (int)(rng_next(&rng) % 8);
                    }
                    for (int c = 0; c < clq_sz; c++) {
                        ADD_WORD(sub_u[clique_out[c]]);
                    }
                    // Also greedily add any remaining free vertices (including saved_u if still compatible!)
                    while (1) {
                        int rem_f = 0;
                        for (int i = 0; i < N; i++) {
                            if (in_code[i] < 0 && blk_cnt[i] == 0) free_list[rem_f++] = i;
                        }
                        if (rem_f == 0) break;
                        ADD_WORD(free_list[rng_next(&rng) % rem_f]);
                    }
                    if (code_sz > local_best) {
                        local_best = code_sz;
                        since_imp = 0;
                        if (code_sz > G_BEST_SIZE) {
                            for (int i = 0; i < code_sz; i++) code_words[i] = G_UNIV[code_idx[i]];
                            update_global_best(code_words, code_sz, tid);
                        }
                    } else {
                        since_imp++;
                    }
                    continue;
                }
            }
            // Restore saved_u
            for (int a = 0; a < K; a++) {
                if (in_code[saved_u[a]] < 0 && blk_cnt[saved_u[a]] == 0) {
                    ADD_WORD(saved_u[a]);
                }
            }
            since_imp++;
        }
    }

    free(blk_cnt);
    free(blk_who);
    free(code_idx);
    free(code_words);
    free(in_code);
    free(free_list);
    free(tabu_until);
    free(one_blk_cnt);
    return NULL;
}

// ============================================================================
// MODE 1: WalkSAT Conflict-Minimization + Dynamic Pool Max-Clique LNS (n=13..20)
// ============================================================================
static inline u64 rand_gc_word(rng_t *rng, int n, int w) {
    u32 u = 0;
    int bits = 0;
    while (bits < w) {
        int pos = (int)(rng_next(rng) % n);
        if (!((u >> pos) & 1U)) {
            u |= (1U << pos);
            bits++;
        }
    }
    u32 v = (u32)(rng_next(rng) & ((1U << n) - 1U));
    return ((u64)u << 32) | (u64)v;
}

static inline int eval_conflicts(u64 x, u64 x_rc, const u64 *code, const u64 *code_rc,
                                 int code_sz, int d, int rc, int *first_conf, int *deficit) {
    int conf = 0;
    int def = 0;
    int fc = -1;
    for (int i = 0; i < code_sz; i++) {
        int d1 = dna_dist(x, code[i]);
        if (d1 < d) {
            conf++;
            def += (d - d1);
            if (fc < 0) fc = i;
            continue;
        }
        if (d1 > G_DMAX) {
            conf++;
            def += (d1 - G_DMAX);
            if (fc < 0) fc = i;
            continue;
        }
        if (rc) {
            int d2 = dna_dist(x, code_rc[i]);
            if (d2 < d) {
                conf++;
                def += (d - d2);
                if (fc < 0) fc = i;
            }
        }
    }
    *first_conf = fc;
    *deficit = def;
    return conf;
}

static void *walksat_worker(void *arg) {
    worker_arg_t *wa = (worker_arg_t *)arg;
    int tid = wa->tid;
    int n = G_N, d = G_D, w = G_W, rc = G_RC;
    u32 mask_n = (1U << n) - 1U;

    rng_t rng;
    rng_seed(&rng, 0xCAFEBABE12345678ULL ^ ((u64)tid * 0x9E3779B97F4A7C15ULL) ^ (u64)time(NULL));

    int max_code = 65536;
    u64 *code = (u64 *)malloc(sizeof(u64) * max_code);
    u64 *code_rc = (u64 *)malloc(sizeof(u64) * max_code);
    int code_sz = 0;

    // Pool of low-conflict candidates (<= 2 conflicts with current code)
    #define POOL_CAP 8192
    u64 *pool = (u64 *)malloc(sizeof(u64) * POOL_CAP);
    u64 *pool_rc = (u64 *)malloc(sizeof(u64) * POOL_CAP);
    int pool_sz = 0;

    u64 sub_w[MAX_SUB], sub_rc[MAX_SUB];
    int clique_out[MAX_SUB];

    while (!G_STOP && elapsed_sec() < G_TIME_LIMIT) {
        code_sz = 0;
        pool_sz = 0;

        int pass = 0;
        if (G_BEST_SIZE > 0) {
            pthread_mutex_lock(&G_LOCK);
            int bsz = G_BEST_SIZE;
            u64 *bcopy = (u64 *)malloc(sizeof(u64) * bsz);
            memcpy(bcopy, G_BEST_CODE, sizeof(u64) * bsz);
            pthread_mutex_unlock(&G_LOCK);
            // Shuffle bcopy
            for (int i = 0; i < bsz; i++) {
                int r = i + (int)(rng_next(&rng) % (bsz - i));
                u64 tmp = bcopy[i]; bcopy[i] = bcopy[r]; bcopy[r] = tmp;
            }
            // Keep 100% of G_BEST_CODE most of the time so K-blocker LNS and WalkSAT can climb directly from G_BEST_SIZE!
            int drop_cnt = ((rng_next(&rng) & 3) == 0 && bsz > 4) ? (1 + (int)(rng_next(&rng) % 2)) : 0;
            for (int i = drop_cnt; i < bsz; i++) {
                code[code_sz] = bcopy[i];
                code_rc[code_sz] = word_rc(bcopy[i], n);
                code_sz++;
            }
            free(bcopy);
        } else if (wa->seed_n > 0) {
            for (int i = 0; i < wa->seed_n; i++) {
                u64 x = wa->seed_words[i];
                u64 xrc = word_rc(x, n);
                if (rc && dna_dist(x, xrc) < d) continue;
                int fc, def;
                if (eval_conflicts(x, xrc, code, code_rc, code_sz, d, rc, &fc, &def) == 0) {
                    code[code_sz] = x;
                    code_rc[code_sz] = xrc;
                    code_sz++;
                }
            }
        }

        int stagnation = 0;
        while (stagnation < 2500 && !G_STOP && elapsed_sec() < G_TIME_LIMIT) {
            u64 x;
            if (code_sz > 0 && (rng_next(&rng) % 2 == 0)) {
                x = code[rng_next(&rng) % code_sz];
                u32 u = (u32)(x >> 32);
                u32 v = (u32)x;
                int swaps = (d + 1) / 3;
                for (int s = 0; s < swaps; s++) {
                    int p1 = (int)(rng_next(&rng) % n);
                    int p2 = (int)(rng_next(&rng) % n);
                    if (((u >> p1) & 1U) != ((u >> p2) & 1U)) {
                        u ^= (1U << p1) | (1U << p2);
                    }
                }
                for (int s = 0; s < d / 2; s++) {
                    v ^= (1U << (rng_next(&rng) % n));
                }
                x = ((u64)u << 32) | (u64)v;
            } else {
                x = rand_gc_word(&rng, n, w);
            }

            bool added = false;
            for (int step = 0; step < 50; step++) {
                u64 xrc = word_rc(x, n);
                int self_def = 0;
                if (rc) {
                    int sd = dna_dist(x, xrc);
                    if (sd < d) self_def = (d - sd) * 4;
                }
                int fc = -1, def = 0;
                int conf = eval_conflicts(x, xrc, code, code_rc, code_sz, d, rc, &fc, &def);
                int tot_def = def + self_def;

                if (tot_def == 0) {
                    code[code_sz] = x;
                    code_rc[code_sz] = xrc;
                    code_sz++;
                    added = true;
                    stagnation = 0;
                    if (code_sz > G_BEST_SIZE) {
                        update_global_best(code, code_sz, tid);
                    }
                    break;
                }

                if (self_def == 0 && conf <= 2 && pool_sz < POOL_CAP) {
                    u64 canon = (rc && xrc < x) ? xrc : x;
                    bool dup = false;
                    for (int p = 0; p < pool_sz; p++) {
                        if (pool[p] == canon) { dup = true; break; }
                    }
                    if (!dup) {
                        pool[pool_sz] = canon;
                        pool_rc[pool_sz] = word_rc(canon, n);
                        pool_sz++;
                    }
                }

                // Sample 20 random 1-step neighbors
                u64 best_nx = x;
                int best_ndef = tot_def;
                u32 u = (u32)(x >> 32);
                u32 v = (u32)x;

                for (int trial = 0; trial < 20; trial++) {
                    u32 nu = u, nv = v;
                    if ((trial & 1) == 0) {
                        nv ^= (1U << (rng_next(&rng) % n));
                        if ((trial & 3) == 0) nv ^= (1U << (rng_next(&rng) % n));
                    } else {
                        int p1 = (int)(rng_next(&rng) % n);
                        int p2 = (int)(rng_next(&rng) % n);
                        while (((u >> p1) & 1U) == ((u >> p2) & 1U)) {
                            p2 = (int)(rng_next(&rng) % n);
                        }
                        nu ^= (1U << p1) | (1U << p2);
                        nv ^= ((u32)(rng_next(&rng) & 1U) << p1) ^ ((u32)(rng_next(&rng) & 1U) << p2);
                    }
                    u64 nx = ((u64)nu << 32) | (u64)(nv & mask_n);
                    u64 nxrc = word_rc(nx, n);
                    int ns_def = 0;
                    if (rc) {
                        int sd = dna_dist(nx, nxrc);
                        if (sd < d) ns_def = (d - sd) * 4;
                    }
                    int nfc, ndef;
                    eval_conflicts(nx, nxrc, code, code_rc, code_sz, d, rc, &nfc, &ndef);
                    if (ndef + ns_def < best_ndef || (ndef + ns_def == best_ndef && (rng_next(&rng) & 3) == 0)) {
                        best_ndef = ndef + ns_def;
                        best_nx = nx;
                    }
                }
                x = best_nx;
            }
            if (!added) stagnation++;

            // Periodically run K-blocker LNS using pool (selecting removal set from pool conflicts!)
            if (pool_sz >= 4 && (stagnation % 12 == 0) && code_sz >= 2) {
                int K_max = 2 + (int)(rng_next(&rng) % 2); // 2 or 3
                if (K_max > code_sz) K_max = code_sz;
                int rem[4];
                int K = 0;
                int seed_p = (int)(rng_next(&rng) % pool_sz);
                u64 px = pool[seed_p], px_rc = pool_rc[seed_p];
                for (int c = 0; c < code_sz && K < K_max; c++) {
                    if (!dna_compat(px, code[c], code_rc[c], d, rc)) {
                        rem[K++] = c;
                    }
                }
                if (K > 0 && K < K_max && pool_sz > 1) {
                    int anc_c = rem[0];
                    for (int tries = 0; tries < 25 && K < K_max; tries++) {
                        int p2 = (int)(rng_next(&rng) % pool_sz);
                        if (p2 == seed_p) continue;
                        if (!dna_compat(pool[p2], code[anc_c], code_rc[anc_c], d, rc)) {
                            for (int c = 0; c < code_sz && K < K_max; c++) {
                                if (!dna_compat(pool[p2], code[c], code_rc[c], d, rc)) {
                                    bool dup = false;
                                    for (int j = 0; j < K; j++) if (rem[j] == c) dup = true;
                                    if (!dup) rem[K++] = c;
                                }
                            }
                        }
                    }
                }
                if (K == 0) continue;
                for (int a = 0; a < K; a++)
                    for (int b = a + 1; b < K; b++)
                        if (rem[a] < rem[b]) { int t = rem[a]; rem[a] = rem[b]; rem[b] = t; }

                u64 saved[4];
                for (int a = 0; a < K; a++) {
                    saved[a] = code[rem[a]];
                    code[rem[a]] = code[code_sz - 1];
                    code_rc[rem[a]] = code_rc[code_sz - 1];
                    code_sz--;
                }

                // Filter pool for words that now have 0 conflicts with reduced code!
                int sub_n = 0;
                for (int p = 0; p < pool_sz && sub_n < MAX_SUB - K; p++) {
                    int fc, def;
                    if (eval_conflicts(pool[p], pool_rc[p], code, code_rc, code_sz, d, rc, &fc, &def) == 0) {
                        // Make sure pool[p] != saved[0]
                        u64 s0_rc = word_rc(saved[0], n);
                        u64 s0_can = (rc && s0_rc < saved[0]) ? s0_rc : saved[0];
                        if (pool[p] != s0_can) {
                            sub_w[sub_n] = pool[p];
                            sub_rc[sub_n] = pool_rc[p];
                            sub_n++;
                        }
                    }
                }
                // Include saved[1..K-1] (NOT saved[0])
                for (int a = 1; a < K && sub_n < MAX_SUB; a++) {
                    sub_w[sub_n] = saved[a];
                    sub_rc[sub_n] = word_rc(saved[a], n);
                    sub_n++;
                }

                if (sub_n >= K) {
                    int clq_sz = solve_subgraph_clique(sub_w, sub_rc, sub_n, d, rc, 2500, clique_out);
                    if (clq_sz >= K) {
                        for (int c = 0; c < clq_sz; c++) {
                            code[code_sz] = sub_w[clique_out[c]];
                            code_rc[code_sz] = sub_rc[clique_out[c]];
                            code_sz++;
                        }
                        // Also check if saved[0] is still compatible with new code!
                        int fc, def;
                        u64 s0_rc = word_rc(saved[0], n);
                        if (eval_conflicts(saved[0], s0_rc, code, code_rc, code_sz, d, rc, &fc, &def) == 0) {
                            code[code_sz] = saved[0];
                            code_rc[code_sz] = s0_rc;
                            code_sz++;
                            clq_sz++;
                        }
                        if (clq_sz > K) {
                            stagnation = 0;
                            if (code_sz > G_BEST_SIZE) {
                                update_global_best(code, code_sz, tid);
                            }
                        }
                    } else {
                        for (int a = 0; a < K; a++) {
                            code[code_sz] = saved[a];
                            code_rc[code_sz] = word_rc(saved[a], n);
                            code_sz++;
                        }
                    }
                } else {
                    for (int a = 0; a < K; a++) {
                        code[code_sz] = saved[a];
                        code_rc[code_sz] = word_rc(saved[a], n);
                        code_sz++;
                    }
                }

                if (pool_sz >= POOL_CAP - 64) {
                    int keep = 0;
                    for (int p = 0; p < pool_sz; p++) {
                        int fc, def;
                        int cf = eval_conflicts(pool[p], pool_rc[p], code, code_rc, code_sz, d, rc, &fc, &def);
                        if (cf >= 1 && cf <= 2) {
                            pool[keep] = pool[p];
                            pool_rc[keep] = pool_rc[p];
                            keep++;
                        }
                    }
                    pool_sz = keep;
                }
            }
        }
    }

    free(code);
    free(code_rc);
    free(pool);
    free(pool_rc);
    return NULL;
}

// ============================================================================
// MODE 2: Symmetric Orbit Search (Cyclic for GC, Centralizer Z(RC) for GC,RC)
// ============================================================================
static int G_ORBIT_STEP = 0;
static int G_ORBIT_FLIP = -1;
static int G_ORBIT_RCGEN = -1;

static inline u64 apply_gen(u64 w, int n, int rc_mode, int step, int flip_mode) {
    u32 u = (u32)(w >> 32);
    u32 v = (u32)w;
    u32 mask_n = (1U << n) - 1U;

    for (int s = 0; s < step; s++) {
        u32 nu = 0, nv = 0;
        if (!rc_mode) {
            // Standard cyclic shift of 0..n-1
            for (int i = 0; i < n; i++) {
                int nxt = (i + 1 < n) ? (i + 1) : 0;
                if ((u >> i) & 1U) nu |= (1U << nxt);
                if ((v >> i) & 1U) nv |= (1U << nxt);
            }
            if (flip_mode == 1) nv ^= 1U; // negacyclic on v at pos 0
            else if (flip_mode == 2) nv ^= mask_n;
        } else {
            // Centralizer Z(RC) 2m-cycle: (0, 1, ..., m-1, n-1, n-2, ..., n-m)
            // Middle coordinate m (if n is odd) is fixed!
            int m = n / 2;
            int cyc[24];
            for (int k = 0; k < m; k++) cyc[k] = k;
            for (int k = 0; k < m; k++) cyc[m + k] = n - 1 - k;
            for (int k = 0; k < 2 * m; k++) {
                int src = cyc[k];
                int dst = cyc[(k + 1) % (2 * m)];
                if ((u >> src) & 1U) nu |= (1U << dst);
                if ((v >> src) & 1U) nv |= (1U << dst);
            }
            if (n & 1) {
                if ((u >> m) & 1U) nu |= (1U << m);
                if ((v >> m) & 1U) nv |= (1U << m);
            }
            // Palindromic v-flips (commute with RC!)
            if (flip_mode == 1) {
                nv ^= mask_n;
            } else if (flip_mode == 2) {
                nv ^= (1U << (m - 1)) | (1U << (n - m));
            } else if (flip_mode == 3) {
                nv ^= (1U << 0) | (1U << (n - 1));
                if (n & 1) nv ^= (1U << m);
            }
        }
        u = nu;
        v = nv;
    }
    return ((u64)u << 32) | (u64)v;
}

typedef struct {
    u64 words[40];
    u64 words_rc[40];
    int sz;
} orbit_t;

static inline bool orbits_compat(const orbit_t *A, const orbit_t *B, int d, int rc) {
    // By group invariance, since A and B in a thread's pool are generated by the exact
    // same cyclic subgroup <g>, d_H(g^a(x0), g^b(y0)) = d_H(x0, g^(b-a)(y0)),
    // so checking A->words[0] against all words in B is 100% exact and 20x faster!
    u64 x = A->words[0];
    for (int j = 0; j < B->sz; j++) {
        if (!dna_compat(x, B->words[j], B->words_rc[j], d, rc)) return false;
    }
    return true;
}

static int eval_orbit_self_deficit(u64 seed, int n, int d, int rc, int rc_gen, int step, int flip, int max_len) {
    u64 words[40];
    int sz = 0;
    u64 cur = seed;
    int def = 0;
    for (int k = 0; k < max_len; k++) {
        words[sz++] = cur;
        cur = apply_gen(cur, n, rc_gen, step, flip);
        if (cur == seed) break;
    }
    if (cur != seed || sz < 2) return 999999;
    // Check internal distances from words[0] to words[1..sz-1] (by group invariance, this checks all pairs!)
    u64 w0 = words[0];
    for (int i = 1; i < sz; i++) {
        int dist = dna_dist(w0, words[i]);
        if (dist < d) def += (d - dist);
        else if (dist > G_DMAX) def += (dist - G_DMAX);
    }
    if (rc) {
        for (int i = 0; i < sz; i++) {
            u64 irc = word_rc(words[i], n);
            int dist = dna_dist(w0, irc);
            if (dist < d) def += (d - dist);
        }
    }
    return def;
}

static bool build_valid_orbit(u64 seed, int n, int d, int rc, int rc_gen, int step, int flip, int max_len, orbit_t *out) {
    out->sz = 0;
    u64 cur = seed;
    u64 seed_rc = word_rc(seed, n);
    if (rc && dna_dist(seed, seed_rc) < d) return false;
    for (int k = 0; k < max_len; k++) {
        u64 crc = word_rc(cur, n);
        if (k > 0) {
            if (cur == seed) break;
            if (rc && crc == seed) return false;
            if (!dna_compat(seed, cur, crc, d, rc)) return false;
        }
        out->words[out->sz] = cur;
        out->words_rc[out->sz] = crc;
        out->sz++;
        cur = apply_gen(cur, n, rc_gen, step, flip);
        if (cur == seed) break;
    }
    return (cur == seed && out->sz >= 2);
}

static void *orbit_worker(void *arg) {
    worker_arg_t *wa = (worker_arg_t *)arg;
    int tid = wa->tid;
    int n = G_N, d = G_D, w = G_W, rc = G_RC;
    u32 mask_n = (1U << n) - 1U;

    rng_t rng;
    rng_seed(&rng, 0x7777777711111111ULL ^ ((u64)tid * 0x9E3779B97F4A7C15ULL) ^ (u64)time(NULL));

    int rc_gen = rc ? 1 : ((G_ORBIT_RCGEN >= 0) ? G_ORBIT_RCGEN : (tid & 1));
    int cyc_len = rc_gen ? (2 * (n / 2)) : n;
    int step = G_ORBIT_STEP;
    if (step <= 0) {
        if (tid < 4) step = 1;
        else if (tid < 6 && (cyc_len % 2 == 0)) step = 2;
        else if (tid == 6 && (cyc_len % 3 == 0)) step = 3;
        else if (tid == 7 && (cyc_len % 4 == 0)) step = 4;
        else step = 1;
    }
    int flip = (G_ORBIT_FLIP >= 0) ? G_ORBIT_FLIP : (tid % 4);
    int max_len = 40;

    #define MAX_ORBITS 4096
    orbit_t *pool = (orbit_t *)malloc(sizeof(orbit_t) * MAX_ORBITS);
    int pool_n = 0;

    double collect_deadline = G_TIME_LIMIT * 0.45;
    int attempts = 0;
    int max_attempts = (d >= 10 || rc) ? 120000 : 350000;
    while (pool_n < MAX_ORBITS && !G_STOP && elapsed_sec() < collect_deadline && attempts < max_attempts) {
        attempts++;
        u64 x = rand_gc_word(&rng, n, w);
        int cur_def = eval_orbit_self_deficit(x, n, d, rc, rc_gen, step, flip, max_len);
        // Run WalkSAT on x if cur_def > 0 and either d >= 9, rc == 1, or pool_n < 256!
        if (cur_def > 0 && cur_def < 900000 && (d >= 9 || rc || pool_n < 256 || (attempts & 7) == 0)) {
            for (int ws = 0; ws < 28 && cur_def > 0; ws++) {
                u32 u = (u32)(x >> 32);
                u32 v = (u32)x;
                u64 best_nx = x;
                int best_def = cur_def;
                for (int tr = 0; tr < 14; tr++) {
                    u32 nu = u, nv = v;
                    if (tr & 1) {
                        nv ^= (1U << (rng_next(&rng) % n));
                    } else {
                        int p1 = (int)(rng_next(&rng) % n);
                        int p2 = (int)(rng_next(&rng) % n);
                        while (((u >> p1) & 1U) == ((u >> p2) & 1U)) p2 = (int)(rng_next(&rng) % n);
                        nu ^= (1U << p1) | (1U << p2);
                        nv ^= ((u32)(rng_next(&rng) & 1U) << p1) ^ ((u32)(rng_next(&rng) & 1U) << p2);
                    }
                    u64 nx = ((u64)nu << 32) | (u64)(nv & mask_n);
                    int nd = eval_orbit_self_deficit(nx, n, d, rc, rc_gen, step, flip, max_len);
                    if (nd < best_def || (nd == best_def && (rng_next(&rng) & 3) == 0)) {
                        best_def = nd;
                        best_nx = nx;
                    }
                }
                x = best_nx;
                cur_def = best_def;
            }
        }
        if (cur_def != 0) continue;

        orbit_t orb;
        if (!build_valid_orbit(x, n, d, rc, rc_gen, step, flip, max_len, &orb)) continue;

        if (orb.sz > G_BEST_SIZE) {
            update_global_best(orb.words, orb.sz, tid);
        }

        u64 min_w = orb.words[0];
        for (int i = 1; i < orb.sz; i++) if (orb.words[i] < min_w) min_w = orb.words[i];
        if (rc) {
            for (int i = 0; i < orb.sz; i++) if (orb.words_rc[i] < min_w) min_w = orb.words_rc[i];
        }
        bool dup = false;
        for (int p = 0; p < pool_n; p++) {
            for (int i = 0; i < pool[p].sz; i++) {
                if (pool[p].words[i] == min_w) { dup = true; break; }
            }
            if (dup) break;
        }
        if (!dup) {
            pool[pool_n++] = orb;
        }
    }

    if (pool_n > 0) {
        int W = (pool_n + 63) / 64;
        u64 **adj = (u64 **)malloc(sizeof(u64 *) * pool_n);
        for (int i = 0; i < pool_n; i++) adj[i] = (u64 *)calloc(W, sizeof(u64));
        for (int i = 0; i < pool_n; i++) {
            for (int j = i + 1; j < pool_n; j++) {
                if (orbits_compat(&pool[i], &pool[j], d, rc)) {
                    adj[i][j >> 6] |= (1ULL << (j & 63));
                    adj[j][i >> 6] |= (1ULL << (i & 63));
                }
            }
        }

        int *cur_orbs = (int *)malloc(sizeof(int) * pool_n);
        int *avail = (int *)malloc(sizeof(int) * pool_n);
        u64 *flat_code = (u64 *)malloc(sizeof(u64) * (pool_n * 40 + 100));

        for (int restart = 0; restart < 1200 && !G_STOP && elapsed_sec() < G_TIME_LIMIT * 0.78; restart++) {
            int cur_n = 0;
            u64 *cand_mask = (u64 *)malloc(sizeof(u64) * W);
            for (int w_i = 0; w_i < W; w_i++) cand_mask[w_i] = ~0ULL;
            if (pool_n & 63) cand_mask[W - 1] = (1ULL << (pool_n & 63)) - 1ULL;

            while (1) {
                int na = 0;
                for (int w_i = 0; w_i < W; w_i++) {
                    u64 m = cand_mask[w_i];
                    while (m) {
                        int b = __builtin_ctzll(m);
                        avail[na++] = w_i * 64 + b;
                        m &= m - 1;
                    }
                }
                if (na == 0) break;
                int pick = avail[rng_next(&rng) % na];
                cur_orbs[cur_n++] = pick;
                for (int w_i = 0; w_i < W; w_i++) cand_mask[w_i] &= adj[pick][w_i];
            }

            for (int it = 0; it < 1800 && cur_n >= 1 && !G_STOP; it++) {
                int K = 1 + (int)(rng_next(&rng) % 2);
                if (K > cur_n) K = cur_n;
                int saved[3];
                for (int a = 0; a < K; a++) {
                    int r_idx = (int)(rng_next(&rng) % cur_n);
                    saved[a] = cur_orbs[r_idx];
                    cur_orbs[r_idx] = cur_orbs[--cur_n];
                }
                for (int w_i = 0; w_i < W; w_i++) cand_mask[w_i] = ~0ULL;
                if (pool_n & 63) cand_mask[W - 1] = (1ULL << (pool_n & 63)) - 1ULL;
                for (int j = 0; j < cur_n; j++) {
                    int u_o = cur_orbs[j];
                    for (int w_i = 0; w_i < W; w_i++) cand_mask[w_i] &= adj[u_o][w_i];
                }
                cand_mask[saved[0] >> 6] &= ~(1ULL << (saved[0] & 63));

                int added = 0;
                while (1) {
                    int na = 0;
                    for (int w_i = 0; w_i < W; w_i++) {
                        u64 m = cand_mask[w_i];
                        while (m) {
                            int b = __builtin_ctzll(m);
                            avail[na++] = w_i * 64 + b;
                            m &= m - 1;
                        }
                    }
                    if (na == 0) break;
                    int pick = avail[rng_next(&rng) % na];
                    cur_orbs[cur_n++] = pick;
                    added++;
                    for (int w_i = 0; w_i < W; w_i++) cand_mask[w_i] &= adj[pick][w_i];
                }
                bool s0_ok = true;
                for (int j = 0; j < cur_n; j++) {
                    int u_o = cur_orbs[j];
                    if (u_o == saved[0] || !((adj[saved[0]][u_o >> 6] >> (u_o & 63)) & 1ULL)) {
                        s0_ok = false; break;
                    }
                }
                if (s0_ok) {
                    cur_orbs[cur_n++] = saved[0];
                    added++;
                }
                if (added < K) {
                    cur_n -= added;
                    for (int a = 0; a < K; a++) cur_orbs[cur_n++] = saved[a];
                } else {
                    int tot_words = 0;
                    for (int j = 0; j < cur_n; j++) {
                        for (int k = 0; k < pool[cur_orbs[j]].sz; k++) {
                            flat_code[tot_words++] = pool[cur_orbs[j]].words[k];
                        }
                    }
                    if (tot_words > G_BEST_SIZE) {
                        update_global_best(flat_code, tot_words, tid);
                    }
                }
            }
            free(cand_mask);
        }

        for (int i = 0; i < pool_n; i++) free(adj[i]);
        free(adj);
        free(cur_orbs);
        free(avail);
        free(flat_code);
    }

    free(pool);
    return walksat_worker(arg);
}

int main(int argc, char **argv) {
    char mode[32] = "lns";
    G_ORBIT_STEP = 0;
    G_ORBIT_FLIP = -1;
    G_ORBIT_RCGEN = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n") && i + 1 < argc) G_N = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-d") && i + 1 < argc) G_D = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--dmax") && i + 1 < argc) G_DMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-w") && i + 1 < argc) G_W = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rc")) G_RC = 1;
        else if (!strcmp(argv[i], "-t") && i + 1 < argc) G_TIME_LIMIT = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--threads") && i + 1 < argc) G_THREADS = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--target") && i + 1 < argc) G_TARGET = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--step") && i + 1 < argc) G_ORBIT_STEP = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--flip") && i + 1 < argc) G_ORBIT_FLIP = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rcgen") && i + 1 < argc) G_ORBIT_RCGEN = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--mode") && i + 1 < argc) strncpy(mode, argv[++i], 31);
        else if (!strcmp(argv[i], "-o") && i + 1 < argc) strncpy(G_OUT_PATH, argv[++i], 511);
        else if (!strcmp(argv[i], "--seed") && i + 1 < argc) strncpy(G_SEED_PATH, argv[++i], 511);
    }

    clock_gettime(CLOCK_MONOTONIC, &G_START_TS);

    // If G_OUT_PATH already exists and G_SEED_PATH is not set, load G_OUT_PATH as initial G_BEST_CODE and seed!
    if (G_OUT_PATH[0] != '\0' && G_SEED_PATH[0] == '\0' && access(G_OUT_PATH, F_OK) == 0) {
        strncpy(G_SEED_PATH, G_OUT_PATH, 511);
    }

    u64 *seed_words = NULL;
    int seed_n = 0;
    if (G_SEED_PATH[0] != '\0') {
        FILE *f = fopen(G_SEED_PATH, "r");
        if (f) {
            char line[128];
            int cap = 1024;
            seed_words = (u64 *)malloc(sizeof(u64) * cap);
            while (fgets(line, sizeof(line), f)) {
                u64 w;
                if (str_to_word(line, G_N, G_W, &w)) {
                    if (seed_n >= cap) {
                        cap *= 2;
                        seed_words = (u64 *)realloc(seed_words, sizeof(u64) * cap);
                    }
                    seed_words[seed_n++] = w;
                }
            }
            fclose(f);
            if (seed_n > 0 && verify_code_exact(seed_words, seed_n, G_N, G_D, G_W, G_RC)) {
                G_BEST_SIZE = seed_n;
                G_BEST_CODE = (u64 *)malloc(sizeof(u64) * seed_n);
                memcpy(G_BEST_CODE, seed_words, sizeof(u64) * seed_n);
                printf("[INIT] Loaded valid initial best code of size %d from %s\n", seed_n, G_SEED_PATH);
            }
        }
    }

    if (!strcmp(mode, "lns")) {
        build_universe(G_N, G_D, G_W, G_RC);
        pthread_t *ths = (pthread_t *)malloc(sizeof(pthread_t) * G_THREADS);
        worker_arg_t *args = (worker_arg_t *)malloc(sizeof(worker_arg_t) * G_THREADS);
        for (int t = 0; t < G_THREADS; t++) {
            args[t].tid = t;
            args[t].seed_words = seed_words;
            args[t].seed_n = seed_n;
            pthread_create(&ths[t], NULL, lns_worker, &args[t]);
        }
        for (int t = 0; t < G_THREADS; t++) pthread_join(ths[t], NULL);
        free(ths);
        free(args);
        free(G_UNIV);
        free(G_UNIV_RC);
    } else if (!strcmp(mode, "walksat")) {
        pthread_t *ths = (pthread_t *)malloc(sizeof(pthread_t) * G_THREADS);
        worker_arg_t *args = (worker_arg_t *)malloc(sizeof(worker_arg_t) * G_THREADS);
        for (int t = 0; t < G_THREADS; t++) {
            args[t].tid = t;
            args[t].seed_words = seed_words;
            args[t].seed_n = seed_n;
            pthread_create(&ths[t], NULL, walksat_worker, &args[t]);
        }
        for (int t = 0; t < G_THREADS; t++) pthread_join(ths[t], NULL);
        free(ths);
        free(args);
    } else if (!strcmp(mode, "orbit")) {
        pthread_t *ths = (pthread_t *)malloc(sizeof(pthread_t) * G_THREADS);
        worker_arg_t *args = (worker_arg_t *)malloc(sizeof(worker_arg_t) * G_THREADS);
        for (int t = 0; t < G_THREADS; t++) {
            args[t].tid = t;
            args[t].seed_words = seed_words;
            args[t].seed_n = seed_n;
            pthread_create(&ths[t], NULL, orbit_worker, &args[t]);
        }
        for (int t = 0; t < G_THREADS; t++) pthread_join(ths[t], NULL);
        free(ths);
        free(args);
    }

    printf("[DONE] Best %s(%d, %d, %d) = %d\n",
           G_RC ? "GC,RC" : "GC", G_N, G_D, G_W, G_BEST_SIZE);
    free(seed_words);
    free(G_BEST_CODE);
    return 0;
}
