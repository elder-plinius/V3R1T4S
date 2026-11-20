/*
 * verify_packing_c99.c
 * Standalone, zero-floating-point, strict ISO C99 exact rational verifier for:
 *   Target: cohn-sphere-packing-density-table (Partial Win p1, dimension 19)
 *
 * Compile: cc -std=c99 -O2 -Wall -Wextra -Werror -Wpedantic -mgeneral-regs-only verify_packing_c99.c -o verify_packing_c99
 * Zero floating-point types, zero <math.h>, zero external dependencies.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

#define MAX_DIM 24
#define MAX_TRANS 8
#define MAX_CONTACTS_STORE 4096
#define MAX_TOTAL_CONTACTS 16384
#define TRANS_COLS 95
#define FULL_COLS 285

static int64_t gcd64(int64_t a, int64_t b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) { int64_t t = a % b; a = b; b = t; }
    return a == 0 ? 1 : a;
}

static int64_t isqrt64(int64_t n) {
    if (n <= 0) return 0;
    int64_t x = n, y = (x + 1) / 2;
    while (y < x) { x = y; y = (x + n / x) / 2; }
    while ((x + 1) <= 3037000499LL && (x + 1) * (x + 1) <= n) x++;
    while (x > 3037000499LL || x * x > n) x--;
    return x;
}

static int64_t floor_div64(int64_t a, int64_t b) {
    int64_t q = a / b;
    int64_t r = a % b;
    if (r < 0) q--;
    return q;
}

static int64_t ceil_div64(int64_t a, int64_t b) {
    int64_t q = a / b;
    int64_t r = a % b;
    if (r > 0) q++;
    return q;
}

typedef struct { int64_t n; int64_t d; } rat_t;

static rat_t rat_make(int64_t n, int64_t d) {
    if (d < 0) { n = -n; d = -d; }
    if (d == 0) { fprintf(stderr, "FAIL: zero denominator\n"); exit(1); }
    int64_t g = gcd64(n, d);
    rat_t r; r.n = n / g; r.d = d / g;
    return r;
}
static rat_t rat_add(rat_t a, rat_t b) { return rat_make(a.n * b.d + b.n * a.d, a.d * b.d); }
static rat_t rat_mul(rat_t a, rat_t b) { return rat_make(a.n * b.n, a.d * b.d); }

/* Tiny base-10^9 BigUInt for exact power / center-density cross-multiplication */
typedef struct { uint32_t limb[16]; int len; } biguint_t;

static void big_from_u64(biguint_t *b, uint64_t v) {
    memset(b, 0, sizeof(*b));
    while (v > 0) { b->limb[b->len++] = (uint32_t)(v % 1000000000ULL); v /= 1000000000ULL; }
    if (b->len == 0) b->len = 1;
}
static void big_from_dec(biguint_t *b, const char *s) {
    big_from_u64(b, 0);
    for (const char *p = s; *p; p++) {
        if (!isdigit((unsigned char)*p)) continue;
        uint64_t carry = (uint64_t)(*p - '0');
        for (int i = 0; i < b->len; i++) {
            uint64_t cur = (uint64_t)b->limb[i] * 10ULL + carry;
            b->limb[i] = (uint32_t)(cur % 1000000000ULL);
            carry = cur / 1000000000ULL;
        }
        if (carry) b->limb[b->len++] = (uint32_t)carry;
    }
}
static void big_mul_u64(biguint_t *b, uint64_t m) {
    uint64_t carry = 0;
    for (int i = 0; i < b->len; i++) {
        uint64_t cur = (uint64_t)b->limb[i] * m + carry;
        b->limb[i] = (uint32_t)(cur % 1000000000ULL);
        carry = cur / 1000000000ULL;
    }
    while (carry > 0) {
        b->limb[b->len++] = (uint32_t)(carry % 1000000000ULL);
        carry /= 1000000000ULL;
    }
    while (b->len > 1 && b->limb[b->len - 1] == 0) b->len--;
}
static int big_cmp(const biguint_t *a, const biguint_t *b) {
    if (a->len != b->len) return a->len < b->len ? -1 : 1;
    for (int i = a->len - 1; i >= 0; i--) {
        if (a->limb[i] != b->limb[i]) return a->limb[i] < b->limb[i] ? -1 : 1;
    }
    return 0;
}
static void big_to_str(const biguint_t *b, char *out, size_t cap) {
    int n = snprintf(out, cap, "%u", b->limb[b->len - 1]);
    if (n < 0 || (size_t)n >= cap) { fprintf(stderr, "FAIL: big_to_str buffer overflow\n"); exit(1); }
    size_t pos = (size_t)n;
    for (int i = b->len - 2; i >= 0; i--) {
        n = snprintf(out + pos, cap - pos, "%09u", b->limb[i]);
        if (n < 0 || (size_t)n >= cap - pos) { fprintf(stderr, "FAIL: big_to_str buffer overflow\n"); exit(1); }
        pos += (size_t)n;
    }
}

/* Exact Bareiss determinant using 64-bit integers with overflow guard */
static int64_t bareiss_det(int n, const int64_t A[MAX_DIM][MAX_DIM]) {
    int64_t M[MAX_DIM][MAX_DIM];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            M[i][j] = A[i][j];
    int64_t prev = 1;
    int sign = 1;
    for (int k = 0; k < n - 1; k++) {
        if (M[k][k] == 0) {
            int sw = -1;
            for (int r = k + 1; r < n; r++) if (M[r][k] != 0) { sw = r; break; }
            if (sw < 0) return 0;
            for (int c = k; c < n; c++) { int64_t t = M[k][c]; M[k][c] = M[sw][c]; M[sw][c] = t; }
            sign = -sign;
        }
        for (int i = k + 1; i < n; i++) {
            for (int j = k + 1; j < n; j++) {
                int64_t a = M[k][k], b = M[i][j], c = M[i][k], d = M[k][j];
                if ((a != 0 && llabs(b) > (INT64_MAX / 4) / llabs(a)) ||
                    (c != 0 && llabs(d) > (INT64_MAX / 4) / llabs(c))) {
                    fprintf(stderr, "FAIL: Bareiss 64-bit guard triggered\n");
                    exit(1);
                }
                int64_t num = a * b - c * d;
                if (num % prev != 0) { fprintf(stderr, "FAIL: Bareiss division not exact\n"); exit(1); }
                M[i][j] = num / prev;
            }
            M[i][k] = 0;
        }
        prev = M[k][k];
    }
    return sign * M[n - 1][n - 1];
}

/* Minimal JSON navigation helpers (exact key search within scope) */
static const char *find_key_in_range(const char *start, const char *end, const char *key) {
    char pat[128];
    int n = snprintf(pat, sizeof(pat), "\"%s\"", key);
    if (n < 0 || (size_t)n >= sizeof(pat)) { fprintf(stderr, "FAIL: key too long\n"); exit(1); }
    size_t plen = (size_t)n;
    const char *p = start;
    while (p + plen < end) {
        const char *q = strstr(p, pat);
        if (!q || q + plen >= end) return NULL;
        const char *after = q + plen;
        while (after < end && isspace((unsigned char)*after)) after++;
        if (after < end && *after == ':') return after + 1;
        p = q + plen;
    }
    return NULL;
}

static const char *find_matching_brace(const char *p) {
    while (*p && isspace((unsigned char)*p)) p++;
    char open = *p, close = (open == '{') ? '}' : ']';
    int depth = 0, in_str = 0, escaped = 0;
    for (; *p; p++) {
        if (escaped) { escaped = 0; continue; }
        if (in_str && *p == '\\') { escaped = 1; continue; }
        if (*p == '"') { in_str = !in_str; continue; }
        if (!in_str) {
            if (*p == open) depth++;
            else if (*p == close) { depth--; if (depth == 0) return p + 1; }
        }
    }
    return NULL;
}

static int64_t parse_int_at(const char **pp) {
    const char *p = *pp;
    while (*p && (isspace((unsigned char)*p) || *p == ',')) p++;
    char *endp = NULL;
    long long v = strtoll(p, &endp, 10);
    if (endp == p) { fprintf(stderr, "FAIL: expected int near %.30s\n", p); exit(1); }
    *pp = endp;
    return (int64_t)v;
}

static rat_t parse_rat_str_at(const char **pp) {
    const char *p = *pp;
    while (*p && (isspace((unsigned char)*p) || *p == ',')) p++;
    if (*p != '"') { fprintf(stderr, "FAIL: expected string near %.30s\n", p); exit(1); }
    p++;
    char *end1 = NULL;
    long long num = strtoll(p, &end1, 10);
    long long den = 1;
    if (*end1 == '/') {
        char *end2 = NULL;
        den = strtoll(end1 + 1, &end2, 10);
        end1 = end2;
    }
    if (*end1 != '"') { fprintf(stderr, "FAIL: expected closing quote near %.30s\n", end1); exit(1); }
    *pp = end1 + 1;
    return rat_make((int64_t)num, (int64_t)den);
}

static void parse_int_mat(const char *start, const char *end, const char *key, int rows, int cols, int64_t out[MAX_DIM][MAX_DIM]) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && *p != '[') p++;
    p++;
    for (int i = 0; i < rows; i++) {
        while (*p && *p != '[') p++;
        p++;
        for (int j = 0; j < cols; j++) out[i][j] = parse_int_at(&p);
        while (*p && *p != ']') p++;
        p++;
    }
}

static void parse_int_vec(const char *start, const char *end, const char *key, int len, int64_t *out) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && *p != '[') p++;
    p++;
    for (int i = 0; i < len; i++) out[i] = parse_int_at(&p);
}

static void parse_rat_mat(const char *start, const char *end, const char *key, int rows, int cols, rat_t out[MAX_DIM][MAX_DIM]) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && *p != '[') p++;
    p++;
    for (int i = 0; i < rows; i++) {
        while (*p && *p != '[') p++;
        p++;
        for (int j = 0; j < cols; j++) out[i][j] = parse_rat_str_at(&p);
        while (*p && *p != ']') p++;
        p++;
    }
}

static void parse_rat_vec(const char *start, const char *end, const char *key, int len, rat_t out[MAX_DIM]) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && *p != '[') p++;
    p++;
    for (int i = 0; i < len; i++) out[i] = parse_rat_str_at(&p);
}

static int64_t parse_scalar_int(const char *start, const char *end, const char *key) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    return parse_int_at(&p);
}

static rat_t parse_scalar_rat(const char *start, const char *end, const char *key) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    return parse_rat_str_at(&p);
}

static int parse_scalar_bool(const char *start, const char *end, const char *key) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && isspace((unsigned char)*p)) p++;
    if (strncmp(p, "true", 4) == 0) return 1;
    if (strncmp(p, "false", 5) == 0) return 0;
    fprintf(stderr, "FAIL: expected bool for %s\n", key);
    exit(1);
}

static void parse_scalar_str(const char *start, const char *end, const char *key, char *buf, size_t bsz) {
    const char *p = find_key_in_range(start, end, key);
    if (!p) { fprintf(stderr, "FAIL: missing key %s\n", key); exit(1); }
    while (*p && isspace((unsigned char)*p)) p++;
    if (*p != '"') { fprintf(stderr, "FAIL: expected quote for %s\n", key); exit(1); }
    p++;
    size_t i = 0;
    while (*p && *p != '"' && i + 1 < bsz) buf[i++] = *p++;
    buf[i] = '\0';
}

/* MOG Extended Binary Golay Code G_24 from first principles */
static uint32_t golay_words[4096];
static void build_mog_golay(void) {
    static const int add4[4][4] = {{0,1,2,3},{1,0,3,2},{2,3,0,1},{3,2,1,0}};
    static const int mul4[4][4] = {{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
    static const int hg[3][6] = {{1,0,0,1,3,2},{0,1,0,1,2,3},{0,0,1,1,1,1}};
    int col_masks[2][4][2], col_b0[2][4][2], col_cnt[2][4];
    memset(col_cnt, 0, sizeof(col_cnt));
    for (int m = 0; m < 16; m++) {
        int b0 = m & 1, b1 = (m >> 1) & 1, b2 = (m >> 2) & 1, b3 = (m >> 3) & 1;
        int p = b0 ^ b1 ^ b2 ^ b3;
        int s = 0;
        if (b1) s = add4[s][1];
        if (b2) s = add4[s][2];
        if (b3) s = add4[s][3];
        int idx = col_cnt[p][s]++;
        col_masks[p][s][idx] = m;
        col_b0[p][s][idx] = b0;
    }
    int n_out = 0;
    for (int p = 0; p <= 1; p++) {
        for (int a = 0; a < 4; a++)
        for (int b = 0; b < 4; b++)
        for (int c = 0; c < 4; c++) {
            int hw[6];
            for (int j = 0; j < 6; j++)
                hw[j] = add4[mul4[a][hg[0][j]]][add4[mul4[b][hg[1][j]]][mul4[c][hg[2][j]]]];
            for (int mask5 = 0; mask5 < 32; mask5++) {
                int top_sum = 0;
                uint32_t w24 = 0;
                for (int j = 0; j < 5; j++) {
                    int sel = (mask5 >> j) & 1;
                    top_sum ^= col_b0[p][hw[j]][sel];
                    w24 |= ((uint32_t)col_masks[p][hw[j]][sel] << (4 * j));
                }
                int need_b0 = p ^ top_sum;
                int sel5 = (col_b0[p][hw[5]][0] == need_b0) ? 0 : 1;
                w24 |= ((uint32_t)col_masks[p][hw[5]][sel5] << 20);
                golay_words[n_out++] = w24;
            }
        }
    }
    if (n_out != 4096) { fprintf(stderr, "FAIL: Golay size %d\n", n_out); exit(1); }
}

static int in_golay(uint32_t w) {
    for (int i = 0; i < 4096; i++) if (golay_words[i] == w) return 1;
    return 0;
}

static int in_leech_scaled(const int64_t v[24]) {
    int m = (int)(v[0] & 1);
    uint32_t w = 0;
    int64_t sum = 0;
    for (int i = 0; i < 24; i++) {
        if ((int)(v[i] & 1) != m) return 0;
        if (((v[i] - m) >> 1) & 1) w |= (1U << i);
        sum += v[i];
    }
    if (!in_golay(w)) return 0;
    int64_t rem = (sum - 4 * m) % 8;
    return rem == 0;
}

/* Solve y * leech_B == row (upper-triangular 24x24) in exact int64_t */
static void solve_leech_coords_row(const int64_t row[24], const int64_t leech_B[MAX_DIM][MAX_DIM],
                                   int64_t y_out[24], const char *label) {
    int64_t rem[24];
    for (int c = 0; c < 24; c++) rem[c] = row[c];
    for (int i = 0; i < 24; i++) {
        int64_t piv = leech_B[i][i];
        if (piv <= 0 || rem[i] % piv != 0) {
            fprintf(stderr, "FAIL [%s]: row not in Z-span of leech_B at col %d\n", label, i);
            exit(1);
        }
        int64_t yi = rem[i] / piv;
        y_out[i] = yi;
        for (int c = i; c < 24; c++) rem[c] -= yi * leech_B[i][c];
    }
    for (int c = 0; c < 24; c++) {
        if (rem[c] != 0) {
            fprintf(stderr, "FAIL [%s]: residual non-zero in leech_B solve\n", label);
            exit(1);
        }
    }
}

/*
 * 100% Exact Zero-Float Sylvester/Gauss Integer Fincke-Pohst Enumeration.
 */
typedef struct {
    int d;
    int64_t G[MAX_DIM][MAX_DIM];
    int64_t M_min[MAX_DIM + 1];
    int64_t N_r[MAX_DIM][MAX_DIM];
    int64_t dc_num[MAX_DIM];
    int64_t den_c;
    int64_t P_bound;
    int64_t Q_bound;
    int skip_zero;

    int64_t x[MAX_DIM];
    int64_t z[MAX_DIM];
    rat_t best_sq;
    int has_best;
    int count_at_bound;
    int count_strictly_below;
    int64_t stored_z[MAX_CONTACTS_STORE][MAX_DIM];
    int n_stored;
} exact_fp_t;

static void exact_fp_dfs(exact_fp_t *fp, int m, int64_t A_next) {
    if (m < 0) {
        if (fp->skip_zero) {
            int allz = 1;
            for (int i = 0; i < fp->d; i++) if (fp->x[i] != 0) { allz = 0; break; }
            if (allz) return;
        }
        int64_t qf = 0;
        for (int i = 0; i < fp->d; i++)
            for (int j = 0; j < fp->d; j++)
                qf += fp->z[i] * fp->G[i][j] * fp->z[j];
        if (qf != A_next) {
            fprintf(stderr, "FAIL: Sylvester SOS mismatch qf=%lld vs A0=%lld\n", (long long)qf, (long long)A_next);
            exit(1);
        }
        int64_t den2 = fp->den_c * fp->den_c;
        int64_t lhs = qf * fp->Q_bound;
        int64_t rhs = fp->P_bound * den2;
        if (lhs <= rhs) {
            rat_t cur = rat_make(qf, den2);
            if (!fp->has_best || cur.n * fp->best_sq.d < fp->best_sq.n * cur.d) {
                fp->best_sq = cur;
                fp->has_best = 1;
            }
            if (lhs < rhs) {
                fp->count_strictly_below++;
            } else {
                fp->count_at_bound++;
                if (!fp->skip_zero) {
                    if (fp->n_stored >= MAX_CONTACTS_STORE) {
                        fprintf(stderr, "FAIL: per-pair contact buffer exceeded\n");
                        exit(1);
                    }
                    for (int i = 0; i < fp->d; i++) fp->stored_z[fp->n_stored][i] = fp->z[i];
                    fp->n_stored++;
                }
            }
        }
        return;
    }

    int64_t Mm = fp->M_min[m];
    int64_t Mm1 = fp->M_min[m + 1];
    int64_t den2 = fp->den_c * fp->den_c;

    int64_t rem_num = fp->P_bound * den2 * Mm1 - fp->Q_bound * A_next;
    if (rem_num < 0) return;
    int64_t rhs_T2 = (Mm * rem_num) / fp->Q_bound;
    int64_t max_abs_T = isqrt64(rhs_T2);

    int64_t tail = 0;
    for (int l = m + 1; l < fp->d; l++) tail += fp->N_r[m][l] * fp->z[l];

    int64_t denom_x = Mm1 * fp->den_c;
    int64_t lo_num = -max_abs_T - tail - Mm1 * fp->dc_num[m];
    int64_t hi_num =  max_abs_T - tail - Mm1 * fp->dc_num[m];
    int64_t x_lo = ceil_div64(lo_num, denom_x);
    int64_t x_hi = floor_div64(hi_num, denom_x);

    for (int64_t xv = x_lo; xv <= x_hi; xv++) {
        fp->x[m] = xv;
        int64_t zm = fp->den_c * xv + fp->dc_num[m];
        fp->z[m] = zm;
        int64_t Tm = Mm1 * zm + tail;
        if (fp->Q_bound * Tm * Tm <= Mm * rem_num) {
            int64_t num_Am = Mm * A_next + Tm * Tm;
            if (num_Am % Mm1 != 0) {
                fprintf(stderr, "FAIL: Sylvester divisibility failed at m=%d\n", m);
                exit(1);
            }
            exact_fp_dfs(fp, m - 1, num_Am / Mm1);
        }
    }
}

static void setup_fp_basis(exact_fp_t *fp, int d, const int64_t G[MAX_DIM][MAX_DIM],
                           const rat_t R_in[MAX_DIM][MAX_DIM], const rat_t D_in[MAX_DIM]) {
    memset(fp, 0, sizeof(*fp));
    fp->d = d;
    for (int i = 0; i < d; i++)
        for (int j = 0; j < d; j++)
            fp->G[i][j] = G[i][j];

    for (int i = 0; i < d; i++) {
        if (D_in[i].n <= 0) { fprintf(stderr, "FAIL: D[%d] not positive\n", i); exit(1); }
        if (R_in[i][i].n != 1 || R_in[i][i].d != 1) { fprintf(stderr, "FAIL: R[%d][%d] != 1\n", i, i); exit(1); }
        for (int j = 0; j < i; j++) {
            if (R_in[i][j].n != 0) { fprintf(stderr, "FAIL: R not upper triangular\n"); exit(1); }
        }
    }
    for (int i = 0; i < d; i++) {
        for (int j = 0; j < d; j++) {
            rat_t s = rat_make(0, 1);
            int lim = i < j ? i : j;
            for (int k = 0; k <= lim; k++) {
                s = rat_add(s, rat_mul(R_in[k][i], rat_mul(D_in[k], R_in[k][j])));
            }
            if (s.d != 1 || s.n != G[i][j]) {
                fprintf(stderr, "FAIL: R^T D R != G at (%d,%d)\n", i, j);
                exit(1);
            }
        }
    }

    fp->M_min[0] = 1;
    for (int m = 0; m < d; m++) {
        int64_t sub[MAX_DIM][MAX_DIM];
        for (int a = 0; a <= m; a++)
            for (int b = 0; b <= m; b++)
                sub[a][b] = G[a][b];
        int64_t det_m = bareiss_det(m + 1, sub);
        if (det_m <= 0) { fprintf(stderr, "FAIL: non-positive minor %d\n", m + 1); exit(1); }
        fp->M_min[m + 1] = det_m;
        rat_t expected_d = rat_make(fp->M_min[m + 1], fp->M_min[m]);
        if (expected_d.n != D_in[m].n || expected_d.d != D_in[m].d) {
            fprintf(stderr, "FAIL: D[%d] mismatch vs minors\n", m);
            exit(1);
        }
        for (int l = m; l < d; l++) {
            rat_t scaled = rat_mul(rat_make(det_m, 1), R_in[m][l]);
            if (scaled.d != 1) { fprintf(stderr, "FAIL: M_{m+1}*R not integer\n"); exit(1); }
            fp->N_r[m][l] = scaled.n;
        }
    }
}

typedef struct {
    int i;
    int j;
    int64_t z[19];
    int64_t w[19];
} contact_rec_t;

static int64_t mod_pow(int64_t base, int64_t exp, int64_t mod) {
    int64_t res = 1;
    base %= mod;
    if (base < 0) base += mod;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}

static void fill_contact_row_mod(const contact_rec_t *cr, int full_mode, int64_t prime, int64_t *row) {
    int pos = 0;
    if (full_mode) {
        for (int a = 0; a < 19; a++) {
            int64_t dval = (cr->z[a] * cr->z[a]) % prime;
            if (dval < 0) dval += prime;
            row[pos++] = dval;
            for (int b = a + 1; b < 19; b++) {
                int64_t oval = (2LL * cr->z[a] * cr->z[b]) % prime;
                if (oval < 0) oval += prime;
                row[pos++] = oval;
            }
        }
    }
    for (int c = 0; c < TRANS_COLS; c++) row[pos + c] = 0;
    if (cr->j > 0) {
        int base = pos + (cr->j - 1) * 19;
        for (int m = 0; m < 19; m++) {
            int64_t v = (row[base + m] + cr->w[m]) % prime;
            if (v < 0) v += prime;
            row[base + m] = v;
        }
    }
    if (cr->i > 0) {
        int base = pos + (cr->i - 1) * 19;
        for (int m = 0; m < 19; m++) {
            int64_t v = (row[base + m] - cr->w[m]) % prime;
            if (v < 0) v += prime;
            row[base + m] = v;
        }
    }
}

/*
 * Incremental row-echelon elimination over F_p in round-robin pair order.
 * Every nonzero pivot certifies an integer subdeterminant != 0 mod p, hence != 0 over Q,
 * establishing the exact lower bound on the bilateral bar-framework contact-Jacobian rank.
 */
static int incremental_rank_mod_p(int n_pairs, const int *pair_start, const int *pair_len,
                                  const contact_rec_t *contacts, int full_mode,
                                  int rank_upper, int64_t prime) {
    int ncols = full_mode ? FULL_COLS : TRANS_COLS;
    int64_t *piv_mat = (int64_t *)calloc((size_t)ncols * (size_t)ncols, sizeof(int64_t));
    int *has_piv = (int *)calloc((size_t)ncols, sizeof(int));
    if (!piv_mat || !has_piv) { fprintf(stderr, "FAIL: OOM\n"); exit(1); }

    int max_len = 0;
    for (int p = 0; p < n_pairs; p++) if (pair_len[p] > max_len) max_len = pair_len[p];

    int rk = 0;
    int64_t row[FULL_COLS];
    for (int off = 0; off < max_len && rk < rank_upper; off++) {
        for (int p = 0; p < n_pairs && rk < rank_upper; p++) {
            if (off >= pair_len[p]) continue;
            fill_contact_row_mod(&contacts[pair_start[p] + off], full_mode, prime, row);
            for (int c = 0; c < ncols; c++) {
                if (row[c] != 0) {
                    if (has_piv[c]) {
                        int64_t f = row[c];
                        const int64_t *prow = piv_mat + (size_t)c * (size_t)ncols;
                        for (int j = c; j < ncols; j++) {
                            if (prow[j] != 0) {
                                int64_t sub = (f * prow[j]) % prime;
                                row[j] -= sub;
                                if (row[j] < 0) row[j] += prime;
                            }
                        }
                    } else {
                        int64_t inv = mod_pow(row[c], prime - 2, prime);
                        int64_t *prow = piv_mat + (size_t)c * (size_t)ncols;
                        for (int j = c; j < ncols; j++) prow[j] = (row[j] * inv) % prime;
                        has_piv[c] = 1;
                        rk++;
                        break;
                    }
                }
            }
        }
    }
    free(has_piv);
    free(piv_mat);
    return rk;
}

typedef struct {
    int64_t det_G;
    int leech_sat;
    int sym_trans_stab_size;
    int norm4_L;
    int tau[6];
    int tau_sorted[6];
    int tau_min;
    int tau_max;
    rat_t tau_avg;
    int tight_pairs;
    int connected;
    int triangles_translate_graph;
    int bilat_rank_trans;
    int bilat_nullity_trans;
    int bilat_rank_full;
    int bilat_nullity_full;
} packing_result_t;

static void sort_ints(int n, int *a) {
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[i]) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}

static packing_result_t verify_one_d19_packing(const char *sec_start, const char *sec_end,
                                               const int64_t leech_B[MAX_DIM][MAX_DIM],
                                               const char *label, int corrupt_test) {
    int64_t A_sec[MAX_DIM][MAX_DIM], ZA_T[MAX_DIM][MAX_DIM];
    int64_t B_orig[MAX_DIM][MAX_DIM], U_lll[MAX_DIM][MAX_DIM], B_lll[MAX_DIM][MAX_DIM], ZB_T[MAX_DIM][MAX_DIM];
    int64_t YA[MAX_DIM][MAX_DIM], YB[MAX_DIM][MAX_DIM];
    int64_t G[MAX_DIM][MAX_DIM], C_num[MAX_DIM][MAX_DIM], T_amb[MAX_DIM][MAX_DIM];
    rat_t R_in[MAX_DIM][MAX_DIM], D_in[MAX_DIM];

    char parsed_name[128];
    parse_scalar_str(sec_start, sec_end, "name", parsed_name, sizeof(parsed_name));
    if (!corrupt_test && strcmp(parsed_name, label) != 0) {
        fprintf(stderr, "FAIL [%s]: unexpected entry name %s\n", label, parsed_name);
        exit(1);
    }

    parse_int_mat(sec_start, sec_end, "leech_section_A_scaled", 5, 24, A_sec);
    parse_int_mat(sec_start, sec_end, "leech_section_A_right_inv_T_5x24", 5, 24, ZA_T);
    parse_int_mat(sec_start, sec_end, "leech_complement_B_original_scaled", 19, 24, B_orig);
    parse_int_mat(sec_start, sec_end, "unimodular_U_lll", 19, 19, U_lll);
    int64_t det_U_cert = parse_scalar_int(sec_start, sec_end, "det_U_lll");
    parse_int_mat(sec_start, sec_end, "leech_complement_B_lll_scaled", 19, 24, B_lll);
    parse_int_mat(sec_start, sec_end, "leech_complement_B_lll_right_inv_T_19x24", 19, 24, ZB_T);
    parse_int_mat(sec_start, sec_end, "gram_G_19x19", 19, 19, G);
    parse_rat_mat(sec_start, sec_end, "cholesky_R_19x19", 19, 19, R_in);
    parse_rat_vec(sec_start, sec_end, "cholesky_D_19", 19, D_in);
    int64_t den_c = parse_scalar_int(sec_start, sec_end, "translates_basis_coords_den");
    parse_int_mat(sec_start, sec_end, "translates_basis_coords_num", 6, 19, C_num);
    int64_t den_amb = parse_scalar_int(sec_start, sec_end, "translates_ambient_24d_den");
    parse_int_mat(sec_start, sec_end, "translates_ambient_24d_num", 6, 24, T_amb);

    if (corrupt_test) {
        C_num[1][0] += 30;
    }

    /* 1. Verify MOG Leech membership, integer saturation (Y*Z == I), orthogonality, unimodularity of U_lll, and B_lll * B_lll^T == 8 * G */
    for (int i = 0; i < 5; i++) {
        if (!in_leech_scaled(A_sec[i])) { fprintf(stderr, "FAIL [%s]: A row %d not in Leech\n", label, i); exit(1); }
        solve_leech_coords_row(A_sec[i], leech_B, YA[i], label);
    }
    for (int a = 0; a < 5; a++) {
        for (int b = 0; b < 5; b++) {
            int64_t dot = 0;
            for (int c = 0; c < 24; c++) dot += YA[a][c] * ZA_T[b][c];
            if (dot != (a == b ? 1 : 0)) {
                fprintf(stderr, "FAIL [%s]: section A saturation right-inverse failed at (%d,%d)\n", label, a, b);
                exit(1);
            }
        }
    }

    int64_t K_sec[MAX_DIM][MAX_DIM];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            int64_t dot = 0;
            for (int c = 0; c < 24; c++) dot += A_sec[i][c] * A_sec[j][c];
            if (dot % 8 != 0) { fprintf(stderr, "FAIL [%s]: A*A^T not divisible by 8\n", label); exit(1); }
            K_sec[i][j] = dot / 8;
        }
    }
    if (bareiss_det(5, K_sec) != 300) { fprintf(stderr, "FAIL [%s]: det(K_sec) != 300\n", label); exit(1); }

    for (int i = 0; i < 19; i++) {
        if (!in_leech_scaled(B_orig[i])) { fprintf(stderr, "FAIL [%s]: B_orig row %d not in Leech\n", label, i); exit(1); }
        for (int r = 0; r < 5; r++) {
            int64_t dot = 0;
            for (int c = 0; c < 24; c++) dot += B_orig[i][c] * A_sec[r][c];
            if (dot != 0) { fprintf(stderr, "FAIL [%s]: B_orig not orthogonal to A\n", label); exit(1); }
        }
    }
    int64_t det_U = bareiss_det(19, U_lll);
    if (det_U != det_U_cert || (det_U != 1 && det_U != -1)) {
        fprintf(stderr, "FAIL [%s]: det(U_lll)=%lld invalid\n", label, (long long)det_U); exit(1);
    }
    for (int i = 0; i < 19; i++) {
        for (int c = 0; c < 24; c++) {
            int64_t s = 0;
            for (int k = 0; k < 19; k++) s += U_lll[i][k] * B_orig[k][c];
            if (s != B_lll[i][c]) { fprintf(stderr, "FAIL [%s]: U_lll * B_orig != B_lll\n", label); exit(1); }
        }
        solve_leech_coords_row(B_lll[i], leech_B, YB[i], label);
    }
    for (int a = 0; a < 19; a++) {
        for (int b = 0; b < 19; b++) {
            int64_t dot = 0;
            for (int c = 0; c < 24; c++) dot += YB[a][c] * ZB_T[b][c];
            if (dot != (a == b ? 1 : 0)) {
                fprintf(stderr, "FAIL [%s]: complement B_lll saturation right-inverse failed at (%d,%d)\n", label, a, b);
                exit(1);
            }
        }
    }

    for (int i = 0; i < 19; i++) {
        for (int j = 0; j < 19; j++) {
            int64_t dot = 0;
            for (int c = 0; c < 24; c++) dot += B_lll[i][c] * B_lll[j][c];
            if (dot != 8 * G[i][j]) { fprintf(stderr, "FAIL [%s]: B_lll Gram != 8*G\n", label); exit(1); }
        }
    }

    if (!corrupt_test) {
        if (den_amb <= 0 || den_c <= 0) { fprintf(stderr, "FAIL [%s]: non-positive den\n", label); exit(1); }
        for (int c = 0; c < 24; c++) {
            if (T_amb[0][c] != 0) { fprintf(stderr, "FAIL [%s]: T_amb[0] != 0\n", label); exit(1); }
        }
        for (int m = 0; m < 19; m++) {
            if (C_num[0][m] != 0) { fprintf(stderr, "FAIL [%s]: C_num[0] != 0\n", label); exit(1); }
        }
        int64_t prod_den = den_amb * den_c;
        for (int s = 0; s < 6; s++) {
            for (int r = 0; r < 5; r++) {
                int64_t dot = 0;
                for (int c = 0; c < 24; c++) dot += T_amb[s][c] * A_sec[r][c];
                if (dot != 0) { fprintf(stderr, "FAIL [%s]: T_amb not orthogonal to A\n", label); exit(1); }
            }
            /* Since L = K^perp cap Lambda_24 is proved saturated above, (T_amb/den_amb - C_num/den_c * B_lll) lies in L
               iff it is an integral vector in sqrt(8)*Lambda_24 orthogonal to A_sec. */
            int64_t diff_vec[24];
            for (int c = 0; c < 24; c++) {
                int64_t bsum = 0;
                for (int m = 0; m < 19; m++) bsum += C_num[s][m] * B_lll[m][c];
                int64_t num_sc = den_c * T_amb[s][c] - den_amb * bsum;
                if (num_sc % prod_den != 0) {
                    fprintf(stderr, "FAIL [%s]: 24D vs 19D translate non-integral difference\n", label);
                    exit(1);
                }
                diff_vec[c] = num_sc / prod_den;
            }
            if (!in_leech_scaled(diff_vec)) {
                fprintf(stderr, "FAIL [%s]: 24D vs 19D translate difference not in Leech\n", label);
                exit(1);
            }
            for (int r = 0; r < 5; r++) {
                int64_t dot = 0;
                for (int c = 0; c < 24; c++) dot += diff_vec[c] * A_sec[r][c];
                if (dot != 0) { fprintf(stderr, "FAIL [%s]: 24D vs 19D diff not perp A\n", label); exit(1); }
            }
        }
    }

    /* 2. Setup exact Sylvester-Cholesky Fincke-Pohst on G */
    static exact_fp_t fp;
    setup_fp_basis(&fp, 19, G, R_in, D_in);
    int64_t det_G = fp.M_min[19];

    /* 3. Intra-lattice SVP/kissing of L at norm^2 <= 4 */
    memset(fp.dc_num, 0, sizeof(fp.dc_num));
    fp.den_c = 1;
    fp.P_bound = 4;
    fp.Q_bound = 1;
    fp.skip_zero = 1;
    fp.has_best = 0;
    fp.count_at_bound = 0;
    fp.count_strictly_below = 0;
    fp.n_stored = 0;
    exact_fp_dfs(&fp, 18, 0);
    if (!corrupt_test && (fp.count_strictly_below > 0 || fp.best_sq.n != 4 || fp.best_sq.d != 1)) {
        fprintf(stderr, "FAIL [%s]: intra-lattice min_sq != 4\n", label);
        exit(1);
    }
    int norm4_L = fp.count_at_bound;

    /* 4. Primitivity & Sym_trans coset-stabilizer check:
     *    (a) No two translates congruent mod Z^19.
     *    (b) (c_i + c_s) mod Z^19 preserves {c_0..c_5} mod Z^19 iff s == 0, proving Sym_trans(P) == L.
     */
    for (int i = 0; i < 6; i++) {
        for (int j = i + 1; j < 6; j++) {
            int all_div = 1;
            for (int m = 0; m < 19; m++) {
                if ((C_num[j][m] - C_num[i][m]) % den_c != 0) { all_div = 0; break; }
            }
            if (all_div) { fprintf(stderr, "FAIL [%s]: duplicate translate mod L\n", label); exit(1); }
        }
    }
    int stab_cnt = 0;
    int stab_zero = 0;
    for (int s = 0; s < 6; s++) {
        int preserves_all = 1;
        for (int i = 0; i < 6; i++) {
            int found_j = 0;
            for (int j = 0; j < 6; j++) {
                int cong = 1;
                for (int m = 0; m < 19; m++) {
                    if ((C_num[i][m] + C_num[s][m] - C_num[j][m]) % den_c != 0) { cong = 0; break; }
                }
                if (cong) { found_j = 1; break; }
            }
            if (!found_j) { preserves_all = 0; break; }
        }
        if (preserves_all) {
            stab_cnt++;
            if (s == 0) stab_zero = 1;
        }
    }
    if (!corrupt_test && (stab_cnt != 1 || !stab_zero)) {
        fprintf(stderr, "FAIL [%s]: Sym_trans coset stabilizer size=%d != 1\n", label, stab_cnt);
        exit(1);
    }

    /* 5. Exhaustive Fincke-Pohst over all 15 translate pairs (0 <= i < j < 6) at target 52/15 */
    packing_result_t res;
    memset(&res, 0, sizeof(res));
    res.det_G = det_G;
    res.leech_sat = 1;
    res.sym_trans_stab_size = stab_cnt;
    res.norm4_L = norm4_L;

    int adj_t[6][6];
    memset(adj_t, 0, sizeof(adj_t));

    contact_rec_t *contacts = (contact_rec_t *)calloc(MAX_TOTAL_CONTACTS, sizeof(contact_rec_t));
    if (!contacts) { fprintf(stderr, "FAIL: OOM\n"); exit(1); }
    int n_contacts = 0;
    int pair_start[15], pair_len[15], n_tpairs = 0;

    for (int i = 0; i < 6; i++) {
        for (int j = i + 1; j < 6; j++) {
            for (int m = 0; m < 19; m++) fp.dc_num[m] = C_num[j][m] - C_num[i][m];
            fp.den_c = den_c;
            fp.P_bound = 52;
            fp.Q_bound = 15;
            fp.skip_zero = 0;
            fp.has_best = 0;
            fp.count_at_bound = 0;
            fp.count_strictly_below = 0;
            fp.n_stored = 0;
            exact_fp_dfs(&fp, 18, 0);

            if (fp.count_strictly_below > 0) {
                free(contacts);
                if (corrupt_test == 1) {
                    printf("[C99 NEGATIVE CONTROL] Perturbed packing rejected as expected: pair (%d,%d) has %d vectors strictly below 52/15 (min_sq = %lld/%lld)\n",
                           i, j, fp.count_strictly_below, (long long)fp.best_sq.n, (long long)fp.best_sq.d);
                    res.det_G = -1;
                    return res;
                }
                if (corrupt_test == 2) {
                    printf("FAIL: corrupted certificate rejected at pair (%d,%d) with min_sq = %lld/%lld strictly_below 52/15\n",
                           i, j, (long long)fp.best_sq.n, (long long)fp.best_sq.d);
                    exit(1);
                }
                fprintf(stderr, "FAIL [%s]: pair (%d,%d) violates min_sq strictly_below 52/15\n", label, i, j);
                exit(1);
            }
            if (fp.count_at_bound > 0) {
                adj_t[i][j] = adj_t[j][i] = 1;
                res.tight_pairs++;
                res.tau[i] += fp.count_at_bound;
                res.tau[j] += fp.count_at_bound;
                if (fp.n_stored != fp.count_at_bound || n_contacts + fp.n_stored > MAX_TOTAL_CONTACTS) {
                    fprintf(stderr, "FAIL [%s]: contact count overflow\n", label);
                    exit(1);
                }
                pair_start[n_tpairs] = n_contacts;
                pair_len[n_tpairs] = fp.n_stored;
                n_tpairs++;
                for (int c = 0; c < fp.n_stored; c++) {
                    contact_rec_t *cr = &contacts[n_contacts++];
                    cr->i = i;
                    cr->j = j;
                    for (int m = 0; m < 19; m++) cr->z[m] = fp.stored_z[c][m];
                    for (int m = 0; m < 19; m++) {
                        int64_t s = 0;
                        for (int l = 0; l < 19; l++) s += G[m][l] * cr->z[l];
                        cr->w[m] = s;
                    }
                }
            }
        }
    }
    if (corrupt_test) {
        free(contacts);
        fprintf(stderr, "FAIL: negative control did NOT trigger violation!\n");
        exit(1);
    }

    int sum_tau = 0;
    res.tau_min = res.tau[0];
    res.tau_max = res.tau[0];
    for (int i = 0; i < 6; i++) {
        res.tau_sorted[i] = res.tau[i];
        if (res.tau[i] < res.tau_min) res.tau_min = res.tau[i];
        if (res.tau[i] > res.tau_max) res.tau_max = res.tau[i];
        sum_tau += res.tau[i];
    }
    if (2 * n_contacts != sum_tau) { fprintf(stderr, "FAIL [%s]: 2*n_contacts != sum_tau\n", label); exit(1); }
    sort_ints(6, res.tau_sorted);
    res.tau_avg = rat_make(sum_tau, 6);

    /* Connected components & triangles of 6-translate tight-contact graph */
    int comp[6] = {-1, -1, -1, -1, -1, -1};
    int n_comp = 0;
    for (int s = 0; s < 6; s++) {
        if (comp[s] < 0) {
            comp[s] = n_comp;
            int q[6], qh = 0, qt = 0;
            q[qt++] = s;
            while (qh < qt) {
                int u = q[qh++];
                for (int v = 0; v < 6; v++) {
                    if (adj_t[u][v] && comp[v] < 0) {
                        comp[v] = n_comp;
                        q[qt++] = v;
                    }
                }
            }
            n_comp++;
        }
    }
    res.connected = (n_comp == 1) ? 1 : 0;

    int tri = 0;
    for (int a = 0; a < 6; a++)
        for (int b = a + 1; b < 6; b++)
            for (int c = b + 1; c < 6; c++)
                if (adj_t[a][b] && adj_t[b][c] && adj_t[a][c]) tri++;
    res.triangles_translate_graph = tri;

    /*
     * Exact Q-rank of bilateral bar-framework contact-Jacobian matrices J_trans (95 cols) and J_full (285 cols):
     *   Upper bound: each non-root connected component k >= 1 gives 19 independent integer vectors in ker_Z(J).
     *   Lower bound: non-zero subdeterminant modulo two independent primes 1000000007 and 1000000009.
     */
    for (int k = 1; k < n_comp; k++) {
        if (comp[0] == k) { fprintf(stderr, "FAIL: component 0 misindexed\n"); exit(1); }
        for (int idx = 0; idx < n_contacts; idx++) {
            int coeff = ((comp[contacts[idx].j] == k) ? 1 : 0) - ((comp[contacts[idx].i] == k) ? 1 : 0);
            for (int m = 0; m < 19; m++) {
                if ((int64_t)coeff * contacts[idx].w[m] != 0) {
                    fprintf(stderr, "FAIL [%s]: cluster nullspace check failed\n", label);
                    exit(1);
                }
            }
        }
    }
    int trans_rank_upper = TRANS_COLS - 19 * (n_comp - 1);
    int full_rank_upper  = FULL_COLS  - 19 * (n_comp - 1);

    int trk1 = incremental_rank_mod_p(n_tpairs, pair_start, pair_len, contacts, 0, trans_rank_upper, 1000000007LL);
    int trk2 = incremental_rank_mod_p(n_tpairs, pair_start, pair_len, contacts, 0, trans_rank_upper, 1000000009LL);
    if (trk1 != trk2 || trk1 != trans_rank_upper) {
        fprintf(stderr, "FAIL [%s]: bilateral_contact_rank_trans %d/%d != upper %d\n", label, trk1, trk2, trans_rank_upper);
        exit(1);
    }
    int frk1 = incremental_rank_mod_p(n_tpairs, pair_start, pair_len, contacts, 1, full_rank_upper, 1000000007LL);
    int frk2 = incremental_rank_mod_p(n_tpairs, pair_start, pair_len, contacts, 1, full_rank_upper, 1000000009LL);
    if (frk1 != frk2 || frk1 != full_rank_upper) {
        fprintf(stderr, "FAIL [%s]: bilateral_contact_rank_full %d/%d != upper %d\n", label, frk1, frk2, full_rank_upper);
        exit(1);
    }
    free(contacts);

    res.bilat_rank_trans = trk1;
    res.bilat_nullity_trans = TRANS_COLS - trk1;
    res.bilat_rank_full = frk1;
    res.bilat_nullity_full = FULL_COLS - frk1;

    /* Verify expected_invariants block in certificate */
    const char *exp_p = find_key_in_range(sec_start, sec_end, "expected_invariants");
    if (!exp_p) { fprintf(stderr, "FAIL [%s]: missing expected_invariants\n", label); exit(1); }
    const char *exp_end = find_matching_brace(exp_p);
    int64_t exp_tau[6], exp_tau_sorted[6];
    parse_int_vec(exp_p, exp_end, "kissing_per_translate", 6, exp_tau);
    parse_int_vec(exp_p, exp_end, "kissing_sorted", 6, exp_tau_sorted);
    rat_t exp_avg = parse_scalar_rat(exp_p, exp_end, "kissing_avg");
    rat_t exp_lmin = parse_scalar_rat(exp_p, exp_end, "intra_lattice_min_sq");
    rat_t exp_pmin = parse_scalar_rat(exp_p, exp_end, "packing_min_sq");

    if (res.det_G != parse_scalar_int(exp_p, exp_end, "det_G") ||
        res.leech_sat != parse_scalar_bool(exp_p, exp_end, "leech_saturation_unimodular") ||
        res.sym_trans_stab_size != (int)parse_scalar_int(exp_p, exp_end, "sym_trans_stabilizer_size") ||
        exp_lmin.n != 4 || exp_lmin.d != 1 ||
        res.norm4_L != (int)parse_scalar_int(exp_p, exp_end, "intra_lattice_norm4_count") ||
        exp_pmin.n != 52 || exp_pmin.d != 15 ||
        res.tau_min != (int)parse_scalar_int(exp_p, exp_end, "kissing_min") ||
        res.tau_max != (int)parse_scalar_int(exp_p, exp_end, "kissing_max") ||
        res.tau_avg.n != exp_avg.n || res.tau_avg.d != exp_avg.d ||
        res.tight_pairs != (int)parse_scalar_int(exp_p, exp_end, "tight_translate_pairs") ||
        res.triangles_translate_graph != (int)parse_scalar_int(exp_p, exp_end, "translate_contact_triangles") ||
        res.connected != parse_scalar_bool(exp_p, exp_end, "translate_contact_graph_connected") ||
        res.bilat_rank_trans != (int)parse_scalar_int(exp_p, exp_end, "bilateral_contact_rank_trans") ||
        res.bilat_nullity_trans != (int)parse_scalar_int(exp_p, exp_end, "bilateral_contact_nullity_trans") ||
        res.bilat_rank_full != (int)parse_scalar_int(exp_p, exp_end, "bilateral_contact_rank_full") ||
        res.bilat_nullity_full != (int)parse_scalar_int(exp_p, exp_end, "bilateral_contact_nullity_full")) {
        fprintf(stderr, "FAIL [%s]: expected_invariants mismatch\n", label);
        exit(1);
    }
    for (int i = 0; i < 6; i++) {
        if (res.tau[i] != (int)exp_tau[i] || res.tau_sorted[i] != (int)exp_tau_sorted[i]) {
            fprintf(stderr, "FAIL [%s]: kissing vector mismatch\n", label);
            exit(1);
        }
    }

    printf("[C99 PROVED] %s: det(G)=%lld, leech_sat=%d, sym_trans_stab_size=%d, norm4(L)=%d, min_sq=52/15, tau_sorted=(%d,%d,%d,%d,%d,%d), min=%d, max=%d, avg=%lld/%lld, tight_pairs=%d/15, triangles=%d, connected=%d, bilateral_contact_rank_trans=%d/95, bilateral_contact_nullity_trans=%d, bilateral_contact_rank_full=%d/285, bilateral_contact_nullity_full=%d\n",
           label, (long long)res.det_G, res.leech_sat, res.sym_trans_stab_size, res.norm4_L,
           res.tau_sorted[0], res.tau_sorted[1], res.tau_sorted[2],
           res.tau_sorted[3], res.tau_sorted[4], res.tau_sorted[5],
           res.tau_min, res.tau_max, (long long)res.tau_avg.n, (long long)res.tau_avg.d,
           res.tight_pairs, res.triangles_translate_graph, res.connected,
           res.bilat_rank_trans, res.bilat_nullity_trans, res.bilat_rank_full, res.bilat_nullity_full);
    return res;
}

int main(int argc, char **argv) {
    int cli_corrupt = 0;
    if (argc >= 3 && strcmp(argv[2], "--corrupt") == 0) cli_corrupt = 1;
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <certificate.json> [--corrupt]\n", argv[0]);
        return 1;
    }
    FILE *fp_in = fopen(argv[1], "rb");
    if (!fp_in) { perror("fopen"); return 1; }
    fseek(fp_in, 0, SEEK_END);
    long fsz = ftell(fp_in);
    fseek(fp_in, 0, SEEK_SET);
    char *json = (char *)malloc((size_t)fsz + 1);
    if (!json || (long)fread(json, 1, (size_t)fsz, fp_in) != fsz) { fprintf(stderr, "FAIL: fread\n"); return 1; }
    json[fsz] = '\0';
    fclose(fp_in);
    const char *jend = json + fsz;

    /* Verify top-level certificate metadata */
    char schema_buf[128], target_buf[128], claim_buf[64], formula_buf[128];
    parse_scalar_str(json, jend, "schema", schema_buf, sizeof(schema_buf));
    parse_scalar_str(json, jend, "target_id", target_buf, sizeof(target_buf));
    parse_scalar_str(json, jend, "claim_level", claim_buf, sizeof(claim_buf));
    parse_scalar_str(json, jend, "cohn_live_center_density_formula", formula_buf, sizeof(formula_buf));
    rat_t top_min_sq = parse_scalar_rat(json, jend, "minimal_squared_distance");
    rat_t top_rad_sq = parse_scalar_rat(json, jend, "packing_radius_squared");
    if (strcmp(schema_buf, "v3r1t4s-periodic-sphere-packing-certificate-v2") != 0 ||
        strcmp(target_buf, "cohn-sphere-packing-density-table") != 0 ||
        strcmp(claim_buf, "partial_win_p1") != 0 ||
        strcmp(formula_buf, "3^(-9) * 5^(-21/2) * 13^(19/2)") != 0 ||
        parse_scalar_int(json, jend, "dimension") != 19 ||
        parse_scalar_int(json, jend, "num_translates") != 6 ||
        top_min_sq.n != 52 || top_min_sq.d != 15 ||
        top_rad_sq.n != 13 || top_rad_sq.d != 15) {
        fprintf(stderr, "FAIL: top-level metadata mismatch\n");
        return 1;
    }

    /* 0. Build MOG Golay code & verify Leech HNF basis det == 2^36 */
    build_mog_golay();
    int64_t leech_B[MAX_DIM][MAX_DIM];
    parse_int_mat(json, jend, "leech_lattice_basis_scaled_sqrt8", 24, 24, leech_B);
    int64_t det_leech = 1;
    for (int i = 0; i < 24; i++) {
        if (!in_leech_scaled(leech_B[i])) { fprintf(stderr, "FAIL: leech_B row %d invalid\n", i); return 1; }
        for (int j = 0; j < i; j++) if (leech_B[i][j] != 0) { fprintf(stderr, "FAIL: leech_B[%d][%d] != 0\n", i, j); return 1; }
        det_leech *= leech_B[i][i];
    }
    if (det_leech != (1LL << 36)) { fprintf(stderr, "FAIL: det(leech_B)=%lld != 2^36\n", (long long)det_leech); return 1; }
    printf("[C99 CALIBRATION] MOG Golay G_24 (4096 words) and unimodular Leech lattice basis (det(Lambda_24)=1) verified.\n");

    /* 1. Positive Calibration: E_8 lattice */
    const char *e8_p = find_key_in_range(json, jend, "calibration_e8");
    const char *e8_end = find_matching_brace(e8_p);
    int64_t G_e8[MAX_DIM][MAX_DIM];
    rat_t R_e8[MAX_DIM][MAX_DIM], D_e8[MAX_DIM];
    parse_int_mat(e8_p, e8_end, "gram_G_8x8", 8, 8, G_e8);
    parse_rat_mat(e8_p, e8_end, "cholesky_R_8x8", 8, 8, R_e8);
    parse_rat_vec(e8_p, e8_end, "cholesky_D_8", 8, D_e8);
    static exact_fp_t fp_e8;
    setup_fp_basis(&fp_e8, 8, G_e8, R_e8, D_e8);
    fp_e8.den_c = 1; fp_e8.P_bound = 2; fp_e8.Q_bound = 1; fp_e8.skip_zero = 1;
    exact_fp_dfs(&fp_e8, 7, 0);
    if (fp_e8.M_min[8] != 1 || fp_e8.count_strictly_below != 0 || fp_e8.count_at_bound != 240) {
        fprintf(stderr, "FAIL: E8 calibration failed\n"); return 1;
    }
    printf("[C99 CALIBRATION] E_8 verified: det=1, min_sq=2, kissing=240, center_density=1/16.\n");

    /* 2. Certify New Packing P19_II_vtx & Reference Packing Chen et al. (2025) */
    const char *new_p = find_key_in_range(json, jend, "new_packing");
    const char *new_end = find_matching_brace(new_p);
    const char *ref_p = find_key_in_range(json, jend, "reference_packing_chen2025");
    const char *ref_end = find_matching_brace(ref_p);

    packing_result_t r_new = verify_one_d19_packing(new_p, new_end, leech_B, "P19_II_vtx", cli_corrupt ? 2 : 0);
    packing_result_t r_ref = verify_one_d19_packing(ref_p, ref_end, leech_B, "P19_ChenHuLiWangWu2025_ref", 0);

    /* 3. Exact BigUInt Center Density Proof */
    char num_str[128], den_str[128];
    parse_scalar_str(json, jend, "center_density_squared_num", num_str, sizeof(num_str));
    parse_scalar_str(json, jend, "center_density_squared_den", den_str, sizeof(den_str));
    biguint_t cert_num, cert_den, pow13_19, pow3_18_5_21, lhs_cd, rhs_cd;
    big_from_dec(&cert_num, num_str);
    big_from_dec(&cert_den, den_str);

    big_from_u64(&pow13_19, 1);
    for (int i = 0; i < 19; i++) big_mul_u64(&pow13_19, 13ULL);
    big_from_u64(&pow3_18_5_21, 1);
    for (int i = 0; i < 18; i++) big_mul_u64(&pow3_18_5_21, 3ULL);
    for (int i = 0; i < 21; i++) big_mul_u64(&pow3_18_5_21, 5ULL);

    if (big_cmp(&cert_num, &pow13_19) != 0 || big_cmp(&cert_den, &pow3_18_5_21) != 0) {
        fprintf(stderr, "FAIL: certificate center_density_squared != 13^19 / (3^18 * 5^21)\n");
        return 1;
    }

    big_from_u64(&lhs_cd, 36ULL);
    for (int i = 0; i < 19; i++) big_mul_u64(&lhs_cd, 52ULL);
    for (int i = 0; i < 18; i++) big_mul_u64(&lhs_cd, 3ULL);
    for (int i = 0; i < 21; i++) big_mul_u64(&lhs_cd, 5ULL);

    big_from_u64(&rhs_cd, (uint64_t)r_new.det_G);
    for (int i = 0; i < 19; i++) big_mul_u64(&rhs_cd, 60ULL);
    for (int i = 0; i < 19; i++) big_mul_u64(&rhs_cd, 13ULL);

    if (big_cmp(&lhs_cd, &rhs_cd) != 0 || r_new.det_G != r_ref.det_G) {
        fprintf(stderr, "FAIL: center density cross-product mismatch!\n");
        return 1;
    }
    char p13_buf[128], p35_buf[128];
    big_to_str(&pow13_19, p13_buf, sizeof(p13_buf));
    big_to_str(&pow3_18_5_21, p35_buf, sizeof(p35_buf));
    printf("[C99 PROVED] Exact center density squared = %s / %s == (3^(-9) * 5^(-21/2) * 13^(19/2))^2 (MATCHES COHN LIVE RECORD).\n",
           p13_buf, p35_buf);

    /* 4. Strict Non-Isometry, Non-Subsumption & Kissing-Stratum Vertex Isolation Assertions */
    if (r_new.norm4_L == r_ref.norm4_L || !r_new.leech_sat || !r_ref.leech_sat ||
        r_new.sym_trans_stab_size != 1 || r_ref.sym_trans_stab_size != 1) {
        fprintf(stderr, "FAIL: Sym_trans / saturation / norm4 non-isometry check failed\n"); return 1;
    }
    int same_tau = 1;
    for (int i = 0; i < 6; i++) if (r_new.tau_sorted[i] != r_ref.tau_sorted[i]) same_tau = 0;
    if (same_tau) { fprintf(stderr, "FAIL: kissing multisets are identical\n"); return 1; }
    if (r_new.bilat_rank_trans != 95 || r_new.bilat_nullity_trans != 0 ||
        r_new.bilat_rank_full != 285 || r_new.bilat_nullity_full != 0 || !r_new.connected) {
        fprintf(stderr, "FAIL: new packing does not have full bilateral contact-Jacobian rank or connectivity\n"); return 1;
    }
    if (!(r_new.tau_max < r_ref.tau_min)) {
        fprintf(stderr, "FAIL: expected max(tau_new) strictly_below min(tau_ref)\n"); return 1;
    }
    printf("[C99 PROVED] Strict Non-Isometry & Kissing-Stratum Vertex Isolation certified: leech_sat=1; sym_trans_stab_size=1; norm4(L_new)=%d != norm4(L_ref)=%d; max(tau_new)=%d strictly_below min(tau_ref)=%d; bilateral_contact_rank_trans=95/95 (nullity=0); bilateral_contact_rank_full=285/285 (nullity=0).\n",
           r_new.norm4_L, r_ref.norm4_L, r_new.tau_max, r_ref.tau_min);

    /* 5. Built-in Negative Control Corruption Test */
    packing_result_t r_corrupt = verify_one_d19_packing(new_p, new_end, leech_B, "P19_II_vtx_CORRUPTED", 1);
    if (r_corrupt.det_G != -1) { fprintf(stderr, "FAIL: negative control did not fail\n"); return 1; }

    printf("C99_VERIFIER: PASS\n");
    free(json);
    return 0;
}
