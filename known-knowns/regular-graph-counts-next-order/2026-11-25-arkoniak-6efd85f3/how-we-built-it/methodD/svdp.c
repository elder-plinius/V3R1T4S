/* svdp: C port of Svdp.S_all (vertex DP for the short part of method D), modulo the Mersenne prime 2^E-1.
   usage: svdp D SIDE N E < shifts   (stdin: K, then K lines of D ints)  ->  K lines, value in hex.
   Same states, transitions and prunes as Svdp.S_all (Python, run 2026-11-20-0141); exact mod 2^E-1, E <= 639. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/resource.h>
typedef unsigned __int128 u128;
#ifndef NL
#define NL 10
#endif
typedef struct { uint64_t l[NL]; } mp;
static int E, TOPB, TOPL; /* bits of top limb */
static void fold(mp *a) { /* value = low E bits + (value >> E), repeated (2^E == 1 mod P); input < 2^(64*NL) */
  for (;;) { mp hi; int nz = 0;
    for (int i = 0; i < NL; i++) { int bit = E + 64 * i, w = bit / 64, s = bit % 64; uint64_t v = 0;
      if (w < NL) { v = a->l[w] >> s; if (s && w + 1 < NL) v |= a->l[w + 1] << (64 - s); } hi.l[i] = v; nz |= v != 0; }
    if (!nz) return;
    a->l[TOPL] &= ((uint64_t)1 << TOPB) - 1; for (int i = TOPL + 1; i < NL; i++) a->l[i] = 0;
    u128 c = 0; for (int i = 0; i < NL; i++) { c += (u128)a->l[i] + hi.l[i]; a->l[i] = (uint64_t)c; c >>= 64; } } }
static void addto(mp *a, const mp *b) { u128 c = 0; for (int i = 0; i < NL; i++) { c += (u128)a->l[i] + b->l[i]; a->l[i] = (uint64_t)c; c >>= 64; } fold(a); }
static void mulsmall(mp *r, const mp *a, uint64_t s) { /* a < 2^E */
  u128 c = 0; mp t; for (int i = 0; i < NL; i++) { c += (u128)a->l[i] * s; t.l[i] = (uint64_t)c; c >>= 64; }
  uint64_t ex = (uint64_t)c; fold(&t); /* t < 2^E; ex sits at bit 64*NL == bit (64*NL - E) mod P */
  if (ex) { int sh = 64 * NL - E; mp u; memset(&u, 0, sizeof u); u.l[sh / 64] = ex << (sh % 64); if (sh % 64) u.l[sh / 64 + 1] = ex >> (64 - sh % 64);
    u128 cc = 0; for (int i = 0; i < NL; i++) { cc += (u128)t.l[i] + u.l[i]; t.l[i] = (uint64_t)cc; cc >>= 64; } fold(&t); }
  *r = t; }
static void mulmod(mp *r, const mp *a, const mp *b) {
  uint64_t p[2 * NL + 1]; memset(p, 0, sizeof p);
  for (int i = 0; i < NL; i++) { if (!a->l[i]) continue; u128 c = 0;
    for (int j = 0; j < NL; j++) { c += (u128)a->l[i] * b->l[j] + p[i + j]; p[i + j] = (uint64_t)c; c >>= 64; }
    p[i + NL] += (uint64_t)c; }
  /* r = low E bits + (p >> E) */
  mp lo, hi; memset(&lo, 0, sizeof lo); memset(&hi, 0, sizeof hi);
  for (int i = 0; i <= TOPL; i++) lo.l[i] = p[i]; lo.l[TOPL] &= ((uint64_t)1 << TOPB) - 1;
  for (int i = 0; i < NL; i++) { int bit = E + 64 * i, w = bit / 64, s = bit % 64;
    uint64_t v = p[w] >> s; if (s && w + 1 < 2 * NL + 1) v |= p[w + 1] << (64 - s); hi.l[i] = v; }
  addto(&lo, &hi); *r = lo; }
static void canon(mp *a) { fold(a); /* if a == P (all E bits set) -> 0 */
  int all = 1; for (int i = 0; i < TOPL; i++) if (a->l[i] != ~(uint64_t)0) all = 0;
  if (a->l[TOPL] != (((uint64_t)1 << TOPB) - 1)) all = 0; if (all) memset(a, 0, sizeof *a); }
static void inv(mp *r, uint64_t x) { /* x^(P-2), P-2 = 2^E - 3: bits: E-1..2 ones, bit1 = 0, bit0 = 1 */
  mp b; memset(&b, 0, sizeof b); b.l[0] = x; mp acc; memset(&acc, 0, sizeof acc); acc.l[0] = 1;
  for (int i = E - 1; i >= 0; i--) { mulmod(&acc, &acc, &acc); if (i != 1) mulmod(&acc, &acc, &b); }
  canon(&acc); *r = acc; }

static int D, SIDE, N, G, SELF;
static int cap[8], capw;
static uint64_t radR, radB[8], mulR[8], mulB[8];
/* hash table: dense key/value arrays + a uint32 index table (2026-11-23: was key+mp+flag per slot, old+new alive on grow) */
typedef struct { uint64_t *k; mp *v; uint32_t *ix; size_t cap, n, vcap; } ht;
static void oom(void) { fprintf(stderr, "svdp: out of memory\n"); exit(3); }
static void ht_init(ht *h, size_t c) { h->cap = c; h->n = 0; h->vcap = c / 2; h->k = malloc(h->vcap * 8); h->v = malloc(h->vcap * sizeof(mp)); h->ix = calloc(c, 4);
  if (!h->k || !h->v || !h->ix) oom(); }
static void ht_free(ht *h) { free(h->k); free(h->v); free(h->ix); }
static inline size_t hsh(uint64_t k, size_t c) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; return (size_t)(k & (c - 1)); }
static void ht_grow(ht *h) { size_t c = h->cap * 2; uint32_t *ix = calloc(c, 4); if (!ix) oom(); free(h->ix);
  for (size_t j = 0; j < h->n; j++) { size_t i = hsh(h->k[j], c); while (ix[i]) i = (i + 1) & (c - 1); ix[i] = (uint32_t)(j + 1); }
  h->ix = ix; h->cap = c; }
static mp *ht_get(ht *h, uint64_t key) { if (h->n * 10 >= h->cap * 7) ht_grow(h);
  size_t i = hsh(key, h->cap); while (h->ix[i]) { size_t j = h->ix[i] - 1; if (h->k[j] == key) return &h->v[j]; i = (i + 1) & (h->cap - 1); }
  if (h->n == h->vcap) { size_t vc = h->vcap * 2; uint64_t *k2 = realloc(h->k, vc * 8); if (!k2) oom(); h->k = k2;
    mp *v2 = realloc(h->v, vc * sizeof(mp)); if (!v2) oom(); h->v = v2; h->vcap = vc; }
  size_t j = h->n++; h->ix[i] = (uint32_t)(j + 1); h->k[j] = key; memset(&h->v[j], 0, sizeof(mp)); return &h->v[j]; }

static uint64_t binom[64][64];
static mp invf[16]; /* inv(c!) */

/* emit enumeration */
typedef struct { int load; int B2[8]; int cs[8]; } emit_t;
static emit_t emits[200000]; static int nemit;
static void emit_rec(int j, int load, int lim, const int *B, int *Bl, int *cs) {
  if (j == D) { emit_t *e = &emits[nemit++]; e->load = load; memcpy(e->B2, Bl, sizeof(int) * 8); memcpy(e->cs, cs, sizeof(int) * 8); return; }
  int size = j + 1;
  for (int c = 0; B[j] + c <= cap[j] && load + c * size <= lim; c++) { Bl[j] = B[j] + c; cs[j] = c; emit_rec(j + 1, load + c * size, lim, B, Bl, cs); }
  Bl[j] = B[j]; cs[j] = 0; }
/* edges enumeration */
typedef struct { int R2[8]; int used; uint64_t w; } edge_t;
static edge_t edges[400000]; static int nedge;
static int Rcur[8], NEED;
static void edge_rec(int r, int *Rl, int used, uint64_t wt);
static void rk_rec(int r, int i, int nks, int avail, int *Rl, int used, uint64_t wt) {
  if (i == nks) { edge_rec(r + 1, Rl, used, wt); return; }
  int k = i + 1;
  for (int m = 0; m <= avail && used + m * k <= NEED; m++) {
    int R3[8]; memcpy(R3, Rl, sizeof R3);
    if (m) { R3[r - 1] -= m; if (r - k) R3[r - k - 1] += m; }
    uint64_t w2 = wt * binom[avail][m]; uint64_t gk = binom[G][k]; for (int t = 0; t < m; t++) w2 *= gk;
    rk_rec(r, i + 1, nks, avail - m, R3, used + m * k, w2); } }
static void edge_rec(int r, int *Rl, int used, uint64_t wt) {
  if (r > D) { edge_t *e = &edges[nedge++]; memcpy(e->R2, Rl, sizeof(int) * 8); e->used = used; e->w = wt; return; }
  int nks = G < r ? G : r; rk_rec(r, 0, nks, Rcur[r - 1], Rl, used, wt); }

int main(int argc, char **argv) {
  if (argc != 5) { fprintf(stderr, "usage: svdp D SIDE N E < shifts\n"); return 2; }
  D = atoi(argv[1]); SIDE = atoi(argv[2]); N = atoi(argv[3]); E = atoi(argv[4]);
  if (D < 1 || D > 8 || E < 64 || E > 64 * NL - 1 || N < 0 || N > 62) { fprintf(stderr, "svdp: bad args\n"); return 2; }
  TOPL = (E - 1) / 64; TOPB = E - 64 * TOPL; if (TOPB == 64) { fprintf(stderr, "svdp: E multiple of 64 unsupported\n"); return 2; }
  G = SIDE == 0 ? 1 : 2; SELF = SIDE == 1;
  for (int i = 0; i < 64; i++) { binom[i][0] = 1; for (int j = 1; j <= i; j++) binom[i][j] = binom[i - 1][j - 1] + (j <= i - 1 ? binom[i - 1][j] : 0); }
  int K; if (scanf("%d", &K) != 1) return 2;
  int (*sh)[8] = calloc(K + 1, sizeof *sh);
  for (int s = 0; s < K; s++) for (int j = 0; j < D; j++) if (scanf("%d", &sh[s][j]) != 1) return 2;
  memset(cap, 0, sizeof cap); capw = 0;
  for (int s = 0; s < K; s++) { int w = 0; for (int j = 0; j < D; j++) { if (sh[s][j] > cap[j]) cap[j] = sh[s][j]; w += (j + 1) * sh[s][j]; } if (w > capw) capw = w; }
  { mp one; memset(&one, 0, sizeof one); invf[0] = one; invf[0].l[0] = 1; uint64_t f = 1;
    for (int c = 1; c <= D; c++) { f *= c; inv(&invf[c], f); } }
  /* mixed radix: R_r in [0, N], B_j in [0, cap_j] */
  double tot = 1; uint64_t m = 1;
  for (int r = 0; r < D; r++) { mulR[r] = m; m *= (uint64_t)(N + 1); tot *= N + 1; }
  for (int j = 0; j < D; j++) { mulB[j] = m; m *= (uint64_t)(cap[j] + 1); tot *= cap[j] + 1; }
  if (tot > 1.8e19) { fprintf(stderr, "svdp: key space too large\n"); return 2; }
  ht cur, nxt; ht_init(&cur, 1 << 10); ht_get(&cur, 0)->l[0] = 1;
  size_t maxst = 1;
  for (int v = 0; v < N; v++) {
    int left = N - v - 1; ht_init(&nxt, 1 << 10);
    for (size_t si = 0; si < cur.n; si++) {
      mp w = cur.v[si]; uint64_t key = cur.k[si]; int R[8] = {0}, B[8] = {0};
      { uint64_t t = key; for (int r = 0; r < D; r++) { R[r] = t % (N + 1); t /= (N + 1); } for (int j = 0; j < D; j++) { B[j] = t % (cap[j] + 1); t /= (cap[j] + 1); } }
      int bw0 = 0; for (int j = 0; j < D; j++) bw0 += (j + 1) * B[j];
      int lim = capw - bw0; if (lim > D) lim = D;
      nemit = 0; { int Bl[8], cs[8]; memcpy(Bl, B, sizeof Bl); memset(cs, 0, sizeof cs); if (lim >= 0) emit_rec(0, 0, lim, B, Bl, cs); }
      /* edges depend on (R, need); compute per need value lazily */
      static edge_t *ecache[9]; static int ecount[9]; static int ehave[9];
      for (int q = 0; q <= D; q++) ehave[q] = 0;
      memcpy(Rcur, R, sizeof Rcur);
      for (int ei = 0; ei < nemit; ei++) {
        emit_t *em = &emits[ei]; mp wb; int any = 0;
        mp bwv; memset(&bwv, 0, sizeof bwv); bwv.l[0] = 1;
        for (int j = 0; j < D; j++) if (em->cs[j] > 1) { mulmod(&bwv, &bwv, &invf[em->cs[j]]); any = 1; }
        if (any) mulmod(&wb, &w, &bwv); else wb = w;
        uint64_t kB = 0; for (int j = 0; j < D; j++) kB += (uint64_t)em->B2[j] * mulB[j];
        for (int so = 0; so <= SELF; so++) {
          int need = D - em->load - so; if (need < 0) continue;
          if (!ehave[need]) { NEED = need; nedge = 0; int Rl[8]; memcpy(Rl, R, sizeof Rl); edge_rec(1, Rl, 0, 1);
            free(ecache[need]); ecache[need] = malloc(sizeof(edge_t) * (nedge ? nedge : 1)); memcpy(ecache[need], edges, sizeof(edge_t) * nedge); ecount[need] = nedge; ehave[need] = 1; }
          for (int k = 0; k < ecount[need]; k++) {
            edge_t *ed = &ecache[need][k]; int res = need - ed->used;
            if (res > left * G) continue;
            int R3[8]; memcpy(R3, ed->R2, sizeof R3); if (res) R3[res - 1]++;
            int bad = 0; for (int r = left * G + 1; r <= D; r++) if (R3[r - 1]) { bad = 1; break; } if (bad) continue;
            int sr = 0; for (int r = 1; r <= D; r++) sr += r * R3[r - 1]; if (sr > left * D) continue;
            uint64_t kk = kB; for (int r = 0; r < D; r++) kk += (uint64_t)R3[r] * mulR[r];
            mp t; mulsmall(&t, &wb, ed->w); addto(ht_get(&nxt, kk), &t);
          }
        }
      }
    }
    ht_free(&cur); cur = nxt; if (cur.n > maxst) maxst = cur.n;
  }
  uint64_t fact[16]; fact[0] = 1; for (int i = 1; i < 16; i++) fact[i] = fact[i - 1] * i;
  for (int s = 0; s < K; s++) {
    uint64_t kk = 0; for (int j = 0; j < D; j++) kk += (uint64_t)sh[s][j] * mulB[j];
    mp val; memset(&val, 0, sizeof val);
    size_t i = hsh(kk, cur.cap); while (cur.ix[i]) { size_t j = cur.ix[i] - 1; if (cur.k[j] == kk) { val = cur.v[j]; break; } i = (i + 1) & (cur.cap - 1); }
    for (int j = 0; j < D; j++) { int c = sh[s][j]; while (c > 1) { mulsmall(&val, &val, (uint64_t)c); c--; } }
    canon(&val);
    int started = 0; for (int i2 = NL - 1; i2 >= 0; i2--) { if (!started && !val.l[i2] && i2) continue; printf(started ? "%016llx" : "%llx", (unsigned long long)val.l[i2]); started = 1; }
    printf("\n");
  }
  { struct rusage ru; getrusage(RUSAGE_SELF, &ru); fprintf(stderr, "svdp: d=%d side=%d n=%d K=%d maxstates=%zu maxrss=%ldMB\n", D, SIDE, N, K, maxst, ru.ru_maxrss / 1024); }
  return 0;
}
