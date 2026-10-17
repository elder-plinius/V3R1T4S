// brute-scale lens: C inner loops for spherical-code objectives (all pairs; N up to a few thousand).
// Points x (N*d, row-major) are unnormalised; objectives are functions of y_i = x_i/|x_i|.
// Build: clang -O3 -march=native -shared -fPIC -o liblse.so lse.c
#include <math.h>
#include <stdlib.h>
#include <string.h>

// LogSumExp surrogate of max_{i<j} <y_i,y_j>; returns value, writes gradient wrt x into grad.
// work must hold N*d + N + N*(N-1)/2 doubles.
double lse_fg(int N, int d, const double *x, double beta, double *grad, double *work) {
    double *Y = work, *nrm = work + (size_t)N * d, *g = nrm + N;
    for (int i = 0; i < N; i++) {
        double s = 0;
        for (int k = 0; k < d; k++) s += x[i * d + k] * x[i * d + k];
        s = sqrt(s); nrm[i] = s;
        for (int k = 0; k < d; k++) Y[i * d + k] = x[i * d + k] / s;
    }
    double m = -3.0; size_t p = 0;
    for (int i = 0; i < N; i++) {
        const double *yi = Y + (size_t)i * d;
        for (int j = i + 1; j < N; j++) {
            const double *yj = Y + (size_t)j * d;
            double s = 0;
            for (int k = 0; k < d; k++) s += yi[k] * yj[k];
            g[p++] = s; if (s > m) m = s;
        }
    }
    double S = 0; p = 0;
    double cut = -40.0 / beta;
    memset(grad, 0, sizeof(double) * (size_t)N * d);
    for (int i = 0; i < N; i++) {
        for (int j = i + 1; j < N; j++) {
            double t = g[p] - m;
            if (t > cut) { double e = exp(beta * t); g[p] = e; S += e; } else g[p] = 0.0;
            p++;
        }
    }
    p = 0;
    double invS = 1.0 / S;
    for (int i = 0; i < N; i++) {
        double *gi = grad + (size_t)i * d; const double *yi = Y + (size_t)i * d;
        for (int j = i + 1; j < N; j++) {
            double w = g[p++];
            if (w == 0.0) continue;
            w *= invS;
            double *gj = grad + (size_t)j * d; const double *yj = Y + (size_t)j * d;
            for (int k = 0; k < d; k++) { gi[k] += w * yj[k]; gj[k] += w * yi[k]; }
        }
    }
    for (int i = 0; i < N; i++) {
        double *gi = grad + (size_t)i * d; const double *yi = Y + (size_t)i * d;
        double s = 0;
        for (int k = 0; k < d; k++) s += gi[k] * yi[k];
        for (int k = 0; k < d; k++) gi[k] = (gi[k] - s * yi[k]) / nrm[i];
    }
    return m + log(S) / beta;
}

// Overlap penalty at target t: sum_{i<j} max(0, <y_i,y_j> - t)^2 ; gradient into grad. work: N*d + N doubles.
double pen_fg(int N, int d, const double *x, double t, double *grad, double *work) {
    double *Y = work, *nrm = work + (size_t)N * d;
    for (int i = 0; i < N; i++) {
        double s = 0;
        for (int k = 0; k < d; k++) s += x[i * d + k] * x[i * d + k];
        s = sqrt(s); nrm[i] = s;
        for (int k = 0; k < d; k++) Y[i * d + k] = x[i * d + k] / s;
    }
    memset(grad, 0, sizeof(double) * (size_t)N * d);
    double E = 0;
    for (int i = 0; i < N; i++) {
        const double *yi = Y + (size_t)i * d; double *gi = grad + (size_t)i * d;
        for (int j = i + 1; j < N; j++) {
            const double *yj = Y + (size_t)j * d;
            double s = 0;
            for (int k = 0; k < d; k++) s += yi[k] * yj[k];
            double o = s - t;
            if (o > 0) {
                E += o * o;
                double w = 2 * o; double *gj = grad + (size_t)j * d;
                for (int k = 0; k < d; k++) { gi[k] += w * yj[k]; gj[k] += w * yi[k]; }
            }
        }
    }
    for (int i = 0; i < N; i++) {
        double *gi = grad + (size_t)i * d; const double *yi = Y + (size_t)i * d;
        double s = 0;
        for (int k = 0; k < d; k++) s += gi[k] * yi[k];
        for (int k = 0; k < d; k++) gi[k] = (gi[k] - s * yi[k]) / nrm[i];
    }
    return E;
}

// max pairwise cosine of normalised rows
double cmax(int N, int d, const double *x, double *work) {
    double *Y = work;
    for (int i = 0; i < N; i++) {
        double s = 0;
        for (int k = 0; k < d; k++) s += x[i * d + k] * x[i * d + k];
        s = sqrt(s);
        for (int k = 0; k < d; k++) Y[i * d + k] = x[i * d + k] / s;
    }
    double m = -3.0;
    for (int i = 0; i < N; i++) {
        const double *yi = Y + (size_t)i * d;
        for (int j = i + 1; j < N; j++) {
            const double *yj = Y + (size_t)j * d;
            double s = 0;
            for (int k = 0; k < d; k++) s += yi[k] * yj[k];
            if (s > m) m = s;
        }
    }
    return m;
}
