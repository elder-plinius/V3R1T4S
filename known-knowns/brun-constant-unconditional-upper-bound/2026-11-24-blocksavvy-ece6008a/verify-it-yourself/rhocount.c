/* Checker's own exact accumulator (independent of the author's rhofx.c: sort-based, not segment-based).
   stdin: "n N" then N lines "d L" (d odd squarefree <= n <= 20000, |L| < 2^50). For every unordered pair i <= j it forms the
   key (lcm(d_i,d_j) << 28) | (i << 14) | j, sorts the keys, and sums w = L_i L_j (times 2 if i < j) over each run of equal lcm,
   exactly in __int128. Prints "n N sumL sumAbsL S Pcheck" with S = sum_q |P_q| and Pcheck = 1 iff sum_q P_q == (sum L)^2. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef __int128 i128;
static void pr(i128 v) { char b[64]; int k = 63; b[k] = 0; int neg = v < 0; unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
  if (!u) b[--k] = '0'; while (u) { b[--k] = '0' + (int)(u % 10); u /= 10; } if (neg) b[--k] = '-'; fputs(b + k, stdout); }
static int cmpu(const void *x, const void *y) { uint64_t a = *(const uint64_t *)x, b = *(const uint64_t *)y; return a < b ? -1 : a > b; }
static uint64_t g(uint64_t a, uint64_t b) { while (b) { uint64_t t = a % b; a = b; b = t; } return a; }
int main(void) {
  long n, N; if (scanf("%ld %ld", &n, &N) != 2 || n < 1 || n > 20000 || N < 1 || N >= 16384) return 2;
  uint64_t *d = malloc(8 * N); long long *L = malloc(8 * N);
  for (long i = 0; i < N; i++) if (scanf("%lu %lld", &d[i], &L[i]) != 2 || d[i] > (uint64_t)n || !(d[i] & 1) || L[i] > (1LL << 50) || L[i] < -(1LL << 50)) return 2;
  uint64_t np = (uint64_t)N * (N + 1) / 2; uint64_t *K = malloc(8 * np); if (!K) return 3;
  uint64_t k = 0;
  for (uint64_t i = 0; i < (uint64_t)N; i++) for (uint64_t j = i; j < (uint64_t)N; j++) K[k++] = ((d[i] / g(d[i], d[j]) * d[j]) << 28) | (i << 14) | j;
  qsort(K, np, 8, cmpu);
  i128 S = 0, tot = 0, run = 0, sL = 0, sAL = 0; uint64_t cur = K[0] >> 28;
  for (uint64_t t = 0; t < np; t++) {
    uint64_t q = K[t] >> 28, i = (K[t] >> 14) & 16383, j = K[t] & 16383;
    if (q != cur) { S += run < 0 ? -run : run; tot += run; run = 0; cur = q; }
    i128 w = (i128)L[i] * L[j]; run += (i == j) ? w : 2 * w;
  }
  S += run < 0 ? -run : run; tot += run;
  for (long i = 0; i < N; i++) { sL += L[i]; sAL += L[i] < 0 ? -(i128)L[i] : L[i]; }
  printf("%ld %ld ", n, N); pr(sL); putchar(' '); pr(sAL); putchar(' '); pr(S); printf(" %d\n", tot == sL * sL);
  return 0;
}
