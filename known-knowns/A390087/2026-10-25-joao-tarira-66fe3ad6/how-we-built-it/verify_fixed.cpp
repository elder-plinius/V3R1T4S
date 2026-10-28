// SPDX-License-Identifier: AGPL-3.0-or-later
// Independent re-implementation (C++/std::bitset) for the non-existence part.
// Question: is there an irreducible zero-sum set of exactly L distinct odd integers whose largest |x| is exactly M?
// Elements are decided from the largest magnitude down; each magnitude is +, -, or absent (no sign symmetry breaking).
// Invariant: P = subset sums of positives, Q = subset sums of |negatives|, P∩Q = {0} until the set is complete;
// complete set requires sum(+) == sum(-) and P∩Q == {0, S}.
#include <bitset>
#include <cstdio>
#include <cstdlib>
typedef std::bitset<1600> B;
static int L, M; static long long nodes;
static bool go(int m, const B& P, const B& Q, int sp, int sn, int cnt) {
  ++nodes;
  if (cnt == L) {
    if (sp != sn) return false;
    B I = P & Q; I.reset(0); I.reset(sp); return I.none();
  }
  if (m <= 0) return false;
  int left = L - cnt, avail = (m + 1) / 2;
  if (avail < left) return false;
  int gap = sp > sn ? sp - sn : sn - sp, best = 0;
  for (int i = 0; i < left; ++i) best += m - 2 * i;           // largest possible total of the remaining elements
  if (gap > best) return false;
  B P2 = P | (P << m);                                        // m as positive
  { B I = P2 & Q; I.reset(0);
    bool okI = I.none() || (cnt + 1 == L && I.count() == 1 && I.test(sp + m) && sp + m == sn);
    if (okI && go(m - 2, P2, Q, sp + m, sn, cnt + 1)) return true; }
  B Q2 = Q | (Q << m);                                        // m as negative
  { B I = P & Q2; I.reset(0);
    bool okI = I.none() || (cnt + 1 == L && I.count() == 1 && I.test(sn + m) && sn + m == sp);
    if (okI && go(m - 2, P, Q2, sp, sn + m, cnt + 1)) return true; }
  return go(m - 2, P, Q, sp, sn, cnt);                        // m absent
}
int main(int argc, char** argv) {
  M = atoi(argv[1]); L = atoi(argv[2]);
  B z; z.set(0);
  // largest magnitude M must be present, with either sign
  bool r = go(M - 2, z | (z << M), z, M, 0, 1) || go(M - 2, z, z | (z << M), 0, M, 1);
  printf("M=%d L=%d %s nodes=%lld\n", M, L, r ? "FOUND" : "NONE", nodes);
  return 0;
}
