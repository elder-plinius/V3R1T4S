/* Hard-sphere Monte Carlo compression of N balls in the unit 4-ball.
   Each sweep: one trial move per ball (accepted if no overlap at current r);
   then r grows by a fraction of the gap to the current feasible radius. */
#include <math.h>
#include <stdint.h>
#define D 4
static uint64_t s_[2];
static inline uint64_t xs(void) { uint64_t a = s_[0], b = s_[1]; s_[0] = b; a ^= a << 23;
    s_[1] = a ^ b ^ (a >> 17) ^ (b >> 26); return s_[1] + b; }
static inline double ur(void) { return (xs() >> 11) * (1.0 / 9007199254740992.0); }

static double feas(const double *x, int n) {
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

/* x must be feasible for radius *r (r <= feas). Returns final acceptance rate. */
double mc(double *x, int n, double *r, int nsweeps, double growth, double step0, uint64_t seed) {
    s_[0] = seed * 0x9E3779B97F4A7C15ULL + 1; s_[1] = seed ^ 0xD1B54A32D192ED03ULL; xs(); xs();
    double R = *r, step = step0 * R; long acc = 0, tri = 0; double rate = 0;
    for (int sw = 0; sw < nsweeps; sw++) {
        for (int t = 0; t < n; t++) {
            int i = xs() % n; double y[D], s = 0;
            for (int a = 0; a < D; a++) { y[a] = x[i*D+a] + step * (2 * ur() - 1); s += y[a]*y[a]; }
            tri++;
            if (sqrt(s) > 1 - R) continue;
            double lim = 4 * R * R; int ok = 1;
            for (int j = 0; j < n && ok; j++) { if (j == i) continue; double q = 0;
                for (int a = 0; a < D; a++) { double d = y[a] - x[j*D+a]; q += d*d; }
                if (q < lim) ok = 0; }
            if (ok) { for (int a = 0; a < D; a++) x[i*D+a] = y[a]; acc++; }
        }
        if ((sw & 15) == 15) {
            rate = (double)acc / tri; acc = tri = 0;
            if (rate < 0.25) step *= 0.8; else if (rate > 0.4) step *= 1.2;
            double f = feas(x, n); R += growth * (f - R);
        }
    }
    *r = R; return rate;
}
