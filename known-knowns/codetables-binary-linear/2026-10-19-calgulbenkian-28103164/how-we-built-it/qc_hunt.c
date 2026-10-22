/*
 * qc_hunt.c
 *
 * Supercharged CRT Orbit-Permutation & Coset-Weighted Construction X Search
 * with Exhaustive Grassmannian Subspace Enumeration (all 21 2D subspaces of GF(4)^3,
 * all 13 2D subspaces of GF(3)^3, etc.) and Exhaustive Lift Scanning.
 */

#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "time.h"

#define MAX_M 128
#define MAX_K 26
#define MAX_L 6
#define MAX_T 24
#define MAX_S 7
#define MAX_QS 128

static int Q_VAL = 2;
static uint8_t GF_ADD[10][10];
static uint8_t GF_SUB[10][10];
static uint8_t GF_MUL[10][10];
static uint8_t GF_INV[10];

static void init_gf(int q) {
    Q_VAL = q;
    memset(GF_ADD, 0, sizeof(GF_ADD));
    memset(GF_SUB, 0, sizeof(GF_SUB));
    memset(GF_MUL, 0, sizeof(GF_MUL));
    memset(GF_INV, 0, sizeof(GF_INV));
    if (q == 2 || q == 3 || q == 5 || q == 7) {
        for (int a = 0; a < q; a++) {
            for (int b = 0; b < q; b++) {
                GF_ADD[a][b] = (a + b) % q;
                GF_SUB[a][b] = (a - b + q) % q;
                GF_MUL[a][b] = (a * b) % q;
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    } else if (q == 4) {
        const uint8_t mul4[4][4] = {
            {0, 0, 0, 0},
            {0, 1, 2, 3},
            {0, 2, 3, 1},
            {0, 3, 1, 2}
        };
        for (int a = 0; a < 4; a++) {
            for (int b = 0; b < 4; b++) {
                GF_ADD[a][b] = a ^ b;
                GF_SUB[a][b] = a ^ b;
                GF_MUL[a][b] = mul4[a][b];
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    } else if (q == 8) {
        for (int a = 0; a < 8; a++) {
            for (int b = 0; b < 8; b++) {
                GF_ADD[a][b] = a ^ b;
                GF_SUB[a][b] = a ^ b;
                int p = 0, aa = a, bb = b;
                for (int i = 0; i < 3; i++) {
                    if (bb & 1) p ^= aa;
                    aa <<= 1;
                    if (aa & 8) aa ^= 11;
                    bb >>= 1;
                }
                GF_MUL[a][b] = p;
                if (p == 1) GF_INV[a] = b;
            }
        }
    } else if (q == 9) {
        for (int a = 0; a < 9; a++) {
            int a0 = a % 3, a1 = a / 3;
            for (int b = 0; b < 9; b++) {
                int b0 = b % 3, b1 = b / 3;
                GF_ADD[a][b] = ((a0 + b0) % 3) + 3 * ((a1 + b1) % 3);
                GF_SUB[a][b] = ((a0 - b0 + 3) % 3) + 3 * ((a1 - b1 + 3) % 3);
                int c0 = (a0 * b0 - a1 * b1 + 9) % 3;
                int c1 = (a0 * b1 + a1 * b0) % 3;
                GF_MUL[a][b] = c0 + 3 * c1;
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    }
}

typedef struct {
    int deg;
    uint8_t c[MAX_M + 1];
} Poly;

static void poly_normalize(Poly *p) {
    while (p->deg > 0 && p->c[p->deg] == 0) p->deg--;
}

static Poly poly_zero(void) {
    Poly p;
    memset(&p, 0, sizeof(p));
    p.deg = 0;
    return p;
}

static Poly poly_one(void) {
    Poly p = poly_zero();
    p.c[0] = 1;
    return p;
}

static int poly_is_zero(const Poly *p) {
    return p->deg == 0 && p->c[0] == 0;
}

static Poly poly_mul(const Poly *a, const Poly *b) {
    Poly r = poly_zero();
    if (poly_is_zero(a) || poly_is_zero(b)) return r;
    r.deg = a->deg + b->deg;
    for (int i = 0; i <= a->deg; i++) {
        if (!a->c[i]) continue;
        for (int j = 0; j <= b->deg; j++) {
            if (b->c[j]) {
                r.c[i + j] = GF_ADD[r.c[i + j]][GF_MUL[a->c[i]][b->c[j]]];
            }
        }
    }
    poly_normalize(&r);
    return r;
}

static void poly_divmod(const Poly *a, const Poly *b, Poly *q_out, Poly *r_out) {
    Poly rem = *a;
    Poly quo = poly_zero();
    poly_normalize(&rem);
    int db = b->deg;
    uint8_t inv_lead = GF_INV[b->c[db]];
    if (rem.deg >= db && !poly_is_zero(&rem)) {
        quo.deg = rem.deg - db;
    }
    while (rem.deg >= db && !poly_is_zero(&rem)) {
        int shift = rem.deg - db;
        uint8_t factor = GF_MUL[rem.c[rem.deg]][inv_lead];
        quo.c[shift] = factor;
        for (int i = 0; i <= db; i++) {
            if (b->c[i]) {
                uint8_t sub = GF_MUL[factor][b->c[i]];
                rem.c[shift + i] = GF_SUB[rem.c[shift + i]][sub];
            }
        }
        poly_normalize(&rem);
    }
    poly_normalize(&quo);
    if (q_out) *q_out = quo;
    if (r_out) *r_out = rem;
}

static Poly poly_mul_mod(const Poly *a, const Poly *b, const Poly *mod) {
    Poly prod = poly_mul(a, b);
    Poly rem;
    poly_divmod(&prod, mod, NULL, &rem);
    return rem;
}

static int poly_weight(const Poly *p, int m) {
    int w = 0;
    for (int i = 0; i < m && i <= p->deg; i++) {
        if (p->c[i] != 0) w++;
    }
    return w;
}

static uint32_t poly_to_int(const Poly *p, int k, int q) {
    uint32_t val = 0;
    uint32_t pw = 1;
    for (int i = 0; i < k; i++) {
        uint8_t ci = (i <= p->deg) ? p->c[i] : 0;
        val += ci * pw;
        pw *= q;
    }
    return val;
}

static Poly int_to_poly(uint32_t val, int k, int q) {
    Poly p = poly_zero();
    p.deg = k - 1;
    for (int i = 0; i < k; i++) {
        p.c[i] = val % q;
        val /= q;
    }
    poly_normalize(&p);
    return p;
}

static int factor_xm_lambda(int m, int lambda, int q, Poly *factors, int max_factors) {
    Poly xm = poly_zero();
    xm.deg = m;
    xm.c[m] = 1;
    xm.c[0] = GF_SUB[0][lambda];

    int n_fac = 0;
    for (int d = 1; d <= m; d++) {
        uint64_t lim = 1;
        for (int i = 0; i < d; i++) {
            lim *= q;
            if (lim > 4000000ULL) break;
        }
        if (lim > 3000000ULL && d < xm.deg) continue;
        if (d > xm.deg) break;
        if (d * 2 > xm.deg) {
            if (xm.deg >= 1 && n_fac < max_factors) {
                uint8_t inv = GF_INV[xm.c[xm.deg]];
                for (int i = 0; i <= xm.deg; i++) xm.c[i] = GF_MUL[xm.c[i]][inv];
                factors[n_fac++] = xm;
                xm = poly_one();
            }
            break;
        }
        for (uint64_t mask = 1; mask < lim; mask++) {
            if ((mask % q) == 0) continue;
            Poly cand = poly_zero();
            cand.deg = d;
            cand.c[d] = 1;
            uint64_t tmp = mask;
            for (int i = 0; i < d; i++) {
                cand.c[i] = tmp % q;
                tmp /= q;
            }
            while (xm.deg >= d) {
                Poly quo, rem;
                poly_divmod(&xm, &cand, &quo, &rem);
                if (poly_is_zero(&rem)) {
                    if (n_fac < max_factors) factors[n_fac++] = cand;
                    xm = quo;
                } else {
                    break;
                }
            }
            if (xm.deg < d) break;
        }
    }
    if (xm.deg >= 1 && n_fac < max_factors) {
        uint8_t inv = GF_INV[xm.c[xm.deg]];
        for (int i = 0; i <= xm.deg; i++) xm.c[i] = GF_MUL[xm.c[i]][inv];
        factors[n_fac++] = xm;
    }
    return n_fac;
}

static int D_LO[10][260][40];
static int D_LO_ORIG[10][260][40];
static int D_UP[10][260][40];

static void load_bounds_tsv(const char *path) {
    memset(D_LO, 0, sizeof(D_LO));
    memset(D_LO_ORIG, 0, sizeof(D_LO_ORIG));
    memset(D_UP, 0, sizeof(D_UP));
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Warning: could not open %s\n", path);
        return;
    }
    int q, n, k, dlo, dup;
    while (fscanf(f, "%d %d %d %d %d", &q, &n, &k, &dlo, &dup) == 5) {
        if (q >= 2 && q <= 9 && n >= 1 && n < 260 && k >= 1 && k < 40) {
            D_LO[q][n][k] = dlo;
            D_LO_ORIG[q][n][k] = dlo;
            D_UP[q][n][k] = dup;
        }
    }
    fclose(f);
}

static int is_excluded_cell(int q, int n, int k) {
    /* Exclude LinCodeEvolve region q=2, k in 19..22, n in 170..240 */
    if (q == 2 && k >= 19 && k <= 22 && n >= 170 && n <= 240) return 1;
    /* Exclude Trophy #4 and merged PRs */
    if (q == 2 && k == 22 && (n == 95 || n == 96)) return 1;
    if (q == 2 && k == 25 && n == 175) return 1;
    if (q == 2 && k == 26 && n == 213) return 1;
    if (q == 2 && k == 17 && n >= 170 && n <= 174) return 1;
    if (q == 4 && k == 10 && n == 156) return 1;
    if (q == 4 && k == 11 && (n == 154 || n == 155 || n == 157 || n == 158 || n == 162 || n == 163)) return 1;
    return 0;
}

static uint64_t rng_state = 0x853c49e6748fea9bULL;
static uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static int solve_tail_matrix(int s_prime, int q, int t, const int *req, uint32_t *T_cols) {
    uint32_t N = 1;
    for (int i = 0; i < s_prime; i++) N *= q;
    if (N > MAX_QS) return 0;

    int max_req = 0;
    for (uint32_t u = 1; u < N; u++) {
        if (req[u] > max_req) max_req = req[u];
    }
    if (max_req <= 0) return 1;
    if (max_req > t) return 0;

    /* Plotkin/average weight bound quick filter: sum_{u!=0} req[u] <= t * (N - N/q) */
    int sum_req = 0;
    for (uint32_t u = 1; u < N; u++) {
        if (req[u] > 0) sum_req += req[u];
    }
    if (sum_req > t * (int)(N - N / q)) return 0;

    uint32_t proj_cols[MAX_QS];
    int p_cnt = 0;
    for (uint32_t c = 1; c < N; c++) {
        uint32_t tmp = c;
        int first_nz = 0;
        while (tmp > 0) {
            int digit = tmp % q;
            if (digit != 0) { first_nz = digit; break; }
            tmp /= q;
        }
        if (first_nz == 1 && p_cnt < MAX_QS) {
            proj_cols[p_cnt++] = c;
        }
    }

    uint8_t cov[MAX_QS][MAX_QS];
    for (int p = 0; p < p_cnt; p++) {
        uint32_t col = proj_cols[p];
        uint8_t c_vec[MAX_S];
        uint32_t tc = col;
        for (int i = 0; i < s_prime; i++) { c_vec[i] = tc % q; tc /= q; }
        for (uint32_t u = 1; u < N; u++) {
            uint32_t tu = u;
            uint8_t dot = 0;
            for (int i = 0; i < s_prime; i++) {
                uint8_t ui = tu % q;
                tu /= q;
                if (ui && c_vec[i]) dot = GF_ADD[dot][GF_MUL[ui][c_vec[i]]];
            }
            cov[p][u] = (dot != 0) ? 1 : 0;
        }
    }

    int cur_wt[MAX_QS];
    int cols_idx[MAX_T];

    for (int restart = 0; restart < 60; restart++) {
        memset(cur_wt, 0, sizeof(cur_wt));
        for (int j = 0; j < t; j++) {
            int best_p = 0;
            int64_t best_score = -1;
            for (int p = 0; p < p_cnt; p++) {
                int64_t sc = 0;
                for (uint32_t u = 1; u < N; u++) {
                    int def = req[u] - cur_wt[u];
                    if (def > 0 && cov[p][u]) {
                        sc += (int64_t)def * def * 16 + 1;
                    }
                }
                if (restart > 0) sc = sc * 8 + (xorshift64() & 7);
                if (sc > best_score) {
                    best_score = sc;
                    best_p = p;
                }
            }
            cols_idx[j] = best_p;
            for (uint32_t u = 1; u < N; u++) cur_wt[u] += cov[best_p][u];
        }

        int total_def = 0;
        for (uint32_t u = 1; u < N; u++) {
            if (cur_wt[u] < req[u]) total_def += (req[u] - cur_wt[u]);
        }
        if (total_def == 0) {
            for (int j = 0; j < t; j++) T_cols[j] = proj_cols[cols_idx[j]];
            return 1;
        }

        for (int step = 0; step < 300 && total_def > 0; step++) {
            int j = step % t;
            int old_p = cols_idx[j];
            for (uint32_t u = 1; u < N; u++) cur_wt[u] -= cov[old_p][u];

            int best_p = old_p;
            int best_def = 999999;
            int best_sq = 999999;
            for (int p = 0; p < p_cnt; p++) {
                int d_sum = 0, sq_sum = 0;
                for (uint32_t u = 1; u < N; u++) {
                    int rem = req[u] - (cur_wt[u] + cov[p][u]);
                    if (rem > 0) {
                        d_sum += rem;
                        sq_sum += rem * rem;
                    }
                }
                if (d_sum < best_def || (d_sum == best_def && (sq_sum < best_sq || (xorshift64() & 3) == 0))) {
                    best_def = d_sum;
                    best_sq = sq_sum;
                    best_p = p;
                }
            }
            cols_idx[j] = best_p;
            for (uint32_t u = 1; u < N; u++) cur_wt[u] += cov[best_p][u];
            total_def = best_def;
        }

        if (total_def == 0) {
            for (int j = 0; j < t; j++) T_cols[j] = proj_cols[cols_idx[j]];
            return 1;
        }
    }
    return 0;
}

static int verify_and_save_code(
    int q, int m, int lambda, int l, const Poly *h_core, const Poly *h_sub,
    const Poly *f_polys, int s_prime, const uint32_t *basis_r,
    int t, const uint32_t *T_cols, int d_target
) {
    int k_core = h_core->deg;
    int s = h_sub->deg;
    int k = k_core + s_prime;
    int n = m * l + t;

    Poly xm = poly_zero();
    xm.deg = m;
    xm.c[m] = 1;
    xm.c[0] = GF_SUB[0][lambda];

    Poly h_full = poly_mul(h_core, h_sub);
    Poly g0, rem;
    poly_divmod(&xm, &h_full, &g0, &rem);
    if (!poly_is_zero(&rem)) return 0;

    Poly g_blk[MAX_L];
    for (int j = 0; j < l; j++) {
        g_blk[j] = poly_mul_mod(&g0, &f_polys[j], &xm);
    }

    uint8_t G[MAX_K][260];
    memset(G, 0, sizeof(G));

    for (int i = 0; i < k_core; i++) {
        Poly x_i = poly_zero();
        x_i.deg = i;
        x_i.c[i] = 1;
        Poly b_poly = poly_mul(&x_i, h_sub);
        for (int j = 0; j < l; j++) {
            Poly cw = poly_mul_mod(&b_poly, &g_blk[j], &xm);
            for (int c = 0; c < m; c++) {
                G[i][j * m + c] = (c <= cw.deg) ? cw.c[c] : 0;
            }
        }
    }

    for (int idx = 0; idx < s_prime; idx++) {
        int row_idx = k_core + idx;
        Poly r_poly = int_to_poly(basis_r[idx], s, q);
        for (int j = 0; j < l; j++) {
            Poly cw = poly_mul_mod(&r_poly, &g_blk[j], &xm);
            for (int c = 0; c < m; c++) {
                G[row_idx][j * m + c] = (c <= cw.deg) ? cw.c[c] : 0;
            }
        }
        for (int c = 0; c < t; c++) {
            uint32_t col = T_cols[c];
            for (int p = 0; p < idx; p++) col /= q;
            G[row_idx][m * l + c] = col % q;
        }
    }

    uint8_t cw[260];
    uint8_t u[MAX_K];
    int min_w = n + 1;
    uint64_t A_d = 0;

    for (int lead = 0; lead < k; lead++) {
        memset(u, 0, sizeof(u));
        u[lead] = 1;
        for (int c = 0; c < n; c++) cw[c] = G[lead][c];
        while (1) {
            int w = 0;
            for (int c = 0; c < n; c++) if (cw[c]) w++;
            if (w < min_w) {
                min_w = w;
                A_d = (q - 1);
                if (min_w < d_target) return 0;
            } else if (w == min_w) {
                A_d += (q - 1);
            }
            int pos = lead - 1;
            while (pos >= 0 && u[pos] == q - 1) {
                uint8_t old_v = u[pos];
                u[pos] = 0;
                for (int c = 0; c < n; c++) {
                    if (G[pos][c]) cw[c] = GF_SUB[cw[c]][GF_MUL[old_v][G[pos][c]]];
                }
                pos--;
            }
            if (pos < 0) break;
            uint8_t old_u = u[pos];
            u[pos]++;
            uint8_t delta = GF_SUB[u[pos]][old_u];
            for (int c = 0; c < n; c++) {
                if (G[pos][c]) cw[c] = GF_ADD[cw[c]][GF_MUL[delta][G[pos][c]]];
            }
        }
    }

    int d_lo = D_LO[q][n][k];
    int d_lo_orig = D_LO_ORIG[q][n][k];
    int d_up = D_UP[q][n][k];
    if (min_w <= d_lo) return 0;

    D_LO[q][n][k] = min_w;

    printf("\n*** BRAND-NEW BREAKTHROUGH WIN: [%d, %d, %d]_%d (beats codetables.de d_lo=%d, d_up=%d, A_d=%llu) ***\n",
           n, k, min_w, q, d_lo_orig, d_up, (unsigned long long)A_d);
    fflush(stdout);

    char fname[256];
    snprintf(fname, sizeof(fname), "results/new_win_q%d_n%d_k%d_d%d.json",
             q, n, k, min_w);
    FILE *fp = fopen(fname, "w");
    if (fp) {
        fprintf(fp, "{\n");
        fprintf(fp, "  \"type\": \"classical\",\n");
        fprintf(fp, "  \"q\": %d,\n", q);
        fprintf(fp, "  \"n\": %d,\n", n);
        fprintf(fp, "  \"k\": %d,\n", k);
        fprintf(fp, "  \"d\": %d,\n", min_w);
        fprintf(fp, "  \"d_lo_codetables\": %d,\n", d_lo_orig);
        fprintf(fp, "  \"d_up_codetables\": %d,\n", d_up);
        fprintf(fp, "  \"A_d\": %llu,\n", (unsigned long long)A_d);
        fprintf(fp, "  \"construction\": \"QC/QT + Coset-Weighted Construction X (m=%d, lambda=%d, l=%d, k_core=%d, s=%d, s_prime=%d, t=%d)\",\n",
                m, lambda, l, k_core, s, s_prime, t);
        fprintf(fp, "  \"G\": [\n");
        for (int r = 0; r < k; r++) {
            fprintf(fp, "    [");
            for (int c = 0; c < n; c++) {
                fprintf(fp, "%d%s", G[r][c], (c + 1 < n) ? "," : "");
            }
            fprintf(fp, "]%s\n", (r + 1 < k) ? "," : "");
        }
        fprintf(fp, "  ]\n}\n");
        fclose(fp);
    }
    return 1;
}

/* Helper: combine two elements v1, v2 in GF(q)^s represented as base-q integers: v1 + alpha * v2 */
static uint32_t gf_vec_comb(uint32_t v1, uint32_t v2, int alpha, int s, int q) {
    uint32_t comb = 0, pw = 1;
    for (int i = 0; i < s; i++) {
        uint8_t c1 = v1 % q, c2 = v2 % q;
        v1 /= q; v2 /= q;
        uint8_t sum = GF_ADD[c1][GF_MUL[alpha][c2]];
        comb += sum * pw;
        pw *= q;
    }
    return comb;
}

static void search_config(
    int q, int m, int lambda, int l,
    const Poly *h_core, const Poly *h_sub,
    int max_iters
) {
    int k_core = h_core->deg;
    int s = h_sub->deg;
    int k_max = k_core + s;
    if (k_core < 3 || k_max >= MAX_K) return;

    uint64_t q_kcore = 1;
    for (int i = 0; i < k_core; i++) q_kcore *= q;
    uint64_t q_kmax = q_kcore;
    for (int i = 0; i < s; i++) q_kmax *= q;
    if (q_kmax > (1ULL << 22)) return;

    int any_open = 0;
    for (int s_p = 0; s_p <= s; s_p++) {
        int k = k_core + s_p;
        for (int t = 0; t <= 18; t++) {
            int n = m * l + t;
            if (n < 256 && !is_excluded_cell(q, n, k)) {
                if (D_LO[q][n][k] > 0 && D_LO[q][n][k] < D_UP[q][n][k]) {
                    any_open = 1;
                    break;
                }
            }
        }
    }
    if (!any_open) return;

    Poly xm = poly_zero();
    xm.deg = m;
    xm.c[m] = 1;
    xm.c[0] = GF_SUB[0][lambda];

    Poly g_sub, rem;
    poly_divmod(&xm, h_core, &g_sub, &rem);
    if (!poly_is_zero(&rem)) return;

    uint8_t *vis_core = (uint8_t *)calloc(q_kcore, 1);
    uint8_t *wt_core = (uint8_t *)calloc(q_kcore, 1);
    uint32_t *core_reps = (uint32_t *)malloc(q_kcore * sizeof(uint32_t));
    int n_core_orbs = 0;

    Poly x_poly = poly_zero();
    x_poly.deg = 1;
    x_poly.c[1] = 1;

    for (uint32_t a = 1; a < q_kcore; a++) {
        if (!vis_core[a]) {
            core_reps[n_core_orbs++] = a;
            Poly pa = int_to_poly(a, k_core, q);
            Poly cw = poly_mul_mod(&pa, &g_sub, &xm);
            uint8_t w = (uint8_t)poly_weight(&cw, m);

            Poly cur = pa;
            for (int step = 0; step < m; step++) {
                for (int alpha = 1; alpha < q; alpha++) {
                    Poly scaled = cur;
                    for (int i = 0; i <= scaled.deg; i++) scaled.c[i] = GF_MUL[scaled.c[i]][alpha];
                    poly_normalize(&scaled);
                    uint32_t idx = poly_to_int(&scaled, k_core, q);
                    vis_core[idx] = 1;
                    wt_core[idx] = w;
                }
                cur = poly_mul_mod(&cur, &x_poly, h_core);
            }
        }
    }

    for (int i = 0; i < n_core_orbs - 1; i++) {
        for (int j = i + 1; j < n_core_orbs; j++) {
            if (wt_core[core_reps[j]] < wt_core[core_reps[i]]) {
                uint32_t tmp = core_reps[i];
                core_reps[i] = core_reps[j];
                core_reps[j] = tmp;
            }
        }
    }

    Poly *core_rep_polys = (Poly *)malloc(n_core_orbs * sizeof(Poly));
    for (int o = 0; o < n_core_orbs; o++) {
        core_rep_polys[o] = int_to_poly(core_reps[o], k_core, q);
    }

    int best_d_c2 = 0;
    uint32_t top_f_core[16][MAX_L];
    int top_d_c2[16];
    int n_top = 0;

    if (l == 2) {
        for (int o2 = 0; o2 < n_core_orbs; o2++) {
            Poly f2 = core_rep_polys[o2];
            int d_min = 9999;
            int cutoff = (best_d_c2 > 0) ? best_d_c2 - 1 : 1;
            for (int o = 0; o < n_core_orbs; o++) {
                Poly prod = poly_mul_mod(&core_rep_polys[o], &f2, h_core);
                uint32_t idx2 = poly_to_int(&prod, k_core, q);
                int w = wt_core[core_reps[o]] + wt_core[idx2];
                if (w < d_min) {
                    d_min = w;
                    if (d_min < cutoff) break;
                }
            }
            if (d_min > best_d_c2) {
                best_d_c2 = d_min;
                n_top = 0;
            }
            if (d_min >= best_d_c2 && n_top < 16) {
                top_f_core[n_top][0] = 1;
                top_f_core[n_top][1] = core_reps[o2];
                top_d_c2[n_top] = d_min;
                n_top++;
            }
        }
    } else {
        int *w_partial = (int *)malloc(n_core_orbs * sizeof(int));
        int actual_iters = (n_core_orbs > 2500) ? 50 : max_iters;
        for (int restart = 0; restart < actual_iters; restart++) {
            uint32_t cur_f[MAX_L];
            cur_f[0] = 1;
            for (int j = 1; j < l; j++) {
                cur_f[j] = core_reps[xorshift64() % n_core_orbs];
            }
            int cur_d = 0;
            for (int sweep = 0; sweep < 3; sweep++) {
                int changed = 0;
                for (int j = 1; j < l; j++) {
                    for (int o = 0; o < n_core_orbs; o++) {
                        int wp = wt_core[core_reps[o]];
                        for (int jj = 1; jj < l; jj++) {
                            if (jj == j) continue;
                            Poly fj = int_to_poly(cur_f[jj], k_core, q);
                            Poly prod = poly_mul_mod(&core_rep_polys[o], &fj, h_core);
                            wp += wt_core[poly_to_int(&prod, k_core, q)];
                        }
                        w_partial[o] = wp;
                    }
                    int best_j_d = cur_d;
                    uint32_t best_j_f = cur_f[j];
                    int n_try = (n_core_orbs <= 600) ? n_core_orbs : 600;
                    for (int t_idx = 0; t_idx < n_try; t_idx++) {
                        int cand_o = (n_core_orbs <= 600) ? t_idx : (int)(xorshift64() % n_core_orbs);
                        Poly fj = core_rep_polys[cand_o];
                        int d_min = 9999;
                        for (int o = 0; o < n_core_orbs; o++) {
                            Poly prod = poly_mul_mod(&core_rep_polys[o], &fj, h_core);
                            int w = w_partial[o] + wt_core[poly_to_int(&prod, k_core, q)];
                            if (w < d_min) {
                                d_min = w;
                                if (d_min <= best_j_d) break;
                            }
                        }
                        if (d_min > best_j_d) {
                            best_j_d = d_min;
                            best_j_f = core_reps[cand_o];
                            changed = 1;
                        }
                    }
                    cur_f[j] = best_j_f;
                    cur_d = best_j_d;
                }
                if (!changed) break;
            }
            if (cur_d > best_d_c2) {
                best_d_c2 = cur_d;
                n_top = 0;
            }
            if (cur_d == best_d_c2 && n_top < 16) {
                int dup = 0;
                for (int i = 0; i < n_top; i++) {
                    int same = 1;
                    for (int j = 1; j < l; j++) if (top_f_core[i][j] != cur_f[j]) same = 0;
                    if (same) { dup = 1; break; }
                }
                if (!dup) {
                    for (int j = 0; j < l; j++) top_f_core[n_top][j] = cur_f[j];
                    top_d_c2[n_top] = cur_d;
                    n_top++;
                }
            }
        }
        free(w_partial);
    }

    if (!is_excluded_cell(q, m * l, k_core) &&
        D_LO[q][m * l][k_core] > 0 &&
        best_d_c2 > D_LO[q][m * l][k_core]) {
        Poly f_polys[MAX_L];
        f_polys[0] = poly_one();
        for (int j = 1; j < l; j++) f_polys[j] = int_to_poly(top_f_core[0][j], k_core, q);
        Poly h_one = poly_one();
        verify_and_save_code(q, m, lambda, l, h_core, &h_one, f_polys, 0, NULL, 0, NULL, best_d_c2);
    }

    int worth_lifting = 0;
    for (int s_p = 1; s_p <= s; s_p++) {
        int k = k_core + s_p;
        for (int t = 0; t <= 18; t++) {
            int n = m * l + t;
            if (n < 256 && !is_excluded_cell(q, n, k) &&
                D_LO[q][n][k] > 0 && best_d_c2 > D_LO[q][n][k]) {
                worth_lifting = 1;
                break;
            }
        }
    }

    if (worth_lifting && s >= 1 && n_top > 0) {
        Poly h_full = poly_mul(h_core, h_sub);
        Poly g0;
        poly_divmod(&xm, &h_full, &g0, &rem);
        if (poly_is_zero(&rem)) {
            uint32_t q_s = 1;
            for (int i = 0; i < s; i++) q_s *= q;

            int coset_orb_id[MAX_QS];
            memset(coset_orb_id, -1, sizeof(coset_orb_id));
            coset_orb_id[0] = 0;
            int n_coset_orbs = 1;
            for (uint32_t r = 1; r < q_s; r++) {
                if (coset_orb_id[r] < 0) {
                    int cid = n_coset_orbs++;
                    Poly r_cur = int_to_poly(r, s, q);
                    for (int step = 0; step < m; step++) {
                        for (int alpha = 1; alpha < q; alpha++) {
                            Poly rs = r_cur;
                            for (int i = 0; i <= rs.deg; i++) rs.c[i] = GF_MUL[rs.c[i]][alpha];
                            poly_normalize(&rs);
                            coset_orb_id[poly_to_int(&rs, s, q)] = cid;
                        }
                        r_cur = poly_mul_mod(&r_cur, &x_poly, h_sub);
                    }
                }
            }

            uint8_t *vis_full = (uint8_t *)calloc(q_kmax, 1);
            uint8_t *wt_full = (uint8_t *)calloc(q_kmax, 1);
            uint32_t *full_reps = (uint32_t *)malloc((q_kmax / m + 1024) * sizeof(uint32_t));
            uint8_t *full_rep_cid = (uint8_t *)malloc((q_kmax / m + 1024) * sizeof(uint8_t));
            int n_full_orbs = 0;

            for (uint32_t b = 1; b < q_kmax; b++) {
                if (!vis_full[b]) {
                    Poly pb = int_to_poly(b, k_max, q);
                    Poly r_sub;
                    poly_divmod(&pb, h_sub, NULL, &r_sub);
                    uint32_t r_int = poly_to_int(&r_sub, s, q);
                    if (r_int != 0) {
                        full_rep_cid[n_full_orbs] = (uint8_t)coset_orb_id[r_int];
                        full_reps[n_full_orbs++] = b;
                    }
                    Poly cw = poly_mul_mod(&pb, &g0, &xm);
                    uint8_t w = (uint8_t)poly_weight(&cw, m);

                    Poly cur = pb;
                    for (int step = 0; step < m; step++) {
                        for (int alpha = 1; alpha < q; alpha++) {
                            Poly scaled = cur;
                            for (int i = 0; i <= scaled.deg; i++) scaled.c[i] = GF_MUL[scaled.c[i]][alpha];
                            poly_normalize(&scaled);
                            uint32_t idx = poly_to_int(&scaled, k_max, q);
                            vis_full[idx] = 1;
                            wt_full[idx] = w;
                        }
                        cur = poly_mul_mod(&cur, &x_poly, &h_full);
                    }
                }
            }

            Poly *full_rep_polys = (Poly *)malloc(n_full_orbs * sizeof(Poly));
            for (int o = 0; o < n_full_orbs; o++) {
                full_rep_polys[o] = int_to_poly(full_reps[o], k_max, q);
            }

            /* Precompute all 1D and 2D subspaces of GF(q)^s when q_s <= MAX_QS */
            uint32_t sub1d[MAX_QS];
            int n_sub1d = 0;
            for (uint32_t r = 1; r < q_s; r++) {
                uint32_t tmp = r;
                int fnz = 0;
                while (tmp > 0) { int d = tmp % q; if (d != 0) { fnz = d; break; } tmp /= q; }
                if (fnz == 1) sub1d[n_sub1d++] = r;
            }

            /* Precompute all distinct 2D subspaces (represented by basis pair (r1, r2)) */
            uint32_t sub2d_r1[600], sub2d_r2[600];
            int n_sub2d = 0;
            if (s >= 2 && n_sub1d <= 64) {
                for (int i = 0; i < n_sub1d; i++) {
                    for (int j = i + 1; j < n_sub1d; j++) {
                        uint32_t r1 = sub1d[i], r2 = sub1d[j];
                        /* Canonical check: is (r1, r2) the lexicographically smallest projective pair in its 2D span? */
                        int is_canon = 1;
                        for (int a1 = 1; a1 < q && is_canon; a1++) {
                            for (int a2 = 1; a2 < q && is_canon; a2++) {
                                uint32_t comb = gf_vec_comb(
                                    gf_vec_comb(0, r1, a1, s, q),
                                    r2, a2, s, q
                                );
                                /* Normalize comb to monic */
                                uint32_t tmp = comb;
                                int fnz = 1;
                                while (tmp > 0) { int d = tmp % q; if (d != 0) { fnz = d; break; } tmp /= q; }
                                uint32_t monic = gf_vec_comb(0, comb, GF_INV[fnz], s, q);
                                if (monic < r2) is_canon = 0;
                            }
                        }
                        if (is_canon && n_sub2d < 600) {
                            sub2d_r1[n_sub2d] = r1;
                            sub2d_r2[n_sub2d] = r2;
                            n_sub2d++;
                        }
                    }
                }
            }

            uint64_t total_lifts = 1;
            for (int j = 1; j < l; j++) total_lifts *= q_s;
            int lift_samples = (total_lifts <= 1024) ? (int)total_lifts : 600;
            if (n_full_orbs > 20000 && lift_samples > 500) lift_samples = 500;
            int max_t_idx = (n_top > 6) ? 6 : n_top;

            for (int t_idx = 0; t_idx < max_t_idx; t_idx++) {
                int d_subcode = top_d_c2[t_idx];
                for (int l_samp = 0; l_samp < lift_samples; l_samp++) {
                    uint64_t code_u = (total_lifts <= (uint64_t)lift_samples) ? (uint64_t)l_samp : (xorshift64() % total_lifts);
                    Poly f_polys[MAX_L];
                    f_polys[0] = poly_one();
                    for (int j = 1; j < l; j++) {
                        uint32_t u_val = code_u % q_s;
                        code_u /= q_s;
                        Poly fc = int_to_poly(top_f_core[t_idx][j], k_core, q);
                        Poly u_poly = int_to_poly(u_val, s, q);
                        Poly term = poly_mul(&u_poly, h_core);
                        for (int i = 0; i <= term.deg; i++) {
                            fc.c[i] = GF_ADD[(i <= fc.deg) ? fc.c[i] : 0][term.c[i]];
                        }
                        if (term.deg > fc.deg) fc.deg = term.deg;
                        poly_normalize(&fc);
                        f_polys[j] = fc;
                    }

                    int W_orb[MAX_QS];
                    for (int cid = 0; cid < n_coset_orbs; cid++) W_orb[cid] = 9999;
                    W_orb[0] = d_subcode;

                    for (int o = 0; o < n_full_orbs; o++) {
                        int cid = full_rep_cid[o];
                        uint32_t b = full_reps[o];
                        int w = wt_full[b];
                        for (int j = 1; j < l; j++) {
                            Poly prod = poly_mul_mod(&full_rep_polys[o], &f_polys[j], &h_full);
                            w += wt_full[poly_to_int(&prod, k_max, q)];
                        }
                        if (w < W_orb[cid]) W_orb[cid] = w;
                    }

                    int W_min[MAX_QS];
                    W_min[0] = d_subcode;
                    for (uint32_t r = 1; r < q_s; r++) {
                        W_min[r] = W_orb[coset_orb_id[r]];
                    }

                    /* Case s_p = 1: pick best 1D subspace */
                    {
                        int s_p = 1;
                        int k = k_core + 1;
                        uint32_t best_r = sub1d[0];
                        for (int i = 1; i < n_sub1d; i++) {
                            if (W_min[sub1d[i]] > W_min[best_r]) best_r = sub1d[i];
                        }
                        uint32_t basis_r[1] = {best_r};
                        for (int t = 0; t <= 18; t++) {
                            int n = m * l + t;
                            if (n >= 256 || is_excluded_cell(q, n, k)) continue;
                            int d_lo = D_LO[q][n][k];
                            if (d_lo <= 0 || d_subcode <= d_lo) continue;
                            int d_target = d_lo + 1;
                            if (W_min[best_r] + t >= d_target) {
                                uint32_t T_cols[MAX_T];
                                for (int c = 0; c < t; c++) T_cols[c] = 1;
                                verify_and_save_code(q, m, lambda, l, h_core, h_sub,
                                                     f_polys, s_p, basis_r, t, T_cols, d_target);
                            }
                        }
                    }

                    /* Case s_p = 2: test ALL 2D subspaces in Grassmannian Gr(2, s)! */
                    if (s >= 2 && n_sub2d > 0) {
                        int s_p = 2;
                        int k = k_core + 2;
                        uint32_t q_sp = q * q;
                        for (int idx2 = 0; idx2 < n_sub2d; idx2++) {
                            uint32_t r1 = sub2d_r1[idx2], r2 = sub2d_r2[idx2];
                            uint32_t basis_r[2] = {r1, r2};
                            int sub_W[MAX_QS];
                            sub_W[0] = d_subcode;
                            for (uint32_t u = 1; u < q_sp; u++) {
                                int u0 = u % q, u1 = u / q;
                                uint32_t vec = gf_vec_comb(
                                    gf_vec_comb(0, r1, u0, s, q),
                                    r2, u1, s, q
                                );
                                sub_W[u] = W_min[vec];
                            }
                            for (int t = 0; t <= 18; t++) {
                                int n = m * l + t;
                                if (n >= 256 || is_excluded_cell(q, n, k)) continue;
                                int d_lo = D_LO[q][n][k];
                                if (d_lo <= 0 || d_subcode <= d_lo) continue;
                                int d_target = d_lo + 1;
                                int req[MAX_QS];
                                int possible = 1;
                                int sum_req = 0;
                                for (uint32_t u = 1; u < q_sp; u++) {
                                    req[u] = d_target - sub_W[u];
                                    if (req[u] > t) { possible = 0; break; }
                                    if (req[u] < 0) req[u] = 0;
                                    sum_req += req[u];
                                }
                                if (!possible || sum_req > t * (int)(q_sp - q)) continue;
                                uint32_t T_cols[MAX_T];
                                if (solve_tail_matrix(s_p, q, t, req, T_cols)) {
                                    verify_and_save_code(q, m, lambda, l, h_core, h_sub,
                                                         f_polys, s_p, basis_r, t, T_cols, d_target);
                                }
                            }
                        }
                    }

                    /* Case s_p = s (for s >= 3): full residue space */
                    if (s >= 3) {
                        int s_p = s;
                        int k = k_core + s;
                        uint32_t basis_r[MAX_S];
                        uint32_t pw = 1;
                        for (int i = 0; i < s; i++) { basis_r[i] = pw; pw *= q; }
                        for (int t = 0; t <= 18; t++) {
                            int n = m * l + t;
                            if (n >= 256 || is_excluded_cell(q, n, k)) continue;
                            int d_lo = D_LO[q][n][k];
                            if (d_lo <= 0 || d_subcode <= d_lo) continue;
                            int d_target = d_lo + 1;
                            int req[MAX_QS];
                            int possible = 1;
                            int sum_req = 0;
                            for (uint32_t u = 1; u < q_s; u++) {
                                req[u] = d_target - W_min[u];
                                if (req[u] > t) { possible = 0; break; }
                                if (req[u] < 0) req[u] = 0;
                                sum_req += req[u];
                            }
                            if (!possible || sum_req > t * (int)(q_s - q_s / q)) continue;
                            uint32_t T_cols[MAX_T];
                            if (solve_tail_matrix(s_p, q, t, req, T_cols)) {
                                verify_and_save_code(q, m, lambda, l, h_core, h_sub,
                                                     f_polys, s_p, basis_r, t, T_cols, d_target);
                            }
                        }
                    }
                }
            }

            free(vis_full);
            free(wt_full);
            free(full_reps);
            free(full_rep_cid);
            free(full_rep_polys);
        }
    }

    free(vis_core);
    free(wt_core);
    free(core_reps);
    free(core_rep_polys);
}

static void run_factor_combinations(
    int q, int m, int lambda, int l,
    int k_core_min, int k_core_max, int s_max, int max_iters, int max_combos
) {
    Poly factors[48];
    int n_fac = factor_xm_lambda(m, lambda, q, factors, 48);

    for (int i = 0; i < n_fac - 1; i++) {
        for (int j = i + 1; j < n_fac; j++) {
            if (factors[j].deg > factors[i].deg) {
                Poly tmp = factors[i];
                factors[i] = factors[j];
                factors[j] = tmp;
            }
        }
    }

    printf("[q=%d, m=%d, lambda=%d, l=%d] Factored x^%d - %d into %d irreducible factors: degs = [",
           q, m, lambda, l, m, lambda, n_fac);
    for (int i = 0; i < n_fac; i++) printf("%d%s", factors[i].deg, (i + 1 < n_fac) ? "," : "");
    printf("]\n");
    fflush(stdout);

    int n_use = (n_fac <= 20) ? n_fac : 20;
    uint64_t total_masks = 1ULL << n_use;
    uint64_t *valid_masks = (uint64_t *)malloc(4096 * sizeof(uint64_t));
    int n_valid = 0;

    /* Collect valid masks for each target degree from k_core_max down to k_core_min */
    for (int target_deg = k_core_max; target_deg >= k_core_min; target_deg--) {
        int cnt_deg = 0;
        for (uint64_t mask = 1; mask < total_masks; mask++) {
            int deg_core = 0;
            for (int i = 0; i < n_use; i++) {
                if ((mask >> i) & 1) deg_core += factors[i].deg;
            }
            if (deg_core == target_deg) {
                if (n_valid < 4096 && cnt_deg < 12) {
                    valid_masks[n_valid++] = mask;
                    cnt_deg++;
                }
            }
        }
    }

    int tested_combos = 0;
    for (int m_idx = 0; m_idx < n_valid && tested_combos < max_combos; m_idx++) {
        uint64_t mask_core = valid_masks[m_idx];
        int deg_core = 0;
        for (int i = 0; i < n_use; i++) {
            if ((mask_core >> i) & 1) deg_core += factors[i].deg;
        }

        Poly h_core = poly_one();
        for (int i = 0; i < n_use; i++) {
            if ((mask_core >> i) & 1) h_core = poly_mul(&h_core, &factors[i]);
        }

        Poly h_sub = poly_one();
        uint64_t q_km = 1;
        for (int d = 0; d < deg_core; d++) q_km *= q;
        for (int i = n_fac - 1; i >= 0; i--) {
            if (i < n_use && !((mask_core >> i) & 1)) {
                uint64_t next_q = q_km;
                for (int d = 0; d < factors[i].deg; d++) next_q *= q;
                if (h_sub.deg + factors[i].deg <= s_max && next_q <= (1ULL << 22)) {
                    h_sub = poly_mul(&h_sub, &factors[i]);
                    q_km = next_q;
                }
            }
        }
        if (h_sub.deg == 0) continue;
        tested_combos++;
        search_config(q, m, lambda, l, &h_core, &h_sub, max_iters);
    }
    free(valid_masks);
}

int main(int argc, char **argv) {
    load_bounds_tsv("data/bounds.tsv");
    int mode = (argc > 1) ? atoi(argv[1]) : 4;
    printf("=== Supercharged QC/QT + Grassmannian Construction X Search (mode=%d) ===\n", mode);

    if (mode == 4 || mode == 0) {
        init_gf(4);
        /* Fast scan across multiple factor combinations on q=4 */
        run_factor_combinations(4, 51, 1, 3, 7, 10, 3, 200, 12);
        run_factor_combinations(4, 51, 2, 3, 7, 10, 3, 200, 10);
        run_factor_combinations(4, 45, 1, 3, 6, 9, 3, 200, 10);
        run_factor_combinations(4, 45, 2, 3, 6, 9, 3, 200, 10);
        run_factor_combinations(4, 63, 1, 2, 6, 9, 3, 200, 10);
        run_factor_combinations(4, 65, 1, 2, 6, 9, 3, 200, 10);
        run_factor_combinations(4, 85, 1, 2, 6, 9, 3, 200, 10);
    }

    if (mode == 2 || mode == 0) {
        init_gf(2);
        run_factor_combinations(2, 85, 1, 2, 12, 17, 5, 300, 30);
        run_factor_combinations(2, 51, 1, 3, 14, 18, 4, 300, 25);
        run_factor_combinations(2, 51, 1, 4, 14, 18, 4, 300, 25);
        run_factor_combinations(2, 63, 1, 2, 14, 18, 5, 300, 25);
        run_factor_combinations(2, 63, 1, 3, 14, 17, 4, 300, 25);
        run_factor_combinations(2, 73, 1, 2, 14, 18, 4, 300, 25);
        run_factor_combinations(2, 93, 1, 2, 14, 17, 4, 300, 25);
    }

    if (mode == 3 || mode == 0) {
        init_gf(3);
        run_factor_combinations(3, 40, 1, 3, 7, 11, 3, 300, 25);
        run_factor_combinations(3, 40, 2, 3, 7, 11, 3, 300, 25);
        run_factor_combinations(3, 40, 1, 4, 7, 10, 3, 300, 25);
        run_factor_combinations(3, 52, 1, 3, 7, 10, 3, 300, 25);
        run_factor_combinations(3, 52, 2, 3, 7, 10, 3, 300, 25);
        run_factor_combinations(3, 28, 1, 4, 7, 11, 3, 300, 25);
        run_factor_combinations(3, 28, 2, 4, 7, 11, 3, 300, 25);
        run_factor_combinations(3, 35, 1, 4, 7, 10, 3, 300, 25);
    }

    if (mode == 5 || mode == 0) {
        init_gf(5);
        run_factor_combinations(5, 31, 1, 3, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 31, 4, 3, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 31, 1, 4, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 31, 4, 4, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 26, 1, 4, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 26, 4, 4, 5, 8, 2, 300, 25);
        run_factor_combinations(5, 39, 1, 3, 6, 8, 2, 300, 25);
    }

    if (mode == 7 || mode == 0) {
        init_gf(7);
        run_factor_combinations(7, 19, 1, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(7, 19, 6, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(7, 19, 1, 4, 4, 6, 2, 300, 25);
        run_factor_combinations(7, 24, 1, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(7, 24, 6, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(7, 30, 1, 3, 4, 6, 2, 300, 25);
    }

    if (mode == 8 || mode == 0) {
        init_gf(8);
        run_factor_combinations(8, 21, 1, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(8, 21, 1, 4, 4, 6, 2, 300, 25);
        run_factor_combinations(8, 21, 1, 5, 4, 6, 2, 300, 25);
        run_factor_combinations(8, 35, 1, 3, 4, 6, 2, 300, 25);
    }

    if (mode == 9 || mode == 0) {
        init_gf(9);
        run_factor_combinations(9, 20, 1, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(9, 20, 2, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(9, 20, 1, 4, 4, 6, 2, 300, 25);
        run_factor_combinations(9, 20, 2, 4, 4, 6, 2, 300, 25);
        run_factor_combinations(9, 26, 1, 3, 4, 6, 2, 300, 25);
        run_factor_combinations(9, 28, 1, 3, 4, 6, 2, 300, 25);
    }

    printf("=== Supercharged QC search finished ===\n");
    return 0;
}
