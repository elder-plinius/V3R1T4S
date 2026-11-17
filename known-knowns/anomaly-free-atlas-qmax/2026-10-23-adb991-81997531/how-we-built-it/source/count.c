/* Count bounded integer solutions of the six ACCs (BRIEF.md), meet in the middle.
   N(Q) = number of 5- or 6-tuples of sorted species triples (x<=y<=z, |x|<=Q) satisfying all ACCs (zero included).
   Linear ACCs (sums a_X over each species):
     a_d = -2 a_Q - a_u,  a_L = -3 a_Q,  a_e = 2 a_Q - a_u,  a_nu = 4 a_Q + a_u   (SM: a_nu must be 0)
   quadratic: b_Q - 2 b_u + b_d - b_L + b_e = 0;  cubic: 6c_Q + 3c_u + 3c_d + 2c_L + c_e + c_nu = 0.
   For each (a_Q, a_u): side A = (Q,u,d) keys (b_Q-2b_u+b_d, 6c_Q+3c_u+3c_d); side B = (L,e,nu) keys
   (-b_L+b_e, 2c_L+c_e+c_nu); count pairs with keyA + keyB = 0 by sort-merge.
   Usage: count QMAX NU   -> prints "N Q NU value" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
typedef struct { ll b, c; } key;
static int cmpk(const void *p, const void *q) {
  const key *x = p, *y = q;
  if (x->b != y->b) return x->b < y->b ? -1 : 1;
  if (x->c != y->c) return x->c < y->c ? -1 : 1;
  return 0;
}
int Q;
/* triples grouped by sum: for sum s in [-3Q,3Q], arrays of (b,c) */
int *cnt; ll **tb, **tc;
#define IDX(s) ((s) + 3*Q)
int main(int argc, char **argv) {
  Q = atoi(argv[1]); int nu = atoi(argv[2]);
  int S = 6*Q + 1;
  cnt = calloc(S, sizeof(int)); tb = calloc(S, sizeof(ll*)); tc = calloc(S, sizeof(ll*));
  for (int pass = 0; pass < 2; pass++) {
    if (pass == 1) for (int s = 0; s < S; s++) { tb[s] = malloc((cnt[s]+1)*sizeof(ll)); tc[s] = malloc((cnt[s]+1)*sizeof(ll)); cnt[s] = 0; }
    for (int x = -Q; x <= Q; x++) for (int y = x; y <= Q; y++) for (int z = y; z <= Q; z++) {
      int s = IDX(x+y+z);
      if (pass == 1) { tb[s][cnt[s]] = (ll)x*x+(ll)y*y+(ll)z*z; tc[s][cnt[s]] = (ll)x*x*x+(ll)y*y*y+(ll)z*z*z; }
      cnt[s]++;
    }
  }
  size_t cap = 1 << 20; key *A = malloc(cap*sizeof(key)), *B = malloc(cap*sizeof(key));
  ll total = 0;
  for (int aQ = -3*Q; aQ <= 3*Q; aQ++) for (int au = -3*Q; au <= 3*Q; au++) {
    int ad = -2*aQ - au, aL = -3*aQ, ae = 2*aQ - au, an = 4*aQ + au;
    if (ad < -3*Q || ad > 3*Q || aL < -3*Q || aL > 3*Q || ae < -3*Q || ae > 3*Q) continue;
    if (nu) { if (an < -3*Q || an > 3*Q) continue; } else if (an != 0) continue;
    int iQ = IDX(aQ), iu = IDX(au), id = IDX(ad), iL = IDX(aL), ie = IDX(ae), in = IDX(an);
    size_t nA = (size_t)cnt[iQ]*cnt[iu]*cnt[id];
    size_t nB = (size_t)cnt[iL]*cnt[ie]*(nu ? cnt[in] : 1);
    if (!nA || !nB) continue;
    size_t need = nA > nB ? nA : nB;
    if (need > cap) { cap = need; A = realloc(A, cap*sizeof(key)); B = realloc(B, cap*sizeof(key)); }
    size_t k = 0;
    for (int i = 0; i < cnt[iQ]; i++) for (int j = 0; j < cnt[iu]; j++) for (int l = 0; l < cnt[id]; l++) {
      A[k].b = tb[iQ][i] - 2*tb[iu][j] + tb[id][l];
      A[k].c = 6*tc[iQ][i] + 3*tc[iu][j] + 3*tc[id][l]; k++;
    }
    k = 0;
    int nn = nu ? cnt[in] : 1;
    for (int i = 0; i < cnt[iL]; i++) for (int j = 0; j < cnt[ie]; j++) for (int l = 0; l < nn; l++) {
      B[k].b = -(-tb[iL][i] + tb[ie][j]);
      B[k].c = -(2*tc[iL][i] + tc[ie][j] + (nu ? tc[in][l] : 0)); k++;
    }
    qsort(A, nA, sizeof(key), cmpk); qsort(B, nB, sizeof(key), cmpk);
    size_t i = 0, j = 0;
    while (i < nA && j < nB) {
      int r = cmpk(&A[i], &B[j]);
      if (r < 0) i++; else if (r > 0) j++;
      else { size_t i2 = i, j2 = j; while (i2 < nA && !cmpk(&A[i2], &A[i])) i2++; while (j2 < nB && !cmpk(&B[j2], &B[j])) j2++;
             total += (ll)(i2 - i) * (ll)(j2 - j); i = i2; j = j2; }
    }
  }
  printf("N %d %d %lld\n", Q, nu, total);
  return 0;
}
