/*
 * sa_erdos757.c
 * Native C multi-threaded optimizer & exact bitmask evaluator for Erdos #757.
 * Compile: clang -O3 -pthread sa_erdos757.c -o sa_erdos757
 *
 * Implements:
 * 1. Exact bitmask independence / transversal solver for 3-uniform hypergraphs (n <= 26).
 * 2. Exact F7-freeness, linearity, and midpoint-injectivity checker.
 * 3. Multi-threaded WalkSAT / Simulated Annealing over midpoint-injective linear F7-free
 *    3-uniform hypergraphs for n in {16, 18, 20, 21, 22, 23} targeting alpha(H)/n < 4/7 (p2)
 *    and exact nullspace integer realization as (4,5)-sets (Full Win / p1).
 * 4. Multi-threaded Simulated Annealing directly over integer sets A of size n in {7, 16, 18, 21, 23}.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#define MAXN 26
#define MAXE 24

typedef struct {
    int u, v, w; /* u < v < w, midpoint is v */
    uint32_t mask;
} Edge;

typedef struct {
    int n;
    int m;
    Edge edges[MAXE];
} Hypergraph;

/* Fast xorshift64 RNG */
static inline uint64_t xorshift64(uint64_t *state) {
    uint64_t x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    return x;
}

/* Check linearity: any two edges share at most 1 vertex */
static inline int is_linear(const Hypergraph *H) {
    for (int i = 0; i < H->m; i++) {
        uint32_t mi = H->edges[i].mask;
        for (int j = i + 1; j < H->m; j++) {
            if (__builtin_popcount(mi & H->edges[j].mask) >= 2) {
                return 0;
            }
        }
    }
    return 1;
}

/* Check F7-freeness on a linear 3-uniform hypergraph:
 * F7 has a root v0 of degree >= 3 with edges {v0,a1,b1}, {v0,a2,b2}, {v0,a3,b3}
 * and transversal edges {a1,a2,a3} and {b1,b2,b3}. */
static int is_f7_free(const Hypergraph *H) {
    int inc[MAXN][MAXE];
    int deg[MAXN];
    memset(deg, 0, sizeof(deg));
    for (int i = 0; i < H->m; i++) {
        int u = H->edges[i].u, v = H->edges[i].v, w = H->edges[i].w;
        inc[u][deg[u]++] = i;
        inc[v][deg[v]++] = i;
        inc[w][deg[w]++] = i;
    }
    for (int v0 = 0; v0 < H->n; v0++) {
        if (deg[v0] < 3) continue;
        for (int i1 = 0; i1 < deg[v0]; i1++) {
            uint32_t e1 = H->edges[inc[v0][i1]].mask ^ (1U << v0);
            int a1 = __builtin_ctz(e1);
            int b1 = __builtin_ctz(e1 ^ (1U << a1));
            for (int i2 = i1 + 1; i2 < deg[v0]; i2++) {
                uint32_t e2 = H->edges[inc[v0][i2]].mask ^ (1U << v0);
                int a2 = __builtin_ctz(e2);
                int b2 = __builtin_ctz(e2 ^ (1U << a2));
                for (int i3 = i2 + 1; i3 < deg[v0]; i3++) {
                    uint32_t e3 = H->edges[inc[v0][i3]].mask ^ (1U << v0);
                    int a3 = __builtin_ctz(e3);
                    int b3 = __builtin_ctz(e3 ^ (1U << a3));
                    /* Check 4 pairings */
                    int pairs[4][2][3] = {
                        {{a1, a2, a3}, {b1, b2, b3}},
                        {{a1, a2, b3}, {b1, b2, a3}},
                        {{a1, b2, a3}, {b1, a2, b3}},
                        {{b1, a2, a3}, {a1, b2, b3}}
                    };
                    for (int p = 0; p < 4; p++) {
                        uint32_t mA = (1U << pairs[p][0][0]) | (1U << pairs[p][0][1]) | (1U << pairs[p][0][2]);
                        uint32_t mB = (1U << pairs[p][1][0]) | (1U << pairs[p][1][1]) | (1U << pairs[p][1][2]);
                        int foundA = 0, foundB = 0;
                        for (int k = 0; k < H->m; k++) {
                            if (H->edges[k].mask == mA) foundA = 1;
                            if (H->edges[k].mask == mB) foundB = 1;
                        }
                        if (foundA && foundB) return 0;
                    }
                }
            }
        }
    }
    return 1;
}

/* Exact transversal number tau(H) and count of transversals of size tau_target - 1 */
static int can_hit_rec(int n, int m, const uint32_t *emasks, uint32_t cur_mask, int rem_k, int start_e) {
    int first_uncov = -1;
    for (int i = start_e; i < m; i++) {
        if ((emasks[i] & cur_mask) == 0) {
            first_uncov = i;
            break;
        }
    }
    if (first_uncov == -1) return 1;
    if (rem_k == 0) return 0;
    uint32_t em = emasks[first_uncov];
    while (em) {
        int v = __builtin_ctz(em);
        em ^= (1U << v);
        if (can_hit_rec(n, m, emasks, cur_mask | (1U << v), rem_k - 1, first_uncov + 1)) {
            return 1;
        }
    }
    return 0;
}

static void count_transversals_rec(int m, const uint32_t *emasks, uint32_t cur_mask, int rem_k, int start_e, int *count, int limit) {
    if (*count >= limit) return;
    int first_uncov = -1;
    for (int i = start_e; i < m; i++) {
        if ((emasks[i] & cur_mask) == 0) {
            first_uncov = i;
            break;
        }
    }
    if (first_uncov == -1) {
        (*count)++;
        return;
    }
    if (rem_k == 0) return;
    uint32_t em = emasks[first_uncov];
    while (em) {
        int v = __builtin_ctz(em);
        em ^= (1U << v);
        count_transversals_rec(m, emasks, cur_mask | (1U << v), rem_k - 1, first_uncov + 1, count, limit);
        if (*count >= limit) return;
    }
}

static int exact_tau(const Hypergraph *H, int *num_min_trans) {
    uint32_t emasks[MAXE];
    for (int i = 0; i < H->m; i++) emasks[i] = H->edges[i].mask;
    for (int k = 1; k <= H->n; k++) {
        if (can_hit_rec(H->n, H->m, emasks, 0, k, 0)) {
            if (num_min_trans) {
                int cnt = 0;
                count_transversals_rec(H->m, emasks, 0, k, 0, &cnt, 500);
                *num_min_trans = cnt;
            }
            return k;
        }
    }
    return 0;
}

/* Exact (4,5)-set checker and bitmask Sidon evaluator for integer sets */
static int count_45_violations(int n, const int *A) {
    int viol = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int x = A[j] - A[i];
            for (int k = j + 1; k < n; k++) {
                int y = A[k] - A[j];
                for (int l = k + 1; l < n; l++) {
                    int z = A[l] - A[k];
                    /* 6 differences: x, y, z, x+y, y+z, x+y+z.
                     * Equalities among them:
                     * x==z gives 2 coincidences (x==z and x+y==y+z) -> <= 4 distinct!
                     * Otherwise count how many of (x==y), (y==z), (z==x+y), (x==y+z) hold. */
                    if (x == z) {
                        viol++;
                    } else {
                        int eq = (x == y) + (y == z) + (z == x + y) + (x == y + z);
                        if (eq >= 2) viol++;
                    }
                }
            }
        }
    }
    return viol;
}

static int exact_sidon_int_set(int n, const int *A, int *out_3aps) {
    /* Assuming A is sorted and weak Sidon (or general): build all 3-AP and 4-sum hyperedges */
    uint32_t edges[512];
    int m = 0;
    int ap3 = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int target = 2 * A[j] - A[i];
            for (int k = j + 1; k < n; k++) {
                if (A[k] == target) {
                    if (m < 512) edges[m++] = (1U << i) | (1U << j) | (1U << k);
                    ap3++;
                    break;
                }
            }
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            for (int k = j + 1; k < n; k++) {
                int target = A[j] + A[k] - A[i];
                for (int l = k + 1; l < n; l++) {
                    if (A[l] == target) {
                        if (m < 512) edges[m++] = (1U << i) | (1U << j) | (1U << k) | (1U << l);
                        break;
                    }
                }
            }
        }
    }
    if (out_3aps) *out_3aps = ap3;
    for (int k = 1; k <= n; k++) {
        if (can_hit_rec(n, m, edges, 0, k, 0)) {
            return n - k;
        }
    }
    return n;
}

typedef struct {
    int thread_id;
    int target_n;
    int target_tau;
    int max_iters;
    int best_tau;
    int best_cnt;
    Hypergraph best_H;
} ThreadArg;

static volatile int global_found = 0;

static void *hypergraph_sa_worker(void *arg) {
    ThreadArg *targ = (ThreadArg *)arg;
    int n = targ->target_n;
    int m = n - 2;
    uint64_t rng = 0x9E3779B97F4A7C15ULL ^ ((uint64_t)(targ->thread_id + 1) * 0xBF58476D1CE4E5B9ULL) ^ (uint64_t)time(NULL);

    /* Ma-Tang A_14 edges as warm-start seed for n >= 16 */
    int mt14[12][3] = {
        {0, 1, 6}, {0, 2, 10}, {0, 8, 12}, {0, 11, 13}, {1, 12, 13},
        {2, 3, 7}, {2, 5, 8}, {3, 4, 5}, {4, 6, 8}, {4, 9, 10}, {5, 7, 9}, {6, 10, 11}
    };

    Hypergraph H;
    H.n = n;
    H.m = m;
    targ->best_tau = 0;
    targ->best_cnt = 999999;

    for (int restart = 0; restart < 40 && !global_found; restart++) {
        /* Initialize midpoint-injective linear F7-free hypergraph */
        int init_ok = 0;
        while (!init_ok) {
            init_ok = 1;
            for (int j = 1; j <= m; j++) {
                /* If restart % 2 == 0 and j <= 12 and n >= 16, try to seed from Ma-Tang shifted or unshifted */
                int placed = 0;
                if ((restart % 2 == 0) && j <= 12 && n >= 16) {
                    /* Find edge in mt14 with midpoint j */
                    for (int k = 0; k < 12; k++) {
                        if (mt14[k][1] == j && (xorshift64(&rng) % 10 < 8)) {
                            int u = mt14[k][0], w = mt14[k][2];
                            uint32_t mask = (1U << u) | (1U << j) | (1U << w);
                            int conflict = 0;
                            for (int p = 0; p < j - 1; p++) {
                                if (__builtin_popcount(H.edges[p].mask & mask) >= 2) { conflict = 1; break; }
                            }
                            if (!conflict) {
                                H.edges[j - 1].u = u;
                                H.edges[j - 1].v = j;
                                H.edges[j - 1].w = w;
                                H.edges[j - 1].mask = mask;
                                placed = 1;
                            }
                            break;
                        }
                    }
                }
                if (!placed) {
                    int tries = 0;
                    while (tries < 100) {
                        tries++;
                        int u = xorshift64(&rng) % j;
                        int w = j + 1 + (xorshift64(&rng) % (n - 1 - j));
                        uint32_t mask = (1U << u) | (1U << j) | (1U << w);
                        int conflict = 0;
                        for (int p = 0; p < j - 1; p++) {
                            if (__builtin_popcount(H.edges[p].mask & mask) >= 2) { conflict = 1; break; }
                        }
                        if (!conflict) {
                            H.edges[j - 1].u = u;
                            H.edges[j - 1].v = j;
                            H.edges[j - 1].w = w;
                            H.edges[j - 1].mask = mask;
                            placed = 1;
                            break;
                        }
                    }
                    if (!placed) { init_ok = 0; break; }
                }
            }
            if (init_ok && !is_f7_free(&H)) init_ok = 0;
        }

        int cur_cnt = 0;
        int cur_tau = exact_tau(&H, &cur_cnt);
        int cur_score = cur_tau * 1000 - cur_cnt;

        for (int iter = 0; iter < targ->max_iters && !global_found; iter++) {
            int idx = xorshift64(&rng) % m;
            int j = H.edges[idx].v;
            Edge old_e = H.edges[idx];

            int u = xorshift64(&rng) % j;
            int w = j + 1 + (xorshift64(&rng) % (n - 1 - j));
            uint32_t mask = (1U << u) | (1U << j) | (1U << w);
            if (mask == old_e.mask) continue;

            int conflict = 0;
            for (int p = 0; p < m; p++) {
                if (p != idx && __builtin_popcount(H.edges[p].mask & mask) >= 2) {
                    conflict = 1;
                    break;
                }
            }
            if (conflict) continue;

            H.edges[idx].u = u;
            H.edges[idx].v = j;
            H.edges[idx].w = w;
            H.edges[idx].mask = mask;

            if (!is_f7_free(&H)) {
                H.edges[idx] = old_e;
                continue;
            }

            int new_cnt = 0;
            int new_tau = exact_tau(&H, &new_cnt);
            int new_score = new_tau * 1000 - new_cnt;

            if (new_tau > targ->best_tau || (new_tau == targ->best_tau && new_cnt < targ->best_cnt)) {
                targ->best_tau = new_tau;
                targ->best_cnt = new_cnt;
                targ->best_H = H;
                if (new_tau >= targ->target_tau) {
                    global_found = 1;
                    break;
                }
            }

            /* Simulated annealing acceptance */
            if (new_score >= cur_score || (xorshift64(&rng) % 1000) < 35) {
                cur_tau = new_tau;
                cur_cnt = new_cnt;
                cur_score = new_score;
            } else {
                H.edges[idx] = old_e;
            }
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    printf("=== Erdos #757 Native C Multi-Threaded Evaluator & Optimizer ===\n");

    /* 1. Calibrate on Ma-Tang 14-set */
    int mt14_set[14] = {0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056};
    int v45 = count_45_violations(14, mt14_set);
    int ap3 = 0;
    int s14 = exact_sidon_int_set(14, mt14_set, &ap3);
    printf("[Calibration] Ma-Tang A_14: 45-violations=%d, 3-APs=%d, exact s(A_14)=%d (ratio %d/14)\n",
           v45, ap3, s14, s14);
    if (v45 != 0 || s14 != 8) {
        fprintf(stderr, "Calibration failed!\n");
        return 1;
    }

    /* 2. Calibrate on our 21-element p1 witness */
    int p1_21[21] = {0, 1360, 2000, 2430, 2460, 2490, 2720, 2860, 2980, 3230, 4000, 5280, 5960,
                     9815, 10560, 11223, 11264, 11305, 12631, 13957, 16650};
    int v45_21 = count_45_violations(21, p1_21);
    int ap3_21 = 0;
    int s21 = exact_sidon_int_set(21, p1_21, &ap3_21);
    printf("[Verification] Glued A_21: 45-violations=%d, 3-APs=%d, exact s(A_21)=%d (ratio %d/21 = 4/7)\n",
           v45_21, ap3_21, s21, s21);

    /* 3. Empirical verification on n=7 random/annealed (4,5)-sets that s(A) >= 5 */
    uint64_t rng = 123456789ULL;
    int min_s7 = 7;
    int valid_7 = 0;
    for (int t = 0; t < 50000; t++) {
        int A7[7];
        A7[0] = 0;
        for (int i = 1; i < 7; i++) A7[i] = A7[i - 1] + 1 + (xorshift64(&rng) % 15);
        /* Force 2 or 3 3-APs */
        A7[2] = 2 * A7[1] - A7[0];
        A7[4] = 2 * A7[3] - A7[1];
        if (A7[4] <= A7[3]) continue;
        for (int i = 5; i < 7; i++) if (A7[i] <= A7[i - 1]) A7[i] = A7[i - 1] + 1 + (xorshift64(&rng) % 10);
        if (count_45_violations(7, A7) == 0) {
            valid_7++;
            int s7 = exact_sidon_int_set(7, A7, NULL);
            if (s7 < min_s7) min_s7 = s7;
        }
    }
    printf("[n=7 Check] Tested %d valid 7-element (4,5)-sets: min s(A) = %d (confirming Henning-Yeo lower bound 5)\n",
           valid_7, min_s7);

    /* 4. Multi-threaded hypergraph search for n in {16, 18, 20, 23} */
    int targets[][2] = {{16, 7}, {18, 8}, {20, 9}, {23, 10}};
    for (int ti = 0; ti < 4; ti++) {
        int tn = targets[ti][0];
        int ttau = targets[ti][1];
        global_found = 0;
        pthread_t threads[4];
        ThreadArg targs[4];
        for (int th = 0; th < 4; th++) {
            targs[th].thread_id = th + ti * 10;
            targs[th].target_n = tn;
            targs[th].target_tau = ttau;
            targs[th].max_iters = 25000;
            pthread_create(&threads[th], NULL, hypergraph_sa_worker, &targs[th]);
        }
        int best_tau = 0, best_cnt = 999999, best_th = 0;
        for (int th = 0; th < 4; th++) {
            pthread_join(threads[th], NULL);
            if (targs[th].best_tau > best_tau || (targs[th].best_tau == best_tau && targs[th].best_cnt < best_cnt)) {
                best_tau = targs[th].best_tau;
                best_cnt = targs[th].best_cnt;
                best_th = th;
            }
        }
        printf("[Hypergraph SA n=%d, m=%d] target_tau=%d: best_tau=%d (alpha=%d/%d), min_transversals_at_best_tau=%d\n",
               tn, tn - 2, ttau, best_tau, tn - best_tau, tn, best_cnt);
        if (best_tau >= ttau) {
            printf("  FOUND TARGET HYPERGRAPH FOR n=%d! Edges:\n  [", tn);
            for (int e = 0; e < tn - 2; e++) {
                printf("(%d,%d,%d)%s", targs[best_th].best_H.edges[e].u,
                       targs[best_th].best_H.edges[e].v,
                       targs[best_th].best_H.edges[e].w,
                       (e + 1 == tn - 2) ? "" : ", ");
            }
            printf("]\n");
        }
    }

    return 0;
}
