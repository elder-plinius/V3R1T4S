/* [2026-11-24: copy of claim_v2/verify/vcount.c, adds W] For each n prints  n S(n) M(n) SW(n),  SW(n) = sum ceil(2^40 m / prod_{p|m}(p-2)) >= 2^40 W(n).
   Standalone checker part 1 (written from the definition, separate from the contributor's sieve).
   For each requested n (sorted, one per line on stdin) prints  n S(n) M(n)  where
     M(n) = #{ m <= n : m odd, squarefree }                       (exact)
     S(n) = sum_{m <= n, m odd squarefree} floor(2^64 / prod_{p | m} (p - 2))   (exact integer, printed in decimal)
   so that S(n)/2^64 <= V(n) = sum_{m <= n, m odd squarefree} prod_{p|m} 1/(p-2) < (S(n) + M(n))/2^64.
   Method: segmented sieve over odd m with a running cofactor (divide out each prime p <= sqrt(N) found; a second division
   by p marks m non-squarefree; a cofactor > 1 left at the end is one prime > sqrt(N)). Usage: vcount N THREADS < points */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
typedef unsigned __int128 u128;
static long *P; static long nP, N, T, *pts, npts;
static u128 *pS, *pW; static uint64_t *pC;          /* per point, partial sums inside the owning thread's range */
static u128 *tS, *tW; static uint64_t *tC;          /* per thread totals */
#define B 65536
typedef struct { int id; long lo, hi; } job;  /* odd m in [lo, hi] */
static void *run(void *a) {
  job *J = a; uint64_t *rem = malloc(8*B), *pr = malloc(8*B); unsigned char *ok = malloc(B);
  u128 s = 0, w = 0; uint64_t c = 0; long k = 0; while (k < npts && pts[k] < J->lo) k++;
  for (long base = J->lo; base <= J->hi; base += 2*B) {
    long cnt = (J->hi - base)/2 + 1; if (cnt > B) cnt = B; long top = base + 2*(cnt-1);
    for (long j = 0; j < cnt; j++) { rem[j] = base + 2*j; pr[j] = 1; ok[j] = 1; }
    for (long i = 0; i < nP && P[i]*P[i] <= top; i++) {
      long p = P[i], m0 = ((base + p - 1)/p)*p; if (!(m0 & 1)) m0 += p;
      for (long j = (m0 - base)/2; j < cnt; j += p) { rem[j] /= p; pr[j] *= (uint64_t)(p - 2); if (rem[j] % p == 0) ok[j] = 0; }
    }
    for (long j = 0; j < cnt; j++) {
      long m = base + 2*j;
      while (k < npts && pts[k] < m) { pS[k] = s; pW[k] = w; pC[k] = c; k++; }
      if (ok[j]) { uint64_t q = rem[j]; uint64_t d = pr[j] * (q > 1 ? q - 2 : 1); s += (((u128)1) << 64) / d; c++; u128 num = ((u128)m) << 40; w += num / d + ((num % d) ? 1 : 0); }
      while (k < npts && pts[k] == m) { pS[k] = s; pW[k] = w; pC[k] = c; k++; }
    }
  }
  while (k < npts && pts[k] <= J->hi + 1) { pS[k] = s; pW[k] = w; pC[k] = c; k++; }
  tS[J->id] = s; tW[J->id] = w; tC[J->id] = c; return 0;
}
static void pr128(u128 x) { char b[64]; int i = 63; b[i] = 0; if (!x) b[--i] = '0'; while (x) { b[--i] = '0' + (int)(x % 10); x /= 10; } fputs(b + i, stdout); }
int main(int argc, char **argv) {
  N = atol(argv[1]); T = atol(argv[2]); long cap = 1 << 16; pts = malloc(8*cap); npts = 0; long v;
  while (scanf("%ld", &v) == 1) { if (npts == cap) { cap *= 2; pts = realloc(pts, 8*cap); } pts[npts++] = v; }
  for (long i = 1; i < npts; i++) if (pts[i] < pts[i-1] || pts[i] > N) { fprintf(stderr, "points must be sorted and <= N\n"); return 2; }
  long L = 2; while (L*L <= N) L++; char *c = calloc(L+1, 1); P = malloc(8*L); nP = 0;
  for (long i = 3; i <= L; i += 2) if (!c[i]) { P[nP++] = i; for (long m = i*i; m <= L; m += 2*i) c[m] = 1; }
  pS = calloc(npts, 16); pW = calloc(npts, 16); tW = calloc(T, 16); pC = calloc(npts, 8); tS = calloc(T, 16); tC = calloc(T, 8);
  pthread_t th[64]; job J[64]; long odd = (N + 1)/2;               /* odd m = 1, 3, ..., <= N */
  for (int t = 0; t < T; t++) { long a = odd*t/T, b = odd*(t+1)/T; J[t].id = t; J[t].lo = 2*a + 1; J[t].hi = 2*b - 1; }
  for (int t = 0; t < T; t++) pthread_create(&th[t], 0, run, &J[t]);
  for (int t = 0; t < T; t++) pthread_join(th[t], 0);
  for (long k = 0; k < npts; k++) {                               /* add totals of all earlier threads */
    u128 s, ww; uint64_t cc;
    /* owning thread = first t with pts[k] <= J[t].hi + 1 */
    int own = 0; while (own < T-1 && pts[k] > J[own].hi + 1) own++;
    s = pS[k]; ww = pW[k]; cc = pC[k]; for (int t = 0; t < own; t++) { s += tS[t]; ww += tW[t]; cc += tC[t]; }
    printf("%ld ", pts[k]); pr128(s); printf(" %lu ", (unsigned long)cc); pr128(ww); printf("\n");
  }
  return 0;
}
