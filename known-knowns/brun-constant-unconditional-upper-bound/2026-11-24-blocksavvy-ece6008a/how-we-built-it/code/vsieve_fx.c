/* Rigorous V(z) = sum_{n<=z, n odd squarefree} prod_{p|n} 1/(p-2) in exact fixed point.
   Each term is replaced by floor(2^64 / P), P = prod (p-2) (exact u64), so S_lo = sum floor(...) is an exact integer with
   S_lo <= 2^64 V(z) < S_lo + count(z). Segmented sieve over odd n, primes <= sqrt(N).
   mode "chunks N STEP T out": T threads; writes for k=1..N/STEP the exact cumulative S_lo(k*STEP) (u128, 16 bytes LE)
                               and cumulative count (u64).
   mode "dense N out": writes for n=0..N a double d(n) <= S_lo(n)/2^64 <= V(n) (rounded down rigorously). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
typedef unsigned __int128 u128;
static uint32_t *pr; static long npr;
#define SEG (1L<<20)   /* odd numbers per segment */
static void segment(long lo, long cnt, u128 *term) { /* odd n = lo + 2j, j < cnt; lo odd; term[j] = floor(2^64/P) or 0 */
  static __thread uint64_t *acc, *prod; static __thread unsigned char *sf;
  if (!acc) { acc = malloc(8*SEG); prod = malloc(8*SEG); sf = malloc(SEG); }
  long hi = lo + 2*(cnt-1);
  for (long j = 0; j < cnt; j++) { acc[j] = 1; prod[j] = 1; sf[j] = 1; }
  for (long i = 0; i < npr; i++) {
    long p = pr[i]; if (p*p > hi) { if (p > hi) break; }
    long m = ((lo + p - 1)/p)*p; if (m % 2 == 0) m += p;           /* first odd multiple >= lo */
    for (long j = (m - lo)/2; j < cnt; j += p) { acc[j] *= p; prod[j] *= (p-2); }
    if (p*p <= hi) { long q = p*p; long m2 = ((lo + q - 1)/q)*q; if (m2 % 2 == 0) m2 += q;
      for (long j = (m2 - lo)/2; j < cnt; j += q) sf[j] = 0; }
  }
  for (long j = 0; j < cnt; j++) {
    long n = lo + 2*j;
    if (!sf[j] || n < 1) { term[j] = 0; continue; }
    if (acc[j] != (uint64_t)n) { uint64_t q = n / acc[j]; prod[j] *= (q - 2); }  /* one prime factor > sqrt(N) */
    term[j] = (((u128)1) << 64) / prod[j];
  }
}
typedef struct { long k0, k1, step; u128 *S; uint64_t *C; } job;
static void *work(void *a) { job *J = a; u128 *t = malloc(16*SEG);
  for (long k = J->k0; k < J->k1; k++) { /* chunk k covers n in ((k)*step, (k+1)*step] */
    long a0 = k*J->step + 1, b0 = (k+1)*J->step; long lo = (a0 % 2) ? a0 : a0 + 1; u128 s = 0; uint64_t c = 0;
    while (lo <= b0) { long cnt = (b0 - lo)/2 + 1; if (cnt > SEG) cnt = SEG; segment(lo, cnt, t);
      for (long j = 0; j < cnt; j++) if (t[j]) { s += t[j]; c++; } lo += 2*cnt; }
    J->S[k] = s; J->C[k] = c; }
  return 0; }
int main(int argc, char **argv) {
  long N = atol(argv[2]); long L = (long)sqrt((double)N) + 2; char *c = calloc(L+1, 1); pr = malloc(4*L); npr = 0;
  for (long i = 3; i <= L; i += 2) if (!c[i]) { pr[npr++] = i; for (long m = i*i; m <= L; m += 2*i) c[m] = 1; }
  if (!strcmp(argv[1], "chunks")) {
    long step = atol(argv[3]); int T = atoi(argv[4]); long K = N/step;
    u128 *S = malloc(16*K); uint64_t *C = malloc(8*K); pthread_t th[64]; job J[64];
    /* interleave work: thread t takes contiguous blocks; chunks cost about the same, so split evenly */
    for (int t = 0; t < T; t++) { J[t].k0 = K*t/T; J[t].k1 = K*(t+1)/T; J[t].step = step; J[t].S = S; J[t].C = C; pthread_create(&th[t], 0, work, &J[t]); }
    for (int t = 0; t < T; t++) pthread_join(th[t], 0);
    FILE *f = fopen(argv[5], "wb"); u128 s = 0; uint64_t cc = 0;
    for (long k = 0; k < K; k++) { s += S[k]; cc += C[k]; fwrite(&s, 16, 1, f); fwrite(&cc, 8, 1, f); }
    fclose(f);
    printf("N=%ld step=%ld S_lo(N)=%.17Lg count=%lu Vlo=%.15Lf Vhi=%.15Lf\n", N, step, (long double)s, (unsigned long)cc,
      (long double)s / 18446744073709551616.0L, ((long double)s + cc) / 18446744073709551616.0L);
  } else { /* dense */
    FILE *f = fopen(argv[3], "wb"); u128 *t = malloc(16*SEG); u128 s = 0; double d = 0; fwrite(&d, 8, 1, f);
    long n = 1; double *buf = malloc(8*2*SEG);
    while (n <= N) { long cnt = (N - n)/2 + 1; if (cnt > SEG) cnt = SEG; segment(n, cnt, t); long w = 0;
      for (long j = 0; j < cnt; j++) { long m = n + 2*j;
        for (int r = 0; r < 2 && m + r <= N; r++) { if (r == 0) s += t[j];
          uint64_t x = (uint64_t)(s >> 11); double v = (double)x; if ((u128)v > (u128)x) v = nextafter(v, 0); buf[w++] = ldexp(v, -53); } }
      fwrite(buf, 8, w, f); n += 2*cnt; }
    fclose(f); printf("dense N=%ld Vlo(N)=%.15f\n", N, (double)(s>>11)/9007199254740992.0);
  }
  return 0; }
