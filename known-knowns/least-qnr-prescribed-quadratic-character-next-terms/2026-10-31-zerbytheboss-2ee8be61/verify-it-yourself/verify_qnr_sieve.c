#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#if defined(__GNUC__) || defined(__clang__)
#define NOINLINE __attribute__((noinline))
#define UNLIKELY(x) __builtin_expect(!!(x), 0)
#else
#define NOINLINE
#define UNLIKELY(x) (x)
#endif

static const int PRIMES[45] = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197
};

static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a;
    uint64_t y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}

static int legendre(long long a, int p) {
    a %= p;
    if (a < 0) a += p;
    if (a == 0) return 0;
    long long res = 1, base = a;
    int exp = (p - 1) / 2;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % p;
        base = (base * base) % p;
        exp >>= 1;
    }
    return (res == 1) ? 1 : -1;
}

static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m) {
    return (uint64_t)(((__int128)a * b) % m);
}

static uint64_t powmod(uint64_t base, uint64_t exp, uint64_t mod) {
    uint64_t res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = mulmod(res, base, mod);
        base = mulmod(base, base, mod);
        exp >>= 1;
    }
    return res;
}

static inline bool is_odd_square(uint64_t n) {
    if ((n & 7) != 1) return false;
    double d = (double)n;
    union { double d; uint64_t u; } u = { d };
    u.u = 0x5fe6eb50c7b537a9ULL - (u.u >> 1);
    double half_d = 0.5 * d;
    double y = u.d;
    y = y * (1.5 - half_d * y * y);
    y = y * (1.5 - half_d * y * y);
    y = y * (1.5 - half_d * y * y);
    uint64_t rt = (uint64_t)(d * y + 0.5);
    return rt * rt == n;
}

NOINLINE
static bool is_prime(uint64_t n) {
    if (n < 2) return false;
    if (is_odd_square(n)) return false;
    static const uint64_t small_primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        if (n == small_primes[i]) return true;
        if (n % small_primes[i] == 0) return false;
    }
    uint64_t d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    static const uint64_t bases[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (int i = 0; i < 12; i++) {
        uint64_t a = bases[i];
        if (n <= a) break;
        uint64_t x = powmod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int r = 1; r < s; r++) {
            x = mulmod(x, x, n);
            if (x == n - 1) { composite = false; break; }
        }
        if (composite) return false;
    }
    return true;
}

static long long extgcd(long long a, long long b, long long *x, long long *y) {
    if (b == 0) { *x = 1; *y = 0; return a; }
    long long x1, y1;
    long long g = extgcd(b, a % b, &x1, &y1);
    *x = y1;
    *y = x1 - (a / b) * y1;
    return g;
}

static long long modinv(long long a, long long m) {
    long long x, y;
    extgcd(((a % m) + m) % m, m, &x, &y);
    return (x % m + m) % m;
}

static inline bool is_qr_p_over_q(int p, uint64_t q) {
    int r = (int)(q % (uint64_t)p);
    if (r == 0) return false;
    int leg = legendre(r, p);
    if ((p & 3) == 3 && (q & 3) == 3) leg = -leg;
    return leg == 1;
}

static uint64_t min_prime_for_n[45];
static uint64_t min_odd_for_n[45];
static uint64_t min_qr_for_n[45];
static uint64_t hits_1mod8_38qr[16];
static int n_hits_1mod8_38qr = 0;

/*
 * Stage 1 Enumerator 1:
 * 9-prime CRT wheel M1 = 8*3*5*7*11*13*17*19*23 = 892,371,480
 * with 20 sieve primes p_10=29 .. p_29=109.
 * Radix decomposition k = 899 * k1 + k0 (899 = 29 * 31, 0 <= k0 < 899, 0 <= k1 <= 395).
 */
#define E1_WORDS 7

static uint64_t g_e1_single_masks[18][115][E1_WORDS];
static int g_e1_sieve_p[18];

NOINLINE
static void handle_e1_hit(uint64_t v, int w, uint16_t k0, uint64_t r, uint64_t M1, uint64_t Q_MAX, int q_mod_8) {
    uint64_t base_q = (uint64_t)k0 * M1 + r;
    for (int s = 10; s < 18; s++) {
        v &= g_e1_single_masks[s][base_q % (uint64_t)g_e1_sieve_p[s]][w];
        if (!v) return;
    }
    while (v) {
        int bit = __builtin_ctzll(v);
        v &= v - 1;
        uint64_t k1 = (uint64_t)w * 64 + (uint64_t)bit;
        uint64_t k = k1 * 899ULL + (uint64_t)k0;
        uint64_t q = k * M1 + r;
        if (q <= 1 || q > Q_MAX) continue;
        if (is_odd_square(q)) continue;
        int first_fail = 29;
        while (first_fail < 44 && is_qr_p_over_q(PRIMES[first_fail], q)) {
            first_fail++;
        }
        if (is_prime(q)) {
            int n_qnr = first_fail + 1;
            if (n_qnr <= 44 && q < min_prime_for_n[n_qnr]) {
                min_prime_for_n[n_qnr] = q;
            }
            for (int m = 29; m <= first_fail && m <= 44; m++) {
                if (q_mod_8 == 7) {
                    if (q < min_odd_for_n[m]) min_odd_for_n[m] = q;
                } else {
                    if (q < min_qr_for_n[m]) min_qr_for_n[m] = q;
                }
            }
            if (q_mod_8 == 1 && first_fail >= 38 && n_hits_1mod8_38qr < 16) {
                hits_1mod8_38qr[n_hits_1mod8_38qr++] = q;
            }
        }
    }
}

static void run_enumerator1_case(int q_mod_8, uint64_t Q_MAX) {
    uint64_t M1 = 8ULL * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23;
    int mods1[9] = {8, 3, 5, 7, 11, 13, 17, 19, 23};
    int allow1[9][12];
    int n_allow1[9];
    allow1[0][0] = q_mod_8;
    n_allow1[0] = 1;
    for (int idx = 1; idx < 9; idx++) {
        int p = mods1[idx];
        int cnt = 0;
        for (int r = 1; r < p; r++) {
            int leg = legendre(r, p);
            if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
            if (leg == 1) allow1[idx][cnt++] = r;
        }
        n_allow1[idx] = cnt;
    }

    uint64_t crt_coeff[9];
    for (int idx = 0; idx < 9; idx++) {
        uint64_t m = (uint64_t)mods1[idx];
        uint64_t Mi = M1 / m;
        uint64_t inv = (uint64_t)modinv((long long)(Mi % m), (long long)m);
        crt_coeff[idx] = mulmod(Mi, inv, M1);
    }

    bool ok29[29] = {0}, ok31[31] = {0};
    for (int u = 1; u < 29; u++) {
        if (legendre(u, 29) == 1) ok29[u] = true;
    }
    for (int u = 1; u < 31; u++) {
        int leg = legendre(u, 31);
        if ((q_mod_8 & 3) == 3) leg = -leg;
        if (leg == 1) ok31[u] = true;
    }
    static uint16_t adm_k0[899][210];
    int m1_mod_899 = (int)(M1 % 899ULL);
    for (int r0 = 0; r0 < 899; r0++) {
        int cnt = 0;
        for (int k0 = 0; k0 < 899; k0++) {
            int val = (r0 + k0 * m1_mod_899) % 899;
            if (ok29[val % 29] && ok31[val % 31]) {
                adm_k0[r0][cnt++] = (uint16_t)k0;
            }
        }
    }

    uint64_t S1 = M1 * 899ULL;
    int max_k1 = (int)(Q_MAX / S1);
    memset(g_e1_single_masks, 0, sizeof(g_e1_single_masks));
    for (int s = 0; s < 18; s++) {
        int p = PRIMES[11 + s];
        g_e1_sieve_p[s] = p;
        int inv_S1 = (int)modinv((long long)(S1 % (uint64_t)p), p);
        for (int r0 = 0; r0 < p; r0++) {
            for (int u = 1; u < p; u++) {
                int leg = legendre(u, p);
                if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
                if (leg == 1) {
                    int k_mod_p = (int)((((long long)(u - r0) % p + p) % p * inv_S1) % p);
                    for (int k1 = k_mod_p; k1 <= max_k1; k1 += p) {
                        g_e1_single_masks[s][r0][k1 >> 6] |= (1ULL << (k1 & 63));
                    }
                }
            }
        }
    }

    int pair_mod[5];
    uint64_t *pair_masks[5];
    static uint16_t k0_off[5][899];
    for (int c = 0; c < 5; c++) {
        int pa = g_e1_sieve_p[2 * c];
        int pb = g_e1_sieve_p[2 * c + 1];
        int pm = pa * pb;
        pair_mod[c] = pm;
        uint64_t m1_mod_pm = M1 % (uint64_t)pm;
        for (int k0 = 0; k0 < 899; k0++) {
            k0_off[c][k0] = (uint16_t)(((uint64_t)k0 * m1_mod_pm) % (uint64_t)pm);
        }
        pair_masks[c] = (uint64_t *)malloc((size_t)(2 * pm) * E1_WORDS * sizeof(uint64_t));
        for (int r0 = 0; r0 < pm; r0++) {
            uint64_t *d1 = pair_masks[c] + (size_t)r0 * E1_WORDS;
            uint64_t *d2 = pair_masks[c] + (size_t)(r0 + pm) * E1_WORDS;
            for (int w = 0; w < E1_WORDS; w++) {
                uint64_t v = g_e1_single_masks[2 * c][r0 % pa][w] & g_e1_single_masks[2 * c + 1][r0 % pb][w];
                d1[w] = v;
                d2[w] = v;
            }
        }
    }

    int total_r = 142560;
    int idx_tuple[9] = {0};

    for (int iter = 0; iter < total_r; iter++) {
        uint64_t r = 0;
        for (int j = 0; j < 9; j++) {
            uint64_t term = mulmod(crt_coeff[j], (uint64_t)allow1[j][idx_tuple[j]], M1);
            r += term;
            if (r >= M1) r -= M1;
        }
        int carry = 8;
        while (carry >= 0) {
            idx_tuple[carry]++;
            if (idx_tuple[carry] < n_allow1[carry]) break;
            idx_tuple[carry] = 0;
            carry--;
        }

        const uint16_t *k0_list = adm_k0[r % 899ULL];
        int b0 = (int)(r % (uint64_t)pair_mod[0]);
        int b1 = (int)(r % (uint64_t)pair_mod[1]);
        int b2 = (int)(r % (uint64_t)pair_mod[2]);
        int b3 = (int)(r % (uint64_t)pair_mod[3]);
        int b4 = (int)(r % (uint64_t)pair_mod[4]);

        for (int idx = 0; idx < 210; idx++) {
            uint16_t k0 = k0_list[idx];
            const uint64_t *r0 = pair_masks[0] + (size_t)(b0 + k0_off[0][k0]) * E1_WORDS;
            const uint64_t *r1 = pair_masks[1] + (size_t)(b1 + k0_off[1][k0]) * E1_WORDS;
            const uint64_t *r2 = pair_masks[2] + (size_t)(b2 + k0_off[2][k0]) * E1_WORDS;
            const uint64_t *r3 = pair_masks[3] + (size_t)(b3 + k0_off[3][k0]) * E1_WORDS;
            const uint64_t *r4 = pair_masks[4] + (size_t)(b4 + k0_off[4][k0]) * E1_WORDS;

            for (int w = 0; w < E1_WORDS; w++) {
                uint64_t v = r0[w] & r1[w] & r2[w] & r3[w] & r4[w];
                if (UNLIKELY(v != 0)) {
                    handle_e1_hit(v, w, k0, r, M1, Q_MAX, q_mod_8);
                }
            }
        }
    }

    for (int c = 0; c < 5; c++) free(pair_masks[c]);
}

/*
 * Shared M2 Sieve Engine (Stage 1 Enumerator 2 & Stage 2 Enumerator A):
 * 10-prime CRT wheel M2 = 8*3*5*7*11*13*17*19*23*29 = 25,878,772,920
 * with 28 sieve primes (31..163, Stage 1) or 30 sieve primes (31..173, Stage 2).
 * Radix decomposition k = 1147 * k1 + k0 (1147 = 31 * 37, 0 <= k0 < 1147, 0 <= k1 <= 49).
 */
static uint64_t g_M2;
static int g_n_allowA[10];
static uint64_t g_termA[10][15];
static uint16_t g_u_tilde[270];
static uint16_t g_T_off[6][270];
static uint16_t g_shift_for_r0[1147];
static uint16_t g_split_for_r0[1147];
static uint16_t g_shift_mod_pm[1147][6];
static uint16_t g_wrap_sub_pm[6];
static int g_pair_modA[6];
static uint64_t *g_pair_maskA[6];
static int g_rem_pA[16];
static int g_n_remA;
static uint64_t g_rem_maskA[16][200];
static uint64_t g_Q_MAXA;
static uint64_t *g_out_hitsA;
static int g_n_foundA;
static int g_max_hitsA;

NOINLINE
static void handle_M2_hit(uint64_t v, uint16_t k0, uint64_t r) {
    uint64_t base_q = (uint64_t)k0 * g_M2 + r;
    for (int s = 0; s < g_n_remA; s++) {
        v &= g_rem_maskA[s][base_q % (uint64_t)g_rem_pA[s]];
        if (!v) return;
    }
    while (v) {
        int k1 = __builtin_ctzll(v);
        v &= v - 1;
        uint64_t k = (uint64_t)k1 * 1147ULL + (uint64_t)k0;
        uint64_t q = k * g_M2 + r;
        if (q <= 1 || q > g_Q_MAXA) continue;
        if (is_prime(q) && g_n_foundA < g_max_hitsA) {
            g_out_hitsA[g_n_foundA++] = q;
        }
    }
}

static void dfs_enum_M2(int depth, uint64_t r) {
    if (depth == 10) {
        int r0 = (int)(r % 1147ULL);
        uint16_t shift = g_shift_for_r0[r0];
        int split = (int)g_split_for_r0[r0];
        const uint16_t *sh_pm = g_shift_mod_pm[shift];

        int b0 = (int)(r % (uint64_t)g_pair_modA[0]) + sh_pm[0];
        if (b0 >= g_pair_modA[0]) b0 -= g_pair_modA[0];
        int b1 = (int)(r % (uint64_t)g_pair_modA[1]) + sh_pm[1];
        if (b1 >= g_pair_modA[1]) b1 -= g_pair_modA[1];
        int b2 = (int)(r % (uint64_t)g_pair_modA[2]) + sh_pm[2];
        if (b2 >= g_pair_modA[2]) b2 -= g_pair_modA[2];
        int b3 = (int)(r % (uint64_t)g_pair_modA[3]) + sh_pm[3];
        if (b3 >= g_pair_modA[3]) b3 -= g_pair_modA[3];
        int b4 = (int)(r % (uint64_t)g_pair_modA[4]) + sh_pm[4];
        if (b4 >= g_pair_modA[4]) b4 -= g_pair_modA[4];
        int b5 = (int)(r % (uint64_t)g_pair_modA[5]) + sh_pm[5];
        if (b5 >= g_pair_modA[5]) b5 -= g_pair_modA[5];

        const uint64_t *m0 = g_pair_maskA[0] + b0;
        const uint64_t *m1 = g_pair_maskA[1] + b1;
        const uint64_t *m2 = g_pair_maskA[2] + b2;
        const uint64_t *m3 = g_pair_maskA[3] + b3;
        const uint64_t *m4 = g_pair_maskA[4] + b4;
        const uint64_t *m5 = g_pair_maskA[5] + b5;

        const uint16_t *t0 = g_T_off[0], *t1 = g_T_off[1], *t2 = g_T_off[2];
        const uint16_t *t3 = g_T_off[3], *t4 = g_T_off[4], *t5 = g_T_off[5];

        for (int idx = 0; idx < split; idx++) {
            uint64_t v = m0[t0[idx]] & m1[t1[idx]] & m2[t2[idx]] & m3[t3[idx]] & m4[t4[idx]] & m5[t5[idx]];
            if (UNLIKELY(v != 0)) {
                handle_M2_hit(v, (uint16_t)(g_u_tilde[idx] + shift), r);
            }
        }

        int w0 = b0 + g_wrap_sub_pm[0]; if (w0 >= g_pair_modA[0]) w0 -= g_pair_modA[0];
        int w1 = b1 + g_wrap_sub_pm[1]; if (w1 >= g_pair_modA[1]) w1 -= g_pair_modA[1];
        int w2 = b2 + g_wrap_sub_pm[2]; if (w2 >= g_pair_modA[2]) w2 -= g_pair_modA[2];
        int w3 = b3 + g_wrap_sub_pm[3]; if (w3 >= g_pair_modA[3]) w3 -= g_pair_modA[3];
        int w4 = b4 + g_wrap_sub_pm[4]; if (w4 >= g_pair_modA[4]) w4 -= g_pair_modA[4];
        int w5 = b5 + g_wrap_sub_pm[5]; if (w5 >= g_pair_modA[5]) w5 -= g_pair_modA[5];

        m0 = g_pair_maskA[0] + w0;
        m1 = g_pair_maskA[1] + w1;
        m2 = g_pair_maskA[2] + w2;
        m3 = g_pair_maskA[3] + w3;
        m4 = g_pair_maskA[4] + w4;
        m5 = g_pair_maskA[5] + w5;

        for (int idx = split; idx < 270; idx++) {
            uint64_t v = m0[t0[idx]] & m1[t1[idx]] & m2[t2[idx]] & m3[t3[idx]] & m4[t4[idx]] & m5[t5[idx]];
            if (UNLIKELY(v != 0)) {
                handle_M2_hit(v, (uint16_t)(g_u_tilde[idx] + shift - 1147), r);
            }
        }
        return;
    }
    int c = g_n_allowA[depth];
    for (int i = 0; i < c; i++) {
        uint64_t nr = r + g_termA[depth][i];
        if (nr >= g_M2) nr -= g_M2;
        dfs_enum_M2(depth + 1, nr);
    }
}

static int run_M2_sieve(int q_mod_8, uint64_t Q_MAX, int n_sieve_total, uint64_t *out_hits, int n_found, int max_hits) {
    g_M2 = 8ULL * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29;
    int mods2[10] = {8, 3, 5, 7, 11, 13, 17, 19, 23, 29};
    int allow2[10][15];
    allow2[0][0] = q_mod_8;
    g_n_allowA[0] = 1;
    for (int idx = 1; idx < 10; idx++) {
        int p = mods2[idx];
        int cnt = 0;
        for (int r = 1; r < p; r++) {
            int leg = legendre(r, p);
            if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
            if (leg == 1) allow2[idx][cnt++] = r;
        }
        g_n_allowA[idx] = cnt;
    }
    for (int idx = 0; idx < 10; idx++) {
        uint64_t m = (uint64_t)mods2[idx];
        uint64_t Mi = g_M2 / m;
        uint64_t inv = (uint64_t)modinv((long long)(Mi % m), (long long)m);
        uint64_t coeff = mulmod(Mi, inv, g_M2);
        for (int i = 0; i < g_n_allowA[idx]; i++) {
            g_termA[idx][i] = mulmod(coeff, (uint64_t)allow2[idx][i], g_M2);
        }
    }

    bool ok31[31] = {0}, ok37[37] = {0};
    for (int u = 1; u < 31; u++) {
        int leg = legendre(u, 31);
        if ((q_mod_8 & 3) == 3) leg = -leg;
        if (leg == 1) ok31[u] = true;
    }
    for (int u = 1; u < 37; u++) {
        if (legendre(u, 37) == 1) ok37[u] = true;
    }
    int m2_mod_1147 = (int)(g_M2 % 1147ULL);
    int inv_m2_1147 = (int)modinv(m2_mod_1147, 1147);
    int cnt = 0;
    for (int ut = 0; ut < 1147; ut++) {
        int u = (ut * m2_mod_1147) % 1147;
        if (ok31[u % 31] && ok37[u % 37]) {
            g_u_tilde[cnt++] = (uint16_t)ut;
        }
    }
    for (int r0 = 0; r0 < 1147; r0++) {
        int sh = ((1147 - r0) * inv_m2_1147) % 1147;
        g_shift_for_r0[r0] = (uint16_t)sh;
        int lim = 1147 - sh;
        int sp = 0;
        while (sp < 270 && g_u_tilde[sp] < lim) sp++;
        g_split_for_r0[r0] = (uint16_t)sp;
    }

    uint64_t S = g_M2 * 1147ULL;
    int max_k1 = (int)(Q_MAX / S);
    uint64_t valid_bits = (max_k1 >= 63) ? ~0ULL : ((1ULL << (max_k1 + 1)) - 1ULL);

    int n_after_1147 = n_sieve_total - 2;
    uint64_t single_mask[28][200];
    int sieve_p[28];
    for (int s = 0; s < n_after_1147; s++) {
        int p = PRIMES[12 + s];
        sieve_p[s] = p;
        int inv_S = (int)modinv((long long)(S % (uint64_t)p), p);
        for (int r0 = 0; r0 < p; r0++) {
            uint64_t m = 0;
            for (int u = 1; u < p; u++) {
                int leg = legendre(u, p);
                if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
                if (leg == 1) {
                    int k_mod_p = (int)((((long long)(u - r0) % p + p) % p * inv_S) % p);
                    for (int k = k_mod_p; k <= max_k1; k += p) {
                        m |= (1ULL << k);
                    }
                }
            }
            single_mask[s][r0] = m & valid_bits;
        }
    }
    for (int c = 0; c < 6; c++) {
        int pa = sieve_p[2 * c];
        int pb = sieve_p[2 * c + 1];
        int pm = pa * pb;
        g_pair_modA[c] = pm;
        uint64_t m2_mod_pm = g_M2 % (uint64_t)pm;
        for (int idx = 0; idx < 270; idx++) {
            g_T_off[c][idx] = (uint16_t)(((uint64_t)g_u_tilde[idx] * m2_mod_pm) % (uint64_t)pm);
        }
        for (int sh = 0; sh < 1147; sh++) {
            g_shift_mod_pm[sh][c] = (uint16_t)(((uint64_t)sh * m2_mod_pm) % (uint64_t)pm);
        }
        g_wrap_sub_pm[c] = (uint16_t)((pm - (int)((1147ULL * m2_mod_pm) % (uint64_t)pm)) % pm);

        g_pair_maskA[c] = (uint64_t *)malloc((size_t)(2 * pm) * sizeof(uint64_t));
        for (int r0 = 0; r0 < pm; r0++) {
            uint64_t v = single_mask[2 * c][r0 % pa] & single_mask[2 * c + 1][r0 % pb];
            g_pair_maskA[c][r0] = v;
            g_pair_maskA[c][r0 + pm] = v;
        }
    }
    g_n_remA = n_after_1147 - 12;
    for (int s = 0; s < g_n_remA; s++) {
        int p = sieve_p[12 + s];
        g_rem_pA[s] = p;
        for (int r0 = 0; r0 < p; r0++) g_rem_maskA[s][r0] = single_mask[12 + s][r0];
    }
    g_Q_MAXA = Q_MAX;
    g_out_hitsA = out_hits;
    g_n_foundA = n_found;
    g_max_hitsA = max_hits;

    dfs_enum_M2(0, 0);

    for (int c = 0; c < 6; c++) free(g_pair_maskA[c]);
    return g_n_foundA;
}

static int run_enumerator2_1mod8_bracket(uint64_t Q_MAX, uint64_t *out_hits) {
    return run_M2_sieve(1, Q_MAX, 28, out_hits, 0, 16);
}

static int run_stage2_enumA(int q_mod_8, uint64_t Q_MAX, uint64_t *out_hits, int n_found) {
    return run_M2_sieve(q_mod_8, Q_MAX, 30, out_hits, n_found, 32);
}

/*
 * Stage 2 Enumerator B:
 * 11-prime CRT wheel M3 = M2 * 31 = 802,241,960,520
 * with 29 sieve primes p_12=37 .. p_40=173.
 * Radix decomposition k = 37 * k1 + k0 (0 <= k0 < 37, 0 <= k1 <= 49).
 */
static uint64_t g_M3;
static int g_n_allow3[11];
static uint64_t g_term3[11][16];
static uint8_t g_adm_k0_B[37][18];
static uint16_t g_k0_off_B[6][37];
static int g_tm_nowrap3[15][7];
static int g_tm_wrap3[15][7];
static int g_pair_mod3[6];
static uint64_t *g_pair_masks3[6];
static int g_rem_p3[16];
static uint64_t g_rem_mask3[16][200];
static uint64_t g_Q_MAX3;
static uint64_t *g_out_hits3;
static int g_n_found3;

NOINLINE
static void handle_M3_hit(uint64_t v, uint8_t k0, uint64_t nr) {
    uint64_t base_q = (uint64_t)k0 * g_M3 + nr;
    for (int s = 0; s < 16; s++) {
        v &= g_rem_mask3[s][base_q % (uint64_t)g_rem_p3[s]];
        if (!v) return;
    }
    while (v) {
        int k1 = __builtin_ctzll(v);
        v &= v - 1;
        uint64_t k = (uint64_t)k1 * 37ULL + (uint64_t)k0;
        uint64_t q = k * g_M3 + nr;
        if (q <= 1 || q > g_Q_MAX3) continue;
        if (is_prime(q) && g_n_found3 < 32) {
            g_out_hits3[g_n_found3++] = q;
        }
    }
}

static void dfs_stage2_enumB(int depth, uint64_t r) {
    if (depth == 10) {
        int b0 = (int)(r % (uint64_t)g_pair_mod3[0]);
        int b1 = (int)(r % (uint64_t)g_pair_mod3[1]);
        int b2 = (int)(r % (uint64_t)g_pair_mod3[2]);
        int b3 = (int)(r % (uint64_t)g_pair_mod3[3]);
        int b4 = (int)(r % (uint64_t)g_pair_mod3[4]);
        int b5 = (int)(r % (uint64_t)g_pair_mod3[5]);
        int b37 = (int)(r % 37ULL);

        for (int i = 0; i < 15; i++) {
            uint64_t nr = r + g_term3[10][i];
            const int *tm = (nr >= g_M3) ? g_tm_wrap3[i] : g_tm_nowrap3[i];
            if (nr >= g_M3) nr -= g_M3;

            int r37 = b37 + tm[6];
            if (r37 >= 37) r37 -= 37;
            const uint8_t *k0_list = g_adm_k0_B[r37];

            int c0 = b0 + tm[0]; if (c0 >= g_pair_mod3[0]) c0 -= g_pair_mod3[0];
            int c1 = b1 + tm[1]; if (c1 >= g_pair_mod3[1]) c1 -= g_pair_mod3[1];
            int c2 = b2 + tm[2]; if (c2 >= g_pair_mod3[2]) c2 -= g_pair_mod3[2];
            int c3 = b3 + tm[3]; if (c3 >= g_pair_mod3[3]) c3 -= g_pair_mod3[3];
            int c4 = b4 + tm[4]; if (c4 >= g_pair_mod3[4]) c4 -= g_pair_mod3[4];
            int c5 = b5 + tm[5]; if (c5 >= g_pair_mod3[5]) c5 -= g_pair_mod3[5];

            const uint64_t *m0 = g_pair_masks3[0] + c0;
            const uint64_t *m1 = g_pair_masks3[1] + c1;
            const uint64_t *m2 = g_pair_masks3[2] + c2;
            const uint64_t *m3 = g_pair_masks3[3] + c3;
            const uint64_t *m4 = g_pair_masks3[4] + c4;
            const uint64_t *m5 = g_pair_masks3[5] + c5;

            for (int idx = 0; idx < 18; idx++) {
                uint8_t k0 = k0_list[idx];
                uint64_t v = m0[g_k0_off_B[0][k0]] & m1[g_k0_off_B[1][k0]] & m2[g_k0_off_B[2][k0]]
                           & m3[g_k0_off_B[3][k0]] & m4[g_k0_off_B[4][k0]] & m5[g_k0_off_B[5][k0]];
                if (UNLIKELY(v != 0)) {
                    handle_M3_hit(v, k0, nr);
                }
            }
        }
        return;
    }
    int c = g_n_allow3[depth];
    for (int i = 0; i < c; i++) {
        uint64_t nr = r + g_term3[depth][i];
        if (nr >= g_M3) nr -= g_M3;
        dfs_stage2_enumB(depth + 1, nr);
    }
}

static int run_stage2_enumB(int q_mod_8, uint64_t Q_MAX, uint64_t *out_hits, int n_found) {
    g_M3 = 8ULL * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31;
    int mods3[11] = {8, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31};
    int allow3[11][16];
    allow3[0][0] = q_mod_8;
    g_n_allow3[0] = 1;
    for (int idx = 1; idx < 11; idx++) {
        int p = mods3[idx];
        int cnt = 0;
        for (int r = 1; r < p; r++) {
            int leg = legendre(r, p);
            if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
            if (leg == 1) allow3[idx][cnt++] = r;
        }
        g_n_allow3[idx] = cnt;
    }

    for (int idx = 0; idx < 11; idx++) {
        uint64_t m = (uint64_t)mods3[idx];
        uint64_t Mi = g_M3 / m;
        uint64_t inv = (uint64_t)modinv((long long)(Mi % m), (long long)m);
        uint64_t coeff = mulmod(Mi, inv, g_M3);
        for (int i = 0; i < g_n_allow3[idx]; i++) {
            g_term3[idx][i] = mulmod(coeff, (uint64_t)allow3[idx][i], g_M3);
        }
    }

    bool ok37[37] = {0};
    for (int u = 1; u < 37; u++) {
        if (legendre(u, 37) == 1) ok37[u] = true;
    }
    int m3_mod_37 = (int)(g_M3 % 37ULL);
    for (int r0 = 0; r0 < 37; r0++) {
        int cnt = 0;
        for (int k0 = 0; k0 < 37; k0++) {
            int val = (r0 + k0 * m3_mod_37) % 37;
            if (ok37[val]) g_adm_k0_B[r0][cnt++] = (uint8_t)k0;
        }
    }

    uint64_t S = g_M3 * 37ULL;
    int max_k1 = (int)(Q_MAX / S);
    uint64_t valid_bits = (max_k1 >= 63) ? ~0ULL : ((1ULL << (max_k1 + 1)) - 1ULL);

    uint64_t single_mask[28][200];
    int sieve_p[28];
    for (int s = 0; s < 28; s++) {
        int p = PRIMES[12 + s];
        sieve_p[s] = p;
        int inv_S = (int)modinv((long long)(S % (uint64_t)p), p);
        for (int r0 = 0; r0 < p; r0++) {
            uint64_t m = 0;
            for (int u = 1; u < p; u++) {
                int leg = legendre(u, p);
                if ((p & 3) == 3 && (q_mod_8 & 3) == 3) leg = -leg;
                if (leg == 1) {
                    int k_mod_p = (int)((((long long)(u - r0) % p + p) % p * inv_S) % p);
                    for (int k = k_mod_p; k <= max_k1; k += p) {
                        m |= (1ULL << k);
                    }
                }
            }
            single_mask[s][r0] = m & valid_bits;
        }
    }
    for (int c = 0; c < 6; c++) {
        int pa = sieve_p[2 * c];
        int pb = sieve_p[2 * c + 1];
        int pm = pa * pb;
        g_pair_mod3[c] = pm;
        uint64_t m3_mod_pm = g_M3 % (uint64_t)pm;
        for (int i = 0; i < 15; i++) {
            g_tm_nowrap3[i][c] = (int)(g_term3[10][i] % (uint64_t)pm);
            g_tm_wrap3[i][c] = (int)((g_term3[10][i] % (uint64_t)pm + pm - m3_mod_pm) % pm);
        }
        for (int k0 = 0; k0 < 37; k0++) {
            g_k0_off_B[c][k0] = (uint16_t)(((uint64_t)k0 * m3_mod_pm) % (uint64_t)pm);
        }
        g_pair_masks3[c] = (uint64_t *)malloc((size_t)(2 * pm) * sizeof(uint64_t));
        for (int r0 = 0; r0 < pm; r0++) {
            uint64_t v = single_mask[2 * c][r0 % pa] & single_mask[2 * c + 1][r0 % pb];
            g_pair_masks3[c][r0] = v;
            g_pair_masks3[c][r0 + pm] = v;
        }
    }
    for (int i = 0; i < 15; i++) {
        g_tm_nowrap3[i][6] = (int)(g_term3[10][i] % 37ULL);
        g_tm_wrap3[i][6] = (int)((g_term3[10][i] % 37ULL + 37 - m3_mod_37) % 37);
    }
    for (int s = 0; s < 16; s++) {
        int p = sieve_p[12 + s];
        g_rem_p3[s] = p;
        for (int r0 = 0; r0 < p; r0++) g_rem_mask3[s][r0] = single_mask[12 + s][r0];
    }

    g_Q_MAX3 = Q_MAX;
    g_out_hits3 = out_hits;
    g_n_found3 = n_found;

    dfs_stage2_enumB(0, 0);

    for (int c = 0; c < 6; c++) free(g_pair_masks3[c]);
    return g_n_found3;
}

int main(void) {
    uint64_t Q_MAX = 317398900373231ULL;
    for (int i = 0; i < 45; i++) {
        min_prime_for_n[i] = ~0ULL;
        min_odd_for_n[i] = ~0ULL;
        min_qr_for_n[i] = ~0ULL;
    }
    run_enumerator1_case(1, Q_MAX);
    run_enumerator1_case(7, Q_MAX);

    uint64_t enum2_hits[16];
    int n_enum2 = run_enumerator2_1mod8_bracket(Q_MAX, enum2_hits);
    if (n_enum2 != n_hits_1mod8_38qr) {
        printf("Enumerator 1 vs Enumerator 2 hit count mismatch: %d != %d\n", n_hits_1mod8_38qr, n_enum2);
        return 1;
    }
    qsort(hits_1mod8_38qr, (size_t)n_hits_1mod8_38qr, sizeof(uint64_t), cmp_u64);
    qsort(enum2_hits, (size_t)n_enum2, sizeof(uint64_t), cmp_u64);
    for (int i = 0; i < n_enum2; i++) {
        if (hits_1mod8_38qr[i] != enum2_hits[i]) {
            printf("Enumerator 1 vs Enumerator 2 hit[%d] mismatch: %llu != %llu\n",
                   i, (unsigned long long)hits_1mod8_38qr[i], (unsigned long long)enum2_hits[i]);
            return 1;
        }
    }

    uint64_t Q_MAX_41 = 1463971373078639ULL;
    uint64_t hits_A[32], hits_B[32];
    int n_A = 0, n_B = 0;
    n_A = run_stage2_enumA(1, Q_MAX_41, hits_A, n_A);
    n_A = run_stage2_enumA(7, Q_MAX_41, hits_A, n_A);
    n_B = run_stage2_enumB(1, Q_MAX_41, hits_B, n_B);
    n_B = run_stage2_enumB(7, Q_MAX_41, hits_B, n_B);
    if (n_A != n_B || n_A != 5) {
        printf("Stage 2 Enumerator A vs B hit count mismatch: %d vs %d\n", n_A, n_B);
        return 1;
    }
    qsort(hits_A, (size_t)n_A, sizeof(uint64_t), cmp_u64);
    qsort(hits_B, (size_t)n_B, sizeof(uint64_t), cmp_u64);
    for (int i = 0; i < n_A; i++) {
        if (hits_A[i] != hits_B[i]) {
            printf("Stage 2 Enumerator A vs B hit[%d] mismatch: %llu != %llu\n",
                   i, (unsigned long long)hits_A[i], (unsigned long long)hits_B[i]);
            return 1;
        }
        int ff = 40;
        while (ff < 44 && is_qr_p_over_q(PRIMES[ff], hits_A[i])) ff++;
        int n_qnr = ff + 1;
        if (n_qnr <= 44 && hits_A[i] < min_prime_for_n[n_qnr]) {
            min_prime_for_n[n_qnr] = hits_A[i];
        }
    }

    for (int n = 30; n <= 43; n++) {
        printf("A000229(%d)=%llu\n", n, (unsigned long long)min_prime_for_n[n]);
    }
    for (int n = 30; n <= 38; n++) {
        printf("A002223(%d)=%llu\n", n, (unsigned long long)min_odd_for_n[n]);
    }
    for (int n = 30; n <= 41; n++) {
        printf("A002224(%d)=%llu\n", n, (unsigned long long)min_qr_for_n[n]);
    }
    printf("ENUM2_HITS=%d\n", n_enum2);
    for (int i = 0; i < n_enum2; i++) {
        printf("ENUM2_HIT(%d)=%llu\n", i, (unsigned long long)enum2_hits[i]);
    }
    printf("STAGE2_HITS=%d\n", n_A);
    for (int i = 0; i < n_A; i++) {
        printf("STAGE2_HIT(%d)=%llu\n", i, (unsigned long long)hits_A[i]);
    }
    return 0;
}
