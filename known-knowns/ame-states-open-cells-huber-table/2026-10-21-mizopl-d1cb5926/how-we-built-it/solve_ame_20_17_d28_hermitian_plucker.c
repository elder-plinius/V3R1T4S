#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

/*
 * Theorem D22 + D23 + D23b Turbo Solver:
 *   1. Precomputes ALL 1,419,857 (17 x 289 x 289) unitary circulants K in K_TAB (14.2 MB)
 *      in parallel at startup -> O(1) dressing lookup (ZERO inv_circ5 in K-sweeps!).
 *   2. Uses U_22 = U_11^dagger directly (u22[d] = conj_tab[u11[(5-d)%5]]) -> halves convolutions!
 *   3. Theorem D23b Adjugate-Dual Pure-Block Sieve on u12_0 (checks 1x1, 2x2 of u12_0 AND
 *      1x1, 2x2 of u12_0^{-1}, guaranteeing ALL 251 minors of U_12 and U_21 across r=1..5 are non-zero!).
 *   4. Stage-0 (r=1,2) Zero-Tolerance Gate BEFORE D2[45][45] + Stage-1 D2-Only Gate BEFORE D3[120][120].
 */

static const int P = 17;
static const int Q2 = 289;
static const int NONRES = 3;

static uint16_t mul_tab[289][289], add_tab[289][289], sub_tab[289][289], neg_tab[289], inv_tab[289], conj_tab[289];
static int skew_elems[17], herm_elems[17];
static int modp(int x) { x %= P; return x < 0 ? x + P : x; }

static void init_gf289(void) {
    for (int a = 0; a < Q2; a++) {
        int a0 = a % P, a1 = a / P;
        conj_tab[a] = a0 + modp(-a1) * P;
        neg_tab[a] = modp(-a0) + modp(-a1) * P;
        for (int b = 0; b < Q2; b++) {
            int b0 = b % P, b1 = b / P;
            add_tab[a][b] = modp(a0 + b0) + modp(a1 + b1) * P;
            sub_tab[a][b] = modp(a0 - b0) + modp(a1 - b1) * P;
            int c0 = modp(a0 * b0 + NONRES * a1 * b1);
            int c1 = modp(a0 * b1 + a1 * b0);
            mul_tab[a][b] = c0 + c1 * P;
        }
    }
    inv_tab[0] = 0;
    for (int a = 1; a < Q2; a++)
        for (int b = 1; b < Q2; b++)
            if (mul_tab[a][b] == 1) { inv_tab[a] = b; break; }
    int ns = 0, nh = 0;
    for (int a = 0; a < Q2; a++) {
        if (add_tab[a][conj_tab[a]] == 0) skew_elems[ns++] = a;
        if (conj_tab[a] == a) herm_elems[nh++] = a;
    }
}

static int pair_id[10][10];
static uint8_t pairs[45][2];
static int pair_shift[45][5];
static uint8_t pair_flip[45][5];

static int triple_id[10][10][10];
static uint8_t triples[120][3];
static int triple_shift[120][5];
static uint8_t triple_flip[120][5];

static int s_idx(int x, int s) {
    return (x < 5) ? ((x + s) % 5) : (5 + ((x - 5 + s) % 5));
}

static void init_combinatorics(void) {
    int pid = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++) {
            pair_id[i][j] = pid;
            pairs[pid][0] = i;
            pairs[pid][1] = j;
            pid++;
        }
    for (int p = 0; p < 45; p++) {
        for (int s = 0; s < 5; s++) {
            int a = s_idx(pairs[p][0], s);
            int b = s_idx(pairs[p][1], s);
            if (a < b) { pair_shift[p][s] = pair_id[a][b]; pair_flip[p][s] = 0; }
            else       { pair_shift[p][s] = pair_id[b][a]; pair_flip[p][s] = 1; }
        }
    }

    int tid = 0;
    for (int i = 0; i < 10; i++)
        for (int j = i + 1; j < 10; j++)
            for (int k = j + 1; k < 10; k++) {
                triple_id[i][j][k] = tid;
                triples[tid][0] = i;
                triples[tid][1] = j;
                triples[tid][2] = k;
                tid++;
            }
    for (int t = 0; t < 120; t++) {
        for (int s = 0; s < 5; s++) {
            int a = s_idx(triples[t][0], s);
            int b = s_idx(triples[t][1], s);
            int c = s_idx(triples[t][2], s);
            int flip = 0, tmp;
            if (a > b) { tmp = a; a = b; b = tmp; flip ^= 1; }
            if (b > c) { tmp = b; b = c; c = tmp; flip ^= 1; }
            if (a > b) { tmp = a; a = b; b = tmp; flip ^= 1; }
            triple_shift[t][s] = triple_id[a][b][c];
            triple_flip[t][s] = flip;
        }
    }
}

static uint32_t apply_g20(uint32_t m, int s, int w, int r_tr) {
    uint32_t out = 0;
    for (int i = 0; i < 5; i++) {
        int r0 = (m >> i) & 1, r1 = (m >> (i + 5)) & 1;
        int c0 = (m >> (i + 10)) & 1, c1 = (m >> (i + 15)) & 1;
        int nr0 = r0, nr1 = r1, nc0 = c0, nc1 = c1;
        int idx = i;
        if (w) {
            idx = 4 - idx;
            int t = nr0; nr0 = nr1; nr1 = t;
            t = nc0; nc0 = nc1; nc1 = t;
        }
        if (r_tr) {
            idx = 4 - idx;
            int t = nr0; nr0 = nc0; nc0 = t;
            t = nr1; nr1 = nc1; nc1 = t;
        }
        int ni = (idx + s + 5) % 5;
        if (nr0) out |= (1u << ni);
        if (nr1) out |= (1u << (ni + 5));
        if (nc0) out |= (1u << (ni + 10));
        if (nc1) out |= (1u << (ni + 15));
    }
    return out;
}

static uint32_t canon_g20(uint32_t m) {
    uint32_t best = m;
    for (int s = 0; s < 5; s++)
        for (int w = 0; w < 2; w++)
            for (int r = 0; r < 2; r++) {
                uint32_t g = apply_g20(m, s, w, r);
                if (g < best) best = g;
            }
    return best;
}

static uint32_t canon_g40_r5(uint32_t m) {
    uint32_t c1 = canon_g20(m);
    uint32_t c2 = canon_g20((~m) & 0xFFFFFu);
    return (c1 < c2) ? c1 : c2;
}

typedef struct { uint8_t r0, c0; } Orb1;
typedef struct { uint8_t rp, cp, r0, r1, c0, c1; } Orb2;
typedef struct { uint8_t r0, rp_bot, c0, c1, c2, cp12, cp02, cp01; } Orb3;
typedef struct { uint8_t rp_top, rp_bot, cp_top[6], cp_bot[6]; } Orb4;
typedef struct {
    uint8_t rp_top, rt_bot;
    uint8_t cp_top[10], ct_bot[10];
    uint8_t r2, rp34;
    uint8_t c_a[10], c_b[10], c_c[10];
    uint8_t cp_bc[10], cp_ac[10], cp_ab[10];
} Orb5;

static Orb1 orbs1_sub[32],   orbs1_ext[32];   static int n_orbs1_sub = 0, n_orbs1_ext = 0;
static Orb2 orbs2_sub[128],  orbs2_ext[256];  static int n_orbs2_sub = 0, n_orbs2_ext = 0;
static Orb3 orbs3_sub[256],  orbs3_ext[1024]; static int n_orbs3_sub = 0, n_orbs3_ext = 0;
static Orb4 orbs4_sub[256],  orbs4_ext[2500]; static int n_orbs4_sub = 0, n_orbs4_ext = 0;
static Orb5 orbs5_sub[512],  orbs5_ext[2000]; static int n_orbs5_sub = 0, n_orbs5_ext = 0;

typedef struct { uint8_t rp, cp; } Pair2;
static Pair2 z5_pairs[405]; static int n_z5_pairs = 0;
static uint8_t seen_p2[45][45];

typedef struct { uint8_t rt, ct, r0, rp_bot, c0, c1, c2, cp12, cp02, cp01; } Triple3;
static Triple3 z5_triples[2880]; static int n_z5_triples = 0;
static uint8_t seen_t3[120][120];

static const int comb52_a[10]  = {0, 0, 0, 0, 1, 1, 1, 2, 2, 3};
static const int comb52_b[10]  = {1, 2, 3, 4, 2, 3, 4, 3, 4, 4};
static const int comb52_c0[10] = {2, 1, 1, 1, 0, 0, 0, 0, 0, 0};
static const int comb52_c1[10] = {3, 3, 2, 2, 3, 2, 2, 1, 1, 1};
static const int comb52_c2[10] = {4, 4, 4, 3, 4, 4, 3, 4, 3, 2};

static const int comb42_a[6] = {0, 0, 0, 1, 1, 2};
static const int comb42_b[6] = {1, 2, 3, 2, 3, 3};
static const int comb42_c[6] = {2, 1, 1, 0, 0, 0};
static const int comb42_d[6] = {3, 3, 2, 3, 2, 1};

static void build_all_tables(void) {
    for (int p1 = 0; p1 < 45; p1++) {
        for (int p2 = 0; p2 < 45; p2++) {
            if (seen_p2[p1][p2]) continue;
            z5_pairs[n_z5_pairs].rp = p1;
            z5_pairs[n_z5_pairs].cp = p2;
            n_z5_pairs++;
            for (int s = 0; s < 5; s++)
                seen_p2[pair_shift[p1][s]][pair_shift[p2][s]] = 1;
        }
    }
    for (int t1 = 0; t1 < 120; t1++) {
        for (int t2 = 0; t2 < 120; t2++) {
            if (seen_t3[t1][t2]) continue;
            Triple3 *tr = &z5_triples[n_z5_triples++];
            tr->rt = t1; tr->ct = t2;
            tr->r0 = triples[t1][0];
            tr->rp_bot = pair_id[triples[t1][1]][triples[t1][2]];
            tr->c0 = triples[t2][0]; tr->c1 = triples[t2][1]; tr->c2 = triples[t2][2];
            tr->cp12 = pair_id[tr->c1][tr->c2];
            tr->cp02 = pair_id[tr->c0][tr->c2];
            tr->cp01 = pair_id[tr->c0][tr->c1];
            for (int s = 0; s < 5; s++)
                seen_t3[triple_shift[t1][s]][triple_shift[t2][s]] = 1;
        }
    }

    for (int r = 1; r <= 5; r++) {
        for (uint32_t rm = 1; rm < 1024; rm++) {
            if (__builtin_popcount(rm) != r) continue;
            for (uint32_t cm = 1; cm < 1024; cm++) {
                if (__builtin_popcount(cm) != r) continue;
                uint32_t m = rm | (cm << 10);
                if (r < 5) {
                    if (canon_g20(m) != m) continue;
                } else {
                    if (canon_g40_r5(m) != m) continue;
                }
                uint8_t rw[5], cl[5];
                int ri = 0, ci = 0;
                for (int i = 0; i < 10; i++) {
                    if ((rm >> i) & 1) rw[ri++] = i;
                    if ((cm >> i) & 1) cl[ci++] = i;
                }
                uint32_t m_comp = (~m) & 0xFFFFFu;
                int is_sub = 0;
                for (int s = 0; s < 5; s++) {
                    if (apply_g20(m, s, 1, 0) == m || apply_g20(m, s, 1, 1) == m) { is_sub = 1; break; }
                    if (r == 5 && apply_g20(m, s, 0, 1) == m_comp) { is_sub = 1; break; }
                }

                if (r == 1) {
                    Orb1 *o = is_sub ? &orbs1_sub[n_orbs1_sub++] : &orbs1_ext[n_orbs1_ext++];
                    o->r0 = rw[0]; o->c0 = cl[0];
                } else if (r == 2) {
                    Orb2 *o = is_sub ? &orbs2_sub[n_orbs2_sub++] : &orbs2_ext[n_orbs2_ext++];
                    o->r0 = rw[0]; o->r1 = rw[1]; o->c0 = cl[0]; o->c1 = cl[1];
                    o->rp = pair_id[rw[0]][rw[1]]; o->cp = pair_id[cl[0]][cl[1]];
                } else if (r == 3) {
                    Orb3 *o = is_sub ? &orbs3_sub[n_orbs3_sub++] : &orbs3_ext[n_orbs3_ext++];
                    o->r0 = rw[0]; o->rp_bot = pair_id[rw[1]][rw[2]];
                    o->c0 = cl[0]; o->c1 = cl[1]; o->c2 = cl[2];
                    o->cp12 = pair_id[cl[1]][cl[2]];
                    o->cp02 = pair_id[cl[0]][cl[2]];
                    o->cp01 = pair_id[cl[0]][cl[1]];
                } else if (r == 4) {
                    Orb4 *o = is_sub ? &orbs4_sub[n_orbs4_sub++] : &orbs4_ext[n_orbs4_ext++];
                    o->rp_top = pair_id[rw[0]][rw[1]];
                    o->rp_bot = pair_id[rw[2]][rw[3]];
                    for (int k = 0; k < 6; k++) {
                        o->cp_top[k] = pair_id[cl[comb42_a[k]]][cl[comb42_b[k]]];
                        o->cp_bot[k] = pair_id[cl[comb42_c[k]]][cl[comb42_d[k]]];
                    }
                } else if (r == 5) {
                    Orb5 *o = is_sub ? &orbs5_sub[n_orbs5_sub++] : &orbs5_ext[n_orbs5_ext++];
                    o->rp_top = pair_id[rw[0]][rw[1]];
                    o->rt_bot = triple_id[rw[2]][rw[3]][rw[4]];
                    o->r2     = rw[2];
                    o->rp34   = pair_id[rw[3]][rw[4]];
                    for (int k = 0; k < 10; k++) {
                        o->cp_top[k] = pair_id[cl[comb52_a[k]]][cl[comb52_b[k]]];
                        int ca = cl[comb52_c0[k]], cb = cl[comb52_c1[k]], cc = cl[comb52_c2[k]];
                        o->ct_bot[k] = triple_id[ca][cb][cc];
                        o->c_a[k] = ca; o->c_b[k] = cb; o->c_c[k] = cc;
                        o->cp_bc[k] = pair_id[cb][cc];
                        o->cp_ac[k] = pair_id[ca][cc];
                        o->cp_ab[k] = pair_id[ca][cb];
                    }
                }
            }
        }
    }
}

static inline void conv5(const uint16_t x[5], const uint16_t y[5], uint16_t out[5]) {
    for (int k = 0; k < 5; k++) {
        uint16_t s = 0;
        for (int i = 0; i < 5; i++)
            s = add_tab[s][mul_tab[x[i]][y[(k - i + 5) % 5]]];
        out[k] = s;
    }
}

static int inv_circ5(const uint16_t del[5], uint16_t inv_del[5]) {
    uint16_t aug[5][6];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) aug[i][j] = del[(i - j + 5) % 5];
        aug[i][5] = (i == 0) ? 1 : 0;
    }
    for (int col = 0; col < 5; col++) {
        int piv = -1;
        for (int row = col; row < 5; row++) if (aug[row][col] != 0) { piv = row; break; }
        if (piv < 0) return 0;
        if (piv != col) for (int c = col; c <= 5; c++) { uint16_t t = aug[col][c]; aug[col][c] = aug[piv][c]; aug[piv][c] = t; }
        uint16_t inv_p = inv_tab[aug[col][col]];
        for (int c = col; c <= 5; c++) aug[col][c] = mul_tab[aug[col][c]][inv_p];
        for (int row = 0; row < 5; row++) {
            if (row == col) continue;
            uint16_t f = aug[row][col];
            if (!f) continue;
            for (int c = col; c <= 5; c++) aug[row][c] = sub_tab[aug[row][c]][mul_tab[f][aug[col][c]]];
        }
    }
    for (int i = 0; i < 5; i++) inv_del[i] = aug[i][5];
    return 1;
}

/* Precomputed table of ALL 17 x 289 x 289 = 1,419,857 unitary circulants K */
#define N_KTOT (17 * 289 * 289)
static uint16_t (*K_TAB)[5] = NULL;
static uint8_t *K_VALID = NULL;

static void *init_ktab_worker(void *arg) {
    int tid = (int)(uintptr_t)arg;
    for (int s7 = tid; s7 < 17; s7 += 8) {
        for (int s8 = 0; s8 < 289; s8++) {
            for (int s9 = 0; s9 < 289; s9++) {
                int idx = (s7 * 289 + s8) * 289 + s9;
                if (s7 == 0 && s8 == 0 && s9 == 0) {
                    K_TAB[idx][0] = 1; K_TAB[idx][1] = 0; K_TAB[idx][2] = 0; K_TAB[idx][3] = 0; K_TAB[idx][4] = 0;
                    K_VALID[idx] = 1;
                    continue;
                }
                uint16_t ck[5], p1[5], m1[5], inv_p1[5];
                ck[0] = skew_elems[s7];
                ck[1] = s8; ck[4] = neg_tab[conj_tab[ck[1]]];
                ck[2] = s9; ck[3] = neg_tab[conj_tab[ck[2]]];
                for (int k = 0; k < 5; k++) {
                    p1[k] = (k == 0) ? add_tab[1][ck[0]] : ck[k];
                    m1[k] = (k == 0) ? sub_tab[1][ck[0]] : neg_tab[ck[k]];
                }
                if (!inv_circ5(p1, inv_p1)) {
                    K_VALID[idx] = 0;
                } else {
                    conv5(m1, inv_p1, K_TAB[idx]);
                    K_VALID[idx] = 1;
                }
            }
        }
    }
    return NULL;
}

static inline int check_circ5_r12_nonzero(const uint16_t x[5]) {
    if (!x[0] || !x[1] || !x[2] || !x[3] || !x[4]) return 0;
    for (int dr = 1; dr <= 2; dr++) {
        for (int dc = 1; dc <= 2; dc++) {
            for (int j = 0; j < 5; j++) {
                int c0 = j, c1 = (j + dc) % 5;
                uint16_t a00 = x[c0], a01 = x[c1];
                uint16_t a10 = x[(c0 - dr + 5) % 5], a11 = x[(c1 - dr + 5) % 5];
                if (sub_tab[mul_tab[a00][a11]][mul_tab[a01][a10]] == 0) return 0;
            }
        }
    }
    return 1;
}

/* Theorem D23b: Full r=1..5 pure-block sieve on u12_0 via adjugate duality */
static int build_base_blocks(const int state[10], uint16_t u11_0[5], uint16_t u12_0[5], uint16_t u21_0[5]) {
    uint16_t c1[5], b[5], bs[5];
    c1[0] = skew_elems[state[0] % 17];
    c1[1] = state[1] % 289; c1[4] = neg_tab[conj_tab[c1[1]]];
    c1[2] = state[2] % 289; c1[3] = neg_tab[conj_tab[c1[2]]];

    int mode = state[6] & 1;
    if (mode == 0) {
        b[0] = herm_elems[state[3] % 17];
        b[1] = state[4] % 289; b[4] = conj_tab[b[1]];
        b[2] = state[5] % 289; b[3] = conj_tab[b[2]];
    } else {
        b[0] = skew_elems[state[3] % 17];
        b[1] = state[4] % 289; b[4] = neg_tab[conj_tab[b[1]]];
        b[2] = state[5] % 289; b[3] = neg_tab[conj_tab[b[2]]];
    }
    for (int k = 0; k < 5; k++) bs[k] = conj_tab[b[(5 - k) % 5]];

    uint16_t P1[5], Pm1[5];
    for (int k = 0; k < 5; k++) {
        P1[k]  = (k == 0) ? add_tab[1][c1[0]] : c1[k];
        Pm1[k] = (k == 0) ? sub_tab[1][c1[0]] : neg_tab[c1[k]];
    }
    uint16_t P1Pm1[5], Pm1sq[5], BB[5], del[5], inv_del[5];
    conv5(P1, Pm1, P1Pm1); conv5(Pm1, Pm1, Pm1sq); conv5(b, bs, BB);
    for (int k = 0; k < 5; k++) del[k] = add_tab[P1Pm1[k]][BB[k]];
    if (!inv_circ5(del, inv_del)) return 0;

    uint16_t n11[5], n12[5];
    for (int k = 0; k < 5; k++) {
        n11[k] = sub_tab[Pm1sq[k]][BB[k]];
        n12[k] = mul_tab[15][b[k]];
    }
    conv5(inv_del, n12, u12_0);
    if (!check_circ5_r12_nonzero(u12_0)) return 0;
    uint16_t inv_u12[5];
    if (!inv_circ5(u12_0, inv_u12)) return 0;
    if (!check_circ5_r12_nonzero(inv_u12)) return 0;

    conv5(inv_del, n11, u11_0);
    for (int k = 0; k < 5; k++) u21_0[k] = (mode == 0) ? neg_tab[u12_0[k]] : u12_0[k];
    return 1;
}

static inline int get_k_idx(const int state[10]) {
    return ((state[7] % 17) * 289 + (state[8] % 289)) * 289 + (state[9] % 289);
}

static inline int assemble_dressed_u_fast(const uint16_t u11_0[5], const uint16_t u12_0[5], const uint16_t u21_0[5],
                                          const uint16_t k_vec[5], uint16_t U[10][10]) {
    uint16_t u11[5], u22[5];
    conv5(k_vec, u11_0, u11);
    if (!check_circ5_r12_nonzero(u11)) return 0;
    for (int k = 0; k < 5; k++) u22[k] = conj_tab[u11[(5 - k) % 5]];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            U[5 + i][5 + j] = u22[d];
            U[i][5 + j] = u12_0[d];
            U[5 + i][j] = u21_0[d];
        }
    return 1;
}

static int build_d23b_full(const int state[10], uint16_t U[10][10]) {
    int kidx = get_k_idx(state);
    if (!K_VALID[kidx]) return 0;
    uint16_t u11_0[5], u12_0[5], u21_0[5];
    if (!build_base_blocks(state, u11_0, u12_0, u21_0)) return 0;
    return assemble_dressed_u_fast(u11_0, u12_0, u21_0, K_TAB[kidx], U);
}

static inline uint16_t eval_orb4(const uint16_t D2[45][45], const Orb4 *o) {
    const uint16_t *rt = D2[o->rp_top];
    const uint16_t *rb = D2[o->rp_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->cp_bot;
    uint16_t s = sub_tab[mul_tab[rt[ct[0]]][rb[cb[0]]]][mul_tab[rt[ct[1]]][rb[cb[1]]]];
    s = add_tab[s][mul_tab[rt[ct[2]]][rb[cb[2]]]];
    s = add_tab[s][mul_tab[rt[ct[3]]][rb[cb[3]]]];
    s = sub_tab[s][mul_tab[rt[ct[4]]][rb[cb[4]]]];
    s = add_tab[s][mul_tab[rt[ct[5]]][rb[cb[5]]]];
    return s;
}

static inline uint16_t eval_orb5_lazy(const uint16_t U[10][10], const uint16_t D2[45][45], const Orb5 *o) {
    const uint16_t *rt = D2[o->rp_top];
    const uint16_t *ur = U[o->r2];
    const uint16_t *d2r = D2[o->rp34];
    uint16_t rb[10];
    for (int k = 0; k < 10; k++) {
        rb[k] = add_tab[sub_tab[mul_tab[ur[o->c_a[k]]][d2r[o->cp_bc[k]]]][mul_tab[ur[o->c_b[k]]][d2r[o->cp_ac[k]]]]][mul_tab[ur[o->c_c[k]]][d2r[o->cp_ab[k]]]];
    }
    const uint8_t *ct = o->cp_top;
    uint16_t s = sub_tab[mul_tab[rt[ct[0]]][rb[0]]][mul_tab[rt[ct[1]]][rb[1]]];
    s = add_tab[s][mul_tab[rt[ct[2]]][rb[2]]];
    s = sub_tab[s][mul_tab[rt[ct[3]]][rb[3]]];
    s = add_tab[s][mul_tab[rt[ct[4]]][rb[4]]];
    s = sub_tab[s][mul_tab[rt[ct[5]]][rb[5]]];
    s = add_tab[s][mul_tab[rt[ct[6]]][rb[6]]];
    s = add_tab[s][mul_tab[rt[ct[7]]][rb[7]]];
    s = sub_tab[s][mul_tab[rt[ct[8]]][rb[8]]];
    s = add_tab[s][mul_tab[rt[ct[9]]][rb[9]]];
    return s;
}

static inline uint16_t eval_orb5(const uint16_t D2[45][45], const uint16_t D3[120][120], const Orb5 *o) {
    const uint16_t *rt = D2[o->rp_top];
    const uint16_t *rb = D3[o->rt_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->ct_bot;
    uint16_t s = sub_tab[mul_tab[rt[ct[0]]][rb[cb[0]]]][mul_tab[rt[ct[1]]][rb[cb[1]]]];
    s = add_tab[s][mul_tab[rt[ct[2]]][rb[cb[2]]]];
    s = sub_tab[s][mul_tab[rt[ct[3]]][rb[cb[3]]]];
    s = add_tab[s][mul_tab[rt[ct[4]]][rb[cb[4]]]];
    s = sub_tab[s][mul_tab[rt[ct[5]]][rb[cb[5]]]];
    s = add_tab[s][mul_tab[rt[ct[6]]][rb[cb[6]]]];
    s = add_tab[s][mul_tab[rt[ct[7]]][rb[cb[7]]]];
    s = sub_tab[s][mul_tab[rt[ct[8]]][rb[cb[8]]]];
    s = add_tab[s][mul_tab[rt[ct[9]]][rb[cb[9]]]];
    return s;
}

static void eval_g40_d23b(const uint16_t U[10][10], int cap_r12, int cap_sub, int cap_tot,
                          int *out_r12, int *out_sub, int *out_ext) {
    int b_sub = 0, b_ext = 0, b_r12 = 0;

    for (int i = 0; i < n_orbs2_sub; i++) {
        const Orb2 *o = &orbs2_sub[i];
        if (sub_tab[mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]]][mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]] == 0) {
            b_sub++;
            if (++b_r12 > cap_r12 || b_sub > cap_sub) { *out_r12 = b_r12; *out_sub = 999; *out_ext = 9999; return; }
        }
    }
    for (int i = 0; i < n_orbs2_ext; i++) {
        const Orb2 *o = &orbs2_ext[i];
        if (sub_tab[mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]]][mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]] == 0) {
            b_ext++;
            if (++b_r12 > cap_r12) { *out_r12 = b_r12; *out_sub = 999; *out_ext = 9999; return; }
        }
    }
    *out_r12 = b_r12;

    uint16_t D2[45][45];
    for (int k = 0; k < n_z5_pairs; k++) {
        int rp = z5_pairs[k].rp, cp = z5_pairs[k].cp;
        int r0 = pairs[rp][0], r1 = pairs[rp][1];
        int c0 = pairs[cp][0], c1 = pairs[cp][1];
        uint16_t d = sub_tab[mul_tab[U[r0][c0]][U[r1][c1]]][mul_tab[U[r0][c1]][U[r1][c0]]];
        uint16_t nd = neg_tab[d];
        for (int s = 0; s < 5; s++) {
            int srp = pair_shift[rp][s], scp = pair_shift[cp][s];
            D2[srp][scp] = (pair_flip[rp][s] ^ pair_flip[cp][s]) ? nd : d;
        }
    }

    for (int i = 0; i < n_orbs3_sub; i++) {
        const Orb3 *o = &orbs3_sub[i];
        const uint16_t *ur = U[o->r0], *d2r = D2[o->rp_bot];
        if (add_tab[sub_tab[mul_tab[ur[o->c0]][d2r[o->cp12]]][mul_tab[ur[o->c1]][d2r[o->cp02]]]][mul_tab[ur[o->c2]][d2r[o->cp01]]] == 0)
            if (++b_sub > cap_sub) { *out_sub = b_sub; *out_ext = 9999; return; }
    }
    for (int i = 0; i < n_orbs4_sub; i++) {
        if (eval_orb4(D2, &orbs4_sub[i]) == 0)
            if (++b_sub > cap_sub) { *out_sub = b_sub; *out_ext = 9999; return; }
    }
    for (int i = 0; i < n_orbs5_sub; i++) {
        if (eval_orb5_lazy(U, D2, &orbs5_sub[i]) == 0)
            if (++b_sub > cap_sub) { *out_sub = b_sub; *out_ext = 9999; return; }
    }
    *out_sub = b_sub;

    if (cap_tot < 0) {
        *out_ext = 9999;
        return;
    }

    int max_ext = cap_tot - b_sub;
    if (b_ext > max_ext) { *out_ext = 9999; return; }

    for (int i = 0; i < n_orbs3_ext; i++) {
        const Orb3 *o = &orbs3_ext[i];
        const uint16_t *ur = U[o->r0], *d2r = D2[o->rp_bot];
        if (add_tab[sub_tab[mul_tab[ur[o->c0]][d2r[o->cp12]]][mul_tab[ur[o->c1]][d2r[o->cp02]]]][mul_tab[ur[o->c2]][d2r[o->cp01]]] == 0)
            if (++b_ext > max_ext) { *out_ext = b_ext; return; }
    }
    for (int i = 0; i < n_orbs4_ext; i++) {
        if (eval_orb4(D2, &orbs4_ext[i]) == 0)
            if (++b_ext > max_ext) { *out_ext = b_ext; return; }
    }

    uint16_t D3[120][120];
    for (int k = 0; k < n_z5_triples; k++) {
        const Triple3 *tr = &z5_triples[k];
        const uint16_t *ur = U[tr->r0], *d2r = D2[tr->rp_bot];
        uint16_t d = add_tab[sub_tab[mul_tab[ur[tr->c0]][d2r[tr->cp12]]][mul_tab[ur[tr->c1]][d2r[tr->cp02]]]][mul_tab[ur[tr->c2]][d2r[tr->cp01]]];
        uint16_t nd = neg_tab[d];
        int rt = tr->rt, ct = tr->ct;
        for (int s = 0; s < 5; s++) {
            int srt = triple_shift[rt][s], sct = triple_shift[ct][s];
            D3[srt][sct] = (triple_flip[rt][s] ^ triple_flip[ct][s]) ? nd : d;
        }
    }

    for (int i = 0; i < n_orbs5_ext; i++) {
        if (eval_orb5(D2, D3, &orbs5_ext[i]) == 0)
            if (++b_ext > max_ext) { *out_ext = b_ext; return; }
    }
    *out_ext = b_ext;
}

static volatile int found = 0;
static int global_best_tot = 999999;
static int global_best_sub = 999999;
static uint64_t total_evals = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static const int init_seeds[6][10] = {
    {16, 285,  65,  1, 219,  41, 1,  9, 201,  48},
    { 3,  47, 232,  0, 269,  21, 1,  7, 249, 171},
    { 3,  48, 231,  0, 231,  69, 1,  0,  15, 216},
    {15, 178, 130,  3, 215, 230, 1,  2, 286, 190},
    {10, 151, 270,  2, 224, 174, 0,  7,   0,   0},
    {13, 283, 246,  3,  90,  50, 0,  0,   0,   0}
};

static inline int compute_score(int b_r12, int b_sub, int b_ext) {
    if (b_r12 > 0) return 200000 + b_r12 * 10000 + b_sub * 100;
    if (b_sub > 2 || b_ext > 4793) return 50000 + b_sub * 100;
    int tot = b_sub + b_ext;
    return tot * 8 + b_sub;
}

static void *worker(void *arg) {
    int tid = (int)(uintptr_t)arg;
    uint64_t rng = 0x9e3779b97f4a7c15ULL ^ ((uint64_t)(tid + 1) * 0xbf58476d1ce4e5b9ULL) ^ (uint64_t)time(NULL);
    int dom[10] = {17, 289, 289, 17, 289, 289, 2, 17, 289, 289};
    int state[10], best_local[10];
    uint16_t U[10][10];
    uint16_t u11_0[5], u12_0[5], u21_0[5];
    uint64_t local_evals = 0;
    int iter = 0;

    while (!found) {
        if (iter == 0 && tid < 6) {
            memcpy(state, init_seeds[tid], sizeof(state));
        } else {
            for (int j = 0; j < 10; j++) {
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                state[j] = (int)(rng % dom[j]);
            }
        }
        iter++;
        if (!build_d23b_full(state, U)) continue;
        int cur_r12, cur_sub, cur_ext;
        eval_g40_d23b(U, 128, 538, 4970, &cur_r12, &cur_sub, &cur_ext);
        local_evals++;
        int cur_score = compute_score(cur_r12, cur_sub, cur_ext);

        memcpy(best_local, state, sizeof(state));
        int best_local_score = cur_score;
        int plateau = 0;

        for (int step = 0; step < 300 && !found; step++) {
            int improved = 0;
            int v_start = (int)(rng % 10);
            for (int vi = 0; vi < 10; vi++) {
                int v = (v_start + vi) % 10;
                int old_v = state[v], best_d = old_v;
                int d_start = (int)(rng % dom[v]);

                int kidx_fixed = 0;
                if (v >= 7) {
                    if (!build_base_blocks(state, u11_0, u12_0, u21_0)) continue;
                } else {
                    kidx_fixed = get_k_idx(state);
                    if (!K_VALID[kidx_fixed]) continue;
                }

                for (int di = 0; di < dom[v]; di++) {
                    int d = (d_start + di) % dom[v];
                    if (d == old_v) continue;
                    state[v] = d;
                    if (v >= 7) {
                        int kidx = get_k_idx(state);
                        if (!K_VALID[kidx]) continue;
                        if (!assemble_dressed_u_fast(u11_0, u12_0, u21_0, K_TAB[kidx], U)) continue;
                    } else {
                        if (!build_base_blocks(state, u11_0, u12_0, u21_0)) continue;
                        if (!assemble_dressed_u_fast(u11_0, u12_0, u21_0, K_TAB[kidx_fixed], U)) continue;
                    }

                    int r12_cap = cur_r12;
                    int sub_cap = (cur_r12 > 0) ? 177 : ((cur_sub <= 2) ? 2 : cur_sub);
                    int tot_cap = (cur_r12 == 0 && cur_sub <= 2) ? (cur_sub + cur_ext) : -1;
                    int b_r12 = 999, b_sub = 999, b_ext = 9999;
                    eval_g40_d23b(U, r12_cap, sub_cap, tot_cap, &b_r12, &b_sub, &b_ext);
                    local_evals++;
                    if (b_r12 > r12_cap || b_sub > sub_cap) continue;
                    if (tot_cap >= 0 && (b_sub + b_ext) > tot_cap) continue;

                    int sc = compute_score(b_r12, b_sub, b_ext);
                    if (sc < cur_score) {
                        cur_score = sc;
                        cur_r12 = b_r12;
                        cur_sub = b_sub;
                        cur_ext = b_ext;
                        best_d = d;
                        improved = 1;
                    } else if (sc == cur_score && (rng & 7) == 0) {
                        best_d = d;
                    }
                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                }
                state[v] = best_d;
            }

            /* Fast 2048-sample K_TAB burst on elite bases (cur_r12 == 0 && cur_sub <= 2)! */
            if (cur_r12 == 0 && cur_sub <= 2 && build_base_blocks(state, u11_0, u12_0, u21_0)) {
                for (int ks = 0; ks < 2048; ks++) {
                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                    int kidx = (int)(rng % N_KTOT);
                    if (!K_VALID[kidx]) continue;
                    if (!assemble_dressed_u_fast(u11_0, u12_0, u21_0, K_TAB[kidx], U)) continue;
                    int sub_cap = 1;
                    int tot_cap = cur_sub + cur_ext;
                    int b_r12 = 999, b_sub = 999, b_ext = 9999;
                    eval_g40_d23b(U, 0, sub_cap, tot_cap, &b_r12, &b_sub, &b_ext);
                    local_evals++;
                    if (b_r12 == 0 && b_sub <= sub_cap && (b_sub + b_ext) <= tot_cap) {
                        int sc = compute_score(0, b_sub, b_ext);
                        if (sc < cur_score) {
                            cur_score = sc;
                            cur_sub = b_sub;
                            cur_ext = b_ext;
                            state[7] = kidx / (289 * 289);
                            state[8] = (kidx / 289) % 289;
                            state[9] = kidx % 289;
                            improved = 1;
                        }
                    }
                }
            }

            if (cur_r12 == 0 && cur_sub <= 4) {
                if (build_d23b_full(state, U)) {
                    eval_g40_d23b(U, 0, 538, 4970, &cur_r12, &cur_sub, &cur_ext);
                    cur_score = compute_score(cur_r12, cur_sub, cur_ext);
                    int tot = cur_sub + cur_ext;
                    if (tot < global_best_tot || (tot == global_best_tot && cur_sub < global_best_sub)) {
                        pthread_mutex_lock(&lock);
                        if (tot < global_best_tot || (tot == global_best_tot && cur_sub < global_best_sub)) {
                            if (tot < global_best_tot) global_best_tot = tot;
                            if (cur_sub < global_best_sub) global_best_sub = cur_sub;
                            printf("[D23b-Turbo T%d] r12=0 | sub=%d/177 | ext=%d/4793 | TOTAL=%d/4970 (%.4f%%) state=[%d,%d,%d,%d,%d,%d,m=%d | K=%d,%d,%d]\n",
                                   tid, cur_sub, cur_ext, tot, 100.0 * (4970 - tot) / 4970.0,
                                   state[0],state[1],state[2],state[3],state[4],state[5],state[6],
                                   state[7],state[8],state[9]);
                            fflush(stdout);
                            if (tot == 0) found = 1;
                        }
                        pthread_mutex_unlock(&lock);
                    }
                }
            }

            if (cur_score < best_local_score) {
                best_local_score = cur_score;
                memcpy(best_local, state, sizeof(state));
                plateau = 0;
            } else {
                plateau++;
            }

            if (!improved) {
                if (plateau >= 6) break;
                memcpy(state, best_local, sizeof(state));
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                int v1 = (int)(rng % 6);
                int v2 = 7 + (int)(rng % 3);
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                state[v1] = (int)(rng % dom[v1]);
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                state[v2] = (int)(rng % dom[v2]);
                if (!build_d23b_full(state, U)) continue;
                eval_g40_d23b(U, 128, 538, 4970, &cur_r12, &cur_sub, &cur_ext);
                local_evals++;
                cur_score = compute_score(cur_r12, cur_sub, cur_ext);
            }
        }
    }
    pthread_mutex_lock(&lock);
    total_evals += local_evals;
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main(void) {
    init_gf289();
    init_combinatorics();
    build_all_tables();

    K_TAB = malloc(sizeof(uint16_t[5]) * N_KTOT);
    K_VALID = malloc(sizeof(uint8_t) * N_KTOT);
    pthread_t kth[8];
    for (int i = 0; i < 8; i++) pthread_create(&kth[i], NULL, init_ktab_worker, (void*)(uintptr_t)i);
    for (int i = 0; i < 8; i++) pthread_join(kth[i], NULL);
    int n_kval = 0;
    for (int i = 0; i < N_KTOT; i++) if (K_VALID[i]) n_kval++;
    printf("Precomputed K_TAB: %d / %d valid unitary circulants in C_5(F_289)\n", n_kval, N_KTOT);
    fflush(stdout);

    pthread_t th[8];
    for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker, (void*)(uintptr_t)i);
    for (int s = 0; s < 6 && !found; s++) {
        struct timespec ts = {1, 0};
        nanosleep(&ts, NULL);
    }
    found = 1;
    for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
    printf("Total Theorem D23b turbo matrices evaluated in 8s: %llu (%.1f matrices/sec)\n",
           (unsigned long long)total_evals, total_evals / 6.0);
    return 0;
}
