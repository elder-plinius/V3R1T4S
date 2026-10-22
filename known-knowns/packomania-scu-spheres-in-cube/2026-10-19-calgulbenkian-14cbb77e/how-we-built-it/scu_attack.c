#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct { double x, y, z; } Vec3;

static int load_scu(const char *path, Vec3 *c, int max_n) {
    FILE *f = fopen(path, "r");
    if (!f) return 0;
    char line[512];
    int n = 0;
    while (n < max_n && fgets(line, sizeof(line), f)) {
        char *p = line;
        while (*p == ' ' || *p == '\t') p++;
        if (*p == '#' || *p == '\n' || *p == '\r' || *p == '\0') continue;
        double v[6];
        int nf = sscanf(p, "%lf %lf %lf %lf %lf %lf", &v[0], &v[1], &v[2], &v[3], &v[4], &v[5]);
        if (nf == 1) continue;
        if (nf == 3) {
            c[n].x = v[0]; c[n].y = v[1]; c[n].z = v[2];
            n++;
        } else if (nf >= 4) {
            c[n].x = v[1]; c[n].y = v[2]; c[n].z = v[3];
            n++;
        }
    }
    fclose(f);
    return n;
}

static double exact_r_from_c(int n, Vec3 *c) {
    double min_x = 1e9, max_x = -1e9;
    double min_y = 1e9, max_y = -1e9;
    double min_z = 1e9, max_z = -1e9;
    for (int i = 0; i < n; i++) {
        if (c[i].x < min_x) min_x = c[i].x;
        if (c[i].x > max_x) max_x = c[i].x;
        if (c[i].y < min_y) min_y = c[i].y;
        if (c[i].y > max_y) max_y = c[i].y;
        if (c[i].z < min_z) min_z = c[i].z;
        if (c[i].z > max_z) max_z = c[i].z;
    }
    double cx = 0.5 * (min_x + max_x);
    double cy = 0.5 * (min_y + max_y);
    double cz = 0.5 * (min_z + max_z);
    double M = 0.5 * (max_x - min_x);
    if (0.5 * (max_y - min_y) > M) M = 0.5 * (max_y - min_y);
    if (0.5 * (max_z - min_z) > M) M = 0.5 * (max_z - min_z);
    double min_d2 = 1e18;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            double dx = (c[i].x - c[j].x) / M;
            double dy = (c[i].y - c[j].y) / M;
            double dz = (c[i].z - c[j].z) / M;
            double d2 = dx*dx + dy*dy + dz*dz;
            if (d2 < min_d2) min_d2 = d2;
        }
    }
    double d_min = sqrt(min_d2);
    double r = d_min / (2.0 * (2.0 + d_min));
    double scale = (0.5 - r) / M;
    for (int i = 0; i < n; i++) {
        c[i].x = (c[i].x - cx) * scale;
        c[i].y = (c[i].y - cy) * scale;
        c[i].z = (c[i].z - cz) * scale;
    }
    double min_pair = 1e18, max_inf = 0.0;
    for (int i = 0; i < n; i++) {
        if (fabs(c[i].x) > max_inf) max_inf = fabs(c[i].x);
        if (fabs(c[i].y) > max_inf) max_inf = fabs(c[i].y);
        if (fabs(c[i].z) > max_inf) max_inf = fabs(c[i].z);
        for (int j = i + 1; j < n; j++) {
            double dx = c[i].x - c[j].x;
            double dy = c[i].y - c[j].y;
            double dz = c[i].z - c[j].z;
            double d2 = dx*dx + dy*dy + dz*dz;
            if (d2 < min_pair) min_pair = d2;
        }
    }
    double rp = 0.5 * sqrt(min_pair);
    double rw = 0.5 - max_inf;
    return (rp < rw) ? rp : rw;
}

static double eval_wall_pair(int n, const double *x, double R, double *g) {
    int dim = 3 * n;
    for (int i = 0; i < dim; i++) g[i] = 0.0;
    double E = 0.0;
    double D = 2.0 * R;
    double D2 = D * D;
    double wall = 0.5 - R;
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < 3; k++) {
            double v = x[3*i+k];
            if (v > wall) {
                double pen = v - wall;
                E += 0.5 * pen * pen;
                g[3*i+k] += pen;
            } else if (v < -wall) {
                double pen = -wall - v;
                E += 0.5 * pen * pen;
                g[3*i+k] -= pen;
            }
        }
        double xi = x[3*i], yi = x[3*i+1], zi = x[3*i+2];
        for (int j = i + 1; j < n; j++) {
            double dx = xi - x[3*j], dy = yi - x[3*j+1], dz = zi - x[3*j+2];
            double d2 = dx*dx + dy*dy + dz*dz;
            if (d2 < D2) {
                double d = sqrt(d2);
                if (d < 1e-15) d = 1e-15;
                double pen = D - d;
                E += 0.5 * pen * pen;
                double f = -pen / d;
                g[3*i]   += f * dx; g[3*i+1] += f * dy; g[3*i+2] += f * dz;
                g[3*j]   -= f * dx; g[3*j+1] -= f * dy; g[3*j+2] -= f * dz;
            }
        }
    }
    return E;
}

static double lbfgs_wall_pair(int n, Vec3 *c, double R, int max_iter) {
    int dim = 3 * n;
    int m = 15;
    double *x = calloc(dim, sizeof(double));
    double *g = calloc(dim, sizeof(double));
    double *x_old = calloc(dim, sizeof(double));
    double *g_old = calloc(dim, sizeof(double));
    double *d = calloc(dim, sizeof(double));
    double *q = calloc(dim, sizeof(double));
    double *s = calloc(m * dim, sizeof(double));
    double *y = calloc(m * dim, sizeof(double));
    double rho[15], alpha[15];

    for (int i = 0; i < n; i++) {
        x[3*i] = c[i].x; x[3*i+1] = c[i].y; x[3*i+2] = c[i].z;
    }

    double E = eval_wall_pair(n, x, R, g);
    int hist = 0;
    for (int iter = 0; iter < max_iter; iter++) {
        double gnorm2 = 0.0;
        for (int i = 0; i < dim; i++) gnorm2 += g[i] * g[i];
        if (gnorm2 < 1e-32 || E < 1e-33) break;

        for (int i = 0; i < dim; i++) q[i] = g[i];
        int bound = hist < m ? hist : m;
        for (int k = bound - 1; k >= 0; k--) {
            int idx = (hist - 1 - (bound - 1 - k)) % m;
            double dot = 0.0;
            for (int i = 0; i < dim; i++) dot += s[idx*dim + i] * q[i];
            alpha[k] = rho[idx] * dot;
            for (int i = 0; i < dim; i++) q[i] -= alpha[k] * y[idx*dim + i];
        }
        double gamma = 1.0;
        if (hist > 0) {
            int last = (hist - 1) % m;
            double sy = 0.0, yy = 0.0;
            for (int i = 0; i < dim; i++) {
                sy += s[last*dim + i] * y[last*dim + i];
                yy += y[last*dim + i] * y[last*dim + i];
            }
            if (yy > 1e-30 && sy > 1e-30) gamma = sy / yy;
        }
        for (int i = 0; i < dim; i++) d[i] = gamma * q[i];
        for (int k = 0; k < bound; k++) {
            int idx = (hist - bound + k) % m;
            double dot = 0.0;
            for (int i = 0; i < dim; i++) dot += y[idx*dim + i] * d[i];
            double beta = rho[idx] * dot;
            for (int i = 0; i < dim; i++) d[i] += s[idx*dim + i] * (alpha[k] - beta);
        }
        for (int i = 0; i < dim; i++) d[i] = -d[i];

        for (int i = 0; i < dim; i++) { x_old[i] = x[i]; g_old[i] = g[i]; }
        double step = 0.5;
        double E_new = E;
        int accepted = 0;
        for (int ls = 0; ls < 25; ls++) {
            for (int i = 0; i < dim; i++) x[i] = x_old[i] + step * d[i];
            E_new = eval_wall_pair(n, x, R, g);
            if (E_new <= E + 1e-32) { accepted = 1; break; }
            step *= 0.5;
        }
        if (!accepted) {
            step = 0.05;
            for (int i = 0; i < dim; i++) x[i] = x_old[i] - step * g_old[i];
            E_new = eval_wall_pair(n, x, R, g);
            hist = 0;
        } else {
            int slot = hist % m;
            double sy = 0.0;
            for (int i = 0; i < dim; i++) {
                s[slot*dim + i] = x[i] - x_old[i];
                y[slot*dim + i] = g[i] - g_old[i];
                sy += s[slot*dim + i] * y[slot*dim + i];
            }
            if (sy > 1e-32) { rho[slot] = 1.0 / sy; hist++; }
            else hist = 0;
        }
        E = E_new;
    }
    for (int i = 0; i < n; i++) {
        c[i].x = x[3*i]; c[i].y = x[3*i+1]; c[i].z = x[3*i+2];
    }
    free(x); free(g); free(x_old); free(g_old); free(d); free(q); free(s); free(y);
    return E;
}

static double inflate_packing(int n, Vec3 *c, double R_start, double step_init, int stages, int iter_per_stage) {
    Vec3 *best = calloc(n, sizeof(Vec3));
    Vec3 *work = calloc(n, sizeof(Vec3));
    double best_r = exact_r_from_c(n, c);
    memcpy(best, c, n * sizeof(Vec3));
    double R_target = (R_start > best_r) ? R_start : best_r + step_init;
    double step = step_init;
    for (int st = 0; st < stages; st++) {
        memcpy(work, best, n * sizeof(Vec3));
        lbfgs_wall_pair(n, work, R_target, iter_per_stage);
        double r_now = exact_r_from_c(n, work);
        if (r_now > best_r) {
            best_r = r_now;
            memcpy(best, work, n * sizeof(Vec3));
            R_target = best_r + step;
        } else {
            step *= 0.5;
            R_target = best_r + step;
        }
    }
    memcpy(c, best, n * sizeof(Vec3));
    free(best); free(work);
    return best_r;
}

static Vec3 apply_sym(Vec3 p, int sym) {
    double v[3] = {p.x, p.y, p.z};
    int perms[6][3] = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    int pm = sym / 8;
    int sg = sym % 8;
    double x = v[perms[pm][0]] * ((sg & 1) ? -1.0 : 1.0);
    double y = v[perms[pm][1]] * ((sg & 2) ? -1.0 : 1.0);
    double z = v[perms[pm][2]] * ((sg & 4) ? -1.0 : 1.0);
    Vec3 res = {x, y, z};
    return res;
}

static void save_win(int n, const Vec3 *c, double r_opt, double r_tab) {
    char path[256];
    if (r_opt - r_tab >= 1e-11) {
        snprintf(path, sizeof(path), "results/WIN_scu_%d.txt", n);
    } else if (r_opt - r_tab >= -1e-6) {
        snprintf(path, sizeof(path), "results/NEARMISS_scu_%d.txt", n);
    } else {
        return;
    }
    Vec3 *old = calloc(n, sizeof(Vec3));
    if (load_scu(path, old, n) == n) {
        double r_old = exact_r_from_c(n, old);
        if (r_old >= r_opt) { free(old); return; }
    }
    free(old);
    FILE *f = fopen(path, "w");
    for (int i = 0; i < n; i++) {
        fprintf(f, "%.20f %.20f %.20f\n", c[i].x, c[i].y, c[i].z);
    }
    fclose(f);
    printf("   -> Saved %s (r*=%.18f, gain=%+.6e)\n", path, r_opt, r_opt - r_tab);
}

int main(void) {
    Vec3 *c = calloc(2000, sizeof(Vec3));
    Vec3 *c2 = calloc(2000, sizeof(Vec3));

    /* 1. N = 813 (Eckard Specht, MJ=None, in_2026=False) from b4ef1364 scu812.txt + cavity (0.03322779, 0.27689825, 0.36550569) */
    {
        const char *p812 = "cg_branches/2026-10-14-anonymous-c6d1e0ab-b4ef1364/known-knowns/packomania-scu-spheres-in-cube/2026-10-14-anonymous-c6d1e0ab-b4ef1364/object/scu812.txt";
        load_scu(p812, c, 812);
        c[812].x = 0.03322779; c[812].y = 0.27689825; c[812].z = 0.36550569;
        lbfgs_wall_pair(813, c, 0.056960, 2500);
        double r813 = inflate_packing(813, c, 0.05696285, 2e-7, 14, 2000);
        printf("[Voronoi812->813] N=813: r_opt=%.18f vs r_tab=0.056959450362 (gain=%+.6e)\n",
               r813, r813 - 0.056959450362);
        save_win(813, c, r813, 0.056959450362);
        fflush(stdout);
    }

    /* 2. N = 738 (Eckard Specht, in_2026=False) from scu741.txt & scu740.txt */
    {
        load_scu("data/coords/scu/scu740.txt", c, 740);
        lbfgs_wall_pair(738, c, 0.0586275, 2000);
        double r738 = inflate_packing(738, c, 0.058650, 5e-6, 12, 1800);
        printf("[Deletion+LBFGS] N=738: r_opt=%.18f vs r_tab=0.058531064607 (gain=%+.6e, vs_740=%+.6e)\n",
               r738, r738 - 0.058531064607, r738 - 0.058627036756);
        save_win(738, c, r738, 0.058531064607);
        fflush(stdout);
    }

    /* 3. N = 743 & 744 (Eckard Specht, in_2026=False) from scu747.txt */
    {
        load_scu("data/coords/scu/scu747.txt", c, 747);
        lbfgs_wall_pair(744, c, 0.058592, 2000);
        double r744 = inflate_packing(744, c, 0.058595, 2e-6, 12, 1800);
        printf("[Deletion+LBFGS] N=744: r_opt=%.18f vs r_tab=0.058531064606 (gain=%+.6e, vs_747=%+.6e)\n",
               r744, r744 - 0.058531064606, r744 - 0.058586906628);
        save_win(744, c, r744, 0.058531064606);

        load_scu("data/coords/scu/scu747.txt", c, 747);
        lbfgs_wall_pair(743, c, 0.058595, 2000);
        double r743 = inflate_packing(743, c, 0.058605, 2e-6, 12, 1800);
        printf("[Deletion+LBFGS] N=743: r_opt=%.18f vs r_tab=0.058531064606 (gain=%+.6e, vs_747=%+.6e)\n",
               r743, r743 - 0.058531064606, r743 - 0.058586906628);
        save_win(743, c, r743, 0.058531064606);
        fflush(stdout);
    }

    /* 4. N = 471, 472, 473 (with 48-symmetry crystal-vacancy alignment on new scu469.txt + scu500.txt) */
    {
        load_scu("data/coords/scu/scu469.txt", c, 469);
        load_scu("data/coords/scu/scu500.txt", c2, 500);
        Vec3 best_vacs[30]; int best_nv = 0;
        for (int sym = 0; sym < 48; sym++) {
            Vec3 vacs[30]; int nv = 0;
            for (int j = 0; j < 500; j++) {
                Vec3 pj = apply_sym(c2[j], sym);
                double dmin = 1e9;
                for (int i = 0; i < 469; i++) {
                    double d = hypot(hypot(pj.x - c[i].x, pj.y - c[i].y), pj.z - c[i].z);
                    if (d < dmin) dmin = d;
                }
                for (int i = 0; i < nv; i++) {
                    double d = hypot(hypot(pj.x - vacs[i].x, pj.y - vacs[i].y), pj.z - vacs[i].z);
                    if (d < dmin) dmin = d;
                }
                if (dmin > 1.75 * 0.067898240895 && nv < 30) vacs[nv++] = pj;
            }
            if (nv > best_nv) { best_nv = nv; memcpy(best_vacs, vacs, nv * sizeof(Vec3)); }
        }
        printf("scu469 + scu500 best_nv = %d\n", best_nv);
        for (int add = 2; add <= 4; add++) {
            int N = 469 + add;
            double best_r = 0.0;
            for (int t = 0; t < 4; t++) {
                load_scu("data/coords/scu/scu469.txt", c, 469);
                for (int a = 0; a < add; a++) c[469 + a] = best_vacs[(t + a) % best_nv];
                lbfgs_wall_pair(N, c, 0.06789824130, 3000);
                double r_opt = inflate_packing(N, c, 0.06789824095, 5e-11, 8, 1500);
                if (r_opt > best_r) best_r = r_opt;
                save_win(N, c, r_opt, 0.067898240895);
                if (r_opt - 0.067898240895 >= 1e-10) break;
            }
            printf("[Vacancy48] N=%d: best_r=%.18f vs r_tab=0.067898240895 (gain=%+.6e)\n",
                   N, best_r, best_r - 0.067898240895);
            fflush(stdout);
        }
    }

    free(c); free(c2);
    return 0;
}
