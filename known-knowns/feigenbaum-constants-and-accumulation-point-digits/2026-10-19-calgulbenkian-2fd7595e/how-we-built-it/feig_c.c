#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>

typedef long mpfr_prec_t;
typedef int mpfr_sign_t;
typedef long mpfr_exp_t;
typedef unsigned long mp_limb_t;
typedef struct {
    mpfr_prec_t _mpfr_prec;
    mpfr_sign_t _mpfr_sign;
    mpfr_exp_t _mpfr_exp;
    mp_limb_t *_mpfr_d;
} __mpfr_struct;
typedef __mpfr_struct mpfr_t[1];
typedef __mpfr_struct *mpfr_ptr;
typedef const __mpfr_struct *mpfr_srcptr;
typedef int mpfr_rnd_t;
#define MPFR_RNDN 0

void mpfr_init2(mpfr_ptr, mpfr_prec_t);
void mpfr_clear(mpfr_ptr);
int mpfr_set(mpfr_ptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_set_si(mpfr_ptr, long, mpfr_rnd_t);
int mpfr_set_d(mpfr_ptr, double, mpfr_rnd_t);
int mpfr_set_str(mpfr_ptr, const char *, int, mpfr_rnd_t);
double mpfr_get_d(mpfr_srcptr, mpfr_rnd_t);
int mpfr_snprintf(char *, size_t, const char *, ...);
int mpfr_add(mpfr_ptr, mpfr_srcptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_add_si(mpfr_ptr, mpfr_srcptr, long, mpfr_rnd_t);
int mpfr_sub(mpfr_ptr, mpfr_srcptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_sub_si(mpfr_ptr, mpfr_srcptr, long, mpfr_rnd_t);
int mpfr_si_sub(mpfr_ptr, long, mpfr_srcptr, mpfr_rnd_t);
int mpfr_mul(mpfr_ptr, mpfr_srcptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_mul_si(mpfr_ptr, mpfr_srcptr, long, mpfr_rnd_t);
int mpfr_mul_2ui(mpfr_ptr, mpfr_srcptr, unsigned long, mpfr_rnd_t);
int mpfr_div(mpfr_ptr, mpfr_srcptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_div_si(mpfr_ptr, mpfr_srcptr, long, mpfr_rnd_t);
int mpfr_neg(mpfr_ptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_abs(mpfr_ptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_cmp(mpfr_srcptr, mpfr_srcptr);
int mpfr_cmp_si(mpfr_srcptr, long);
int mpfr_cos(mpfr_ptr, mpfr_srcptr, mpfr_rnd_t);
int mpfr_const_pi(mpfr_ptr, mpfr_rnd_t);
int mpfr_pow_ui(mpfr_ptr, mpfr_srcptr, unsigned long, mpfr_rnd_t);

// Clenshaw evaluation of S(u) = sum_{k=0}^{N-1} c_k T_k(2u - 1)
static void clenshaw_S(mpfr_ptr res, const mpfr_t *c, int N, mpfr_srcptr u, mpfr_prec_t prec) {
    mpfr_t t, two_t, b0, b1, b2, tmp;
    mpfr_init2(t, prec); mpfr_init2(two_t, prec);
    mpfr_init2(b0, prec); mpfr_init2(b1, prec); mpfr_init2(b2, prec); mpfr_init2(tmp, prec);
    mpfr_mul_2ui(t, u, 1, MPFR_RNDN);
    mpfr_sub_si(t, t, 1, MPFR_RNDN);
    mpfr_mul_2ui(two_t, t, 1, MPFR_RNDN);
    mpfr_set_si(b1, 0, MPFR_RNDN);
    mpfr_set_si(b2, 0, MPFR_RNDN);
    for (int k = N - 1; k >= 1; k--) {
        mpfr_mul(tmp, two_t, b1, MPFR_RNDN);
        mpfr_sub(tmp, tmp, b2, MPFR_RNDN);
        mpfr_add(b0, c[k], tmp, MPFR_RNDN);
        mpfr_set(b2, b1, MPFR_RNDN);
        mpfr_set(b1, b0, MPFR_RNDN);
    }
    mpfr_mul(tmp, t, b1, MPFR_RNDN);
    mpfr_sub(tmp, tmp, b2, MPFR_RNDN);
    mpfr_add(res, c[0], tmp, MPFR_RNDN);
    mpfr_clear(t); mpfr_clear(two_t);
    mpfr_clear(b0); mpfr_clear(b1); mpfr_clear(b2); mpfr_clear(tmp);
}

// Clenshaw evaluation of phi(u) = 1 + u * S(u) and dphi/du(u) = S(u) + u * dS/du(u)
static void clenshaw_phi_dphi(mpfr_ptr phi, mpfr_ptr dphi, const mpfr_t *c, int N, mpfr_srcptr u, mpfr_prec_t prec) {
    mpfr_t t, two_t, b0, b1, b2, db0, db1, db2, S, dS_du, tmp;
    mpfr_init2(t, prec); mpfr_init2(two_t, prec);
    mpfr_init2(b0, prec); mpfr_init2(b1, prec); mpfr_init2(b2, prec);
    mpfr_init2(db0, prec); mpfr_init2(db1, prec); mpfr_init2(db2, prec);
    mpfr_init2(S, prec); mpfr_init2(dS_du, prec); mpfr_init2(tmp, prec);

    mpfr_mul_2ui(t, u, 1, MPFR_RNDN);
    mpfr_sub_si(t, t, 1, MPFR_RNDN);
    mpfr_mul_2ui(two_t, t, 1, MPFR_RNDN);
    mpfr_set_si(b1, 0, MPFR_RNDN); mpfr_set_si(b2, 0, MPFR_RNDN);
    mpfr_set_si(db1, 0, MPFR_RNDN); mpfr_set_si(db2, 0, MPFR_RNDN);

    for (int k = N - 1; k >= 1; k--) {
        mpfr_mul(tmp, two_t, b1, MPFR_RNDN);
        mpfr_sub(tmp, tmp, b2, MPFR_RNDN);
        mpfr_add(b0, c[k], tmp, MPFR_RNDN);

        if (dphi != NULL) {
            mpfr_mul(tmp, two_t, db1, MPFR_RNDN);
            mpfr_sub(tmp, tmp, db2, MPFR_RNDN);
            mpfr_add(db0, tmp, b1, MPFR_RNDN);
            mpfr_add(db0, db0, b1, MPFR_RNDN);
            mpfr_set(db2, db1, MPFR_RNDN);
            mpfr_set(db1, db0, MPFR_RNDN);
        }
        mpfr_set(b2, b1, MPFR_RNDN);
        mpfr_set(b1, b0, MPFR_RNDN);
    }
    mpfr_mul(tmp, t, b1, MPFR_RNDN);
    mpfr_sub(tmp, tmp, b2, MPFR_RNDN);
    mpfr_add(S, c[0], tmp, MPFR_RNDN);

    mpfr_mul(tmp, u, S, MPFR_RNDN);
    mpfr_add_si(phi, tmp, 1, MPFR_RNDN);

    if (dphi != NULL) {
        mpfr_mul(tmp, t, db1, MPFR_RNDN);
        mpfr_sub(tmp, tmp, db2, MPFR_RNDN);
        mpfr_add(dS_du, b1, tmp, MPFR_RNDN);
        mpfr_mul_2ui(dS_du, dS_du, 1, MPFR_RNDN);
        mpfr_mul(tmp, u, dS_du, MPFR_RNDN);
        mpfr_add(dphi, S, tmp, MPFR_RNDN);
    }

    mpfr_clear(t); mpfr_clear(two_t);
    mpfr_clear(b0); mpfr_clear(b1); mpfr_clear(b2);
    mpfr_clear(db0); mpfr_clear(db1); mpfr_clear(db2);
    mpfr_clear(S); mpfr_clear(dS_du); mpfr_clear(tmp);
}

typedef struct {
    int j_start, j_end, z, N;
    mpfr_prec_t prec;
    const mpfr_t *c;
    const mpfr_t *b;
    const mpfr_t *u_nodes;
    mpfr_srcptr p1;
    mpfr_srcptr sig;
    mpfr_srcptr inv_p1;
    mpfr_srcptr delta;
    mpfr_t *r_out;
    mpfr_t *e_out;
} worker_arg_t;

static void *worker_feig_res(void *arg) {
    worker_arg_t *w = (worker_arg_t *)arg;
    mpfr_t pu, wj, y, v, pv, tmp;
    mpfr_init2(pu, w->prec); mpfr_init2(wj, w->prec);
    mpfr_init2(y, w->prec); mpfr_init2(v, w->prec);
    mpfr_init2(pv, w->prec); mpfr_init2(tmp, w->prec);
    for (int j = w->j_start; j < w->j_end; j++) {
        clenshaw_phi_dphi(pu, NULL, w->c, w->N, w->u_nodes[j], w->prec);
        mpfr_mul(wj, w->sig, w->u_nodes[j], MPFR_RNDN);
        clenshaw_phi_dphi(y, NULL, w->c, w->N, wj, w->prec);
        mpfr_pow_ui(v, y, w->z, MPFR_RNDN);
        clenshaw_phi_dphi(pv, NULL, w->c, w->N, v, w->prec);
        mpfr_mul(tmp, pu, w->p1, MPFR_RNDN);
        mpfr_sub(w->r_out[j], tmp, pv, MPFR_RNDN);
    }
    mpfr_clear(pu); mpfr_clear(wj); mpfr_clear(y); mpfr_clear(v); mpfr_clear(pv); mpfr_clear(tmp);
    return NULL;
}

static void *worker_eigen_res(void *arg) {
    worker_arg_t *w = (worker_arg_t *)arg;
    mpfr_t wj, y, v, pv, dpv, mult, psi_u, psi_w, psi_v, tmp1, tmp2;
    mpfr_init2(wj, w->prec); mpfr_init2(y, w->prec); mpfr_init2(v, w->prec);
    mpfr_init2(pv, w->prec); mpfr_init2(dpv, w->prec); mpfr_init2(mult, w->prec);
    mpfr_init2(psi_u, w->prec); mpfr_init2(psi_w, w->prec); mpfr_init2(psi_v, w->prec);
    mpfr_init2(tmp1, w->prec); mpfr_init2(tmp2, w->prec);
    for (int j = w->j_start; j < w->j_end; j++) {
        mpfr_mul(wj, w->sig, w->u_nodes[j], MPFR_RNDN);
        clenshaw_phi_dphi(y, NULL, w->c, w->N, wj, w->prec);
        mpfr_pow_ui(v, y, w->z, MPFR_RNDN);
        clenshaw_phi_dphi(pv, dpv, w->c, w->N, v, w->prec);
        mpfr_pow_ui(tmp1, y, w->z - 1, MPFR_RNDN);
        mpfr_mul(mult, dpv, tmp1, MPFR_RNDN);
        mpfr_mul_si(mult, mult, w->z, MPFR_RNDN);

        clenshaw_S(psi_u, w->b, w->N, w->u_nodes[j], w->prec);
        clenshaw_S(psi_w, w->b, w->N, wj, w->prec);
        clenshaw_S(psi_v, w->b, w->N, v, w->prec);

        mpfr_mul(tmp1, mult, psi_w, MPFR_RNDN);
        mpfr_add(tmp1, psi_v, tmp1, MPFR_RNDN);
        mpfr_mul(tmp1, w->inv_p1, tmp1, MPFR_RNDN);
        mpfr_mul(tmp2, w->delta, psi_u, MPFR_RNDN);
        mpfr_sub(w->e_out[j], tmp1, tmp2, MPFR_RNDN);
    }
    mpfr_clear(wj); mpfr_clear(y); mpfr_clear(v); mpfr_clear(pv); mpfr_clear(dpv); mpfr_clear(mult);
    mpfr_clear(psi_u); mpfr_clear(psi_w); mpfr_clear(psi_v); mpfr_clear(tmp1); mpfr_clear(tmp2);
    return NULL;
}

// Persistent state for fast collocation refinement at resolution N and precision prec
typedef struct {
    int z, N;
    mpfr_prec_t prec;
    mpfr_t *c;
    mpfr_t *b;
    mpfr_t delta;
    mpfr_t *u_nodes;
    mpfr_t *r_vec;
    mpfr_t *e_vec;
    mpfr_t max_r;
    mpfr_t max_e;
} feig_ctx_t;

feig_ctx_t *feig_ctx_create(int z, int N, long prec_bits) {
    feig_ctx_t *ctx = (feig_ctx_t *)calloc(1, sizeof(feig_ctx_t));
    ctx->z = z;
    ctx->N = N;
    ctx->prec = prec_bits;
    ctx->c = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    ctx->b = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    ctx->u_nodes = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    ctx->r_vec = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    ctx->e_vec = (mpfr_t *)malloc((N + 1) * sizeof(mpfr_t));
    mpfr_init2(ctx->delta, prec_bits);
    mpfr_init2(ctx->max_r, prec_bits);
    mpfr_init2(ctx->max_e, prec_bits);

    mpfr_t pi, tmp;
    mpfr_init2(pi, prec_bits); mpfr_init2(tmp, prec_bits);
    mpfr_const_pi(pi, MPFR_RNDN);
    for (int j = 0; j < N; j++) {
        mpfr_init2(ctx->c[j], prec_bits); mpfr_set_si(ctx->c[j], 0, MPFR_RNDN);
        mpfr_init2(ctx->b[j], prec_bits); mpfr_set_si(ctx->b[j], 0, MPFR_RNDN);
        mpfr_init2(ctx->u_nodes[j], prec_bits);
        mpfr_init2(ctx->r_vec[j], prec_bits);
        mpfr_init2(ctx->e_vec[j], prec_bits);
        mpfr_mul_si(tmp, pi, 2 * j + 1, MPFR_RNDN);
        mpfr_div_si(tmp, tmp, 2 * N, MPFR_RNDN);
        mpfr_cos(tmp, tmp, MPFR_RNDN);
        mpfr_add_si(tmp, tmp, 1, MPFR_RNDN);
        mpfr_div_si(ctx->u_nodes[j], tmp, 2, MPFR_RNDN);
    }
    mpfr_init2(ctx->e_vec[N], prec_bits);
    mpfr_clear(pi); mpfr_clear(tmp);
    return ctx;
}

void feig_ctx_set_initial(feig_ctx_t *ctx, int K, const double *c_init, const double *b_init, double delta_init) {
    for (int k = 0; k < ctx->N; k++) {
        mpfr_set_d(ctx->c[k], (k < K) ? c_init[k] : 0.0, MPFR_RNDN);
        mpfr_set_d(ctx->b[k], (k < K) ? b_init[k] : 0.0, MPFR_RNDN);
    }
    mpfr_set_d(ctx->delta, delta_init, MPFR_RNDN);
}

void feig_ctx_set_coeff_str(feig_ctx_t *ctx, int is_b, int k, const char *s) {
    if (is_b == 0) mpfr_set_str(ctx->c[k], s, 10, MPFR_RNDN);
    else if (is_b == 1) mpfr_set_str(ctx->b[k], s, 10, MPFR_RNDN);
    else mpfr_set_str(ctx->delta, s, 10, MPFR_RNDN);
}

void feig_ctx_copy_from(feig_ctx_t *dst, const feig_ctx_t *src) {
    int K = (src->N < dst->N) ? src->N : dst->N;
    for (int k = 0; k < dst->N; k++) {
        if (k < K) {
            mpfr_set(dst->c[k], src->c[k], MPFR_RNDN);
            mpfr_set(dst->b[k], src->b[k], MPFR_RNDN);
        } else {
            mpfr_set_si(dst->c[k], 0, MPFR_RNDN);
            mpfr_set_si(dst->b[k], 0, MPFR_RNDN);
        }
    }
    mpfr_set(dst->delta, src->delta, MPFR_RNDN);
}

// Evaluates r_vec, sets ctx->max_r, returns log10(max_r) and fills r_scaled[0..N-1]
double feig_ctx_eval_r(feig_ctx_t *ctx, double *r_scaled) {
    mpfr_t p1, sig, abs_r, tmp;
    mpfr_init2(p1, ctx->prec); mpfr_init2(sig, ctx->prec);
    mpfr_init2(abs_r, ctx->prec); mpfr_init2(tmp, ctx->prec);
    mpfr_set_si(p1, 1, MPFR_RNDN);
    for (int k = 0; k < ctx->N; k++) mpfr_add(p1, p1, ctx->c[k], MPFR_RNDN);
    mpfr_pow_ui(sig, p1, ctx->z, MPFR_RNDN);

    int n_threads = 8;
    pthread_t th[8];
    worker_arg_t args[8];
    int chunk = (ctx->N + n_threads - 1) / n_threads;
    for (int t = 0; t < n_threads; t++) {
        args[t].j_start = t * chunk;
        args[t].j_end = (t + 1) * chunk < ctx->N ? (t + 1) * chunk : ctx->N;
        args[t].z = ctx->z; args[t].N = ctx->N; args[t].prec = ctx->prec;
        args[t].c = ctx->c; args[t].u_nodes = ctx->u_nodes;
        args[t].p1 = p1; args[t].sig = sig; args[t].r_out = ctx->r_vec;
        pthread_create(&th[t], NULL, worker_feig_res, &args[t]);
    }
    for (int t = 0; t < n_threads; t++) pthread_join(th[t], NULL);

    mpfr_set_si(ctx->max_r, 0, MPFR_RNDN);
    for (int j = 0; j < ctx->N; j++) {
        mpfr_abs(abs_r, ctx->r_vec[j], MPFR_RNDN);
        if (mpfr_cmp(abs_r, ctx->max_r) > 0) mpfr_set(ctx->max_r, abs_r, MPFR_RNDN);
    }
    double log10_max_r = -9999.0;
    if (mpfr_cmp_si(ctx->max_r, 0) > 0) {
        for (int j = 0; j < ctx->N; j++) {
            mpfr_div(tmp, ctx->r_vec[j], ctx->max_r, MPFR_RNDN);
            r_scaled[j] = mpfr_get_d(tmp, MPFR_RNDN);
        }
        log10_max_r = (double)ctx->max_r[0]._mpfr_exp * 0.3010299956639812;
    }
    mpfr_clear(p1); mpfr_clear(sig); mpfr_clear(abs_r); mpfr_clear(tmp);
    return log10_max_r;
}

void feig_ctx_update_c(feig_ctx_t *ctx, const double *dc_scaled) {
    mpfr_t tmp;
    mpfr_init2(tmp, ctx->prec);
    for (int k = 0; k < ctx->N; k++) {
        mpfr_set_d(tmp, dc_scaled[k], MPFR_RNDN);
        mpfr_mul(tmp, tmp, ctx->max_r, MPFR_RNDN);
        mpfr_add(ctx->c[k], ctx->c[k], tmp, MPFR_RNDN);
    }
    mpfr_clear(tmp);
}

double feig_ctx_eval_e(feig_ctx_t *ctx, double *e_scaled) {
    mpfr_t p1, inv_p1, sig, s_b, abs_e, tmp;
    mpfr_init2(p1, ctx->prec); mpfr_init2(inv_p1, ctx->prec); mpfr_init2(sig, ctx->prec);
    mpfr_init2(s_b, ctx->prec); mpfr_init2(abs_e, ctx->prec); mpfr_init2(tmp, ctx->prec);
    mpfr_set_si(p1, 1, MPFR_RNDN);
    for (int k = 0; k < ctx->N; k++) mpfr_add(p1, p1, ctx->c[k], MPFR_RNDN);
    mpfr_si_sub(inv_p1, 0, p1, MPFR_RNDN); // wait: 1/p1
    mpfr_set_si(inv_p1, 1, MPFR_RNDN);
    mpfr_div(inv_p1, inv_p1, p1, MPFR_RNDN);
    mpfr_pow_ui(sig, p1, ctx->z, MPFR_RNDN);

    int n_threads = 8;
    pthread_t th[8];
    worker_arg_t args[8];
    int chunk = (ctx->N + n_threads - 1) / n_threads;
    for (int t = 0; t < n_threads; t++) {
        args[t].j_start = t * chunk;
        args[t].j_end = (t + 1) * chunk < ctx->N ? (t + 1) * chunk : ctx->N;
        args[t].z = ctx->z; args[t].N = ctx->N; args[t].prec = ctx->prec;
        args[t].c = ctx->c; args[t].b = ctx->b; args[t].u_nodes = ctx->u_nodes;
        args[t].p1 = p1; args[t].inv_p1 = inv_p1; args[t].sig = sig;
        args[t].delta = ctx->delta; args[t].e_out = ctx->e_vec;
        pthread_create(&th[t], NULL, worker_eigen_res, &args[t]);
    }
    for (int t = 0; t < n_threads; t++) pthread_join(th[t], NULL);

    mpfr_set_si(s_b, -1, MPFR_RNDN);
    for (int k = 0; k < ctx->N; k++) {
        if (k % 2 == 0) mpfr_add(s_b, s_b, ctx->b[k], MPFR_RNDN);
        else mpfr_sub(s_b, s_b, ctx->b[k], MPFR_RNDN);
    }
    mpfr_set(ctx->e_vec[ctx->N], s_b, MPFR_RNDN);

    mpfr_set_si(ctx->max_e, 0, MPFR_RNDN);
    for (int j = 0; j <= ctx->N; j++) {
        mpfr_abs(abs_e, ctx->e_vec[j], MPFR_RNDN);
        if (mpfr_cmp(abs_e, ctx->max_e) > 0) mpfr_set(ctx->max_e, abs_e, MPFR_RNDN);
    }
    double log10_max_e = -9999.0;
    if (mpfr_cmp_si(ctx->max_e, 0) > 0) {
        for (int j = 0; j <= ctx->N; j++) {
            mpfr_div(tmp, ctx->e_vec[j], ctx->max_e, MPFR_RNDN);
            e_scaled[j] = mpfr_get_d(tmp, MPFR_RNDN);
        }
        log10_max_e = (double)ctx->max_e[0]._mpfr_exp * 0.3010299956639812;
    }
    mpfr_clear(p1); mpfr_clear(inv_p1); mpfr_clear(sig);
    mpfr_clear(s_b); mpfr_clear(abs_e); mpfr_clear(tmp);
    return log10_max_e;
}

void feig_ctx_update_b_delta(feig_ctx_t *ctx, const double *db_scaled) {
    mpfr_t tmp;
    mpfr_init2(tmp, ctx->prec);
    for (int k = 0; k < ctx->N; k++) {
        mpfr_set_d(tmp, db_scaled[k], MPFR_RNDN);
        mpfr_mul(tmp, tmp, ctx->max_e, MPFR_RNDN);
        mpfr_add(ctx->b[k], ctx->b[k], tmp, MPFR_RNDN);
    }
    mpfr_set_d(tmp, db_scaled[ctx->N], MPFR_RNDN);
    mpfr_mul(tmp, tmp, ctx->max_e, MPFR_RNDN);
    mpfr_add(ctx->delta, ctx->delta, tmp, MPFR_RNDN);
    mpfr_clear(tmp);
}

void feig_ctx_get_strings(feig_ctx_t *ctx, int digits, char *alpha_buf, char *delta_buf, size_t buf_len) {
    mpfr_t p1, alpha;
    mpfr_init2(p1, ctx->prec); mpfr_init2(alpha, ctx->prec);
    mpfr_set_si(p1, 1, MPFR_RNDN);
    for (int k = 0; k < ctx->N; k++) mpfr_add(p1, p1, ctx->c[k], MPFR_RNDN);
    mpfr_set_si(alpha, -1, MPFR_RNDN);
    mpfr_div(alpha, alpha, p1, MPFR_RNDN);
    mpfr_snprintf(alpha_buf, buf_len, "%.*Rf", digits, alpha);
    mpfr_snprintf(delta_buf, buf_len, "%.*Rf", digits, ctx->delta);
    mpfr_clear(p1); mpfr_clear(alpha);
}

void feig_ctx_get_coeff(feig_ctx_t *ctx, int is_b, int k, int digits, char *buf, size_t buf_len) {
    mpfr_snprintf(buf, buf_len, "%.*Re", digits, is_b ? ctx->b[k] : ctx->c[k]);
}

// Fast C Renormalization trajectory evaluation for p1:
// Given N, prec_bits, mu_str, and m_steps, runs m_steps of T(a) and returns s_m(mu) = 1 + sum(a)
typedef struct {
    int N;
    mpfr_prec_t prec;
    mpfr_t *u_nodes;
    mpfr_t *T_mat; // N * N
    mpfr_t *a;
    mpfr_t *vals;
} renorm_ctx_t;

renorm_ctx_t *renorm_ctx_create(int N, long prec_bits) {
    renorm_ctx_t *rc = (renorm_ctx_t *)calloc(1, sizeof(renorm_ctx_t));
    rc->N = N; rc->prec = prec_bits;
    rc->u_nodes = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    rc->T_mat = (mpfr_t *)malloc(N * N * sizeof(mpfr_t));
    rc->a = (mpfr_t *)malloc(N * sizeof(mpfr_t));
    rc->vals = (mpfr_t *)malloc(N * sizeof(mpfr_t));

    mpfr_t pi, tj, two_tj;
    mpfr_init2(pi, prec_bits); mpfr_init2(tj, prec_bits); mpfr_init2(two_tj, prec_bits);
    mpfr_const_pi(pi, MPFR_RNDN);
    for (int j = 0; j < N; j++) {
        mpfr_init2(rc->u_nodes[j], prec_bits);
        mpfr_init2(rc->a[j], prec_bits);
        mpfr_init2(rc->vals[j], prec_bits);
        mpfr_mul_si(tj, pi, 2 * j + 1, MPFR_RNDN);
        mpfr_div_si(tj, tj, 2 * N, MPFR_RNDN);
        mpfr_cos(tj, tj, MPFR_RNDN);
        mpfr_add_si(rc->u_nodes[j], tj, 1, MPFR_RNDN);
        mpfr_div_si(rc->u_nodes[j], rc->u_nodes[j], 2, MPFR_RNDN);
        mpfr_mul_2ui(two_tj, tj, 1, MPFR_RNDN);
        for (int k = 0; k < N; k++) {
            mpfr_init2(rc->T_mat[j * N + k], prec_bits);
            if (k == 0) mpfr_set_si(rc->T_mat[j * N + k], 1, MPFR_RNDN);
            else if (k == 1) mpfr_set(rc->T_mat[j * N + k], tj, MPFR_RNDN);
            else {
                mpfr_mul(rc->T_mat[j * N + k], two_tj, rc->T_mat[j * N + k - 1], MPFR_RNDN);
                mpfr_sub(rc->T_mat[j * N + k], rc->T_mat[j * N + k], rc->T_mat[j * N + k - 2], MPFR_RNDN);
            }
        }
    }
    mpfr_clear(pi); mpfr_clear(tj); mpfr_clear(two_tj);
    return rc;
}

typedef struct {
    int j_start, j_end, N;
    mpfr_prec_t prec;
    const mpfr_t *a;
    const mpfr_t *u_nodes;
    const mpfr_t *T_mat;
    mpfr_srcptr sig;
    mpfr_srcptr inv_s;
    mpfr_t *vals;
    mpfr_t *a_out;
} renorm_worker_t;

static void *worker_renorm_eval(void *arg) {
    renorm_worker_t *w = (renorm_worker_t *)arg;
    mpfr_t wj, yj, vj, pj;
    mpfr_init2(wj, w->prec); mpfr_init2(yj, w->prec);
    mpfr_init2(vj, w->prec); mpfr_init2(pj, w->prec);
    for (int j = w->j_start; j < w->j_end; j++) {
        mpfr_mul(wj, w->sig, w->u_nodes[j], MPFR_RNDN);
        clenshaw_phi_dphi(yj, NULL, w->a, w->N, wj, w->prec);
        mpfr_mul(vj, yj, yj, MPFR_RNDN);
        clenshaw_phi_dphi(pj, NULL, w->a, w->N, vj, w->prec);
        mpfr_mul(pj, pj, w->inv_s, MPFR_RNDN);
        mpfr_sub_si(pj, pj, 1, MPFR_RNDN);
        mpfr_div(w->vals[j], pj, w->u_nodes[j], MPFR_RNDN);
    }
    mpfr_clear(wj); mpfr_clear(yj); mpfr_clear(vj); mpfr_clear(pj);
    return NULL;
}

static void *worker_renorm_dct(void *arg) {
    renorm_worker_t *w = (renorm_worker_t *)arg;
    mpfr_t acc, prod;
    mpfr_init2(acc, w->prec); mpfr_init2(prod, w->prec);
    int N = w->N;
    for (int k = w->j_start; k < w->j_end; k++) {
        mpfr_set_si(acc, 0, MPFR_RNDN);
        for (int j = 0; j < N; j++) {
            mpfr_mul(prod, w->T_mat[j * N + k], w->vals[j], MPFR_RNDN);
            mpfr_add(acc, acc, prod, MPFR_RNDN);
        }
        if (k > 0) mpfr_mul_2ui(acc, acc, 1, MPFR_RNDN);
        mpfr_div_si(w->a_out[k], acc, N, MPFR_RNDN);
    }
    mpfr_clear(acc); mpfr_clear(prod);
    return NULL;
}

void renorm_eval_sm(renorm_ctx_t *rc, const char *mu_str, int m_steps, int digits, char *s_out_buf, size_t buf_len) {
    int N = rc->N;
    mpfr_set_str(rc->a[0], mu_str, 10, MPFR_RNDN);
    mpfr_neg(rc->a[0], rc->a[0], MPFR_RNDN);
    for (int k = 1; k < N; k++) mpfr_set_si(rc->a[k], 0, MPFR_RNDN);

    mpfr_t s, inv_s, sig, wj, yj, vj, pj, acc, prod;
    mpfr_init2(s, rc->prec); mpfr_init2(inv_s, rc->prec); mpfr_init2(sig, rc->prec);
    mpfr_init2(wj, rc->prec); mpfr_init2(yj, rc->prec); mpfr_init2(vj, rc->prec);
    mpfr_init2(pj, rc->prec); mpfr_init2(acc, rc->prec); mpfr_init2(prod, rc->prec);

    for (int step = 0; step < m_steps; step++) {
        mpfr_set_si(s, 1, MPFR_RNDN);
        for (int k = 0; k < N; k++) mpfr_add(s, s, rc->a[k], MPFR_RNDN);
        mpfr_set_si(inv_s, 1, MPFR_RNDN);
        mpfr_div(inv_s, inv_s, s, MPFR_RNDN);
        mpfr_mul(sig, s, s, MPFR_RNDN);

        for (int j = 0; j < N; j++) {
            mpfr_mul(wj, sig, rc->u_nodes[j], MPFR_RNDN);
            clenshaw_phi_dphi(yj, NULL, rc->a, N, wj, rc->prec);
            mpfr_mul(vj, yj, yj, MPFR_RNDN);
            clenshaw_phi_dphi(pj, NULL, rc->a, N, vj, rc->prec);
            mpfr_mul(pj, pj, inv_s, MPFR_RNDN);
            mpfr_sub_si(pj, pj, 1, MPFR_RNDN);
            mpfr_div(rc->vals[j], pj, rc->u_nodes[j], MPFR_RNDN);
        }

        for (int k = 0; k < N; k++) {
            mpfr_set_si(acc, 0, MPFR_RNDN);
            for (int j = 0; j < N; j++) {
                mpfr_mul(prod, rc->T_mat[j * N + k], rc->vals[j], MPFR_RNDN);
                mpfr_add(acc, acc, prod, MPFR_RNDN);
            }
            if (k > 0) mpfr_mul_2ui(acc, acc, 1, MPFR_RNDN);
            mpfr_div_si(rc->a[k], acc, N, MPFR_RNDN);
        }
    }
    mpfr_set_si(s, 1, MPFR_RNDN);
    for (int k = 0; k < N; k++) mpfr_add(s, s, rc->a[k], MPFR_RNDN);
    mpfr_snprintf(s_out_buf, buf_len, "%.*Rf", digits, s);
    mpfr_clear(s); mpfr_clear(inv_s); mpfr_clear(sig);
    mpfr_clear(wj); mpfr_clear(yj); mpfr_clear(vj); mpfr_clear(pj);
    mpfr_clear(acc); mpfr_clear(prod);
}
