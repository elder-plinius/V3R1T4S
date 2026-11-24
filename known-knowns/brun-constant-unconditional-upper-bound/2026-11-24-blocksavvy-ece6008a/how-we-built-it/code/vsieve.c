/* V(z) = sum_{n <= z, n odd squarefree} prod_{p | n} 1/(p-2)  (n = 1 contributes 1),  M(z) = #{n <= z odd squarefree}.
   Writes prefix arrays: V as double for 0..N, M as int32 for 0..NM. Non-rigorous double arithmetic (smoke test only). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc, char **argv) {
  long N = atol(argv[1]), NM = atol(argv[2]);
  double *g = malloc(sizeof(double) * (N + 1)); unsigned char *sf = malloc(N + 1); unsigned char *comp = calloc(N + 1, 1);
  for (long i = 0; i <= N; i++) { g[i] = 1.0; sf[i] = (i % 2 == 1); }
  for (long p = 3; p <= N; p += 2) {
    if (comp[p]) continue;
    for (long m = p * p; m <= N; m += p) comp[m] = 1;
    double inv = 1.0 / (double)(p - 2);
    for (long m = p; m <= N; m += p) g[m] *= inv;
    if (p <= N / p) for (long m = p * p; m <= N; m += p * p) sf[m] = 0;
  }
  FILE *fv = fopen(argv[3], "wb"), *fm = fopen(argv[4], "wb");
  double V = 0; int32_t M = 0;
  for (long n = 0; n <= N; n++) {
    if (n >= 1 && sf[n]) { V += g[n]; if (n <= NM) M++; }
    fwrite(&V, sizeof(double), 1, fv);
    if (n <= NM) fwrite(&M, sizeof(int32_t), 1, fm);
  }
  fclose(fv); fclose(fm);
  printf("N=%ld V(N)=%.15f M(NM=%ld)=%d\n", N, V, NM, M);
  return 0;
}
