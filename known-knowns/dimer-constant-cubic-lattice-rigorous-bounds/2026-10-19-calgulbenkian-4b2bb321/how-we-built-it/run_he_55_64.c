/*
 * run_he_55_64.c
 * Ultra-fast multi-threaded C solver for Qidong He's (arXiv:2607.28810) Corollary 3.4
 * on all Table 2 cross-sections up to (5,5) and beyond ((6,4), (5,5) at p>=4).
 *
 * Key exact algorithmic optimizations:
 *   1. Greedy overlap-maximizing row ordering of U (permanent is row-permutation invariant),
 *      causing neighbor collisions at the top of the DFS tree.
 *   2. Register-only 2-level unrolled leaf counting for Y * 1 at p=0 (zero memory lookups).
 *   3. Future-reachability bitmask cardinality pruning (__builtin_popcount(nu | rem) >= k).
 *   4. Middle-sector-first evaluation (i = floor(N/2) down to 0) with exact monotone
 *      Collatz-Wielandt early stopping (Proposition 3.3: C_{q+1} <= C_q) for non-dominant
 *      sectors i < floor(N/2) once C_{m,n;p}^{(i)} <= C_{m,n;max_p}^{(floor(N/2))}.
 */
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "math.h"
#include "time.h"
#include "pthread.h"

typedef unsigned __int128 u128;

typedef struct {
    uint64_t w[4];
} u256;

static inline u256 u256_zero(void) {
    u256 r = {{0, 0, 0, 0}};
    return r;
}

static inline u256 u256_from_u64(uint64_t x) {
    u256 r = {{x, 0, 0, 0}};
    return r;
}

static inline void u256_add_inplace(u256 *a, const u256 *b) {
    u128 c = (u128)a->w[0] + b->w[0];
    a->w[0] = (uint64_t)c; c >>= 64;
    c += (u128)a->w[1] + b->w[1];
    a->w[1] = (uint64_t)c; c >>= 64;
    c += (u128)a->w[2] + b->w[2];
    a->w[2] = (uint64_t)c; c >>= 64;
    c += (u128)a->w[3] + b->w[3];
    a->w[3] = (uint64_t)c;
}

static int u256_cmp_ratio(const u256 *a, const u256 *b, const u256 *c, const u256 *d) {
    uint64_t ad[8] = {0}, cb[8] = {0};
    for (int i = 0; i < 4; i++) {
        u128 carry1 = 0, carry2 = 0;
        for (int j = 0; j < 4; j++) {
            u128 p1 = (u128)a->w[i] * (u128)d->w[j] + ad[i + j] + carry1;
            ad[i + j] = (uint64_t)p1;
            carry1 = p1 >> 64;

            u128 p2 = (u128)c->w[i] * (u128)b->w[j] + cb[i + j] + carry2;
            cb[i + j] = (uint64_t)p2;
            carry2 = p2 >> 64;
        }
        ad[i + 4] = (uint64_t)carry1;
        cb[i + 4] = (uint64_t)carry2;
    }
    for (int k = 7; k >= 0; k--) {
        if (ad[k] != cb[k]) return (ad[k] > cb[k]) ? 1 : -1;
    }
    return 0;
}

static double u256_to_double(const u256 *a) {
    return (double)a->w[0]
         + ldexp((double)a->w[1], 64)
         + ldexp((double)a->w[2], 128)
         + ldexp((double)a->w[3], 192);
}

#define MAX_N 30

typedef struct {
    int m, n, N;
    int num_perms;
    int perms[300][MAX_N];
    uint32_t nbr_bits[MAX_N][3];
    uint32_t nbr_mask[MAX_N];
    int32_t *orbit_id;
    uint32_t *orbits_by_k[MAX_N + 1];
    int num_orbits[MAX_N + 1];
} GridData;

static void build_grid(GridData *g, int m, int n) {
    g->m = m;
    g->n = n;
    g->N = m * n;
    int N = g->N;

    g->num_perms = 0;
    for (int tx = 0; tx < m; tx++) {
        for (int ty = 0; ty < n; ty++) {
            for (int type = 0; type < 6; type++) {
                if (type == 1 && m != n) continue;
                if (type == 2 && (n % m != 0)) continue;
                if (type == 3 && m != n) continue;
                if (type == 4 && (m % n != 0)) continue;
                if (type == 5 && m != n) continue;

                int *perm = g->perms[g->num_perms++];
                for (int x = 0; x < m; x++) {
                    for (int y = 0; y < n; y++) {
                        int nx = 0, ny = 0;
                        switch (type) {
                            case 0: nx = x; ny = y; break;
                            case 1: nx = y; ny = x; break;
                            case 2: nx = -x - y; ny = y; break;
                            case 3: nx = -x - y; ny = x; break;
                            case 4: nx = x; ny = -x - y; break;
                            case 5: nx = y; ny = -x - y; break;
                        }
                        nx = ((nx + tx) % m + m) % m;
                        ny = ((ny + ty) % n + n) % n;
                        perm[x * n + y] = nx * n + ny;
                    }
                }
            }
        }
    }

    for (int x = 0; x < m; x++) {
        for (int y = 0; y < n; y++) {
            int u = x * n + y;
            int v0 = u;
            int v1 = ((x + 1) % m) * n + y;
            int v2 = x * n + ((y + 1) % n);
            g->nbr_bits[u][0] = 1U << v0;
            g->nbr_bits[u][1] = 1U << v1;
            g->nbr_bits[u][2] = 1U << v2;
            g->nbr_mask[u] = (1U << v0) | (1U << v1) | (1U << v2);
        }
    }

    size_t total_masks = 1ULL << N;
    g->orbit_id = (int32_t *)malloc(total_masks * sizeof(int32_t));
    memset(g->orbit_id, -1, total_masks * sizeof(int32_t));
    for (int k = 0; k <= N; k++) g->num_orbits[k] = 0;

    for (size_t mask = 0; mask < total_masks; mask++) {
        if (g->orbit_id[mask] != -1) continue;
        int k = __builtin_popcount((unsigned)mask);
        int32_t oid = g->num_orbits[k]++;
        for (int p = 0; p < g->num_perms; p++) {
            const int *perm = g->perms[p];
            uint32_t gmask = 0;
            uint32_t tmp = (uint32_t)mask;
            while (tmp) {
                int u = __builtin_ctz(tmp);
                tmp &= tmp - 1;
                gmask |= (1U << perm[u]);
            }
            g->orbit_id[gmask] = oid;
        }
    }

    for (int k = 0; k <= N; k++) {
        g->orbits_by_k[k] = (uint32_t *)malloc((size_t)g->num_orbits[k] * sizeof(uint32_t));
        g->num_orbits[k] = 0;
    }
    memset(g->orbit_id, -1, total_masks * sizeof(int32_t));
    for (size_t mask = 0; mask < total_masks; mask++) {
        if (g->orbit_id[mask] != -1) continue;
        int k = __builtin_popcount((unsigned)mask);
        int32_t oid = g->num_orbits[k]++;
        g->orbits_by_k[k][oid] = (uint32_t)mask;
        for (int p = 0; p < g->num_perms; p++) {
            const int *perm = g->perms[p];
            uint32_t gmask = 0;
            uint32_t tmp = (uint32_t)mask;
            while (tmp) {
                int u = __builtin_ctz(tmp);
                tmp &= tmp - 1;
                gmask |= (1U << perm[u]);
            }
            g->orbit_id[gmask] = oid;
        }
    }
}

static void free_grid(GridData *g) {
    free(g->orbit_id);
    for (int k = 0; k <= g->N; k++) free(g->orbits_by_k[k]);
}

/* Order vertices of U to maximize neighbor overlap with already-placed vertices */
static int order_vertices_greedy(
    const GridData *g,
    uint32_t U,
    uint32_t *b0,
    uint32_t *b1,
    uint32_t *b2,
    uint32_t *bm,
    uint32_t *future_reach
) {
    int raw_u[MAX_N];
    int k = 0;
    uint32_t tmp = U;
    uint32_t all_nbrs = 0;
    while (tmp) {
        int u = __builtin_ctz(tmp);
        tmp &= tmp - 1;
        raw_u[k++] = u;
        all_nbrs |= g->nbr_mask[u];
    }
    if (__builtin_popcount(all_nbrs) < k) return 0;

    uint8_t picked[MAX_N] = {0};
    uint32_t placed_nbrs = 0;
    for (int step = 0; step < k; step++) {
        int best_idx = -1;
        int best_score = -1;
        for (int i = 0; i < k; i++) {
            if (picked[i]) continue;
            int u = raw_u[i];
            uint32_t m = g->nbr_mask[u];
            /* Primary score: overlap with already-placed vertices' neighbors */
            int overlap = __builtin_popcount(m & placed_nbrs) * 16;
            /* Secondary score: overlap with remaining unplaced vertices' neighbors */
            for (int j = 0; j < k; j++) {
                if (i != j && !picked[j]) {
                    overlap += __builtin_popcount(m & g->nbr_mask[raw_u[j]]);
                }
            }
            if (overlap > best_score) {
                best_score = overlap;
                best_idx = i;
            }
        }
        picked[best_idx] = 1;
        int u = raw_u[best_idx];
        placed_nbrs |= g->nbr_mask[u];
        b0[step] = g->nbr_bits[u][0];
        b1[step] = g->nbr_bits[u][1];
        b2[step] = g->nbr_bits[u][2];
        bm[step] = g->nbr_mask[u];
    }
    future_reach[k] = 0;
    for (int r = k - 1; r >= 0; r--) {
        future_reach[r] = future_reach[r + 1] | bm[r];
    }
    return k;
}

/* Register-only DFS for multiplying by the all-ones vector (counts valid matchings) */
static inline uint64_t dfs_count_ones(
    int pos,
    int k,
    uint32_t used,
    const uint32_t * restrict b0,
    const uint32_t * restrict b1,
    const uint32_t * restrict b2,
    const uint32_t * restrict bm,
    const uint32_t * restrict future_reach
) {
    if (pos == k - 1) {
        return (uint64_t)__builtin_popcount(bm[pos] & ~used);
    }
    if (pos == k - 2) {
        uint64_t total = 0;
        uint32_t last_m = bm[pos + 1];
        uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos];
        if (!(used & m0)) total += __builtin_popcount(last_m & ~(used | m0));
        if (!(used & m1)) total += __builtin_popcount(last_m & ~(used | m1));
        if (!(used & m2)) total += __builtin_popcount(last_m & ~(used | m2));
        return total;
    }
    uint64_t total = 0;
    uint32_t rem = future_reach[pos + 1];
    uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos];
    if (!(used & m0)) {
        uint32_t nu = used | m0;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones(pos + 1, k, nu, b0, b1, b2, bm, future_reach);
    }
    if (!(used & m1)) {
        uint32_t nu = used | m1;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones(pos + 1, k, nu, b0, b1, b2, bm, future_reach);
    }
    if (!(used & m2)) {
        uint32_t nu = used | m2;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones(pos + 1, k, nu, b0, b1, b2, bm, future_reach);
    }
    return total;
}

/* General 256-bit DFS for multiplying by arbitrary vec_in */
static inline void dfs_sum(
    int pos,
    int k,
    uint32_t used,
    const uint32_t * restrict b0,
    const uint32_t * restrict b1,
    const uint32_t * restrict b2,
    const uint32_t * restrict future_reach,
    uint32_t full_mask,
    const int32_t * restrict orbit_id,
    const u256 * restrict vec_in,
    u256 * restrict sum
) {
    if (pos == k - 1) {
        uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos];
        if (!(used & m0)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m0)]]);
        if (!(used & m1)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m1)]]);
        if (!(used & m2)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m2)]]);
        return;
    }
    uint32_t rem = future_reach[pos + 1];
    uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos];
    if (!(used & m0)) {
        uint32_t nu = used | m0;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum(pos + 1, k, nu, b0, b1, b2, future_reach, full_mask, orbit_id, vec_in, sum);
    }
    if (!(used & m1)) {
        uint32_t nu = used | m1;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum(pos + 1, k, nu, b0, b1, b2, future_reach, full_mask, orbit_id, vec_in, sum);
    }
    if (!(used & m2)) {
        uint32_t nu = used | m2;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum(pos + 1, k, nu, b0, b1, b2, future_reach, full_mask, orbit_id, vec_in, sum);
    }
}

typedef struct {
    const GridData *g;
    int k_from;
    int is_ones_input;
    const u256 *vec_in;
    u256 *vec_out;
    int next_idx;
} MulContext;

static void *mul_worker(void *arg) {
    MulContext *ctx = (MulContext *)arg;
    const GridData *g = ctx->g;
    int N = g->N;
    uint32_t full_mask = (1U << N) - 1U;
    int k_from = ctx->k_from;
    int num_orbs = g->num_orbits[k_from];
    const uint32_t *orbs = g->orbits_by_k[k_from];
    const int32_t *orbit_id = g->orbit_id;
    const u256 *vec_in = ctx->vec_in;

    while (1) {
        int idx = __sync_fetch_and_add(&ctx->next_idx, 64);
        if (idx >= num_orbs) break;
        int end = idx + 64;
        if (end > num_orbs) end = num_orbs;

        for (int o = idx; o < end; o++) {
            uint32_t U = orbs[o];
            if (U == 0) {
                ctx->vec_out[o] = ctx->is_ones_input ? u256_from_u64(1) : vec_in[orbit_id[full_mask]];
                continue;
            }
            uint32_t b0[MAX_N], b1[MAX_N], b2[MAX_N], bm[MAX_N], future_reach[MAX_N + 1];
            int k = order_vertices_greedy(g, U, b0, b1, b2, bm, future_reach);
            if (k == 0) {
                ctx->vec_out[o] = u256_zero();
                continue;
            }
            if (ctx->is_ones_input) {
                uint64_t cnt = dfs_count_ones(0, k, 0, b0, b1, b2, bm, future_reach);
                ctx->vec_out[o] = u256_from_u64(cnt);
            } else {
                u256 sum = u256_zero();
                dfs_sum(0, k, 0, b0, b1, b2, future_reach, full_mask, orbit_id, vec_in, &sum);
                ctx->vec_out[o] = sum;
            }
        }
    }
    return NULL;
}

static void multiply_step_mt(const GridData *g, int k_from, int is_ones_input, const u256 *vec_in, u256 *vec_out, int nthreads) {
    MulContext ctx;
    ctx.g = g;
    ctx.k_from = k_from;
    ctx.is_ones_input = is_ones_input;
    ctx.vec_in = vec_in;
    ctx.vec_out = vec_out;
    ctx.next_idx = 0;

    pthread_t threads[32];
    if (nthreads > 32) nthreads = 32;
    for (int t = 0; t < nthreads; t++) {
        pthread_create(&threads[t], NULL, mul_worker, &ctx);
    }
    for (int t = 0; t < nthreads; t++) {
        pthread_join(threads[t], NULL);
    }
}

static void solve_he_case(int m, int n, int max_p, int nthreads) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    GridData g;
    build_grid(&g, m, n);
    int N = g.N;

    double max_bound_by_p[20];
    int argmax_sector_by_p[20];
    for (int p = 0; p <= max_p; p++) {
        max_bound_by_p[p] = 0.0;
        argmax_sector_by_p[p] = -1;
    }

    /* Evaluate from i = N/2 down to 0 so the dominant sector i = N/2 sets the threshold */
    for (int i = N / 2; i >= 0; i--) {
        struct timespec si0, si1;
        clock_gettime(CLOCK_MONOTONIC, &si0);
        int dim_even = g.num_orbits[i];
        int dim_odd  = g.num_orbits[N - i];
        u256 *even_vec = (u256 *)malloc((size_t)dim_even * sizeof(u256));
        u256 *odd_vec  = (u256 *)malloc((size_t)dim_odd  * sizeof(u256));
        u256 *new_even = (u256 *)malloc((size_t)dim_even * sizeof(u256));

        for (int u = 0; u < dim_even; u++) even_vec[u] = u256_from_u64(1);

        double last_val = 0.0;
        int steps_run = 0;
        for (int p = 0; p <= max_p; p++) {
            multiply_step_mt(&g, N - i, (p == 0), even_vec, odd_vec, nthreads);
            multiply_step_mt(&g, i, 0, odd_vec, new_even, nthreads);

            int best_u = 0;
            for (int u = 1; u < dim_even; u++) {
                if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[best_u], &even_vec[best_u]) > 0) {
                    best_u = u;
                }
            }
            double ratio = u256_to_double(&new_even[best_u]) / u256_to_double(&even_vec[best_u]);
            double val = log(ratio) / (2.0 * N);
            last_val = val;
            steps_run = p;

            if (val > max_bound_by_p[p]) {
                max_bound_by_p[p] = val;
                argmax_sector_by_p[p] = i;
            }

            /*
             * By Proposition 3.3 (iterated Collatz-Wielandt monotonicity), C_{m,n;q}^{(i)} is
             * non-increasing in q. Thus if at step p, val <= max_bound_by_p[max_p] (already
             * established by sector N/2), then for all q >= p we have
             * C_{m,n;q}^{(i)} <= val <= max_bound_by_p[q], so sector i is strictly dominated!
             */
            if (i < N / 2 && val <= max_bound_by_p[max_p]) {
                break;
            }

            memcpy(even_vec, new_even, (size_t)dim_even * sizeof(u256));
        }

        clock_gettime(CLOCK_MONOTONIC, &si1);
        double sec_el = (si1.tv_sec - si0.tv_sec) + 1e-9 * (si1.tv_nsec - si0.tv_nsec);
        printf("  [(%d,%d) sector i=%2d, orbits=%6d] p=%d bound=%.10f (%.2fs)\n",
               m, n, i, dim_even, steps_run, last_val, sec_el);
        fflush(stdout);

        free(even_vec);
        free(odd_vec);
        free(new_even);
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);

    printf("Case (%d,%d) [N=%d, max_orbits=%d, total_time=%.2fs]:\n",
           m, n, N, g.num_orbits[N / 2], elapsed);
    for (int p = 0; p <= max_p; p++) {
        double up6 = ceil(max_bound_by_p[p] * 1e6) / 1e6;
        printf("  p=%d: bound = %.10f  (ceil_6 = %.6f) [sector i=%d]\n",
               p, max_bound_by_p[p], up6, argmax_sector_by_p[p]);
    }
    fflush(stdout);
    free_grid(&g);
}

int main(void) {
    int nthreads = 14;
    solve_he_case(5, 4, 4, nthreads);
    solve_he_case(5, 5, 4, nthreads);
    solve_he_case(6, 4, 4, nthreads);
    return 0;
}
