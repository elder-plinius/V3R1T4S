/* Bespoke ISO C99 first-principles verifier for perfect-cuboid p1 (v2).
 * Clean under: -std=c99 -O2 -g -Wall -Wextra -Werror -Wpedantic -fsanitize=address,undefined
 */
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEG 26
#define MAX_UNI_DEG 26

typedef struct {
    int64_t c[MAX_DEG + 1][MAX_DEG + 1];
} PolyBiv;

typedef struct {
    int64_t c[MAX_UNI_DEG + 1];
} PolyUni;

typedef struct {
    const char *src;
    size_t pos;
    size_t len;
} Cursor;

static void die(const char *reason) {
    fprintf(stderr, "C99_REJECT: %s\n", reason);
    exit(1);
}

static void skip_ws(Cursor *cur) {
    while (cur->pos < cur->len) {
        unsigned char ch = (unsigned char)cur->src[cur->pos];
        if (ch == ' ' || ch == '\t' || ch == '\n' || ch == '\r') {
            cur->pos++;
        } else {
            break;
        }
    }
}

static void expect_ch(Cursor *cur, char expected) {
    skip_ws(cur);
    if (cur->pos >= cur->len || cur->src[cur->pos] != expected) {
        die("unexpected character in JSON stream");
    }
    cur->pos++;
}

static void parse_str(Cursor *cur, char *buf, size_t cap) {
    size_t out = 0;
    expect_ch(cur, '"');
    while (cur->pos < cur->len && cur->src[cur->pos] != '"') {
        char ch = cur->src[cur->pos++];
        if (ch == '\\' || (unsigned char)ch < 32) {
            die("escape or control char in JSON string");
        }
        if (out + 1 >= cap) {
            die("JSON string exceeds buffer");
        }
        buf[out++] = ch;
    }
    expect_ch(cur, '"');
    buf[out] = '\0';
}

static void expect_key(Cursor *cur, const char *key) {
    char tmp[128];
    parse_str(cur, tmp, sizeof(tmp));
    if (strcmp(tmp, key) != 0) {
        die("JSON key mismatch");
    }
    expect_ch(cur, ':');
}

static int64_t parse_i64(Cursor *cur) {
    int neg = 0;
    uint64_t acc = 0;
    size_t digits = 0;
    skip_ws(cur);
    if (cur->pos < cur->len && cur->src[cur->pos] == '-') {
        neg = 1;
        cur->pos++;
    }
    if (cur->pos < cur->len && cur->src[cur->pos] == '0') {
        cur->pos++;
        if (cur->pos < cur->len && isdigit((unsigned char)cur->src[cur->pos])) {
            die("leading zero in JSON integer");
        }
        if (neg) {
            die("negative zero in JSON integer");
        }
        return 0;
    }
    while (cur->pos < cur->len && isdigit((unsigned char)cur->src[cur->pos])) {
        uint64_t d = (uint64_t)(cur->src[cur->pos] - '0');
        if (acc > 900000000000000000ULL) {
            die("integer literal overflow");
        }
        acc = acc * 10ULL + d;
        cur->pos++;
        digits++;
    }
    if (digits == 0) {
        die("missing integer digits");
    }
    return neg ? -(int64_t)acc : (int64_t)acc;
}

static void poly_biv_zero(PolyBiv *p) { memset(p, 0, sizeof(*p)); }
static void poly_uni_zero(PolyUni *p) { memset(p, 0, sizeof(*p)); }

static int poly_biv_eq(const PolyBiv *a, const PolyBiv *b) {
    for (int i = 0; i <= MAX_DEG; i++) {
        for (int j = 0; j <= MAX_DEG; j++) {
            if (a->c[i][j] != b->c[i][j]) return 0;
        }
    }
    return 1;
}

static int poly_uni_eq(const PolyUni *a, const PolyUni *b) {
    for (int i = 0; i <= MAX_UNI_DEG; i++) {
        if (a->c[i] != b->c[i]) return 0;
    }
    return 1;
}

static void poly_biv_add(PolyBiv *out, const PolyBiv *a, const PolyBiv *b, int64_t sign_b) {
    for (int i = 0; i <= MAX_DEG; i++) {
        for (int j = 0; j <= MAX_DEG; j++) {
            out->c[i][j] = a->c[i][j] + sign_b * b->c[i][j];
        }
    }
}

static void poly_biv_mul(PolyBiv *out, const PolyBiv *a, const PolyBiv *b) {
    PolyBiv res;
    poly_biv_zero(&res);
    for (int i1 = 0; i1 <= MAX_DEG; i1++) {
        for (int j1 = 0; j1 <= MAX_DEG; j1++) {
            int64_t v1 = a->c[i1][j1];
            if (v1 == 0) continue;
            for (int i2 = 0; i2 <= MAX_DEG; i2++) {
                for (int j2 = 0; j2 <= MAX_DEG; j2++) {
                    int64_t v2 = b->c[i2][j2];
                    if (v2 == 0) continue;
                    if (i1 + i2 > MAX_DEG || j1 + j2 > MAX_DEG) die("bivariate degree exceeded");
                    res.c[i1 + i2][j1 + j2] += v1 * v2;
                }
            }
        }
    }
    *out = res;
}

static void poly_biv_pow(PolyBiv *out, const PolyBiv *base, int exp) {
    PolyBiv acc;
    poly_biv_zero(&acc);
    acc.c[0][0] = 1;
    for (int k = 0; k < exp; k++) poly_biv_mul(&acc, &acc, base);
    *out = acc;
}

static void poly_biv_compose(PolyBiv *out, const PolyBiv *u, const PolyBiv *sub_x, const PolyBiv *sub_y) {
    PolyBiv total;
    poly_biv_zero(&total);
    for (int ix = 0; ix <= MAX_DEG; ix++) {
        for (int iy = 0; iy <= MAX_DEG; iy++) {
            int64_t cf = u->c[ix][iy];
            if (cf == 0) continue;
            PolyBiv px, py, prod;
            poly_biv_pow(&px, sub_x, ix);
            poly_biv_pow(&py, sub_y, iy);
            poly_biv_mul(&prod, &px, &py);
            for (int a = 0; a <= MAX_DEG; a++) {
                for (int b = 0; b <= MAX_DEG; b++) {
                    total.c[a][b] += cf * prod.c[a][b];
                }
            }
        }
    }
    *out = total;
}

static void poly_uni_mul(PolyUni *out, const PolyUni *a, const PolyUni *b) {
    PolyUni res;
    poly_uni_zero(&res);
    for (int i = 0; i <= MAX_UNI_DEG; i++) {
        if (a->c[i] == 0) continue;
        for (int j = 0; j <= MAX_UNI_DEG; j++) {
            if (b->c[j] == 0) continue;
            if (i + j > MAX_UNI_DEG) die("univariate degree exceeded");
            res.c[i + j] += a->c[i] * b->c[j];
        }
    }
    *out = res;
}

static void poly_uni_pow(PolyUni *out, const PolyUni *base, int exp) {
    PolyUni acc;
    poly_uni_zero(&acc);
    acc.c[0] = 1;
    for (int k = 0; k < exp; k++) poly_uni_mul(&acc, &acc, base);
    *out = acc;
}

static void poly_biv_eval_uni(PolyUni *out, const PolyBiv *f, const PolyUni *px, const PolyUni *py) {
    PolyUni total;
    poly_uni_zero(&total);
    for (int ix = 0; ix <= MAX_DEG; ix++) {
        for (int iy = 0; iy <= MAX_DEG; iy++) {
            int64_t cf = f->c[ix][iy];
            if (cf == 0) continue;
            PolyUni ux, uy, prod;
            poly_uni_pow(&ux, px, ix);
            poly_uni_pow(&uy, py, iy);
            poly_uni_mul(&prod, &ux, &uy);
            for (int d = 0; d <= MAX_UNI_DEG; d++) total.c[d] += cf * prod.c[d];
        }
    }
    *out = total;
}

static void parse_poly_biv(Cursor *cur, PolyBiv *out) {
    int prev_x = 9999, prev_y = 9999, count = 0;
    poly_biv_zero(out);
    expect_ch(cur, '[');
    for (;;) {
        int64_t ex, ey, cf;
        expect_ch(cur, '[');
        ex = parse_i64(cur); expect_ch(cur, ',');
        ey = parse_i64(cur); expect_ch(cur, ',');
        cf = parse_i64(cur); expect_ch(cur, ']');
        if (ex < 0 || ex > MAX_DEG || ey < 0 || ey > MAX_DEG || cf == 0) die("invalid bivariate monomial");
        if (ex > prev_x || (ex == prev_x && ey >= prev_y)) die("bivariate monomials not descending");
        prev_x = (int)ex; prev_y = (int)ey;
        out->c[ex][ey] = cf;
        count++;
        skip_ws(cur);
        if (cur->pos < cur->len && cur->src[cur->pos] == ',') cur->pos++;
        else break;
    }
    expect_ch(cur, ']');
    if (count == 0) die("empty bivariate polynomial");
}

static void parse_poly_uni(Cursor *cur, PolyUni *out) {
    int prev_m = 9999, count = 0;
    poly_uni_zero(out);
    expect_ch(cur, '[');
    for (;;) {
        int64_t em, cf;
        expect_ch(cur, '[');
        em = parse_i64(cur); expect_ch(cur, ',');
        cf = parse_i64(cur); expect_ch(cur, ']');
        if (em < 0 || em > MAX_UNI_DEG || cf == 0 || em >= prev_m) die("invalid univariate monomial");
        prev_m = (int)em;
        out->c[em] = cf;
        count++;
        skip_ws(cur);
        if (cur->pos < cur->len && cur->src[cur->pos] == ',') cur->pos++;
        else break;
    }
    expect_ch(cur, ']');
    if (count == 0) die("empty univariate polynomial");
}

static int64_t mod_pos(int64_t x, int64_t m) {
    int64_t r = x % m;
    return r < 0 ? r + m : r;
}

static int64_t pow_mod(int64_t base, int exp, int64_t m) {
    int64_t acc = 1 % m;
    int64_t b = mod_pos(base, m);
    for (int i = 0; i < exp; i++) acc = (acc * b) % m;
    return acc;
}

static int64_t poly_biv_eval_mod(const PolyBiv *p, int64_t x, int64_t y, int64_t m) {
    int64_t total = 0;
    for (int i = 0; i <= MAX_DEG; i++) {
        for (int j = 0; j <= MAX_DEG; j++) {
            int64_t cf = p->c[i][j];
            if (cf == 0) continue;
            int64_t term = (mod_pos(cf, m) * pow_mod(x, i, m)) % m;
            term = (term * pow_mod(y, j, m)) % m;
            total = (total + term) % m;
        }
    }
    return total;
}

static int64_t dec_str_mod(const char *s, int64_t m) {
    size_t n = strlen(s);
    int64_t acc = 0;
    if (n == 0 || s[0] == '0') die("invalid positive decimal witness string");
    for (size_t i = 0; i < n; i++) {
        if (!isdigit((unsigned char)s[i])) die("non-digit in decimal witness string");
        acc = (acc * 10 + (s[i] - '0')) % m;
    }
    return acc;
}

static void check_diagonal_identities(
    const PolyBiv *e1, const PolyBiv *e2, const PolyBiv *csq,
    const PolyBiv *dab, const PolyBiv *dac, const PolyBiv *dbc, const PolyBiv *sp)
{
    PolyBiv e1_sq, e2_sq, lhs, rhs;
    poly_biv_mul(&e1_sq, e1, e1);
    poly_biv_mul(&e2_sq, e2, e2);

    poly_biv_add(&lhs, &e1_sq, &e2_sq, 1);
    poly_biv_mul(&rhs, dab, dab);
    if (!poly_biv_eq(&lhs, &rhs)) die("face diagonal ab^2 mismatch");

    poly_biv_add(&lhs, &e1_sq, csq, 1);
    poly_biv_mul(&rhs, dac, dac);
    if (!poly_biv_eq(&lhs, &rhs)) die("face diagonal ac^2 mismatch");

    poly_biv_add(&lhs, &e2_sq, csq, 1);
    poly_biv_mul(&rhs, dbc, dbc);
    if (!poly_biv_eq(&lhs, &rhs)) die("face diagonal bc^2 mismatch");

    poly_biv_add(&lhs, &e1_sq, &e2_sq, 1);
    poly_biv_add(&lhs, &lhs, csq, 1);
    poly_biv_mul(&rhs, sp, sp);
    if (!poly_biv_eq(&lhs, &rhs)) die("space diagonal^2 mismatch");

    if (poly_biv_eval_mod(dab, 4, 1, 1000000007LL) > 500000000LL) die("dab sign flipped");
    if (poly_biv_eval_mod(dac, 4, 1, 1000000007LL) > 500000000LL) die("dac sign flipped");
    if (poly_biv_eval_mod(dbc, 4, 1, 1000000007LL) > 500000000LL) die("dbc sign flipped");
    if (poly_biv_eval_mod(sp,  4, 1, 1000000007LL) > 500000000LL) die("sp sign flipped");
}

static size_t file_size_exact(const char *path) {
    FILE *fp = fopen(path, "rb");
    long sz;
    if (!fp) die("cannot open referenced object file");
    if (fseek(fp, 0, SEEK_END) != 0) { fclose(fp); die("fseek failed"); }
    sz = ftell(fp);
    fclose(fp);
    if (sz <= 0) die("empty object file");
    return (size_t)sz;
}

int main(int argc, char **argv) {
    if (argc != 4) die("usage: verify_c99 cert.json lean_file lean_sha");
    const char *cert_path = argv[1];
    const char *lean_path = argv[2];
    const char *lean_sha_arg = argv[3];

    FILE *fp = fopen(cert_path, "rb");
    if (!fp) die("cannot open certificate.json");
    if (fseek(fp, 0, SEEK_END) != 0) { fclose(fp); die("fseek cert failed"); }
    long fsz = ftell(fp);
    if (fsz <= 0 || fsz > 1000000L) { fclose(fp); die("invalid certificate size"); }
    rewind(fp);
    char *buf = (char *)malloc((size_t)fsz + 1);
    if (!buf) { fclose(fp); die("malloc failed"); }
    if (fread(buf, 1, (size_t)fsz, fp) != (size_t)fsz) { free(buf); fclose(fp); die("fread failed"); }
    buf[fsz] = '\0';
    fclose(fp);

    Cursor cur = { buf, 0, (size_t)fsz };
    expect_ch(&cur, '{');

    expect_key(&cur, "schema_version");
    if (parse_i64(&cur) != 2) die("schema_version != 2");
    expect_ch(&cur, ',');

    expect_key(&cur, "unified_parametrization_count");
    int64_t unif_cnt = parse_i64(&cur);
    if (unif_cnt != 1) die("unified_parametrization_count != 1");
    expect_ch(&cur, ',');

    expect_key(&cur, "excluded_fibration_count");
    int64_t excl_fibs = parse_i64(&cur);
    if (excl_fibs != 2) die("excluded_fibration_count != 2");
    expect_ch(&cur, ',');

    expect_key(&cur, "lean_verified_theorem_count");
    int64_t thm_cnt = parse_i64(&cur);
    if (thm_cnt != 12) die("lean_verified_theorem_count != 12");
    expect_ch(&cur, ',');

    expect_key(&cur, "lean_placeholder_count");
    if (parse_i64(&cur) != 0) die("lean_placeholder_count != 0");
    expect_ch(&cur, ',');

    expect_key(&cur, "lean_reflection_count");
    if (parse_i64(&cur) != 0) die("lean_reflection_count != 0");
    expect_ch(&cur, ',');

    expect_key(&cur, "lean_proof_bytes");
    if ((size_t)parse_i64(&cur) != file_size_exact(lean_path)) die("lean_proof_bytes mismatch");
    expect_ch(&cur, ',');

    char lean_sha_json[128];
    expect_key(&cur, "lean_proof_sha");
    parse_str(&cur, lean_sha_json, sizeof(lean_sha_json));
    if (strlen(lean_sha_json) != 64 || strcmp(lean_sha_json, lean_sha_arg) != 0) die("lean_proof_sha mismatch");
    expect_ch(&cur, ',');

    /* Bivariate polynomials */
    PolyBiv u_e1, u_e2, u_csq;
    PolyBiv fa_e1, fa_e2, fa_csq, fa_dab, fa_dac, fa_dbc, fa_sp;
    PolyBiv fb_e1, fb_e2, fb_csq, fb_dab, fb_dac, fb_dbc, fb_sp;

    expect_key(&cur, "bivariate_polynomials");
    expect_ch(&cur, '{');
    expect_key(&cur, "unified_edge_first");   parse_poly_biv(&cur, &u_e1);   expect_ch(&cur, ',');
    expect_key(&cur, "unified_edge_second");  parse_poly_biv(&cur, &u_e2);   expect_ch(&cur, ',');
    expect_key(&cur, "unified_third_sq");     parse_poly_biv(&cur, &u_csq);  expect_ch(&cur, ',');
    expect_key(&cur, "family_a_edge_first");  parse_poly_biv(&cur, &fa_e1);  expect_ch(&cur, ',');
    expect_key(&cur, "family_a_edge_second"); parse_poly_biv(&cur, &fa_e2);  expect_ch(&cur, ',');
    expect_key(&cur, "family_a_third_sq");    parse_poly_biv(&cur, &fa_csq); expect_ch(&cur, ',');
    expect_key(&cur, "family_a_diag_ab");     parse_poly_biv(&cur, &fa_dab); expect_ch(&cur, ',');
    expect_key(&cur, "family_a_diag_ac");     parse_poly_biv(&cur, &fa_dac); expect_ch(&cur, ',');
    expect_key(&cur, "family_a_diag_bc");     parse_poly_biv(&cur, &fa_dbc); expect_ch(&cur, ',');
    expect_key(&cur, "family_a_space_diag");  parse_poly_biv(&cur, &fa_sp);  expect_ch(&cur, ',');
    expect_key(&cur, "family_b_edge_first");  parse_poly_biv(&cur, &fb_e1);  expect_ch(&cur, ',');
    expect_key(&cur, "family_b_edge_second"); parse_poly_biv(&cur, &fb_e2);  expect_ch(&cur, ',');
    expect_key(&cur, "family_b_third_sq");    parse_poly_biv(&cur, &fb_csq); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_diag_ab");     parse_poly_biv(&cur, &fb_dab); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_diag_ac");     parse_poly_biv(&cur, &fb_dac); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_diag_bc");     parse_poly_biv(&cur, &fb_dbc); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_space_diag");  parse_poly_biv(&cur, &fb_sp);
    expect_ch(&cur, '}');
    expect_ch(&cur, ',');

    PolyBiv def_e1, def_e2, def_csq;
    poly_biv_zero(&def_e1); def_e1.c[5][0] = 1; def_e1.c[3][2] = 1; def_e1.c[1][4] = 1;
    poly_biv_zero(&def_e2); def_e2.c[4][1] = 2; def_e2.c[2][3] = 2;
    poly_biv_zero(&def_csq); def_csq.c[0][10] = 1; def_csq.c[2][8] = 2; def_csq.c[4][6] = -1; def_csq.c[6][4] = -6; def_csq.c[8][2] = -3;

    if (!poly_biv_eq(&u_e1, &def_e1) || !poly_biv_eq(&u_e2, &def_e2) || !poly_biv_eq(&u_csq, &def_csq)) {
        die("unified defining polynomial mismatch");
    }

    PolyBiv p2_minus_q2, two_pq, tmp;
    poly_biv_zero(&p2_minus_q2); p2_minus_q2.c[2][0] = 1; p2_minus_q2.c[0][2] = -1;
    poly_biv_zero(&two_pq);      two_pq.c[1][1] = 2;

    poly_biv_compose(&tmp, &u_e1, &p2_minus_q2, &two_pq); if (!poly_biv_eq(&tmp, &fa_e1)) die("FamA e1 != Unified");
    poly_biv_compose(&tmp, &u_e2, &p2_minus_q2, &two_pq); if (!poly_biv_eq(&tmp, &fa_e2)) die("FamA e2 != Unified");
    poly_biv_compose(&tmp, &u_csq, &p2_minus_q2, &two_pq); if (!poly_biv_eq(&tmp, &fa_csq)) die("FamA csq != Unified");

    poly_biv_compose(&tmp, &u_e1, &two_pq, &p2_minus_q2); if (!poly_biv_eq(&tmp, &fb_e1)) die("FamB e1 != Unified");
    poly_biv_compose(&tmp, &u_e2, &two_pq, &p2_minus_q2); if (!poly_biv_eq(&tmp, &fb_e2)) die("FamB e2 != Unified");
    poly_biv_compose(&tmp, &u_csq, &two_pq, &p2_minus_q2); if (!poly_biv_eq(&tmp, &fb_csq)) die("FamB csq != Unified");

    check_diagonal_identities(&fa_e1, &fa_e2, &fa_csq, &fa_dab, &fa_dac, &fa_dbc, &fa_sp);
    check_diagonal_identities(&fb_e1, &fb_e2, &fb_csq, &fb_dab, &fb_dac, &fb_dbc, &fb_sp);

    /* Univariate positive subfamilies */
    PolyUni sa_e1, sa_e2, sa_csq, sb_e1, sb_e2, sb_csq;
    expect_key(&cur, "univariate_positive_subfamilies");
    expect_ch(&cur, '{');
    expect_key(&cur, "subfamily_a_min_k"); if (parse_i64(&cur) != 1) die("subfamily_a_min_k != 1"); expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_a_edge_first");  parse_poly_uni(&cur, &sa_e1);  expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_a_edge_second"); parse_poly_uni(&cur, &sa_e2);  expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_a_third_sq");    parse_poly_uni(&cur, &sa_csq); expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_b_min_k"); if (parse_i64(&cur) != 2) die("subfamily_b_min_k != 2"); expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_b_edge_first");  parse_poly_uni(&cur, &sb_e1);  expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_b_edge_second"); parse_poly_uni(&cur, &sb_e2);  expect_ch(&cur, ',');
    expect_key(&cur, "subfamily_b_third_sq");    parse_poly_uni(&cur, &sb_csq);
    expect_ch(&cur, '}');
    expect_ch(&cur, ',');

    PolyUni m_plus_2, m_plus_1, two_m_plus_4, const_1, ucheck;
    poly_uni_zero(&m_plus_2);     m_plus_2.c[1] = 1; m_plus_2.c[0] = 2;
    poly_uni_zero(&m_plus_1);     m_plus_1.c[1] = 1; m_plus_1.c[0] = 1;
    poly_uni_zero(&two_m_plus_4); two_m_plus_4.c[1] = 2; two_m_plus_4.c[0] = 4;
    poly_uni_zero(&const_1);      const_1.c[0] = 1;

    poly_biv_eval_uni(&ucheck, &fa_e1, &m_plus_2, &m_plus_1); if (!poly_uni_eq(&ucheck, &sa_e1)) die("sa_e1 mismatch");
    poly_biv_eval_uni(&ucheck, &fa_e2, &m_plus_2, &m_plus_1); if (!poly_uni_eq(&ucheck, &sa_e2)) die("sa_e2 mismatch");
    poly_biv_eval_uni(&ucheck, &fa_csq, &m_plus_2, &m_plus_1); if (!poly_uni_eq(&ucheck, &sa_csq)) die("sa_csq mismatch");
    poly_biv_eval_uni(&ucheck, &fb_e1, &two_m_plus_4, &const_1); if (!poly_uni_eq(&ucheck, &sb_e1)) die("sb_e1 mismatch");
    poly_biv_eval_uni(&ucheck, &fb_e2, &two_m_plus_4, &const_1); if (!poly_uni_eq(&ucheck, &sb_e2)) die("sb_e2 mismatch");
    poly_biv_eval_uni(&ucheck, &fb_csq, &two_m_plus_4, &const_1); if (!poly_uni_eq(&ucheck, &sb_csq)) die("sb_csq mismatch");

    const PolyUni *pos_list[6] = { &sa_e1, &sa_e2, &sa_csq, &sb_e1, &sb_e2, &sb_csq };
    for (int idx = 0; idx < 6; idx++) {
        if (pos_list[idx]->c[0] <= 0) die("positive subfamily constant term not positive");
        for (int d = 0; d <= MAX_UNI_DEG; d++) {
            if (pos_list[idx]->c[d] < 0) die("negative coefficient in positive subfamily");
        }
    }

    /* High-parameter witnesses */
    expect_key(&cur, "high_parameter_witnesses");
    expect_ch(&cur, '{');
    expect_key(&cur, "family_a_p"); int64_t wap = parse_i64(&cur); expect_ch(&cur, ',');
    expect_key(&cur, "family_a_q"); int64_t waq = parse_i64(&cur); expect_ch(&cur, ',');
    char wa_e1_s[128], wa_e2_s[128], wa_csq_s[128];
    expect_key(&cur, "family_a_edge_first_dec");  parse_str(&cur, wa_e1_s, sizeof(wa_e1_s));   expect_ch(&cur, ',');
    expect_key(&cur, "family_a_edge_second_dec"); parse_str(&cur, wa_e2_s, sizeof(wa_e2_s));   expect_ch(&cur, ',');
    expect_key(&cur, "family_a_third_sq_dec");    parse_str(&cur, wa_csq_s, sizeof(wa_csq_s)); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_p"); int64_t wbp = parse_i64(&cur); expect_ch(&cur, ',');
    expect_key(&cur, "family_b_q"); int64_t wbq = parse_i64(&cur); expect_ch(&cur, ',');
    char wb_e1_s[128], wb_e2_s[128], wb_csq_s[128];
    expect_key(&cur, "family_b_edge_first_dec");  parse_str(&cur, wb_e1_s, sizeof(wb_e1_s));   expect_ch(&cur, ',');
    expect_key(&cur, "family_b_edge_second_dec"); parse_str(&cur, wb_e2_s, sizeof(wb_e2_s));   expect_ch(&cur, ',');
    expect_key(&cur, "family_b_third_sq_dec");    parse_str(&cur, wb_csq_s, sizeof(wb_csq_s));
    expect_ch(&cur, '}');

    expect_ch(&cur, '}');
    skip_ws(&cur);
    if (cur.pos != cur.len) die("trailing bytes after JSON object");

    if (wap != 101 || waq != 100 || wbp != 100 || wbq != 1) die("unexpected witness coordinates");
    static const int64_t mods[3] = { 2147483647LL, 2147483629LL, 2147483587LL };
    for (int k = 0; k < 3; k++) {
        int64_t M = mods[k];
        if (dec_str_mod(wa_e1_s, M)  != poly_biv_eval_mod(&fa_e1, wap, waq, M))  die("wa_e1 residue mismatch");
        if (dec_str_mod(wa_e2_s, M)  != poly_biv_eval_mod(&fa_e2, wap, waq, M))  die("wa_e2 residue mismatch");
        if (dec_str_mod(wa_csq_s, M) != poly_biv_eval_mod(&fa_csq, wap, waq, M)) die("wa_csq residue mismatch");
        if (dec_str_mod(wb_e1_s, M)  != poly_biv_eval_mod(&fb_e1, wbp, wbq, M))  die("wb_e1 residue mismatch");
        if (dec_str_mod(wb_e2_s, M)  != poly_biv_eval_mod(&fb_e2, wbp, wbq, M))  die("wb_e2 residue mismatch");
        if (dec_str_mod(wb_csq_s, M) != poly_biv_eval_mod(&fb_csq, wbp, wbq, M)) die("wb_csq residue mismatch");
    }

    free(buf);
    printf("C99_VERIFIER: unified_parametrizations=%lld excluded_fibrations=%lld lean_theorems=%lld PASS\n",
           (long long)unif_cnt, (long long)excl_fibs, (long long)thm_cnt);
    return 0;
}
