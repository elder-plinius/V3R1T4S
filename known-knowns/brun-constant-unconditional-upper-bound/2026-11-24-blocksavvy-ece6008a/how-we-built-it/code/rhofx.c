/* Exact integer per-modulus combination of rounded Selberg weights.
   stdin: "n N" then N lines "d L_d" (d odd squarefree <= n, L_d integer with |L_d| < 2^62).
   Computes P_q = sum over ORDERED pairs (a,b) with lcm(a,b) = q of L_a L_b, exactly in signed 128-bit integers,
   and prints:  n N sumL sumAbsL S  where S = sum_q |P_q|  (decimal, exact), after checking sum_q P_q == (sum L)^2 exactly.
   Memory: one uint32 lcm per unordered pair, then q is processed in segments of SEG odd values (16 bytes each).
   Exit 4 if the identity check fails, 3 on allocation failure, 2 on bad input. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef __int128 i128;
static void pr(i128 v) { char b[64]; int k = 63; b[k] = 0; int neg = v < 0; unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
  if (!u) b[--k] = '0'; while (u) { b[--k] = '0' + (int)(u % 10); u /= 10; } if (neg) b[--k] = '-'; fputs(b + k, stdout); }
static uint64_t gcdu(uint64_t a, uint64_t b) { while (b) { uint64_t t = a % b; a = b; b = t; } return a; }
int main(void) {
  long n, N; if (scanf("%ld %ld", &n, &N) != 2 || n < 1 || n > 65535 || N < 1) return 2;
  long *d = malloc(sizeof(long) * N); long long *L = malloc(sizeof(long long) * N); if (!d || !L) return 3;
  for (long i = 0; i < N; i++) { if (scanf("%ld %lld", &d[i], &L[i]) != 2) return 2; if (d[i] < 1 || d[i] > n || d[i] % 2 == 0) return 2;
    if (L[i] > (1LL << 62) || L[i] < -(1LL << 62)) return 2; }
  long np = N * (N + 1) / 2; uint32_t *Q = malloc(sizeof(uint32_t) * np); if (!Q) return 3;
  long k = 0; for (long i = 0; i < N; i++) for (long j = i; j < N; j++) { uint64_t g = gcdu(d[i], d[j]); Q[k++] = (uint32_t)((uint64_t)d[i] / g * (uint64_t)d[j]); }
  uint64_t qmax = (uint64_t)n * (uint64_t)n; long nidx = (long)((qmax - 1) / 2) + 1;
  const long SEG = 1L << 23; i128 *acc = malloc(sizeof(i128) * SEG); if (!acc) return 3;
  i128 sumP = 0, S = 0, sumL = 0, sumAbsL = 0;
  for (long i = 0; i < N; i++) { sumL += L[i]; sumAbsL += L[i] < 0 ? -(i128)L[i] : (i128)L[i]; }
  for (long lo = 0; lo < nidx; lo += SEG) {
    long hi = lo + SEG < nidx ? lo + SEG : nidx; memset(acc, 0, sizeof(i128) * (hi - lo));
    k = 0;
    for (long i = 0; i < N; i++) { i128 li = L[i];
      long t = ((long)Q[k] - 1) / 2; if (t >= lo && t < hi) acc[t - lo] += li * li; k++;   /* j = i */
      for (long j = i + 1; j < N; j++, k++) { long t2 = ((long)Q[k] - 1) / 2; if (t2 >= lo && t2 < hi) acc[t2 - lo] += 2 * li * (i128)L[j]; } }
    for (long t = 0; t < hi - lo; t++) { sumP += acc[t]; S += acc[t] < 0 ? -acc[t] : acc[t]; }
  }
  if (sumP != sumL * sumL) { fprintf(stderr, "identity sum_q P_q == (sum L)^2 FAILED\n"); return 4; }
  printf("%ld %ld ", n, N); pr(sumL); putchar(' '); pr(sumAbsL); putchar(' '); pr(S); putchar('\n');
  return 0;
}
