/*
 * test_he_speed.c
 * Fast C implementation of Qidong He's (arXiv:2607.28810) Corollary 3.4
 * for upper bounding the 3D cubic lattice dimer constant l_3.
 */
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "math.h"
#include "time.h"
#include "pthread.h"

typedef unsigned __int128 u128;

/* 256-bit unsigned integer for exact arithmetic at p >= 4 */
typedef struct {
    uint64_t w[4]; /* w[0] is LSW, w[3] is MSW */
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
    u128 c = 0;
    for (int i = 0; i < 4; i++) {
        c += (u128)a->w[i] + (u128)b->w[i];
        a->w[i] = (uint64_t)c;
        c >>= 64;
    }
}

/* Compare a/b vs c/d by exact cross-multiplication a*d vs c*b (512-bit product) */
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
    int32_t *orbit_id;       /* size 2^N */
    uint32_t *orbits_by_k[MAX_N + 1];
    int num_orbits[MAX_N + 1];
} GridData;

static void build_grid(GridData *g, int m, int n) {
    g->m = m;
    g->n = n;
    g->N = m * n;
    int N = g->N;

    /* Build K_{m,n} maps as in Table 1 of He (arXiv:2607.28810) */
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
        }
    }

    size_t total_masks = 1ULL << N;
    g->orbit_id = (int32_t *)malloc(total_masks * sizeof(int32_t));
    memset(g->orbit_id, -1, total_masks * sizeof(int32_t));
    for (int k = 0; k <= N; k++) g->num_orbits[k] = 0;

    /* First pass: identify orbit representatives and counts */
    for (size_t mask = 0; mask < total_masks; mask++) {
        if (g->orbit_id[mask] != -1) continue;
        int k = __builtin_popcount((unsigned)mask);
        int32_t oid = g->num_orbits[k]++;
        /* Apply all group elements */
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
    /* Reset and record canonical representatives */
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

typedef struct {
    const GridData *g;
    int k_from;
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
                ctx->vec_out[o] = vec_in[orbit_id[full_mask]];
                continue;
            }
            uint32_t b0[MAX_N], b1[MAX_N], b2[MAX_N];
            int k = 0;
            uint32_t tmp = U;
            while (tmp) {
                int u = __builtin_ctz(tmp);
                tmp &= tmp - 1;
                b0[k] = g->nbr_bits[u][0];
                b1[k] = g->nbr_bits[u][1];
                b2[k] = g->nbr_bits[u][2];
                k++;
            }

            u256 sum = u256_zero();
            /* Iterative stack-based backtracking over k vertices */
            uint32_t used_stack[MAX_N + 1];
            int choice_stack[MAX_N + 1];
            used_stack[0] = 0;
            choice_stack[0] = 0;
            int depth = 0;

            while (depth >= 0) {
                if (depth == k) {
                    uint32_t V = full_mask ^ used_stack[k];
                    u256_add_inplace(&sum, &vec_in[orbit_id[V]]);
                    depth--;
                    continue;
                }
                int c = choice_stack[depth];
                if (c >= 3) {
                    depth--;
                    continue;
                }
                choice_stack[depth] = c + 1;
                uint32_t bit = (c == 0) ? b0[depth] : ((c == 1) ? b1[depth] : b2[depth]);
                if (!(used_stack[depth] & bit)) {
                    used_stack[depth + 1] = used_stack[depth] | bit;
                    choice_stack[depth + 1] = 0;
                    depth++;
                }
            }
            ctx->vec_out[o] = sum;
        }
    }
    return NULL;
}

static void multiply_step_mt(const GridData *g, int k_from, const u256 *vec_in, u256 *vec_out, int nthreads) {
    MulContext ctx;
    ctx.g = g;
    ctx.k_from = k_from;
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
    for (int p = 0; p <= max_p; p++) max_bound_by_p[p] = 0.0;

    for (int i = 0; i <= N / 2; i++) {
        int dim_even = g.num_orbits[i];
        int dim_odd  = g.num_orbits[N - i];
        u256 *even_vec = (u256 *)malloc((size_t)dim_even * sizeof(u256));
        u256 *odd_vec  = (u256 *)malloc((size_t)dim_odd  * sizeof(u256));
        u256 *new_even = (u256 *)malloc((size_t)dim_even * sizeof(u256));

        for (int u = 0; u < dim_even; u++) even_vec[u] = u256_from_u64(1);

        for (int p = 0; p <= max_p; p++) {
            multiply_step_mt(&g, N - i, even_vec, odd_vec, nthreads);
            multiply_step_mt(&g, i, odd_vec, new_even, nthreads);

            int best_u = 0;
            for (int u = 1; u < dim_even; u++) {
                if (u256_cmp_ratio(&new_even[u], &even_vec[u], &new_even[best_u], &even_vec[best_u]) > 0) {
                    best_u = u;
                }
            }
            double ratio = u256_to_double(&new_even[best_u]) / u256_to_double(&even_vec[best_u]);
            double val = log(ratio) / (2.0 * N);
            if (val > max_bound_by_p[p]) max_bound_by_p[p] = val;

            memcpy(even_vec, new_even, (size_t)dim_even * sizeof(u256));
        }

        free(even_vec);
        free(odd_vec);
        free(new_even);
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);

    printf("Case (%d,%d) [N=%d, max_orbits=%d, time=%.2fs]:\n",
           m, n, N, g.num_orbits[N / 2], elapsed);
    for (int p = 0; p <= max_p; p++) {
        double up6 = ceil(max_bound_by_p[p] * 1e6) / 1e6;
        printf("  p=%d: bound = %.10f  (ceil_6 = %.6f)\n", p, max_bound_by_p[p], up6);
    }
    fflush(stdout);
    free_grid(&g);
}

int main(void) {
    int nthreads = 10;
    solve_he_case(2, 2, 4, nthreads);
    solve_he_case(3, 2, 4, nthreads);
    solve_he_case(3, 3, 4, nthreads);
    solve_he_case(4, 2, 4, nthreads);
    solve_he_case(4, 3, 4, nthreads);
    solve_he_case(4, 4, 4, nthreads);
    solve_he_case(5, 2, 4, nthreads);
    solve_he_case(5, 3, 4, nthreads);
    solve_he_case(5, 4, 4, nthreads);
    solve_he_case(6, 2, 4, nthreads);
    solve_he_case(6, 3, 4, nthreads);
    return 0;
}
