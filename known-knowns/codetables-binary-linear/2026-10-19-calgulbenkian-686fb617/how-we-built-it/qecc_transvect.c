/*
 * qecc_transvect.c
 *
 * Quantum Stabilizer Code [[n, k, d]]_2 Record Hunter (p1) via:
 *   1. Toeplitz / Bordered Double-Circulant Seeding over GF(4)
 *   2. Weight-4 Unitary (Hermitian) Transvection Tabu / Simulated Annealing over GF(4)^n:
 *        T_v(x) = x + <x, v>_H * v   for wt(v) = 4  (preserves G G^dagger = 0 mod 2 and rank(G) = k4)
 *   3. Weight-2 and Weight-3 Binary Symplectic Transvection Climb in Sp(2n, GF(2)):
 *        T_v(x) = x ^ <x, v>_s * v   for wt_s(v) in {2, 3}
 *      (preserves X Z^T + Z X^T = 0 mod 2 and rank([X|Z]) = n - k, breaking GF(4)-symmetry
 *       to eliminate the final weight-(d-1) centralizer words!)
 *
 * Exact minimum distance d is computed at every step via bit-sliced Gray-code enumeration
 * + Exact Quantum MacWilliams Identity (Quaternary Krawtchouk Transform).
 */

#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"

#define MAX_N 64
#define MAX_K4 16
#define MAX_R 32

static const uint8_t GF4_ADD[4][4] = {
    {0,1,2,3}, {1,0,3,2}, {2,3,0,1}, {3,2,1,0}
};
static const uint8_t GF4_MUL[4][4] = {
    {0,0,0,0}, {0,1,2,3}, {0,2,3,1}, {0,3,1,2}
};
static const uint8_t GF4_CONJ[4] = {0, 1, 3, 2};

static int64_t KRAW4[12][MAX_N + 1];

static void init_kraw4(int n) {
    for (int i = 0; i <= n; i++) {
        KRAW4[0][i] = 1;
        if (n >= 1) KRAW4[1][i] = 3LL * n - 4LL * i;
        for (int j = 1; j < 11; j++) {
            int64_t t1 = (3LL * (n - j) + (int64_t)j - 4LL * i) * KRAW4[j][i];
            int64_t t2 = 3LL * (n - j + 1) * KRAW4[j - 1][i];
            KRAW4[j + 1][i] = (t1 - t2) / (j + 1);
        }
    }
}

static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return rng_state = x;
}

static inline uint8_t h_dot(const uint8_t *u, const uint8_t *v, int len) {
    uint8_t s = 0;
    for (int i = 0; i < len; i++) {
        if (u[i] && v[i]) s ^= GF4_MUL[u[i]][GF4_CONJ[v[i]]];
    }
    return s;
}

static uint32_t compute_sig(const uint8_t *a, int m, int k4) {
    uint32_t sig = 0;
    uint8_t w0 = h_dot(a, a, m) & 1;
    sig |= (uint32_t)w0;
    int max_s = (k4 - 1 < m - 1) ? (k4 - 1) : (m - 1);
    for (int s = 1; s <= max_s; s++) {
        uint8_t acc = 0;
        for (int c = 0; c < m; c++) {
            uint8_t u = a[c];
            uint8_t v = a[(c + s) % m];
            if (u && v) acc ^= GF4_MUL[u][GF4_CONJ[v]];
        }
        sig |= ((uint32_t)(acc & 3)) << (2 * s - 1);
    }
    return sig;
}

static uint32_t compute_sig_ones(int k4) {
    uint32_t sig = 1;
    for (int s = 1; s < k4; s++) {
        sig |= (1U << (2 * s - 1));
    }
    return sig;
}

static int check_rank_gf4(int k4, int n, const uint8_t G[MAX_K4][MAX_N]) {
    uint8_t M[MAX_K4][MAX_N];
    for (int i = 0; i < k4; i++) memcpy(M[i], G[i], n);
    int rank = 0;
    for (int col = 0; col < n && rank < k4; col++) {
        int piv = -1;
        for (int r = rank; r < k4; r++) {
            if (M[r][col] != 0) { piv = r; break; }
        }
        if (piv < 0) continue;
        if (piv != rank) {
            for (int c = col; c < n; c++) {
                uint8_t tmp = M[rank][c]; M[rank][c] = M[piv][c]; M[piv][c] = tmp;
            }
        }
        uint8_t inv = (M[rank][col] == 1) ? 1 : (M[rank][col] == 2 ? 3 : 2);
        for (int c = col; c < n; c++) M[rank][c] = GF4_MUL[M[rank][c]][inv];
        for (int r = 0; r < k4; r++) {
            if (r != rank && M[r][col] != 0) {
                uint8_t f = M[r][col];
                for (int c = col; c < n; c++) M[r][c] ^= GF4_MUL[f][M[rank][c]];
            }
        }
        rank++;
    }
    return rank;
}

static int verify_hermitian_self_orth(int k4, int n, const uint8_t G[MAX_K4][MAX_N]) {
    for (int i = 0; i < k4; i++) {
        for (int j = i; j < k4; j++) {
            if (h_dot(G[i], G[j], n) != 0) return 0;
        }
    }
    return 1;
}

/* Evaluate GF(4)-linear code and compute exact penalty for weights 1 .. d_target-1 */
static int64_t eval_gf4_penalty(int k4, int n, const uint8_t G[MAX_K4][MAX_N], int d_target, int *d_out) {
    uint64_t row_lo[MAX_K4][4], row_hi[MAX_K4][4];
    for (int i = 0; i < k4; i++) {
        uint64_t l1 = 0, h1 = 0;
        for (int c = 0; c < n; c++) {
            if (G[i][c] & 1) l1 |= (1ULL << c);
            if (G[i][c] & 2) h1 |= (1ULL << c);
        }
        row_lo[i][0] = 0;       row_hi[i][0] = 0;
        row_lo[i][1] = l1;      row_hi[i][1] = h1;
        row_lo[i][2] = h1;      row_hi[i][2] = l1 ^ h1;
        row_lo[i][3] = l1 ^ h1; row_hi[i][3] = l1;
    }

    int64_t A[MAX_N + 1];
    memset(A, 0, sizeof(A));
    A[0] = 1;

    uint64_t cw_lo = 0, cw_hi = 0;
    int coeff[MAX_K4];

    for (int lead = 0; lead < k4; lead++) {
        int rem = k4 - 1 - lead;
        cw_lo = row_lo[lead][1];
        cw_hi = row_hi[lead][1];
        for (int i = 0; i < rem; i++) coeff[i] = 0;

        while (1) {
            int w = __builtin_popcountll(cw_lo | cw_hi);
            A[w] += 3;

            int pos = 0;
            while (pos < rem) {
                int r_idx = lead + 1 + pos;
                int old_c = coeff[pos];
                int new_c = (old_c + 1) & 3;
                cw_lo ^= row_lo[r_idx][old_c] ^ row_lo[r_idx][new_c];
                cw_hi ^= row_hi[r_idx][old_c] ^ row_hi[r_idx][new_c];
                coeff[pos] = new_c;
                if (new_c != 0) break;
                pos++;
            }
            if (pos == rem) break;
        }
    }

    int64_t scale = 1LL << (2 * k4);
    int64_t pen = 0;
    int first_d = d_target;
    for (int j = 1; j < d_target; j++) {
        int64_t sum = 0;
        for (int i = 0; i <= n; i++) {
            if (A[i]) sum += A[i] * KRAW4[j][i];
        }
        int64_t diff = (sum / scale) - A[j];
        if (diff > 0) {
            if (first_d == d_target) first_d = j;
            int64_t mult = 1;
            for (int p = 0; p < (d_target - 1 - j); p++) mult *= 50000LL;
            pen += diff * mult;
        }
    }
    if (d_out) *d_out = first_d;
    return pen;
}

/* Evaluate general binary stabilizer code S of rank r = 2*k4 given by rx[0..r-1], rz[0..r-1] */
static int64_t eval_f2_stab_penalty(int r, int n, const uint64_t *rx, const uint64_t *rz, int d_target, int *d_out) {
    int64_t A[MAX_N + 1];
    memset(A, 0, sizeof(A));
    A[0] = 1;

    uint64_t cx = 0, cz = 0;
    uint32_t total = 1U << r;
    for (uint32_t i = 1; i < total; i++) {
        int bit = __builtin_ctz(i);
        cx ^= rx[bit];
        cz ^= rz[bit];
        int w = __builtin_popcountll(cx | cz);
        A[w]++;
    }

    int64_t scale = 1LL << r;
    int64_t pen = 0;
    int first_d = d_target;
    for (int j = 1; j < d_target; j++) {
        int64_t sum = 0;
        for (int i = 0; i <= n; i++) {
            if (A[i]) sum += A[i] * KRAW4[j][i];
        }
        int64_t diff = (sum / scale) - A[j];
        if (diff > 0) {
            if (first_d == d_target) first_d = j;
            int64_t mult = 1;
            for (int p = 0; p < (d_target - 1 - j); p++) mult *= 50000LL;
            pen += diff * mult;
        }
    }
    if (d_out) *d_out = first_d;
    return pen;
}

static int verify_f2_symplectic(int r, int n, const uint64_t *rx, const uint64_t *rz) {
    /* Check symplectic self-orthogonality */
    for (int i = 0; i < r; i++) {
        for (int j = i + 1; j < r; j++) {
            int s = (__builtin_popcountll(rx[i] & rz[j]) + __builtin_popcountll(rz[i] & rx[j])) & 1;
            if (s != 0) return 0;
        }
    }
    /* Check F2 rank = r */
    uint64_t mx[MAX_R], mz[MAX_R];
    for (int i = 0; i < r; i++) { mx[i] = rx[i]; mz[i] = rz[i]; }
    int rank = 0;
    for (int b = 0; b < 2 * n && rank < r; b++) {
        int piv = -1;
        for (int i = rank; i < r; i++) {
            uint64_t bit = (b < n) ? ((mx[i] >> b) & 1ULL) : ((mz[i] >> (b - n)) & 1ULL);
            if (bit) { piv = i; break; }
        }
        if (piv < 0) continue;
        uint64_t tx = mx[rank]; mx[rank] = mx[piv]; mx[piv] = tx;
        uint64_t tz = mz[rank]; mz[rank] = mz[piv]; mz[piv] = tz;
        for (int i = 0; i < r; i++) {
            if (i != rank) {
                uint64_t bit = (b < n) ? ((mx[i] >> b) & 1ULL) : ((mz[i] >> (b - n)) & 1ULL);
                if (bit) { mx[i] ^= mx[rank]; mz[i] ^= mz[rank]; }
            }
        }
        rank++;
    }
    return (rank == r);
}

static void save_f2_qecc_json(int n, int k, int r, int d, int d_lo, int d_up,
                              const uint64_t *rx, const uint64_t *rz, const char *desc) {
    char fname[256];
    snprintf(fname, sizeof(fname), "results/qecc_p1_n%d_k%d_d%d.json", n, k, d);
    FILE *fp = fopen(fname, "w");
    if (!fp) return;

    fprintf(fp, "{\n");
    fprintf(fp, "  \"kind\": \"qecc\",\n");
    fprintf(fp, "  \"n\": %d,\n", n);
    fprintf(fp, "  \"k\": %d,\n", k);
    fprintf(fp, "  \"d\": %d,\n", d);
    fprintf(fp, "  \"d_lo_codetables\": %d,\n", d_lo);
    fprintf(fp, "  \"d_up_codetables\": %d,\n", d_up);
    fprintf(fp, "  \"construction\": \"%s\",\n", desc);
    fprintf(fp, "  \"X\": [\n");
    for (int i = 0; i < r; i++) {
        fprintf(fp, "    [");
        for (int c = 0; c < n; c++) fprintf(fp, "%d%s", (int)((rx[i] >> c) & 1ULL), (c + 1 < n) ? "," : "");
        fprintf(fp, "]%s\n", (i + 1 < r) ? "," : "");
    }
    fprintf(fp, "  ],\n");
    fprintf(fp, "  \"Z\": [\n");
    for (int i = 0; i < r; i++) {
        fprintf(fp, "    [");
        for (int c = 0; c < n; c++) fprintf(fp, "%d%s", (int)((rz[i] >> c) & 1ULL), (c + 1 < n) ? "," : "");
        fprintf(fp, "]%s\n", (i + 1 < r) ? "," : "");
    }
    fprintf(fp, "  ]\n}\n");
    fclose(fp);
}

typedef struct {
    uint8_t a[32];
    uint32_t sig;
} PolyItem;

static int cmp_sig(const void *p1, const void *p2) {
    uint32_t s1 = ((const PolyItem *)p1)->sig;
    uint32_t s2 = ((const PolyItem *)p2)->sig;
    return (s1 > s2) - (s1 < s2);
}

static int hunt_qecc_cell(int n, int k, int d_lo, int d_up) {
    int r = n - k;
    int k4 = r / 2;
    int is_odd = n & 1;
    int m = n / 2;
    int d_target = d_lo + 1;

    init_kraw4(n);
    printf("[QECC-Transvect] Hunting [[%d, %d, >=%d]]_2 (r=%d, k4=%d, live=%d-%d)...\n",
           n, k, d_target, r, k4, d_lo, d_up);
    fflush(stdout);

    /* Step 1: Collect top 16 Toeplitz seeds */
    int pool_size = 120000;
    PolyItem *pool = (PolyItem *)malloc(pool_size * sizeof(PolyItem));
    for (int i = 0; i < pool_size; i++) {
        pool[i].a[0] = 1;
        for (int c = 1; c < m; c++) pool[i].a[c] = xorshift64() & 3;
        pool[i].sig = compute_sig(pool[i].a, m, k4);
    }
    qsort(pool, pool_size, sizeof(PolyItem), cmp_sig);

    uint32_t target_xor = is_odd ? compute_sig_ones(k4) : 0;
    uint8_t seeds[16][MAX_K4][MAX_N];
    int64_t seed_pen[16];
    int n_seeds = 0;
    for (int i = 0; i < 16; i++) seed_pen[i] = 0x7fffffffffffffffLL;

    int tested = 0;
    for (int i = 0; i < pool_size && tested < 40000; i++) {
        uint32_t want = pool[i].sig ^ target_xor;
        int lo = 0, hi = pool_size - 1, start = -1;
        while (lo <= hi) {
            int mid = (lo + hi) >> 1;
            if (pool[mid].sig >= want) {
                if (pool[mid].sig == want) start = mid;
                hi = mid - 1;
            } else lo = mid + 1;
        }
        if (start < 0) continue;
        for (int j = start; j < pool_size && pool[j].sig == want && tested < 40000; j++) {
            if (!is_odd && j <= i) continue;
            uint8_t G[MAX_K4][MAX_N];
            memset(G, 0, sizeof(G));
            for (int r_idx = 0; r_idx < k4; r_idx++) {
                for (int c = 0; c < m; c++) {
                    G[r_idx][(c + r_idx) % m] = pool[i].a[c];
                    G[r_idx][m + ((c + r_idx) % m)] = pool[j].a[c];
                }
                if (is_odd) G[r_idx][2 * m] = 1;
            }
            if (check_rank_gf4(k4, n, G) < k4) continue;
            tested++;
            int d_cur = 0;
            int64_t pen = eval_gf4_penalty(k4, n, G, d_target, &d_cur);
            if (pen == 0 && verify_hermitian_self_orth(k4, n, G)) {
                uint64_t rx[MAX_R], rz[MAX_R];
                for (int row = 0; row < k4; row++) {
                    rx[2 * row] = rz[2 * row] = rx[2 * row + 1] = rz[2 * row + 1] = 0;
                    for (int c = 0; c < n; c++) {
                        uint8_t v1 = G[row][c], v2 = GF4_MUL[2][v1];
                        if (v1 & 1) rx[2 * row] |= (1ULL << c);
                        if (v1 & 2) rz[2 * row] |= (1ULL << c);
                        if (v2 & 1) rx[2 * row + 1] |= (1ULL << c);
                        if (v2 & 2) rz[2 * row + 1] |= (1ULL << c);
                    }
                }
                printf("\n*** QUANTUM BREAKTHROUGH WIN (p1): [[%d, %d, %d]]_2 (Toeplitz) ***\n", n, k, d_target);
                save_f2_qecc_json(n, k, r, d_target, d_lo, d_up, rx, rz, "Toeplitz Hermitian self-orthogonal code");
                free(pool);
                return 1;
            }
            /* Insert into top 16 */
            if (n_seeds < 16 || pen < seed_pen[15]) {
                int pos = (n_seeds < 16) ? n_seeds++ : 15;
                seed_pen[pos] = pen;
                memcpy(seeds[pos], G, sizeof(G));
                while (pos > 0 && seed_pen[pos] < seed_pen[pos - 1]) {
                    int64_t tp = seed_pen[pos]; seed_pen[pos] = seed_pen[pos - 1]; seed_pen[pos - 1] = tp;
                    uint8_t tg[MAX_K4][MAX_N];
                    memcpy(tg, seeds[pos], sizeof(tg));
                    memcpy(seeds[pos], seeds[pos - 1], sizeof(tg));
                    memcpy(seeds[pos - 1], tg, sizeof(tg));
                    pos--;
                }
            }
        }
    }
    free(pool);
    printf("  Top Toeplitz seed penalty = %lld (from %d valid seeds)\n", (long long)seed_pen[0], n_seeds);
    fflush(stdout);

    /* Step 2: Weight-4 Hermitian Transvection Climb over GF(4) on top 8 seeds */
    for (int s_idx = 0; s_idx < 8 && s_idx < n_seeds; s_idx++) {
        uint8_t G[MAX_K4][MAX_N], best_G[MAX_K4][MAX_N];
        memcpy(G, seeds[s_idx], sizeof(G));
        memcpy(best_G, G, sizeof(G));
        int d_cur = 0;
        int64_t cur_pen = eval_gf4_penalty(k4, n, G, d_target, &d_cur);
        int64_t best_pen = cur_pen;

        for (int step = 0; step < 25000; step++) {
            /* Pick 4 distinct columns and 4 nonzero GF(4) values */
            int c0 = xorshift64() % n;
            int c1 = xorshift64() % n; while (c1 == c0) c1 = xorshift64() % n;
            int c2 = xorshift64() % n; while (c2 == c0 || c2 == c1) c2 = xorshift64() % n;
            int c3 = xorshift64() % n; while (c3 == c0 || c3 == c1 || c3 == c2) c3 = xorshift64() % n;
            uint8_t v0 = 1 + (xorshift64() % 3);
            uint8_t v1 = 1 + (xorshift64() % 3);
            uint8_t v2 = 1 + (xorshift64() % 3);
            uint8_t v3 = 1 + (xorshift64() % 3);

            uint8_t G_try[MAX_K4][MAX_N];
            memcpy(G_try, G, sizeof(G));
            for (int row = 0; row < k4; row++) {
                uint8_t dot = GF4_MUL[G[row][c0]][GF4_CONJ[v0]]
                            ^ GF4_MUL[G[row][c1]][GF4_CONJ[v1]]
                            ^ GF4_MUL[G[row][c2]][GF4_CONJ[v2]]
                            ^ GF4_MUL[G[row][c3]][GF4_CONJ[v3]];
                if (dot) {
                    G_try[row][c0] ^= GF4_MUL[dot][v0];
                    G_try[row][c1] ^= GF4_MUL[dot][v1];
                    G_try[row][c2] ^= GF4_MUL[dot][v2];
                    G_try[row][c3] ^= GF4_MUL[dot][v3];
                }
            }
            int d_try = 0;
            int64_t try_pen = eval_gf4_penalty(k4, n, G_try, d_target, &d_try);
            if (try_pen == 0 && verify_hermitian_self_orth(k4, n, G_try) && check_rank_gf4(k4, n, G_try) == k4) {
                uint64_t rx[MAX_R], rz[MAX_R];
                for (int row = 0; row < k4; row++) {
                    rx[2 * row] = rz[2 * row] = rx[2 * row + 1] = rz[2 * row + 1] = 0;
                    for (int c = 0; c < n; c++) {
                        uint8_t u1 = G_try[row][c], u2 = GF4_MUL[2][u1];
                        if (u1 & 1) rx[2 * row] |= (1ULL << c);
                        if (u1 & 2) rz[2 * row] |= (1ULL << c);
                        if (u2 & 1) rx[2 * row + 1] |= (1ULL << c);
                        if (u2 & 2) rz[2 * row + 1] |= (1ULL << c);
                    }
                }
                printf("\n*** QUANTUM BREAKTHROUGH WIN (p1): [[%d, %d, %d]]_2 (GF4 Unitary Transvection Climb, seed=%d, step=%d) ***\n",
                       n, k, d_target, s_idx, step);
                fflush(stdout);
                save_f2_qecc_json(n, k, r, d_target, d_lo, d_up, rx, rz,
                                  "GF(4) Hermitian self-orthogonal code via weight-4 unitary transvection climb");
                return 1;
            }
            if (try_pen < cur_pen || (try_pen == cur_pen && (xorshift64() & 1)) || (try_pen <= best_pen + 9 && (xorshift64() & 63) == 0)) {
                memcpy(G, G_try, sizeof(G));
                cur_pen = try_pen;
                if (cur_pen < best_pen) {
                    best_pen = cur_pen;
                    memcpy(best_G, G, sizeof(G));
                }
            }
        }
        memcpy(seeds[s_idx], best_G, sizeof(best_G));
        seed_pen[s_idx] = best_pen;
    }
    printf("  After GF(4) unitary transvections: best penalty = %lld\n", (long long)seed_pen[0]);
    fflush(stdout);

    /* Step 3: General Binary Symplectic Transvection Climb in Sp(2n, GF(2)) (if r <= 18) */
    if (r <= 18) {
        for (int s_idx = 0; s_idx < 6 && s_idx < n_seeds; s_idx++) {
            uint64_t rx[MAX_R], rz[MAX_R], best_rx[MAX_R], best_rz[MAX_R];
            for (int row = 0; row < k4; row++) {
                rx[2 * row] = rz[2 * row] = rx[2 * row + 1] = rz[2 * row + 1] = 0;
                for (int c = 0; c < n; c++) {
                    uint8_t u1 = seeds[s_idx][row][c], u2 = GF4_MUL[2][u1];
                    if (u1 & 1) rx[2 * row] |= (1ULL << c);
                    if (u1 & 2) rz[2 * row] |= (1ULL << c);
                    if (u2 & 1) rx[2 * row + 1] |= (1ULL << c);
                    if (u2 & 2) rz[2 * row + 1] |= (1ULL << c);
                }
            }
            memcpy(best_rx, rx, sizeof(rx));
            memcpy(best_rz, rz, sizeof(rz));
            int d_cur = 0;
            int64_t cur_pen = eval_f2_stab_penalty(r, n, rx, rz, d_target, &d_cur);
            int64_t best_pen = cur_pen;

            for (int step = 0; step < 30000; step++) {
                /* Generate random weight-2 or weight-3 symplectic vector v = (vx, vz) */
                int wt_v = (xorshift64() & 1) ? 2 : 3;
                uint64_t vx = 0, vz = 0;
                for (int w = 0; w < wt_v; w++) {
                    int c = xorshift64() % n;
                    int p = 1 + (xorshift64() % 3);
                    if (p & 1) vx |= (1ULL << c);
                    if (p & 2) vz |= (1ULL << c);
                }
                if ((vx | vz) == 0) continue;

                uint64_t try_rx[MAX_R], try_rz[MAX_R];
                for (int i = 0; i < r; i++) {
                    int s = (__builtin_popcountll(rx[i] & vz) + __builtin_popcountll(rz[i] & vx)) & 1;
                    try_rx[i] = s ? (rx[i] ^ vx) : rx[i];
                    try_rz[i] = s ? (rz[i] ^ vz) : rz[i];
                }
                int d_try = 0;
                int64_t try_pen = eval_f2_stab_penalty(r, n, try_rx, try_rz, d_target, &d_try);
                if (try_pen == 0 && verify_f2_symplectic(r, n, try_rx, try_rz)) {
                    printf("\n*** QUANTUM BREAKTHROUGH WIN (p1): [[%d, %d, %d]]_2 (Sp(2n,2) Transvection Climb, seed=%d, step=%d) ***\n",
                           n, k, d_target, s_idx, step);
                    fflush(stdout);
                    save_f2_qecc_json(n, k, r, d_target, d_lo, d_up, try_rx, try_rz,
                                      "Binary stabilizer code via Sp(2n, GF(2)) symplectic transvection climb");
                    return 1;
                }
                if (try_pen < cur_pen || (try_pen == cur_pen && (xorshift64() & 1)) || (try_pen <= best_pen + 4 && (xorshift64() & 31) == 0)) {
                    memcpy(rx, try_rx, sizeof(rx));
                    memcpy(rz, try_rz, sizeof(rz));
                    cur_pen = try_pen;
                    if (cur_pen < best_pen) {
                        best_pen = cur_pen;
                        memcpy(best_rx, rx, sizeof(rx));
                        memcpy(best_rz, rz, sizeof(rz));
                    }
                }
            }
            if (best_pen < seed_pen[0]) seed_pen[0] = best_pen;
        }
        printf("  After Sp(2n,2) symplectic transvections: best penalty = %lld\n", (long long)seed_pen[0]);
        fflush(stdout);
    }
    return 0;
}

int main(void) {
    hunt_qecc_cell(23, 9,  4, 6);
    hunt_qecc_cell(25, 7,  5, 7);
    hunt_qecc_cell(39, 23, 4, 6);
    hunt_qecc_cell(32, 18, 4, 5);
    hunt_qecc_cell(33, 19, 4, 5);
    hunt_qecc_cell(34, 20, 4, 6);
    return 0;
}
