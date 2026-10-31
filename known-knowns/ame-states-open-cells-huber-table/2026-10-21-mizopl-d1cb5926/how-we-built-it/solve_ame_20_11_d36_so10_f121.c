#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

/*
 * Theorem D36 (`scripts/solve_ame_20_11_d36_so10_f121.c` — Shell v19 Track C):
 *   1. Exact 12-Orbit Diagnostic of the L-ASOC-021 Record State in U(10, F_121):
 *      u11 = [109, 59, 31, 90, 110], u12 = [74, 39, 50, 66, 109] (12 / 4,970 bad orbits:
 *      sub = 2/177, ext = 10/4793, 99.7586% non-zero across all 184,755 minors!).
 *   2. Frobenius-Free Orthogonal Block-Circulant Solver in SO(10, F_121) (U * U^T = I_10):
 *      In U(10, F_121) (D33 and D33B), the reflection W acts conjugate-linearly (Frobenius
 *      parity b(W) = 1), forcing 177 orbits into the base field F_11 where they vanish with
 *      probability 1/11 = 9.09% (expected 16.09 bad sub orbits).
 *      By contrast, in SO(10, F_121):
 *        U = [ U_11,  U_12 ]
 *            [-U_12, U_11^T]   with U_12^T = U_12 and U_11 * U_11^T + U_12^2 = I_5,
 *      every generator of G_40 = <Z_5, W, R, comp> acts F_121-LINEARLY (b(g) == 0 identically!).
 *      Hence ALL 177 `sub` orbits are liberated from F_11 into F_121 (vanishing at ~1/121 = 0.826%
 *      instead of 1/11 = 9.09%, reducing expected bad sub orbits from 16.09 to 1.48!).
 *      Furthermore, over F_121, 5-point DFT splits C_5(F_121) completely (zeta_5 = 3 in F_11),
 *      giving 14,400 exact orthogonal dressings K * K^T = I_5 in L1/L2 cache.
 */

#define P 11
#define Q2 121
#define NONRES 7

static uint8_t mul_tab[121][121], add_tab[121][121], sub_tab[121][121], neg_tab[121], inv_tab[121], conj_tab[121];
static uint8_t sqrt_tab[121]; /* sqrt_tab[w] = s in F_121 such that s*s = w, or 0 if non-square */
static const uint8_t zeta5[5] = {1, 3, 9, 5, 4};

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

    memset(sqrt_tab, 0, sizeof(sqrt_tab));
    for (int a = 1; a < Q2; a++) {
        uint8_t sq = mul_tab[a][a];
        if (!sqrt_tab[sq]) sqrt_tab[sq] = (uint8_t)a;
    }
}

static inline void dft5(const uint8_t x[5], uint8_t lam[5]) {
    for (int k = 0; k < 5; k++) {
        uint8_t s = 0;
        for (int d = 0; d < 5; d++)
            s = add_tab[s][mul_tab[x[d]][zeta5[(k * d) % 5]]];
        lam[k] = s;
    }
}

static inline void idft5(const uint8_t lam[5], uint8_t x[5]) {
    for (int d = 0; d < 5; d++) {
        uint8_t s = 0;
        for (int k = 0; k < 5; k++)
            s = add_tab[s][mul_tab[lam[k]][zeta5[(5 - ((k * d) % 5)) % 5]]];
        x[d] = mul_tab[9][s];
    }
}

static inline void conv5(const uint8_t x[5], const uint8_t y[5], uint8_t out[5]) {
    for (int k = 0; k < 5; k++) {
        uint8_t s = 0;
        for (int i = 0; i < 5; i++)
            s = add_tab[s][mul_tab[x[i]][y[(k - i + 5) % 5]]];
        out[k] = s;
    }
}

static inline int check_circ5_r12_nonzero(const uint8_t x[5]) {
    if (!x[0] || !x[1] || !x[2] || !x[3] || !x[4]) return 0;
    for (int dr = 1; dr <= 2; dr++) {
        for (int dc = 1; dc <= 2; dc++) {
            for (int j = 0; j < 5; j++) {
                int c0 = j, c1 = (j + dc) % 5;
                uint8_t a00 = x[c0], a01 = x[c1];
                uint8_t a10 = x[(c0 - dr + 5) % 5], a11 = x[(c1 - dr + 5) % 5];
                if (sub_tab[mul_tab[a00][a11]][mul_tab[a01][a10]] == 0) return 0;
            }
        }
    }
    return 1;
}

/* 14,400 projective orthogonal circulants K in C_5(F_121) satisfying K * K^T = I_5:
 * lam = [1, k1, k2, k2^{-1}, k1^{-1}]
 */
#define N_KTOT (120 * 120)
static uint8_t K_ORTHO[N_KTOT][5];
static uint8_t K_ORTHO_T[N_KTOT][5];

static void init_k_ortho(void) {
    int idx = 0;
    for (int k1 = 1; k1 < Q2; k1++) {
        uint8_t k4 = inv_tab[k1];
        for (int k2 = 1; k2 < Q2; k2++) {
            uint8_t k3 = inv_tab[k2];
            uint8_t lam[5] = {1, (uint8_t)k1, (uint8_t)k2, k3, k4};
            idft5(lam, K_ORTHO[idx]);
            for (int d = 0; d < 5; d++)
                K_ORTHO_T[idx][d] = K_ORTHO[idx][(5 - d) % 5];
            idx++;
        }
    }
    printf("Precomputed K_ORTHO: %d exact projective orthogonal circulants (K * K^T = I_5) over F_121\n", idx);
}

typedef struct {
    uint8_t u12[5];
    uint8_t u21[5];
    uint8_t u11_0[5];
    uint8_t inv_u11_0[5];
} BaseSO10;

static BaseSO10 *BASES = NULL;
static int N_BASES = 0;

/* Under Z_4 automorphism d -> 2*d mod 5 on symmetric circulants [u0, u1, u2, u2, u1],
 * (u1, u2) -> (u2, u1), and overall sign flip (u0, u1, u2) -> (-u0, -u1, -u2).
 */
static void init_bases_so10(void) {
    int cap = 120 * 120 * 120;
    BASES = malloc(sizeof(BaseSO10) * 60000);
    for (int u0 = 1; u0 < Q2; u0++) {
        /* Up to global sign +-1 on U_12, require u0 < neg_tab[u0] */
        if (u0 > neg_tab[u0]) continue;
        for (int u1 = 1; u1 < Q2; u1++) {
            for (int u2 = u1; u2 < Q2; u2++) {
                uint8_t u12[5] = {(uint8_t)u0, (uint8_t)u1, (uint8_t)u2, (uint8_t)u2, (uint8_t)u1};
                if (!check_circ5_r12_nonzero(u12)) continue;

                uint8_t mu[5], inv_mu[5];
                dft5(u12, mu);
                int ok = 1;
                for (int k = 0; k < 5; k++) {
                    if (!mu[k]) { ok = 0; break; }
                    inv_mu[k] = inv_tab[mu[k]];
                }
                if (!ok) continue;
                uint8_t inv_u12[5];
                idft5(inv_mu, inv_u12);
                if (!check_circ5_r12_nonzero(inv_u12)) continue;

                /* w_lam[k] = 1 - mu[k]^2 in F_121 */
                uint8_t w_lam[5];
                for (int k = 0; k < 5; k++) {
                    uint8_t sq = mul_tab[mu[k]][mu[k]];
                    w_lam[k] = sub_tab[1][sq];
                    if (!w_lam[k]) { ok = 0; break; }
                }
                if (!ok) continue;
                /* Need w_lam[0] = 1 - mu[0]^2 to be a square in F_121^* */
                uint8_t s0 = sqrt_tab[w_lam[0]];
                if (!s0) continue;

                uint8_t u11_lam[5] = {s0, 1, 1, w_lam[3], w_lam[4]};
                uint8_t inv_u11_lam[5];
                for (int k = 0; k < 5; k++) inv_u11_lam[k] = inv_tab[u11_lam[k]];
                BaseSO10 *b = &BASES[N_BASES++];
                idft5(u11_lam, b->u11_0);
                idft5(inv_u11_lam, b->inv_u11_0);
                for (int d = 0; d < 5; d++) {
                    b->u12[d] = u12[d];
                    b->u21[d] = neg_tab[u12[d]]; /* U_21 = -U_12^T = -U_12 */
                }
            }
        }
    }
    printf("Precomputed SO(10, F_121) canonical BASES: %d (x 14,400 K_ORTHO = %llu pairs)\n",
           N_BASES, (unsigned long long)N_BASES * N_KTOT);
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

typedef struct { uint8_t r0, c0; uint32_t mask; } Orb1;
typedef struct { uint8_t rp, cp, r0, r1, c0, c1; uint32_t mask; } Orb2;
typedef struct { uint8_t r0, r1, r2, rp_bot, c0, c1, c2, cp12, cp02, cp01; uint32_t mask; } Orb3;
typedef struct { uint8_t rp_top, rp_bot, cp_top[6], cp_bot[6]; uint32_t mask; } Orb4;
typedef struct {
    uint8_t rp_top, rt_bot;
    uint8_t cp_top[10], ct_bot[10];
    uint8_t r2, rp34;
    uint8_t c_a[10], c_b[10], c_c[10];
    uint8_t cp_bc[10], cp_ac[10], cp_ab[10];
    uint32_t mask;
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
                    o->r0 = rw[0]; o->c0 = cl[0]; o->mask = m;
                } else if (r == 2) {
                    Orb2 *o = is_sub ? &orbs2_sub[n_orbs2_sub++] : &orbs2_ext[n_orbs2_ext++];
                    o->r0 = rw[0]; o->r1 = rw[1]; o->c0 = cl[0]; o->c1 = cl[1];
                    o->rp = pair_id[rw[0]][rw[1]]; o->cp = pair_id[cl[0]][cl[1]]; o->mask = m;
                } else if (r == 3) {
                    Orb3 *o = is_sub ? &orbs3_sub[n_orbs3_sub++] : &orbs3_ext[n_orbs3_ext++];
                    o->r0 = rw[0]; o->r1 = rw[1]; o->r2 = rw[2];
                    o->rp_bot = pair_id[rw[1]][rw[2]];
                    o->c0 = cl[0]; o->c1 = cl[1]; o->c2 = cl[2];
                    o->cp12 = pair_id[cl[1]][cl[2]];
                    o->cp02 = pair_id[cl[0]][cl[2]];
                    o->cp01 = pair_id[cl[0]][cl[1]]; o->mask = m;
                } else if (r == 4) {
                    Orb4 *o = is_sub ? &orbs4_sub[n_orbs4_sub++] : &orbs4_ext[n_orbs4_ext++];
                    o->rp_top = pair_id[rw[0]][rw[1]];
                    o->rp_bot = pair_id[rw[2]][rw[3]];
                    for (int k = 0; k < 6; k++) {
                        o->cp_top[k] = pair_id[cl[comb42_a[k]]][cl[comb42_b[k]]];
                        o->cp_bot[k] = pair_id[cl[comb42_c[k]]][cl[comb42_d[k]]];
                    }
                    o->mask = m;
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
                    o->mask = m;
                }
            }
        }
    }
}

static inline uint8_t eval_orb3_direct(const uint8_t U[10][10], const Orb3 *o) {
    const uint8_t *r0 = U[o->r0], *r1 = U[o->r1], *r2 = U[o->r2];
    int c0 = o->c0, c1 = o->c1, c2 = o->c2;
    uint8_t d12 = sub_tab[mul_tab[r1[c1]][r2[c2]]][mul_tab[r1[c2]][r2[c1]]];
    uint8_t d02 = sub_tab[mul_tab[r1[c0]][r2[c2]]][mul_tab[r1[c2]][r2[c0]]];
    uint8_t d01 = sub_tab[mul_tab[r1[c0]][r2[c1]]][mul_tab[r1[c1]][r2[c0]]];
    return add_tab[sub_tab[mul_tab[r0[c0]][d12]][mul_tab[r0[c1]][d02]]][mul_tab[r0[c2]][d01]];
}

static inline uint8_t eval_orb4(const uint8_t D2[45][45], const Orb4 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *rb = D2[o->rp_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->cp_bot;
    uint8_t s = sub_tab[mul_tab[rt[ct[0]]][rb[cb[0]]]][mul_tab[rt[ct[1]]][rb[cb[1]]]];
    s = add_tab[s][mul_tab[rt[ct[2]]][rb[cb[2]]]];
    s = add_tab[s][mul_tab[rt[ct[3]]][rb[cb[3]]]];
    s = sub_tab[s][mul_tab[rt[ct[4]]][rb[cb[4]]]];
    s = add_tab[s][mul_tab[rt[ct[5]]][rb[cb[5]]]];
    return s;
}

static inline uint8_t eval_orb5_lazy(const uint8_t U[10][10], const uint8_t D2[45][45], const Orb5 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *ur = U[o->r2];
    const uint8_t *d2r = D2[o->rp34];
    uint8_t rb[10];
    for (int k = 0; k < 10; k++) {
        rb[k] = add_tab[sub_tab[mul_tab[ur[o->c_a[k]]][d2r[o->cp_bc[k]]]][mul_tab[ur[o->c_b[k]]][d2r[o->cp_ac[k]]]]][mul_tab[ur[o->c_c[k]]][d2r[o->cp_ab[k]]]];
    }
    const uint8_t *ct = o->cp_top;
    uint8_t s = sub_tab[mul_tab[rt[ct[0]]][rb[0]]][mul_tab[rt[ct[1]]][rb[1]]];
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

static inline uint8_t eval_orb5(const uint8_t D2[45][45], const uint8_t D3[120][120], const Orb5 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *rb = D3[o->rt_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->ct_bot;
    uint8_t s = sub_tab[mul_tab[rt[ct[0]]][rb[cb[0]]]][mul_tab[rt[ct[1]]][rb[cb[1]]]];
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

static void eval_g40_d28_fast(const uint8_t U[10][10], int cap_sub, int cap_tot,
                              int *out_sub, int *out_ext) {
    int b_sub = 0, b_ext = 0;

    for (int i = 0; i < n_orbs2_sub; i++) {
        const Orb2 *o = &orbs2_sub[i];
        if (sub_tab[mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]]][mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]] == 0) {
            if (++b_sub > cap_sub) { *out_sub = 999; *out_ext = 9999; return; }
        }
    }
    for (int i = 0; i < n_orbs3_sub; i++) {
        if (eval_orb3_direct(U, &orbs3_sub[i]) == 0) {
            if (++b_sub > cap_sub) { *out_sub = 999; *out_ext = 9999; return; }
        }
    }

    uint8_t D2[45][45];
    for (int k = 0; k < n_z5_pairs; k++) {
        int rp = z5_pairs[k].rp, cp = z5_pairs[k].cp;
        int r0 = pairs[rp][0], r1 = pairs[rp][1];
        int c0 = pairs[cp][0], c1 = pairs[cp][1];
        uint8_t d = sub_tab[mul_tab[U[r0][c0]][U[r1][c1]]][mul_tab[U[r0][c1]][U[r1][c0]]];
        uint8_t nd = neg_tab[d];
        for (int s = 0; s < 5; s++) {
            int srp = pair_shift[rp][s], scp = pair_shift[cp][s];
            D2[srp][scp] = (pair_flip[rp][s] ^ pair_flip[cp][s]) ? nd : d;
        }
    }

    for (int i = 0; i < n_orbs4_sub; i++) {
        if (eval_orb4(D2, &orbs4_sub[i]) == 0)
            if (++b_sub > cap_sub) { *out_sub = 999; *out_ext = 9999; return; }
    }
    for (int i = 0; i < n_orbs5_sub; i++) {
        if (eval_orb5_lazy(U, D2, &orbs5_sub[i]) == 0)
            if (++b_sub > cap_sub) { *out_sub = 999; *out_ext = 9999; return; }
    }
    *out_sub = b_sub;

    int max_ext = cap_tot - b_sub;
    if (max_ext < 0) { *out_ext = 9999; return; }

    for (int i = 0; i < n_orbs2_ext; i++) {
        const Orb2 *o = &orbs2_ext[i];
        if (D2[o->rp][o->cp] == 0)
            if (++b_ext > max_ext) { *out_ext = 9999; return; }
    }
    for (int i = 0; i < n_orbs3_ext; i++) {
        const Orb3 *o = &orbs3_ext[i];
        const uint8_t *ur = U[o->r0], *d2r = D2[o->rp_bot];
        if (add_tab[sub_tab[mul_tab[ur[o->c0]][d2r[o->cp12]]][mul_tab[ur[o->c1]][d2r[o->cp02]]]][mul_tab[ur[o->c2]][d2r[o->cp01]]] == 0)
            if (++b_ext > max_ext) { *out_ext = 9999; return; }
    }
    for (int i = 0; i < n_orbs4_ext; i++) {
        if (eval_orb4(D2, &orbs4_ext[i]) == 0)
            if (++b_ext > max_ext) { *out_ext = 9999; return; }
    }

    uint8_t D3[120][120];
    for (int k = 0; k < n_z5_triples; k++) {
        const Triple3 *tr = &z5_triples[k];
        const uint8_t *ur = U[tr->r0], *d2r = D2[tr->rp_bot];
        uint8_t d = add_tab[sub_tab[mul_tab[ur[tr->c0]][d2r[tr->cp12]]][mul_tab[ur[tr->c1]][d2r[tr->cp02]]]][mul_tab[ur[tr->c2]][d2r[tr->cp01]]];
        uint8_t nd = neg_tab[d];
        int rt = tr->rt, ct = tr->ct;
        for (int s = 0; s < 5; s++) {
            int srt = triple_shift[rt][s], sct = triple_shift[ct][s];
            D3[srt][sct] = (triple_flip[rt][s] ^ triple_flip[ct][s]) ? nd : d;
        }
    }

    for (int i = 0; i < n_orbs5_ext; i++) {
        if (eval_orb5(D2, D3, &orbs5_ext[i]) == 0)
            if (++b_ext > max_ext) { *out_ext = 9999; return; }
    }
    *out_ext = b_ext;
}

static void diagnose_12bad_state(void) {
    uint8_t u11[5] = {109, 59, 31, 90, 110};
    uint8_t u12[5] = {74, 39, 50, 66, 109};
    uint8_t U[10][10];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            U[5 + i][5 + j] = conj_tab[u11[(5 - d) % 5]];
            U[i][5 + j] = u12[d];
            U[5 + i][j] = neg_tab[conj_tab[u12[(5 - d) % 5]]];
        }
    int b_sub = 0, b_ext = 0;
    eval_g40_d28_fast(U, 177, 4970, &b_sub, &b_ext);
    printf("=== 1. EXACT ANATOMY OF L-ASOC-021 RECORD STATE (sub=%d/177, ext=%d/4793, tot=%d/4970) ===\n",
           b_sub, b_ext, b_sub + b_ext);

    uint8_t D2[45][45];
    for (int k = 0; k < n_z5_pairs; k++) {
        int rp = z5_pairs[k].rp, cp = z5_pairs[k].cp;
        int r0 = pairs[rp][0], r1 = pairs[rp][1];
        int c0 = pairs[cp][0], c1 = pairs[cp][1];
        uint8_t d = sub_tab[mul_tab[U[r0][c0]][U[r1][c1]]][mul_tab[U[r0][c1]][U[r1][c0]]];
        uint8_t nd = neg_tab[d];
        for (int s = 0; s < 5; s++) {
            int srp = pair_shift[rp][s], scp = pair_shift[cp][s];
            D2[srp][scp] = (pair_flip[rp][s] ^ pair_flip[cp][s]) ? nd : d;
        }
    }
    int r_sub_cnt[6] = {0}, r_ext_cnt[6] = {0};
    for (int i = 0; i < n_orbs2_sub; i++) if (D2[orbs2_sub[i].rp][orbs2_sub[i].cp] == 0) r_sub_cnt[2]++;
    for (int i = 0; i < n_orbs3_sub; i++) if (eval_orb3_direct(U, &orbs3_sub[i]) == 0) r_sub_cnt[3]++;
    for (int i = 0; i < n_orbs4_sub; i++) if (eval_orb4(D2, &orbs4_sub[i]) == 0) r_sub_cnt[4]++;
    for (int i = 0; i < n_orbs5_sub; i++) if (eval_orb5_lazy(U, D2, &orbs5_sub[i]) == 0) r_sub_cnt[5]++;

    for (int i = 0; i < n_orbs2_ext; i++) if (D2[orbs2_ext[i].rp][orbs2_ext[i].cp] == 0) r_ext_cnt[2]++;
    for (int i = 0; i < n_orbs3_ext; i++) if (eval_orb3_direct(U, &orbs3_ext[i]) == 0) r_ext_cnt[3]++;
    for (int i = 0; i < n_orbs4_ext; i++) if (eval_orb4(D2, &orbs4_ext[i]) == 0) r_ext_cnt[4]++;
    for (int i = 0; i < n_orbs5_ext; i++) if (eval_orb5_lazy(U, D2, &orbs5_ext[i]) == 0) r_ext_cnt[5]++;

    printf("  Bad orbits by rank r=2..5: sub = [r2:%d, r3:%d, r4:%d, r5:%d] | ext = [r2:%d, r3:%d, r4:%d, r5:%d]\n\n",
           r_sub_cnt[2], r_sub_cnt[3], r_sub_cnt[4], r_sub_cnt[5],
           r_ext_cnt[2], r_ext_cnt[3], r_ext_cnt[4], r_ext_cnt[5]);
}

static inline int assemble_u_so10(const BaseSO10 *b, int kidx, uint8_t U[10][10]) {
    uint8_t u11[5], inv_u11[5], u22[5];
    conv5(K_ORTHO[kidx], b->u11_0, u11);
    if (!check_circ5_r12_nonzero(u11)) return 0;
    conv5(K_ORTHO_T[kidx], b->inv_u11_0, inv_u11);
    if (!check_circ5_r12_nonzero(inv_u11)) return 0;
    for (int d = 0; d < 5; d++) u22[d] = u11[(5 - d) % 5]; /* U_22 = U_11^T */
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            U[5 + i][5 + j] = u22[d];
            U[i][5 + j] = b->u12[d];
            U[5 + i][j] = b->u21[d];
        }
    return 1;
}

static int next_bidx = 0;
static int global_best_sub = 999;
static int global_best_tot = 9999;
static uint64_t total_valid_pairs = 0;
static uint64_t sub_hist[16];
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static int MAX_BASES_TO_SWEEP = 4000;

static void *worker_so10(void *arg) {
    int tid = (int)(uintptr_t)arg;
    uint8_t U[10][10];
    uint64_t local_valid = 0;
    uint64_t local_hist[16] = {0};

    while (1) {
        int bidx = __sync_fetch_and_add(&next_bidx, 1);
        if (bidx >= MAX_BASES_TO_SWEEP || bidx >= N_BASES) break;
        const BaseSO10 *b = &BASES[bidx];

        for (int kidx = 0; kidx < N_KTOT; kidx++) {
            if (!assemble_u_so10(b, kidx, U)) continue;
            local_valid++;
            int b_sub = 999, b_ext = 9999;
            eval_g40_d28_fast(U, 1, global_best_tot, &b_sub, &b_ext);
            if (b_sub <= 1) {
                local_hist[b_sub]++;
                if (b_sub < global_best_sub || (b_sub + b_ext) < global_best_tot) {
                    int full_sub = 999, full_ext = 9999;
                    eval_g40_d28_fast(U, 177, 4970, &full_sub, &full_ext);
                    int tot = full_sub + full_ext;
                    pthread_mutex_lock(&lock);
                    if (full_sub < global_best_sub || tot < global_best_tot) {
                        if (full_sub < global_best_sub) global_best_sub = full_sub;
                        if (tot < global_best_tot) global_best_tot = tot;
                        uint8_t u11[5];
                        conv5(K_ORTHO[kidx], b->u11_0, u11);
                        printf("[SO(10,F_121) T%d] sub=%d/177 | ext=%d/4793 | TOTAL=%d/4970 (%.4f%%) bidx=%d/%d kidx=%d u11=[%d,%d,%d,%d,%d] u12=[%d,%d,%d,%d,%d]\n",
                               tid, full_sub, full_ext, tot, 100.0 * (4970 - tot) / 4970.0,
                               bidx, MAX_BASES_TO_SWEEP, kidx,
                               u11[0], u11[1], u11[2], u11[3], u11[4],
                               b->u12[0], b->u12[1], b->u12[2], b->u12[3], b->u12[4]);
                        fflush(stdout);
                    }
                    pthread_mutex_unlock(&lock);
                }
            }
        }
    }

    pthread_mutex_lock(&lock);
    total_valid_pairs += local_valid;
    for (int i = 0; i <= 1; i++) sub_hist[i] += local_hist[i];
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc > 1) MAX_BASES_TO_SWEEP = atoi(argv[1]);
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    init_gf121();
    init_combinatorics();
    build_all_tables();
    diagnose_12bad_state();
    init_k_ortho();
    init_bases_so10();
    if (MAX_BASES_TO_SWEEP > N_BASES) MAX_BASES_TO_SWEEP = N_BASES;

    printf("=== 2. SWEEPING FIRST %d / %d CANONICAL SO(10, F_121) BASES ===\n", MAX_BASES_TO_SWEEP, N_BASES);
    fflush(stdout);

    pthread_t th[8];
    for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker_so10, (void*)(uintptr_t)i);
    for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);

    printf("\n=== SO(10, F_121) FROBENIUS-FREE SWEEP COMPLETE in %.2f s ===\n", dt);
    printf("Swept %d / %d bases | Valid r=1..2 pairs: %llu (%.1f pairs/s)\n",
           MAX_BASES_TO_SWEEP, N_BASES, (unsigned long long)total_valid_pairs, total_valid_pairs / dt);
    printf("Exact sub<=1 count across swept pairs (compare: only 25 sub=0 pairs in ALL 96.2M U(10,F_121) QNR pairs!):\n");
    printf("  sub = 0 / 177 : %llu pairs!\n", (unsigned long long)sub_hist[0]);
    printf("  sub = 1 / 177 : %llu pairs!\n", (unsigned long long)sub_hist[1]);
    printf("Global minimum in SO(10, F_121) sample: sub = %d / 177, TOTAL = %d / 4970\n",
           global_best_sub, global_best_tot);
    return 0;
}
