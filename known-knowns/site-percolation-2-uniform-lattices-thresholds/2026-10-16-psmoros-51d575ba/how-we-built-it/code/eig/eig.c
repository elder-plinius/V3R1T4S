/* eig.c -- eigenvalue form of the Jacobsen-Scullard criterion on semi-infinite cylinders (Jacobsen 2015,
 *          arXiv 1507.03027, eq. 13): P_B = 0 on W x m tori with m -> infinity  <=>  Lambda_open = Lambda_closed.
 *
 * Usage: eig site|bond L P0 [maxpass] < graph.txt
 *   graph.txt: mkgraph.py output for a torus with exactly 2L layers (rows y = 0..2L-1), L = vertical period in rows.
 *   The transfer matrix T adds one period: the vertices of rows L..2L-1 and every edge whose later endpoint lies in
 *   those rows and whose y-seam count is 0 (so the edges from row L-1 to row L are included, the y-seam edges are not).
 *   The frontier before T is row L-1, after T it is row 2L-1 (same x positions), so T maps the state space to itself.
 * Sectors (no strings, cf. 1507.03027 sec 3-4):
 *   closed: no frontier cluster winds around the circumference; creating a winding cycle kills the configuration.
 *   open:   one marked frontier cluster winds; if it leaves the frontier the configuration is 1D (killed); a winding
 *           cycle in an unmarked cluster while the marked one is alive is impossible by planarity (counted, killed).
 * Weights: truncated Taylor series in delta = p - P0. Power iteration with series normalisation gives Lambda(P0+delta)
 * as a series in each sector; Newton on Lambda_open - Lambda_closed gives the root; repeated (maxpass) at the new P0.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#define KT 6
#define MAXV 8192
#define MAXE 32768
#define FMAXC 48

static int N, E, site, Lp;
static int eu[MAXE], ev[MAXE], edx[MAXE], edy[MAXE], vx[MAXV], vy[MAXV];
static double P0;
static int KL;

typedef struct { size_t cap, n; uint8_t *keys; double *w; uint8_t *used; } Table;
static uint64_t hkey(const uint8_t *k) {
  uint64_t h = 0x9E3779B97F4A7C15ULL; const uint64_t *q = (const uint64_t *)k;
  for (int i = 0; i < KL / 8; i++) { h ^= q[i]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 32; }
  h ^= h >> 29; h *= 0xc4ceb9fe1a85ec53ULL; h ^= h >> 32; return h;
}
static void tinit(Table *t, size_t cap) {
  t->cap = cap; t->n = 0; t->keys = (uint8_t *)malloc(cap * KL); t->w = (double *)calloc(cap * KT, sizeof(double));
  t->used = (uint8_t *)calloc(cap, 1);
  if (!t->keys || !t->w || !t->used) { fprintf(stderr, "out of memory\n"); exit(2); }
}
static void tfree(Table *t) { free(t->keys); free(t->w); free(t->used); }
static void tadd(Table *t, const uint8_t *k, const double *w);
static void tgrow(Table *t) { Table nt; tinit(&nt, t->cap * 2);
  for (size_t i = 0; i < t->cap; i++) if (t->used[i]) tadd(&nt, t->keys + i * KL, t->w + i * KT); tfree(t); *t = nt; }
static void tadd(Table *t, const uint8_t *k, const double *w) {
  if (2 * (t->n + 1) > t->cap) tgrow(t);
  size_t m = t->cap - 1, i = hkey(k) & m;
  while (t->used[i]) {
    if (memcmp(t->keys + i * KL, k, KL) == 0) { for (int j = 0; j < KT; j++) t->w[i * KT + j] += w[j]; return; }
    i = (i + 1) & m;
  }
  t->used[i] = 1; memcpy(t->keys + i * KL, k, KL); for (int j = 0; j < KT; j++) t->w[i * KT + j] = w[j]; t->n++;
}
static void mulp(double *o, const double *w) { for (int i = KT - 1; i >= 0; i--) o[i] = P0 * w[i] + (i ? w[i - 1] : 0.0); }
static void mulq(double *o, const double *w) { for (int i = KT - 1; i >= 0; i--) o[i] = (1.0 - P0) * w[i] - (i ? w[i - 1] : 0.0); }
static void sdiv(double *o, const double *a, const double *b) { /* o = a / b as series */
  double r[KT];
  for (int i = 0; i < KT; i++) { double s = a[i]; for (int j = 1; j <= i; j++) s -= b[j] * r[i - j]; r[i] = s / b[0]; }
  memcpy(o, r, sizeof r);
}

typedef struct { int F, nlab; int lab[FMAXC + 2], ox[FMAXC + 2], mk[2 * FMAXC + 6]; } St;
static int sector_open;
static void decode(const uint8_t *k, int F, St *s) {
  s->F = F; s->nlab = 0;
  for (int i = 0; i < F; i++) {
    int l = k[2 * i] & 63, m = (k[2 * i] >> 6) & 1;
    s->lab[i] = l; s->ox[i] = (int8_t)k[2 * i + 1];
    if (l) { if (l > s->nlab) { for (int j = s->nlab + 1; j <= l; j++) s->mk[j] = 0; s->nlab = l; } if (m) s->mk[l] = 1; }
  }
}
static void encode(St *s, const int *keep, int nkeep, uint8_t *k) {
  int map[2 * FMAXC + 6], ref[2 * FMAXC + 6];
  for (int j = 0; j <= s->nlab; j++) map[j] = 0;
  memset(k, 0, KL);
  int nl = 0;
  for (int t = 0; t < nkeep; t++) {
    int i = keep[t], l = s->lab[i];
    if (!l) continue;
    if (!map[l]) { map[l] = ++nl; ref[l] = s->ox[i]; }
    int dx = s->mk[l] ? 0 : s->ox[i] - ref[l];
    if (dx < -127 || dx > 127 || nl > 63) { fprintf(stderr, "encode overflow\n"); exit(4); }
    k[2 * t] = (uint8_t)(map[l] | (s->mk[l] << 6)); k[2 * t + 1] = (uint8_t)(int8_t)dx;
  }
}
static long n_kill_wrap = 0, n_kill_1d = 0, n_impossible = 0;
/* returns 1 if configuration is killed */
static int merge(St *s, int u, int v, int d) {
  int lu = s->lab[u], lv = s->lab[v];
  int c = s->ox[u] + d - s->ox[v];
  if (lu == lv) {
    if (c == 0 || s->mk[lu]) return 0;
    /* new winding cycle in an unmarked cluster */
    if (!sector_open) { n_kill_wrap++; return 1; }
    for (int j = 1; j <= s->nlab; j++) if (s->mk[j]) { n_impossible++; return 1; }
    s->mk[lu] = 1; return 0;     /* open sector with no live marked cluster cannot occur after init; kept general */
  }
  int m = s->mk[lu] | s->mk[lv];
  for (int i = 0; i < s->F; i++) if (s->lab[i] == lv) { s->lab[i] = lu; s->ox[i] += c; }
  s->mk[lu] = m; s->mk[lv] = 0;
  return 0;
}

static int nE_v, Eu_pos[64], Ed_[64], vpos, keep[FMAXC + 2], nkeep, remv[FMAXC + 2], nremv;
static Table *NT;
static void leaf(St *s, const double *w) {
  for (int r = 0; r < nremv; r++) {
    int i = remv[r], l = s->lab[i];
    if (!l) continue;
    int alive = 0;
    for (int t = 0; t < nkeep; t++) if (s->lab[keep[t]] == l) { alive = 1; break; }
    if (!alive && s->mk[l]) { n_kill_1d++; return; }
  }
  uint8_t key[256]; encode(s, keep, nkeep, key); tadd(NT, key, w);
}
static void rec(St *s, int e, const double *w) {
  if (e == nE_v) { leaf(s, w); return; }
  int u = Eu_pos[e];
  if (site) {
    if (s->lab[u] && s->lab[vpos]) { St c = *s; if (merge(&c, u, vpos, Ed_[e])) return; rec(&c, e + 1, w); }
    else rec(s, e + 1, w);
  } else {
    double wo[KT], wc[KT]; mulp(wo, w); mulq(wc, w);
    rec(s, e + 1, wc);
    St c = *s; if (merge(&c, u, vpos, Ed_[e])) return; rec(&c, e + 1, wo);
  }
}

/* period structure */
static int proc[MAXV], nproc, init_front[FMAXC + 2], ninit, lastuse[MAXV];

static void apply_T(Table *in, Table *out) {
  int front[FMAXC + 2], nf = ninit;
  for (int i = 0; i < ninit; i++) front[i] = init_front[i];
  Table T0 = *in;
  int own = 0;
  for (int pi = 0; pi < nproc; pi++) {
    int v = proc[pi];
    int wf[FMAXC + 2], nw = 0;
    for (int i = 0; i < nf; i++) wf[nw++] = front[i];
    wf[nw++] = v; vpos = nw - 1;
    nE_v = 0;
    for (int e = 0; e < E; e++) {
      if (edy[e] != 0 || ev[e] != v || vy[eu[e]] < Lp - 1) continue;
      if (vy[eu[e]] == Lp - 1 && vy[ev[e]] == Lp - 1) continue;
      int up = -1; for (int i = 0; i < nw; i++) if (wf[i] == eu[e]) { up = i; break; }
      if (up < 0) { fprintf(stderr, "endpoint not in frontier\n"); exit(1); }
      Eu_pos[nE_v] = up; Ed_[nE_v] = edx[e]; nE_v++;
    }
    nkeep = nremv = 0;
    for (int i = 0; i < nw; i++) { if (lastuse[wf[i]] == v) remv[nremv++] = i; else keep[nkeep++] = i; }
    Table T1; { size_t c = 1024; while (c < 3 * T0.n) c <<= 1; tinit(&T1, c); } NT = &T1;
    for (size_t i = 0; i < T0.cap; i++) {
      if (!T0.used[i]) continue;
      St s; decode(T0.keys + i * KL, nf, &s);
      s.F = nw; s.lab[vpos] = 0; s.ox[vpos] = 0;
      const double *w = T0.w + i * KT;
      if (site) {
        double wo[KT], wc[KT]; mulp(wo, w); mulq(wc, w);
        rec(&s, 0, wc);
        int l = s.nlab + 1; s.nlab = l; s.lab[vpos] = l; s.mk[l] = 0; rec(&s, 0, wo);
      } else { int l = s.nlab + 1; s.nlab = l; s.lab[vpos] = l; s.mk[l] = 0; rec(&s, 0, w); }
    }
    if (own) tfree(&T0);
    T0 = T1; own = 1;
    nf = 0; for (int t = 0; t < nkeep; t++) front[nf++] = wf[keep[t]];
  }
  if (nf != ninit) { fprintf(stderr, "frontier size mismatch %d %d\n", nf, ninit); exit(1); }
  for (int i = 0; i < nf; i++) if (vx[front[i]] != vx[init_front[i]] || vy[front[i]] != 2 * Lp - 1) {
    fprintf(stderr, "frontier position mismatch\n"); exit(1); }
  *out = T0;
}

static int rot_step = 0;   /* 0 = no symmetry reduction; else translate frontier by rot_step columns */
/* canonical representative of the translation class of a period-boundary state (slots = row in x order) */
static void canon_rot(const uint8_t *k, uint8_t *best) {
  memcpy(best, k, KL);
  St s; decode(k, ninit, &s);
  int W = ninit;
  int idk[FMAXC + 2]; for (int i = 0; i < W; i++) idk[i] = i;
  uint8_t cand[256];
  for (int sh = rot_step; sh < W; sh += rot_step) {
    St r = s;
    for (int j = 0; j < W; j++) {
      int o = (j + sh) % W;                 /* new slot j holds old slot o (configuration translated by -sh) */
      r.lab[j] = s.lab[o];
      r.ox[j] = s.ox[o] - ((j + sh) >= W ? 1 : 0);
    }
    encode(&r, idk, W, cand);
    if (memcmp(cand, best, KL) < 0) memcpy(best, cand, KL);
  }
}
static void reduce_rot(Table *t) {
  if (!rot_step) return;
  Table n; { size_t c = 1024; while (c < 3 * t->n) c <<= 1; tinit(&n, c); }
  uint8_t b[256];
  for (size_t i = 0; i < t->cap; i++) if (t->used[i]) { canon_rot(t->keys + i * KL, b); tadd(&n, b, t->w + i * KT); }
  tfree(t); *t = n;
}

static void sumw(Table *t, double *s) { for (int j = 0; j < KT; j++) s[j] = 0;
  for (size_t i = 0; i < t->cap; i++) if (t->used[i]) for (int j = 0; j < KT; j++) s[j] += t->w[i * KT + j]; }

/* power iteration in a sector, returns eigenvalue series and iteration count */
static int power(int open, double *lam, int maxit, size_t *nstates) {
  sector_open = open;
  Table v; tinit(&v, 1024);
  uint8_t k[256]; memset(k, 0, KL);
  double w1[KT] = {0}; w1[0] = 1.0;
  for (int i = 0; i < ninit; i++) {
    if (site) { if (open) { k[2 * i] = 1 | 64; } else k[2 * i] = 0; }
    else { if (open) k[2 * i] = 1 | 64; else k[2 * i] = (uint8_t)(i + 1); }
  }
  tadd(&v, k, w1);
  double prev[KT] = {0};
  int it;
  for (it = 1; it <= maxit; it++) {
    Table w; apply_T(&v, &w); reduce_rot(&w);
    double sv[KT], sw[KT]; sumw(&v, sv); sumw(&w, sw);
    sdiv(lam, sw, sv);
    /* normalise w by sw (series) */
    double inv[KT], one[KT] = {0}; one[0] = 1.0; sdiv(inv, one, sw);
    for (size_t i = 0; i < w.cap; i++) if (w.used[i]) {
      double *x = w.w + i * KT, r[KT];
      for (int a = 0; a < KT; a++) { double s = 0; for (int b = 0; b <= a; b++) s += x[b] * inv[a - b]; r[a] = s; }
      memcpy(x, r, sizeof r);
    }
    tfree(&v); v = w;
    int conv = it > 8;
    for (int j = 0; j < KT; j++) {
      double scale = fabs(lam[j]) + fabs(lam[0]) * pow(10.0, j);   /* relative tolerance per coefficient */
      if (fabs(lam[j] - prev[j]) > 1e-13 * scale) conv = 0;
    }
    memcpy(prev, lam, sizeof prev);
    if (conv) break;
  }
  *nstates = v.n;
  tfree(&v);
  return it;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: eig site|bond L P0 [maxpass] < graph\n"); return 1; }
  site = strcmp(argv[1], "site") == 0; Lp = atoi(argv[2]); P0 = atof(argv[3]);
  int maxpass = argc > 4 ? atoi(argv[4]) : 3;
  if (getenv("EIG_ROT")) rot_step = atoi(getenv("EIG_ROT"));
  if (scanf("%d %d", &N, &E) != 2) return 1;
  for (int i = 0; i < N; i++) if (scanf("%d %d", &vx[i], &vy[i]) != 2) return 1;
  for (int e = 0; e < E; e++) if (scanf("%d %d %d %d", &eu[e], &ev[e], &edx[e], &edy[e]) != 4) return 1;
  int R = 0; for (int i = 0; i < N; i++) if (vy[i] + 1 > R) R = vy[i] + 1;
  if (R != 2 * Lp) { fprintf(stderr, "graph must have 2L rows\n"); return 1; }
  nproc = 0; ninit = 0;
  for (int i = 0; i < N; i++) { if (vy[i] >= Lp) proc[nproc++] = i; if (vy[i] == Lp - 1) init_front[ninit++] = i; }
  for (int i = 0; i < N; i++) lastuse[i] = (vy[i] == 2 * Lp - 1) ? -1 : i;
  for (int e = 0; e < E; e++) {
    if (edy[e] != 0 || vy[eu[e]] < Lp - 1) continue;
    if (vy[eu[e]] == Lp - 1 && vy[ev[e]] == Lp - 1) continue;
    int a = eu[e], b = ev[e];
    if (lastuse[a] != -1 && lastuse[a] < b) lastuse[a] = b;
    if (lastuse[b] != -1 && lastuse[b] < b) lastuse[b] = b;
  }
  /* initial-frontier vertices with no edge in the period would be removed at once: give them their own index? */
  for (int i = 0; i < ninit; i++) if (lastuse[init_front[i]] == init_front[i]) { fprintf(stderr, "frontier vertex without period edge\n"); return 1; }
  int fmax = ninit + 2 + ninit; if (fmax > FMAXC) fmax = FMAXC;
  KL = ((2 * fmax) + 7) / 8 * 8;
  fprintf(stderr, "eig: N=%d E=%d L=%d W=%d mode=%s rot_step=%d\n", N, E, Lp, ninit, site ? "site" : "bond", rot_step);
  if (rot_step) for (int i = 0; i < ninit; i++) if (vx[init_front[i]] != i) { fprintf(stderr, "rotation needs a full row frontier\n"); return 1; }
  for (int pass = 1; pass <= maxpass; pass++) {
    clock_t t0 = clock();
    double lo[KT], lc[KT]; size_t so, sc;
    int io = power(1, lo, 5000, &so), ic = power(0, lc, 5000, &sc);
    double g[KT]; for (int j = 0; j < KT; j++) g[j] = lo[j] - lc[j];
    double d = 0;
    for (int it = 0; it < 60; it++) { double f = 0, fp = 0;
      for (int j = KT - 1; j >= 0; j--) f = f * d + g[j];
      for (int j = KT - 1; j >= 1; j--) fp = fp * d + j * g[j];
      double nd = d - f / fp; if (nd == d) break; d = nd; }
    double trunc = fabs(g[KT - 1] * pow(fabs(d), KT - 1) / g[1]);
    printf("pass %d mode %s W %d L %d iters_open %d iters_closed %d states_open %zu states_closed %zu cpu %.1f kills_wrap %ld kills_1d %ld kill_newwrap %ld\n",
           pass, site ? "site" : "bond", ninit, Lp, io, ic, so, sc, (double)(clock() - t0) / CLOCKS_PER_SEC, n_kill_wrap, n_kill_1d, n_impossible);
    printf("P0 %.17g\nLopen", P0); for (int j = 0; j < KT; j++) printf(" %.17e", lo[j]);
    printf("\nLclosed"); for (int j = 0; j < KT; j++) printf(" %.17e", lc[j]);
    printf("\ndelta %.17e\ntrunc_est %.3e\nroot %.17g\n", d, trunc, P0 + d); fflush(stdout);
    if (fabs(d) < 1e-14 || trunc < 1e-16) break;
    P0 += d;
  }
  return 0;
}
