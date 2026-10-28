/*
 * transplant_scan.c — Two-Stage Inner-Core + Outer-Shell Transplant Optimizer for hsp4
 *
 * Stage A: Rotate Core(M1) by Q in O(4) and optimize ONLY the inner spheres inside fixed Outer(M2).
 * Stage B: Unfreeze all N = |Core(M1)| + |Outer(M2)| spheres and polish with L-BFGS soft-sphere jamming.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#define D 4
#define MAX_N 310
#define MAX_VARS (MAX_N * D)
#define LBFGS_M 12

typedef struct { uint64_t s; } Rng;

static inline uint64_t rng_next(Rng *r) {
    uint64_t x = r->s;
    x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
    r->s = x;
    return x * 2685821657736338717ULL;
}
static inline double rng_uniform(Rng *r) {
    return (rng_next(r) >> 11) * (1.0 / 9007199254740992.0);
}
static inline double rng_normal(Rng *r) {
    double u1 = rng_uniform(r), u2 = rng_uniform(r);
    if (u1 < 1e-15) u1 = 1e-15;
    return sqrt(-2.0 * log(u1)) * cos(6.28318530717958647692 * u2);
}

/* Generate random 4x4 orthogonal matrix via Gram-Schmidt */
static void random_orth4(Rng *rng, double Q[4][4]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) Q[i][j] = rng_normal(rng);
        for (int k = 0; k < i; k++) {
            double dot = 0.0;
            for (int j = 0; j < 4; j++) dot += Q[i][j] * Q[k][j];
            for (int j = 0; j < 4; j++) Q[i][j] -= dot * Q[k][j];
        }
        double norm = 0.0;
        for (int j = 0; j < 4; j++) norm += Q[i][j] * Q[i][j];
        norm = sqrt(norm + 1e-30);
        for (int j = 0; j < 4; j++) Q[i][j] /= norm;
    }
}

static long double eval_exact_radius_ld(int n, const double *x) {
    long double min_sq_dist = 1e30L;
    long double max_sq_norm = 0.0L;
    for (int i = 0; i < n; i++) {
        const double *ci = x + i * D;
        long double sq_n = 0.0L;
        for (int k = 0; k < D; k++) {
            long double v = (long double)ci[k];
            sq_n += v * v;
        }
        if (sq_n > max_sq_norm) max_sq_norm = sq_n;
        for (int j = i + 1; j < n; j++) {
            const double *cj = x + j * D;
            long double sq_d = 0.0L;
            for (int k = 0; k < D; k++) {
                long double df = (long double)ci[k] - (long double)cj[k];
                sq_d += df * df;
            }
            if (sq_d < min_sq_dist) min_sq_dist = sq_d;
        }
    }
    long double r_pair = 0.5L * sqrtl(min_sq_dist);
    long double r_wall = 1.0L - sqrtl(max_sq_norm);
    return (r_pair < r_wall) ? r_pair : r_wall;
}

/* Harmonic overlap energy where indices [0 .. n_free-1] are movable and [n_free .. n-1] are frozen */
static double eval_harm_partial_fg(int n, int n_free, const double *x, double r_tgt,
                                   double *g, double *out_r_star) {
    int nv = n * D;
    for (int i = 0; i < nv; i++) g[i] = 0.0;
    double two_r = 2.0 * r_tgt;
    double wall_lim = 1.0 - r_tgt;
    double energy = 0.0;
    double min_sq_dist = 1e30;
    double max_sq_norm = 0.0;

    for (int i = 0; i < n; i++) {
        const double *ci = x + i * D;
        double *gi = g + i * D;
        double sq_n = 0.0;
        for (int k = 0; k < D; k++) sq_n += ci[k] * ci[k];
        if (sq_n > max_sq_norm) max_sq_norm = sq_n;
        if (sq_n > wall_lim * wall_lim) {
            double norm = sqrt(sq_n);
            double pen = norm - wall_lim;
            energy += pen * pen;
            if (i < n_free) {
                double scale = 2.0 * pen / (norm + 1e-30);
                for (int k = 0; k < D; k++) gi[k] += scale * ci[k];
            }
        }
        for (int j = i + 1; j < n; j++) {
            if (i >= n_free && j >= n_free) {
                /* Both frozen: still track min_sq_dist on first pass if needed, or skip if pre-checked */
                const double *cj = x + j * D;
                double sq_d = 0.0;
                for (int k = 0; k < D; k++) {
                    double df = ci[k] - cj[k];
                    sq_d += df * df;
                }
                if (sq_d < min_sq_dist) min_sq_dist = sq_d;
                continue;
            }
            const double *cj = x + j * D;
            double *gj = g + j * D;
            double dx[D], sq_d = 0.0;
            for (int k = 0; k < D; k++) {
                dx[k] = ci[k] - cj[k];
                sq_d += dx[k] * dx[k];
            }
            if (sq_d < min_sq_dist) min_sq_dist = sq_d;
            if (sq_d < two_r * two_r) {
                double dist = sqrt(sq_d);
                double pen = two_r - dist;
                energy += pen * pen;
                if (dist > 1e-18) {
                    double scale = -2.0 * pen / dist;
                    for (int k = 0; k < D; k++) {
                        double f = scale * dx[k];
                        if (i < n_free) gi[k] += f;
                        if (j < n_free) gj[k] -= f;
                    }
                }
            }
        }
    }
    double r_pair = 0.5 * sqrt(min_sq_dist);
    double r_wall = 1.0 - sqrt(max_sq_norm);
    *out_r_star = (r_pair < r_wall) ? r_pair : r_wall;
    return energy;
}

typedef struct {
    double s[LBFGS_M][MAX_VARS];
    double y[LBFGS_M][MAX_VARS];
    double rho[LBFGS_M];
    double q[MAX_VARS];
    double dir[MAX_VARS];
    double x_new[MAX_VARS];
    double g_new[MAX_VARS];
    double g[MAX_VARS];
} LbfgsWorkspace;

static double dot_vec(int n, const double *a, const double *b) {
    double s = 0.0;
    for (int i = 0; i < n; i++) s += a[i] * b[i];
    return s;
}

static double lbfgs_partial(int n, int n_free, double *x, double r_tgt, int max_iter,
                            double *best_x, double *best_r, LbfgsWorkspace *ws) {
    int nv_free = n_free * D;
    int nv_all = n * D;
    double cur_r = 0.0;
    double f = eval_harm_partial_fg(n, n_free, x, r_tgt, ws->g, &cur_r);
    if (cur_r > *best_r) {
        *best_r = cur_r;
        memcpy(best_x, x, nv_all * sizeof(double));
    }

    int hist_cnt = 0, hist_head = 0;
    double alpha_hist[LBFGS_M];
    memcpy(ws->x_new, x, nv_all * sizeof(double));

    for (int iter = 0; iter < max_iter; iter++) {
        double gnorm2 = dot_vec(nv_free, ws->g, ws->g);
        if (gnorm2 < 1e-28 || f < 1e-28) break;

        for (int i = 0; i < nv_free; i++) ws->q[i] = ws->g[i];
        int m_cur = (hist_cnt < LBFGS_M) ? hist_cnt : LBFGS_M;
        for (int k = m_cur - 1; k >= 0; k--) {
            int idx = (hist_head - m_cur + k + LBFGS_M * 2) % LBFGS_M;
            double a = ws->rho[idx] * dot_vec(nv_free, ws->s[idx], ws->q);
            alpha_hist[k] = a;
            for (int i = 0; i < nv_free; i++) ws->q[i] -= a * ws->y[idx][i];
        }
        double gamma = 1.0;
        if (m_cur > 0) {
            int last = (hist_head - 1 + LBFGS_M) % LBFGS_M;
            double yy = dot_vec(nv_free, ws->y[last], ws->y[last]);
            if (yy > 1e-30) gamma = 1.0 / (ws->rho[last] * yy);
        }
        for (int i = 0; i < nv_free; i++) ws->dir[i] = ws->q[i] * gamma;
        for (int k = 0; k < m_cur; k++) {
            int idx = (hist_head - m_cur + k + LBFGS_M * 2) % LBFGS_M;
            double b = ws->rho[idx] * dot_vec(nv_free, ws->y[idx], ws->dir);
            double diff = alpha_hist[k] - b;
            for (int i = 0; i < nv_free; i++) ws->dir[i] += diff * ws->s[idx][i];
        }
        for (int i = 0; i < nv_free; i++) ws->dir[i] = -ws->dir[i];

        double dg = dot_vec(nv_free, ws->dir, ws->g);
        if (dg >= 0.0) {
            for (int i = 0; i < nv_free; i++) ws->dir[i] = -ws->g[i];
            dg = -gnorm2;
            hist_cnt = 0;
        }

        double step = 1.0, f_new = f, r_new = cur_r;
        bool accepted = false;
        for (int ls = 0; ls < 18; ls++) {
            for (int i = 0; i < nv_free; i++) ws->x_new[i] = x[i] + step * ws->dir[i];
            f_new = eval_harm_partial_fg(n, n_free, ws->x_new, r_tgt, ws->g_new, &r_new);
            if (r_new > *best_r) {
                *best_r = r_new;
                memcpy(best_x, ws->x_new, nv_all * sizeof(double));
            }
            if (f_new <= f + 1e-4 * step * dg || f_new < f) {
                accepted = true;
                break;
            }
            step *= 0.45;
        }
        if (!accepted) {
            hist_cnt = 0;
            break;
        }

        int slot = hist_head;
        double sy = 0.0;
        for (int i = 0; i < nv_free; i++) {
            double si = ws->x_new[i] - x[i];
            double yi = ws->g_new[i] - ws->g[i];
            ws->s[slot][i] = si;
            ws->y[slot][i] = yi;
            sy += si * yi;
        }
        if (sy > 1e-28) {
            ws->rho[slot] = 1.0 / sy;
            hist_head = (hist_head + 1) % LBFGS_M;
            hist_cnt++;
        }
        memcpy(x, ws->x_new, nv_free * sizeof(double));
        memcpy(ws->g, ws->g_new, nv_free * sizeof(double));
        f = f_new;
        cur_r = r_new;
    }
    return f;
}

typedef struct {
    int n_in;
    int n_out;
    double r_tab;
    double in_pts[MAX_VARS];
    double out_pts[MAX_VARS];
} ShellSplit;

static ShellSplit splits[MAX_N];

static bool load_all_splits(const char *data_dir) {
    FILE *fr = fopen("data/hsp4/radius.txt", "r");
    if (!fr) return false;
    int n; double r;
    double r_table[MAX_N] = {0};
    while (fscanf(fr, "%d %lf", &n, &r) == 2) {
        if (n >= 2 && n <= 300) r_table[n] = r;
    }
    fclose(fr);

    for (n = 2; n <= 300; n++) {
        char path[256];
        snprintf(path, sizeof(path), "%s/coords/hsp4/hsp4-%d.txt", data_dir, n);
        FILE *f = fopen(path, "r");
        if (!f) continue;
        double hdr;
        if (fscanf(f, "%lf", &hdr) != 1) { fclose(f); continue; }
        splits[n].r_tab = r_table[n];
        splits[n].n_in = 0;
        splits[n].n_out = 0;
        for (int i = 0; i < n; i++) {
            int idx;
            double pt[D], sn = 0.0;
            if (fscanf(f, "%d %lf %lf %lf %lf", &idx, &pt[0], &pt[1], &pt[2], &pt[3]) != 5) break;
            for (int k = 0; k < D; k++) sn += pt[k] * pt[k];
            sn = sqrt(sn);
            if (sn < 1.0 - 1.5 * r_table[n]) {
                memcpy(&splits[n].in_pts[splits[n].n_in * D], pt, D * sizeof(double));
                splits[n].n_in++;
            } else {
                memcpy(&splits[n].out_pts[splits[n].n_out * D], pt, D * sizeof(double));
                splits[n].n_out++;
            }
        }
        fclose(f);
    }
    return true;
}

static void save_hsp_coords(const char *path, int n, const double *x, long double r_star) {
    FILE *f = fopen(path, "w");
    if (!f) return;
    fprintf(f, "%.20Lf\n", r_star);
    for (int i = 0; i < n; i++) {
        fprintf(f, "%4d", i + 1);
        for (int k = 0; k < D; k++) fprintf(f, " %22.17f", x[i * D + k]);
        fprintf(f, "\n");
    }
    fclose(f);
}

int main(void) {
    if (!load_all_splits("data")) {
        fprintf(stderr, "Failed to load hsp4 splits\n");
        return 1;
    }

    LbfgsWorkspace *ws = (LbfgsWorkspace *)calloc(1, sizeof(LbfgsWorkspace));
    Rng rng = { 0x123456789ABCDEF0ULL };

    for (int n = 146; n <= 300; n++) {
        if (n == 170) continue; /* Already won and verified WIN_transplant_hsp4_170.txt */
        double rt = splits[n].r_tab;
        int best_m1[6] = {0}, best_m2[6] = {0};
        double best_bound[6] = {0};
        for (int m1 = 20; m1 <= 300; m1++) {
            if (splits[m1].r_tab <= rt + 1e-9 || splits[m1].n_in == 0) continue;
            for (int m2 = 20; m2 <= 300; m2++) {
                if (splits[m2].r_tab <= rt + 1e-9 || splits[m2].n_out == 0) continue;
                if (splits[m1].n_in + splits[m2].n_out == n) {
                    double rb = (splits[m1].r_tab < splits[m2].r_tab) ? splits[m1].r_tab : splits[m2].r_tab;
                    if (abs(m2 - n) > 25) continue;
                    /* Allow m1=142,145 or nearby m1 */
                    if (abs(m1 - n) > 25 && m1 != 142 && m1 != 145) continue;
                    for (int s = 0; s < 6; s++) {
                        if (rb > best_bound[s]) {
                            for (int k = 5; k > s; k--) {
                                best_bound[k] = best_bound[k - 1];
                                best_m1[k] = best_m1[k - 1];
                                best_m2[k] = best_m2[k - 1];
                            }
                            best_bound[s] = rb;
                            best_m1[s] = m1;
                            best_m2[s] = m2;
                            break;
                        }
                    }
                }
            }
        }
        if (best_bound[0] <= 0.0) continue;

        double best_x[MAX_VARS];
        double best_r = 0.0;
        for (int s = 0; s < 6 && best_bound[s] > 0.0; s++) {
            int m1 = best_m1[s], m2 = best_m2[s];
            int nin = splits[m1].n_in, nout = splits[m2].n_out;
            double rb = best_bound[s];
            double alpha = (rt + 5e-5) / splits[m1].r_tab;
            if (alpha > 1.0) alpha = 1.0;
            double beta_out = (1.0 - (rt + 5e-5)) / (1.0 - splits[m2].r_tab);
            if (beta_out < 1.0) beta_out = 1.0;

            for (int rot = 0; rot < 20; rot++) {
                double Q[4][4];
                random_orth4(&rng, Q);
                double x[MAX_VARS];
                double cur_alpha = (rot % 2 == 0) ? alpha : 1.0;
                double cur_beta  = (rot % 2 == 0) ? beta_out : 1.0;
                for (int i = 0; i < nin; i++) {
                    const double *p = &splits[m1].in_pts[i * D];
                    for (int k = 0; k < D; k++) {
                        double v = 0.0;
                        for (int j = 0; j < D; j++) v += Q[k][j] * p[j];
                        x[i * D + k] = cur_alpha * v;
                    }
                }
                for (int i = 0; i < nout * D; i++) {
                    x[nin * D + i] = cur_beta * splits[m2].out_pts[i];
                }

                double trial_best_x[MAX_VARS];
                double trial_best_r = (double)eval_exact_radius_ld(n, x);
                memcpy(trial_best_x, x, n * D * sizeof(double));

                /* Stage A: Optimize ONLY the nin inner spheres */
                lbfgs_partial(n, nin, x, rt + 0.5 * (rb - rt), 220, trial_best_x, &trial_best_r, ws);
                lbfgs_partial(n, nin, x, rt + 2e-5, 180, trial_best_x, &trial_best_r, ws);

                /* Stage B: Unfreeze all n spheres and jam */
                lbfgs_partial(n, n, x, rt + 0.3 * (rb - rt), 220, trial_best_x, &trial_best_r, ws);
                lbfgs_partial(n, n, x, rt + 1e-5, 220, trial_best_x, &trial_best_r, ws);

                if (trial_best_r > rt - 5e-4) {
                    memcpy(x, trial_best_x, n * D * sizeof(double));
                    double delta = 1e-5;
                    for (int st = 0; st < 20 && delta >= 1e-15; st++) {
                        double r_bef = trial_best_r;
                        lbfgs_partial(n, n, x, trial_best_r + delta, 140, trial_best_x, &trial_best_r, ws);
                        memcpy(x, trial_best_x, n * D * sizeof(double));
                        if (trial_best_r <= r_bef + 0.05 * delta) delta *= 0.35;
                    }
                }

                if (trial_best_r > best_r) {
                    best_r = trial_best_r;
                    memcpy(best_x, trial_best_x, n * D * sizeof(double));
                }
            }
        }

        long double r_ld = eval_exact_radius_ld(n, best_x);
        long double gain = r_ld - (long double)rt;
        printf("[TRANSPLANT] N=%3d (M1=%d[%d] + M2=%d[%d]): r_tab=%.12f best_r*=%.16Lf gain=%+.4Le\n",
               n, best_m1[0], splits[best_m1[0]].n_in, best_m2[0], splits[best_m2[0]].n_out, rt, r_ld, gain);
        fflush(stdout);

        if (gain >= 1e-10L) {
            char out_path[256];
            snprintf(out_path, sizeof(out_path), "attempts/far-import-shell-deletion/WIN_transplant_hsp4_%d.txt", n);
            save_hsp_coords(out_path, n, best_x, r_ld);
            printf("  >>> BREAKTHROUGH! SAVED %s (gain=%+.6Le) <<<\n", out_path, gain);
            fflush(stdout);
        }
    }

    free(ws);
    return 0;
}
