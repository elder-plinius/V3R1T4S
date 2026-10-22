/* Monomer-dimer transfer matrix on a row of m sites (open or periodic), unit weights.
   State s = set of sites whose vertical dimer enters the row from above; s' = set leaving downward.
   T[s,s'] = [s & s' == 0] * (number of matchings of the row graph induced on the sites not in s|s').
   Matrix-vector product y = T x by a site-by-site sweep with a 1-bit carry.
   Build: cc -O3 -DEXACT mdtm.c -o mdtm_ex   (unsigned __int128 elements, exact integers)
          cc -O3 mdtm.c -o mdtm_dbl            (double elements)
   Modes:
     mdtm dense m P                 print dense T (rows s, cols s') for small m
     mdtm count m P L               (exact) print (T^L)[0,0]: matchings of the m x L board (P=0) or of the
                                    cylinder with periodic rows of length m and L rows, free ends (P=1)
     mdtm tracedense m P L          (exact, m<=12) print Tr T^L by applying T to every basis vector
     mdtm pow m P iters vecfile     (double) power iteration from the all-ones vector; writes the vector (doubles)
     mdtm cw m P vecfile refine NTH (exact) make an exact integer vector from the double vector, refine it by `refine`
                                    exact multiplications, then print the EXACT Collatz-Wielandt max/min ratios
     mdtm hp m P iters [vecin] [vecout]   (exact) fixed-point power iteration; prints ||Tx||^2 and ||x||^2 as exact sums
*/
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "math.h"
#include "pthread.h"
#ifdef EXACT
typedef unsigned __int128 E;
#else
typedef double E;
#endif
static int m, P, NT = 12;
static uint64_t N;
static volatile int overflow_flag = 0;

typedef struct { void (*fn)(int, int, void*); void *arg; int t, nt; } job_t;
static void *runjob(void *p) { job_t *j = p; j->fn(j->t, j->nt, j->arg); return 0; }
static void pfor(void (*fn)(int, int, void*), void *arg) {
  pthread_t th[64]; job_t jb[64];
  for (int t = 0; t < NT; t++) { jb[t].fn = fn; jb[t].arg = arg; jb[t].t = t; jb[t].nt = NT; pthread_create(&th[t], 0, runjob, &jb[t]); }
  for (int t = 0; t < NT; t++) pthread_join(th[t], 0);
}
#ifdef EXACT
#define ADD(a,b,ov) ({ E _r=(a)+(b); if(_r<(a)) (ov)=1; _r; })
#else
#define ADD(a,b,ov) ((a)+(b))
#endif

static inline void step_range(E *G0, E *G1, int j, uint64_t p0, uint64_t p1, int *ov) {
  uint64_t lowmask = ((uint64_t)1 << j) - 1;
  for (uint64_t p = p0; p < p1; p++) {
    uint64_t i0 = ((p >> j) << (j + 1)) | (p & lowmask), i1 = i0 | ((uint64_t)1 << j);
    E a0 = G0[i0], a1 = G1[i0], b0 = G0[i1], b1 = G1[i1];
    E s = ADD(a0, a1, *ov);
    E t = ADD(b0, b1, *ov); t = ADD(t, a1, *ov);
    G0[i0] = t; G0[i1] = s; G1[i0] = s; G1[i1] = 0;
  }
}
typedef struct { E *G0, *G1; int nb; } sweep_arg;
#define CHUNKBITS 13
static void sweep_low(int t, int nt, void *vp) {
  sweep_arg *a = vp; int cb = a->nb < CHUNKBITS ? a->nb : CHUNKBITS;
  uint64_t nchunks = (uint64_t)1 << (a->nb - cb), csz = (uint64_t)1 << cb; int ov = 0;
  for (uint64_t c = t; c < nchunks; c += nt) {
    E *g0 = a->G0 + c * csz, *g1 = a->G1 + c * csz;
    for (int j = 0; j < cb; j++) step_range(g0, g1, j, 0, csz / 2, &ov);
  }
  if (ov) overflow_flag = 1;
}
typedef struct { E *G0, *G1; int nb; int j; } hi_arg;
static void sweep_hi(int t, int nt, void *vp) {
  hi_arg *a = vp; uint64_t np = (uint64_t)1 << (a->nb - 1); int ov = 0;
  uint64_t per = np / nt, p0 = per * t, p1 = (t == nt - 1) ? np : per * (t + 1);
  step_range(a->G0, a->G1, a->j, p0, p1, &ov);
  if (ov) overflow_flag = 1;
}
/* open chain sweep over nb sites; input in G0 (carry 0), G1 = 0 */
static void chain_sweep(E *G0, E *G1, int nb) {
  sweep_arg sa = { G0, G1, nb };
  int cb = nb < CHUNKBITS ? nb : CHUNKBITS;
  if (nb >= 4 + CHUNKBITS) pfor(sweep_low, &sa); else sweep_low(0, 1, &sa);
  for (int j = cb; j < nb; j++) { hi_arg h = { G0, G1, nb, j }; if (nb >= 16) pfor(sweep_hi, &h); else sweep_hi(0, 1, &h); }
}
typedef struct { E *G0, *G1; uint64_t n; } sum_arg;
static void sum_job(int t, int nt, void *vp) {
  sum_arg *a = vp; uint64_t per = a->n / nt, p0 = per * t, p1 = (t == nt - 1) ? a->n : per * (t + 1); int ov = 0;
  for (uint64_t i = p0; i < p1; i++) a->G0[i] = ADD(a->G0[i], a->G1[i], ov);
  if (ov) overflow_flag = 1;
}
typedef struct { const E *x; E *G0, *G1; int nb; int shift; } ld_arg;
static void load_job(int t, int nt, void *vp) {
  ld_arg *a = vp; uint64_t n = (uint64_t)1 << a->nb, per = n / nt, p0 = per * t, p1 = (t == nt - 1) ? n : per * (t + 1);
  for (uint64_t i = p0; i < p1; i++) { a->G0[i] = a->x[i << a->shift]; a->G1[i] = 0; }
}
typedef struct { E *y; const E *H0, *H1; int nb; } ad_arg;
static void add_job(int t, int nt, void *vp) {
  ad_arg *a = vp; uint64_t n = (uint64_t)1 << a->nb, per = n / nt, p0 = per * t, p1 = (t == nt - 1) ? n : per * (t + 1); int ov = 0;
  for (uint64_t i = p0; i < p1; i++) { E s = ADD(a->H0[i], a->H1[i], ov); a->y[i << 1] = ADD(a->y[i << 1], s, ov); }
  if (ov) overflow_flag = 1;
}
static E *W1 = 0;
/* y = T x ; x,y distinct arrays of N elements */
static void apply(const E *x, E *y) {
  if (!W1) { W1 = malloc(N * sizeof(E)); if (!W1) { fprintf(stderr, "oom\n"); exit(1); } }
  ld_arg l = { x, y, W1, m, 0 }; pfor(load_job, &l);
  chain_sweep(y, W1, m);
  sum_arg s = { y, W1, N }; pfor(sum_job, &s);
  if (P) {
    int nb = m - 2; uint64_t n2 = (uint64_t)1 << nb;
    E *H0 = W1, *H1 = W1 + n2;
    ld_arg l2 = { x, H0, H1, nb, 1 }; pfor(load_job, &l2);
    chain_sweep(H0, H1, nb);
    ad_arg ad = { y, H0, H1, nb }; pfor(add_job, &ad);
  }
}

#ifdef EXACT
static void pr128(E v) { char b[48]; int n = 0; if (!v) b[n++] = '0'; while (v) { b[n++] = '0' + (int)(v % 10); v /= 10; } while (n--) putchar(b[n]); }
/* 128x128 -> 256 */
static void mul128(E a, E b, E *hi, E *lo) {
  uint64_t a0 = (uint64_t)a, a1 = (uint64_t)(a >> 64), b0 = (uint64_t)b, b1 = (uint64_t)(b >> 64);
  E p00 = (E)a0 * b0, p01 = (E)a0 * b1, p10 = (E)a1 * b0, p11 = (E)a1 * b1;
  E mid = (p00 >> 64) + (uint64_t)p01 + (uint64_t)p10;
  *lo = (p00 & 0xFFFFFFFFFFFFFFFFULL) | (mid << 64);
  *hi = p11 + (p01 >> 64) + (p10 >> 64) + (mid >> 64);
}
static int gt256(E ah, E al, E bh, E bl) { return ah > bh || (ah == bh && al > bl); }
typedef struct { E *y, *x; uint64_t n; E ymax, xmax, ymin, xmin; int has; E xminall; } cw_arg;
static cw_arg cwa[64];
static void cw_job(int t, int nt, void *vp) {
  cw_arg *g = vp; uint64_t per = g->n / nt, p0 = per * t, p1 = (t == nt - 1) ? g->n : per * (t + 1);
  cw_arg *a = &cwa[t]; a->has = 0; a->xminall = ~(E)0;
  for (uint64_t i = p0; i < p1; i++) {
    E y = g->y[i], x = g->x[i];
    if (x < a->xminall) a->xminall = x;
    if (x == 0) continue;
    if (!a->has) { a->ymax = a->ymin = y; a->xmax = a->xmin = x; a->has = 1; continue; }
    E h1, l1, h2, l2;
    mul128(y, a->xmax, &h1, &l1); mul128(a->ymax, x, &h2, &l2);   /* y/x > ymax/xmax  <=>  y*xmax > ymax*x */
    if (gt256(h1, l1, h2, l2)) { a->ymax = y; a->xmax = x; }
    mul128(y, a->xmin, &h1, &l1); mul128(a->ymin, x, &h2, &l2);
    if (gt256(h2, l2, h1, l1)) { a->ymin = y; a->xmin = x; }
  }
}
typedef struct { E *v; uint64_t n; } vv_arg;
static E maxel(const E *v) { E mx = 0; for (uint64_t i = 0; i < N; i++) if (v[i] > mx) mx = v[i]; return mx; }
static int bitlen(E v) { int b = 0; while (v) { b++; v >>= 1; } return b; }
typedef struct { E *v; int sh; } sh_arg;
static void sh_job(int t, int nt, void *vp) {
  sh_arg *a = vp; uint64_t per = N / nt, p0 = per * t, p1 = (t == nt - 1) ? N : per * (t + 1);
  for (uint64_t i = p0; i < p1; i++) a->v[i] = a->sh >= 0 ? (a->v[i] >> a->sh) : (a->v[i] << (-a->sh));
}
static void rescale(E *v, int target_bits) { E mx = maxel(v); int sh = bitlen(mx) - target_bits; sh_arg a = { v, sh }; pfor(sh_job, &a); }
/* sum of squares with 32-bit limbs: c[k] (k=0..6) as u128, S = sum c[k] 2^(32k) */
typedef struct { const E *v; E c[64][7]; } sq_arg;
static sq_arg SQ;
static void sq_job(int t, int nt, void *vp) {
  sq_arg *g = vp; uint64_t per = N / nt, p0 = per * t, p1 = (t == nt - 1) ? N : per * (t + 1);
  E c[7] = {0, 0, 0, 0, 0, 0, 0};
  for (uint64_t i = p0; i < p1; i++) {
    E x = g->v[i]; uint64_t l[4] = { (uint32_t)x, (uint32_t)(x >> 32), (uint32_t)(x >> 64), (uint32_t)(x >> 96) };
    for (int a = 0; a < 4; a++) { c[2 * a] += (E)(l[a] * l[a]); for (int b = a + 1; b < 4; b++) c[a + b] += (E)2 * (l[a] * l[b]); }
  }
  for (int k = 0; k < 7; k++) g->c[t][k] = c[k];
}
static void sumsq(const E *v, E out[7]) {
  SQ.v = v; pfor(sq_job, &SQ);
  for (int k = 0; k < 7; k++) { out[k] = 0; for (int t = 0; t < NT; t++) out[k] += SQ.c[t][k]; }
}
static double e2d(E v) { return (double)v; }
#endif

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
  const char *mode = argv[1]; m = atoi(argv[2]); P = atoi(argv[3]); N = (uint64_t)1 << m;
  if (getenv("NTH")) NT = atoi(getenv("NTH"));
  if (!strcmp(mode, "dense")) {
#ifndef EXACT
    E *x = calloc(N, sizeof(E)), *y = calloc(N, sizeof(E));
    double *T = malloc(N * N * sizeof(double));
    for (uint64_t s = 0; s < N; s++) { memset(x, 0, N * sizeof(E)); x[s] = 1; apply(x, y); for (uint64_t t = 0; t < N; t++) T[s * N + t] = y[t]; }
    for (uint64_t s = 0; s < N; s++) { for (uint64_t t = 0; t < N; t++) printf("%d ", (int)T[s * N + t]); printf("\n"); }
#endif
    return 0;
  }
#ifdef EXACT
  if (!strcmp(mode, "count")) {
    int L = atoi(argv[4]);
    E *x = calloc(N, sizeof(E)), *y = calloc(N, sizeof(E)); x[0] = 1;
    for (int r = 0; r < L; r++) { apply(x, y); E *t = x; x = y; y = t; }
    pr128(x[0]); printf("\n"); if (overflow_flag) printf("OVERFLOW\n");
    return 0;
  }
  if (!strcmp(mode, "tracedense")) {
    int L = atoi(argv[4]);
    E tr = 0; E *x = calloc(N, sizeof(E)), *y = calloc(N, sizeof(E));
    for (uint64_t s = 0; s < N; s++) {
      memset(x, 0, N * sizeof(E)); x[s] = 1; E *a = x, *b = y;
      for (int r = 0; r < L; r++) { apply(a, b); E *t = a; a = b; b = t; }
      tr += a[s];
    }
    pr128(tr); printf("\n"); if (overflow_flag) printf("OVERFLOW\n");
    return 0;
  }
  if (!strcmp(mode, "cw")) {
    const char *fn = argv[4]; int refine = atoi(argv[5]); int SC = getenv("SC") ? atoi(getenv("SC")) : 80;
    double *d = malloc(N * sizeof(double)); FILE *f = fopen(fn, "rb"); if (!f || fread(d, sizeof(double), N, f) != N) { fprintf(stderr, "read fail\n"); return 1; } fclose(f);
    double mx = 0; for (uint64_t i = 0; i < N; i++) if (d[i] > mx) mx = d[i];
    E *x = malloc(N * sizeof(E)), *y = malloc(N * sizeof(E));
    for (uint64_t i = 0; i < N; i++) { double v = d[i] / mx; if (v < 0) { fprintf(stderr, "negative entry\n"); return 1; } x[i] = (E)ldexp(v, SC); }
    free(d);
    for (int r = 0; r < refine; r++) { apply(x, y); E *t = x; x = y; y = t; rescale(x, SC + 1); }
    apply(x, y);
    cw_arg g = { y, x, N };
    pfor(cw_job, &g);
    int has = 0; E ymax = 0, xmax = 1, ymin = 0, xmin = 1, xminall = ~(E)0;
    for (int t = 0; t < NT; t++) {
      cw_arg *a = &cwa[t]; if (a->xminall < xminall) xminall = a->xminall; if (!a->has) continue;
      if (!has) { ymax = a->ymax; xmax = a->xmax; ymin = a->ymin; xmin = a->xmin; has = 1; continue; }
      E h1, l1, h2, l2;
      mul128(a->ymax, xmax, &h1, &l1); mul128(ymax, a->xmax, &h2, &l2); if (gt256(h1, l1, h2, l2)) { ymax = a->ymax; xmax = a->xmax; }
      mul128(a->ymin, xmin, &h1, &l1); mul128(ymin, a->xmin, &h2, &l2); if (gt256(h2, l2, h1, l1)) { ymin = a->ymin; xmin = a->xmin; }
    }
    printf("CW m=%d P=%d refine=%d SC=%d\n", m, P, refine, SC);
    printf("min_x "); pr128(xminall); printf("\nupper_num "); pr128(ymax); printf("\nupper_den "); pr128(xmax);
    printf("\nlower_num "); pr128(ymin); printf("\nlower_den "); pr128(xmin);
    printf("\nratios %.17g %.17g\noverflow %d\n", e2d(ymax) / e2d(xmax), e2d(ymin) / e2d(xmin), (int)overflow_flag);
    if (getenv("VECOUT")) { FILE *o = fopen(getenv("VECOUT"), "wb"); fwrite(x, sizeof(E), N, o); fclose(o); }
    return 0;
  }
  if (!strcmp(mode, "hp")) {
    int iters = atoi(argv[4]); int SC = getenv("SC") ? atoi(getenv("SC")) : 84;
    E *x = malloc(N * sizeof(E)), *y = malloc(N * sizeof(E));
    if (argc > 5 && strcmp(argv[5], "-")) {
      FILE *f = fopen(argv[5], "rb"); if (!f) { fprintf(stderr, "no vecin\n"); return 1; }
      size_t got = fread(x, sizeof(E), N, f); if (got != N) { fprintf(stderr, "short vecin\n"); return 1; } fclose(f);
    } else { for (uint64_t i = 0; i < N; i++) x[i] = (E)1 << SC; }
    for (int it = 0; it < iters; it++) {
      apply(x, y);
      E sx[7], sy[7]; sumsq(x, sx); sumsq(y, sy);
      printf("IT %d XX", it); for (int k = 0; k < 7; k++) { printf(" "); pr128(sx[k]); }
      printf(" YY"); for (int k = 0; k < 7; k++) { printf(" "); pr128(sy[k]); }
      printf(" ovf %d\n", (int)overflow_flag); fflush(stdout);
      E *t = x; x = y; y = t; rescale(x, SC);
    }
    if (argc > 6) { FILE *o = fopen(argv[6], "wb"); fwrite(x, sizeof(E), N, o); fclose(o); }
    return 0;
  }
#else
  if (!strcmp(mode, "pow")) {
    int iters = atoi(argv[4]);
    E *x = malloc(N * sizeof(E)), *y = malloc(N * sizeof(E));
    for (uint64_t i = 0; i < N; i++) x[i] = 1.0;
    double lam = 0;
    for (int it = 0; it < iters; it++) {
      apply(x, y);
      double nx = 0, ny = 0, mx = 0; for (uint64_t i = 0; i < N; i++) { nx += x[i] * x[i]; ny += y[i] * y[i]; if (y[i] > mx) mx = y[i]; }
      lam = sqrt(ny / nx);
      double lmax = 0, lmin = 1e300; /* CW ratios (double) for monitoring */
      for (uint64_t i = 0; i < N; i++) { double r = y[i] / x[i]; if (r > lmax) lmax = r; if (r < lmin) lmin = r; }
      if (it % 5 == 4 || it == iters - 1) { printf("it %d lam %.16g cwmin %.16g cwmax %.16g\n", it, lam, lmin, lmax); fflush(stdout); }
      for (uint64_t i = 0; i < N; i++) x[i] = y[i] / mx;
      /* x is now normalised; next iterate */
    }
    FILE *o = fopen(argv[5], "wb"); fwrite(x, sizeof(E), N, o); fclose(o);
    return 0;
  }
#endif
  fprintf(stderr, "bad mode for this build\n");
  return 1;
}
