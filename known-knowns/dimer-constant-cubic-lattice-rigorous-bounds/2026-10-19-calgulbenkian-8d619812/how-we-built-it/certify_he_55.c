#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "math.h"
#include "pthread.h"
#include "time.h"

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

static void u256_to_dec(u256 a, char *buf) {
    if ((a.w[0] | a.w[1] | a.w[2] | a.w[3]) == 0) {
        strcpy(buf, "0");
        return;
    }
    char tmp[100];
    int pos = 0;
    while ((a.w[0] | a.w[1] | a.w[2] | a.w[3]) != 0) {
        u128 rem = 0;
        for (int i = 3; i >= 0; i--) {
            u128 cur = (rem << 64) | a.w[i];
            a.w[i] = (uint64_t)(cur / 10);
            rem = cur % 10;
        }
        tmp[pos++] = '0' + (int)rem;
    }
    for (int i = 0; i < pos; i++) buf[i] = tmp[pos - 1 - i];
    buf[pos] = '\0';
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
            int overlap = __builtin_popcount(m & placed_nbrs) * 16;
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

int main(void) {
    int nthreads = 14;
    GridData g;
    build_grid(&g, 5, 5);
    int N = g.N;
    int i = 12;
    int dim_even = g.num_orbits[i];
    int dim_odd  = g.num_orbits[N - i];

    printf("Built (5,5) GridData: N=%d, |K_5,5|=%d, sector i=12 orbits=%d\n", N, g.num_perms, dim_even);

    u256 *even_vec = (u256 *)malloc((size_t)dim_even * sizeof(u256));
    u256 *odd_vec  = (u256 *)malloc((size_t)dim_odd  * sizeof(u256));
    u256 *new_even = (u256 *)malloc((size_t)dim_even * sizeof(u256));

    for (int u = 0; u < dim_even; u++) even_vec[u] = u256_from_u64(1);

    /* Run up to p = 5 and save both p = 4 certificate and converged quantized certificate */
    for (int p = 0; p <= 5; p++) {
        multiply_step_mt(&g, N - i, (p == 0), even_vec, odd_vec, nthreads);
        multiply_step_mt(&g, i, 0, odd_vec, new_even, nthreads);

        int best_u = 0, worst_u = 0;
        for (int u = 1; u < dim_even; u++) {
            if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[best_u], &even_vec[best_u]) > 0)
                best_u = u;
            if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[worst_u], &even_vec[worst_u]) < 0)
                worst_u = u;
        }
        double r_max = u256_to_double(&new_even[best_u]) / u256_to_double(&even_vec[best_u]);
        double r_min = u256_to_double(&new_even[worst_u]) / u256_to_double(&even_vec[worst_u]);
        double ub = log(r_max) / (2.0 * N);
        double lb = log(r_min) / (2.0 * N);
        char num_s[100], den_s[100];
        u256_to_dec(new_even[best_u], num_s);
        u256_to_dec(even_vec[best_u], den_s);
        printf("  p=%d: l_3 <= %.10f (ceil_6 = %.6f), lb = %.10f, argmax_u=%d (%s / %s)\n",
               p, ub, ceil(ub * 1e6) / 1e6, lb, best_u, num_s, den_s);

        if (p == 4) {
            FILE *fp = fopen("results/cert_he_55_p4_sector12.txt", "w");
            fprintf(fp, "# Exact integer Collatz-Wielandt certificate for He (m,n)=(5,5), sector i=12 at p=4\n");
            fprintf(fp, "# Certifies l_3 <= %.10f (ceil_6 = %.6f)\n", ub, ceil(ub * 1e6) / 1e6);
            fprintf(fp, "# Format: orbit_id canonical_mask v_p4 (T*v_p4)\n");
            for (int u = 0; u < dim_even; u++) {
                char s1[100], s2[100];
                u256_to_dec(even_vec[u], s1);
                u256_to_dec(new_even[u], s2);
                fprintf(fp, "%d %u %s %s\n", u, g.orbits_by_k[i][u], s1, s2);
            }
            fclose(fp);
        }
        memcpy(even_vec, new_even, (size_t)dim_even * sizeof(u256));
    }

    /* Now converge further by rescaling to 52-bit positive integers and running 8 more iterations */
    for (int iter = 6; iter <= 14; iter++) {
        double max_d = 0.0;
        for (int u = 0; u < dim_even; u++) {
            double d = u256_to_double(&even_vec[u]);
            if (d > max_d) max_d = d;
        }
        const double SCALE = (double)(1ULL << 48);
        for (int u = 0; u < dim_even; u++) {
            double d = u256_to_double(&even_vec[u]);
            uint64_t q = (uint64_t)llround((d / max_d) * SCALE);
            if (q == 0) q = 1;
            even_vec[u] = u256_from_u64(q);
        }
        multiply_step_mt(&g, N - i, 0, even_vec, odd_vec, nthreads);
        multiply_step_mt(&g, i, 0, odd_vec, new_even, nthreads);

        int best_u = 0, worst_u = 0;
        for (int u = 1; u < dim_even; u++) {
            if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[best_u], &even_vec[best_u]) > 0)
                best_u = u;
            if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[worst_u], &even_vec[worst_u]) < 0)
                worst_u = u;
        }
        double r_max = u256_to_double(&new_even[best_u]) / u256_to_double(&even_vec[best_u]);
        double r_min = u256_to_double(&new_even[worst_u]) / u256_to_double(&even_vec[worst_u]);
        double ub = log(r_max) / (2.0 * N);
        double lb = log(r_min) / (2.0 * N);
        char num_s[100], den_s[100];
        u256_to_dec(new_even[best_u], num_s);
        u256_to_dec(even_vec[best_u], den_s);
        printf("  rescaled exact iter %2d: l_3 <= %.10f (ceil_6 = %.6f), lb = %.10f, argmax_u=%d (%s / %s)\n",
               iter, ub, ceil(ub * 1e6) / 1e6, lb, best_u, num_s, den_s);

        if (iter == 14) {
            FILE *fp = fopen("results/cert_he_55_converged_sector12.txt", "w");
            fprintf(fp, "# Converged 64-bit positive integer Collatz-Wielandt certificate for He (m,n)=(5,5), sector i=12\n");
            fprintf(fp, "# Certifies l_3 <= %.10f (ceil_6 = %.6f)\n", ub, ceil(ub * 1e6) / 1e6);
            fprintf(fp, "# Format: orbit_id canonical_mask x_u (T*x)_u\n");
            for (int u = 0; u < dim_even; u++) {
                char s1[100], s2[100];
                u256_to_dec(even_vec[u], s1);
                u256_to_dec(new_even[u], s2);
                fprintf(fp, "%d %u %s %s\n", u, g.orbits_by_k[i][u], s1, s2);
            }
            fclose(fp);
        }
        memcpy(even_vec, new_even, (size_t)dim_even * sizeof(u256));
    }

    free(even_vec);
    free(odd_vec);
    free(new_even);
    free_grid(&g);
    return 0;
}
