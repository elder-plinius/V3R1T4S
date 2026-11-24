/* Rigorous UPPER bound for W(z) = sum_{n<=z, n odd squarefree} prod_{p|n} p/(p-2) = sum n/P(n), P(n)=prod (p-2), in exact
   fixed point. Each term is replaced by ceil(2^40 n / P) (exact u128 integer division), so S_hi = sum ceil(...) satisfies
   2^40 W(z) <= S_hi(z). Adapted from runs/2026-11-23-1618/claim_v2/code/vsieve_fx.c (same segmented sieve).
   mode "chunks N STEP T out": cumulative S_hi(k*STEP), k=1..N/STEP, u128 LE (16 bytes) each.
   mode "dense N out": for n=0..N a double w(n) >= S_hi(n)/2^40 >= W(n) (rounded up: two nextafter steps toward +inf). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
typedef unsigned __int128 u128;
static uint32_t *pr; static long npr;
#define SEG (1L<<20)
static void segment(long lo, long cnt, u128 *term) {
  static __thread uint64_t *acc, *prod; static __thread unsigned char *sf;
  if (!acc) { acc = malloc(8*SEG); prod = malloc(8*SEG); sf = malloc(SEG); }
  long hi = lo + 2*(cnt-1);
  for (long j = 0; j < cnt; j++) { acc[j] = 1; prod[j] = 1; sf[j] = 1; }
  for (long i = 0; i < npr; i++) {
    long p = pr[i]; if (p > hi) break;
    long m = ((lo + p - 1)/p)*p; if (m % 2 == 0) m += p;
    for (long j = (m - lo)/2; j < cnt; j += p) { acc[j] *= p; prod[j] *= (p-2); }
    if (p*p <= hi) { long q = p*p; long m2 = ((lo + q - 1)/q)*q; if (m2 % 2 == 0) m2 += q;
      for (long j = (m2 - lo)/2; j < cnt; j += q) sf[j] = 0; }
  }
  for (long j = 0; j < cnt; j++) {
    long n = lo + 2*j;
    if (!sf[j] || n < 1) { term[j] = 0; continue; }
    if (acc[j] != (uint64_t)n) { uint64_t q = n / acc[j]; prod[j] *= (q - 2); }
    u128 num = ((u128)n) << 40; term[j] = num / prod[j] + ((num % prod[j]) ? 1 : 0);
  }
}
typedef struct { long k0, k1, step; u128 *S; } job;
static void *work(void *a) { job *J = a; u128 *t = malloc(16*SEG);
  for (long k = J->k0; k < J->k1; k++) {
    long a0 = k*J->step + 1, b0 = (k+1)*J->step; long lo = (a0 % 2) ? a0 : a0 + 1; u128 s = 0;
    while (lo <= b0) { long cnt = (b0 - lo)/2 + 1; if (cnt > SEG) cnt = SEG; segment(lo, cnt, t);
      for (long j = 0; j < cnt; j++) s += t[j]; lo += 2*cnt; }
    J->S[k] = s; }
  return 0; }
int main(int argc, char **argv) {
  long N = atol(argv[2]); long L = (long)sqrt((double)N) + 2; char *c = calloc(L+1, 1); pr = malloc(4*L); npr = 0;
  for (long i = 3; i <= L; i += 2) if (!c[i]) { pr[npr++] = i; for (long m = i*i; m <= L; m += 2*i) c[m] = 1; }
  if (!strcmp(argv[1], "chunks")) {
    long step = atol(argv[3]); int T = atoi(argv[4]); long K = N/step;
    u128 *S = malloc(16*K); pthread_t th[64]; job J[64];
    for (int t = 0; t < T; t++) { J[t].k0 = K*t/T; J[t].k1 = K*(t+1)/T; J[t].step = step; J[t].S = S; pthread_create(&th[t], 0, work, &J[t]); }
    for (int t = 0; t < T; t++) pthread_join(th[t], 0);
    FILE *f = fopen(argv[5], "wb"); u128 s = 0;
    for (long k = 0; k < K; k++) { s += S[k]; fwrite(&s, 16, 1, f); }
    fclose(f);
    printf("N=%ld step=%ld S_hi(N)=%.20Lg Whi=%.15Lf\n", N, step, (long double)s, (long double)s / 1099511627776.0L);
  } else {
    FILE *f = fopen(argv[3], "wb"); u128 *t = malloc(16*SEG); u128 s = 0; double d = 0; fwrite(&d, 8, 1, f);
    long n = 1; double *buf = malloc(8*2*SEG);
    while (n <= N) { long cnt = (N - n)/2 + 1; if (cnt > SEG) cnt = SEG; segment(n, cnt, t); long w = 0;
      for (long j = 0; j < cnt; j++) { long m = n + 2*j;
        for (int r = 0; r < 2 && m + r <= N; r++) { if (r == 0) s += t[j];
          double v = (double)((long double)s / 1099511627776.0L); v = nextafter(nextafter(v, INFINITY), INFINITY); buf[w++] = v; } }
      fwrite(buf, 8, w, f); n += 2*cnt; }
    fclose(f); printf("dense N=%ld Whi(N)=%.15f\n", N, (double)((long double)s / 1099511627776.0L));
  }
  return 0; }
