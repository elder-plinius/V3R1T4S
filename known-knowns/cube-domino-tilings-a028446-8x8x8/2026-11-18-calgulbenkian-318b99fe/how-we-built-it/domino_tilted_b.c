/*
 * domino_tilted_b.c — Engine 2 (Attempt 2, Zero-Shared-Code Independent Implementation)
 * Exact 3D Grid Perfect Matching Counter via:
 *   1. Full End-to-End Sweep (NO Meet-in-the-Middle)
 *   2. Non-Isomorphic Tilted Hyperplane Vertex Order B: (4x + 5y + 5z, x - y, z, x, y)
 *   3. Push-DP with Zero-State Skipping + Deferred uint16_t Atomic Accumulation
 *   4. Two Preallocated Anonymous mmap Buffers (strictly <= 2.15 GiB Peak RSS)
 *   5. 4-Byte L1-Resident Combinadic Rank Table (byte_rank[4][34][256])
 *   6. Disjoint Prime Set B: 15 distinct primes in [10909..21841]
 *      (Every vertex in monotone order 4x+5y+5z has <= 3 past neighbors, verified by
 *       hard runtime check; 3 * 21840 = 65520 < 65536 => zero uint16_t overflow;
 *       product of first 12 primes > 1.12e52 > 52x Bregman bound 2.13e50; 3 extra check primes!)
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <sys/mman.h>
#include <time.h>

#define MAX_NODES 512
#define MAX_FRONT 33
#define MAX_BUF_ELEMS 565722720ULL /* C(32, 15) */
#define NUM_PRIMES_B 15
#define THREAD_CAP 4

static const uint16_t PRIMES_B[NUM_PRIMES_B] = {
    21841, 21839, 21821, 21817, 21803,
    21799, 21787, 21773, 21767, 21757,
    21751, 21739, 21737, 21727, 10909
};

static uint64_t C_binom[MAX_FRONT + 2][MAX_FRONT + 2];
static uint8_t  pc8[256];
static uint32_t byte_rank[4][MAX_FRONT + 2][256];
static uint16_t *g_buf0 = NULL;
static uint16_t *g_buf1 = NULL;

static void setup_tables_and_buffers(void) {
    memset(C_binom, 0, sizeof(C_binom));
    for (int n = 0; n <= MAX_FRONT + 1; n++) {
        C_binom[n][0] = 1ULL;
        for (int k = 1; k <= n; k++) {
            C_binom[n][k] = C_binom[n - 1][k - 1] + C_binom[n - 1][k];
        }
    }
    for (int m = 0; m < 256; m++) {
        pc8[m] = (uint8_t)__builtin_popcount((unsigned)m);
    }
    for (int q = 0; q < 4; q++) {
        for (int cprev = 0; cprev <= MAX_FRONT; cprev++) {
            for (int m = 0; m < 256; m++) {
                uint32_t acc = 0;
                int k = cprev + 1;
                int tmp = m;
                while (tmp) {
                    int b = __builtin_ctz((unsigned)tmp);
                    int pos = 8 * q + b;
                    if (pos <= MAX_FRONT && k <= MAX_FRONT) {
                        acc += (uint32_t)C_binom[pos][k];
                    }
                    k++;
                    tmp &= tmp - 1;
                }
                byte_rank[q][cprev][m] = acc;
            }
        }
    }
    size_t bytes = (size_t)MAX_BUF_ELEMS * sizeof(uint16_t);
    g_buf0 = (uint16_t *)mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    g_buf1 = (uint16_t *)mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    if (g_buf0 == MAP_FAILED || g_buf1 == MAP_FAILED) {
        fprintf(stderr, "FATAL: mmap failed\n");
        exit(1);
    }
}

static inline size_t rank_4byte(uint32_t B) {
    uint8_t x0 = (uint8_t)(B & 0xFFU);
    uint8_t x1 = (uint8_t)((B >> 8) & 0xFFU);
    uint8_t x2 = (uint8_t)((B >> 16) & 0xFFU);
    uint8_t x3 = (uint8_t)((B >> 24) & 0xFFU);
    int c0 = pc8[x0];
    int c1 = c0 + pc8[x1];
    int c2 = c1 + pc8[x2];
    return (size_t)byte_rank[0][0][x0]
         + (size_t)byte_rank[1][c0][x1]
         + (size_t)byte_rank[2][c1][x2]
         + (size_t)byte_rank[3][c2][x3];
}

static uint64_t unrank_comb(int W, int K, size_t idx) {
    if (K == 0) return 0ULL;
    uint64_t mask = 0ULL;
    int k = K;
    for (int b = W - 1; b >= 0 && k > 0; b--) {
        uint64_t c = C_binom[b][k];
        if (idx >= c) {
            idx -= c;
            mask |= (1ULL << b);
            k--;
        }
    }
    return mask;
}

typedef struct {
    uint16_t *arr;
    size_t s, e;
} ZeroJob;

static void *zero_worker(void *arg) {
    ZeroJob *z = (ZeroJob *)arg;
    if (z->e > z->s) {
        memset(z->arr + z->s, 0, (z->e - z->s) * sizeof(uint16_t));
    }
    return NULL;
}

static void zero_parallel(uint16_t *arr, size_t sz, int nth) {
    if (sz < 262144 || nth <= 1) {
        memset(arr, 0, sz * sizeof(uint16_t));
        return;
    }
    pthread_t th[THREAD_CAP];
    ZeroJob jobs[THREAD_CAP];
    int T = (nth > THREAD_CAP) ? THREAD_CAP : nth;
    size_t ch = (sz + T - 1) / T;
    int act = 0;
    for (int i = 0; i < T; i++) {
        size_t s = (size_t)i * ch, e = s + ch;
        if (e > sz) e = sz;
        if (s >= e) break;
        jobs[i] = (ZeroJob){arr, s, e};
        pthread_create(&th[i], NULL, zero_worker, &jobs[i]);
        act++;
    }
    for (int i = 0; i < act; i++) pthread_join(th[i], NULL);
}

typedef struct {
    int W_old, K_old;
    int W_new, K_new;
    uint64_t even_old, even_new;
    uint64_t leave_mask;
    int n_drop;
    int drop_desc[6];
    int enters;
    int n_surv_nb;
    int surv_newpos[6];
} PushTransition;

static inline uint64_t compress_drops(uint64_t x, int n_drop, const int *drop_desc) {
    for (int i = 0; i < n_drop; i++) {
        int d = drop_desc[i];
        uint64_t lo = (d == 0) ? 0ULL : ((1ULL << d) - 1ULL);
        x = (x & lo) | ((x >> 1) & ~lo);
    }
    return x;
}

typedef struct {
    const uint16_t *cur;
    uint16_t *nxt;
    const PushTransition *tr;
    uint16_t mod;
    size_t s_idx;
    size_t e_idx;
} PushJob;

static void *push_worker(void *arg) {
    PushJob *job = (PushJob *)arg;
    const uint16_t *cur = job->cur;
    uint16_t *nxt = job->nxt;
    const PushTransition *tr = job->tr;
    const uint16_t mod = job->mod;
    const uint16_t mod2 = (uint16_t)(2U * mod);
    size_t idx = job->s_idx;
    const size_t e_idx = job->e_idx;
    if (idx >= e_idx) return NULL;

    const int K_old = tr->K_old;
    const uint64_t even_old = tr->even_old;
    const uint64_t even_new = tr->even_new;
    const uint64_t leave_mask = tr->leave_mask;
    const int n_drop = tr->n_drop;
    const int enters = tr->enters;
    const uint64_t enter_bit = enters ? (1ULL << (tr->W_new - 1)) : 0ULL;
    const int n_surv_nb = tr->n_surv_nb;
    uint64_t surv_bits[6];
    for (int i = 0; i < n_surv_nb; i++) surv_bits[i] = (1ULL << tr->surv_newpos[i]);

    uint64_t B = unrank_comb(tr->W_old, K_old, idx);
    for (; idx < e_idx; idx++) {
        uint16_t val = cur[idx];
        if (val != 0) {
            if (val >= mod2) val = (uint16_t)(val - mod2);
            if (val >= mod)  val = (uint16_t)(val - mod);
            if (val != 0) {
                uint64_t U_old = B ^ even_old;
                uint64_t ul = U_old & leave_mask;
                if (ul == 0ULL) {
                    uint64_t U_comp = compress_drops(U_old, n_drop, tr->drop_desc);
                    if (enters) {
                        uint32_t B_new = (uint32_t)((U_comp | enter_bit) ^ even_new);
                        __atomic_fetch_add(&nxt[rank_4byte(B_new)], val, __ATOMIC_RELAXED);
                    }
                    for (int q = 0; q < n_surv_nb; q++) {
                        if (U_comp & surv_bits[q]) {
                            uint32_t B_new = (uint32_t)((U_comp ^ surv_bits[q]) ^ even_new);
                            __atomic_fetch_add(&nxt[rank_4byte(B_new)], val, __ATOMIC_RELAXED);
                        }
                    }
                } else if ((ul & (ul - 1ULL)) == 0ULL) {
                    uint64_t U_comp = compress_drops(U_old ^ ul, n_drop, tr->drop_desc);
                    uint32_t B_new = (uint32_t)(U_comp ^ even_new);
                    __atomic_fetch_add(&nxt[rank_4byte(B_new)], val, __ATOMIC_RELAXED);
                }
            }
        }
        if (K_old > 0 && idx + 1 < e_idx) {
            int tz = __builtin_ctzll(B);
            uint64_t r = B + (1ULL << tz);
            B = (((r ^ B) >> (tz + 2))) | r;
        }
    }
    return NULL;
}

typedef struct {
    int x, y, z;
} Coord3;

static int cmp_tilted_order_b(const void *pa, const void *pb) {
    const Coord3 *a = (const Coord3 *)pa;
    const Coord3 *b = (const Coord3 *)pb;
    int wa = 4 * a->x + 5 * a->y + 5 * a->z;
    int wb = 4 * b->x + 5 * b->y + 5 * b->z;
    if (wa != wb) return wa - wb;
    int da = a->x - a->y, db = b->x - b->y;
    if (da != db) return da - db;
    if (a->z != b->z) return a->z - b->z;
    if (a->x != b->x) return a->x - b->x;
    return a->y - b->y;
}

static uint16_t solve_end2end_u16(int Lx, int Ly, int Lz, uint16_t mod, int n_threads) {
    int N = Lx * Ly * Lz;
    if (N == 0) return (uint16_t)(1U % mod);
    if (N & 1) return 0U;

    Coord3 ord[MAX_NODES];
    int pos_of[8][8][16];
    memset(pos_of, -1, sizeof(pos_of));
    int cnt = 0;
    for (int x = 0; x < Lx; x++)
        for (int y = 0; y < Ly; y++)
            for (int z = 0; z < Lz; z++)
                ord[cnt++] = (Coord3){x, y, z};

    qsort(ord, N, sizeof(Coord3), cmp_tilted_order_b);
    for (int i = 0; i < N; i++) {
        pos_of[ord[i].x][ord[i].y][ord[i].z] = i;
    }

    int adj_cnt[MAX_NODES];
    int adj_list[MAX_NODES][6];
    int max_nb[MAX_NODES];
    const int dx[6] = {-1, 1, 0, 0, 0, 0};
    const int dy[6] = {0, 0, -1, 1, 0, 0};
    const int dz[6] = {0, 0, 0, 0, -1, 1};
    for (int i = 0; i < N; i++) {
        int d = 0, mx = -1;
        for (int k = 0; k < 6; k++) {
            int nx = ord[i].x + dx[k], ny = ord[i].y + dy[k], nz = ord[i].z + dz[k];
            if (nx >= 0 && nx < Lx && ny >= 0 && ny < Ly && nz >= 0 && nz < Lz) {
                int j = pos_of[nx][ny][nz];
                adj_list[i][d++] = j;
                if (j > mx) mx = j;
            }
        }
        adj_cnt[i] = d;
        max_nb[i] = mx;
    }

    int F_cur[MAX_FRONT], W_cur = 0, K_cur = 0;
    uint64_t even_cur = 0ULL;
    int odd_seen = 0, even_seen = 0;

    uint16_t *cur = g_buf0;
    uint16_t *nxt = g_buf1;
    cur[0] = 1U;

    for (int t = 0; t < N; t++) {
        int v_par = (ord[t].x + ord[t].y + ord[t].z) & 1;
        if (v_par) odd_seen++; else even_seen++;

        PushTransition tr;
        memset(&tr, 0, sizeof(tr));
        tr.W_old = W_cur;
        tr.K_old = K_cur;
        tr.even_old = even_cur;

        int F_new[MAX_FRONT], W_new = 0;
        int drops_asc[6], nd = 0;
        for (int j = 0; j < W_cur; j++) {
            int u = F_cur[j];
            if (max_nb[u] > t) {
                int np = W_new;
                F_new[W_new++] = u;
                for (int k = 0; k < adj_cnt[t]; k++) {
                    if (adj_list[t][k] == u) {
                        tr.surv_newpos[tr.n_surv_nb++] = np;
                        break;
                    }
                }
            } else {
                tr.leave_mask |= (1ULL << j);
                drops_asc[nd++] = j;
            }
        }
        if (nd + tr.n_surv_nb > 3) {
            fprintf(stderr, "FATAL: >3 past neighbors (%d)\n", nd + tr.n_surv_nb);
            exit(1);
        }
        tr.n_drop = nd;
        for (int i = 0; i < nd; i++) {
            tr.drop_desc[i] = drops_asc[nd - 1 - i];
        }
        tr.enters = (max_nb[t] > t) ? 1 : 0;
        if (tr.enters) {
            F_new[W_new++] = t;
        }
        if (W_new > MAX_FRONT) {
            fprintf(stderr, "FATAL Engine 2: W_new=%d > MAX_FRONT\n", W_new);
            exit(1);
        }

        int we = 0;
        uint64_t even_new = 0ULL;
        for (int j = 0; j < W_new; j++) {
            int u = F_new[j];
            if (((ord[u].x + ord[u].y + ord[u].z) & 1) == 0) {
                we++;
                even_new |= (1ULL << j);
            }
        }
        int K_new = (odd_seen - even_seen) + we;
        if (K_new < 0 || K_new > W_new) {
            return 0U;
        }
        tr.W_new = W_new;
        tr.K_new = K_new;
        tr.even_new = even_new;

        size_t sz_old = (size_t)C_binom[W_cur][K_cur];
        size_t sz_new = (size_t)C_binom[W_new][K_new];
        if (sz_new > MAX_BUF_ELEMS) {
            fprintf(stderr, "FATAL: sz_new=%zu > MAX_BUF_ELEMS\n", sz_new);
            exit(1);
        }
        zero_parallel(nxt, sz_new, n_threads);

        if (sz_old < 65536 || n_threads <= 1) {
            PushJob job = { cur, nxt, &tr, mod, 0, sz_old };
            push_worker(&job);
        } else {
            pthread_t th[THREAD_CAP];
            PushJob jobs[THREAD_CAP];
            int T = (n_threads > THREAD_CAP) ? THREAD_CAP : n_threads;
            size_t chunk = (sz_old + T - 1) / T;
            int act = 0;
            for (int i = 0; i < T; i++) {
                size_t s = (size_t)i * chunk;
                size_t e = s + chunk;
                if (e > sz_old) e = sz_old;
                if (s >= e) break;
                jobs[i] = (PushJob){ cur, nxt, &tr, mod, s, e };
                pthread_create(&th[i], NULL, push_worker, &jobs[i]);
                act++;
            }
            for (int i = 0; i < act; i++) pthread_join(th[i], NULL);
        }

        uint16_t *tmp = cur; cur = nxt; nxt = tmp;
        memcpy(F_cur, F_new, W_new * sizeof(int));
        W_cur = W_new;
        K_cur = K_new;
        even_cur = even_new;
    }

    return cur[0] % mod;
}

typedef struct {
    uint32_t limbs[32];
    int n;
} DecBig;

static void db_set(DecBig *x, uint32_t v) {
    memset(x, 0, sizeof(*x));
    x->limbs[0] = v % 10000U;
    x->limbs[1] = v / 10000U;
    x->n = (x->limbs[1] > 0) ? 2 : 1;
}
static uint16_t db_mod(const DecBig *x, uint16_t m) {
    uint32_t r = 0;
    for (int i = x->n - 1; i >= 0; i--) r = (r * 10000U + x->limbs[i]) % m;
    return (uint16_t)r;
}
static void db_mul_small(DecBig *x, uint16_t m) {
    uint32_t c = 0;
    for (int i = 0; i < x->n; i++) {
        uint32_t v = x->limbs[i] * (uint32_t)m + c;
        x->limbs[i] = v % 10000U;
        c = v / 10000U;
    }
    while (c > 0) {
        x->limbs[x->n++] = c % 10000U;
        c /= 10000U;
    }
}
static void db_add_prod(DecBig *x, const DecBig *M, uint16_t t) {
    uint32_t c = 0;
    int lim = (x->n > M->n + 2) ? x->n : (M->n + 2);
    for (int i = 0; i < lim; i++) {
        uint32_t xv = (i < x->n) ? x->limbs[i] : 0;
        uint32_t mv = (i < M->n) ? M->limbs[i] : 0;
        uint32_t v = xv + mv * (uint32_t)t + c;
        x->limbs[i] = v % 10000U;
        c = v / 10000U;
    }
    x->n = lim;
    while (x->n > 1 && x->limbs[x->n - 1] == 0) x->n--;
}
static void db_format(const DecBig *x, char *out) {
    int p = sprintf(out, "%u", x->limbs[x->n - 1]);
    for (int i = x->n - 2; i >= 0; i--) p += sprintf(out + p, "%04u", x->limbs[i]);
}
static uint16_t inv_mod16(uint16_t a, uint16_t p) {
    uint32_t r = 1, b = a % p, e = p - 2;
    while (e > 0) {
        if (e & 1) r = (r * b) % p;
        b = (b * b) % p;
        e >>= 1;
    }
    return (uint16_t)r;
}
static void garner_u16(int k, const uint16_t *primes, const uint16_t *rems, DecBig *out) {
    DecBig X, M;
    db_set(&X, rems[0]);
    db_set(&M, primes[0]);
    for (int i = 1; i < k; i++) {
        uint16_t p = primes[i];
        uint16_t xm = db_mod(&X, p);
        uint16_t mm = db_mod(&M, p);
        uint16_t diff = (rems[i] >= xm) ? (rems[i] - xm) : (uint16_t)(rems[i] + p - xm);
        uint16_t t = (uint16_t)(((uint32_t)diff * inv_mod16(mm, p)) % p);
        db_add_prod(&X, &M, t);
        db_mul_small(&M, p);
    }
    *out = X;
}

static double wall_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static void run_exact_b(int Lx, int Ly, int Lz, int np, int nth, char *dec_out) {
    uint16_t rems[NUM_PRIMES_B];
    for (int i = 0; i < np; i++) {
        rems[i] = solve_end2end_u16(Lx, Ly, Lz, PRIMES_B[i], nth);
    }
    DecBig ans;
    garner_u16(np, PRIMES_B, rems, &ans);
    db_format(&ans, dec_out);
}

int main(int argc, char **argv) {
    setup_tables_and_buffers();
    int mode_667 = (argc > 1 && strcmp(argv[1], "--solve-667") == 0);
    int nth = 4;

    printf("=== Engine 2 (Zero-Shared-Code End-to-End Push-DP u16, Tilted Order B) ===\n");
    double t0 = wall_sec();
    struct { int x, y, z, np; const char *label, *exp; } cal[] = {
        {2, 2, 2,  1, "A028446(1) = P_2^3", "9"},
        {4, 4, 4,  3, "A028446(2) = P_4^3", "5051532105"},
        {4, 4, 1,  1, "A028454(1) = P_4xP_4xP_1", "36"},
        {4, 4, 2,  2, "A028454(2) = P_4xP_4xP_2", "32000"},
        {4, 4, 3,  2, "A028454(3) = P_4xP_4xP_3", "10885344"},
        {4, 4, 5,  3, "A028454(5) = P_4xP_4xP_5", "2132137503232"},
        {4, 4, 6,  4, "A028454(6) = P_4xP_4xP_6", "932814464901633"},
        {6, 4, 4,  4, "A028454(6) = P_6xP_4xP_4", "932814464901633"},
        {4, 4, 7,  5, "A028454(7) = P_4xP_4xP_7", "403325499406267520"},
        {6, 6, 0,  1, "A049507(0) = P_6xP_6xP_0", "1"},
        {6, 6, 1,  1, "A049507(1) = P_6xP_6xP_1", "6728"},
        {6, 6, 2,  3, "A049507(2) = P_6xP_6xP_2", "53786626921"},
        {6, 6, 3,  4, "A049507(3) = P_6xP_6xP_3", "57248060375968384"},
        {6, 6, 4,  6, "A049507(4) = P_6xP_6xP_4", "123115692449982216049513"},
        {6, 6, 5,  7, "A049507(5) = P_6xP_6xP_5", "216388579168758145017797108072"},
        {6, 6, 6,  9, "A028446(3) = A049507(6) = P_6^3", "417898687046465734392674187695263185"},
    };
    int n_cal = (int)(sizeof(cal) / sizeof(cal[0]));
    char buf[256];
    for (int i = 0; i < n_cal; i++) {
        double ts = wall_sec();
        run_exact_b(cal[i].x, cal[i].y, cal[i].z, cal[i].np, nth, buf);
        double te = wall_sec();
        int ok = (strcmp(buf, cal[i].exp) == 0);
        printf("[%s] %-34s = %s (%.3fs)\n", ok ? "OK" : "FAIL", cal[i].label, buf, te - ts);
        if (!ok) {
            fprintf(stderr, "CALIBRATION MISMATCH: expected %s got %s\n", cal[i].exp, buf);
            return 1;
        }
    }
    printf("All %d Engine 2 calibration checks PASSED in %.3fs.\n", n_cal, wall_sec() - t0);
    fflush(stdout);

    if (mode_667) {
        printf("\n--- Computing A049507(7) = M(P_6 x P_6 x P_7) across %d primes in Prime Set B ---\n", NUM_PRIMES_B);
        uint16_t rems[NUM_PRIMES_B];
        for (int i = 0; i < NUM_PRIMES_B; i++) {
            double ts = wall_sec();
            rems[i] = solve_end2end_u16(6, 6, 7, PRIMES_B[i], nth);
            double te = wall_sec();
            printf("  Prime B[%2d] = %u -> residue = %5u (%.3fs)\n", i, PRIMES_B[i], rems[i], te - ts);
            fflush(stdout);
        }
        DecBig ans10, ans12, ans15;
        char s10[256], s12[256], s15[256];
        garner_u16(10, PRIMES_B, rems, &ans10);
        garner_u16(12, PRIMES_B, rems, &ans12);
        garner_u16(NUM_PRIMES_B, PRIMES_B, rems, &ans15);
        db_format(&ans10, s10);
        db_format(&ans12, s12);
        db_format(&ans15, s15);
        printf("CRT(10 primes) = %s\n", s10);
        printf("CRT(12 primes) = %s\n", s12);
        printf("CRT(15 primes) = %s\n", s15);
        if (strcmp(s10, s15) != 0 || strcmp(s12, s15) != 0) {
            fprintf(stderr, "FATAL: Engine 2 overdetermined CRT mismatch!\n");
            return 1;
        }
        printf("OVERDETERMINED 5-PRIME CHECK: PASS (primes 11..15 match 10-prime & 12-prime Bregman CRT identically!)\n");
        printf("RESULT A049507(7) = %s\n", s15);
    }
    return 0;
}
