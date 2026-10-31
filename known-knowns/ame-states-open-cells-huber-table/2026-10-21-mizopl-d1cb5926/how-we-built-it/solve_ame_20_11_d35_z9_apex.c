/*
 * solve_ame_20_11_d35_z9_apex.c — Theorem D35: Apex-Bordered Z_9 Unitary Engine
 * for AME(20, 11) ([[20, 0, 11]]_11) and AME(19, 11) ([[19, 0, 10]]_11)
 * ==============================================================================
 * Structural Pivot (M2): Moving from 10 = 5 + 5 (D_5 x Z_2) to 10 = 9 + 1 (Z_9 x| Z_2):
 *
 *   U = [ C               beta * 1_9 ]
 *       [ -conj(beta)1_9^T   u_inf   ]  in U(10, F_121),
 *
 * where C in C_9(F_121) is a 9x9 circulant satisfying:
 *   1. u_inf * conj(u_inf) + 9 * beta * conj(beta) = 1  (mod 11),
 *   2. lambda_0(C) = conj(u_inf),
 *   3. C * C^\dagger |_{1_9^\perp} = I_8.
 *
 * By Theorem D35, 1_9^\perp subset C_9(F_121) splits into Ideal_0 (m=3,6 over F_121),
 * Ideal_1 = F_121[S]/(S^3 - W3) ~= F_{11^6}, and Ideal_2 = F_121[S]/(S^3 - W3^2) ~= F_{11^6},
 * giving a 0-inversion bijective parameterization of all 255,498,624 unitary 9x9 circulants on 1_9^\perp:
 *   (lambda_3, lambda_6, z_1, z_2) in C_12 x C_12 x C_1332 x C_1332.
 *
 * Symmetry group G_18 = Z_9 x| Z_2 (order 18 at r=1..4, order 36 at r=5 with J_comp)
 * has ZERO forced zero minors across all ranks r=1..5 and orbit counts:
 *   sub = 126 [0, 0, 0, 0, 126] (0 sub orbits at r=1..4!),
 *   ext = 5,327 [11, 135, 861, 2556, 1764],
 *   tot = 5,453 (24.413 decades).
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define P 11
#define Q2 121
#define NONRES 7

static uint8_t mul_tab[121][121], add_tab[121][121], sub_tab[121][121], neg_tab[121], inv_tab[121], conj_tab[121];
static uint8_t u1_tab[12];
static uint8_t W3, W3_2;
static uint8_t z1_tab[1332][3], z2_tab[1332][3];
static int z1_mult[1332][12], z2_mult[1332][12];

static int modp(int x) { x %= P; return x < 0 ? x + P : x; }

static void init_gf121(void) {
    for (int a = 0; a < Q2; a++) {
        int a0 = a % P, a1 = a / P;
        conj_tab[a] = (uint8_t)(a0 + modp(-a1) * P);
        neg_tab[a] = (uint8_t)(modp(-a0) + modp(-a1) * P);
        for (int b = 0; b < Q2; b++) {
            int b0 = b % P, b1 = b / P;
            add_tab[a][b] = (uint8_t)(modp(a0 + b0) + modp(a1 + b1) * P);
            sub_tab[a][b] = (uint8_t)(modp(a0 - b0) + modp(a1 - b1) * P);
            int c0 = modp(a0 * b0 + NONRES * a1 * b1);
            int c1 = modp(a0 * b1 + a1 * b0);
            mul_tab[a][b] = (uint8_t)(c0 + c1 * P);
        }
    }
    inv_tab[0] = 0;
    for (int a = 1; a < Q2; a++)
        for (int b = 1; b < Q2; b++)
            if (mul_tab[a][b] == 1) { inv_tab[a] = (uint8_t)b; break; }

    int u1c = 0;
    for (int a = 1; a < Q2; a++)
        if (mul_tab[a][conj_tab[a]] == 1) u1_tab[u1c++] = (uint8_t)a;

    for (int i = 0; i < 12; i++) {
        uint8_t w = u1_tab[i];
        if (w != 1 && mul_tab[w][mul_tab[w][w]] == 1) {
            W3 = w;
            W3_2 = mul_tab[w][w];
            break;
        }
    }

    int c1 = 0, c2 = 0;
    for (int a0 = 0; a0 < 121; a0++)
        for (int a1 = 0; a1 < 121; a1++)
            for (int a2 = 0; a2 < 121; a2++) {
                uint8_t ca0 = conj_tab[a0], ca1 = conj_tab[a1], ca2 = conj_tab[a2];
                uint8_t n0 = add_tab[mul_tab[a0][ca0]][add_tab[mul_tab[a1][ca1]][mul_tab[a2][ca2]]];
                if (n0 != 1) continue;
                uint8_t base = add_tab[mul_tab[a1][ca0]][mul_tab[a2][ca1]];
                uint8_t n1_w3  = add_tab[base][mul_tab[W3_2][mul_tab[a0][ca2]]];
                uint8_t n1_w32 = add_tab[base][mul_tab[W3][mul_tab[a0][ca2]]];
                if (n1_w3 == 0)  { z1_tab[c1][0] = a0; z1_tab[c1][1] = a1; z1_tab[c1][2] = a2; c1++; }
                if (n1_w32 == 0) { z2_tab[c2][0] = a0; z2_tab[c2][1] = a1; z2_tab[c2][2] = a2; c2++; }
            }
}

/* Z_9 shift on {0..8}, fixing 9 */
static inline int s9_idx(int x, int s) {
    return (x == 9) ? 9 : ((x + s) % 9);
}

static uint32_t apply_z9(uint32_t m, int s, int rev_tr, int comp) {
    if (comp) m = (~m) & 0xFFFFFu;
    uint32_t rmask = m & 0x3FFu;
    uint32_t cmask = (m >> 10) & 0x3FFu;
    if (rev_tr) {
        uint32_t nr = (cmask & (1u << 9)), nc = (rmask & (1u << 9));
        for (int i = 0; i < 9; i++) {
            int ni = (9 - i) % 9;
            if ((cmask >> i) & 1) nr |= (1u << ni);
            if ((rmask >> i) & 1) nc |= (1u << ni);
        }
        rmask = nr; cmask = nc;
    }
    uint32_t nr = (rmask & (1u << 9)), nc = (cmask & (1u << 9));
    for (int i = 0; i < 9; i++) {
        int ni = (i + s) % 9;
        if ((rmask >> i) & 1) nr |= (1u << ni);
        if ((cmask >> i) & 1) nc |= (1u << ni);
    }
    return nr | (nc << 10);
}

/* Combinatorial Plücker indexing with Z_9 row canonicalization */
static int pair_id[10][10];
static uint8_t pairs[45][2];
static int pair_shift[45][9];
static uint8_t pair_flip[45][9];
static int pair_canon_idx[45], pair_canon_s[45];
static uint8_t pair_canon_flip[45];
static int canon_pairs[5]; /* 5 Z_9-orbits on 45 pairs! */

static int triple_id[10][10][10];
static uint8_t triples[120][3];
static int triple_shift[120][9];
static uint8_t triple_flip[120][9];
static int triple_canon_idx[120], triple_canon_s[120];
static uint8_t triple_canon_flip[120];
static int canon_triples[14]; /* 14 Z_9-orbits on 120 triples! */

static int quad_id[10][10][10][10];
static uint8_t quads[210][4];
static int quad_shift[210][9];
static uint8_t quad_flip[210][9];
static int quad_canon_idx[210], quad_canon_s[210];
static uint8_t quad_canon_flip[210];
static int canon_quads[24]; /* 24 Z_9-orbits on 210 quads! */

static int quint_id[10][10][10][10][10];
static uint8_t quints[252][5];

static void sort_arr(int n, int *a, int *flips) {
    *flips = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i] > a[j]) { int t = a[i]; a[i] = a[j]; a[j] = t; (*flips) ^= 1; }
}

static void init_combinatorics(void) {
    int pid = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++) {
            pair_id[i][j] = pid; pairs[pid][0] = i; pairs[pid][1] = j; pid++;
        }
    for (int p = 0; p < 45; p++) {
        for (int s = 0; s < 9; s++) {
            int a[2] = { s9_idx(pairs[p][0], s), s9_idx(pairs[p][1], s) }, fl;
            sort_arr(2, a, &fl);
            pair_shift[p][s] = pair_id[a[0]][a[1]];
            pair_flip[p][s] = (uint8_t)fl;
        }
    }
    int cp_cnt = 0;
    memset(pair_canon_idx, -1, sizeof(pair_canon_idx));
    for (int p = 0; p < 45; p++) {
        if (pair_canon_idx[p] != -1) continue;
        int cid = cp_cnt++;
        canon_pairs[cid] = p;
        for (int s = 0; s < 9; s++) {
            int ps = pair_shift[p][s];
            if (pair_canon_idx[ps] == -1) {
                pair_canon_idx[ps] = cid;
                pair_canon_s[ps] = (9 - s) % 9; /* shift ps by (9-s) gives p! */
                pair_canon_flip[ps] = pair_flip[ps][(9 - s) % 9];
            }
        }
    }

    int tid = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++)
            for (int k = j + 1; k < 10; k++) {
                triple_id[i][j][k] = tid;
                triples[tid][0] = i; triples[tid][1] = j; triples[tid][2] = k;
                tid++;
            }
    for (int t = 0; t < 120; t++) {
        for (int s = 0; s < 9; s++) {
            int a[3] = { s9_idx(triples[t][0], s), s9_idx(triples[t][1], s), s9_idx(triples[t][2], s) }, fl;
            sort_arr(3, a, &fl);
            triple_shift[t][s] = triple_id[a[0]][a[1]][a[2]];
            triple_flip[t][s] = (uint8_t)fl;
        }
    }
    int ct_cnt = 0;
    memset(triple_canon_idx, -1, sizeof(triple_canon_idx));
    for (int t = 0; t < 120; t++) {
        if (triple_canon_idx[t] != -1) continue;
        int cid = ct_cnt++;
        canon_triples[cid] = t;
        for (int s = 0; s < 9; s++) {
            int ts = triple_shift[t][s];
            if (triple_canon_idx[ts] == -1) {
                triple_canon_idx[ts] = cid;
                triple_canon_s[ts] = (9 - s) % 9;
                triple_canon_flip[ts] = triple_flip[ts][(9 - s) % 9];
            }
        }
    }

    int qid = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++)
            for (int k = j + 1; k < 10; k++)
                for (int l = k + 1; l < 10; l++) {
                    quad_id[i][j][k][l] = qid;
                    quads[qid][0] = i; quads[qid][1] = j; quads[qid][2] = k; quads[qid][3] = l;
                    qid++;
                }
    for (int q = 0; q < 210; q++) {
        for (int s = 0; s < 9; s++) {
            int a[4] = { s9_idx(quads[q][0], s), s9_idx(quads[q][1], s), s9_idx(quads[q][2], s), s9_idx(quads[q][3], s) }, fl;
            sort_arr(4, a, &fl);
            quad_shift[q][s] = quad_id[a[0]][a[1]][a[2]][a[3]];
            quad_flip[q][s] = (uint8_t)fl;
        }
    }
    int cq_cnt = 0;
    memset(quad_canon_idx, -1, sizeof(quad_canon_idx));
    for (int q = 0; q < 210; q++) {
        if (quad_canon_idx[q] != -1) continue;
        int cid = cq_cnt++;
        canon_quads[cid] = q;
        for (int s = 0; s < 9; s++) {
            int qs = quad_shift[q][s];
            if (quad_canon_idx[qs] == -1) {
                quad_canon_idx[qs] = cid;
                quad_canon_s[qs] = (9 - s) % 9;
                quad_canon_flip[qs] = quad_flip[qs][(9 - s) % 9];
            }
        }
    }

    int q5id = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++)
            for (int k = j + 1; k < 10; k++)
                for (int l = k + 1; l < 10; l++)
                    for (int m = l + 1; m < 10; m++) {
                        quint_id[i][j][k][l][m] = q5id;
                        quints[q5id][0] = i; quints[q5id][1] = j; quints[q5id][2] = k;
                        quints[q5id][3] = l; quints[q5id][4] = m;
                        q5id++;
                    }
    printf("Z_9 canonical subsets: pairs=%d, triples=%d, quads=%d\n", cp_cnt, ct_cnt, cq_cnt);
}

typedef struct { uint8_t r_cid, c_id; } OrbitRep2;
typedef struct { uint8_t r_cid, c_id; } OrbitRep3;
typedef struct { uint8_t r_cid, c_id; } OrbitRep4;
typedef struct {
    uint8_t r_last;
    uint8_t r_qcid;
    uint8_t col_x[5];
    uint8_t col_q_shifted[5];
    uint8_t flip_total[5];
} OrbitRep5;

static OrbitRep2 ext_r2[135]; static int n_ext_r2 = 0;
static OrbitRep3 ext_r3[861]; static int n_ext_r3 = 0;
static OrbitRep4 ext_r4[2556]; static int n_ext_r4 = 0;
static OrbitRep5 sub_r5[126]; static int n_sub_r5 = 0;
static OrbitRep5 ext_r5[1764]; static int n_ext_r5 = 0;

static void build_orbits(void) {
    uint8_t *vis = (uint8_t *)calloc(1 << 20, 1);
    for (uint32_t m = 0; m < (1u << 20); m++) {
        int r = __builtin_popcount(m & 0x3FFu);
        int c = __builtin_popcount((m >> 10) & 0x3FFu);
        if (r != c || r < 2 || r > 5 || vis[m]) continue;
        int is_sub = 0;
        int cmax = (r == 5) ? 2 : 1;
        for (int s = 0; s < 9; s++)
            for (int rt = 0; rt < 2; rt++)
                for (int cp = 0; cp < cmax; cp++) {
                    uint32_t nm = apply_z9(m, s, rt, cp);
                    vis[nm] = 1;
                    if (nm == m && cp == 1) is_sub = 1;
                }
        int rows[5], cols[5], ri = 0, ci = 0;
        for (int i = 0; i < 10; i++) {
            if ((m >> i) & 1) rows[ri++] = i;
            if ((m >> (i + 10)) & 1) cols[ci++] = i;
        }
        if (r == 2) {
            int p = pair_id[rows[0]][rows[1]];
            int c0 = pair_id[cols[0]][cols[1]];
            int s = pair_canon_s[p];
            OrbitRep2 rep = { (uint8_t)pair_canon_idx[p], (uint8_t)pair_shift[c0][s] };
            ext_r2[n_ext_r2++] = rep;
        } else if (r == 3) {
            int t = triple_id[rows[0]][rows[1]][rows[2]];
            int c0 = triple_id[cols[0]][cols[1]][cols[2]];
            int s = triple_canon_s[t];
            OrbitRep3 rep = { (uint8_t)triple_canon_idx[t], (uint8_t)triple_shift[c0][s] };
            ext_r3[n_ext_r3++] = rep;
        } else if (r == 4) {
            int q = quad_id[rows[0]][rows[1]][rows[2]][rows[3]];
            int c0 = quad_id[cols[0]][cols[1]][cols[2]][cols[3]];
            int s = quad_canon_s[q];
            OrbitRep4 rep = { (uint8_t)quad_canon_idx[q], (uint8_t)quad_shift[c0][s] };
            ext_r4[n_ext_r4++] = rep;
        } else if (r == 5) {
            int rq = quad_id[rows[0]][rows[1]][rows[2]][rows[3]];
            int s = quad_canon_s[rq];
            OrbitRep5 rep;
            rep.r_last = (uint8_t)s9_idx(rows[4], s);
            rep.r_qcid = (uint8_t)quad_canon_idx[rq];
            for (int idx = 0; idx < 5; idx++) {
                rep.col_x[idx] = (uint8_t)s9_idx(cols[idx], s);
                int sub4[4], k = 0;
                for (int j = 0; j < 5; j++) if (j != idx) sub4[k++] = cols[j];
                int cq = quad_id[sub4[0]][sub4[1]][sub4[2]][sub4[3]];
                rep.col_q_shifted[idx] = (uint8_t)quad_shift[cq][s];
                rep.flip_total[idx] = (uint8_t)((idx & 1) ^ quad_canon_flip[rq] ^ quad_flip[cq][s]);
            }
            if (is_sub) sub_r5[n_sub_r5++] = rep;
            else        ext_r5[n_ext_r5++] = rep;
        }
    }
    printf("Orbits built: r2=%d, r3=%d, r4=%d, r5_sub=%d, r5_ext=%d (total r2..5=%d)\n",
           n_ext_r2, n_ext_r3, n_ext_r4, n_sub_r5, n_ext_r5,
           n_ext_r2 + n_ext_r3 + n_ext_r4 + n_sub_r5 + n_ext_r5);
    free(vis);
}

/* Precomputed Plücker step tables for r=3 (14 x 120) and r=4 (24 x 210) */
static uint8_t t3_r_last[14], t3_r_pcid[14], t3_r_s[14], t3_r_flip[14];
static uint8_t t3_col_x[120][3], t3_col_p[120][3];

static uint8_t q4_r_last[24], q4_r_tcid[24], q4_r_s[24], q4_r_flip[24];
static uint8_t q4_col_x[210][4], q4_col_t[210][4];

static void init_plucker_tables(void) {
    for (int cid = 0; cid < 14; cid++) {
        int t = canon_triples[cid];
        int rp = pair_id[triples[t][0]][triples[t][1]];
        t3_r_last[cid] = triples[t][2];
        t3_r_pcid[cid] = (uint8_t)pair_canon_idx[rp];
        t3_r_s[cid]    = (uint8_t)pair_canon_s[rp];
        t3_r_flip[cid] = pair_canon_flip[rp];
    }
    for (int ct = 0; ct < 120; ct++) {
        int c0 = triples[ct][0], c1 = triples[ct][1], c2 = triples[ct][2];
        t3_col_x[ct][0] = c0; t3_col_p[ct][0] = (uint8_t)pair_id[c1][c2];
        t3_col_x[ct][1] = c1; t3_col_p[ct][1] = (uint8_t)pair_id[c0][c2];
        t3_col_x[ct][2] = c2; t3_col_p[ct][2] = (uint8_t)pair_id[c0][c1];
    }

    for (int cid = 0; cid < 24; cid++) {
        int q = canon_quads[cid];
        int rt = triple_id[quads[q][0]][quads[q][1]][quads[q][2]];
        q4_r_last[cid] = quads[q][3];
        q4_r_tcid[cid] = (uint8_t)triple_canon_idx[rt];
        q4_r_s[cid]    = (uint8_t)triple_canon_s[rt];
        q4_r_flip[cid] = triple_canon_flip[rt];
    }
    for (int cq = 0; cq < 210; cq++) {
        int c0 = quads[cq][0], c1 = quads[cq][1], c2 = quads[cq][2], c3 = quads[cq][3];
        q4_col_x[cq][0] = c0; q4_col_t[cq][0] = (uint8_t)triple_id[c1][c2][c3];
        q4_col_x[cq][1] = c1; q4_col_t[cq][1] = (uint8_t)triple_id[c0][c2][c3];
        q4_col_x[cq][2] = c2; q4_col_t[cq][2] = (uint8_t)triple_id[c0][c1][c3];
        q4_col_x[cq][3] = c3; q4_col_t[cq][3] = (uint8_t)triple_id[c0][c1][c2];
    }
}

static inline void build_U_from_params(uint8_t beta, uint8_t u_inf, uint8_t lam3, uint8_t lam6, int idx1, int idx2, uint8_t c[9], uint8_t U[10][10]) {
    uint8_t lam0 = conj_tab[u_inf];
    uint8_t u0[3];
    u0[0] = mul_tab[5][add_tab[lam0][add_tab[lam3][lam6]]];
    u0[1] = mul_tab[5][add_tab[lam0][add_tab[mul_tab[W3_2][lam3]][mul_tab[W3][lam6]]]];
    u0[2] = mul_tab[5][add_tab[lam0][add_tab[mul_tab[W3][lam3]][mul_tab[W3_2][lam6]]]];

    const uint8_t *a = z1_tab[idx1];
    const uint8_t *b = z2_tab[idx2];
    uint8_t w_pow1[3] = {1, W3_2, W3};
    uint8_t w_pow2[3] = {1, W3, W3_2};

    for (int r = 0; r < 3; r++) {
        uint8_t ar4 = mul_tab[4][a[r]];
        uint8_t br4 = mul_tab[4][b[r]];
        for (int q = 0; q < 3; q++) {
            uint8_t term1 = mul_tab[ar4][w_pow1[q]];
            uint8_t term2 = mul_tab[br4][w_pow2[q]];
            c[r + 3 * q] = add_tab[u0[r]][add_tab[term1][term2]];
        }
    }
    uint8_t m_cbeta = neg_tab[conj_tab[beta]];
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) U[i][j] = c[(j - i + 9) % 9];
        U[i][9] = beta;
        U[9][i] = m_cbeta;
    }
    U[9][9] = u_inf;
}

static void eval_full(const uint8_t c[9], uint8_t beta, uint8_t u_inf, const uint8_t U[10][10],
                      int *out_sub, int *out_ext, int sub_cutoff, int tot_cutoff) {
    int ext_bad = 0;
    for (int d = 0; d < 9; d++) if (c[d] == 0) ext_bad++;
    if (beta == 0) ext_bad++;
    if (u_inf == 0) ext_bad++;

    uint8_t M2[5][45];
    for (int cid = 0; cid < 5; cid++) {
        int rp = canon_pairs[cid];
        int r0 = pairs[rp][0], r1 = pairs[rp][1];
        const uint8_t *U_r0 = U[r0], *U_r1 = U[r1];
        for (int cp = 0; cp < 45; cp++) {
            int c0 = pairs[cp][0], c1 = pairs[cp][1];
            M2[cid][cp] = sub_tab[mul_tab[U_r0[c0]][U_r1[c1]]][mul_tab[U_r0[c1]][U_r1[c0]]];
        }
    }
    for (int i = 0; i < n_ext_r2; i++)
        if (M2[ext_r2[i].r_cid][ext_r2[i].c_id] == 0) ext_bad++;

    uint8_t M3[14][120];
    for (int cid = 0; cid < 14; cid++) {
        int r2 = t3_r_last[cid];
        int rpcid = t3_r_pcid[cid];
        int s = t3_r_s[cid];
        int rfl = t3_r_flip[cid];
        const uint8_t *U_r2 = U[r2];
        const uint8_t *M2_row = M2[rpcid];
        for (int ct = 0; ct < 120; ct++) {
            int p0 = pair_shift[t3_col_p[ct][0]][s];
            int p1 = pair_shift[t3_col_p[ct][1]][s];
            int p2 = pair_shift[t3_col_p[ct][2]][s];
            uint8_t m0 = M2_row[p0]; if (rfl ^ pair_flip[t3_col_p[ct][0]][s]) m0 = neg_tab[m0];
            uint8_t m1 = M2_row[p1]; if (rfl ^ pair_flip[t3_col_p[ct][1]][s]) m1 = neg_tab[m1];
            uint8_t m2 = M2_row[p2]; if (rfl ^ pair_flip[t3_col_p[ct][2]][s]) m2 = neg_tab[m2];
            uint8_t v0 = mul_tab[U_r2[t3_col_x[ct][0]]][m0];
            uint8_t v1 = mul_tab[U_r2[t3_col_x[ct][1]]][m1];
            uint8_t v2 = mul_tab[U_r2[t3_col_x[ct][2]]][m2];
            M3[cid][ct] = add_tab[sub_tab[v0][v1]][v2];
        }
    }
    for (int i = 0; i < n_ext_r3; i++)
        if (M3[ext_r3[i].r_cid][ext_r3[i].c_id] == 0) ext_bad++;

    uint8_t M4[24][210];
    for (int cid = 0; cid < 24; cid++) {
        int r3 = q4_r_last[cid];
        int rtcid = q4_r_tcid[cid];
        int s = q4_r_s[cid];
        int rfl = q4_r_flip[cid];
        const uint8_t *U_r3 = U[r3];
        const uint8_t *M3_row = M3[rtcid];
        for (int cq = 0; cq < 210; cq++) {
            int t0 = triple_shift[q4_col_t[cq][0]][s];
            int t1 = triple_shift[q4_col_t[cq][1]][s];
            int t2 = triple_shift[q4_col_t[cq][2]][s];
            int t3 = triple_shift[q4_col_t[cq][3]][s];
            uint8_t m0 = M3_row[t0]; if (rfl ^ triple_flip[q4_col_t[cq][0]][s]) m0 = neg_tab[m0];
            uint8_t m1 = M3_row[t1]; if (rfl ^ triple_flip[q4_col_t[cq][1]][s]) m1 = neg_tab[m1];
            uint8_t m2 = M3_row[t2]; if (rfl ^ triple_flip[q4_col_t[cq][2]][s]) m2 = neg_tab[m2];
            uint8_t m3 = M3_row[t3]; if (rfl ^ triple_flip[q4_col_t[cq][3]][s]) m3 = neg_tab[m3];
            uint8_t v0 = mul_tab[U_r3[q4_col_x[cq][0]]][m0];
            uint8_t v1 = mul_tab[U_r3[q4_col_x[cq][1]]][m1];
            uint8_t v2 = mul_tab[U_r3[q4_col_x[cq][2]]][m2];
            uint8_t v3 = mul_tab[U_r3[q4_col_x[cq][3]]][m3];
            M4[cid][cq] = sub_tab[add_tab[sub_tab[v3][v2]][v1]][v0];
        }
    }
    for (int i = 0; i < n_ext_r4; i++)
        if (M4[ext_r4[i].r_cid][ext_r4[i].c_id] == 0) ext_bad++;

    int sub_bad = 0;
    for (int i = 0; i < n_sub_r5; i++) {
        const OrbitRep5 *rep = &sub_r5[i];
        const uint8_t *U_r = U[rep->r_last];
        const uint8_t *M4_row = M4[rep->r_qcid];
        uint8_t s = 0;
        for (int idx = 0; idx < 5; idx++) {
            uint8_t m = M4_row[rep->col_q_shifted[idx]];
            if (rep->flip_total[idx]) m = neg_tab[m];
            s = add_tab[s][mul_tab[U_r[rep->col_x[idx]]][m]];
        }
        if (s == 0) {
            sub_bad++;
            if (sub_bad > sub_cutoff && (sub_bad + ext_bad) > tot_cutoff) {
                *out_sub = sub_bad; *out_ext = ext_bad; return;
            }
        }
    }

    if (sub_bad + ext_bad <= tot_cutoff || sub_bad <= sub_cutoff) {
        for (int i = 0; i < n_ext_r5; i++) {
            const OrbitRep5 *rep = &ext_r5[i];
            const uint8_t *U_r = U[rep->r_last];
            const uint8_t *M4_row = M4[rep->r_qcid];
            uint8_t s = 0;
            for (int idx = 0; idx < 5; idx++) {
                uint8_t m = M4_row[rep->col_q_shifted[idx]];
                if (rep->flip_total[idx]) m = neg_tab[m];
                s = add_tab[s][mul_tab[U_r[rep->col_x[idx]]][m]];
            }
            if (s == 0) {
                ext_bad++;
                if (sub_bad > sub_cutoff && (sub_bad + ext_bad) > tot_cutoff) break;
            }
        }
    }
    *out_sub = sub_bad;
    *out_ext = ext_bad;
}

/* Global search state */
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static int g_best_sub = 999999, g_best_sub_tot = 999999;
static int g_best_tot = 999999, g_best_tot_sub = 999999;
static int g_sub0_cnt = 0, g_sub1_cnt = 0;
static uint64_t g_evals = 0;

/* Canonical apex pairs (beta, u_inf): 9 norms w_beta in {1,2,3,4,6,7,8,9,10} x 12 phases of u_inf = 108 */
static uint8_t apex_beta[108], apex_uinf[108];
static int n_apex = 0;

static void init_apex(void) {
    for (int wb = 1; wb < 11; wb++) {
        if (wb == 5) continue; /* 1 + 2*5 = 0 mod 11 */
        uint8_t beta = 0;
        for (int a = 1; a < 121; a++) if (mul_tab[a][conj_tab[a]] == wb) { beta = (uint8_t)a; break; }
        int wu = (1 + 2 * wb) % 11;
        for (int a = 1; a < 121; a++) {
            if (mul_tab[a][conj_tab[a]] == wu) {
                apex_beta[n_apex] = beta;
                apex_uinf[n_apex] = (uint8_t)a;
                n_apex++;
            }
        }
    }
    printf("Initialized %d apex (beta, u_inf) pairs.\n", n_apex);
}

#define NTHREADS 8

static void *worker(void *arg) {
    int tid = *(int *)arg;
    uint64_t rng = 0x9E3779B97F4A7C15ULL ^ ((uint64_t)(tid + 1) * 0xBF58476D1CE4E5B9ULL);
    uint8_t c[9], U[10][10];

    /* Phase 1: Structured sweep over z1_idx and z2_idx with multi-start coordinate polish */
    for (int iter = 0; iter < 3500; iter++) {
        rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
        int ap = (int)((rng * 0x2545F4914F6CDD1DULL >> 32) % n_apex);
        rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
        int l3 = (int)((rng * 0x2545F4914F6CDD1DULL >> 32) % 12);
        rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
        int l6 = (int)((rng * 0x2545F4914F6CDD1DULL >> 32) % 12);
        rng ^= rng >> 12; rng ^= rng << 25; rng ^= rng >> 27;
        int idx1 = (int)((rng * 0x2545F4914F6CDD1DULL >> 32) % 1332);

        /* Sweep all 1332 values of idx2 for this (ap, l3, l6, idx1)! */
        int best_idx2 = 0, best_score = 999999;
        for (int idx2 = 0; idx2 < 1332; idx2++) {
            build_U_from_params(apex_beta[ap], apex_uinf[ap], u1_tab[l3], u1_tab[l6], idx1, idx2, c, U);
            /* Fast r1 check */
            if (!c[0]||!c[1]||!c[2]||!c[3]||!c[4]||!c[5]||!c[6]||!c[7]||!c[8]) continue;
            int sb, eb;
            eval_full(c, apex_beta[ap], apex_uinf[ap], U, &sb, &eb, 2, g_best_tot + 8);
            int tot = sb + eb;
            int sc = sb * 12 + eb;
            if (sc < best_score) { best_score = sc; best_idx2 = idx2; }
            if (sb <= 1 || tot < g_best_tot) {
                pthread_mutex_lock(&lock);
                if (sb == 0) g_sub0_cnt++;
                if (sb == 1) g_sub1_cnt++;
                if (sb < g_best_sub || (sb == g_best_sub && tot < g_best_sub_tot)) {
                    g_best_sub = sb; g_best_sub_tot = tot;
                    printf("  [T%d] NEW BEST SUB: sub=%d/126, ext=%d/5327, tot=%d/5453 (ap=%d, l3=%d, l6=%d, z1=%d, z2=%d)\n",
                           tid, sb, eb, tot, ap, l3, l6, idx1, idx2);
                    fflush(stdout);
                }
                if (tot < g_best_tot) {
                    g_best_tot = tot; g_best_tot_sub = sb;
                    printf("  [T%d] NEW BEST TOT: tot=%d/5453 (sub=%d/126, ext=%d/5327) (ap=%d, l3=%d, l6=%d, z1=%d, z2=%d) | c=[%d,%d,%d,%d,%d,%d,%d,%d,%d] beta=%d uinf=%d\n",
                           tid, tot, sb, eb, ap, l3, l6, idx1, idx2,
                           c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8], apex_beta[ap], apex_uinf[ap]);
                    fflush(stdout);
                }
                pthread_mutex_unlock(&lock);
            }
        }
        /* Coordinate polish on idx1 (1332) and (ap, l3, l6) around best_idx2 */
        int cur_idx2 = best_idx2;
        int best_idx1 = idx1;
        for (int i1 = 0; i1 < 1332; i1++) {
            build_U_from_params(apex_beta[ap], apex_uinf[ap], u1_tab[l3], u1_tab[l6], i1, cur_idx2, c, U);
            if (!c[0]||!c[1]||!c[2]||!c[3]||!c[4]||!c[5]||!c[6]||!c[7]||!c[8]) continue;
            int sb, eb;
            eval_full(c, apex_beta[ap], apex_uinf[ap], U, &sb, &eb, 2, g_best_tot + 8);
            int tot = sb + eb;
            int sc = sb * 12 + eb;
            if (sc < best_score) { best_score = sc; best_idx1 = i1; }
            if (sb <= 1 || tot < g_best_tot) {
                pthread_mutex_lock(&lock);
                if (sb == 0) g_sub0_cnt++;
                if (sb == 1) g_sub1_cnt++;
                if (sb < g_best_sub || (sb == g_best_sub && tot < g_best_sub_tot)) {
                    g_best_sub = sb; g_best_sub_tot = tot;
                    printf("  [T%d] NEW BEST SUB: sub=%d/126, ext=%d/5327, tot=%d/5453 (ap=%d, l3=%d, l6=%d, z1=%d, z2=%d)\n",
                           tid, sb, eb, tot, ap, l3, l6, i1, cur_idx2);
                    fflush(stdout);
                }
                if (tot < g_best_tot) {
                    g_best_tot = tot; g_best_tot_sub = sb;
                    printf("  [T%d] NEW BEST TOT: tot=%d/5453 (sub=%d/126, ext=%d/5327) (ap=%d, l3=%d, l6=%d, z1=%d, z2=%d) | c=[%d,%d,%d,%d,%d,%d,%d,%d,%d] beta=%d uinf=%d\n",
                           tid, tot, sb, eb, ap, l3, l6, i1, cur_idx2,
                           c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8], apex_beta[ap], apex_uinf[ap]);
                    fflush(stdout);
                }
                pthread_mutex_unlock(&lock);
            }
        }
        pthread_mutex_lock(&lock);
        g_evals += 2664;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    init_gf121();
    init_combinatorics();
    build_orbits();
    init_plucker_tables();
    init_apex();

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    pthread_t th[NTHREADS];
    int tids[NTHREADS];
    for (int i = 0; i < NTHREADS; i++) {
        tids[i] = i;
        pthread_create(&th[i], NULL, worker, &tids[i]);
    }
    for (int i = 0; i < NTHREADS; i++) pthread_join(th[i], NULL);

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double el = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) * 1e-9;
    printf("\n=== D35 APEX-BORDERED Z_9 UNITARY SUMMARY (%.2f s, %llu evals) ===\n", el, (unsigned long long)g_evals);
    printf("  sub=0/126 hits: %d | sub=1/126 hits: %d\n", g_sub0_cnt, g_sub1_cnt);
    printf("  Global best sub: %d / 126 (tot=%d / 5453)\n", g_best_sub, g_best_sub_tot);
    printf("  Global best tot: %d / 5453 (sub=%d / 126, %.4f%% non-zero)\n",
           g_best_tot, g_best_tot_sub, 100.0 * (5453.0 - g_best_tot) / 5453.0);
    return 0;
}
