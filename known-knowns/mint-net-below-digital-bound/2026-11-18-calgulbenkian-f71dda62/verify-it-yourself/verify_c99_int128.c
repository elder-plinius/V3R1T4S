/*
 * Independent C99 exact 128-bit integer verifier for the closed MinT cell
 * (t=3, m=11, s=19) in base 3 via the OOA(3^11, 19, S_3, T=4, k=8) LP dual bound.
 *
 * Zero external dependencies; shares zero code with verify_python_exact.py.
 */
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef __int128 i128;

#define BASE 3
#define DEPTH 4
#define DIM_S 19
#define STRENGTH_K 8
#define TARGET_M 177147LL
#define MAX_TERMS 256

typedef struct {
    int f[5];
    int size;
    i128 u_num;
    i128 u_den;
    i128 u_scaled;
} DualTerm;

static int64_t pasc[32][32];

static void init_pascal(void) {
    memset(pasc, 0, sizeof(pasc));
    for (int n = 0; n < 32; n++) {
        pasc[n][0] = 1;
        for (int r = 1; r <= n; r++) {
            pasc[n][r] = pasc[n - 1][r - 1] + pasc[n - 1][r];
        }
    }
}

static i128 parse_i128_str(const char *s) {
    while (*s && (isspace((unsigned char)*s) || *s == '"')) s++;
    int neg = 0;
    if (*s == '-') { neg = 1; s++; }
    else if (*s == '+') { s++; }
    if (!isdigit((unsigned char)*s)) {
        fprintf(stderr, "Invalid integer token near: %.20s\n", s);
        exit(2);
    }
    i128 val = 0;
    while (isdigit((unsigned char)*s)) {
        val = val * 10 + (*s - '0');
        s++;
    }
    return neg ? -val : val;
}

static const char *find_key_after(const char *p, const char *key) {
    const char *hit = strstr(p, key);
    if (!hit) return NULL;
    hit += strlen(key);
    while (*hit && (*hit == ' ' || *hit == '\t' || *hit == '\n' || *hit == '\r' || *hit == ':')) hit++;
    return hit;
}

static int64_t kraw_1d(int deg, int a, int b) {
    if (b < 0 || a + b < deg) return 0;
    int64_t total = 0;
    for (int j = 0; j <= deg; j++) {
        int rem = deg - j;
        if (j > a || rem > b) continue;
        int64_t pow2 = 1LL << rem; /* (BASE - 1)^(deg - j) = 2^(deg - j) since BASE = 3 */
        int64_t term = pasc[a][j] * pasc[b][rem] * pow2;
        if (j & 1) total -= term;
        else total += term;
    }
    return total;
}

static int64_t kraw_5d(const int f[5], const int x[5]) {
    int sz = f[1] + 2 * f[2] + 3 * f[3] + 4 * f[4];
    int br = f[1] + f[2] + f[3] + f[4];
    if (br == 0) return 1;
    int64_t prod = 1;
    int suf = 0;
    for (int i = 4; i >= 1; i--) {
        int fi = f[i];
        int a = x[i - 1];
        int b = x[i] + suf;
        if (b < 0 || a + b < fi) return 0;
        if (fi > 0) {
            int64_t kv = kraw_1d(fi, a, b);
            if (kv == 0) return 0;
            prod *= kv;
        }
        suf += x[i] - fi;
    }
    int64_t p3 = 1;
    for (int e = 0; e < sz - br; e++) p3 *= 3LL;
    return p3 * prod;
}

static int verify_model(const DualTerm *terms, int n_terms, i128 L, i128 claimed_num, i128 claimed_den, int verbose) {
    if (L <= 0 || n_terms <= 0 || claimed_den <= 0) return 0;

    for (int i = 0; i < n_terms; i++) {
        int sum_f = 0, sz = 0;
        for (int r = 0; r <= 4; r++) {
            if (terms[i].f[r] < 0) return 0;
            sum_f += terms[i].f[r];
            sz += r * terms[i].f[r];
        }
        if (sum_f != DIM_S || terms[i].f[0] == DIM_S) return 0;
        if (sz != terms[i].size) return 0;
        if (terms[i].u_den <= 0 || (L % terms[i].u_den) != 0) return 0;
        if (terms[i].u_num * (L / terms[i].u_den) != terms[i].u_scaled) return 0;
        if (sz > STRENGTH_K && terms[i].u_scaled > 0) return 0;
        for (int j = 0; j < i; j++) {
            if (memcmp(terms[i].f, terms[j].f, sizeof(terms[i].f)) == 0) return 0;
        }
    }

    int count_non_diag = 0;
    i128 min_lhs = -1;
    int first_min = 1;

    for (int x0 = 0; x0 <= DIM_S; x0++) {
        for (int x1 = 0; x0 + x1 <= DIM_S; x1++) {
            for (int x2 = 0; x0 + x1 + x2 <= DIM_S; x2++) {
                for (int x3 = 0; x0 + x1 + x2 + x3 <= DIM_S; x3++) {
                    int x4 = DIM_S - (x0 + x1 + x2 + x3);
                    if (x4 == DIM_S) continue; /* skip diagonal (0,0,0,0,19) */
                    int x[5] = {x0, x1, x2, x3, x4};
                    i128 acc = L;
                    for (int t = 0; t < n_terms; t++) {
                        int64_t kv = kraw_5d(terms[t].f, x);
                        if (kv != 0) acc += terms[t].u_scaled * (i128)kv;
                    }
                    if (acc < 0) return 0;
                    if (first_min || acc < min_lhs) {
                        min_lhs = acc;
                        first_min = 0;
                    }
                    count_non_diag++;
                }
            }
        }
    }

    if (count_non_diag != 8854) return 0;

    int x_diag[5] = {0, 0, 0, 0, DIM_S};
    i128 diag_acc = L;
    for (int t = 0; t < n_terms; t++) {
        int64_t kv = kraw_5d(terms[t].f, x_diag);
        diag_acc += terms[t].u_scaled * (i128)kv;
    }

    if (diag_acc <= (i128)TARGET_M * L) return 0;
    if (diag_acc * claimed_den != L * claimed_num) return 0;

    if (verbose) {
        long double approx = (long double)diag_acc / (long double)L;
        printf("[C99 __int128] VERIFIED: M >= %.6Lf > 3^11 = %lld across all %d non-diagonal shapes (min_scaled_LHS = %lld)\n",
               approx, (long long)TARGET_M, count_non_diag, (long long)min_lhs);
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <certificate.json> [--corrupt-test]\n", argv[0]);
        return 2;
    }
    init_pascal();

    FILE *fp = fopen(argv[1], "rb");
    if (!fp) { perror("fopen"); return 2; }
    fseek(fp, 0, SEEK_END);
    long sz = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *buf = (char *)malloc((size_t)sz + 1);
    if (!buf || fread(buf, 1, (size_t)sz, fp) != (size_t)sz) {
        fprintf(stderr, "Read failed\n");
        return 2;
    }
    buf[sz] = '\0';
    fclose(fp);

    const char *pL = find_key_after(buf, "\"common_denominator_L\"");
    const char *pelb = find_key_after(buf, "\"exact_lower_bound\"");
    const char *pnum = pelb ? find_key_after(pelb, "\"numerator\"") : NULL;
    const char *pden = pelb ? find_key_after(pelb, "\"denominator\"") : NULL;
    const char *parr = find_key_after(buf, "\"dual_weights_u\"");
    if (!pL || !pnum || !pden || !parr) {
        fprintf(stderr, "Missing required JSON fields\n");
        return 2;
    }
    i128 L = parse_i128_str(pL);
    i128 claimed_num = parse_i128_str(pnum);
    i128 claimed_den = parse_i128_str(pden);

    DualTerm terms[MAX_TERMS];
    int n_terms = 0;
    const char *cur = parr;
    while ((cur = find_key_after(cur, "\"f\"")) != NULL) {
        if (n_terms >= MAX_TERMS) { fprintf(stderr, "Too many terms\n"); return 2; }
        cur = strchr(cur, '[');
        if (!cur) break;
        cur++;
        for (int r = 0; r < 5; r++) {
            terms[n_terms].f[r] = (int)strtol(cur, (char **)&cur, 10);
            while (*cur && (*cur == ',' || isspace((unsigned char)*cur))) cur++;
        }
        const char *psz = find_key_after(cur, "\"size\"");
        const char *pun = find_key_after(cur, "\"u_num\"");
        const char *pud = find_key_after(cur, "\"u_den\"");
        const char *pus = find_key_after(cur, "\"u_scaled_by_L\"");
        if (!psz || !pun || !pud || !pus) { fprintf(stderr, "Malformed entry\n"); return 2; }
        terms[n_terms].size = (int)strtol(psz, NULL, 10);
        terms[n_terms].u_num = parse_i128_str(pun);
        terms[n_terms].u_den = parse_i128_str(pud);
        terms[n_terms].u_scaled = parse_i128_str(pus);
        cur = pus;
        n_terms++;
    }

    if (!verify_model(terms, n_terms, L, claimed_num, claimed_den, 1)) {
        printf("FAIL\n");
        free(buf);
        return 1;
    }

    if (argc >= 3 && strcmp(argv[2], "--corrupt-test") == 0) {
        /* Corrupt 1: flip sign of a |f| > 8 term */
        DualTerm bad1[MAX_TERMS];
        memcpy(bad1, terms, sizeof(terms));
        for (int i = 0; i < n_terms; i++) {
            if (bad1[i].size > STRENGTH_K && bad1[i].u_scaled < 0) {
                bad1[i].u_num = -bad1[i].u_num;
                bad1[i].u_scaled = -bad1[i].u_scaled;
                break;
            }
        }
        if (verify_model(bad1, n_terms, L, claimed_num, claimed_den, 0)) {
            fprintf(stderr, "FAIL: C99 verifier accepted corrupted sign!\n");
            free(buf);
            return 1;
        }

        /* Corrupt 2: perturb scaled weights by 101/100 so tight non-diagonal inequality fails */
        DualTerm bad2[MAX_TERMS];
        memcpy(bad2, terms, sizeof(terms));
        i128 L100 = L * 100;
        for (int i = 0; i < n_terms; i++) {
            bad2[i].u_num *= 101;
            bad2[i].u_den *= 100;
            bad2[i].u_scaled *= 101;
        }
        if (verify_model(bad2, n_terms, L100, claimed_num, claimed_den, 0)) {
            fprintf(stderr, "FAIL: C99 verifier accepted infeasible scaled weights!\n");
            free(buf);
            return 1;
        }
        printf("[C99 __int128] Negative corruption checks (sign & slack violations rejected): OK\n");
    }

    free(buf);
    return 0;
}
