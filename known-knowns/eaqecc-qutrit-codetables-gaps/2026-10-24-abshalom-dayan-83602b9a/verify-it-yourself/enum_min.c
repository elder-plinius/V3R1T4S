/* Exhaustive minimum symplectic weight over span(S)^perp minus its isotropic part, over GF(3).
   Input (stdin, written by check_eaqecc.py prepare): "n dimI dim", then dim rows of 2n trits (0,1,2): a basis of
   span(S)^perp whose first dimI rows span the isotropic part span(S) ∩ span(S)^perp.
   A vector is isotropic iff all its coefficients on rows dimI..dim-1 are zero; those vectors are skipped.
   Every one of the 3^dim coefficient vectors is visited once by a ternary reflected Gray code (one row added or
   subtracted per step). Vectors are stored one-hot: bit i of x1 (x2) says x_i = 1 (x_i = 2); same for z.
   The top T = 2 coefficients are fixed per job (9 jobs); jobs j with j % nparts == part run in this process.
   Usage: enum_min part nparts < basis.txt      Output: "d=<min> count=<words of weight d> enumerated=<vectors>" */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef struct { uint32_t x1, x2, z1, z2; } V;
static inline V add(V a, V b) {
  V r; uint32_t a0 = ~(a.x1 | a.x2), b0 = ~(b.x1 | b.x2);
  r.x1 = (a0 & b.x1) | (a.x1 & b0) | (a.x2 & b.x2);
  r.x2 = (a0 & b.x2) | (a.x2 & b0) | (a.x1 & b.x1);
  a0 = ~(a.z1 | a.z2); b0 = ~(b.z1 | b.z2);
  r.z1 = (a0 & b.z1) | (a.z1 & b0) | (a.z2 & b.z2);
  r.z2 = (a0 & b.z2) | (a.z2 & b0) | (a.z1 & b.z1);
  return r;
}
static inline V neg(V a) { V r = { a.x2, a.x1, a.z2, a.z1 }; return r; }
static inline int wt(V a) { return __builtin_popcount(a.x1 | a.x2 | a.z1 | a.z2); }
int main(int argc, char **argv) {
  int part = argc > 2 ? atoi(argv[1]) : 0, nparts = argc > 2 ? atoi(argv[2]) : 1;
  int n, dimI, dim;
  if (scanf("%d %d %d", &n, &dimI, &dim) != 3 || n > 32 || dim > 40 || dim < 3) { printf("bad input\n"); return 2; }
  V B[40], NB[40];
  for (int r = 0; r < dim; r++) {
    V v = {0, 0, 0, 0};
    for (int t = 0; t < 2 * n; t++) {
      int e; if (scanf("%d", &e) != 1 || e < 0 || e > 2) { printf("bad input\n"); return 2; }
      uint32_t bit = 1u << (t % n);
      if (t < n) { if (e == 1) v.x1 |= bit; if (e == 2) v.x2 |= bit; }
      else       { if (e == 1) v.z1 |= bit; if (e == 2) v.z2 |= bit; }
    }
    B[r] = v; NB[r] = neg(v);
  }
  const int T = 2; int m = dim - T;               /* free digits 0..m-1, fixed digits m..dim-1 (logical) */
  if (m < dimI) { printf("bad split\n"); return 2; }
  int best = 1 << 30; long long cnt = 0, total = 0;
  for (int job = 0; job < 9; job++) {
    if (job % nparts != part) continue;
    int fx[2] = { job % 3, job / 3 };
    V v = {0, 0, 0, 0}; int nzlog = 0;
    for (int f = 0; f < T; f++) {
      for (int a = 0; a < fx[f]; a++) v = add(v, B[m + f]);
      if (fx[f]) nzlog++;
    }
    int g[40] = {0}, dir[40];
    for (int i = 0; i < m; i++) dir[i] = 1;
    for (;;) {
      total++;
      if (nzlog) { int w = wt(v); if (w < best) { best = w; cnt = 1; } else if (w == best) cnt++; }
      int i = 0;
      while (i < m && (g[i] + dir[i] < 0 || g[i] + dir[i] > 2)) { dir[i] = -dir[i]; i++; }
      if (i == m) break;
      int old = g[i]; g[i] += dir[i];
      v = add(v, dir[i] > 0 ? B[i] : NB[i]);
      if (i >= dimI) { if (old == 0 && g[i] != 0) nzlog++; else if (old != 0 && g[i] == 0) nzlog--; }
    }
  }
  printf("d=%d count=%lld enumerated=%lld\n", best, cnt, total);
  return 0;
}
