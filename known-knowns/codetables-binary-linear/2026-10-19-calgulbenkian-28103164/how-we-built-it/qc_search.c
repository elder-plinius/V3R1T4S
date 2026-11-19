/*
 * qc_search.c
 *
 * Lens 1 (symmetry-orbit-join):
 * CRT Hierarchical Orbit-Permutation & Coset-Weighted Construction X Search
 * for record-breaking [n, k, d]_q linear codes over GF(q), q in {2, 3, 4, 5}.
 *
 * Key mathematical mechanism:
 * 1. Let h(x) = h_core(x) * h_sub(x) divide (x^m - lambda) over GF(q), where
 *    deg(h_core) = k_core and deg(h_sub) = s.
 * 2. By the Orbit-Permutation Law, multiplication by <x, GF(q)*> partitions
 *    GF(q)[x]/(h_core) \ {0} into N_core constacyclic-scalar orbits O_o, all of
 *    whose elements have identical Hamming weight in every circulant/constacyclic
 *    block. Any multiplier polynomial f_j(x) simply permutes these orbits!
 * 3. By the Chinese Remainder Theorem (CRT), when gcd(h_core, h_sub) = 1, the
 *    subcode C_2 (of dimension k_core, where h_sub(x) | b(x)) depends ONLY on
 *    f_j(x) mod h_core(x). We first find (f_2^core, ..., f_l^core) maximizing
 *    the subcode distance d(C_2) over the N_core orbits of C_2.
 * 4. We then lift f_j^core to f_j in GF(q)[x]/(h_core * h_sub), compute the
 *    exact coset minimum weights W_min[r] for all r in GF(q)^s \ {0}, and solve
 *    the Coset-Weighted Tail covering problem: for any subspace V_{s'} subset
 *    GF(q)^s of dimension s' (1 <= s' <= s, giving code dimension k = k_core + s')
 *    and tail length t, find an s' x t matrix T over GF(q) such that
 *      wt(u * T) >= d_target - W_min[u * B]   for all u in GF(q)^{s'} \ {0}.
 */

#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "time.h"

#define MAX_M 128
#define MAX_K 26
#define MAX_L 5
#define MAX_T 24
#define MAX_S 7
#define MAX_QS 128

/* Finite field GF(q) tables for q in {2, 3, 4, 5} */
static int Q_VAL = 2;
static uint8_t GF_ADD[8][8];
static uint8_t GF_SUB[8][8];
static uint8_t GF_MUL[8][8];
static uint8_t GF_INV[8];

static void init_gf(int q) {
    Q_VAL = q;
    memset(GF_ADD, 0, sizeof(GF_ADD));
    memset(GF_SUB, 0, sizeof(GF_SUB));
    memset(GF_MUL, 0, sizeof(GF_MUL));
    memset(GF_INV, 0, sizeof(GF_INV));
    if (q == 2 || q == 3 || q == 5) {
        for (int a = 0; a < q; a++) {
            for (int b = 0; b < q; b++) {
                GF_ADD[a][b] = (a + b) % q;
                GF_SUB[a][b] = (a - b + q) % q;
                GF_MUL[a][b] = (a * b) % q;
                if (GF_MUL[a][b] == 1) GF_INV[a] = b;
            }
        }
    } else if (q == 4) {
        /* GF(4) = GF(2)[w] / (w^2 + w + 1) */
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
    }
}

/* Polynomial representation over GF(q): degree <= MAX_M */
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

/* Factor x^m - lambda over GF(q) into monic irreducible factors */
static int factor_xm_lambda(int m, int lambda, int q, Poly *factors, int max_factors) {
    Poly xm = poly_zero();
    xm.deg = m;
    xm.c[m] = 1;
    xm.c[0] = GF_SUB[0][lambda];

    int n_fac = 0;
    for (int d = 1; d <= m; d++) {
        uint64_t lim = 1;
        for (int i = 0; i < d; i++) lim *= q;
        if (lim > 2000000ULL && d < xm.deg) continue;
        if (d > xm.deg) break;
        if (d * 2 > xm.deg) {
            /* Remaining xm must be irreducible */
            if (xm.deg >= 1 && n_fac < max_factors) {
                /* make monic */
                uint8_t inv = GF_INV[xm.c[xm.deg]];
                for (int i = 0; i <= xm.deg; i++) xm.c[i] = GF_MUL[xm.c[i]][inv];
                factors[n_fac++] = xm;
                xm = poly_one();
            }
            break;
        }
        for (uint64_t mask = 1; mask < lim; mask++) {
            if ((mask % q) == 0) continue; /* constant term != 0 */
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

/* Bound table d_lo[q][n][k] and d_up[q][n][k] loaded from TSV/text or embedded */
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
    return 0;
}

/* RNG */
static uint64_t rng_state = 0x853c49e6748fea9bULL;
static uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

/*
 * Solve the Coset-Weighted Tail Problem:
 * Given s' (1 <= s' <= 7), q, tail length t (1 <= t <= MAX_T), and required tail
 * weight req[u] for each nonzero u in {1, ..., q^{s'} - 1}, find an s' x t
 * matrix T over GF(q) such that wt(u * T) >= req[u] for all u != 0.
 * Returns 1 if solved (writing columns into T_cols[0..t-1]), 0 otherwise.
 */
static int solve_tail_matrix(int s_prime, int q, int t, const int *req, uint32_t *T_cols) {
    uint32_t N = 1;
    for (int i = 0; i < s_prime; i++) N *= q;

    /* Check if t == 0 already satisfies all req[u] <= 0 */
    int max_req = 0;
    for (uint32_t u = 1; u < N; u++) {
        if (req[u] > max_req) max_req = req[u];
    }
    if (max_req <= 0) return 1;
    if (max_req > t) return 0;

    /* Precompute dot products <u, col> != 0 for all u in 1..N-1 and projective cols */
    uint32_t proj_cols[MAX_QS];
    int p_cnt = 0;
    for (uint32_t c = 1; c < N; c++) {
        /* Canonical projective vector: first nonzero coordinate == 1 */
        uint32_t tmp = c;
        int first_nz = 0;
        while (tmp > 0) {
            int digit = tmp % q;
            if (digit != 0) {
                first_nz = digit;
                break;
            }
            tmp /= q;
        }
        if (first_nz == 1 && p_cnt < MAX_QS) {
            proj_cols[p_cnt++] = c;
        }
    }

    /* Precompute support bitmask or indicator: cov[p_idx][u] = 1 if <u, proj_cols[p_idx]> != 0 */
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

    /* Multi-start greedy + tabu column replacement */
    int cur_wt[MAX_QS];
    int cols_idx[MAX_T];

    for (int restart = 0; restart < 40; restart++) {
        memset(cur_wt, 0, sizeof(cur_wt));
        /* Greedy construction of t columns */
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
                /* Small random tie-break on restarts > 0 */
                if (restart > 0) sc = sc * 8 + (xorshift64() & 7);
                if (sc > best_score) {
                    best_score = sc;
                    best_p = p;
                }
            }
            cols_idx[j] = best_p;
            for (uint32_t u = 1; u < N; u++) cur_wt[u] += cov[best_p][u];
        }

        /* Check if solved */
        int total_def = 0;
        for (uint32_t u = 1; u < N; u++) {
            if (cur_wt[u] < req[u]) total_def += (req[u] - cur_wt[u]);
        }
        if (total_def == 0) {
            for (int j = 0; j < t; j++) T_cols[j] = proj_cols[cols_idx[j]];
            return 1;
        }

        /* Local search (column replacement) */
        for (int step = 0; step < 250 && total_def > 0; step++) {
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

/* Build explicit generator matrix and verify exact minimum distance via full row-space odometer */
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

    /*
     * Construct the k basis message polynomials b_0(x), ..., b_{k-1}(x) in GF(q)[x]/(h_full):
     * - First k_core rows: b_i(x) = x^i * h_sub(x)  (0 <= i < k_core).
     *   Notice b_i(x) mod h_sub(x) == 0, so tail columns are 0 on these k_core rows!
     * - Next s_prime rows: for each basis vector basis_r[idx] in GF(q)^s (0 <= idx < s_prime),
     *   let r_poly(x) be the polynomial of degree < s representing basis_r[idx].
     *   Row k_core + idx has message polynomial b(x) = r_poly(x), and its tail row is
     *   e_{idx} * T!
     */
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
        /* Tail coordinates are 0 since b_poly == 0 mod h_sub */
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
        /* Tail coordinate c_idx for row_idx is the idx-th digit of T_cols[c_idx] */
        for (int c = 0; c < t; c++) {
            uint32_t col = T_cols[c];
            for (int p = 0; p < idx; p++) col /= q;
            G[row_idx][m * l + c] = col % q;
        }
    }

    /* Quick exact full-enumeration verification over monic messages in GF(q)^k */
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
                if (min_w < d_target) return 0; /* early abort if invalid */
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

    /* Update live lower bound so we only report strictly better records for (q, n, k) */
    D_LO[q][n][k] = min_w;

    printf("\n*** BREAKTHROUGH WIN: [%d, %d, %d]_%d (beats codetables.de d_lo=%d, d_up=%d, A_d=%llu) ***\n",
           n, k, min_w, q, d_lo_orig, d_up, (unsigned long long)A_d);
    fflush(stdout);

    char fname[256];
    snprintf(fname, sizeof(fname), "attempts/symmetry-orbit-join/result/win_q%d_n%d_k%d_d%d.json",
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

/*
 * Search a specific (q, m, lambda, l, h_core, h_sub) configuration
 */
static void search_config(
    int q, int m, int lambda, int l,
    const Poly *h_core, const Poly *h_sub,
    int max_iters
) {
    int k_core = h_core->deg;
    int s = h_sub->deg;
    int k_max = k_core + s;
    if (k_core < 4 || k_max >= MAX_K) return;

    uint64_t q_kcore = 1;
    for (int i = 0; i < k_core; i++) q_kcore *= q;
    uint64_t q_kmax = q_kcore;
    for (int i = 0; i < s; i++) q_kmax *= q;
    if (q_kmax > (1ULL << 22)) return;

    /* Check if any (n = m*l + t, k = k_core + s') in range has an open bound worth attacking */
    int any_open = 0;
    for (int s_p = 0; s_p <= s; s_p++) {
        int k = k_core + s_p;
        for (int t = 0; t <= 16; t++) {
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

    /* 1. Partition GF(q)[x]/(h_core) \ {0} into constacyclic-scalar orbits */
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

    /* Sort core_reps in increasing order of wt_core[core_reps[o]] for instant early exit */
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

    /*
     * 2. Find the best core multiplier tuples (f_2^core, ..., f_l^core) maximizing d(C_2).
     * Keep a top list of up to 6 distinct core multiplier tuples achieving best_d_c2.
     */
    int best_d_c2 = 0;
    uint32_t top_f_core[8][MAX_L];
    int top_d_c2[8];
    int n_top = 0;

    if (l == 2) {
        /* 100% exhaustive scan over all n_core_orbs choices of f_2^core */
        for (int o2 = 0; o2 < n_core_orbs; o2++) {
            Poly f2 = core_rep_polys[o2];
            int d_min = 9999;
            int cutoff = (best_d_c2 > 0) ? best_d_c2 : 1;
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
            if (d_min == best_d_c2 && n_top < 8) {
                top_f_core[n_top][0] = 1;
                top_f_core[n_top][1] = core_reps[o2];
                top_d_c2[n_top] = d_min;
                n_top++;
            }
        }
    } else {
        /* Coordinate descent over orbit representatives for l >= 3 */
        int *w_partial = (int *)malloc(n_core_orbs * sizeof(int));
        int actual_iters = (n_core_orbs > 1500) ? 30 : max_iters;
        for (int restart = 0; restart < actual_iters; restart++) {
            uint32_t cur_f[MAX_L];
            cur_f[0] = 1;
            for (int j = 1; j < l; j++) {
                cur_f[j] = core_reps[xorshift64() % n_core_orbs];
            }
            int cur_d = 0;
            for (int sweep = 0; sweep < 2; sweep++) {
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
                    int n_try = (n_core_orbs <= 400) ? n_core_orbs : 400;
                    for (int t_idx = 0; t_idx < n_try; t_idx++) {
                        int cand_o = (n_core_orbs <= 400) ? t_idx : (int)(xorshift64() % n_core_orbs);
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
                        }
                    }
                    cur_f[j] = best_j_f;
                    cur_d = best_j_d;
                }
            }
            if (cur_d > best_d_c2) {
                best_d_c2 = cur_d;
                n_top = 0;
            }
            if (cur_d == best_d_c2 && n_top < 8) {
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

    /* Check if best_d_c2 directly beats codetables at k = k_core, t = 0 */
    if (!is_excluded_cell(q, m * l, k_core) &&
        D_LO[q][m * l][k_core] > 0 &&
        best_d_c2 > D_LO[q][m * l][k_core]) {
        Poly f_polys[MAX_L];
        f_polys[0] = poly_one();
        for (int j = 1; j < l; j++) f_polys[j] = int_to_poly(top_f_core[0][j], k_core, q);
        Poly h_one = poly_one();
        verify_and_save_code(q, m, lambda, l, h_core, &h_one, f_polys, 0, NULL, 0, NULL, best_d_c2);
    }

    /* Check if best_d_c2 is high enough to beat ANY open bound at k = k_core + s' (1 <= s' <= s) */
    int worth_lifting = 0;
    for (int s_p = 1; s_p <= s; s_p++) {
        int k = k_core + s_p;
        for (int t = 0; t <= 16; t++) {
            int n = m * l + t;
            if (n < 256 && !is_excluded_cell(q, n, k) &&
                D_LO[q][n][k] > 0 && best_d_c2 > D_LO[q][n][k]) {
                worth_lifting = 1;
                break;
            }
        }
    }

    if (worth_lifting && s >= 1 && n_top > 0) {
        /* 3. Build full-code orbit table for h_full = h_core * h_sub */
        Poly h_full = poly_mul(h_core, h_sub);
        Poly g0;
        poly_divmod(&xm, &h_full, &g0, &rem);
        if (poly_is_zero(&rem)) {
            uint32_t q_s = 1;
            for (int i = 0; i < s; i++) q_s *= q;

            /* Precompute coset orbits in GF(q)[x]/(h_sub) */
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

            uint64_t total_lifts = 1;
            for (int j = 1; j < l; j++) total_lifts *= q_s;
            int lift_samples = (q == 4 && m == 51 && l == 3 && best_d_c2 >= 100)
                               ? 300
                               : ((total_lifts <= 48) ? (int)total_lifts : 48);

            for (int t_idx = 0; t_idx < n_top; t_idx++) {
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

                    /* Compute coset orbit minimum weights W_orb[cid] in a single pass! */
                    int W_orb[MAX_QS];
                    for (int cid = 0; cid < n_coset_orbs; cid++) W_orb[cid] = 9999;
                    W_orb[0] = d_subcode;

                    for (int o = 0; o < n_full_orbs; o++) {
                        uint32_t b = full_reps[o];
                        int w = wt_full[b];
                        for (int j = 1; j < l; j++) {
                            Poly prod = poly_mul_mod(&full_rep_polys[o], &f_polys[j], &h_full);
                            w += wt_full[poly_to_int(&prod, k_max, q)];
                        }
                        int cid = full_rep_cid[o];
                        if (w < W_orb[cid]) W_orb[cid] = w;
                    }

                    int W_min[MAX_QS];
                    W_min[0] = d_subcode;
                    for (uint32_t r = 1; r < q_s; r++) {
                        W_min[r] = W_orb[coset_orb_id[r]];
                    }

                    /*
                     * Test subspaces V_{s'} subset GF(q)^s for 1 <= s' <= s
                     */
                    for (int s_p = 1; s_p <= s; s_p++) {
                        int k = k_core + s_p;
                        uint32_t basis_r[MAX_S];
                        int sub_W[MAX_QS];

                        if (s_p == s) {
                            uint32_t pw = 1;
                            for (int i = 0; i < s; i++) { basis_r[i] = pw; pw *= q; }
                            for (uint32_t u = 1; u < q_s; u++) sub_W[u] = W_min[u];
                        } else if (s_p == 2 && q == 2) {
                            uint32_t best_r1 = 0, best_r2 = 0;
                            int best_min3 = -1, best_sum3 = -1;
                            for (uint32_t r1 = 1; r1 < q_s; r1++) {
                                for (uint32_t r2 = r1 + 1; r2 < q_s; r2++) {
                                    uint32_t r3 = r1 ^ r2;
                                    int w1 = W_min[r1], w2 = W_min[r2], w3 = W_min[r3];
                                    int mn = w1;
                                    if (w2 < mn) mn = w2;
                                    if (w3 < mn) mn = w3;
                                    int sm = w1 + w2 + w3;
                                    if (mn > best_min3 || (mn == best_min3 && sm > best_sum3)) {
                                        best_min3 = mn;
                                        best_sum3 = sm;
                                        best_r1 = r1;
                                        best_r2 = r2;
                                    }
                                }
                            }
                            if (best_r1 == 0) continue;
                            basis_r[0] = best_r1;
                            basis_r[1] = best_r2;
                            sub_W[1] = W_min[best_r1];
                            sub_W[2] = W_min[best_r2];
                            sub_W[3] = W_min[best_r1 ^ best_r2];
                        } else {
                            uint32_t span_set[MAX_QS];
                            uint8_t in_span[MAX_QS];
                            memset(in_span, 0, sizeof(in_span));
                            span_set[0] = 0;
                            in_span[0] = 1;
                            int cur_span_sz = 1;
                            int ok_basis = 1;

                            for (int b_idx = 0; b_idx < s_p; b_idx++) {
                                uint32_t best_r = 0;
                                int best_min_w = -1;
                                int best_sum_w = -1;
                                for (uint32_t cand_r = 1; cand_r < q_s; cand_r++) {
                                    if (in_span[cand_r]) continue;
                                    int min_new_w = W_min[cand_r];
                                    int sum_new_w = 0;
                                    for (int sp = 0; sp < cur_span_sz; sp++) {
                                        for (int alpha = 1; alpha < q; alpha++) {
                                            uint32_t v1 = span_set[sp], v2 = cand_r, comb = 0, pw = 1;
                                            for (int d_i = 0; d_i < s; d_i++) {
                                                uint8_t c1 = v1 % q, c2 = v2 % q;
                                                v1 /= q; v2 /= q;
                                                uint8_t sum = GF_ADD[c1][GF_MUL[alpha][c2]];
                                                comb += sum * pw;
                                                pw *= q;
                                            }
                                            if (W_min[comb] < min_new_w) min_new_w = W_min[comb];
                                            sum_new_w += W_min[comb];
                                        }
                                    }
                                    if (min_new_w > best_min_w || (min_new_w == best_min_w && sum_new_w > best_sum_w)) {
                                        best_min_w = min_new_w;
                                        best_sum_w = sum_new_w;
                                        best_r = cand_r;
                                    }
                                }
                                if (best_r == 0) { ok_basis = 0; break; }
                                basis_r[b_idx] = best_r;
                                int old_sz = cur_span_sz;
                                for (int sp = 0; sp < old_sz; sp++) {
                                    for (int alpha = 1; alpha < q; alpha++) {
                                        uint32_t v1 = span_set[sp], v2 = best_r, comb = 0, pw = 1;
                                        for (int d_i = 0; d_i < s; d_i++) {
                                            uint8_t c1 = v1 % q, c2 = v2 % q;
                                            v1 /= q; v2 /= q;
                                            uint8_t sum = GF_ADD[c1][GF_MUL[alpha][c2]];
                                            comb += sum * pw;
                                            pw *= q;
                                        }
                                        span_set[cur_span_sz++] = comb;
                                        in_span[comb] = 1;
                                    }
                                }
                                for (int sp = 1; sp < cur_span_sz; sp++) {
                                    sub_W[sp] = W_min[span_set[sp]];
                                }
                            }
                            if (!ok_basis) continue;
                        }

                        uint32_t q_sp = 1;
                        for (int i = 0; i < s_p; i++) q_sp *= q;

                        for (int t = 0; t <= 16; t++) {
                            int n = m * l + t;
                            if (n >= 256 || is_excluded_cell(q, n, k)) continue;
                            int d_lo = D_LO[q][n][k];
                            if (d_lo <= 0 || d_subcode <= d_lo) continue;
                            int d_target = d_lo + 1;
                            int req[MAX_QS];
                            int possible = 1;
                            for (uint32_t u = 1; u < q_sp; u++) {
                                req[u] = d_target - sub_W[u];
                                if (req[u] > t) { possible = 0; break; }
                                if (req[u] < 0) req[u] = 0;
                            }
                            if (!possible) continue;

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

/* Recursively enumerate subsets of irreducible factors of x^m - lambda to form h_core and h_sub */
static void run_factor_combinations(
    int q, int m, int lambda, int l,
    int k_core_min, int k_core_max, int s_max, int max_iters
) {
    Poly factors[40];
    int n_fac = factor_xm_lambda(m, lambda, q, factors, 40);

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

    int tested_combos = 0;
    uint64_t total_masks = (n_fac <= 20) ? (1ULL << n_fac) : (1ULL << 20);

    for (uint64_t mask_core = 1; mask_core < total_masks && tested_combos < 14; mask_core++) {
        int deg_core = 0;
        for (int i = 0; i < n_fac && i < 20; i++) {
            if ((mask_core >> i) & 1) deg_core += factors[i].deg;
        }
        if (deg_core < k_core_min || deg_core > k_core_max) continue;
        tested_combos++;

        Poly h_core = poly_one();
        for (int i = 0; i < n_fac && i < 20; i++) {
            if ((mask_core >> i) & 1) h_core = poly_mul(&h_core, &factors[i]);
        }

        Poly h_sub = poly_one();
        for (int i = n_fac - 1; i >= 0; i--) {
            if (i < 20 && !((mask_core >> i) & 1)) {
                if (h_sub.deg + factors[i].deg <= s_max) {
                    h_sub = poly_mul(&h_sub, &factors[i]);
                }
            }
        }

        search_config(q, m, lambda, l, &h_core, &h_sub, max_iters);
    }
}

int main(int argc, char **argv) {
    load_bounds_tsv("attempts/symmetry-orbit-join/bounds.tsv");

    int mode = (argc > 1) ? atoi(argv[1]) : 0;
    printf("=== Lens 1: CRT Orbit-Permutation & Coset-Weighted Construction X Search (mode=%d) ===\n", mode);

    if (mode == 0 || mode == 2) {
        init_gf(2);
        /* 1. m=85, l=2 (base=170): target k=16, 17, 18 and k=23, 24 (outside LinCodeEvolve k=19..22!) */
        run_factor_combinations(2, 85, 1, 2, 12, 16, 5, 120);
        /* 2. m=51, l=3 (base=153, n=153..169 < 170, outside LinCodeEvolve!): target k=16..20 */
        run_factor_combinations(2, 51, 1, 3, 15, 18, 4, 150);
        /* 3. m=51, l=4 (base=204): target k=16, 17, 18 (outside LinCodeEvolve k=19..22!) */
        run_factor_combinations(2, 51, 1, 4, 15, 18, 3, 120);
        /* 4. m=63, l=2 (base=126 < 170): target k=18..23 */
        run_factor_combinations(2, 63, 1, 2, 15, 18, 5, 100);
        /* 5. m=63, l=3 (base=189): target k=15..18 (outside LinCodeEvolve!) */
        run_factor_combinations(2, 63, 1, 3, 14, 16, 4, 150);
        /* 6. m=65, l=2,3 (base=130, 195): target k=16, 17, 18 */
        run_factor_combinations(2, 65, 1, 2, 12, 16, 5, 100);
        run_factor_combinations(2, 65, 1, 3, 12, 16, 5, 150);
        /* 7. m=105, l=2 (base=210): target k=15..18 */
        run_factor_combinations(2, 105, 1, 2, 14, 16, 4, 100);
    }

    if (mode == 0 || mode == 3) {
        rng_state = 0x853c49e6748fea9bULL;
        init_gf(3);
        /* GF(3) QC and Constacyclic (lambda = 1, 2) */
        run_factor_combinations(3, 40, 1, 2, 7, 11, 3, 120);
        run_factor_combinations(3, 40, 2, 2, 7, 11, 3, 120);
        run_factor_combinations(3, 40, 1, 3, 7, 11, 3, 150);
        run_factor_combinations(3, 26, 1, 3, 7, 11, 3, 150);
        run_factor_combinations(3, 26, 2, 3, 7, 11, 3, 150);
        run_factor_combinations(3, 26, 1, 4, 7, 11, 3, 150);
        run_factor_combinations(3, 28, 1, 3, 7, 11, 3, 150);
        run_factor_combinations(3, 28, 2, 3, 7, 11, 3, 150);
        run_factor_combinations(3, 52, 1, 2, 7, 11, 3, 120);
        run_factor_combinations(3, 52, 2, 2, 7, 11, 3, 120);
        run_factor_combinations(3, 80, 1, 2, 8, 11, 3, 120);
    }

    if (mode == 0 || mode == 4) {
        rng_state = 0x853c49e6748fea9bULL;
        init_gf(4);
        /* GF(4) QC and Constacyclic (lambda = 1, 2) */
        run_factor_combinations(4, 51, 1, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 51, 2, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 51, 1, 3, 6, 9, 3, 150);
        run_factor_combinations(4, 63, 1, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 65, 1, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 85, 1, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 35, 1, 3, 6, 9, 3, 150);
        run_factor_combinations(4, 45, 1, 2, 6, 9, 3, 120);
        run_factor_combinations(4, 45, 1, 3, 6, 9, 3, 150);
    }

    if (mode == 0 || mode == 5) {
        rng_state = 0x853c49e6748fea9bULL;
        init_gf(5);
        /* GF(5) QC and Constacyclic (lambda = 1, 2, 4) */
        run_factor_combinations(5, 31, 1, 2, 5, 7, 2, 120);
        run_factor_combinations(5, 31, 4, 2, 5, 7, 2, 120);
        run_factor_combinations(5, 31, 1, 3, 5, 7, 2, 150);
        run_factor_combinations(5, 31, 1, 4, 5, 7, 2, 150);
        run_factor_combinations(5, 26, 1, 3, 5, 7, 2, 150);
        run_factor_combinations(5, 26, 4, 3, 5, 7, 2, 150);
        run_factor_combinations(5, 24, 1, 3, 5, 7, 2, 150);
        run_factor_combinations(5, 24, 4, 3, 5, 7, 2, 150);
    }

    printf("=== Lens 1 search finished ===\n");
    return 0;
}
