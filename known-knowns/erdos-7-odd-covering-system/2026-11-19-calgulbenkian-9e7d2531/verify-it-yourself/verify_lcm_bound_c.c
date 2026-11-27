/*
 * Standalone Exact Integer Verifier 1 (C99, zero floating-point)
 * Certifies that any finite covering system of Z with pairwise distinct odd moduli > 1
 * has least common multiple L >= 168,131,152,814,625.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

__extension__ typedef __int128 i128;

#define BOUND_STRICT ((i128)168131152814625ULL)
#define B0_MAX       ((i128)168131152814624ULL)
#define CAP_DEN      32
#define MAX_PRIMES   20
#define MAX_M_VAL    16384

static __attribute__((noreturn)) void die(const char *msg) {
    fprintf(stderr, "VERIFY_C ERROR: %s\n", msg);
    printf("FAIL\n");
    exit(1);
}

static i128 safe_add(i128 a, i128 b) {
    i128 res;
    if (__builtin_add_overflow(a, b, &res)) die("i128 addition overflow");
    return res;
}

static i128 safe_sub(i128 a, i128 b) {
    i128 res;
    if (__builtin_sub_overflow(a, b, &res)) die("i128 subtraction overflow");
    return res;
}

static i128 safe_mul(i128 a, i128 b) {
    i128 res;
    if (__builtin_mul_overflow(a, b, &res)) die("i128 multiplication overflow");
    return res;
}

static i128 gcd128(i128 a, i128 b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) {
        i128 t = a % b;
        a = b;
        b = t;
    }
    return a;
}

typedef struct {
    i128 num;
    i128 den;
} Rat;

static Rat rat_norm(i128 n, i128 d) {
    if (d <= 0) die("non-positive denominator");
    if (n == 0) return (Rat){0, 1};
    i128 g = gcd128(n, d);
    return (Rat){n / g, d / g};
}

static Rat rat_add(Rat a, Rat b) {
    if (a.num == 0) return b;
    if (b.num == 0) return a;
    i128 g = gcd128(a.den, b.den);
    i128 bd = b.den / g;
    i128 ad = a.den / g;
    i128 den = safe_mul(a.den, bd);
    i128 num = safe_add(safe_mul(a.num, bd), safe_mul(b.num, ad));
    return rat_norm(num, den);
}

static Rat rat_sub(Rat a, Rat b) {
    i128 g = gcd128(a.den, b.den);
    i128 bd = b.den / g;
    i128 ad = a.den / g;
    i128 den = safe_mul(a.den, bd);
    i128 num = safe_sub(safe_mul(a.num, bd), safe_mul(b.num, ad));
    return rat_norm(num, den);
}

static Rat rat_mul(Rat a, Rat b) {
    if (a.num == 0 || b.num == 0) return (Rat){0, 1};
    i128 g1 = gcd128(a.num, b.den);
    i128 g2 = gcd128(b.num, a.den);
    return rat_norm(safe_mul(a.num / g1, b.num / g2), safe_mul(a.den / g2, b.den / g1));
}

static int rat_lt(Rat a, Rat b) {
    /* Compare a.num / a.den < b.num / b.den safely */
    i128 g = gcd128(a.den, b.den);
    i128 lhs = safe_mul(a.num, b.den / g);
    i128 rhs = safe_mul(b.num, a.den / g);
    return lhs < rhs;
}

static i128 ipow128(int base, int exp) {
    i128 r = 1;
    for (int i = 0; i < exp; i++) r = safe_mul(r, base);
    return r;
}

static int parse_i128_dec(const char *s, i128 *out) {
    if (!s || !*s) return 0;
    i128 v = 0;
    for (const char *p = s; *p; p++) {
        if (*p < '0' || *p > '9') return 0;
        v = safe_add(safe_mul(v, 10), (i128)(*p - '0'));
    }
    *out = v;
    return 1;
}

static void format_i128_dec(i128 v, char *buf, size_t cap) {
    char tmp[64];
    int pos = 0;
    if (v == 0) {
        snprintf(buf, cap, "0");
        return;
    }
    int neg = 0;
    if (v < 0) { neg = 1; v = -v; }
    while (v > 0) {
        tmp[pos++] = (char)('0' + (int)(v % 10));
        v /= 10;
    }
    if (neg) tmp[pos++] = '-';
    if ((size_t)(pos + 1) > cap) die("buffer too small");
    for (int i = 0; i < pos; i++) buf[i] = tmp[pos - 1 - i];
    buf[pos] = '\0';
}

/* Generate first MAX_PRIMES odd primes from scratch */
static int ODD_PRIMES[MAX_PRIMES];
static void init_odd_primes(void) {
    int cnt = 0;
    for (int n = 3; cnt < MAX_PRIMES; n += 2) {
        int is_p = 1;
        for (int d = 3; d * d <= n; d += 2) {
            if (n % d == 0) { is_p = 0; break; }
        }
        if (is_p) ODD_PRIMES[cnt++] = n;
    }
}

/* Certificate table loaded from TSV */
typedef struct {
    int r;
    int exps[MAX_PRIMES];
    int k0;
    int ms[MAX_PRIMES];
    Rat expected_bound;
    int matched;
} CertRow;

static CertRow *CERTS = NULL;
static int N_CERTS = 0;

static int cmp_exps(int r1, const int *e1, int r2, const int *e2) {
    int m = (r1 < r2) ? r1 : r2;
    for (int i = 0; i < m; i++) {
        if (e1[i] != e2[i]) return (e1[i] < e2[i]) ? -1 : 1;
    }
    if (r1 != r2) return (r1 < r2) ? -1 : 1;
    return 0;
}

static void load_certificate(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) die("cannot open certificate file");
    int cap = 8192;
    CERTS = (CertRow *)calloc((size_t)cap, sizeof(CertRow));
    if (!CERTS) die("oom");

    char line[1024];
    if (!fgets(line, sizeof(line), fp)) die("empty certificate file");
    if (strcmp(line, "exponents\tk0\tm_over_32\texact_upper_bound\n") != 0) {
        die("unexpected TSV header");
    }

    while (fgets(line, sizeof(line), fp)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';
        if (len == 0) die("blank line in certificate");

        char *c1 = line;
        char *t1 = strchr(c1, '\t'); if (!t1) die("malformed TSV row (missing tab 1)"); *t1 = '\0';
        char *c2 = t1 + 1;
        char *t2 = strchr(c2, '\t'); if (!t2) die("malformed TSV row (missing tab 2)"); *t2 = '\0';
        char *c3 = t2 + 1;
        char *t3 = strchr(c3, '\t'); if (!t3) die("malformed TSV row (missing tab 3)"); *t3 = '\0';
        char *c4 = t3 + 1;
        if (strchr(c4, '\t')) die("extra tab in TSV row");

        if (N_CERTS >= cap) {
            cap *= 2;
            CERTS = (CertRow *)realloc(CERTS, (size_t)cap * sizeof(CertRow));
            if (!CERTS) die("oom realloc");
        }
        CertRow *row = &CERTS[N_CERTS];
        memset(row, 0, sizeof(*row));

        /* Parse exponents */
        char *tok = strtok(c1, ",");
        while (tok) {
            i128 v;
            if (!parse_i128_dec(tok, &v) || v < 1 || v > 60) die("bad exponent");
            if (row->r >= MAX_PRIMES) die("too many primes in row");
            row->exps[row->r++] = (int)v;
            tok = strtok(NULL, ",");
        }
        if (row->r < 2) die("row rank < 2");

        /* Parse k0 */
        i128 k0v;
        if (!parse_i128_dec(c2, &k0v) || k0v < 1 || k0v >= row->r) die("invalid k0");
        row->k0 = (int)k0v;

        /* Parse ms */
        int mc = 0;
        tok = strtok(c3, ",");
        while (tok) {
            i128 mv;
            if (!parse_i128_dec(tok, &mv) || mv <= CAP_DEN || mv > 10000) die("invalid m_i");
            if (mc >= row->r - row->k0) die("too many m_i entries");
            row->ms[mc++] = (int)mv;
            tok = strtok(NULL, ",");
        }
        if (mc != row->r - row->k0) die("m_i count mismatch");

        /* Parse exact_upper_bound = num/den */
        char *slash = strchr(c4, '/');
        if (!slash) die("missing slash in exact_upper_bound");
        *slash = '\0';
        i128 rn = 0, rd = 0;
        if (!parse_i128_dec(c4, &rn) || !parse_i128_dec(slash + 1, &rd) || rn <= 0 || rd <= 0) {
            die("invalid rational in exact_upper_bound");
        }
        if (gcd128(rn, rd) != 1) die("exact_upper_bound not in lowest terms");
        if (rn >= rd) die("recorded bound >= 1");
        row->expected_bound = (Rat){rn, rd};

        /* Enforce strict canonical sort order (no duplicates) */
        if (N_CERTS > 0) {
            if (cmp_exps(CERTS[N_CERTS - 1].r, CERTS[N_CERTS - 1].exps, row->r, row->exps) >= 0) {
                die("certificate rows not strictly sorted");
            }
        }
        N_CERTS++;
    }
    fclose(fp);
}

static CertRow *find_cert_row(int r, const int *exps) {
    int lo = 0, hi = N_CERTS - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int c = cmp_exps(CERTS[mid].r, CERTS[mid].exps, r, exps);
        if (c == 0) return &CERTS[mid];
        if (c < 0) lo = mid + 1;
        else hi = mid - 1;
    }
    return NULL;
}

/* Pure-deletion Berger-Felzenbaum-Fraenkel check (k0 = r) in exact i128 Rat */
static Rat max_bff_seen = {0, 1};
static int check_bff_exact(int r, const int *exps) {
    Rat prod = {1, 1};
    Rat sum = {0, 1};
    for (int m = 0; m < r; m++) {
        int p = ODD_PRIMES[m];
        i128 pe = ipow128(p, exps[m]);
        Rat th = rat_norm(pe - 1, safe_add(safe_mul(p - 2, pe), 1));
        prod = rat_mul(prod, rat_add((Rat){1, 1}, th));
        sum = rat_add(sum, th);
    }
    Rat cov = rat_sub(rat_sub(prod, (Rat){1, 1}), sum);
    if (rat_lt(cov, (Rat){1, 1})) { if (rat_lt(max_bff_seen, cov)) max_bff_seen = cov; return 1; }
    return 0;
}

/* Exact i128 rational evaluation of finite-exponent scalar distortion */
static i128 P_cur[MAX_M_VAL], P_nxt[MAX_M_VAL];
static int V_cur[4096], V_nxt[4096];

static Rat eval_distortion_exact(const CertRow *row) {
    int r = row->r;
    int k0 = row->k0;

    Rat prod_base = {1, 1};
    Rat sum_base = {0, 1};
    i128 D_dist = 1;
    int n_cur = 1;
    V_cur[0] = 1;
    P_cur[1] = 1;

    for (int m = 0; m < k0; m++) {
        int p = ODD_PRIMES[m];
        int e = row->exps[m];
        i128 pe = ipow128(p, e);
        i128 s_m = (safe_mul(p - 2, pe) + 1) / (p - 1);
        Rat th = rat_norm((pe - 1) / (p - 1), s_m);
        prod_base = rat_mul(prod_base, rat_add((Rat){1, 1}, th));
        sum_base = rat_add(sum_base, th);

        i128 tails_num[64];
        tails_num[0] = s_m;
        for (int t = 1; t <= e; t++) {
            tails_num[t] = ipow128(p, e - t);
            if (tails_num[t] > tails_num[t - 1]) die("base tail non-monotone");
        }
        tails_num[e + 1] = 0;

        int n_nxt = 0;
        for (int idx = 0; idx < n_cur; idx++) {
            int mv = V_cur[idx];
            i128 pv = P_cur[mv];
            P_cur[mv] = 0;
            for (int t = 0; t <= e; t++) {
                i128 pr = safe_sub(tails_num[t], tails_num[t + 1]);
                if (pr == 0) continue;
                int nmv = mv * (1 + t);
                if (nmv >= MAX_M_VAL) die("M exceeded MAX_M_VAL");
                if (P_nxt[nmv] == 0) V_nxt[n_nxt++] = nmv;
                P_nxt[nmv] = safe_add(P_nxt[nmv], safe_mul(pv, pr));
            }
        }
        D_dist = safe_mul(D_dist, s_m);
        n_cur = n_nxt;
        i128 chk_sum = 0;
        for (int idx = 0; idx < n_nxt; idx++) {
            int nmv = V_nxt[idx];
            V_cur[idx] = nmv;
            P_cur[nmv] = P_nxt[nmv];
            chk_sum = safe_add(chk_sum, P_nxt[nmv]);
            P_nxt[nmv] = 0;
        }
        if (chk_sum != D_dist) die("base distribution sum mismatch");
    }

    Rat total_loss = rat_sub(rat_sub(prod_base, (Rat){1, 1}), sum_base);

    for (int i = k0; i < r; i++) {
        int p = ODD_PRIMES[i];
        int e = row->exps[i];
        int m_i = row->ms[i - k0];
        i128 pe = ipow128(p, e);

        /* Verify 1 < C_i = m_i / 32 <= p and delta_i = 1 - 32/m_i >= rho_pure = (pe - 1)/((p - 1)*pe) */
        if (m_i <= CAP_DEN || m_i > p * CAP_DEN) die("C_i out of (1, p]");
        /* delta_i >= rho_pure <=> (m_i - 32)*(p - 1)*pe >= m_i*(pe - 1) */
        i128 lhs_adm = safe_mul(safe_mul(m_i - CAP_DEN, p - 1), pe);
        i128 rhs_adm = safe_mul(m_i, pe - 1);
        if (lhs_adm < rhs_adm) die("delta_i < rho_pure");

        /* Stage i loss: sum_{mv} (P_cur[mv] / D_dist) * max(0, m_i*(pe-1)*mv - (m_i-32)*(p-1)*pe) / (32*(p-1)*pe) */
        Rat stage_loss = {0, 1};
        i128 term_den = safe_mul(CAP_DEN * (p - 1), pe);
        for (int idx = 0; idx < n_cur; idx++) {
            int mv = V_cur[idx];
            i128 a_num = safe_mul(safe_mul(m_i, pe - 1), mv);
            if (a_num > lhs_adm) {
                Rat prob = rat_norm(P_cur[mv], D_dist);
                Rat hval = rat_norm(safe_sub(a_num, lhs_adm), term_den);
                stage_loss = rat_add(stage_loss, rat_mul(prob, hval));
            }
        }
        total_loss = rat_add(total_loss, stage_loss);

        if (i < r - 1) {
            i128 full_den_step = safe_mul(CAP_DEN, pe);
            i128 tails_num[64];
            tails_num[0] = full_den_step;
            for (int t = 1; t <= e; t++) {
                i128 raw = safe_mul(m_i, ipow128(p, e - t));
                tails_num[t] = (raw < full_den_step) ? raw : full_den_step;
                if (tails_num[t] > tails_num[t - 1]) die("stage tail non-monotone");
            }
            tails_num[e + 1] = 0;

            int n_nxt = 0;
            for (int idx = 0; idx < n_cur; idx++) {
                int mv = V_cur[idx];
                i128 pv = P_cur[mv];
                P_cur[mv] = 0;
                for (int t = 0; t <= e; t++) {
                    i128 pr = safe_sub(tails_num[t], tails_num[t + 1]);
                    if (pr == 0) continue;
                    int nmv = mv * (1 + t);
                    if (nmv >= MAX_M_VAL) die("M exceeded MAX_M_VAL at stage");
                    if (P_nxt[nmv] == 0) V_nxt[n_nxt++] = nmv;
                    P_nxt[nmv] = safe_add(P_nxt[nmv], safe_mul(pv, pr));
                }
            }
            D_dist = safe_mul(D_dist, full_den_step);
            n_cur = n_nxt;
            i128 chk_sum = 0;
            for (int idx = 0; idx < n_nxt; idx++) {
                int nmv = V_nxt[idx];
                V_cur[idx] = nmv;
                P_cur[nmv] = P_nxt[nmv];
                chk_sum = safe_add(chk_sum, P_nxt[nmv]);
                P_nxt[nmv] = 0;
            }
            if (chk_sum != D_dist) die("stage distribution sum mismatch");
        } else {
            for (int idx = 0; idx < n_cur; idx++) P_cur[V_cur[idx]] = 0;
        }
    }
    return total_loss;
}

/* Exhaustive tree walk of ALL initial-prime abundant profiles <= B0_MAX */
static int walk_exps[MAX_PRIMES];
static uint64_t cnt_all_abundant = 0;
static uint64_t cnt_band = 0;
static uint64_t cnt_bff = 0;
static uint64_t cnt_cert = 0;
static Rat max_loss_seen = {0, 1};

static void walk_profiles(int idx, i128 cur_L, i128 sig_num, i128 sig_den) {
    if (idx > 0 && sig_num >= safe_mul(2, sig_den)) {
        cnt_all_abundant++;
        /* Check 3^k scaling lands in (B0_MAX / 3, B0_MAX] */
        i128 scaled = cur_L;
        while (scaled <= B0_MAX / 3) scaled = safe_mul(scaled, 3);
        if (scaled <= B0_MAX / 3 || scaled > B0_MAX) die("3^k scaling failed");

        if (cur_L > B0_MAX / 3) {
            cnt_band++;
            CertRow *crow = find_cert_row(idx, walk_exps);
            if (check_bff_exact(idx, walk_exps)) {
                if (crow != NULL) die("BFF-killed profile unexpectedly present in certificate");
                cnt_bff++;
            } else {
                if (crow == NULL) die("non-BFF band profile missing from certificate");
                if (crow->matched) die("certificate row matched twice");
                crow->matched = 1;
                Rat actual = eval_distortion_exact(crow);
                if (actual.num != crow->expected_bound.num || actual.den != crow->expected_bound.den) {
                    die("exact_upper_bound mismatch in certificate row");
                }
                if (!rat_lt(actual, (Rat){1, 1})) {
                    die("recomputed upper bound is not strictly < 1");
                }
                if (rat_lt(max_loss_seen, actual)) max_loss_seen = actual;
                cnt_cert++;
            }
        }
    }
    if (idx >= MAX_PRIMES) return;
    int p = ODD_PRIMES[idx];
    if (cur_L > B0_MAX / p) return;
    i128 pe = p;
    i128 psum = 1 + p;
    int e = 1;
    while (cur_L <= B0_MAX / pe) {
        walk_exps[idx] = e;
        walk_profiles(idx + 1, safe_mul(cur_L, pe), safe_mul(sig_num, psum), safe_mul(sig_den, pe));
        if (pe > (B0_MAX / cur_L) / p) break;
        pe = safe_mul(pe, p);
        psum = safe_add(psum, pe);
        e++;
    }
}

/* Positive sanity check: Erdos (1950) distinct covering {0 mod 2, 0 mod 3, 1 mod 4, 5 mod 6, 7 mod 12} */
static void sanity_check_erdos_1950(void) {
    const int a[5] = {0, 0, 1, 5, 7};
    const int n[5] = {2, 3, 4, 6, 12};
    for (int x = 0; x < 12; x++) {
        int cov = 0;
        for (int i = 0; i < 5; i++) if (x % n[i] == a[i]) cov = 1;
        if (!cov) die("Erdos 1950 positive sanity check failed");
    }
    /* Pure-deletion bound at L = 12 = 2^2 * 3^1 must be >= 1 */
    /* p0=2, e0=2: s0 = 1, theta0 = 3; p1=3, e1=1: s1 = 2, theta1 = 1/2 -> (1+3)*(3/2) - 1 - 7/2 = 3/2 >= 1 */
    Rat bff12 = rat_sub(rat_sub(rat_mul((Rat){4, 1}, (Rat){3, 2}), (Rat){1, 1}), (Rat){7, 2});
    if (rat_lt(bff12, (Rat){1, 1})) die("soundness bug: L=12 falsely excluded");
}

int main(int argc, char **argv) {
    if (argc != 2) die("usage: verify_lcm_bound_c <certificate.tsv>");
    init_odd_primes();
    sanity_check_erdos_1950();

    /* Verify BOUND_STRICT = 3^4 * 5^3 * 7^2 * 11^2 * 13 * 17 * 19 * 23 * 29 = 168131152814625 */
    i128 fchk = safe_mul(ipow128(3, 4), safe_mul(ipow128(5, 3), safe_mul(ipow128(7, 2), ipow128(11, 2))));
    const int tail_p[5] = {13, 17, 19, 23, 29};
    for (int i = 0; i < 5; i++) fchk = safe_mul(fchk, tail_p[i]);
    if (fchk != BOUND_STRICT) die("BOUND_STRICT factorization mismatch");
    if (BOUND_STRICT <= (i128)11486475ULL || BOUND_STRICT <= (i128)9704539845ULL) {
        die("BOUND_STRICT does not exceed prior bounds");
    }

    load_certificate(argv[1]);
    walk_profiles(0, 1, 1, 1);

    for (int i = 0; i < N_CERTS; i++) {
        if (!CERTS[i].matched) die("unused extra row in certificate");
    }
    if ((int)cnt_cert != N_CERTS) die("certificate count mismatch");

    char b_str[64], b0_str[64], band_lo_str[64], n_str[64], d_str[64], sur_str[64], bn_str[64], bd_str[64];
    format_i128_dec(BOUND_STRICT, b_str, sizeof(b_str));
    format_i128_dec(B0_MAX, b0_str, sizeof(b0_str));
    format_i128_dec(B0_MAX / 3, band_lo_str, sizeof(band_lo_str));
    format_i128_dec(max_loss_seen.num, n_str, sizeof(n_str));
    format_i128_dec(max_loss_seen.den, d_str, sizeof(d_str));
    format_i128_dec(safe_sub(max_loss_seen.den, max_loss_seen.num), sur_str, sizeof(sur_str));
    format_i128_dec(max_bff_seen.num, bn_str, sizeof(bn_str));
    format_i128_dec(max_bff_seen.den, bd_str, sizeof(bd_str));

    printf("[Verifier 1 - C99 Exact i128] Certified lower bound L at least %s (168,131,152,814,625)\n", b_str);
    printf("  max_excluded_lcm                                  = %s (168,131,152,814,624)\n", b0_str);
    printf("  band_lower_threshold_floor_B0_div_3               = %s\n", band_lo_str);
    printf("  total_initial_prime_abundant_profiles_below_bound = %llu\n", (unsigned long long)cnt_all_abundant);
    printf("  band_profiles_checked                             = %llu\n", (unsigned long long)cnt_band);
    printf("  refuted_by_pure_deletion_bff                      = %llu\n", (unsigned long long)cnt_bff);
    printf("  max_pure_deletion_bff_measure                     = %s/%s\n", bn_str, bd_str);
    printf("  refuted_by_distortion_certificate                 = %llu\n", (unsigned long long)cnt_cert);
    printf("  max_certified_covered_measure                     = %s/%s\n", n_str, d_str);
    printf("  min_certified_uncovered_numerator_surplus         = %s\n", sur_str);
    printf("VERIFY_C: PASS\n");
    free(CERTS);
    return 0;
}
