/* Penalty relaxation for N equal balls of radius r in the unit ball, R^D.
   Minimise f(x,r) = -r + k/2 * ( sum_{i<j} max(0,2r-|xi-xj|)^2
                                 + sum_i max(0,|xi|+r-1)^2 )
   with L-BFGS, for an increasing sequence of k. */
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define D 4
#define M 12

static double energy(const double *v, double *g, int n, double k) {
    const double *x = v; double r = v[n * D];
    double e = 0.0, gr = -1.0, two_r = 2.0 * r, tr2 = two_r * two_r;
    memset(g, 0, sizeof(double) * (n * D + 1));
    for (int i = 0; i < n; i++) {
        const double *xi = x + i * D;
        for (int j = i + 1; j < n; j++) {
            const double *xj = x + j * D;
            double d0 = xi[0]-xj[0], d1 = xi[1]-xj[1], d2 = xi[2]-xj[2], d3 = xi[3]-xj[3];
            double s = d0*d0 + d1*d1 + d2*d2 + d3*d3;
            if (s >= tr2) continue;
            double d = sqrt(s); if (d < 1e-300) d = 1e-300;
            double ov = two_r - d;
            e += 0.5 * k * ov * ov;
            double c = k * ov / d;
            g[i*D+0] -= c*d0; g[i*D+1] -= c*d1; g[i*D+2] -= c*d2; g[i*D+3] -= c*d3;
            g[j*D+0] += c*d0; g[j*D+1] += c*d1; g[j*D+2] += c*d2; g[j*D+3] += c*d3;
            gr += 2.0 * k * ov;
        }
        double s = xi[0]*xi[0] + xi[1]*xi[1] + xi[2]*xi[2] + xi[3]*xi[3];
        double nr = sqrt(s);
        double ob = nr + r - 1.0;
        if (ob > 0) {
            e += 0.5 * k * ob * ob;
            double c = k * ob / (nr > 1e-300 ? nr : 1e-300);
            for (int a = 0; a < D; a++) g[i*D+a] += c * xi[a];
            gr += k * ob;
        }
    }
    g[n * D] = gr;
    return e - r;
}

static double dot(const double *a, const double *b, int m) {
    double s = 0; for (int i = 0; i < m; i++) s += a[i]*b[i]; return s;
}

/* returns number of iterations used */
typedef double (*efn)(const double *, double *, int, double);
static int lbfgs_f(efn energy, double *v, int n, double k, int maxit, double gtol, int m) {
    double *g = malloc(sizeof(double)*m), *gn = malloc(sizeof(double)*m);
    double *vn = malloc(sizeof(double)*m), *dir = malloc(sizeof(double)*m);
    double *S = malloc(sizeof(double)*m*M), *Y = malloc(sizeof(double)*m*M);
    double rho[M], alpha[M];
    int head = 0, cnt = 0, it;
    double f = energy(v, g, n, k);
    for (it = 0; it < maxit; it++) {
        double gmax = 0; for (int i = 0; i < m; i++) if (fabs(g[i]) > gmax) gmax = fabs(g[i]);
        if (gmax < gtol) break;
        memcpy(dir, g, sizeof(double)*m);
        for (int c = 0; c < cnt; c++) {
            int idx = (head - 1 - c + M) % M;
            alpha[idx] = rho[idx] * dot(S + idx*m, dir, m);
            for (int i = 0; i < m; i++) dir[i] -= alpha[idx] * Y[idx*m+i];
        }
        double gam = 1e-3 / (gmax > 0 ? gmax : 1);
        if (cnt > 0) { int l = (head - 1 + M) % M; gam = 1.0 / (rho[l] * dot(Y+l*m, Y+l*m, m)); }
        for (int i = 0; i < m; i++) dir[i] *= gam;
        for (int c = cnt - 1; c >= 0; c--) {
            int idx = (head - 1 - c + M) % M;
            double b = rho[idx] * dot(Y + idx*m, dir, m);
            for (int i = 0; i < m; i++) dir[i] += S[idx*m+i] * (alpha[idx] - b);
        }
        double gd = dot(g, dir, m);
        if (gd <= 0) { cnt = 0; memcpy(dir, g, sizeof(double)*m);
            for (int i = 0; i < m; i++) dir[i] *= 1e-3 / gmax; gd = dot(g, dir, m); }
        /* limit step so no coordinate moves more than 0.05 */
        double dm = 0; for (int i = 0; i < m; i++) if (fabs(dir[i]) > dm) dm = fabs(dir[i]);
        double step = 1.0; if (dm * step > 0.05) step = 0.05 / dm;
        double fn; int ok = 0;
        for (int ls = 0; ls < 40; ls++) {
            for (int i = 0; i < m; i++) vn[i] = v[i] - step * dir[i];
            fn = energy(vn, gn, n, k);
            if (fn <= f - 1e-4 * step * gd) { ok = 1; break; }
            step *= 0.5;
        }
        if (!ok) { if (cnt == 0) break; cnt = 0; continue; }
        double *s = S + head*m, *y = Y + head*m;
        for (int i = 0; i < m; i++) { s[i] = vn[i] - v[i]; y[i] = gn[i] - g[i]; }
        double sy = dot(s, y, m);
        if (sy > 1e-300) { rho[head] = 1.0 / sy; head = (head + 1) % M; if (cnt < M) cnt++; }
        memcpy(v, vn, sizeof(double)*m); memcpy(g, gn, sizeof(double)*m);
        if (fabs(f - fn) < 1e-17 * (1 + fabs(f))) { f = fn; break; }
        f = fn;
    }
    free(g); free(gn); free(vn); free(dir); free(S); free(Y);
    return it;
}

/* v: n*D coordinates followed by r. Runs the k-continuation. */
int relax(double *v, int n, double k0, double k1, double kfac, int maxit) {
    int tot = 0;
    for (double k = k0; k <= k1 * 1.0000001; k *= kfac)
        tot += lbfgs_f(energy, v, n, k, maxit, 1e-14, n * D + 1);
    return tot;
}

/* feasible radius after optimal uniform scaling; rescales x in place */
double feasible(double *x, int n) {
    double dmin2 = 1e300, mx = 0;
    for (int i = 0; i < n; i++) {
        double s = 0; for (int a = 0; a < D; a++) s += x[i*D+a]*x[i*D+a];
        if (s > mx) mx = s;
        for (int j = i + 1; j < n; j++) {
            double t = 0; for (int a = 0; a < D; a++) { double d = x[i*D+a]-x[j*D+a]; t += d*d; }
            if (t < dmin2) dmin2 = t;
        }
    }
    double dmin = sqrt(dmin2), M_ = sqrt(mx);
    double sc = 1.0 / (dmin / 2 + M_);
    for (int i = 0; i < n * D; i++) x[i] *= sc;
    return dmin / (dmin + 2 * M_);
}

/* Riesz-type energy on x only (r slot ignored): sum (1/d_ij)^p + sum (1/(2(1-|x_i|)))^p,
   distances first divided by scale (global sc_). Returns log of energy for conditioning. */
static double sc_ = 1.0;
static double riesz(const double *x, double *g, int n, double p) {
    double e = 0;
    memset(g, 0, sizeof(double) * (n * D + 1));
    for (int i = 0; i < n; i++) {
        const double *xi = x + i * D;
        for (int j = i + 1; j < n; j++) {
            const double *xj = x + j * D;
            double d0 = xi[0]-xj[0], d1 = xi[1]-xj[1], d2 = xi[2]-xj[2], d3 = xi[3]-xj[3];
            double s = (d0*d0 + d1*d1 + d2*d2 + d3*d3) / (sc_ * sc_);
            double t = pow(s, -0.5 * p);
            e += t;
            double c = -p * t / s / (sc_ * sc_);   /* dE/dx_i = c * (xi-xj) */
            g[i*D+0] += c*d0; g[i*D+1] += c*d1; g[i*D+2] += c*d2; g[i*D+3] += c*d3;
            g[j*D+0] -= c*d0; g[j*D+1] -= c*d1; g[j*D+2] -= c*d2; g[j*D+3] -= c*d3;
        }
        double nr = sqrt(xi[0]*xi[0] + xi[1]*xi[1] + xi[2]*xi[2] + xi[3]*xi[3]);
        double w = 2 * (1 - nr) / sc_;
        if (w <= 0) return 1e300;
        double t = pow(w, -p);
        e += t;
        double c = p * t / w * 2 / sc_ / (nr > 1e-300 ? nr : 1e-300);
        for (int a = 0; a < D; a++) g[i*D+a] += c * xi[a];
    }
    /* minimise log(e): gradient divided by e */
    for (int i = 0; i < n * D; i++) g[i] /= e;
    return log(e);
}
static double feas_r(const double *x, int n) {
    double dmin2 = 1e300, mx = 0;
    for (int i = 0; i < n; i++) {
        double s = 0; for (int a = 0; a < D; a++) s += x[i*D+a]*x[i*D+a];
        if (s > mx) mx = s;
        for (int j = i + 1; j < n; j++) { double t = 0;
            for (int a = 0; a < D; a++) { double d = x[i*D+a]-x[j*D+a]; t += d*d; }
            if (t < dmin2) dmin2 = t; }
    }
    double a = sqrt(dmin2) / 2, b = 1 - sqrt(mx); return a < b ? a : b;
}
/* x: n*D (+1 spare slot). Anneal p from p0 to p1 by factor pfac. */
int riesz_anneal(double *v, int n, double p0, double p1, double pfac, int maxit) {
    int tot = 0;
    for (double p = p0; p <= p1 * 1.0000001; p *= pfac) {
        sc_ = 2 * feas_r(v, n);
        if (sc_ <= 0) sc_ = 1e-3;
        tot += lbfgs_f(riesz, v, n, p, maxit, 1e-12, n * D);
    }
    return tot;
}
