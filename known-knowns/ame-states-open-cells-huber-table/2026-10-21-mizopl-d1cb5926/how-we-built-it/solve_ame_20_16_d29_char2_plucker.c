#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

/*
 * Theorem D29 (Characteristic-2 Exact 5-Point DFT Unitary Factorization for AME(20, 16) = [[20, 0, 11]]_16):
 *   Over F_256 = F_2[x]/(x^8 + x^4 + x^3 + x^2 + 1), q = 16 = 1 (mod 5), so a primitive 5th root
 *   of unity zeta = g^51 lies in the base field F_16^* (conj(zeta) = zeta^16 = zeta).
 *   For any Hermitian circulant U_12 = U_12^dagger in C_5(F_256) (u_0 in F_16, u_4 = conj(u_1), u_3 = conj(u_2))
 *   with det(I_5 + U_12) != 0, every G_40-symmetric unitary matrix U in U(10, F_256) (U * U^dagger = I_10)
 *   has the exact inversion-free factorization:
 *     U_11 = K * (I_5 + U_12),   U_22 = U_11^dagger,   U_21 = U_12,
 *   where K in U(C_5(F_256)) / U(1, F_256) is parameterized in closed form by (kappa_1, kappa_2) in (F_256^*)^2
 *   (255 x 255 = 65,025 projective unitary circulants):
 *     K_d = 1 + kappa_1 * zeta^{-d} + conj(kappa_1)^{-1} * zeta^d
 *             + kappa_2 * zeta^{-2d} + conj(kappa_2)^{-1} * zeta^{2d}.
 *   Combined with the Theorem D28 exact 177-orbit Z_2-Frobenius parity sieve (b(g) = 1).
 */

#define Q2 256
static uint8_t mul_tab[256][256], inv_tab[256], conj_tab[256];
static uint8_t exp_tab[512], log_tab[256];
static uint8_t f16_elems[16];
static uint8_t zeta5[5]; /* zeta^0 .. zeta^4 in F_16^* */

static void init_gf256(void) {
    /* Primitive polynomial x^8 + x^4 + x^3 + x^2 + 1 (0x11D), primitive root g = 2 */
    int x = 1;
    for (int i = 0; i < 255; i++) {
        exp_tab[i] = (uint8_t)x;
        exp_tab[i + 255] = (uint8_t)x;
        log_tab[x] = (uint8_t)i;
        x <<= 1;
        if (x & 0x100) x ^= 0x11D;
    }
    log_tab[0] = 0;
    for (int a = 0; a < 256; a++) {
        for (int b = 0; b < 256; b++) {
            mul_tab[a][b] = (a && b) ? exp_tab[(int)log_tab[a] + (int)log_tab[b]] : 0;
        }
        inv_tab[a] = a ? exp_tab[255 - log_tab[a]] : 0;
        /* Frobenius in F_256 / F_16 is a -> a^16 */
        conj_tab[a] = a ? exp_tab[((int)log_tab[a] * 16) % 255] : 0;
    }
    int nf = 0;
    for (int a = 0; a < 256; a++) {
        if (conj_tab[a] == a) f16_elems[nf++] = (uint8_t)a;
    }
    /* Primitive 5th root of unity: g^(255/5) = g^51 (lies in F_16^* since 17 | 51) */
    for (int k = 0; k < 5; k++) {
        zeta5[k] = exp_tab[(51 * k) % 255];
    }
    printf("init_gf256: nf16=%d, zeta5=[%d,%d,%d,%d,%d], conj(zeta5[1])=%d\n",
           nf, zeta5[0], zeta5[1], zeta5[2], zeta5[3], zeta5[4], conj_tab[zeta5[1]]);
}

static int pair_id[10][10];
static uint8_t pairs[45][2];
static int pair_shift[45][5];

static int triple_id[10][10][10];
static uint8_t triples[120][3];
static int triple_shift[120][5];

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
            pair_shift[p][s] = (a < b) ? pair_id[a][b] : pair_id[b][a];
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
            int tmp;
            if (a > b) { tmp = a; a = b; b = tmp; }
            if (b > c) { tmp = b; b = c; c = tmp; }
            if (a > b) { tmp = a; a = b; b = tmp; }
            triple_shift[t][s] = triple_id[a][b][c];
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

/* 5-point DFT and IDFT over F_256 using zeta5 in F_16^* */
static inline void dft5(const uint8_t x[5], uint8_t lam[5]) {
    for (int k = 0; k < 5; k++) {
        uint8_t s = 0;
        for (int d = 0; d < 5; d++)
            s ^= mul_tab[x[d]][zeta5[(k * d) % 5]];
        lam[k] = s;
    }
}

static inline void idft5(const uint8_t lam[5], uint8_t x[5]) {
    for (int d = 0; d < 5; d++) {
        uint8_t s = 0;
        for (int k = 0; k < 5; k++)
            s ^= mul_tab[lam[k]][zeta5[(5 - ((k * d) % 5)) % 5]];
        x[d] = s;
    }
}

static inline void conv5(const uint8_t x[5], const uint8_t y[5], uint8_t out[5]) {
    for (int k = 0; k < 5; k++) {
        uint8_t s = 0;
        for (int i = 0; i < 5; i++)
            s ^= mul_tab[x[i]][y[(k - i + 5) % 5]];
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
                if ((mul_tab[a00][a11] ^ mul_tab[a01][a10]) == 0) return 0;
            }
        }
    }
    return 1;
}

/* Precompute ALL 255 x 255 = 65,025 projective unitary circulants K in C_5(F_256) */
#define N_KTOT (255 * 255)
static uint8_t K_TAB[N_KTOT][5];

static void init_ktab(void) {
    int idx = 0;
    for (int k1 = 1; k1 < 256; k1++) {
        uint8_t k4 = inv_tab[conj_tab[k1]];
        for (int k2 = 1; k2 < 256; k2++) {
            uint8_t k3 = inv_tab[conj_tab[k2]];
            uint8_t lam[5] = {1, (uint8_t)k1, (uint8_t)k2, k3, k4};
            idft5(lam, K_TAB[idx++]);
        }
    }
    printf("Precomputed K_TAB: %d exact projective unitary circulants in C_5(F_256)\n", idx);
}

/* Precompute ALL valid dressable Hermitian circulants U_12 (passing D23b r=1..5 pure-block sieve!) */
typedef struct {
    uint8_t u12[5];
    uint8_t u11_0[5]; /* I_5 + U_12 */
} BaseU12;

static BaseU12 *BASES = NULL;
static int N_BASES = 0;

static void init_bases(void) {
    int cap = 16 * 256 * 256;
    BASES = malloc(sizeof(BaseU12) * cap);
    for (int i0 = 0; i0 < 16; i0++) {
        uint8_t u0 = f16_elems[i0];
        if (!u0) continue;
        for (int u1 = 1; u1 < 256; u1++) {
            for (int u2 = 1; u2 < 256; u2++) {
                uint8_t u12[5] = {u0, (uint8_t)u1, (uint8_t)u2, conj_tab[u2], conj_tab[u1]};
                if (!check_circ5_r12_nonzero(u12)) continue;
                uint8_t mu[5];
                dft5(u12, mu);
                /* Need mu_k != 0 (U_12 invertible) and mu_k != 1 (I_5 + U_12 invertible) */
                int ok = 1;
                uint8_t inv_mu[5];
                for (int k = 0; k < 5; k++) {
                    if (mu[k] == 0 || mu[k] == 1) { ok = 0; break; }
                    inv_mu[k] = inv_tab[mu[k]];
                }
                if (!ok) continue;
                uint8_t inv_u12[5];
                idft5(inv_mu, inv_u12);
                if (!check_circ5_r12_nonzero(inv_u12)) continue;

                BaseU12 *b = &BASES[N_BASES++];
                for (int d = 0; d < 5; d++) {
                    b->u12[d] = u12[d];
                    b->u11_0[d] = (d == 0) ? (u12[0] ^ 1) : u12[d];
                }
            }
        }
    }
    printf("Precomputed BASES: %d / %d Hermitian circulants U_12 passing D23b r=1..5 pure-block sieve\n",
           N_BASES, 15 * 255 * 255);
}

static inline int assemble_u(const BaseU12 *b, const uint8_t k_vec[5], uint8_t U[10][10]) {
    uint8_t u11[5], u22[5];
    conv5(k_vec, b->u11_0, u11);
    if (!check_circ5_r12_nonzero(u11)) return 0;
    for (int d = 0; d < 5; d++) u22[d] = conj_tab[u11[(5 - d) % 5]];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            U[5 + i][5 + j] = u22[d];
            U[i][5 + j] = b->u12[d];
            U[5 + i][j] = b->u12[d];
        }
    return 1;
}

static inline uint8_t eval_orb4(const uint8_t D2[45][45], const Orb4 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *rb = D2[o->rp_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->cp_bot;
    return mul_tab[rt[ct[0]]][rb[cb[0]]] ^ mul_tab[rt[ct[1]]][rb[cb[1]]]
         ^ mul_tab[rt[ct[2]]][rb[cb[2]]] ^ mul_tab[rt[ct[3]]][rb[cb[3]]]
         ^ mul_tab[rt[ct[4]]][rb[cb[4]]] ^ mul_tab[rt[ct[5]]][rb[cb[5]]];
}

static inline uint8_t eval_orb5_lazy(const uint8_t U[10][10], const uint8_t D2[45][45], const Orb5 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *ur = U[o->r2];
    const uint8_t *d2r = D2[o->rp34];
    const uint8_t *ct = o->cp_top;
    uint8_t s = 0;
    for (int k = 0; k < 10; k++) {
        uint8_t rb = mul_tab[ur[o->c_a[k]]][d2r[o->cp_bc[k]]]
                   ^ mul_tab[ur[o->c_b[k]]][d2r[o->cp_ac[k]]]
                   ^ mul_tab[ur[o->c_c[k]]][d2r[o->cp_ab[k]]];
        s ^= mul_tab[rt[ct[k]]][rb];
    }
    return s;
}

static inline uint8_t eval_orb5(const uint8_t D2[45][45], const uint8_t D3[120][120], const Orb5 *o) {
    const uint8_t *rt = D2[o->rp_top];
    const uint8_t *rb = D3[o->rt_bot];
    const uint8_t *ct = o->cp_top;
    const uint8_t *cb = o->ct_bot;
    uint8_t s = 0;
    for (int k = 0; k < 10; k++) s ^= mul_tab[rt[ct[k]]][rb[cb[k]]];
    return s;
}

static void eval_g40_char2(const uint8_t U[10][10], int cap_r12, int cap_sub, int cap_tot,
                           int *out_r12, int *out_sub, int *out_ext) {
    int b_sub = 0, b_ext = 0, b_r12 = 0;

    for (int i = 0; i < n_orbs2_sub; i++) {
        const Orb2 *o = &orbs2_sub[i];
        if ((mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]] ^ mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]) == 0) {
            b_sub++;
            if (++b_r12 > cap_r12 || b_sub > cap_sub) { *out_r12 = b_r12; *out_sub = 999; *out_ext = 9999; return; }
        }
    }
    for (int i = 0; i < n_orbs2_ext; i++) {
        const Orb2 *o = &orbs2_ext[i];
        if ((mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]] ^ mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]) == 0) {
            b_ext++;
            if (++b_r12 > cap_r12) { *out_r12 = b_r12; *out_sub = 999; *out_ext = 9999; return; }
        }
    }
    *out_r12 = b_r12;

    uint8_t D2[45][45];
    for (int k = 0; k < n_z5_pairs; k++) {
        int rp = z5_pairs[k].rp, cp = z5_pairs[k].cp;
        int r0 = pairs[rp][0], r1 = pairs[rp][1];
        int c0 = pairs[cp][0], c1 = pairs[cp][1];
        uint8_t d = mul_tab[U[r0][c0]][U[r1][c1]] ^ mul_tab[U[r0][c1]][U[r1][c0]];
        for (int s = 0; s < 5; s++) {
            D2[pair_shift[rp][s]][pair_shift[cp][s]] = d;
        }
    }

    for (int i = 0; i < n_orbs3_sub; i++) {
        const Orb3 *o = &orbs3_sub[i];
        const uint8_t *ur = U[o->r0], *d2r = D2[o->rp_bot];
        if ((mul_tab[ur[o->c0]][d2r[o->cp12]] ^ mul_tab[ur[o->c1]][d2r[o->cp02]] ^ mul_tab[ur[o->c2]][d2r[o->cp01]]) == 0)
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

    if (cap_tot < 0) { *out_ext = 9999; return; }
    int max_ext = cap_tot - b_sub;
    if (b_ext > max_ext) { *out_ext = 9999; return; }

    for (int i = 0; i < n_orbs3_ext; i++) {
        const Orb3 *o = &orbs3_ext[i];
        const uint8_t *ur = U[o->r0], *d2r = D2[o->rp_bot];
        if ((mul_tab[ur[o->c0]][d2r[o->cp12]] ^ mul_tab[ur[o->c1]][d2r[o->cp02]] ^ mul_tab[ur[o->c2]][d2r[o->cp01]]) == 0)
            if (++b_ext > max_ext) { *out_ext = b_ext; return; }
    }
    for (int i = 0; i < n_orbs4_ext; i++) {
        if (eval_orb4(D2, &orbs4_ext[i]) == 0)
            if (++b_ext > max_ext) { *out_ext = b_ext; return; }
    }

    uint8_t D3[120][120];
    for (int k = 0; k < n_z5_triples; k++) {
        const Triple3 *tr = &z5_triples[k];
        const uint8_t *ur = U[tr->r0], *d2r = D2[tr->rp_bot];
        uint8_t d = mul_tab[ur[tr->c0]][d2r[tr->cp12]] ^ mul_tab[ur[tr->c1]][d2r[tr->cp02]] ^ mul_tab[ur[tr->c2]][d2r[tr->cp01]];
        int rt = tr->rt, ct = tr->ct;
        for (int s = 0; s < 5; s++) {
            D3[triple_shift[rt][s]][triple_shift[ct][s]] = d;
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

static inline int compute_score(int b_r12, int b_sub, int b_ext) {
    if (b_r12 > 0) return 200000 + b_r12 * 10000 + b_sub * 100;
    if (b_sub > 2 || b_ext > 4793) return 50000 + b_sub * 100;
    int tot = b_sub + b_ext;
    return tot * 8 + b_sub;
}

static void *worker(void *arg) {
    int tid = (int)(uintptr_t)arg;
    uint64_t rng = 0x9e3779b97f4a7c15ULL ^ ((uint64_t)(tid + 1) * 0xbf58476d1ce4e5b9ULL) ^ (uint64_t)time(NULL);
    uint8_t U[10][10];
    uint64_t local_evals = 0;

    while (!found) {
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        int bidx = (int)(rng % N_BASES);
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        int kidx = (int)(rng % N_KTOT);
        if (!assemble_u(&BASES[bidx], K_TAB[kidx], U)) continue;

        int cur_r12, cur_sub, cur_ext;
        eval_g40_char2(U, 128, 177, 4970, &cur_r12, &cur_sub, &cur_ext);
        local_evals++;
        int cur_score = compute_score(cur_r12, cur_sub, cur_ext);

        int best_b = bidx, best_k = kidx, best_score = cur_score;
        int plateau = 0;

        for (int step = 0; step < 200 && !found; step++) {
            int improved = 0;
            /* Sweep 512 random K_TAB dressings on current base */
            for (int ks = 0; ks < 512; ks++) {
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                int nk = (int)(rng % N_KTOT);
                if (!assemble_u(&BASES[bidx], K_TAB[nk], U)) continue;
                int r12_cap = cur_r12;
                int sub_cap = (cur_r12 > 0) ? 177 : ((cur_sub <= 2) ? 2 : cur_sub);
                int tot_cap = (cur_r12 == 0 && cur_sub <= 2) ? (cur_sub + cur_ext) : -1;
                int b_r12 = 999, b_sub = 999, b_ext = 9999;
                eval_g40_char2(U, r12_cap, sub_cap, tot_cap, &b_r12, &b_sub, &b_ext);
                local_evals++;
                if (b_r12 > r12_cap || b_sub > sub_cap) continue;
                if (tot_cap >= 0 && (b_sub + b_ext) > tot_cap) continue;
                int sc = compute_score(b_r12, b_sub, b_ext);
                if (sc < cur_score) {
                    cur_score = sc; cur_r12 = b_r12; cur_sub = b_sub; cur_ext = b_ext;
                    kidx = nk; improved = 1;
                }
            }

            /* Sweep 256 random BASES with current K */
            for (int bs = 0; bs < 256; bs++) {
                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                int nb = (int)(rng % N_BASES);
                if (!assemble_u(&BASES[nb], K_TAB[kidx], U)) continue;
                int r12_cap = cur_r12;
                int sub_cap = (cur_r12 > 0) ? 177 : ((cur_sub <= 2) ? 2 : cur_sub);
                int tot_cap = (cur_r12 == 0 && cur_sub <= 2) ? (cur_sub + cur_ext) : -1;
                int b_r12 = 999, b_sub = 999, b_ext = 9999;
                eval_g40_char2(U, r12_cap, sub_cap, tot_cap, &b_r12, &b_sub, &b_ext);
                local_evals++;
                if (b_r12 > r12_cap || b_sub > sub_cap) continue;
                if (tot_cap >= 0 && (b_sub + b_ext) > tot_cap) continue;
                int sc = compute_score(b_r12, b_sub, b_ext);
                if (sc < cur_score) {
                    cur_score = sc; cur_r12 = b_r12; cur_sub = b_sub; cur_ext = b_ext;
                    bidx = nb; improved = 1;
                }
            }

            /* If elite base (r12 == 0 && sub <= 1), sweep 4096 more K dressings */
            if (cur_r12 == 0 && cur_sub <= 1) {
                for (int ks = 0; ks < 4096; ks++) {
                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                    int nk = (int)(rng % N_KTOT);
                    if (!assemble_u(&BASES[bidx], K_TAB[nk], U)) continue;
                    int b_r12 = 999, b_sub = 999, b_ext = 9999;
                    int tot_cap = cur_sub + cur_ext;
                    eval_g40_char2(U, 0, 1, tot_cap, &b_r12, &b_sub, &b_ext);
                    local_evals++;
                    if (b_r12 == 0 && b_sub <= 1 && (b_sub + b_ext) <= tot_cap) {
                        int sc = compute_score(0, b_sub, b_ext);
                        if (sc < cur_score) {
                            cur_score = sc; cur_sub = b_sub; cur_ext = b_ext;
                            kidx = nk; improved = 1;
                        }
                    }
                }
            }

            if (cur_r12 == 0 && cur_sub <= 4) {
                if (assemble_u(&BASES[bidx], K_TAB[kidx], U)) {
                    eval_g40_char2(U, 0, 177, 4970, &cur_r12, &cur_sub, &cur_ext);
                    int tot = cur_sub + cur_ext;
                    if (tot < global_best_tot || (tot == global_best_tot && cur_sub < global_best_sub)) {
                        pthread_mutex_lock(&lock);
                        if (tot < global_best_tot || (tot == global_best_tot && cur_sub < global_best_sub)) {
                            if (tot < global_best_tot) global_best_tot = tot;
                            if (cur_sub < global_best_sub) global_best_sub = cur_sub;
                            uint8_t u11[5];
                            conv5(K_TAB[kidx], BASES[bidx].u11_0, u11);
                            printf("[D29-Char2 T%d] r12=0 | sub=%d/177 | ext=%d/4793 | TOTAL=%d/4970 (%.4f%%) bidx=%d kidx=%d u11=[%d,%d,%d,%d,%d] u12=[%d,%d,%d,%d,%d]\n",
                                   tid, cur_sub, cur_ext, tot, 100.0 * (4970 - tot) / 4970.0,
                                   bidx, kidx,
                                   u11[0], u11[1], u11[2], u11[3], u11[4],
                                   BASES[bidx].u12[0], BASES[bidx].u12[1], BASES[bidx].u12[2], BASES[bidx].u12[3], BASES[bidx].u12[4]);
                            fflush(stdout);
                            if (tot == 0) found = 1;
                        }
                        pthread_mutex_unlock(&lock);
                    }
                }
            }

            if (cur_score < best_score) {
                best_score = cur_score; best_b = bidx; best_k = kidx; plateau = 0;
            } else {
                plateau++;
            }
            if (!improved && plateau >= 3) break;
        }
    }

    pthread_mutex_lock(&lock);
    total_evals += local_evals;
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main(void) {
    init_gf256();
    init_combinatorics();
    build_all_tables();
    init_ktab();
    init_bases();

    pthread_t th[8];
    for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker, (void*)(uintptr_t)i);
    for (int s = 0; s < 12 && !found; s++) {
        struct timespec ts = {1, 0};
        nanosleep(&ts, NULL);
    }
    found = 1;
    for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
    printf("Total Theorem D29 char-2 matrices evaluated in 12s: %llu (%.1f matrices/sec)\n",
           (unsigned long long)total_evals, total_evals / 12.0);
    return 0;
}
