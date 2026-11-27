/* Per-modulus combination of Selberg weights (Klyve (5.16): error = sum_{d1,d2} lambda_d1 lambda_d2 R_[d1,d2]
   = sum_q rho_q R_q, rho_q = sum_{[d1,d2]=q} lambda_d1 lambda_d2, so |error| <= (sum_q |rho_q|) max_q |R_q|).
   For integer n = floor(z): lambda_d = mu(d) prod_{p|d} (p-1)/(p-2) * G_d(n/d) / V(n), G_d(y) = sum_{t<=y, t odd sqfree, (t,d)=1} prod 1/(p-2)
   (Klyve (5.24)-(5.26)). Long double arithmetic; prints n, Lambda=sum|lambda|, R=sum_q|rho_q|, and Rup = R*(1+1e-10) + 1e-12*Lambda^2,
   a rigorous upper bound given the rounding analysis in ../NOTES.md (all relative errors < 1e-14 for n <= 2e4).
   Usage: rho n1 n2 ...   (n <= 20000) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }
int main(int argc, char **argv) {
  for (int ai = 1; ai < argc; ai++) {
    long n = atol(argv[ai]); if (n > 20000 || n < 1) { fprintf(stderr, "n out of range\n"); return 2; }
    int *spf = calloc(n + 1, sizeof(int));
    for (long i = 2; i <= n; i++) if (!spf[i]) for (long m = i; m <= n; m += i) if (!spf[m]) spf[m] = i;
    long double *h = calloc(n + 1, sizeof(long double)), *k = calloc(n + 1, sizeof(long double)); char *ok = calloc(n + 1, 1);
    long *ds = malloc(sizeof(long) * (n + 1)); long nd = 0; int *mu = calloc(n + 1, sizeof(int));
    for (long d = 1; d <= n; d += 2) {
      long m = d; long double hh = 1, kk = 1; int good = 1, s = 1;
      while (m > 1) { long p = spf[m]; m /= p; if (m % p == 0) { good = 0; break; } hh /= (p - 2); kk *= (long double)(p - 1) / (p - 2); s = -s; }
      if (good) { ok[d] = 1; h[d] = hh; k[d] = kk; mu[d] = s; ds[nd++] = d; }
    }
    long double V = 0; for (long i = 0; i < nd; i++) V += h[ds[i]];
    long double *lam = calloc(n + 1, sizeof(long double)); long double L = 0;
    for (long i = 0; i < nd; i++) { long d = ds[i]; long double G = 0; long y = n / d;
      for (long t = 1; t <= y; t += 2) if (ok[t] && gcdl(t, d) == 1) G += h[t];
      lam[d] = mu[d] * k[d] * G / V; L += fabsl(lam[d]); }
    long Q = n * n; long double *rho = calloc(Q / 2 + 1, sizeof(long double));
    if (!rho) { fprintf(stderr, "alloc\n"); return 3; }
    for (long i = 0; i < nd; i++) { long a = ds[i]; long double la = lam[a];
      for (long j = 0; j < nd; j++) { long b = ds[j]; long q = a / gcdl(a, b) * b; rho[q / 2] += la * lam[b]; } }
    long double R = 0; for (long i = 0; i <= Q / 2; i++) R += fabsl(rho[i]);
    long double Rup = R * (1 + 1e-10L) + 1e-12L * L * L;
    printf("%ld %.18Lg %.18Lg %.18Lg %.18Lg\n", n, L, L * L, R, Rup); fflush(stdout);
    free(spf); free(h); free(k); free(ok); free(ds); free(mu); free(lam); free(rho);
  }
  return 0;
}
