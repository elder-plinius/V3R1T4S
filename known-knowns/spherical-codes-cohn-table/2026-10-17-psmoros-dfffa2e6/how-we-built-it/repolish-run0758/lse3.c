// brute-scale lens: BLAS-backed (Accelerate) objectives, all pairs. Build:
// clang -O3 -mcpu=native -shared -fPIC -o liblse2.so lse2.c -framework Accelerate
#define ACCELERATE_NEW_LAPACK
#include <Accelerate/Accelerate.h>
#include <math.h>
#include <string.h>

static void normrows(int N, int d, const double *x, double *Y, double *nrm) {
    for (int i = 0; i < N; i++) {
        double s = 0;
        for (int k = 0; k < d; k++) s += x[i * d + k] * x[i * d + k];
        s = sqrt(s); nrm[i] = s;
        double inv = 1.0 / s;
        for (int k = 0; k < d; k++) Y[i * d + k] = x[i * d + k] * inv;
    }
}

static void project(int N, int d, const double *Y, const double *nrm, double *grad) {
    for (int i = 0; i < N; i++) {
        double *gi = grad + (size_t)i * d; const double *yi = Y + (size_t)i * d;
        double s = 0;
        for (int k = 0; k < d; k++) s += gi[k] * yi[k];
        for (int k = 0; k < d; k++) gi[k] = (gi[k] - s * yi[k]) / nrm[i];
    }
}

// work: N*d + N + N*N doubles
double lse_fg(int N, int d, const double *x, double beta, double *grad, double *work) {
    double *Y = work, *nrm = work + (size_t)N * d, *G = nrm + N;
    normrows(N, d, x, Y, nrm);
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, d, 1.0, Y, d, Y, d, 0.0, G, N);
    double m = -3.0;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) { double s = G[(size_t)i * N + j]; if (s > m) m = s; }
    double S = 0, cut = -40.0 / beta;
    for (int i = 0; i < N; i++) {
        G[(size_t)i * N + i] = 0.0;
        for (int j = i + 1; j < N; j++) {
            double t = G[(size_t)i * N + j] - m, e = 0.0;
            if (t > cut) { e = exp(beta * t); S += e; }
            G[(size_t)i * N + j] = e; G[(size_t)j * N + i] = e;
        }
    }
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, N, d, N, 1.0 / S, G, N, Y, d, 0.0, grad, d);
    project(N, d, Y, nrm, grad);
    return m + log(S) / beta;
}

double pen_fg(int N, int d, const double *x, double t, double *grad, double *work) {
    double *Y = work, *nrm = work + (size_t)N * d, *G = nrm + N;
    normrows(N, d, x, Y, nrm);
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, d, 1.0, Y, d, Y, d, 0.0, G, N);
    double E = 0;
    for (int i = 0; i < N; i++) {
        G[(size_t)i * N + i] = 0.0;
        for (int j = i + 1; j < N; j++) {
            double o = G[(size_t)i * N + j] - t, w = 0.0;
            if (o > 0) { E += o * o; w = 2 * o; }
            G[(size_t)i * N + j] = w; G[(size_t)j * N + i] = w;
        }
    }
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, N, d, N, 1.0, G, N, Y, d, 0.0, grad, d);
    project(N, d, Y, nrm, grad);
    return E;
}

double cmax(int N, int d, const double *x, double *work) {
    double *Y = work, *nrm = work + (size_t)N * d, *G = nrm + N;
    normrows(N, d, x, Y, nrm);
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, d, 1.0, Y, d, Y, d, 0.0, G, N);
    double m = -3.0;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) { double s = G[(size_t)i * N + j]; if (s > m) m = s; }
    return m;
}

// ---------- L-BFGS polish entirely in C ----------
// Minimises lse_fg(x; beta) for each beta in betas[0..nb-1], maxiter iterations per stage, memory M.
// x is updated in place (rows renormalised after each stage). Returns the final cmax.
// work: N*d + N + N*N doubles (objective) ; lw: (2*M+4)*n + 2*M doubles with n = N*d.
static double dotn(int n, const double *a, const double *b) { double s = 0; for (int i = 0; i < n; i++) s += a[i] * b[i]; return s; }

static int MODE = 0;
static double objf(int N, int d, const double *x, double p, double *g, double *w) { return MODE ? pen_fg(N, d, x, p, g, w) : lse_fg(N, d, x, p, g, w); }
int lbfgs_stage(int N, int d, double *x, double beta, int maxiter, int M, double *work, double *lw, double gtol) {
    int n = N * d;
    double *S = lw, *Yv = lw + (size_t)M * n, *g = lw + (size_t)2 * M * n, *dir = g + n, *xn = dir + n, *gn = xn + n;
    double *rho = gn + n, *alpha = rho + M;
    double f = objf(N, d, x, beta, g, work);
    int k = 0, head = 0, it;
    for (it = 0; it < maxiter; it++) {
        double gg = sqrt(dotn(n, g, g));
        if (gg < gtol) break;
        // two-loop recursion
        for (int i = 0; i < n; i++) dir[i] = -g[i];
        int mm = k < M ? k : M;
        for (int j = 0; j < mm; j++) {
            int idx = (head - 1 - j + M) % M;
            double a = rho[idx] * dotn(n, S + (size_t)idx * n, dir);
            alpha[idx] = a;
            double *yy = Yv + (size_t)idx * n;
            for (int i = 0; i < n; i++) dir[i] -= a * yy[i];
        }
        double gam;
        if (mm > 0) {
            int idx = (head - 1 + M) % M;
            double *yy = Yv + (size_t)idx * n;
            gam = dotn(n, S + (size_t)idx * n, yy) / dotn(n, yy, yy);
        } else gam = 1e-3 / gg;
        for (int i = 0; i < n; i++) dir[i] *= gam;
        for (int j = mm - 1; j >= 0; j--) {
            int idx = (head - 1 - j + M) % M;
            double b = rho[idx] * dotn(n, Yv + (size_t)idx * n, dir);
            double *ss = S + (size_t)idx * n;
            for (int i = 0; i < n; i++) dir[i] += (alpha[idx] - b) * ss[i];
        }
        double gd = dotn(n, g, dir);
        if (gd >= 0) { // not a descent direction: reset to steepest descent
            for (int i = 0; i < n; i++) dir[i] = -g[i] * 1e-3 / gg;
            gd = dotn(n, g, dir); k = 0; head = 0;
        }
        double step = 1.0, fn = 0;
        int ok = 0;
        for (int ls = 0; ls < 30; ls++) {
            for (int i = 0; i < n; i++) xn[i] = x[i] + step * dir[i];
            fn = objf(N, d, xn, beta, gn, work);
            if (fn <= f + 1e-4 * step * gd) { ok = 1; break; }
            step *= 0.5;
        }
        if (!ok) break;
        // update memory
        double *ss = S + (size_t)head * n, *yy = Yv + (size_t)head * n;
        for (int i = 0; i < n; i++) { ss[i] = xn[i] - x[i]; yy[i] = gn[i] - g[i]; }
        double sy = dotn(n, ss, yy);
        memcpy(x, xn, sizeof(double) * n); memcpy(g, gn, sizeof(double) * n);
        double df = f - fn; f = fn;
        if (sy > 1e-300) { rho[head] = 1.0 / sy; head = (head + 1) % M; if (k < M) k++; }
        if (df < 1e-17 * (fabs(f) + 1e-30) && it > 5) break;
        // keep rows near unit norm (objective is scale invariant per row; renormalising keeps conditioning)
        if ((it & 63) == 63) {
            double *Y = work, *nr = work + (size_t)n;
            normrows(N, d, x, Y, nr); memcpy(x, Y, sizeof(double) * n);
            f = objf(N, d, x, beta, g, work); k = 0; head = 0;
        }
    }
    return it;
}

double lbfgs_polish(int N, int d, double *x, int nb, const double *betas, int maxiter, int M, double *work, double *lw) {
    int n = N * d;
    double *Y = work, *nr = work + (size_t)n;
    for (int b = 0; b < nb; b++) {
        normrows(N, d, x, Y, nr); memcpy(x, Y, sizeof(double) * n);
        lbfgs_stage(N, d, x, betas[b], maxiter, M, work, lw, 1e-14);
    }
    normrows(N, d, x, Y, nr); memcpy(x, Y, sizeof(double) * n);
    return cmax(N, d, x, work);
}

// penalty polish at target t (mode 1); returns final cmax. x updated in place.
double lbfgs_pen(int N, int d, double *x, double t, int maxiter, int M, double *work, double *lw) {
    int n = N * d;
    double *Y = work, *nr = work + (size_t)n;
    MODE = 1;
    normrows(N, d, x, Y, nr); memcpy(x, Y, sizeof(double) * n);
    lbfgs_stage(N, d, x, t, maxiter, M, work, lw, 1e-18);
    MODE = 0;
    normrows(N, d, x, Y, nr); memcpy(x, Y, sizeof(double) * n);
    return cmax(N, d, x, work);
}
