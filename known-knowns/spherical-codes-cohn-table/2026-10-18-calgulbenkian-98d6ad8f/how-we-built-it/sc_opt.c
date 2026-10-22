/*
 * sc_opt.c - High-speed Riemannian L-BFGS Log-Sum-Exp & Basin-Hopping Optimizer
 * for Spherical Codes on S^{d-1} (Cohn's spherical-codes.org table).
 *
 * Minimizes c* = max_{j < k} <x_j, x_k> for N unit vectors in R^d.
 * Compile: cc -O3 -o sc_opt sc_opt.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

static uint64_t rng_state = 0x853c49e6748fea9bULL;

static inline uint64_t xorshift64star(void) {
    uint64_t x = rng_state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    rng_state = x;
    return x * 0x2545F4914F6CDD1DULL;
}

static inline double rand_uniform(void) {
    return (xorshift64star() >> 11) * (1.0 / 9007199254740992.0);
}

static inline double rand_normal(void) {
    double u1 = rand_uniform();
    double u2 = rand_uniform();
    if (u1 < 1e-15) u1 = 1e-15;
    return sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
}

static void normalize_vectors(double *x, int d, int n) {
    for (int j = 0; j < n; j++) {
        double *xj = x + j * d;
        double norm_sq = 0.0;
        for (int a = 0; a < d; a++) norm_sq += xj[a] * xj[a];
        double inv = 1.0 / sqrt(norm_sq);
        for (int a = 0; a < d; a++) xj[a] *= inv;
    }
}

static void project_tangent(double *g, const double *x, int d, int n) {
    for (int j = 0; j < n; j++) {
        const double *xj = x + j * d;
        double *gj = g + j * d;
        double dot = 0.0;
        for (int a = 0; a < d; a++) dot += gj[a] * xj[a];
        for (int a = 0; a < d; a++) gj[a] -= dot * xj[a];
    }
}

static double compute_exact_c(const double *x, int d, int n, int *c_1e6, int *c_1e9) {
    double c_max = -2.0;
    int num_pairs = n * (n - 1) / 2;
    double *s_arr = (double *)malloc(sizeof(double) * num_pairs);
    int idx = 0;
    for (int j = 0; j < n; j++) {
        const double *xj = x + j * d;
        for (int k = j + 1; k < n; k++) {
            const double *xk = x + k * d;
            double s = 0.0;
            for (int a = 0; a < d; a++) s += xj[a] * xk[a];
            s_arr[idx++] = s;
            if (s > c_max) c_max = s;
        }
    }
    int c6 = 0, c9 = 0;
    for (int i = 0; i < num_pairs; i++) {
        if (c_max - s_arr[i] <= 1e-6) c6++;
        if (c_max - s_arr[i] <= 1e-9) c9++;
    }
    if (c_1e6) *c_1e6 = c6;
    if (c_1e9) *c_1e9 = c9;
    free(s_arr);
    return c_max;
}

static double eval_lse_fg(const double *x, double *g, int d, int n, double beta, double *out_c) {
    int D = d * n;
    int num_pairs = n * (n - 1) / 2;
    double *s_arr = (double *)malloc(sizeof(double) * num_pairs);
    double *w_arr = (double *)malloc(sizeof(double) * num_pairs);

    double c_max = -2.0;
    int idx = 0;
    for (int j = 0; j < n; j++) {
        const double *xj = x + j * d;
        for (int k = j + 1; k < n; k++) {
            const double *xk = x + k * d;
            double s = 0.0;
            for (int a = 0; a < d; a++) s += xj[a] * xk[a];
            s_arr[idx++] = s;
            if (s > c_max) c_max = s;
        }
    }
    if (out_c) *out_c = c_max;

    double sum_exp = 0.0;
    for (int i = 0; i < num_pairs; i++) {
        double diff = beta * (s_arr[i] - c_max);
        double e = (diff > -700.0) ? exp(diff) : 0.0;
        w_arr[i] = e;
        sum_exp += e;
    }

    double fval = c_max + log(sum_exp) / beta;
    double inv_sum = 1.0 / sum_exp;

    memset(g, 0, sizeof(double) * D);
    idx = 0;
    for (int j = 0; j < n; j++) {
        const double *xj = x + j * d;
        double *gj = g + j * d;
        for (int k = j + 1; k < n; k++) {
            double w = w_arr[idx++] * inv_sum;
            if (w > 1e-30) {
                const double *xk = x + k * d;
                double *gk = g + k * d;
                for (int a = 0; a < d; a++) {
                    gj[a] += w * xk[a];
                    gk[a] += w * xj[a];
                }
            }
        }
    }

    project_tangent(g, x, d, n);
    free(s_arr);
    free(w_arr);
    return fval;
}

static double vec_dot(const double *a, const double *b, int D) {
    double s = 0.0;
    for (int i = 0; i < D; i++) s += a[i] * b[i];
    return s;
}

static void lbfgs_optimize(double *x, double *best_x, double *best_c,
                           int d, int n, double beta, int max_iter) {
    int D = d * n;
    int M = 24;

    double *S = (double *)calloc(M * D, sizeof(double));
    double *Y = (double *)calloc(M * D, sizeof(double));
    double *rho = (double *)calloc(M, sizeof(double));
    double *alpha = (double *)calloc(M, sizeof(double));

    double *g = (double *)malloc(sizeof(double) * D);
    double *g_new = (double *)malloc(sizeof(double) * D);
    double *x_new = (double *)malloc(sizeof(double) * D);
    double *q = (double *)malloc(sizeof(double) * D);
    double *dir = (double *)malloc(sizeof(double) * D);

    double cur_c = 2.0;
    double f = eval_lse_fg(x, g, d, n, beta, &cur_c);
    if (cur_c < *best_c) {
        *best_c = cur_c;
        memcpy(best_x, x, sizeof(double) * D);
    }

    int hist_len = 0;
    int hist_head = 0;

    for (int iter = 0; iter < max_iter; iter++) {
        double gnorm = sqrt(vec_dot(g, g, D));
        if (gnorm < 1e-14) break;

        memcpy(q, g, sizeof(double) * D);
        for (int i = 0; i < hist_len; i++) {
            int idx = (hist_head - 1 - i + M) % M;
            alpha[idx] = rho[idx] * vec_dot(S + idx * D, q, D);
            const double *y_i = Y + idx * D;
            double a = alpha[idx];
            for (int k = 0; k < D; k++) q[k] -= a * y_i[k];
        }

        double gamma = 1.0;
        if (hist_len > 0) {
            int last = (hist_head - 1 + M) % M;
            double sy = vec_dot(S + last * D, Y + last * D, D);
            double yy = vec_dot(Y + last * D, Y + last * D, D);
            if (yy > 1e-30 && sy > 1e-30) gamma = sy / yy;
        }
        for (int k = 0; k < D; k++) dir[k] = gamma * q[k];

        for (int i = hist_len - 1; i >= 0; i--) {
            int idx = (hist_head - 1 - i + M) % M;
            double b = rho[idx] * vec_dot(Y + idx * D, dir, D);
            const double *s_i = S + idx * D;
            double diff = alpha[idx] - b;
            for (int k = 0; k < D; k++) dir[k] += diff * s_i[k];
        }

        for (int k = 0; k < D; k++) dir[k] = -dir[k];

        double g_d = vec_dot(g, dir, D);
        if (g_d >= 0.0) {
            hist_len = 0;
            hist_head = 0;
            for (int k = 0; k < D; k++) dir[k] = -g[k] / gnorm;
            g_d = vec_dot(g, dir, D);
        }

        double step = 1.0;
        double dnorm = sqrt(vec_dot(dir, dir, D));
        if (step * dnorm > 0.5) step = 0.5 / dnorm;

        int accepted = 0;
        double f_new = f;
        for (int ls = 0; ls < 35; ls++) {
            for (int k = 0; k < D; k++) x_new[k] = x[k] + step * dir[k];
            normalize_vectors(x_new, d, n);
            f_new = eval_lse_fg(x_new, g_new, d, n, beta, &cur_c);
            if (cur_c < *best_c) {
                *best_c = cur_c;
                memcpy(best_x, x_new, sizeof(double) * D);
            }
            if (f_new <= f + 1e-4 * step * g_d || f_new < f) {
                accepted = 1;
                break;
            }
            step *= 0.5;
        }

        if (!accepted) {
            hist_len = 0;
            hist_head = 0;
            break;
        }

        double *s_cur = S + hist_head * D;
        double *y_cur = Y + hist_head * D;
        for (int k = 0; k < D; k++) {
            s_cur[k] = x_new[k] - x[k];
            y_cur[k] = g_new[k] - g[k];
        }
        project_tangent(s_cur, x_new, d, n);
        project_tangent(y_cur, x_new, d, n);

        double sy = vec_dot(s_cur, y_cur, D);
        if (sy > 1e-28) {
            rho[hist_head] = 1.0 / sy;
            hist_head = (hist_head + 1) % M;
            if (hist_len < M) hist_len++;
        }

        memcpy(x, x_new, sizeof(double) * D);
        memcpy(g, g_new, sizeof(double) * D);
        f = f_new;
    }

    free(S);
    free(Y);
    free(rho);
    free(alpha);
    free(g);
    free(g_new);
    free(x_new);
    free(q);
    free(dir);
}

static void load_csv_file(const char *path, double *x, int d, int n) {
    FILE *fp = fopen(path, "r");
    if (!fp) {
        fprintf(stderr, "Cannot open %s\n", path);
        exit(1);
    }
    for (int j = 0; j < n; j++) {
        for (int a = 0; a < d; a++) {
            if (fscanf(fp, " %lf", &x[j * d + a]) != 1) {
                fprintf(stderr, "Error reading entry (%d,%d) from %s\n", j, a, path);
                exit(1);
            }
            int ch = fgetc(fp);
            if (ch != ',' && ch != '\n' && ch != '\r' && ch != EOF) {
                ungetc(ch, fp);
            }
        }
    }
    fclose(fp);
}

static void save_csv_file(const char *path, const double *x, int d, int n) {
    FILE *fp = fopen(path, "w");
    if (!fp) {
        fprintf(stderr, "Cannot write %s\n", path);
        exit(1);
    }
    for (int j = 0; j < n; j++) {
        for (int a = 0; a < d; a++) {
            fprintf(fp, "%.17g%s", x[j * d + a], (a == d - 1) ? "\n" : ",");
        }
    }
    fclose(fp);
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s {d} {N} {in_file|RANDOM} {out_file} [restarts] [noise_amp] [seed]\n", argv[0]);
        return 1;
    }
    int d = atoi(argv[1]);
    int n = atoi(argv[2]);
    const char *in_file = argv[3];
    const char *out_file = argv[4];
    int restarts = (argc >= 6) ? atoi(argv[5]) : 5;
    double noise_amp = (argc >= 7) ? atof(argv[6]) : 0.005;
    uint64_t seed = (argc >= 8) ? (uint64_t)atoll(argv[7]) : (uint64_t)time(NULL);
    rng_state = seed ^ 0x9e3779b97f4a7c15ULL;

    int D = d * n;
    double *x_init = (double *)malloc(sizeof(double) * D);
    double *x = (double *)malloc(sizeof(double) * D);
    double *best_x = (double *)malloc(sizeof(double) * D);

    int use_random = (strcmp(in_file, "RANDOM") == 0);
    if (!use_random) {
        load_csv_file(in_file, x_init, d, n);
        normalize_vectors(x_init, d, n);
    } else {
        for (int i = 0; i < D; i++) x_init[i] = rand_normal();
        normalize_vectors(x_init, d, n);
    }

    int c6 = 0, c9 = 0;
    double init_c = compute_exact_c(x_init, d, n, &c6, &c9);
    printf("[sc_opt] d=%d N=%d init_c=%.15f (contacts 1e-6:%d 1e-9:%d)\n", d, n, init_c, c6, c9);

    double best_c = init_c;
    memcpy(best_x, x_init, sizeof(double) * D);

    double betas[] = {
        30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0,
        100000.0, 300000.0, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10
    };
    int num_betas = sizeof(betas) / sizeof(betas[0]);

    for (int r = 0; r < restarts; r++) {
        if (r == 0 && !use_random) {
            memcpy(x, x_init, sizeof(double) * D);
        } else if (use_random) {
            for (int i = 0; i < D; i++) x[i] = rand_normal();
            normalize_vectors(x, d, n);
        } else {
            double amp = noise_amp * pow(0.65, (double)((r - 1) % 6));
            for (int i = 0; i < D; i++) {
                x[i] = best_x[i] + amp * rand_normal();
            }
            normalize_vectors(x, d, n);
        }

        int start_b = 0;
        if (!use_random) {
            start_b = (r == 0) ? 7 : 3;
        }
        for (int b = start_b; b < num_betas; b++) {
            if (r == 0 && !use_random) {
                /* Always start each beta stage from best_x during warm polish! */
                memcpy(x, best_x, sizeof(double) * D);
            }
            lbfgs_optimize(x, best_x, &best_c, d, n, betas[b], 600);
        }
        double trial_c = compute_exact_c(x, d, n, &c6, &c9);
        printf("  [restart %d/%d] trial_c=%.15f best_c=%.15f (diff=%.12f, c6=%d, c9=%d)\n",
               r + 1, restarts, trial_c, best_c, init_c - best_c, c6, c9);
        save_csv_file(out_file, best_x, d, n);
    }

    memcpy(x, best_x, sizeof(double) * D);
    for (int b = 9; b < num_betas; b++) {
        lbfgs_optimize(x, best_x, &best_c, d, n, betas[b], 1000);
    }

    double final_c = compute_exact_c(best_x, d, n, &c6, &c9);
    printf("[sc_opt] FINAL d=%d N=%d final_c=%.15f (improvement=%.12f, contacts 1e-6:%d 1e-9:%d)\n",
           d, n, final_c, init_c - final_c, c6, c9);
    save_csv_file(out_file, best_x, d, n);

    free(x_init);
    free(x);
    free(best_x);
    return 0;
}
