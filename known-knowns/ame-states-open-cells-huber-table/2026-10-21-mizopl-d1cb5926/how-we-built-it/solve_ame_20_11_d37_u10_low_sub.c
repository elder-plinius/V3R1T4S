#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

/*
 * Theorem D33B (100% Exhaustive Sweep of the Disjoint QNR Coset U_12 = beta * H_0 in G_40 over F_121):
 *   In F_121 = F_11[alpha]/(alpha^2 - 7), primitive root g = 14 has beta = g^5 = 74 (8 + 6*alpha)
 *   with norm(beta) = beta * conj(beta) = 10 == -1 (mod 11) in QNR_11 = {2, 6, 7, 8, 10},
 *   and omega_0 = conj(beta)/beta = 91 in U(1, F_121).
 *   For any Hermitian circulant H_0 in C_5(F_121) (H_0^dagger = H_0), setting
 *     U_12 = beta * H_0,   U_21 = -U_12^dagger = -omega_0 * U_12
 *   preserves the entire G_40 minor-orbit group (4,970 orbits: 177 sub + 4,793 ext) while flipping
 *   every norm mu_k(U_12) * conj(mu_{5-k}(U_12)) = -mu_k(H_0)^2 into the QNR coset (completely
 *   disjoint from mode=0 and mode=1 swept in Theorem D33).
 */

#define P 11
#define Q2 121
#define NONRES 7
#define BETA 74
#define OMEGA0 91

static uint8_t mul_tab[121][121], add_tab[121][121], sub_tab[121][121], neg_tab[121], inv_tab[121], conj_tab[121];
static uint8_t norm_root[11];
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

    for (int w = 1; w < P; w++) {
        for (int a = 1; a < Q2; a++) {
            if (mul_tab[a][conj_tab[a]] == w) { norm_root[w] = (uint8_t)a; break; }
        }
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

#define N_KTOT (120 * 120)
static uint8_t K_TAB[N_KTOT][5];
static uint8_t MDS_TAB[13000][5];
static int N_MDS = 0;
static uint8_t u1_tab[12];
static uint8_t by_norm[11][12];

static void init_ktab(void) {
    int u1_cnt = 0;
    int norm_cnt[11] = {0};
    for (int a = 1; a < Q2; a++) {
        uint8_t n = mul_tab[a][conj_tab[a]];
        by_norm[n][norm_cnt[n]++] = (uint8_t)a;
        if (n == 1) u1_tab[u1_cnt++] = (uint8_t)a;
    }
    int idx = 0;
    for (int k1 = 1; k1 < Q2; k1++) {
        uint8_t k4 = inv_tab[conj_tab[k1]];
        for (int k2 = 1; k2 < Q2; k2++) {
            uint8_t k3 = inv_tab[conj_tab[k2]];
            uint8_t lam[5] = {1, (uint8_t)k1, (uint8_t)k2, k3, k4};
            idft5(lam, K_TAB[idx]);
            if (check_circ5_r12_nonzero(K_TAB[idx])) {
                memcpy(MDS_TAB[N_MDS++], K_TAB[idx], 5);
            }
            idx++;
        }
    }
    printf("Precomputed K_TAB: %d projective unitary circulants (%d fully MDS 5x5 circulants)\n", idx, N_MDS);
}

typedef struct {
    uint8_t A[5];
} CandA;

typedef struct {
    uint8_t B[5];
} CandB;

typedef struct {
    uint8_t rho1, rho2, w0, w1, w2;
    int nA, nB;
    CandA listA[144];
    CandB listB[1728];
} BucketD37A;

static BucketD37A *BUCKETS = NULL;
static int N_BUCKETS = 0;

static void init_buckets_d37a(void) {
    int max_b = 1200;
    BUCKETS = malloc(sizeof(BucketD37A) * max_b);
    /* Non-shift (rho1, rho2) pairs in (F_11^*)^2 \ {(3^s, 9^s)}: */
    static const uint8_t bad_r1[5] = {1, 3, 9, 5, 4};
    static const uint8_t bad_r2[5] = {1, 9, 5, 4, 3};
    for (int r1 = 1; r1 < P; r1++) {
        for (int r2 = 1; r2 < P; r2++) {
            int is_shift = 0;
            for (int s = 0; s < 5; s++)
                if (r1 == bad_r1[s] && r2 == bad_r2[s]) is_shift = 1;
            if (is_shift) continue;
            /* Canonical under (r1, r2) <-> (r1^-1, r2^-1) */
            int ir1 = inv_tab[r1], ir2 = inv_tab[r2];
            if (r1 * 16 + r2 > ir1 * 16 + ir2) continue;

            for (int w0 = 1; w0 <= 5; w0++) {
                int v0 = modp(1 - w0);
                if (!v0) continue;
                for (int w1 = 1; w1 < P; w1++) {
                    int v1 = modp(ir1 - w1);
                    if (!v1 || w1 > v1) continue;
                    for (int w2 = 1; w2 < P; w2++) {
                        int v2 = modp(ir2 - w2);
                        if (!v2) continue;
                        if (N_BUCKETS >= max_b) break;

                        BucketD37A *bk = &BUCKETS[N_BUCKETS];
                        bk->rho1 = (uint8_t)r1; bk->rho2 = (uint8_t)r2;
                        bk->w0 = (uint8_t)w0; bk->w1 = (uint8_t)w1; bk->w2 = (uint8_t)w2;
                        bk->nA = 0; bk->nB = 0;

                        uint8_t l0 = by_norm[w0][0];
                        for (int i1 = 0; i1 < 12; i1++) {
                            uint8_t l1 = by_norm[w1][i1];
                            uint8_t l4 = mul_tab[r1][l1];
                            for (int i2 = 0; i2 < 12; i2++) {
                                uint8_t l2 = by_norm[w2][i2];
                                uint8_t l3 = mul_tab[r2][l2];
                                uint8_t lam[5] = {l0, l1, l2, l3, l4};
                                uint8_t A[5], inv_lam[5], invA[5];
                                idft5(lam, A);
                                if (!check_circ5_r12_nonzero(A)) continue;
                                for (int k = 0; k < 5; k++) inv_lam[k] = inv_tab[lam[k]];
                                idft5(inv_lam, invA);
                                if (!check_circ5_r12_nonzero(invA)) continue;
                                memcpy(bk->listA[bk->nA++].A, A, 5);
                            }
                        }
                        if (bk->nA == 0) continue;

                        for (int j0 = 0; j0 < 12; j0++) {
                            uint8_t m0 = by_norm[v0][j0];
                            for (int j1 = 0; j1 < 12; j1++) {
                                uint8_t m1 = by_norm[v1][j1];
                                uint8_t m4 = mul_tab[r1][m1];
                                for (int j2 = 0; j2 < 12; j2++) {
                                    uint8_t m2 = by_norm[v2][j2];
                                    uint8_t m3 = mul_tab[r2][m2];
                                    uint8_t mu[5] = {m0, m1, m2, m3, m4};
                                    uint8_t B[5], inv_mu[5], invB[5];
                                    idft5(mu, B);
                                    if (!check_circ5_r12_nonzero(B)) continue;
                                    for (int k = 0; k < 5; k++) inv_mu[k] = inv_tab[mu[k]];
                                    idft5(inv_mu, invB);
                                    if (!check_circ5_r12_nonzero(invB)) continue;
                                    memcpy(bk->listB[bk->nB++].B, B, 5);
                                }
                            }
                        }
                        if (bk->nB > 0) N_BUCKETS++;
                    }
                }
            }
        }
    }
    printf("Precomputed D37A Bi-Spectral Buckets: %d\n", N_BUCKETS);
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

/*
 * Theorem D37 non-reversal block swap W_0 = (1, 1, 0, 0):
 *   w = 1 swaps row blocks 0<->1 and col blocks 0<->1 WITHOUT reversing idx!
 *   r_tr = 1 swaps rows<->cols AND reverses idx -> 4-idx!
 */
static uint32_t apply_g20_w0(uint32_t m, int s, int w, int r_tr) {
    uint32_t out = 0;
    for (int i = 0; i < 5; i++) {
        int r0 = (m >> i) & 1, r1 = (m >> (i + 5)) & 1;
        int c0 = (m >> (i + 10)) & 1, c1 = (m >> (i + 15)) & 1;
        int nr0 = r0, nr1 = r1, nc0 = c0, nc1 = c1;
        int idx = i;
        if (w) {
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

static uint32_t canon_g10_d37a(uint32_t m) {
    uint32_t best = m;
    for (int s = 0; s < 5; s++)
        for (int w = 0; w < 2; w++) {
            uint32_t g = apply_g20_w0(m, s, w, 0);
            if (g < best) best = g;
        }
    return best;
}

static uint32_t canon_g20_d37a_r5(uint32_t m) {
    uint32_t c1 = canon_g10_d37a(m);
    uint32_t c2 = canon_g10_d37a((~m) & 0xFFFFFu);
    return (c1 < c2) ? c1 : c2;
}

static uint32_t canon_g20_d37b(uint32_t m) {
    uint32_t best = m;
    for (int s = 0; s < 5; s++)
        for (int w = 0; w < 2; w++)
            for (int r = 0; r < 2; r++) {
                uint32_t g = apply_g20_w0(m, s, w, r);
                if (g < best) best = g;
            }
    return best;
}

static uint32_t canon_g40_d37b_r5(uint32_t m) {
    uint32_t c1 = canon_g20_d37b(m);
    uint32_t c2 = canon_g20_d37b((~m) & 0xFFFFFu);
    return (c1 < c2) ? c1 : c2;
}

typedef struct { uint8_t r0, c0; } Orb1;
typedef struct { uint8_t rp, cp, r0, r1, c0, c1; } Orb2;
typedef struct { uint8_t r0, r1, r2, rp_bot, c0, c1, c2, cp12, cp02, cp01; } Orb3;
typedef struct { uint8_t rp_top, rp_bot, cp_top[6], cp_bot[6]; } Orb4;
typedef struct {
    uint8_t rp_top, rt_bot;
    uint8_t cp_top[10], ct_bot[10];
    uint8_t r2, rp34;
    uint8_t c_a[10], c_b[10], c_c[10];
    uint8_t cp_bc[10], cp_ac[10], cp_ab[10];
} Orb5;

static Orb1 orbs1_sub[32],   orbs1_ext[32];   static int n_orbs1_sub = 0, n_orbs1_ext = 0;
static Orb2 orbs2_sub[128],  orbs2_ext[512];  static int n_orbs2_sub = 0, n_orbs2_ext = 0;
static Orb3 orbs3_sub[256],  orbs3_ext[2048]; static int n_orbs3_sub = 0, n_orbs3_ext = 0;
static Orb4 orbs4_sub[256],  orbs4_ext[5000]; static int n_orbs4_sub = 0, n_orbs4_ext = 0;
static Orb5 orbs5_sub[512],  orbs5_ext[4000]; static int n_orbs5_sub = 0, n_orbs5_ext = 0;

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

static void build_z5_tables(void) {
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
}

static void build_orbits_mode(int mode_d37b) {
    n_orbs1_sub = n_orbs1_ext = 0;
    n_orbs2_sub = n_orbs2_ext = 0;
    n_orbs3_sub = n_orbs3_ext = 0;
    n_orbs4_sub = n_orbs4_ext = 0;
    n_orbs5_sub = n_orbs5_ext = 0;

    for (int r = 1; r <= 5; r++) {
        for (uint32_t rm = 1; rm < 1024; rm++) {
            if (__builtin_popcount(rm) != r) continue;
            for (uint32_t cm = 1; cm < 1024; cm++) {
                if (__builtin_popcount(cm) != r) continue;
                uint32_t m = rm | (cm << 10);
                if (!mode_d37b) {
                    if (r < 5 && canon_g10_d37a(m) != m) continue;
                    if (r == 5 && canon_g20_d37a_r5(m) != m) continue;
                } else {
                    if (r < 5 && canon_g20_d37b(m) != m) continue;
                    if (r == 5 && canon_g40_d37b_r5(m) != m) continue;
                }
                uint8_t rw[5], cl[5];
                int ri = 0, ci = 0;
                for (int i = 0; i < 10; i++) {
                    if ((rm >> i) & 1) rw[ri++] = i;
                    if ((cm >> i) & 1) cl[ci++] = i;
                }
                uint32_t m_comp = (~m) & 0xFFFFFu;
                int is_sub = 0;
                if (!mode_d37b) {
                    /* D37A: w=1 has b=1; at r=5, w=1 * J_comp has b = 1^1 = 0! */
                    for (int s = 0; s < 5; s++) {
                        if (apply_g20_w0(m, s, 1, 0) == m) { is_sub = 1; break; }
                        if (r == 5 && apply_g20_w0(m, s, 0, 0) == m_comp) { is_sub = 1; break; }
                    }
                } else {
                    /* D37B: w and r_tr both have b=0; at r=5, g * J_comp has b=1! */
                    if (r == 5) {
                        for (int s = 0; s < 5; s++)
                            for (int w = 0; w < 2; w++)
                                for (int rt = 0; rt < 2; rt++)
                                    if (apply_g20_w0(m, s, w, rt) == m_comp) is_sub = 1;
                    }
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
                    o->r0 = rw[0]; o->r1 = rw[1]; o->r2 = rw[2];
                    o->rp_bot = pair_id[rw[1]][rw[2]];
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
    int tot_sub = n_orbs1_sub + n_orbs2_sub + n_orbs3_sub + n_orbs4_sub + n_orbs5_sub;
    int tot_ext = n_orbs1_ext + n_orbs2_ext + n_orbs3_ext + n_orbs4_ext + n_orbs5_ext;
    printf("[Mode %s] sub=%d [%d,%d,%d,%d,%d] | ext=%d [%d,%d,%d,%d,%d] | TOTAL=%d\n",
           mode_d37b ? "D37B-Had40" : "D37A-Conj20",
           tot_sub, n_orbs1_sub, n_orbs2_sub, n_orbs3_sub, n_orbs4_sub, n_orbs5_sub,
           tot_ext, n_orbs1_ext, n_orbs2_ext, n_orbs3_ext, n_orbs4_ext, n_orbs5_ext,
           tot_sub + tot_ext);
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

static void eval_d37_fast(const uint8_t U[10][10], int cap_sub, int cap_tot,
                          int *out_sub, int *out_ext, int *out_r2_ok) {
    int b_sub = 0, b_ext = 0;
    *out_r2_ok = 0;

    for (int i = 0; i < n_orbs2_sub; i++) {
        const Orb2 *o = &orbs2_sub[i];
        if (sub_tab[mul_tab[U[o->r0][o->c0]][U[o->r1][o->c1]]][mul_tab[U[o->r0][o->c1]][U[o->r1][o->c0]]] == 0) {
            *out_sub = 999; *out_ext = 9999; return;
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

    for (int i = 0; i < n_orbs2_ext; i++) {
        const Orb2 *o = &orbs2_ext[i];
        if (D2[o->rp][o->cp] == 0) {
            *out_sub = 999; *out_ext = 9999; return;
        }
    }
    *out_r2_ok = 1;

    for (int i = 0; i < n_orbs3_sub; i++) {
        if (eval_orb3_direct(U, &orbs3_sub[i]) == 0) {
            if (++b_sub > cap_sub) { *out_sub = 999; *out_ext = 9999; return; }
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

static int next_bidx = 0;
static int global_best_sub = 999;
static int global_best_tot = 9999;
static uint64_t total_valid_pairs = 0;
static uint64_t sub_hist[16];
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static int MAX_CAP_B = 600;

static void *worker_d37a(void *arg) {
    int tid = (int)(uintptr_t)arg;
    uint8_t U[10][10];
    uint64_t local_valid = 0;
    uint64_t local_hist[16] = {0};

    while (1) {
        int bidx = __sync_fetch_and_add(&next_bidx, 1);
        if (bidx >= N_BUCKETS) break;
        const BucketD37A *bk = &BUCKETS[bidx];

        for (int ia = 0; ia < bk->nA; ia++) {
            const uint8_t *A = bk->listA[ia].A;
            for (int ib = 0; ib < bk->nB; ib++) {
                const uint8_t *B = bk->listB[ib].B;
                for (int i = 0; i < 5; i++) {
                    for (int j = 0; j < 5; j++) {
                        int d = (j - i + 5) % 5;
                        U[i][j] = A[d];
                        U[i][5 + j] = B[d];
                        U[5 + i][j] = neg_tab[conj_tab[B[d]]];
                        U[5 + i][5 + j] = conj_tab[A[d]];
                    }
                }
                int b_sub = 999, b_ext = 9999, r2_ok = 0;
                eval_d37_fast(U, 3, global_best_tot, &b_sub, &b_ext, &r2_ok);
                if (r2_ok) local_valid++;
                if (b_sub <= 3) {
                    local_hist[b_sub]++;
                    if (b_sub < global_best_sub || (b_sub + b_ext) < global_best_tot) {
                        int full_sub = 999, full_ext = 9999, dummy = 0;
                        eval_d37_fast(U, 25, 9325, &full_sub, &full_ext, &dummy);
                        int tot = full_sub + full_ext;
                        pthread_mutex_lock(&lock);
                        if (full_sub < global_best_sub || tot < global_best_tot) {
                            if (full_sub < global_best_sub) global_best_sub = full_sub;
                            if (tot < global_best_tot) global_best_tot = tot;
                            printf("[D37A-Conj20 T%d] sub=%d/25 | ext=%d/9300 | TOTAL=%d/9325 (%.4f%%) bidx=%d/%d A=[%d,%d,%d,%d,%d] B=[%d,%d,%d,%d,%d]\n",
                                   tid, full_sub, full_ext, tot, 100.0 * (9325 - tot) / 9325.0,
                                   bidx, N_BUCKETS,
                                   A[0], A[1], A[2], A[3], A[4],
                                   B[0], B[1], B[2], B[3], B[4]);
                            fflush(stdout);
                        }
                        pthread_mutex_unlock(&lock);
                    }
                }
            }
        }
    }

    pthread_mutex_lock(&lock);
    total_valid_pairs += local_valid;
    for (int i = 0; i <= 3; i++) sub_hist[i] += local_hist[i];
    pthread_mutex_unlock(&lock);
    return NULL;
}

static void *worker_d37b(void *arg) {
    int tid = (int)(uintptr_t)arg;
    uint8_t U[10][10], A[5], B[5], um[5];
    uint64_t local_valid = 0;
    uint64_t local_hist[16] = {0};

    while (1) {
        int i_up = __sync_fetch_and_add(&next_bidx, 1);
        if (i_up >= MAX_CAP_B) break;
        const uint8_t *up = MDS_TAB[i_up];

        for (int i_um = i_up + 1; i_um < N_MDS; i_um++) {
            const uint8_t *um0 = MDS_TAB[i_um];
            for (int iw = 0; iw < 12; iw++) {
                uint8_t w = u1_tab[iw];
                int ok = 1;
                for (int d = 0; d < 5; d++) {
                    um[d] = mul_tab[w][um0[d]];
                    A[d] = mul_tab[6][add_tab[up[d]][um[d]]];
                    B[d] = mul_tab[6][sub_tab[up[d]][um[d]]];
                    if (!A[d] || !B[d]) { ok = 0; break; }
                }
                if (!ok) continue;
                if (!check_circ5_r12_nonzero(A) || !check_circ5_r12_nonzero(B)) continue;

                for (int i = 0; i < 5; i++) {
                    for (int j = 0; j < 5; j++) {
                        int d = (j - i + 5) % 5;
                        U[i][j] = A[d];
                        U[5 + i][5 + j] = A[d];
                        U[i][5 + j] = B[d];
                        U[5 + i][j] = B[d];
                    }
                }
                int b_sub = 999, b_ext = 9999, r2_ok = 0;
                eval_d37_fast(U, 3, global_best_tot, &b_sub, &b_ext, &r2_ok);
                if (r2_ok) local_valid++;
                if (b_sub <= 3) {
                    local_hist[b_sub]++;
                    if (b_sub < global_best_sub || (b_sub + b_ext) < global_best_tot) {
                        int full_sub = 999, full_ext = 9999, dummy = 0;
                        eval_d37_fast(U, 178, 4970, &full_sub, &full_ext, &dummy);
                        int tot = full_sub + full_ext;
                        pthread_mutex_lock(&lock);
                        if (full_sub < global_best_sub || tot < global_best_tot) {
                            if (full_sub < global_best_sub) global_best_sub = full_sub;
                            if (tot < global_best_tot) global_best_tot = tot;
                            printf("[D37B-Had40 T%d] sub=%d/178 | ext=%d/4792 | TOTAL=%d/4970 (%.4f%%) i_up=%d i_um=%d iw=%d A=[%d,%d,%d,%d,%d] B=[%d,%d,%d,%d,%d]\n",
                                   tid, full_sub, full_ext, tot, 100.0 * (4970 - tot) / 4970.0,
                                   i_up, i_um, iw,
                                   A[0], A[1], A[2], A[3], A[4],
                                   B[0], B[1], B[2], B[3], B[4]);
                            fflush(stdout);
                        }
                        pthread_mutex_unlock(&lock);
                    }
                }
            }
        }
    }

    pthread_mutex_lock(&lock);
    total_valid_pairs += local_valid;
    for (int i = 0; i <= 3; i++) sub_hist[i] += local_hist[i];
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main(void) {
    struct timespec t0, t1, t2;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    init_gf121();
    init_combinatorics();
    build_z5_tables();
    init_ktab();
    init_buckets_d37a();

    printf("\n--- STAGE 1: Theorem D37A (Conjugate-Block Bi-Spectral Unitary, sub=25 [0,5,0,20,0]) ---\n");
    build_orbits_mode(0);
    next_bidx = 0; global_best_sub = 999; global_best_tot = 9999; total_valid_pairs = 0;
    memset(sub_hist, 0, sizeof(sub_hist));
    pthread_t th[8];
    for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker_d37a, (void*)(uintptr_t)i);
    for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt1 = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("=== STAGE 1 (D37A) COMPLETE in %.2f s | r<=2 valid pairs: %llu ===\n", dt1, (unsigned long long)total_valid_pairs);
    for (int i = 0; i <= 3; i++)
        printf("  D37A sub = %d / 25 : %llu pairs\n", i, (unsigned long long)sub_hist[i]);
    printf("  D37A Best: sub = %d / 25, TOTAL = %d / 9325\n", global_best_sub, global_best_tot);

    printf("\n--- STAGE 2: Theorem D37B (Order-40 Hadamard-Unitary Block-Circulant, sub=178 [0,0,0,0,178]) ---\n");
    build_orbits_mode(1);
    next_bidx = 0; global_best_sub = 999; global_best_tot = 9999; total_valid_pairs = 0;
    memset(sub_hist, 0, sizeof(sub_hist));
    MAX_CAP_B = 200;
    for (int i = 0; i < 8; i++) pthread_create(&th[i], NULL, worker_d37b, (void*)(uintptr_t)i);
    for (int i = 0; i < 8; i++) pthread_join(th[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t2);
    double dt2 = (t2.tv_sec - t1.tv_sec) + 1e-9 * (t2.tv_nsec - t1.tv_nsec);
    printf("=== STAGE 2 (D37B) COMPLETE in %.2f s | r<=2 valid pairs: %llu ===\n", dt2, (unsigned long long)total_valid_pairs);
    for (int i = 0; i <= 3; i++)
        printf("  D37B sub = %d / 178 : %llu pairs\n", i, (unsigned long long)sub_hist[i]);
    printf("  D37B Best: sub = %d / 178, TOTAL = %d / 4970\n", global_best_sub, global_best_tot);
    return 0;
}
