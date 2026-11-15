#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "math.h"
#include "time.h"

typedef unsigned __int128 u128;

static void u128_to_dec(u128 a, char *buf) {
    if (a == 0) { strcpy(buf, "0"); return; }
    char tmp[64]; int pos = 0;
    while (a > 0) {
        tmp[pos++] = '0' + (int)(a % 10);
        a /= 10;
    }
    for (int i = 0; i < pos; i++) buf[i] = tmp[pos - 1 - i];
    buf[pos] = '\0';
}

static int M, N, NV;
static int num_syms;
static int sym_perm[200][36];
static uint32_t nbr_mask[36];

static void init_geometry(int m, int n) {
    M = m; N = n; NV = m * n;
    for (int r = 0; r < M; r++) {
        for (int c = 0; c < N; c++) {
            int u = r * N + c;
            int u1 = r * N + c;
            int u2 = ((r + 1) % M) * N + c;
            int u3 = r * N + ((c + 1) % N);
            nbr_mask[u] = (1U << u1) | (1U << u2) | (1U << u3);
        }
    }
    num_syms = 0;
    int max_swap = (M == N) ? 1 : 0;
    for (int sw = 0; sw <= max_swap; sw++) {
        for (int sr = 0; sr < M; sr++) {
            for (int sc = 0; sc < N; sc++) {
                for (int r = 0; r < M; r++) {
                    for (int c = 0; c < N; c++) {
                        int u = r * N + c;
                        int nr = sw ? c : r;
                        int nc = sw ? r : c;
                        nr = (nr + sr) % M;
                        nc = (nc + sc) % N;
                        sym_perm[num_syms][u] = nr * N + nc;
                    }
                }
                num_syms++;
            }
        }
    }
}

static inline uint32_t apply_sym(uint32_t mask, const int *perm) {
    uint32_t res = 0, tmp = mask;
    while (tmp) {
        int u = __builtin_ctz(tmp);
        res |= (1U << perm[u]);
        tmp &= tmp - 1;
    }
    return res;
}

static int get_order(int k, uint32_t u_mask, int *order, uint32_t *rem_union) {
    uint32_t rem = u_mask;
    for (int step = 0; step < k; step++) {
        int best_u = -1, best_deg = 999, best_ov = -1;
        uint32_t tmp = rem;
        while (tmp) {
            int u = __builtin_ctz(tmp);
            uint32_t nu = nbr_mask[u];
            int deg = __builtin_popcount(nu);
            uint32_t other_nbrs = 0, tmp2 = rem & ~(1U << u);
            while (tmp2) {
                int v = __builtin_ctz(tmp2);
                other_nbrs |= nbr_mask[v];
                tmp2 &= tmp2 - 1;
            }
            int ov = __builtin_popcount(nu & other_nbrs);
            if (deg < best_deg || (deg == best_deg && ov > best_ov)) {
                best_deg = deg; best_ov = ov; best_u = u;
            }
            tmp &= tmp - 1;
        }
        order[step] = best_u;
        rem &= ~(1U << best_u);
    }
    rem_union[k] = 0;
    for (int step = k - 1; step >= 0; step--) {
        rem_union[step] = rem_union[step + 1] | nbr_mask[order[step]];
    }
    return (__builtin_popcount(rem_union[0]) >= k);
}

static double sum_dbl_rec(int idx, int k, const uint32_t *nbrs, const uint32_t *rem_union, uint32_t used, const double *vec_in, const uint32_t *state_to_orbit) {
    if (idx == k) return vec_in[state_to_orbit[used]];
    if (__builtin_popcount(rem_union[idx] & ~used) < k - idx) return 0.0;
    uint32_t avail = nbrs[idx] & ~used;
    if (!avail) return 0.0;
    if (idx == k - 1) {
        double total = 0.0;
        while (avail) {
            uint32_t bit = avail & -avail;
            total += vec_in[state_to_orbit[used | bit]];
            avail &= avail - 1;
        }
        return total;
    }
    double total = 0.0;
    while (avail) {
        uint32_t bit = avail & -avail;
        total += sum_dbl_rec(idx + 1, k, nbrs, rem_union, used | bit, vec_in, state_to_orbit);
        avail &= avail - 1;
    }
    return total;
}

static u128 sum_u128_rec(int idx, int k, const uint32_t *nbrs, const uint32_t *rem_union, uint32_t used, const u128 *vec_in, const uint32_t *state_to_orbit) {
    if (idx == k) return vec_in[state_to_orbit[used]];
    if (__builtin_popcount(rem_union[idx] & ~used) < k - idx) return 0;
    uint32_t avail = nbrs[idx] & ~used;
    if (!avail) return 0;
    if (idx == k - 1) {
        u128 total = 0;
        while (avail) {
            uint32_t bit = avail & -avail;
            total += vec_in[state_to_orbit[used | bit]];
            avail &= avail - 1;
        }
        return total;
    }
    u128 total = 0;
    while (avail) {
        uint32_t bit = avail & -avail;
        total += sum_u128_rec(idx + 1, k, nbrs, rem_union, used | bit, vec_in, state_to_orbit);
        avail &= avail - 1;
    }
    return total;
}

static void solve_md(int m, int n, int n_iters, const char *cert_filename) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    init_geometry(m, n);
    uint32_t n_states = 1U << NV;
    uint32_t *state_to_orbit = (uint32_t *)malloc(n_states * sizeof(uint32_t));
    memset(state_to_orbit, 0xFF, n_states * sizeof(uint32_t));

    uint32_t *orbit_rep = (uint32_t *)malloc(n_states * sizeof(uint32_t));
    int num_orbits = 0;
    for (uint32_t mask = 0; mask < n_states; mask++) {
        if (state_to_orbit[mask] == 0xFFFFFFFFU) {
            uint32_t oid = (uint32_t)num_orbits++;
            orbit_rep[oid] = mask;
            for (int s = 0; s < num_syms; s++) {
                uint32_t sym_m = apply_sym(mask, sym_perm[s]);
                state_to_orbit[sym_m] = oid;
            }
        }
    }

    double *v = (double *)malloc(num_orbits * sizeof(double));
    double *pv = (double *)malloc(num_orbits * sizeof(double));
    double *F = (double *)malloc(n_states * sizeof(double));
    for (int i = 0; i < num_orbits; i++) v[i] = 1.0;

    for (int iter = 0; iter < n_iters; iter++) {
        for (int oid = 0; oid < num_orbits; oid++) {
            uint32_t u_mask = orbit_rep[oid];
            int k = __builtin_popcount(u_mask);
            if (k == 0) { pv[oid] = v[oid]; continue; }
            int order[25]; uint32_t rem_union[26], nbrs[25];
            if (!get_order(k, u_mask, order, rem_union)) { pv[oid] = 0.0; continue; }
            for (int s = 0; s < k; s++) nbrs[s] = nbr_mask[order[s]];
            pv[oid] = sum_dbl_rec(0, k, nbrs, rem_union, 0, v, state_to_orbit);
        }
        for (uint32_t mask = 0; mask < n_states; mask++) {
            F[mask] = pv[state_to_orbit[mask]];
        }
        for (int bit = 0; bit < NV; bit++) {
            uint32_t step = 1U << bit;
            for (uint32_t mask = 0; mask < n_states; mask++) {
                if (mask & step) F[mask] += F[mask ^ step];
            }
        }
        double max_val = F[n_states - 1];
        for (int oid = 0; oid < num_orbits; oid++) {
            uint32_t comp = (n_states - 1) ^ orbit_rep[oid];
            v[oid] = F[comp] / max_val;
        }
    }

    /* Quantize to 64-bit positive integer vector and verify with exact u128 arithmetic */
    u128 *x_int = (u128 *)malloc(num_orbits * sizeof(u128));
    u128 *px_int = (u128 *)malloc(num_orbits * sizeof(u128));
    u128 *F_int = (u128 *)malloc(n_states * sizeof(u128));
    const double SCALE = (double)(1ULL << 48);
    for (int oid = 0; oid < num_orbits; oid++) {
        uint64_t q = (uint64_t)llround(v[oid] * SCALE);
        if (q == 0) q = 1;
        x_int[oid] = (u128)q;
    }

    if (cert_filename != NULL) {
        FILE *fp = fopen(cert_filename, "w");
        if (fp) {
            fprintf(fp, "# Exact positive integer Collatz-Wielandt certificate for 3D Monomer-Dimer h_3 on (m,n)=(%d,%d) (%d orbits)\n", m, n, num_orbits);
            fprintf(fp, "# Format: orbit_id canonical_mask x_int\n");
            for (int oid = 0; oid < num_orbits; oid++) {
                fprintf(fp, "%d %u %llu\n", oid, orbit_rep[oid], (unsigned long long)x_int[oid]);
            }
            fclose(fp);
        }
    }

    for (int oid = 0; oid < num_orbits; oid++) {
        uint32_t u_mask = orbit_rep[oid];
        int k = __builtin_popcount(u_mask);
        if (k == 0) { px_int[oid] = x_int[oid]; continue; }
        int order[25]; uint32_t rem_union[26], nbrs[25];
        if (!get_order(k, u_mask, order, rem_union)) { px_int[oid] = 0; continue; }
        for (int s = 0; s < k; s++) nbrs[s] = nbr_mask[order[s]];
        px_int[oid] = sum_u128_rec(0, k, nbrs, rem_union, 0, x_int, state_to_orbit);
    }
    for (uint32_t mask = 0; mask < n_states; mask++) {
        F_int[mask] = px_int[state_to_orbit[mask]];
    }
    for (int bit = 0; bit < NV; bit++) {
        uint32_t step = 1U << bit;
        for (uint32_t mask = 0; mask < n_states; mask++) {
            if (mask & step) F_int[mask] += F_int[mask ^ step];
        }
    }

    double cw_min = 1e300, cw_max = 0.0;
    int argmax_oid = -1;
    for (int oid = 0; oid < num_orbits; oid++) {
        uint32_t comp = (n_states - 1) ^ orbit_rep[oid];
        u128 tx = F_int[comp];
        double r = (double)tx / (double)x_int[oid];
        if (r > cw_max) { cw_max = r; argmax_oid = oid; }
        if (r < cw_min) cw_min = r;
    }

    char num_s[64], den_s[64];
    u128_to_dec(F_int[(n_states - 1) ^ orbit_rep[argmax_oid]], num_s);
    u128_to_dec(x_int[argmax_oid], den_s);
    double ub = log(cw_max) / (double)NV;
    double lb = log(cw_min) / (double)NV;

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("(m,n)=(%d,%d) [NV=%2d, orbits=%5d]: h_3 <= %.10f (spread [%.10f, %.10f]), max ratio %s / %s at oid=%d [%.2fs]\n",
           m, n, NV, num_orbits, ub, lb, ub, num_s, den_s, argmax_oid, elapsed);

    free(x_int); free(px_int); free(F_int);
    free(v); free(pv); free(F);
    free(orbit_rep); free(state_to_orbit);
}

int main(void) {
    printf("=== 3D MONOMER-DIMER ENTROPY h_3 UPPER BOUNDS (Published: <= 0.7862023450) ===\n");
    solve_md(2, 2, 30, NULL);
    solve_md(3, 2, 30, NULL);
    solve_md(3, 3, 35, "results/cert_md_h3_33.txt");
    solve_md(4, 2, 35, NULL);
    solve_md(4, 3, 40, "results/cert_md_h3_43.txt");
    solve_md(4, 4, 45, "results/cert_md_h3_44.txt");
    solve_md(5, 3, 45, NULL);
    solve_md(5, 4, 50, "results/cert_md_h3_54.txt");
    return 0;
}
