/* Second counter, different split and matching: halves (Q,L,e) | (u,d,nu), hash-table matching (no sorting).
   Same quantity as count.c: N(Q) = number of tuples of sorted species triples satisfying all six ACCs, zero included.
   Linear ACCs: a_d = -2a_Q - a_u, a_L = -3a_Q, a_e = 2a_Q - a_u, a_nu = 4a_Q + a_u (SM: a_nu = 0).
   Key of (Q,L,e): (b_Q - b_L + b_e, 6c_Q + 2c_L + c_e); key of (u,d,nu): (-2b_u + b_d, 3c_u + 3c_d + c_nu).
   Usage: count2 QMAX NU */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll;
static int Q;
static int nt; static int *ts; static ll *tb, *tc;   /* all sorted triples: sum, square-sum, cube-sum */
static uint64_t *hk1, *hk2; static ll *hv; static size_t hcap;
static inline uint64_t mix(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
static void hclear(void) { for (size_t i = 0; i < hcap; i++) hv[i] = 0; }
static void hadd(ll b, ll c) {
  uint64_t h = mix((uint64_t)b * 0x9E3779B97F4A7C15ULL ^ (uint64_t)c) & (hcap - 1);
  while (hv[h] && (hk1[h] != (uint64_t)b || hk2[h] != (uint64_t)c)) h = (h + 1) & (hcap - 1);
  hk1[h] = (uint64_t)b; hk2[h] = (uint64_t)c; hv[h]++;
}
static ll hget(ll b, ll c) {
  uint64_t h = mix((uint64_t)b * 0x9E3779B97F4A7C15ULL ^ (uint64_t)c) & (hcap - 1);
  while (hv[h]) { if (hk1[h] == (uint64_t)b && hk2[h] == (uint64_t)c) return hv[h]; h = (h + 1) & (hcap - 1); }
  return 0;
}
int main(int argc, char **argv) {
  Q = atoi(argv[1]); int nu = atoi(argv[2]);
  int S = 6*Q + 1;
  /* per-sum index lists */
  int maxn = (2*Q+1)*(2*Q+2)*(2*Q+3)/6;
  ts = malloc(maxn*sizeof(int)); tb = malloc(maxn*sizeof(ll)); tc = malloc(maxn*sizeof(ll));
  int **byS = calloc(S, sizeof(int*)); int *nS = calloc(S, sizeof(int));
  nt = 0;
  for (int x = -Q; x <= Q; x++) for (int y = x; y <= Q; y++) for (int z = y; z <= Q; z++) {
    ts[nt] = x+y+z; tb[nt] = (ll)x*x+(ll)y*y+(ll)z*z; tc[nt] = (ll)x*x*x+(ll)y*y*y+(ll)z*z*z; nS[ts[nt]+3*Q]++; nt++;
  }
  for (int s = 0; s < S; s++) { byS[s] = malloc((nS[s]+1)*sizeof(int)); nS[s] = 0; }
  for (int i = 0; i < nt; i++) { int s = ts[i]+3*Q; byS[s][nS[s]++] = i; }
  hcap = 1; ll total = 0;
  for (int aQ = -3*Q; aQ <= 3*Q; aQ++) for (int au = -3*Q; au <= 3*Q; au++) {
    int ad = -2*aQ - au, aL = -3*aQ, ae = 2*aQ - au, an = 4*aQ + au;
    if (ad < -3*Q || ad > 3*Q || aL < -3*Q || aL > 3*Q || ae < -3*Q || ae > 3*Q) continue;
    if (nu) { if (an < -3*Q || an > 3*Q) continue; } else if (an != 0) continue;
    int *LQ = byS[aQ+3*Q], *LL = byS[aL+3*Q], *Le = byS[ae+3*Q], *Lu = byS[au+3*Q], *Ld = byS[ad+3*Q], *Ln = byS[an+3*Q];
    int mQ = nS[aQ+3*Q], mL = nS[aL+3*Q], me = nS[ae+3*Q], mu_ = nS[au+3*Q], md = nS[ad+3*Q], mn = nu ? nS[an+3*Q] : 1;
    size_t nA = (size_t)mQ*mL*me;
    if (!nA || !((size_t)mu_*md*mn)) continue;
    size_t want = 1; while (want < 2*nA) want <<= 1;
    if (want > hcap) { hcap = want; free(hk1); free(hk2); free(hv); hk1 = malloc(hcap*8); hk2 = malloc(hcap*8); hv = malloc(hcap*sizeof(ll)); }
    hclear();
    for (int i = 0; i < mQ; i++) for (int j = 0; j < mL; j++) for (int k = 0; k < me; k++) {
      int a = LQ[i], b = LL[j], c = Le[k];
      hadd(tb[a] - tb[b] + tb[c], 6*tc[a] + 2*tc[b] + tc[c]);
    }
    for (int i = 0; i < mu_; i++) for (int j = 0; j < md; j++) for (int k = 0; k < mn; k++) {
      int a = Lu[i], b = Ld[j];
      ll bb = -2*tb[a] + tb[b], cc = 3*tc[a] + 3*tc[b] + (nu ? tc[Ln[k]] : 0);
      total += hget(-bb, -cc);
    }
  }
  printf("N %d %d %lld\n", Q, nu, total);
  return 0;
}
