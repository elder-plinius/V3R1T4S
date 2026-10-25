// SPDX-License-Identifier: AGPL-3.0-or-later
// vf2: third implementation (C, uint64 words, sign symmetry) for: is there an irreducible zero-sum set of exactly L
// distinct odd integers with largest |x| exactly M?  Largest magnitude forced positive (negating a set keeps it valid).
// P/Q = subset sums of positives / |negatives| as bitsets of NW words; P∩Q = {0} required before completion.
// Bits above 64*NW are dropped: only weakens pruning (fewer detected intersections), never removes a solution,
// provided the final sum S < 64*NW (checked at startup).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#ifndef NW
#define NW 16
#endif
static int L, M; static long long nodes;
typedef struct { uint64_t w[NW]; } bs;
static void shl_or(bs *r, const bs *a, int s) { int q = s >> 6, b = s & 63;
  for (int i = NW - 1; i >= 0; i--) { uint64_t v = 0;
    if (i - q >= 0) { v = a->w[i - q] << b; if (b && i - q - 1 >= 0) v |= a->w[i - q - 1] >> (64 - b); }
    r->w[i] = a->w[i] | v; } }
static int meet(const bs *a, const bs *b, int allow) { // returns 1 if a∩b has a bit other than 0 and allow
  for (int i = 0; i < NW; i++) { uint64_t x = a->w[i] & b->w[i];
    if (i == 0) x &= ~1ULL;
    if (allow >= 0 && (allow >> 6) == i) x &= ~(1ULL << (allow & 63));
    if (x) return 1; }
  return 0; }
static int go(int m, const bs *P, const bs *Q, int sp, int sn, int cnt) {
  nodes++;
  if (cnt == L) return sp == sn && !meet(P, Q, sp);
  int left = L - cnt; if (m <= 0 || (m + 1) / 2 < left) return 0;
  int gap = abs(sp - sn), best = left * (m - left + 1);       // m + (m-2) + ... (left terms)
  if (gap > best) return 0;
  bs T;
  shl_or(&T, P, m);
  if (cnt + 1 == L ? (sp + m == sn && !meet(&T, Q, sn)) : !meet(&T, Q, -1))
    if (go(m - 2, &T, Q, sp + m, sn, cnt + 1)) return 1;
  shl_or(&T, Q, m);
  if (cnt + 1 == L ? (sn + m == sp && !meet(P, &T, sp)) : !meet(P, &T, -1))
    if (go(m - 2, P, &T, sp, sn + m, cnt + 1)) return 1;
  return go(m - 2, P, Q, sp, sn, cnt);
}
int main(int argc, char **argv) {
  M = atoi(argv[1]); L = atoi(argv[2]);
  int tot = 0; for (int i = 0; i < L; i++) tot += M - 2 * i;
  if (tot / 2 >= 64 * NW) { fprintf(stderr, "NW too small\n"); return 2; }
  bs P = {{0}}, Q = {{0}}; P.w[0] = 1; Q.w[0] = 1; bs P1; shl_or(&P1, &P, M);
  int r = go(M - 2, &P1, &Q, M, 0, 1);
  printf("M=%d L=%d %s nodes=%lld\n", M, L, r ? "FOUND" : "NONE", nodes);
  return 0; }
