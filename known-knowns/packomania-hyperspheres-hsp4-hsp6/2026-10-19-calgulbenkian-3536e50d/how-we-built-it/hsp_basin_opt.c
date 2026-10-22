/*
 * hsp_basin_opt.c — Lens 2: Compact-Core Shell Transplant, Winner Cascade,
 * and Basin-Hopping L-BFGS + Log-Sum-Exp Optimizer for Packomania hsp4/5/6.
 *
 * Compile:
 *   cc -O3 -march=native -Wall -Wextra -o attempts/c-evaluator-optimizer/hsp_basin_opt attempts/c-evaluator-optimizer/hsp_basin_opt.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#define D 4
#define MAX_N 315
#define MAX_VARS (MAX_N * D)
#define LBFGS_M 14

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
            const double *cj = x + j * D;
            double dx[D], sq_d = 0.0;
            for (int k = 0; k < D; k++) {
                dx[k] = ci[k] - cj[k];
                sq_d += dx[k] * dx[k];
            }
            if (sq_d < min_sq_dist) min_sq_dist = sq_d;
            if (i >= n_free && j >= n_free) continue;
            if (sq_d < two_r * two_r) {
                double dist = sqrt(sq_d);
                double pen = two_r - dist;
                energy += pen * pen;
                if (dist > 1e-18) {
                    double *gj = g + j * D;
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

static void polish_packing(int n, double *x, double *best_x, double *best_r, LbfgsWorkspace *ws) {
    memcpy(x, best_x, n * D * sizeof(double));
    double delta = 2e-5;
    for (int st = 0; st < 28 && delta >= 1e-16; st++) {
        double r_bef = *best_r;
        lbfgs_partial(n, n, x, *best_r + delta, 160, best_x, best_r, ws);
        memcpy(x, best_x, n * D * sizeof(double));
        if (*best_r <= r_bef + 0.05 * delta) delta *= 0.35;
    }
}

typedef struct {
    int n_in;
    int n_out;
    double r_tab;
    double max_in_norm;
    double min_out_norm;
    double in_pts[MAX_VARS];
    double out_pts[MAX_VARS];
    double all_pts[MAX_VARS];
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
        splits[n].max_in_norm = 0.0;
        splits[n].min_out_norm = 1.0;
        for (int i = 0; i < n; i++) {
            int idx;
            double pt[D], sn = 0.0;
            if (fscanf(f, "%d %lf %lf %lf %lf", &idx, &pt[0], &pt[1], &pt[2], &pt[3]) != 5) break;
            memcpy(&splits[n].all_pts[i * D], pt, D * sizeof(double));
            for (int k = 0; k < D; k++) sn += pt[k] * pt[k];
            sn = sqrt(sn);
            if (sn < 1.0 - 1.5 * r_table[n]) {
                memcpy(&splits[n].in_pts[splits[n].n_in * D], pt, D * sizeof(double));
                splits[n].n_in++;
                if (sn > splits[n].max_in_norm) splits[n].max_in_norm = sn;
            } else {
                memcpy(&splits[n].out_pts[splits[n].n_out * D], pt, D * sizeof(double));
                splits[n].n_out++;
                if (sn < splits[n].min_out_norm) splits[n].min_out_norm = sn;
            }
        }
        fclose(f);
    }
    return true;
}

static bool load_coords_file(const char *path, int n, double *x) {
    FILE *f = fopen(path, "r");
    if (!f) return false;
    double hdr;
    if (fscanf(f, "%lf", &hdr) != 1) { fclose(f); return false; }
    for (int i = 0; i < n; i++) {
        int idx;
        if (fscanf(f, "%d %lf %lf %lf %lf", &idx, &x[i*D], &x[i*D+1], &x[i*D+2], &x[i*D+3]) != 5) {
            fclose(f);
            return false;
        }
    }
    fclose(f);
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

static double find_deepest_cavity(int m, const double *x, Rng *rng, double *out_pt) {
    double best_cav_r = -1.0;
    for (int trial = 0; trial < 600; trial++) {
        double pt[D];
        if (trial == 0) {
            pt[0] = pt[1] = pt[2] = pt[3] = 0.0;
        } else if (trial < 300 && m >= 2) {
            int a = (int)(rng_next(rng) % m);
            int b = (int)(rng_next(rng) % m);
            for (int k = 0; k < D; k++) pt[k] = 0.5 * (x[a * D + k] + x[b * D + k]) + 0.06 * rng_normal(rng);
        } else {
            double rad = (trial % 2 == 0) ? (0.35 * rng_uniform(rng)) : (0.60 + 0.18 * rng_uniform(rng));
            double n2 = 0.0;
            for (int k = 0; k < D; k++) { pt[k] = rng_normal(rng); n2 += pt[k] * pt[k]; }
            n2 = sqrt(n2 + 1e-30);
            for (int k = 0; k < D; k++) pt[k] = pt[k] / n2 * rad;
        }
        double step = 0.025;
        for (int it = 0; it < 25; it++) {
            double norm2 = 0.0;
            for (int k = 0; k < D; k++) norm2 += pt[k] * pt[k];
            double norm = sqrt(norm2);
            double min_r = 1.0 - norm;
            int min_j = -1;
            for (int j = 0; j < m; j++) {
                double d2 = 0.0;
                for (int k = 0; k < D; k++) { double df = pt[k] - x[j * D + k]; d2 += df * df; }
                double rj = 0.5 * sqrt(d2);
                if (rj < min_r) { min_r = rj; min_j = j; }
            }
            if (min_r > best_cav_r) {
                best_cav_r = min_r;
                memcpy(out_pt, pt, D * sizeof(double));
            }
            if (min_j == -1) {
                if (norm > 1e-12) for (int k = 0; k < D; k++) pt[k] -= step * (pt[k] / norm);
            } else {
                double d2 = 0.0;
                for (int k = 0; k < D; k++) { double df = pt[k] - x[min_j * D + k]; d2 += df * df; }
                double dist = sqrt(d2 + 1e-30);
                for (int k = 0; k < D; k++) pt[k] += step * (pt[k] - x[min_j * D + k]) / dist;
            }
            step *= 0.88;
        }
    }
    return best_cav_r;
}

int main(void) {
    if (!load_all_splits("data")) return 1;
    LbfgsWorkspace *ws = (LbfgsWorkspace *)calloc(1, sizeof(LbfgsWorkspace));
    Rng rng = { 0xCAFEBABE98765432ULL };

    /* STEP 1: Polish WIN_transplant_hsp4_170.txt and test cascade to N=171 and N=169 */
    double x170[MAX_VARS];
    if (load_coords_file("attempts/far-import-shell-deletion/WIN_transplant_hsp4_170.txt", 170, x170)) {
        double best170[MAX_VARS];
        memcpy(best170, x170, 170 * D * sizeof(double));
        double r170 = (double)eval_exact_radius_ld(170, best170);
        polish_packing(170, x170, best170, &r170, ws);
        long double r170_ld = eval_exact_radius_ld(170, best170);
        printf("[POLISH 170] r_tab=%.12f polished r*=%.20Lf (gain=%+.6Le)\n",
               splits[170].r_tab, r170_ld, r170_ld - (long double)splits[170].r_tab);
        save_hsp_coords("attempts/c-evaluator-optimizer/WIN_hsp4_170_polished.txt", 170, best170, r170_ld);

        /* Cascade 170 -> 171 by inserting 1 sphere at origin or deepest cavity */
        double best171[MAX_VARS], r171 = 0.0;
        for (int t = 0; t < 30; t++) {
            double w[MAX_VARS];
            /* Put newly inserted sphere at index 0, and inner spheres at 1..25 so Stage A adapts inner core */
            double cav[D] = {0, 0, 0, 0};
            if (t > 0) find_deepest_cavity(170, best170, &rng, cav);
            for (int k = 0; k < D; k++) w[k] = cav[k] + 0.01 * rng_normal(&rng);
            int p = 1;
            for (int i = 0; i < 170; i++) {
                double sn = 0.0;
                for (int k = 0; k < D; k++) sn += best170[i*D+k] * best170[i*D+k];
                if (sqrt(sn) < 0.60) {
                    for (int k = 0; k < D; k++) w[p*D+k] = best170[i*D+k] + 0.005 * rng_normal(&rng);
                    p++;
                }
            }
            int nin_171 = p;
            for (int i = 0; i < 170; i++) {
                double sn = 0.0;
                for (int k = 0; k < D; k++) sn += best170[i*D+k] * best170[i*D+k];
                if (sqrt(sn) >= 0.60) {
                    for (int k = 0; k < D; k++) w[p*D+k] = best170[i*D+k];
                    p++;
                }
            }
            double tb_x[MAX_VARS], tb_r = (double)eval_exact_radius_ld(171, w);
            memcpy(tb_x, w, 171 * D * sizeof(double));
            lbfgs_partial(171, nin_171, w, splits[171].r_tab + 1e-4, 250, tb_x, &tb_r, ws);
            lbfgs_partial(171, 171, w, splits[171].r_tab + 1e-4, 250, tb_x, &tb_r, ws);
            lbfgs_partial(171, 171, w, splits[171].r_tab + 1e-5, 250, tb_x, &tb_r, ws);
            if (tb_r > splits[171].r_tab - 5e-4) polish_packing(171, w, tb_x, &tb_r, ws);
            if (tb_r > r171) {
                r171 = tb_r;
                memcpy(best171, tb_x, 171 * D * sizeof(double));
            }
        }
        long double r171_ld = eval_exact_radius_ld(171, best171);
        printf("[CASCADE 170->171] r_tab=%.12f best_r*=%.18Lf gain=%+.4Le\n",
               splits[171].r_tab, r171_ld, r171_ld - (long double)splits[171].r_tab);
        if (r171_ld - (long double)splits[171].r_tab >= 1e-10L) {
            save_hsp_coords("attempts/c-evaluator-optimizer/WIN_hsp4_171.txt", 171, best171, r171_ld);
            printf("  >>> SAVED WIN_hsp4_171.txt! <<<\n");
        }
    }

    /* STEP 2: Extension Row N=301 in d=4 (Milestone p2)
     * First compute exact baseline: hsp4-300.txt + 1 ball at deepest cavity, re-jammed.
     * Then run multi-start Basin-Hopping + shell transplant (e.g. Core(298..300) + Outer(300)) to beat baseline.
     */
    {
        int n_ext = 301;
        double base_x[MAX_VARS], best_base_x[MAX_VARS];
        memcpy(base_x, splits[300].all_pts, 300 * D * sizeof(double));
        Rng base_rng = { 42ULL };
        double cav[D];
        find_deepest_cavity(300, base_x, &base_rng, cav);
        memcpy(&base_x[300 * D], cav, D * sizeof(double));
        double base_r = (double)eval_exact_radius_ld(n_ext, base_x);
        memcpy(best_base_x, base_x, n_ext * D * sizeof(double));
        lbfgs_partial(n_ext, n_ext, base_x, splits[300].r_tab, 300, best_base_x, &base_r, ws);
        polish_packing(n_ext, base_x, best_base_x, &base_r, ws);
        long double base_r_ld = eval_exact_radius_ld(n_ext, best_base_x);
        printf("[EXT N=301 BASELINE] r_base = %.20Lf\n", base_r_ld);
        save_hsp_coords("attempts/c-evaluator-optimizer/EXT_hsp4_301_baseline.txt", n_ext, best_base_x, base_r_ld);

        double best_ext_x[MAX_VARS];
        memcpy(best_ext_x, best_base_x, n_ext * D * sizeof(double));
        double best_ext_r = (double)base_r_ld;

        for (int t = 0; t < 40; t++) {
            double w[MAX_VARS];
            int src = 298 + (t % 3); /* Seed from 298, 299, or 300 */
            int m_src = src;
            memcpy(w, splits[m_src].all_pts, m_src * D * sizeof(double));
            for (int k = m_src; k < n_ext; k++) {
                double c_pt[D];
                find_deepest_cavity(k, w, &rng, c_pt);
                for (int d_i = 0; d_i < D; d_i++) w[k * D + d_i] = c_pt[d_i];
            }
            for (int i = 0; i < n_ext * D; i++) w[i] += 0.004 * rng_normal(&rng);
            double tb_x[MAX_VARS], tb_r = (double)eval_exact_radius_ld(n_ext, w);
            memcpy(tb_x, w, n_ext * D * sizeof(double));
            lbfgs_partial(n_ext, n_ext, w, splits[300].r_tab, 280, tb_x, &tb_r, ws);
            polish_packing(n_ext, w, tb_x, &tb_r, ws);
            if (tb_r > best_ext_r) {
                best_ext_r = tb_r;
                memcpy(best_ext_x, tb_x, n_ext * D * sizeof(double));
            }
        }
        long double ext_r_ld = eval_exact_radius_ld(n_ext, best_ext_x);
        printf("[EXT N=301 OPTIMIZED] r* = %.20Lf (gain over baseline = %+.6Le)\n",
               ext_r_ld, ext_r_ld - base_r_ld);
        save_hsp_coords("attempts/c-evaluator-optimizer/EXT_hsp4_301.txt", n_ext, best_ext_x, ext_r_ld);
    }

    /* STEP 3: Compact-Core + Best-Outer Transplant Scan across all N=50..300
     * Rank candidate (m1, m2) pairs by RADIAL CLEARANCE (min_out(m2) - max_in(m1))!
     */
    for (int n = 50; n <= 300; n++) {
        double rt = splits[n].r_tab;
        int best_m1[5] = {0}, best_m2[5] = {0};
        double best_score[5] = {-1e9, -1e9, -1e9, -1e9, -1e9};

        for (int m1 = 24; m1 <= 300; m1++) {
            if (splits[m1].r_tab <= rt + 1e-9 || splits[m1].n_in == 0) continue;
            for (int m2 = 24; m2 <= 300; m2++) {
                if (splits[m2].r_tab <= rt + 1e-9 || splits[m2].n_out == 0) continue;
                if (splits[m1].n_in + splits[m2].n_out == n) {
                    if (abs(m2 - n) > 15 || abs(m1 - n) > 30) continue;
                    double rad_clear = splits[m2].min_out_norm - splits[m1].max_in_norm;
                    double rb = (splits[m1].r_tab < splits[m2].r_tab) ? splits[m1].r_tab : splits[m2].r_tab;
                    /* Score prioritizes large radial clearance and high rb */
                    double score = rad_clear + 2.0 * (rb - rt);
                    for (int s = 0; s < 5; s++) {
                        if (score > best_score[s]) {
                            for (int k = 4; k > s; k--) {
                                best_score[k] = best_score[k - 1];
                                best_m1[k] = best_m1[k - 1];
                                best_m2[k] = best_m2[k - 1];
                            }
                            best_score[s] = score;
                            best_m1[s] = m1;
                            best_m2[s] = m2;
                            break;
                        }
                    }
                }
            }
        }
        if (best_m1[0] == 0) continue;

        double best_x[MAX_VARS];
        double best_r = 0.0;
        int win_m1 = best_m1[0], win_m2 = best_m2[0];

        for (int s = 0; s < 5 && best_m1[s] > 0; s++) {
            int m1 = best_m1[s], m2 = best_m2[s];
            int nin = splits[m1].n_in, nout = splits[m2].n_out;
            double rb = (splits[m1].r_tab < splits[m2].r_tab) ? splits[m1].r_tab : splits[m2].r_tab;

            for (int rot = 0; rot < 24; rot++) {
                double Q[4][4];
                random_orth4(&rng, Q);
                double x[MAX_VARS];
                for (int i = 0; i < nin; i++) {
                    const double *p = &splits[m1].in_pts[i * D];
                    for (int k = 0; k < D; k++) {
                        double v = 0.0;
                        for (int j = 0; j < D; j++) v += Q[k][j] * p[j];
                        x[i * D + k] = v;
                    }
                }
                memcpy(&x[nin * D], splits[m2].out_pts, nout * D * sizeof(double));

                double trial_best_x[MAX_VARS];
                double trial_best_r = (double)eval_exact_radius_ld(n, x);
                memcpy(trial_best_x, x, n * D * sizeof(double));

                lbfgs_partial(n, nin, x, rb, 240, trial_best_x, &trial_best_r, ws);
                lbfgs_partial(n, nin, x, rt + 0.5 * (rb - rt), 180, trial_best_x, &trial_best_r, ws);
                lbfgs_partial(n, n, x, rt + 0.5 * (rb - rt), 240, trial_best_x, &trial_best_r, ws);
                lbfgs_partial(n, n, x, rt + 1e-5, 240, trial_best_x, &trial_best_r, ws);

                if (trial_best_r > rt - 4e-4) {
                    polish_packing(n, x, trial_best_x, &trial_best_r, ws);
                }
                if (trial_best_r > best_r) {
                    best_r = trial_best_r;
                    win_m1 = m1; win_m2 = m2;
                    memcpy(best_x, trial_best_x, n * D * sizeof(double));
                }
            }
        }

        long double r_ld = eval_exact_radius_ld(n, best_x);
        long double gain = r_ld - (long double)rt;
        if (gain >= -1e-4L) {
            printf("[COMPACT-SCAN] N=%3d (M1=%d[%d] + M2=%d[%d]): r_tab=%.12f best_r*=%.18Lf gain=%+.4Le\n",
                   n, win_m1, splits[win_m1].n_in, win_m2, splits[win_m2].n_out, rt, r_ld, gain);
            fflush(stdout);
        }
        if (gain >= 1e-10L) {
            char out_path[256];
            snprintf(out_path, sizeof(out_path), "attempts/c-evaluator-optimizer/WIN_hsp4_%d.txt", n);
            save_hsp_coords(out_path, n, best_x, r_ld);
            printf("  >>> BREAKTHROUGH! SAVED %s (gain=%+.6Le) <<<\n", out_path, gain);
            fflush(stdout);
        }
    }

    free(ws);
    return 0;
}
