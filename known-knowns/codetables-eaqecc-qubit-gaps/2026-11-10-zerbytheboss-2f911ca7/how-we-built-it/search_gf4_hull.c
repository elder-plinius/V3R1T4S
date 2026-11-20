#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/*
 * GF(4) = {0, 1, 2=w, 3=w^2}, w^2 = w + 1.
 * Normal basis map phi(u) = (x | z) where u = x*w + z*w^2:
 *   u=0 -> (0,0), u=1=w+w^2 -> (1,1), u=2=w -> (1,0), u=3=w^2 -> (0,1).
 * Under phi, Tr(u * conj(v)) == x*z' ^ z*x' (exact binary symplectic inner product!),
 * and Hamming weight over GF(4) == binary symplectic weight!
 *
 * Bit-sliced representation of u in GF(4)^n (n <= 32):
 *   x bitmask = coefficient of w, z bitmask = coefficient of w^2!
 *Wait: let's see how fast bit-sliced (x, z) arithmetic over GF(4)^n is in C!
 *   - Addition u + v: (ux ^ vx, uz ^ vz) -> 2 instructions!
 *   - Multiply by w (since w * (x*w + z*w^2) = x*w^2 + z*(1) = x*w^2 + z*(w+w^2) = z*w + (x^z)*w^2):
 *       mul_w(x, z) = (z, x ^ z) -> 1 XOR!!
 *   - Multiply by w^2:
 *       mul_w2(x, z) = (x ^ z, x) -> 1 XOR!!
 *   - Symplectic weight == GF(4) Hamming weight:
 *       __builtin_popcount(ux | uz) -> 1 instruction!!
 *   - Hermitian inner product <u, v>_h in {0, 1=w+w^2, 2=w, 3=w^2}:
 *       We know Tr(u * conj(v)) = popcount((ux & vz) ^ (uz & vx)) & 1
 *       and Tr(w * u * conj(v)) = Tr(mul_w(u) * conj(v)) = popcount((uz & vz) ^ ((ux^uz) & vx)) & 1!
 *       Let t0 = Tr(u * conj(v)), t1 = Tr(w * u * conj(v)).
 *       Let alpha = a*w + b*w^2 = <u, v>_h:
 *         t0 = Tr(alpha) = a ^ b
 *         t1 = Tr(w * alpha) = Tr(a*w^2 + b*1) = a
 *       Therefore: a = t1, b = t0 ^ t1!
 *       Check: if u=v=(1,0) (which is w), u*conj(v) = w*w^2 = 1 = 1*w + 1*w^2.
 *         t0 = pop(0) = 0, t1 = pop((0) ^ (1&1)) = 1 => a = 1, b = 1 => 1*w + 1*w^2 = 1! EXACT!!
 */

static uint64_t rng_state = 0x243f6a8885a308d3ULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return x;
}

static inline void mul_gf4_vec(int scalar_ab, uint32_t ux, uint32_t uz, uint32_t *ox, uint32_t *oz) {
    /* scalar_ab: 0=0, 1=w (1,0), 2=w^2 (0,1), 3=1=w+w^2 (1,1) */
    switch (scalar_ab) {
        case 0: *ox = 0; *oz = 0; break;
        case 1: *ox = uz; *oz = ux ^ uz; break;       /* * w */
        case 2: *ox = ux ^ uz; *oz = ux; break;       /* * w^2 */
        case 3: *ox = ux; *oz = uz; break;            /* * 1 */
    }
}

static inline int mul_gf4_scal(int s1, int s2) {
    /* 0=0, 1=w, 2=w^2, 3=1 */
    static const int tab[4][4] = {
        {0, 0, 0, 0},
        {0, 2, 3, 1},
        {0, 3, 1, 2},
        {0, 1, 2, 3}
    };
    return tab[s1][s2];
}

static inline int inv_gf4_scal(int s) {
    static const int inv[4] = {0, 2, 1, 3};
    return inv[s];
}

static inline int conj_gf4_scal(int s) {
    static const int cj[4] = {0, 2, 1, 3};
    return cj[s];
}

/* Returns <u, v>_h encoded as 0=0, 1=w, 2=w^2, 3=1=w+w^2 */
static inline int herm_ip(uint32_t ux, uint32_t uz, uint32_t vx, uint32_t vz) {
    int t0 = __builtin_popcount((ux & vz) ^ (uz & vx)) & 1;
    int t1 = __builtin_popcount((uz & vz) ^ ((ux ^ uz) & vx)) & 1;
    int a = t1;
    int b = t0 ^ t1;
    return (a ? 1 : 0) | (b ? 2 : 0);
}

static inline int symp_ip(uint32_t ux, uint32_t uz, uint32_t vx, uint32_t vz) {
    return __builtin_popcount((ux & vz) ^ (uz & vx)) & 1;
}

/* Exact unitary reflection/transvection in U(n, GF(4))!
 * - If <g, g>_h == 0 (even weight): T_g(u) = u + <u, g>_h * g  (or w * 0? Wait: Tr(alpha)=0 => alpha in {0, 1}, so u + <u,g>_h * g!)
 * - If <g, g>_h == 3 (i.e. scalar 1, odd weight): R_g(u) = u + w * <u, g>_h * g!
 */
static void apply_unitary(int K, uint32_t gx, uint32_t gz, int odd_mode, uint32_t *cx, uint32_t *cz) {
    int gg = __builtin_popcount(gx | gz) & 1;
    int lam = (gg == 0) ? 3 : (odd_mode ? 2 : 1); /* 3=1 if even weight; 1=w or 2=w^2 if odd weight */
    for (int i = 0; i < K; i++) {
        int ip = herm_ip(cx[i], cz[i], gx, gz);
        if (ip) {
            int sc = mul_gf4_scal(lam, ip);
            uint32_t dx, dz;
            mul_gf4_vec(sc, gx, gz, &dx, &dz);
            cx[i] ^= dx;
            cz[i] ^= dz;
        }
    }
}

static uint32_t EX[1 << 18];
static uint32_t EZ[1 << 18];

/* Enumerate all 4^K vectors of C = span_GF4(c_0..c_{K-1}); skip first 4^l vectors (H_0)! */
static int64_t eval_gf4_code(int K, int l, int d_t, const uint32_t *cx, const uint32_t *cz, int *out_min_d, int *out_bad_idx) {
    EX[0] = 0;
    EZ[0] = 0;
    for (int i = 0; i < K; i++) {
        int step = 1 << (2 * i);
        uint32_t x1 = cx[i], z1 = cz[i];             /* * 1 */
        uint32_t xw = z1, zw = x1 ^ z1;               /* * w */
        uint32_t xw2 = x1 ^ z1, zw2 = x1;             /* * w^2 */
        for (int j = 0; j < step; j++) {
            uint32_t bx = EX[j], bz = EZ[j];
            EX[step + j]     = bx ^ xw;  EZ[step + j]     = bz ^ zw;
            EX[2 * step + j] = bx ^ xw2; EZ[2 * step + j] = bz ^ zw2;
            EX[3 * step + j] = bx ^ x1;  EZ[3 * step + j] = bz ^ z1;
        }
    }
    int start = 1 << (2 * l);
    int total = 1 << (2 * K);
    int min_d = 999;
    int bad_i = -1, seen = 0;
    int64_t pen = 0;
    for (int mask = start; mask < total; mask++) {
        int w = __builtin_popcount(EX[mask] | EZ[mask]);
        if (w < min_d) min_d = w;
        if (w < d_t) {
            seen++;
            if (bad_i < 0 || (xorshift64() % seen) == 0) bad_i = mask;
            int diff = d_t - w;
            pen += (1LL << (3 * diff));
        }
    }
    if (out_min_d) *out_min_d = min_d;
    if (out_bad_idx) *out_bad_idx = bad_i;
    return pen;
}

static int gf4_gram_rank(int k, const uint32_t *wx, const uint32_t *wz) {
    int G[16][16];
    for (int i = 0; i < k; i++)
        for (int j = 0; j < k; j++)
            G[i][j] = herm_ip(wx[i], wz[i], wx[j], wz[j]);
    int rk = 0;
    for (int col = 0; col < k && rk < k; col++) {
        int sel = -1;
        for (int row = rk; row < k; row++) {
            if (G[row][col] != 0) { sel = row; break; }
        }
        if (sel < 0) continue;
        for (int c = 0; c < k; c++) { int t = G[rk][c]; G[rk][c] = G[sel][c]; G[sel][c] = t; }
        int inv = inv_gf4_scal(G[rk][col]);
        for (int c = 0; c < k; c++) G[rk][c] = mul_gf4_scal(G[rk][c], inv);
        for (int row = 0; row < k; row++) {
            if (row != rk && G[row][col] != 0) {
                int f = G[row][col];
                for (int c = 0; c < k; c++) G[row][c] ^= mul_gf4_scal(f, G[rk][c]);
            }
        }
        rk++;
    }
    return rk;
}

/* Compute binary symplectic dual basis of binary span of C (dim 2K -> dual dim 2(n-K)) */
static int compute_bin_dual(int n, int m_bin, const uint32_t *bx, const uint32_t *bz, uint32_t *sx, uint32_t *sz) {
    uint64_t H[64];
    for (int i = 0; i < m_bin; i++) {
        H[i] = ((uint64_t)bz[i]) | (((uint64_t)bx[i]) << n);
    }
    int piv_col[64];
    int rank = 0;
    uint64_t used_piv = 0;
    for (int col = 0; col < 2 * n && rank < m_bin; col++) {
        int sel = -1;
        for (int row = rank; row < m_bin; row++) {
            if ((H[row] >> col) & 1ULL) { sel = row; break; }
        }
        if (sel < 0) continue;
        uint64_t tmp = H[rank]; H[rank] = H[sel]; H[sel] = tmp;
        piv_col[rank] = col;
        used_piv |= (1ULL << col);
        for (int row = 0; row < m_bin; row++) {
            if (row != rank && ((H[row] >> col) & 1ULL)) H[row] ^= H[rank];
        }
        rank++;
    }
    if (rank != m_bin) return 0;
    int ns = 0;
    uint64_t mask_n = (1ULL << n) - 1ULL;
    for (int col = 0; col < 2 * n; col++) {
        if ((used_piv >> col) & 1ULL) continue;
        uint64_t vec = (1ULL << col);
        for (int p = 0; p < rank; p++) {
            if ((H[p] >> col) & 1ULL) vec |= (1ULL << piv_col[p]);
        }
        sx[ns] = (uint32_t)(vec & mask_n);
        sz[ns] = (uint32_t)((vec >> n) & mask_n);
        ns++;
    }
    return ns;
}

/* Compute GF(4) Hermitian dual basis D = C^{perp_h} of dimension n - K */
static int compute_gf4_dual(int n, int K, const uint32_t *cx, const uint32_t *cz, uint32_t *dx, uint32_t *dz) {
    /* A vector v in GF(4)^n is in C^{perp_h} iff it is binary-symplectically orthogonal to c_i and w*c_i!
     * And we can compute D directly by GF(4) RREF on conj(C)! */
    uint8_t M[32][32];
    for (int i = 0; i < K; i++) {
        for (int col = 0; col < n; col++) {
            int x = (cx[i] >> col) & 1U;
            int z = (cz[i] >> col) & 1U;
            int val = (x && z) ? 3 : (x ? 1 : (z ? 2 : 0)); /* 0, 1=w, 2=w^2, 3=1 */
            /* Equation: sum_col conj(c_i[col]) * v[col] = 0 */
            M[i][col] = (uint8_t)conj_gf4_scal(val);
        }
    }
    int piv[32], used[32] = {0}, rk = 0;
    for (int col = 0; col < n && rk < K; col++) {
        int sel = -1;
        for (int row = rk; row < K; row++) {
            if (M[row][col] != 0) { sel = row; break; }
        }
        if (sel < 0) continue;
        for (int c = 0; c < n; c++) { uint8_t t = M[rk][c]; M[rk][c] = M[sel][c]; M[sel][c] = t; }
        int inv = inv_gf4_scal(M[rk][col]);
        for (int c = 0; c < n; c++) M[rk][c] = (uint8_t)mul_gf4_scal(M[rk][c], inv);
        for (int row = 0; row < K; row++) {
            if (row != rk && M[row][col] != 0) {
                int f = M[row][col];
                for (int c = 0; c < n; c++) M[row][c] ^= (uint8_t)mul_gf4_scal(f, M[rk][c]);
            }
        }
        piv[rk] = col;
        used[col] = 1;
        rk++;
    }
    if (rk != K) return 0;
    int nd = 0;
    for (int col = 0; col < n; col++) {
        if (used[col]) continue;
        uint32_t vx = 0, vz = 0;
        /* Set free coordinate col to 1 (= 3 = w + w^2) */
        vx |= (1U << col); vz |= (1U << col);
        for (int p = 0; p < rk; p++) {
            int val = M[p][col]; /* v[piv[p]] = M[p][col] * 1 = val */
            int pc = piv[p];
            if (val == 1 || val == 3) vx |= (1U << pc);
            if (val == 2 || val == 3) vz |= (1U << pc);
        }
        dx[nd] = vx;
        dz[nd] = vz;
        nd++;
    }
    return nd;
}

static int in_gf4_span(int l, const uint32_t *cx, const uint32_t *cz, uint32_t vx, uint32_t vz) {
    int lim = 1 << (2 * l);
    for (int m = 0; m < lim; m++) {
        uint32_t ux = 0, uz = 0;
        for (int i = 0; i < l; i++) {
            int sc = (m >> (2 * i)) & 3;
            if (sc) {
                uint32_t tx, tz;
                mul_gf4_vec(sc, cx[i], cz[i], &tx, &tz);
                ux ^= tx; uz ^= tz;
            }
        }
        if (ux == vx && uz == vz) return 1;
    }
    return 0;
}

/* Full standalone binary symplectic verification of S = phi(D) */
static int verify_binary_eaqecc(int n, int k, int c, int d_target, const uint32_t *cx, const uint32_t *cz, uint32_t *sx, uint32_t *sz) {
    int l = (n - k - c) / 2;
    int K = k + l;
    uint32_t dx[32], dz[32];
    int nd = compute_gf4_dual(n, K, cx, cz, dx, dz);
    if (nd != n - K) return 0;

    int s_rows = 2 * nd; /* == n - k + c */
    if (s_rows != n - k + c) return 0;
    for (int i = 0; i < nd; i++) {
        sx[2 * i] = dx[i];     sz[2 * i] = dz[i];
        mul_gf4_vec(1, dx[i], dz[i], &sx[2 * i + 1], &sz[2 * i + 1]);
    }

    /* 1. RREF of S over GF(2) */
    uint64_t S_rref[64];
    int s_piv[64];
    for (int i = 0; i < s_rows; i++) {
        S_rref[i] = ((uint64_t)sx[i]) | (((uint64_t)sz[i]) << n);
    }
    int rk_s = 0;
    for (int col = 0; col < 2 * n && rk_s < s_rows; col++) {
        int sel = -1;
        for (int row = rk_s; row < s_rows; row++) {
            if ((S_rref[row] >> col) & 1ULL) { sel = row; break; }
        }
        if (sel < 0) continue;
        uint64_t tmp = S_rref[rk_s]; S_rref[rk_s] = S_rref[sel]; S_rref[sel] = tmp;
        s_piv[rk_s] = col;
        for (int row = 0; row < s_rows; row++) {
            if (row != rk_s && ((S_rref[row] >> col) & 1ULL)) S_rref[row] ^= S_rref[rk_s];
        }
        rk_s++;
    }
    if (rk_s != s_rows) return 0;

    /* 2. Symplectic Gram rank of S == 2*c */
    uint64_t G[64];
    for (int i = 0; i < s_rows; i++) {
        uint64_t grow = 0;
        for (int j = 0; j < s_rows; j++) {
            if (symp_ip(sx[i], sz[i], sx[j], sz[j])) grow |= (1ULL << j);
        }
        G[i] = grow;
    }
    int grank = 0;
    for (int col = 0; col < s_rows && grank < s_rows; col++) {
        int sel = -1;
        for (int row = grank; row < s_rows; row++) {
            if ((G[row] >> col) & 1ULL) { sel = row; break; }
        }
        if (sel < 0) continue;
        uint64_t tmp = G[grank]; G[grank] = G[sel]; G[sel] = tmp;
        for (int row = 0; row < s_rows; row++) {
            if (row != grank && ((G[row] >> col) & 1ULL)) G[row] ^= G[grank];
        }
        grank++;
    }
    if (grank != 2 * c) return 0;

    /* 3. Independent binary symplectic dual of S and FULL enumeration of all 2^(2K) vectors */
    uint32_t bx[64], bz[64];
    int m_bin = 2 * K;
    if (compute_bin_dual(n, s_rows, sx, sz, bx, bz) != m_bin) return 0;

    int min_d = 999, in_s = 0;
    for (int mask = 0; mask < (1 << m_bin); mask++) {
        uint32_t ux = 0, uz = 0;
        for (int b = 0; b < m_bin; b++) {
            if ((mask >> b) & 1) { ux ^= bx[b]; uz ^= bz[b]; }
        }
        uint64_t v = ((uint64_t)ux) | (((uint64_t)uz) << n);
        for (int p = 0; p < rk_s; p++) {
            if ((v >> s_piv[p]) & 1ULL) v ^= S_rref[p];
        }
        if (v == 0) in_s++;
        else {
            int w = __builtin_popcount(ux | uz);
            if (w < min_d) min_d = w;
        }
    }
    if (in_s != (1 << (2 * l))) return 0;
    return (min_d >= d_target) ? min_d : 0;
}

typedef struct {
    int n, k, c, d_target;
    const char *note;
} GF4Target;

static int search_gf4(GF4Target t, int restarts, int steps_per_rep, const char *dump_dir) {
    int n = t.n, k = t.k, c = t.c, d_t = t.d_target;
    int l = (n - k - c) / 2;
    int K = l + k;
    int nd_exp = n - K;
    uint32_t mask_n = (1U << n) - 1U;

    uint32_t cx[16], cz[16], cand_cx[16], cand_cz[16];
    uint32_t dx[32], dz[32], sx[64], sz[64];
    int best_d = 0;
    int64_t best_pen = INT64_MAX;

    for (int rep = 0; rep < restarts; rep++) {
        memset(cx, 0, sizeof(cx));
        memset(cz, 0, sizeof(cz));
        /* Initialize l isotropic pairs on 2*l coordinates: (1, 1) has weight 2 => <h_i, h_i>_h = 0! */
        for (int i = 0; i < l; i++) {
            uint32_t bits = (1U << (2 * i)) | (1U << (2 * i + 1));
            cx[i] = bits; cz[i] = bits; /* scalar 1 on positions 2i, 2i+1 */
        }
        /* Initialize k orthonormal vectors on positions 2l .. 2l + k - 1 (weight 1 => <w_a, w_b>_h = delta_ab) */
        for (int a = 0; a < k; a++) {
            uint32_t bit = (1U << (2 * l + a));
            cx[l + a] = bit; cz[l + a] = bit;
        }
        /* Scramble with 160 random U(n, GF(4)) unitary reflections/transvections */
        for (int s = 0; s < 160; s++) {
            uint32_t gx = (uint32_t)xorshift64() & mask_n;
            uint32_t gz = (uint32_t)xorshift64() & mask_n;
            if ((gx | gz) == 0) gx = 1;
            apply_unitary(K, gx, gz, (int)(s & 1), cx, cz);
        }

        int cur_d = 0, bad_m = -1;
        int64_t cur_pen = eval_gf4_code(K, l, d_t, cx, cz, &cur_d, &bad_m);
        double temp = 10.0;
        int d_valid = 0;

        for (int step = 0; step < steps_per_rep && cur_pen > 0; step++) {
            memcpy(cand_cx, cx, K * sizeof(uint32_t));
            memcpy(cand_cz, cz, K * sizeof(uint32_t));

            uint64_t rv = xorshift64();
            int mode = (int)(rv & 7ULL);
            int valid_move = 1;

            if (mode < 4) {
                /* GF(4) Hermitian dual coset move! */
                if (!d_valid) {
                    if (compute_gf4_dual(n, K, cx, cz, dx, dz) == nd_exp) d_valid = 1;
                }
                if (d_valid) {
                    int idx = (int)((rv >> 16) % K);
                    if (bad_m > 0 && (rv & 8ULL)) {
                        int ch[16], nc = 0;
                        for (int j = 0; j < K; j++) {
                            if ((bad_m >> (2 * j)) & 3) ch[nc++] = j;
                        }
                        if (nc > 0) idx = ch[(rv >> 20) % nc];
                    }
                    uint32_t ux = 0, uz = 0;
                    int nterms = 1 + (int)((rv >> 4) % 3);
                    for (int t_i = 0; t_i < nterms; t_i++) {
                        uint64_t rc = xorshift64();
                        int bi = (int)(rc % nd_exp);
                        int sc = 1 + (int)((rc >> 8) % 3);
                        uint32_t tx, tz;
                        mul_gf4_vec(sc, dx[bi], dz[bi], &tx, &tz);
                        ux ^= tx; uz ^= tz;
                    }
                    if ((ux | uz) == 0) valid_move = 0;
                    else if (idx < l) {
                        /* Must have EVEN weight (<delta, delta>_h == 0) AND not lie in H_0! */
                        if ((__builtin_popcount(ux | uz) & 1) != 0) valid_move = 0;
                        else if (l <= 6 && in_gf4_span(l, cx, cz, ux, uz)) valid_move = 0;
                    }
                    if (valid_move) {
                        cand_cx[idx] ^= ux;
                        cand_cz[idx] ^= uz;
                        if (idx >= l && (__builtin_popcount(ux | uz) & 1) != 0) {
                            /* Check that W stays Hermitian-nondegenerate */
                            if (gf4_gram_rank(k, cand_cx + l, cand_cz + l) != k) valid_move = 0;
                        }
                    }
                } else {
                    valid_move = 0;
                }
            } else {
                /* Sparse weight 2..4 U(n, GF(4)) unitary reflection/transvection */
                uint32_t gx = 0, gz = 0;
                int wt = 2 + (int)((rv >> 4) % 3);
                for (int q = 0; q < wt; q++) {
                    uint64_t rq = xorshift64();
                    int pos = (int)(rq % n);
                    int sc = 1 + (int)((rq >> 8) % 3);
                    uint32_t tx = (sc == 1 || sc == 3) ? (1U << pos) : 0;
                    uint32_t tz = (sc == 2 || sc == 3) ? (1U << pos) : 0;
                    gx ^= tx; gz ^= tz;
                }
                if ((gx | gz) == 0) gx = 1;
                apply_unitary(K, gx, gz, (int)((rv >> 12) & 1ULL), cand_cx, cand_cz);
            }

            if (!valid_move) continue;

            int nxt_d = 0, nxt_b = -1;
            int64_t nxt_pen = eval_gf4_code(K, l, d_t, cand_cx, cand_cz, &nxt_d, &nxt_b);
            int accept = 0;
            if (nxt_pen <= cur_pen) accept = 1;
            else {
                double diff = (double)(nxt_pen - cur_pen);
                if (diff < temp * 8.0) {
                    double u = (double)(xorshift64() & 0xffffffULL) / (double)0x1000000ULL;
                    double x = diff / temp;
                    double prob = 1.0 / (1.0 + x + 0.5 * x * x + 0.1666667 * x * x * x);
                    if (u < prob) accept = 1;
                }
            }
            if (accept) {
                memcpy(cx, cand_cx, K * sizeof(uint32_t));
                memcpy(cz, cand_cz, K * sizeof(uint32_t));
                cur_pen = nxt_pen;
                cur_d = nxt_d;
                bad_m = nxt_b;
                d_valid = 0;
            }
            temp *= 0.99965;
            if (temp < 0.25) temp = 0.25;
            if (step % 15000 == 14999 && cur_pen > 0) temp = 4.5;
        }

        if (cur_pen < best_pen) best_pen = cur_pen;
        if (cur_d > best_d) best_d = cur_d;

        if (cur_pen == 0) {
            int vd = verify_binary_eaqecc(n, k, c, d_t, cx, cz, sx, sz);
            if (vd >= d_t) {
                int s_rows = n - k + c;
                printf("HIT! [[%d, %d, %d; c=%d]]_2 (rep=%d, binary-verified d=%d, %s)\n",
                       n, k, vd, c, rep, vd, t.note);
                char fname[256];
                snprintf(fname, sizeof(fname), "%s/hit_n%d_k%d_d%d_c%d.tsv", dump_dir, n, k, vd, c);
                FILE *fp = fopen(fname, "w");
                if (fp) {
                    fprintf(fp, "# EAQECC [[%d, %d, %d; %d]]_2 over GF(2) (symplectic form [X | Z])\n", n, k, vd, c);
                    fprintf(fp, "# rows=%d cols=%d rank=%d symp_gram_rank=%d d_EA=%d\n", s_rows, 2 * n, s_rows, 2 * c, vd);
                    for (int i = 0; i < s_rows; i++) {
                        for (int col = 0; col < n; col++) {
                            if (col) fputc('\t', fp);
                            fputc(((sx[i] >> col) & 1U) ? '1' : '0', fp);
                        }
                        for (int col = 0; col < n; col++) {
                            fputc('\t', fp);
                            fputc(((sz[i] >> col) & 1U) ? '1' : '0', fp);
                        }
                        fputc('\n', fp);
                    }
                    fclose(fp);
                }
                fflush(stdout);
                return 1;
            } else {
                printf("INTERNAL BUG: cur_pen=0 but verify_binary_eaqecc=%d!\n", vd);
                fflush(stdout);
            }
        }
    }
    printf("MISS [[%d, %d, %d; c=%d]]_2: best_d=%d best_pen=%lld (%s)\n",
           n, k, d_t, c, best_d, (long long)best_pen, t.note);
    fflush(stdout);
    return 0;
}

int main(void) {
    GF4Target targets[] = {
        {19, 2,  9, 11, "K=6 l=4 (4096 cw) | Grassl 10-17 | LCD_Griesmer(11,2)=8<11 | BKLC(19,6)=12"},
        {18, 3,  9, 10, "K=6 l=3 (4096 cw) | Grassl 9-15 | LCD_Griesmer(12,3)=8<10 | BKLC(18,6)=12"},
        {19, 3,  8, 10, "K=7 l=4 (16384 cw) | Grassl 9-15 | LCD_Griesmer(11,3)=8<10 | BKLC(19,7)=11"},
        {21, 4, 11, 11, "K=7 l=3 (16384 cw) | Grassl 10-17 | LCD_Griesmer(15,4)=10<11 | BKLC(21,7)=12"},
        {22, 3, 11, 12, "K=7 l=4 (16384 cw) | Grassl 11-19 | LCD_Griesmer(14,3)=10<12 | BKLC(22,7)=13"},
        {20, 5,  9,  9, "K=8 l=3 (65536 cw) | Grassl 8-14 | LCD_Griesmer(14,5)=8<9 | BKLC(20,8)=10"},
        {19, 4,  7,  9, "K=8 l=4 (65536 cw) | Grassl 8-14 | LCD_Griesmer(11,4)=7<9 | BKLC(19,8)=9"},
        {24, 3, 11, 12, "K=8 l=5 (65536 cw) | Grassl 11-21 | LCD_Griesmer(14,3)=10<12 | BKLC(24,8)=13"}
    };
    int nt = (int)(sizeof(targets) / sizeof(targets[0]));
    for (int i = 0; i < nt; i++) {
        if (search_gf4(targets[i], 60, 50000, ".")) {
            printf("STOPPING ON FIRST BINARY-VERIFIED HIT!\n");
            break;
        }
    }
    return 0;
}
