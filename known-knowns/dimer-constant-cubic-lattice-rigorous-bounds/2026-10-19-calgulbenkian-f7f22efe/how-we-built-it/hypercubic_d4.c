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

#define MAX_N 28

typedef struct {
    int m1, m2, m3, N;
    int num_perms;
    int perms[1200][MAX_N];
    uint32_t nbr_bits[MAX_N][4];
    uint32_t nbr_mask[MAX_N];
    int32_t *orbit_id;
    uint32_t *orbits_by_k[MAX_N + 1];
    int num_orbits[MAX_N + 1];
} Grid4D;

static inline uint32_t apply_perm_mask(uint32_t mask, const int *perm) {
    uint32_t res = 0;
    while (mask) {
        int u = __builtin_ctz(mask);
        mask &= mask - 1;
        res |= (1U << perm[u]);
    }
    return res;
}

static void build_grid_4d(Grid4D *g, int m1, int m2, int m3) {
    g->m1 = m1; g->m2 = m2; g->m3 = m3;
    g->N = m1 * m2 * m3;
    int N = g->N;

    for (int x = 0; x < m1; x++) {
        for (int y = 0; y < m2; y++) {
            for (int z = 0; z < m3; z++) {
                int u = (x * m2 + y) * m3 + z;
                int v0 = u;
                int v1 = (((x + 1) % m1) * m2 + y) * m3 + z;
                int v2 = (x * m2 + ((y + 1) % m2)) * m3 + z;
                int v3 = (x * m2 + y) * m3 + ((z + 1) % m3);
                g->nbr_bits[u][0] = 1U << v0;
                g->nbr_bits[u][1] = 1U << v1;
                g->nbr_bits[u][2] = 1U << v2;
                g->nbr_bits[u][3] = 1U << v3;
                g->nbr_mask[u] = (1U << v0) | (1U << v1) | (1U << v2) | (1U << v3);
            }
        }
    }

    /* Precompute pure translations for verifying S_4 linear symmetries */
    int trans_perms[64][MAX_N];
    int num_trans = 0;
    for (int tx = 0; tx < m1; tx++) {
        for (int ty = 0; ty < m2; ty++) {
            for (int tz = 0; tz < m3; tz++) {
                for (int x = 0; x < m1; x++) {
                    for (int y = 0; y < m2; y++) {
                        for (int z = 0; z < m3; z++) {
                            int nx = (x + tx) % m1;
                            int ny = (y + ty) % m2;
                            int nz = (z + tz) % m3;
                            trans_perms[num_trans][(x * m2 + y) * m3 + z] = (nx * m2 + ny) * m3 + nz;
                        }
                    }
                }
                num_trans++;
            }
        }
    }

    /* S_4 permutations of (x, y, z, -x-y-z) */
    int s4[24][4];
    int n_s4 = 0;
    for (int a = 0; a < 4; a++)
        for (int b = 0; b < 4; b++) if (b != a)
            for (int c = 0; c < 4; c++) if (c != a && c != b)
                for (int d = 0; d < 4; d++) if (d != a && d != b && d != c) {
                    s4[n_s4][0] = a; s4[n_s4][1] = b; s4[n_s4][2] = c; s4[n_s4][3] = d;
                    n_s4++;
                }

    g->num_perms = 0;
    for (int p = 0; p < 24; p++) {
        int lin[MAX_N];
        uint32_t seen = 0;
        for (int x = 0; x < m1; x++) {
            for (int y = 0; y < m2; y++) {
                for (int z = 0; z < m3; z++) {
                    int coords[4] = {x, y, z, -x - y - z};
                    int nx = ((coords[s4[p][0]] % m1) + m1) % m1;
                    int ny = ((coords[s4[p][1]] % m2) + m2) % m2;
                    int nz = ((coords[s4[p][2]] % m3) + m3) % m3;
                    int nu = (nx * m2 + ny) * m3 + nz;
                    lin[(x * m2 + y) * m3 + z] = nu;
                    seen |= (1U << nu);
                }
            }
        }
        if (seen != (1U << N) - 1U) continue;
        /* Check if there exists a translation tau such that tau(lin(N(u))) == N(lin(u)) for all u */
        int valid = 0;
        for (int t = 0; t < num_trans; t++) {
            int ok = 1;
            for (int u = 0; u < N; u++) {
                uint32_t lhs = apply_perm_mask(apply_perm_mask(g->nbr_mask[u], lin), trans_perms[t]);
                uint32_t rhs = g->nbr_mask[lin[u]];
                if (lhs != rhs) { ok = 0; break; }
            }
            if (ok) { valid = 1; break; }
        }
        if (!valid) continue;

        for (int t = 0; t < num_trans; t++) {
            int *perm = g->perms[g->num_perms++];
            for (int u = 0; u < N; u++) {
                perm[u] = trans_perms[t][lin[u]];
            }
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
            uint32_t gmask = apply_perm_mask((uint32_t)mask, g->perms[p]);
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
            uint32_t gmask = apply_perm_mask((uint32_t)mask, g->perms[p]);
            g->orbit_id[gmask] = oid;
        }
    }
}

static void free_grid_4d(Grid4D *g) {
    free(g->orbit_id);
    for (int k = 0; k <= g->N; k++) free(g->orbits_by_k[k]);
}

static int order_vertices_4d(
    const Grid4D *g,
    uint32_t U,
    uint32_t *b0,
    uint32_t *b1,
    uint32_t *b2,
    uint32_t *b3,
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
        b3[step] = g->nbr_bits[u][3];
        bm[step] = g->nbr_mask[u];
    }
    future_reach[k] = 0;
    for (int r = k - 1; r >= 0; r--) {
        future_reach[r] = future_reach[r + 1] | bm[r];
    }
    return k;
}

static inline uint64_t dfs_count_ones_4d(
    int pos,
    int k,
    uint32_t used,
    const uint32_t * restrict b0,
    const uint32_t * restrict b1,
    const uint32_t * restrict b2,
    const uint32_t * restrict b3,
    const uint32_t * restrict bm,
    const uint32_t * restrict future_reach
) {
    if (pos == k - 1) {
        return (uint64_t)__builtin_popcount(bm[pos] & ~used);
    }
    if (pos == k - 2) {
        uint64_t total = 0;
        uint32_t last_m = bm[pos + 1];
        uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos], m3 = b3[pos];
        if (!(used & m0)) total += __builtin_popcount(last_m & ~(used | m0));
        if (!(used & m1)) total += __builtin_popcount(last_m & ~(used | m1));
        if (!(used & m2)) total += __builtin_popcount(last_m & ~(used | m2));
        if (!(used & m3)) total += __builtin_popcount(last_m & ~(used | m3));
        return total;
    }
    uint64_t total = 0;
    uint32_t rem = future_reach[pos + 1];
    uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos], m3 = b3[pos];
    if (!(used & m0)) {
        uint32_t nu = used | m0;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones_4d(pos + 1, k, nu, b0, b1, b2, b3, bm, future_reach);
    }
    if (!(used & m1)) {
        uint32_t nu = used | m1;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones_4d(pos + 1, k, nu, b0, b1, b2, b3, bm, future_reach);
    }
    if (!(used & m2)) {
        uint32_t nu = used | m2;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones_4d(pos + 1, k, nu, b0, b1, b2, b3, bm, future_reach);
    }
    if (!(used & m3)) {
        uint32_t nu = used | m3;
        if (__builtin_popcount(nu | rem) >= k)
            total += dfs_count_ones_4d(pos + 1, k, nu, b0, b1, b2, b3, bm, future_reach);
    }
    return total;
}

static inline void dfs_sum_4d(
    int pos,
    int k,
    uint32_t used,
    const uint32_t * restrict b0,
    const uint32_t * restrict b1,
    const uint32_t * restrict b2,
    const uint32_t * restrict b3,
    const uint32_t * restrict future_reach,
    uint32_t full_mask,
    const int32_t * restrict orbit_id,
    const u256 * restrict vec_in,
    u256 * restrict sum
) {
    if (pos == k - 1) {
        uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos], m3 = b3[pos];
        if (!(used & m0)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m0)]]);
        if (!(used & m1)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m1)]]);
        if (!(used & m2)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m2)]]);
        if (!(used & m3)) u256_add_inplace(sum, &vec_in[orbit_id[full_mask ^ (used | m3)]]);
        return;
    }
    uint32_t rem = future_reach[pos + 1];
    uint32_t m0 = b0[pos], m1 = b1[pos], m2 = b2[pos], m3 = b3[pos];
    if (!(used & m0)) {
        uint32_t nu = used | m0;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum_4d(pos + 1, k, nu, b0, b1, b2, b3, future_reach, full_mask, orbit_id, vec_in, sum);
    }
    if (!(used & m1)) {
        uint32_t nu = used | m1;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum_4d(pos + 1, k, nu, b0, b1, b2, b3, future_reach, full_mask, orbit_id, vec_in, sum);
    }
    if (!(used & m2)) {
        uint32_t nu = used | m2;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum_4d(pos + 1, k, nu, b0, b1, b2, b3, future_reach, full_mask, orbit_id, vec_in, sum);
    }
    if (!(used & m3)) {
        uint32_t nu = used | m3;
        if (__builtin_popcount(nu | rem) >= k)
            dfs_sum_4d(pos + 1, k, nu, b0, b1, b2, b3, future_reach, full_mask, orbit_id, vec_in, sum);
    }
}

typedef struct {
    const Grid4D *g;
    int k_from;
    int is_ones_input;
    const u256 *vec_in;
    u256 *vec_out;
    int next_idx;
} MulContext4D;

static void *mul_worker_4d(void *arg) {
    MulContext4D *ctx = (MulContext4D *)arg;
    const Grid4D *g = ctx->g;
    int N = g->N;
    uint32_t full_mask = (1U << N) - 1U;
    int k_from = ctx->k_from;
    int num_orbs = g->num_orbits[k_from];
    const uint32_t *orbs = g->orbits_by_k[k_from];
    const int32_t *orbit_id = g->orbit_id;
    const u256 *vec_in = ctx->vec_in;

    while (1) {
        int idx = __sync_fetch_and_add(&ctx->next_idx, 32);
        if (idx >= num_orbs) break;
        int end = idx + 32;
        if (end > num_orbs) end = num_orbs;

        for (int o = idx; o < end; o++) {
            uint32_t U = orbs[o];
            if (U == 0) {
                ctx->vec_out[o] = ctx->is_ones_input ? u256_from_u64(1) : vec_in[orbit_id[full_mask]];
                continue;
            }
            uint32_t b0[MAX_N], b1[MAX_N], b2[MAX_N], b3[MAX_N], bm[MAX_N], future_reach[MAX_N + 1];
            int k = order_vertices_4d(g, U, b0, b1, b2, b3, bm, future_reach);
            if (k == 0) {
                ctx->vec_out[o] = u256_zero();
                continue;
            }
            if (ctx->is_ones_input) {
                uint64_t cnt = dfs_count_ones_4d(0, k, 0, b0, b1, b2, b3, bm, future_reach);
                ctx->vec_out[o] = u256_from_u64(cnt);
            } else {
                u256 sum = u256_zero();
                dfs_sum_4d(0, k, 0, b0, b1, b2, b3, future_reach, full_mask, orbit_id, vec_in, &sum);
                ctx->vec_out[o] = sum;
            }
        }
    }
    return NULL;
}

static void multiply_step_4d(const Grid4D *g, int k_from, int is_ones_input, const u256 *vec_in, u256 *vec_out, int nthreads) {
    MulContext4D ctx;
    ctx.g = g;
    ctx.k_from = k_from;
    ctx.is_ones_input = is_ones_input;
    ctx.vec_in = vec_in;
    ctx.vec_out = vec_out;
    ctx.next_idx = 0;

    pthread_t threads[32];
    if (nthreads > 32) nthreads = 32;
    for (int t = 0; t < nthreads; t++) {
        pthread_create(&threads[t], NULL, mul_worker_4d, &ctx);
    }
    for (int t = 0; t < nthreads; t++) {
        pthread_join(threads[t], NULL);
    }
}

static void solve_4d_case(int m1, int m2, int m3, int max_p, int nthreads, const char *cert_filename) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    Grid4D g;
    build_grid_4d(&g, m1, m2, m3);
    int N = g.N;

    double max_bound_by_p[20];
    int argmax_sector_by_p[20];
    for (int p = 0; p <= max_p; p++) {
        max_bound_by_p[p] = 0.0;
        argmax_sector_by_p[p] = -1;
    }

    for (int i = N / 2; i >= 0; i--) {
        int dim_even = g.num_orbits[i];
        int dim_odd  = g.num_orbits[N - i];
        u256 *even_vec = (u256 *)malloc((size_t)dim_even * sizeof(u256));
        u256 *odd_vec  = (u256 *)malloc((size_t)dim_odd  * sizeof(u256));
        u256 *new_even = (u256 *)malloc((size_t)dim_even * sizeof(u256));

        for (int u = 0; u < dim_even; u++) even_vec[u] = u256_from_u64(1);

        for (int p = 0; p <= max_p; p++) {
            multiply_step_4d(&g, N - i, (p == 0), even_vec, odd_vec, nthreads);
            multiply_step_4d(&g, i, 0, odd_vec, new_even, nthreads);

            int best_u = 0;
            for (int u = 1; u < dim_even; u++) {
                if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[best_u], &even_vec[best_u]) > 0) {
                    best_u = u;
                }
            }
            double ratio = u256_to_double(&new_even[best_u]) / u256_to_double(&even_vec[best_u]);
            double val = log(ratio) / (2.0 * N);

            if (val > max_bound_by_p[p]) {
                max_bound_by_p[p] = val;
                argmax_sector_by_p[p] = i;
            }

            if (p == max_p && i == N / 2 && cert_filename != NULL) {
                FILE *fp = fopen(cert_filename, "w");
                if (fp) {
                    fprintf(fp, "# Exact integer Collatz-Wielandt certificate for 4D Dimer l_4 on (%d,%d,%d) sector i=%d (%d orbits) at p=%d\n",
                            m1, m2, m3, i, dim_even, p);
                    fprintf(fp, "# Certifies l_4 <= %.10f (ceil_6 = %.6f)\n", val, ceil(val * 1e6) / 1e6);
                    fprintf(fp, "# Format: orbit_id canonical_mask v_p (T*v_p)\n");
                    for (int u = 0; u < dim_even; u++) {
                        char s1[100], s2[100];
                        u256_to_dec(even_vec[u], s1);
                        u256_to_dec(new_even[u], s2);
                        fprintf(fp, "%d %u %s %s\n", u, g.orbits_by_k[i][u], s1, s2);
                    }
                    fclose(fp);
                }
            }

            if (i < N / 2 && val <= max_bound_by_p[max_p]) {
                break;
            }

            memcpy(even_vec, new_even, (size_t)dim_even * sizeof(u256));
        }

        free(even_vec);
        free(odd_vec);
        free(new_even);
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    double best = max_bound_by_p[max_p];
    printf("(%d,%d,%d) [N=%2d, |K|=%3d, max_orbits=%5d]: p=%d -> l_4 <= %.10f (ceil_6 = %.6f) [%.2fs]\n",
           m1, m2, m3, N, g.num_perms, g.num_orbits[N / 2], max_p, best, ceil(best * 1e6) / 1e6, elapsed);
    fflush(stdout);
    free_grid_4d(&g);
}

int main(void) {
    int nthreads = 14;
    printf("=== 4D HYPERCUBIC DIMER CONSTANT l_4 UPPER BOUNDS (Published: <= 0.66278769) ===\n");
    solve_4d_case(2, 2, 2, 4, nthreads, "results/cert_4d_222.txt");
    solve_4d_case(3, 2, 2, 4, nthreads, "results/cert_4d_322.txt");
    solve_4d_case(4, 2, 2, 4, nthreads, NULL);
    solve_4d_case(3, 3, 2, 4, nthreads, "results/cert_4d_332.txt");
    return 0;
}
