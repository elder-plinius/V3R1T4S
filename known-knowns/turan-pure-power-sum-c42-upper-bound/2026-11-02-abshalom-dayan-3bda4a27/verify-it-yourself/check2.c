/*
 * checker2.c : independent outward-rounded interval checker for the finite hypotheses
 * (HJB, INIT, TERM, Lipschitz) on the table V_b.npy.
 *
 * Rounding model: no fesetround.  Every + - * / sqrt result is widened by one ulp each way
 * (up1/dn1 are exact nextafter by bit manipulation); every libm result (sin cos exp) is widened
 * by 4 ulps each way.  Constants that are rationals are enclosed by [dn1(a/b), up1(a/b)].
 *
 * HJB: for each cell, branch and bound over the box (sigma,theta,rho,psi) where
 * tau = tau_i + d*sigma, phi = phi_j + dphi*theta (sigma,theta in [0,1]); the cell's bilinear V is
 * written in sigma,theta, so (tau,phi) stay tied to the cell function.  A box is accepted if
 * max( natural interval range lower end, mean value form lower end ) >= thr.  The mean value form
 * uses interval gradients from forward-mode automatic differentiation over intervals.
 * A box whose centre value has an upper end < thr is a certified violation (WITNESS FAIL).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

/* ---------------- directed padding ---------------- */
static inline double dn1(double x) {
  if (x != x || fabs(x) > 1e300) return x;
  if (x == 0.0) return -4.9406564584124654e-324;
  uint64_t u; memcpy(&u, &x, 8);
  if (x > 0) u--; else u++;
  memcpy(&x, &u, 8); return x;
}
static inline double up1(double x) {
  if (x != x || fabs(x) > 1e300) return x;
  if (x == 0.0) return 4.9406564584124654e-324;
  uint64_t u; memcpy(&u, &x, 8);
  if (x > 0) u++; else u--;
  memcpy(&x, &u, 8); return x;
}
static inline double dn4(double x) { return dn1(dn1(dn1(dn1(x)))); }
static inline double up4(double x) { return up1(up1(up1(up1(x)))); }

typedef struct { double lo, hi; } I;

static inline I mk(double a, double b) { I r = {a, b}; return r; }
static inline I pt(double a) { I r = {a, a}; return r; }
static inline I cdiv(double a, double b) { double q = a / b; I r = {dn1(q), up1(q)}; return r; }

static inline I iadd(I a, I b) { I r = {dn1(a.lo + b.lo), up1(a.hi + b.hi)}; return r; }
static inline I isub(I a, I b) { I r = {dn1(a.lo - b.hi), up1(a.hi - b.lo)}; return r; }
static inline I ineg(I a) { I r = {-a.hi, -a.lo}; return r; }
static inline I imul(I a, I b) {
  double p1 = a.lo * b.lo, p2 = a.lo * b.hi, p3 = a.hi * b.lo, p4 = a.hi * b.hi;
  double lo = p1 < p2 ? p1 : p2, hi = p1 > p2 ? p1 : p2;
  if (p3 < lo) lo = p3; if (p3 > hi) hi = p3;
  if (p4 < lo) lo = p4; if (p4 > hi) hi = p4;
  I r = {dn1(lo), up1(hi)}; return r;
}
static inline I idiv(I a, I b) {
  if (b.lo <= 0.0 && b.hi >= 0.0) { I r = {-INFINITY, INFINITY}; return r; }
  double p1 = a.lo / b.lo, p2 = a.lo / b.hi, p3 = a.hi / b.lo, p4 = a.hi / b.hi;
  double lo = p1 < p2 ? p1 : p2, hi = p1 > p2 ? p1 : p2;
  if (p3 < lo) lo = p3; if (p3 > hi) hi = p3;
  if (p4 < lo) lo = p4; if (p4 > hi) hi = p4;
  I r = {dn1(lo), up1(hi)}; return r;
}
static inline I isqr(I a) {
  I r;
  if (a.lo >= 0) { r.lo = dn1(a.lo * a.lo); r.hi = up1(a.hi * a.hi); }
  else if (a.hi <= 0) { r.lo = dn1(a.hi * a.hi); r.hi = up1(a.lo * a.lo); }
  else { double m = fmax(-a.lo, a.hi); r.lo = 0.0; r.hi = up1(m * m); }
  return r;
}
static inline I isqrt(I a) {
  I r;
  double lo = a.lo > 0 ? a.lo : 0.0;
  r.lo = dn4(sqrt(lo)); if (r.lo < 0) r.lo = 0;
  r.hi = up4(sqrt(a.hi > 0 ? a.hi : 0.0));
  return r;
}
static inline I iexp(I a) { I r = {dn4(exp(a.lo)), up4(exp(a.hi))}; if (r.lo < 0) r.lo = 0; return r; }

static I isin(I a) {
  if (!(a.hi - a.lo <= 6.0)) return mk(-1.0, 1.0);
  double s1 = sin(a.lo), s2 = sin(a.hi);
  I r = {dn4(fmin(s1, s2)), up4(fmax(s1, s2))};
  const double eps = 1e-9, tp = 2.0 * M_PI;
  double kc = floor(a.lo / tp);
  for (int m = -1; m <= 2; m++) {
    double pmax = M_PI_2 + tp * (kc + m), pmin = -M_PI_2 + tp * (kc + m);
    if (pmax >= a.lo - eps && pmax <= a.hi + eps) r.hi = 1.0;
    if (pmin >= a.lo - eps && pmin <= a.hi + eps) r.lo = -1.0;
  }
  if (r.lo < -1.0) r.lo = -1.0;
  if (r.hi > 1.0) r.hi = 1.0;
  return r;
}
static I icos(I a) {
  if (!(a.hi - a.lo <= 6.0)) return mk(-1.0, 1.0);
  double s1 = cos(a.lo), s2 = cos(a.hi);
  I r = {dn4(fmin(s1, s2)), up4(fmax(s1, s2))};
  const double eps = 1e-9, tp = 2.0 * M_PI;
  double kc = floor(a.lo / tp);
  for (int m = -1; m <= 2; m++) {
    double pmax = tp * (kc + m), pmin = M_PI + tp * (kc + m);
    if (pmax >= a.lo - eps && pmax <= a.hi + eps) r.hi = 1.0;
    if (pmin >= a.lo - eps && pmin <= a.hi + eps) r.lo = -1.0;
  }
  if (r.lo < -1.0) r.lo = -1.0;
  if (r.hi > 1.0) r.hi = 1.0;
  return r;
}

/* ---------------- jets: value + up to 4 partial derivatives (all intervals) ---------------- */
typedef struct { I v; I g[4]; unsigned m; } J; /* m: bit k set <=> g[k] may be nonzero */

static inline J jc(I v) { J r; r.v = v; r.m = 0; return r; }
static inline J jvar(int k, I v, int withgrad) {
  J r; r.v = v; r.m = 0;
  if (withgrad) { r.m = 1u << k; r.g[k] = pt(1.0); }
  return r;
}
static inline J jadd(J a, J b) {
  J r; r.v = iadd(a.v, b.v); r.m = a.m | b.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) {
    int ia = a.m >> k & 1, ib = b.m >> k & 1;
    r.g[k] = ia && ib ? iadd(a.g[k], b.g[k]) : ia ? a.g[k] : b.g[k];
  }
  return r;
}
static inline J jneg(J a) {
  J r; r.v = ineg(a.v); r.m = a.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) r.g[k] = ineg(a.g[k]);
  return r;
}
static inline J jsub(J a, J b) {
  J r; r.v = isub(a.v, b.v); r.m = a.m | b.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) {
    int ia = a.m >> k & 1, ib = b.m >> k & 1;
    r.g[k] = ia && ib ? isub(a.g[k], b.g[k]) : ia ? a.g[k] : ineg(b.g[k]);
  }
  return r;
}
static inline J jmul(J a, J b) {
  J r; r.v = imul(a.v, b.v); r.m = a.m | b.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) {
    int ia = a.m >> k & 1, ib = b.m >> k & 1;
    if (ia && ib) r.g[k] = iadd(imul(a.v, b.g[k]), imul(b.v, a.g[k]));
    else if (ia) r.g[k] = imul(b.v, a.g[k]);
    else r.g[k] = imul(a.v, b.g[k]);
  }
  return r;
}
static inline J jdiv(J a, J b) { /* q = a/b ; g = (ga - q gb)/b */
  J r; I q = idiv(a.v, b.v); r.v = q; r.m = a.m | b.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) {
    int ia = a.m >> k & 1, ib = b.m >> k & 1;
    I num = ia && ib ? isub(a.g[k], imul(q, b.g[k])) : ia ? a.g[k] : ineg(imul(q, b.g[k]));
    r.g[k] = idiv(num, b.v);
  }
  return r;
}
static inline J jsqr(J a) {
  J r; r.v = isqr(a.v); r.m = a.m;
  I two_v = imul(pt(2.0), a.v);
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) r.g[k] = imul(two_v, a.g[k]);
  return r;
}
static inline J jsqrt(J a) {
  J r; r.v = isqrt(a.v); r.m = a.m;
  I den = imul(pt(2.0), r.v);
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) r.g[k] = idiv(a.g[k], den);
  return r;
}
static inline J jexp(J a) {
  J r; r.v = iexp(a.v); r.m = a.m;
  for (int k = 0; k < 4; k++) if (r.m >> k & 1) r.g[k] = imul(r.v, a.g[k]);
  return r;
}
static inline void jsincos(J a, J *s, J *c) {
  s->v = isin(a.v); c->v = icos(a.v); s->m = c->m = a.m;
  for (int k = 0; k < 4; k++) if (a.m >> k & 1) {
    s->g[k] = imul(c->v, a.g[k]);
    c->g[k] = ineg(imul(s->v, a.g[k]));
  }
}

/* ---------------- constants ---------------- */
static I C_T, C_085, C_A, C_B, C_L1, C_AL, C_PI, C_2PI, C_INV200, C_K2PI, C_INVDPHI;
static I C_RM, C_RP, C_086, C_L0;
static J J_T, J_085, J_A, J_B, J_L1, J_AL, J_INV200, J_K2PI, J_INVDPHI, J_2, J_200, J_L0, J_05, J_086;

static void init_consts(void) {
  C_T = cdiv(501.0, 1000.0);
  C_085 = cdiv(85.0, 100.0);
  C_086 = cdiv(866.0, 1000.0);
  C_A = cdiv(7361.0, 10000.0); /* Re(gamma beta) = 0.866*0.85 */
  C_B = cdiv(425.0, 1000.0);   /* -Im(gamma beta) = 0.5*0.85  */
  C_L1 = pt(10.0);
  C_L0 = pt(5.0);
  C_AL = cdiv(6.0, 5.0);
  /* pi: M_PI < pi < nextafter(M_PI), widen by 2 ulps for margin */
  C_PI = mk(dn1(dn1(M_PI)), up1(up1(M_PI)));
  C_2PI = imul(pt(2.0), C_PI);
  C_INV200 = cdiv(1.0, 200.0);
  C_K2PI = idiv(C_2PI, pt(2514.0));
  C_INVDPHI = idiv(pt(2514.0), C_2PI);
  I s2 = isqrt(pt(2.0));
  I r0 = idiv(pt(1.0), s2);
  I bb = cdiv(35.0, 10000.0);
  C_RM = isub(r0, bb);
  C_RP = iadd(r0, bb);
  J_T = jc(C_T); J_085 = jc(C_085); J_A = jc(C_A); J_B = jc(C_B); J_L1 = jc(C_L1); J_AL = jc(C_AL);
  J_INV200 = jc(C_INV200); J_K2PI = jc(C_K2PI); J_INVDPHI = jc(C_INVDPHI);
  J_2 = jc(pt(2.0)); J_200 = jc(pt(200.0)); J_L0 = jc(C_L0); J_05 = jc(cdiv(1.0, 2.0)); J_086 = jc(C_086);
}

/* ---------------- table ---------------- */
#define NT 1600
#define NTH 2514
static double *V;           /* (NT+1) x NTH */
#define VV(i, j) V[(size_t)(i) * NTH + (j)]

typedef struct { I a, bs, ct, dd; int i, j; } Cell;

static void make_cell(Cell *c, int i, int j) {
  int j1 = (j + 1) % NTH;
  double v00 = VV(i, j), v10 = VV(i + 1, j), v01 = VV(i, j1), v11 = VV(i + 1, j1);
  c->i = i; c->j = j;
  c->a = pt(v00);
  c->bs = isub(pt(v10), pt(v00));
  c->ct = isub(pt(v01), pt(v00));
  c->dd = iadd(isub(isub(pt(v11), pt(v10)), pt(v01)), pt(v00));
}

/* G over the cell as a jet in (sigma=0, theta=1, rho=2, psi=3) */
static J Gfun(J sg, J th, J rho, J psi, const Cell *c) {
  J sp, cp, sph, cph;
  jsincos(psi, &sp, &cp);
  J tsp = jmul(J_T, sp);
  J re = jsub(rho, jmul(J_T, cp));
  J W = jsqrt(jadd(jsqr(re), jsqr(tsp)));
  J u = jneg(jdiv(tsp, rho));
  J tau = jmul(jadd(sg, jc(pt((double)(c->i - NT)))), J_INV200);
  J x = jexp(tau);
  J p = jmul(J_L1, jexp(jmul(J_AL, tau)));
  J phi = jmul(jadd(th, jc(pt((double)c->j))), J_K2PI);
  jsincos(phi, &sph, &cph);
  J A = jc(c->a), BS = jc(c->bs), CT = jc(c->ct), DD = jc(c->dd);
  J sgth = jmul(sg, th);
  J Vv = jadd(jadd(A, jmul(BS, sg)), jadd(jmul(CT, th), jmul(DD, sgth)));
  J Vtau = jmul(jadd(BS, jmul(DD, th)), J_200);
  J Vphi = jmul(jadd(CT, jmul(DD, sg)), J_INVDPHI);
  J xr = jmul(x, rho);
  J im = jneg(jadd(tsp, jmul(J_085, xr)));
  J N = jsqrt(jadd(jsqr(re), jsqr(im)));
  J e = jdiv(jsqr(jsub(W, jsqr(rho))), jmul(J_2, rho));
  J ph = jadd(jmul(J_A, cph), jmul(J_B, sph));
  J E = jadd(jadd(jneg(jmul(J_T, N)), jmul(jmul(J_2, xr), ph)), jmul(p, e));
  return jadd(jadd(jadd(Vtau, jmul(u, Vphi)), jmul(W, Vv)), E);
}

/* plain double version for sampling / cross-check (not rigorous) */
static double Gpt(double s, double t, double rho, double psi, const Cell *c) {
  double a = c->a.lo, bs = c->bs.lo, ct = c->ct.lo, dd = c->dd.lo;
  double tau = (c->i - NT + s) / 200.0, x = exp(tau), p = 10.0 * pow(x, 1.2);
  double phi = (c->j + t) * (2.0 * M_PI / NTH);
  double T = 0.501;
  double wr = rho - T * cos(psi), wi = -T * sin(psi);
  double W = hypot(wr, wi);
  double Vv = a + bs * s + ct * t + dd * s * t;
  double Vtau = (bs + dd * t) * 200.0, Vphi = (ct + dd * s) / (2.0 * M_PI / NTH);
  double e = (W - rho * rho) * (W - rho * rho) / (2 * rho);
  double N = hypot(wr, wi - 0.85 * x * rho);
  /* Re(gamma*beta*e^{i phi}) with gamma=0.5+0.866i, beta=-0.85i computed with complex arithmetic */
  double gr = 0.5, gi = 0.866, br = 0.0, bi = -0.85;
  double gbr = gr * br - gi * bi, gbi = gr * bi + gi * br;
  double re_gb = gbr * cos(phi) - gbi * sin(phi);
  return Vtau + (wi / rho) * Vphi + W * Vv - T * N + 2 * rho * x * re_gb + p * e;
}

/* ---------------- branch and bound for one cell ---------------- */
typedef struct { double lo[4], hi[4]; int depth; } Box;

typedef struct {
  int status;            /* 0 pass, 1 witness fail, 2 unresolved */
  double minlb;          /* min over accepted leaves of certified lower bound */
  long boxes; double minctr;
  Box failbox; double failbound; double witnessG_hi, witness_pt[4];
} CellRes;

static double THR = 1e-6; /* main() replaces the default by up1(1e-6) so that lb >= THR implies lb > 10^-6 exactly */
static long MAXBOXES = 300000;
static int MAXDEPTH = 64;

static void eval_box(const Box *b, const Cell *c, double *lb, double *vc_hi, int *split_dim, double *center) {
  J v[4];
  for (int k = 0; k < 4; k++) v[k] = jvar(k, mk(b->lo[k], b->hi[k]), 1);
  J g = Gfun(v[0], v[1], v[2], v[3], c);
  double h[4], ctr[4];
  for (int k = 0; k < 4; k++) {
    ctr[k] = 0.5 * (b->lo[k] + b->hi[k]);
    if (ctr[k] < b->lo[k]) ctr[k] = b->lo[k];
    if (ctr[k] > b->hi[k]) ctr[k] = b->hi[k];
    h[k] = up1(fmax(b->hi[k] - ctr[k], ctr[k] - b->lo[k]));
    center[k] = ctr[k];
  }
  J vcen[4];
  for (int k = 0; k < 4; k++) vcen[k] = jvar(k, pt(ctr[k]), 0);
  J gc = Gfun(vcen[0], vcen[1], vcen[2], vcen[3], c);
  double s = 0.0, best = -1.0; int bd = 0;
  for (int k = 0; k < 4; k++) {
    double gm = 0.0;
    if (g.m >> k & 1) { double a1 = fabs(g.g[k].lo), a2 = fabs(g.g[k].hi); gm = (a1 != a1 || a2 != a2) ? INFINITY : fmax(a1, a2); }
    double term = up1(gm * h[k]);
    s = up1(s + term);
    if (term > best) { best = term; bd = k; }
  }
  double mv = dn1(gc.v.lo - s);
  *lb = mv > g.v.lo ? mv : g.v.lo;
  *vc_hi = gc.v.hi;
  *split_dim = bd;
}

static void check_cell(int i, int j, CellRes *R) {
  Cell c; make_cell(&c, i, j);
  static Box stack[1024];
  int sp = 0;
  Box b0;
  b0.lo[0] = 0; b0.hi[0] = 1; b0.lo[1] = 0; b0.hi[1] = 1;
  b0.lo[2] = C_RM.lo; b0.hi[2] = C_RP.hi;
  b0.lo[3] = 0.0; b0.hi[3] = C_2PI.hi; b0.depth = 0;
  stack[sp++] = b0;
  R->status = 0; R->minlb = INFINITY; R->boxes = 0; R->failbound = INFINITY; R->minctr = INFINITY;
  while (sp > 0) {
    Box b = stack[--sp];
    double lb, vch, ctr[4]; int sd;
    eval_box(&b, &c, &lb, &vch, &sd, ctr);
    R->boxes++;
    if (vch < R->minctr) R->minctr = vch;
    if (vch < THR) { /* certified violation at the centre point */
      R->status = 1; R->failbox = b; R->failbound = lb; R->witnessG_hi = vch;
      for (int k = 0; k < 4; k++) R->witness_pt[k] = ctr[k];
      return;
    }
    if (lb >= THR) { if (lb < R->minlb) R->minlb = lb; continue; }
    if (b.depth >= MAXDEPTH || R->boxes >= MAXBOXES) {
      if (R->status == 0 || lb < R->failbound) { R->failbox = b; R->failbound = lb; }
      R->status = 2;
      if (R->boxes >= MAXBOXES) return;
      continue;
    }
    /* bisect along sd (if the box in that dim is degenerate, fall to the widest relative dim) */
    double mid = ctr[sd];
    if (!(mid > b.lo[sd] && mid < b.hi[sd])) {
      R->status = 2; if (lb < R->failbound) { R->failbox = b; R->failbound = lb; }
      continue;
    }
    Box l = b, r = b;
    l.hi[sd] = mid; r.lo[sd] = mid; l.depth = r.depth = b.depth + 1;
    if (sp + 2 > 1023) { R->status = 2; R->failbox = b; R->failbound = lb; return; }
    stack[sp++] = r; stack[sp++] = l;
  }
}

/* float sampling of the cell minimum (not rigorous) */
static double sample_cell_min(const Cell *c, double *arg) {
  double best = INFINITY;
  double rm = C_RM.lo, rp = C_RP.hi;
  for (int a = 0; a < 3; a++) for (int bb = 0; bb < 3; bb++) {
    double s = a * 0.5, t = bb * 0.5;
    for (int ir = 0; ir <= 12; ir++) {
      double rho = rm + (rp - rm) * ir / 12.0;
      for (int ip = 0; ip < 4000; ip++) {
        double psi = 2.0 * M_PI * ip / 4000.0;
        double g = Gpt(s, t, rho, psi, c);
        if (g < best) { best = g; if (arg) { arg[0] = s; arg[1] = t; arg[2] = rho; arg[3] = psi; } }
      }
    }
  }
  return best;
}

static double refine_min(const Cell *c, double *x0) {
  double lo[4] = {0, 0, C_RM.lo, 0}, hi[4] = {1, 1, C_RP.hi, 2.0 * M_PI};
  double x[4]; memcpy(x, x0, sizeof x);
  double f = Gpt(x[0], x[1], x[2], x[3], c);
  double step[4] = {0.05, 0.05, 5e-4, 1e-3};
  for (int it = 0; it < 4000; it++) {
    int improved = 0;
    for (int k = 0; k < 4; k++) for (int sgn = -1; sgn <= 1; sgn += 2) {
      double y[4]; memcpy(y, x, sizeof y);
      y[k] += sgn * step[k]; if (y[k] < lo[k]) y[k] = lo[k]; if (y[k] > hi[k]) y[k] = hi[k];
      double fy = Gpt(y[0], y[1], y[2], y[3], c);
      if (fy < f) { f = fy; memcpy(x, y, sizeof y); improved = 1; }
    }
    if (!improved) { int tiny = 1; for (int k = 0; k < 4; k++) { step[k] *= 0.5; if (step[k] > 1e-12) tiny = 0; } if (tiny) break; }
  }
  memcpy(x0, x, sizeof x);
  return f;
}

/* ---------------- TERM : min over rho in [rho-,rho+], psi in [pi,2pi] ---------------- */
static J term_fun(J rho, J psi) {
  J sp, cp; jsincos(psi, &sp, &cp);
  J tsp = jmul(J_T, sp), tcp = jmul(J_T, cp);
  J re = jsub(rho, tcp);
  J W = jsqrt(jadd(jsqr(re), jsqr(tsp)));
  J e = jdiv(jsqr(jsub(W, jsqr(rho))), jmul(J_2, rho));
  /* Re(gamma (T e^{i psi} - beta rho)) = 0.5*T cos psi - 0.866*(T sin psi + 0.85 rho) */
  J t1 = jmul(J_05, tcp);
  J t2 = jmul(J_086, jadd(tsp, jmul(J_085, rho)));
  return jadd(jsub(t1, t2), jmul(J_L0, e));
}

static double term_min_lb(double *ub_out, long *nb) {
  Box st[1024]; int sp = 0;
  Box b0; b0.lo[2] = C_RM.lo; b0.hi[2] = C_RP.hi; b0.lo[3] = C_PI.lo; b0.hi[3] = C_2PI.hi; b0.depth = 0;
  b0.lo[0] = b0.hi[0] = b0.lo[1] = b0.hi[1] = 0;
  st[sp++] = b0;
  double ubest = INFINITY, L = INFINITY; long n = 0;
  /* seed the incumbent with rigorous point evaluations (upper ends) on a grid inside the box */
  for (int ir = 0; ir <= 100; ir++) for (int ip = 0; ip <= 1000; ip++) {
    double rr_ = b0.lo[2] + (b0.hi[2] - b0.lo[2]) * ir / 100.0, pp_ = b0.lo[3] + (b0.hi[3] - b0.lo[3]) * ip / 1000.0;
    J gg = term_fun(jvar(2, pt(rr_), 0), jvar(3, pt(pp_), 0));
    if (gg.v.hi < ubest) ubest = gg.v.hi;
  }
  while (sp > 0) {
    Box b = st[--sp]; n++;
    if ((n & 0xFFFFF) == 0) { fprintf(stderr, "TERM progress n=%ld sp=%d ubest=%.12g L=%.12g box rho[%.9g,%.9g] psi[%.9g,%.9g]\n", n, sp, ubest, L, b.lo[2], b.hi[2], b.lo[3], b.hi[3]); }
    J r = jvar(2, mk(b.lo[2], b.hi[2]), 1), p = jvar(3, mk(b.lo[3], b.hi[3]), 1);
    J g = term_fun(r, p);
    double ctr[4], h[4];
    for (int k = 2; k < 4; k++) {
      ctr[k] = 0.5 * (b.lo[k] + b.hi[k]);
      h[k] = up1(fmax(b.hi[k] - ctr[k], ctr[k] - b.lo[k]));
    }
    J gc = term_fun(jvar(2, pt(ctr[2]), 0), jvar(3, pt(ctr[3]), 0));
    if (gc.v.hi < ubest) ubest = gc.v.hi;
    double s = 0, best = -1; int bd = 2;
    for (int k = 2; k < 4; k++) {
      double a1 = fabs(g.g[k].lo), a2 = fabs(g.g[k].hi); double gm = (a1 != a1 || a2 != a2) ? INFINITY : fmax(a1, a2);
      double term = up1(gm * h[k]); s = up1(s + term);
      if (term > best) { best = term; bd = k; }
    }
    double lb = fmax(dn1(gc.v.lo - s), g.v.lo);
    int small = (b.hi[2] - b.lo[2] < 1e-10) || (b.hi[3] - b.lo[3] < 1e-10);
    if (lb >= ubest - 1e-9 || small || b.depth >= 80) { if (lb < L) L = lb; continue; }
    double mid = ctr[bd];
    Box l = b, rr = b; l.hi[bd] = mid; rr.lo[bd] = mid; l.depth = rr.depth = b.depth + 1;
    st[sp++] = rr; st[sp++] = l;
  }
  *ub_out = ubest; *nb = n;
  return L;
}

/* ---------------- file loading ---------------- */
static int load_npy(const char *path) {
  FILE *f = fopen(path, "rb");
  if (!f) { fprintf(stderr, "cannot open %s\n", path); return 1; }
  unsigned char hd[12];
  if (fread(hd, 1, 10, f) != 10 || memcmp(hd, "\x93NUMPY", 6) != 0) { fprintf(stderr, "bad npy magic\n"); return 1; }
  size_t hlen = hd[8] | (hd[9] << 8), off = 10;
  if (hd[6] != 1) { fprintf(stderr, "npy version %d unsupported\n", hd[6]); return 1; }
  char *hs = calloc(hlen + 1, 1);
  if (fread(hs, 1, hlen, f) != hlen) return 1;
  if (!strstr(hs, "'<f8'") || !strstr(hs, "'fortran_order': False") || !strstr(hs, "(1601, 2514)")) {
    fprintf(stderr, "npy header unexpected: %s\n", hs); return 1;
  }
  size_t n = (size_t)(NT + 1) * NTH;
  V = malloc(n * sizeof(double));
  if (fread(V, sizeof(double), n, f) != n) { fprintf(stderr, "short read\n"); return 1; }
  fclose(f); (void)off;
  return 0;
}

static double json_num(const char *s, const char *key) {
  char pat[64]; snprintf(pat, sizeof pat, "\"%s\":", key);
  const char *p = strstr(s, pat);
  if (!p) return NAN;
  return strtod(p + strlen(pat), NULL);
}
static int check_json(const char *path) {
  FILE *f = fopen(path, "rb"); if (!f) return 1;
  char buf[4096]; size_t n = fread(buf, 1, sizeof buf - 1, f); buf[n] = 0; fclose(f);
  struct { const char *k; double v; } exp_[] = {{"T", 0.501}, {"b", 0.0035}, {"beta_im", -0.85}, {"gamma_re", 0.5},
    {"gamma_im", 0.866}, {"L0", 5.0}, {"L1", 10.0}, {"al", 1.2}, {"L", 8.0}, {"nt", 1600}, {"nth", 2514}};
  int bad = 0;
  for (size_t k = 0; k < sizeof exp_ / sizeof exp_[0]; k++) {
    double v = json_num(buf, exp_[k].k);
    if (!(fabs(v - exp_[k].v) < 1e-12)) { printf("JSON MISMATCH %s: json %.17g vs coded %.17g\n", exp_[k].k, v, exp_[k].v); bad = 1; }
  }
  printf("json parameters %s the coded statement parameters\n", bad ? "DISAGREE with" : "agree with");
  return bad;
}


/* ---------------- self test: primitives and jets against point evaluation ---------------- */
static int selftest(int N) {
  srand48(20261031);
  long bad = 0, trials = 0;
  /* primitives */
  for (int n = 0; n < 200000; n++) {
    double a = (drand48() * 16 - 4), w = pow(10.0, -6.0 * drand48()) * (drand48() < 0.1 ? 8 : 1);
    I x = mk(a, a + w);
    I sn = isin(x), cs = icos(x), ex = iexp(x);
    I sq = isqr(x), sr = isqrt(mk(fabs(a), fabs(a) + w));
    for (int q = 0; q < 12; q++) {
      double z = x.lo + (x.hi - x.lo) * (q == 0 ? 0.0 : q == 1 ? 1.0 : drand48());
      long double sl = sinl((long double)z), cl = cosl((long double)z), el = expl((long double)z), ql = (long double)z * z;
      trials += 4;
      if (sl < sn.lo || sl > sn.hi) { bad++; printf("sin enclosure fail x=[%.17g,%.17g] z=%.17g\n", x.lo, x.hi, z); }
      if (cl < cs.lo || cl > cs.hi) { bad++; printf("cos enclosure fail x=[%.17g,%.17g] z=%.17g\n", x.lo, x.hi, z); }
      if (el < ex.lo || el > ex.hi) { bad++; printf("exp enclosure fail\n"); }
      if (ql < sq.lo || ql > sq.hi) { bad++; printf("sqr enclosure fail\n"); }
    }
    /* sqrt, mul, div */
    I y = mk(fabs(a) + 0.5, fabs(a) + 0.5 + w);
    I mu = imul(x, y), dv = idiv(x, y), su = isub(x, y), ad = iadd(x, y);
    for (int q = 0; q < 6; q++) {
      double z1 = x.lo + (x.hi - x.lo) * drand48(), z2 = y.lo + (y.hi - y.lo) * drand48();
      long double m = (long double)z1 * z2, d = (long double)z1 / z2, sb = (long double)z1 - z2, sa = (long double)z1 + z2;
      long double rt = sqrtl((long double)z2);
      I yr = isqrt(y);
      trials += 5;
      if (m < mu.lo || m > mu.hi) { bad++; printf("mul fail\n"); }
      if (d < dv.lo || d > dv.hi) { bad++; printf("div fail\n"); }
      if (sb < su.lo || sb > su.hi) { bad++; printf("sub fail\n"); }
      if (sa < ad.lo || sa > ad.hi) { bad++; printf("add fail\n"); }
      if (rt < yr.lo || rt > yr.hi) { bad++; printf("sqrt fail\n"); }
    }
  }
  printf("selftest primitives: trials %ld, enclosure failures %ld\n", trials, bad);
  /* G jets on random boxes */
  long gb = 0, gt = 0, gfd = 0;
  for (int n = 0; n < N; n++) {
    int i = lrand48() % NT, j = lrand48() % NTH; Cell c; make_cell(&c, i, j);
    Box b; double ranges_lo[4] = {0, 0, C_RM.lo, 0}, ranges_hi[4] = {1, 1, C_RP.hi, C_2PI.hi};
    for (int k = 0; k < 4; k++) {
      double R = ranges_hi[k] - ranges_lo[k], w = R * pow(10.0, -3.5 * drand48());
      if (drand48() < 0.15) w = R;
      b.lo[k] = ranges_lo[k] + (R - w) * drand48(); b.hi[k] = b.lo[k] + w;
      if (b.hi[k] > ranges_hi[k]) b.hi[k] = ranges_hi[k];
    }
    double lb, vch, ctr[4]; int sd;
    eval_box(&b, &c, &lb, &vch, &sd, ctr);
    J v[4]; for (int k = 0; k < 4; k++) v[k] = jvar(k, mk(b.lo[k], b.hi[k]), 1);
    J g = Gfun(v[0], v[1], v[2], v[3], &c);
    for (int q = 0; q < 60; q++) {
      double z[4]; for (int k = 0; k < 4; k++) z[k] = b.lo[k] + (b.hi[k] - b.lo[k]) * drand48();
      double gp = Gpt(z[0], z[1], z[2], z[3], &c);
      gt++;
      if (gp < lb - 1e-11 || gp < g.v.lo - 1e-11 || gp > g.v.hi + 1e-11) { gb++; printf("G enclosure/bound fail cell (%d,%d) gp=%.12g lb=%.12g range [%.12g,%.12g]\n", i, j, gp, lb, g.v.lo, g.v.hi); }
      if (gp > vch + 1e-11 && b.hi[0] - b.lo[0] < 0) { }
      for (int k = 0; k < 4; k++) {
        double hh = 1e-6, zp[4], zm[4]; memcpy(zp, z, sizeof z); memcpy(zm, z, sizeof z);
        zp[k] += hh; zm[k] -= hh;
        double fd = (Gpt(zp[0], zp[1], zp[2], zp[3], &c) - Gpt(zm[0], zm[1], zm[2], zm[3], &c)) / (2 * hh);
        double glo = (g.m >> k & 1) ? g.g[k].lo : 0, ghi = (g.m >> k & 1) ? g.g[k].hi : 0;
        double tol = 1e-4 * (1 + fabs(fd));
        if (fd < glo - tol || fd > ghi + tol) { gfd++; if (gfd < 10) printf("gradient fail cell(%d,%d) dim %d fd %.9g jet [%.9g,%.9g]\n", i, j, k, fd, glo, ghi); }
      }
    }
  }
  printf("selftest G jets: %ld sampled points, bound/range failures %ld, finite-difference gradient failures %ld\n", gt, gb, gfd);
  return (int)(bad + gb + gfd);
}

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

int main(int argc, char **argv) {
  const char *npy = "../V_b.npy", *json = "../V_b.json", *logp = NULL;
  int topk_report = 0, thr_given = 0, rstride = 1, cend = NTH, dobisect = 0, selftestN = 0, r0 = 0, r1 = NT, cstride = 1, cstart = 0, perturb = 0, pi_ = 0, pj_ = 0, dosample = 0, synth = 0, skipglobal = 0;
  double pdelta = 0, sK0 = 0, sK1 = 0;
  for (int a = 1; a < argc; a++) {
    if (!strcmp(argv[a], "--rows")) { r0 = atoi(argv[++a]); r1 = atoi(argv[++a]); }
    else if (!strcmp(argv[a], "--colstride")) cstride = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--rowstride")) rstride = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--colstart")) cstart = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--colend")) cend = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--thr")) { THR = strtod(argv[++a], NULL); thr_given = 1; }
    else if (!strcmp(argv[a], "--perturb")) { perturb = 1; pi_ = atoi(argv[++a]); pj_ = atoi(argv[++a]); pdelta = strtod(argv[++a], NULL); }
    else if (!strcmp(argv[a], "--synth")) { synth = atoi(argv[++a]); sK0 = strtod(argv[++a], NULL); sK1 = strtod(argv[++a], NULL); }
    else if (!strcmp(argv[a], "--sample")) dosample = 1;
    else if (!strcmp(argv[a], "--log")) logp = argv[++a];
    else if (!strcmp(argv[a], "--maxboxes")) MAXBOXES = atol(argv[++a]);
    else if (!strcmp(argv[a], "--maxdepth")) MAXDEPTH = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--skipglobal")) skipglobal = 1;
    else if (!strcmp(argv[a], "--bisect")) dobisect = 1;
    else if (!strcmp(argv[a], "--topk")) topk_report = 1;
    else if (!strcmp(argv[a], "--selftest")) selftestN = atoi(argv[++a]);
    else if (!strcmp(argv[a], "--npy")) npy = argv[++a];
    else if (!strcmp(argv[a], "--json")) json = argv[++a];
    else { fprintf(stderr, "unknown option %s\n", argv[a]); return 2; }
  }
  init_consts();
  if (!thr_given) THR = up1(1e-6);
  FILE *lf = logp ? fopen(logp, "a") : NULL;
  double t0 = now();
  if (synth) {
    V = malloc((size_t)(NT + 1) * NTH * sizeof(double));
    for (int i = 0; i <= NT; i++) for (int j = 0; j < NTH; j++) {
      double tau = -8.0 + i / 200.0;
      /* synth 1: constant K0 ; synth 2: K0 + K1*tau (exactly bilinear) ; synth 3: K0 + K1*sin(phi) (not bilinear: table samples) */
      double phi = j * (2.0 * M_PI / NTH);
      VV(i, j) = synth == 1 ? sK0 : synth == 2 ? sK0 + sK1 * tau : sK0 + sK1 * sin(phi);
    }
    printf("SYNTHETIC table mode %d K0=%.17g K1=%.17g\n", synth, sK0, sK1);
  } else {
    if (load_npy(npy)) return 1;
    check_json(json);
  }
  if (perturb) { VV(pi_, pj_) += pdelta; printf("PERTURBED in memory: V[%d][%d] += %.17g -> %.17g\n", pi_, pj_, pdelta, VV(pi_, pj_)); }
  printf("constants: rho_minus=[%.17g, %.17g] rho_plus=[%.17g, %.17g] pi=[%.17g, %.17g] thr=%.3g\n", C_RM.lo, C_RM.hi, C_RP.lo, C_RP.hi, C_PI.lo, C_PI.hi, THR);

  if (selftestN > 0) { int f = selftest(selftestN); printf("SELFTEST %s\n", f ? "FAILED" : "PASSED"); return f ? 3 : 0; }
  if (!skipglobal) {
    /* INIT : V(tau_0, phi_j) >= T + (T+2)|beta| e^{-L} for all j */
    I rhs = iadd(C_T, imul(imul(iadd(C_T, pt(2.0)), C_085), iexp(pt(-8.0))));
    double vmin = INFINITY; int jmin = -1;
    for (int j = 0; j < NTH; j++) if (VV(0, j) < vmin) { vmin = VV(0, j); jmin = j; }
    double slack = dn1(vmin - rhs.hi);
    printf("INIT: rhs in [%.17g, %.17g]; min_j V[0][j]=%.17g at j=%d; INIT slack (lower bound of min V - rhs) = %.17g -> %s\n",
           rhs.lo, rhs.hi, vmin, jmin, slack, slack >= 0 ? "PASS" : "FAIL");
    /* TERM */
    double ub; long nb;
    double L = term_min_lb(&ub, &nb);
    double v00 = VV(NT, 0);
    double mcert = dn1(L - v00);
    printf("TERM: min f lower bound=%.17g (float-centre upper bound of min=%.17g, boxes=%ld); V[nt][0]=%.17g; m_cert=%.17g -> %s (needs > 0.0098)\n",
           L, ub, nb, v00, mcert, mcert > 0.0098 ? "PASS" : "FAIL");
    /* Lipschitz : V_tau = ((v10-v00)(1-t) + (v11-v01) t)/d  -> max abs at t=0 or 1 (linear in t); V_phi analogous */
    double mt = 0, mp = 0;
    for (int i = 0; i < NT; i++) for (int j = 0; j < NTH; j++) {
      int j1 = (j + 1) % NTH;
      double v00_ = VV(i, j), v10 = VV(i + 1, j), v01 = VV(i, j1), v11 = VV(i + 1, j1);
      double dt0 = fabs(v10 - v00_), dt1 = fabs(v11 - v01);
      double dp0 = fabs(v01 - v00_), dp1 = fabs(v11 - v10);
      /* differences of binary64 numbers are rounded: widen */
      double a1 = up1(fmax(dt0, dt1)), a2 = up1(fmax(dp0, dp1));
      if (a1 > mt) mt = a1; if (a2 > mp) mp = a2;
    }
    double Vtau_max = imul(pt(mt), pt(200.0)).hi;            /* /d with d = 1/200 exact */
    double Vphi_max = imul(pt(mp), C_INVDPHI).hi;            /* /dphi, dphi = 2pi/2514 */
    printf("LIPSCHITZ: max|V_tau| <= %.17g ; max|V_phi| <= %.17g\n", Vtau_max, Vphi_max);
    fflush(stdout);
  }

  /* HJB */
  double worst = INFINITY; int wi = -1, wj = -1; long ncell = 0, nfail = 0, nunres = 0, totboxes = 0;
  double unres_worst = INFINITY; int ui = -1, uj = -1; Box ubox; double ubound = INFINITY;
  int sound_viol = 0;
  struct { double mc; int i, j; } topk[8]; for (int q = 0; q < 8; q++) { topk[q].mc = INFINITY; topk[q].i = topk[q].j = -1; }
  for (int i = r0; i < r1; i += rstride) {
    double rowworst = INFINITY; int rowj = -1; long rowboxes = 0; int rowfail = 0;
    for (int j = cstart; j < cend; j += cstride) {
      CellRes R;
      check_cell(i, j, &R);
      ncell++; totboxes += R.boxes; rowboxes += R.boxes;
      if (R.status == 0 && R.minctr < topk[7].mc) { int q = 7; while (q > 0 && topk[q-1].mc > R.minctr) { topk[q] = topk[q-1]; q--; } topk[q].mc = R.minctr; topk[q].i = i; topk[q].j = j; }
      Cell c; make_cell(&c, i, j);
      if (R.status == 0) {
        if (R.minlb < worst) { worst = R.minlb; wi = i; wj = j; }
        if (R.minlb < rowworst) { rowworst = R.minlb; rowj = j; }
      } else if (R.status == 1) {
        nfail++; rowfail++;
        printf("FAIL(WITNESS) cell (i=%d, j=%d): G(point) <= %.17g < thr at sigma=%.17g theta=%.17g rho=%.17g psi=%.17g (box bound %.6g)\n",
               i, j, R.witnessG_hi, R.witness_pt[0], R.witness_pt[1], R.witness_pt[2], R.witness_pt[3], R.failbound);
        fflush(stdout);
      } else {
        nunres++; rowfail++;
        printf("FAIL(UNRESOLVED depth/budget) cell (i=%d, j=%d): box sigma=[%.17g,%.17g] theta=[%.17g,%.17g] rho=[%.17g,%.17g] psi=[%.17g,%.17g] lower bound %.17g < thr (boxes=%ld)\n",
               i, j, R.failbox.lo[0], R.failbox.hi[0], R.failbox.lo[1], R.failbox.hi[1], R.failbox.lo[2], R.failbox.hi[2], R.failbox.lo[3], R.failbox.hi[3], R.failbound, R.boxes);
        fflush(stdout);
        if (R.failbound < ubound) { ubound = R.failbound; ui = i; uj = j; ubox = R.failbox; }
      }
      if (dobisect) {
        double lo_ = -20.0, hi_ = 20.0, save = THR; CellRes Q;
        for (int it = 0; it < 56; it++) {
          double mid_ = 0.5 * (lo_ + hi_); THR = mid_; check_cell(i, j, &Q);
          if (Q.status == 0) lo_ = mid_; else hi_ = mid_;
        }
        THR = save;
        double arg[4]; double sm = sample_cell_min(&c, arg); double rf = refine_min(&c, arg);
        printf("  BISECT cell (%d,%d): certified min G >= %.12g ; refined sampled min = %.12g ; gap (sampled - certified) = %.3g %s\n", i, j, lo_, rf, rf - lo_,
               lo_ <= rf + 1e-12 ? "(consistent)" : "(INCONSISTENT: certified above sampled!)");
        if (lo_ > rf + 1e-12) sound_viol++;
        (void)sm;
      }
      if (dosample && R.status == 0) {
        double arg[4]; double sm = sample_cell_min(&c, arg);
        if (R.minlb > sm) { sound_viol++; printf("SOUNDNESS VIOLATION cell (%d,%d): certified leaf lb %.17g > sampled min %.17g\n", i, j, R.minlb, sm); }
        /* cross check jet value against plain double code at the sample argmin */
        Box bx; for (int k = 0; k < 4; k++) bx.lo[k] = bx.hi[k] = arg[k];
        J v[4]; for (int k = 0; k < 4; k++) v[k] = jvar(k, pt(arg[k]), 0);
        J gj = Gfun(v[0], v[1], v[2], v[3], &c);
        double gp = Gpt(arg[0], arg[1], arg[2], arg[3], &c);
        if (!(gp >= gj.v.lo - 1e-12 && gp <= gj.v.hi + 1e-12)) printf("JET/PLAIN MISMATCH cell (%d,%d): jet [%.17g, %.17g] plain %.17g\n", i, j, gj.v.lo, gj.v.hi, gp);
        printf("  cell (%d,%d): certified leaf-min lb %.9g <= sampled min %.9g (diff %.3g), boxes %ld\n", i, j, R.minlb, sm, sm - R.minlb, R.boxes);
      }
    }
    if (lf || (r1 - r0) <= 50) {
      char line[512];
      snprintf(line, sizeof line, "row %d done: cells %ld, row_worst_lb %.9g at j=%d, row_fails %d, row_boxes %ld | rows_done %d/%d worst_so_far %.9g at (i=%d,j=%d) fails %ld unresolved %ld t=%.0fs",
               i, (long)((cend - cstart + cstride - 1) / cstride), rowworst, rowj, rowfail, rowboxes, i - r0 + 1, r1 - r0, worst, wi, wj, nfail, nunres, now() - t0);
      if (lf) { fprintf(lf, "%s\n", line); fflush(lf); }
      printf("%s\n", line); fflush(stdout);
    }
  }
  printf("HJB SUMMARY: cells checked %ld, boxes %ld, witness-fails %ld, unresolved %ld; smallest certified lower bound of G over passing cells = %.17g at cell (i=%d,j=%d) %s\n",
         ncell, totboxes, nfail, nunres, worst, wi, wj, (nfail + nunres == 0) ? "-> PASS" : "-> FAIL");
  if (topk_report && topk[0].i >= 0) {
    printf("Refinement of the 8 passing cells whose lowest evaluated centre value (an upper bound for the cell minimum of G) is smallest;\n");
    printf("for each, THR is bisected to the largest value for which the same branch and bound still certifies G >= THR on the whole cell:\n");
    double save = THR; double gmin_cert = INFINITY; int gi = -1, gj = -1;
    for (int q = 0; q < 8 && topk[q].i >= 0; q++) {
      double lo_ = THR, hi_ = topk[q].mc; CellRes Q;
      if (hi_ < lo_) hi_ = lo_;
      for (int it = 0; it < 60; it++) {
        double mid_ = 0.5 * (lo_ + hi_); THR = mid_; check_cell(topk[q].i, topk[q].j, &Q);
        if (Q.status == 0) lo_ = mid_; else hi_ = mid_;
      }
      printf("  cell (i=%d,j=%d): certified G >= %.12g on the whole cell; some box centre has G <= %.12g\n", topk[q].i, topk[q].j, lo_, topk[q].mc);
      if (lo_ < gmin_cert) { gmin_cert = lo_; gi = topk[q].i; gj = topk[q].j; }
    }
    THR = save;
    printf("SMALLEST CERTIFIED LOWER BOUND OF G (refined over those 8 cells; all other cells certified >= THR=%.17g): %.12g at cell (i=%d,j=%d)\n", THR, gmin_cert, gi, gj);
  }
  if (nunres) printf("worst unresolved: cell (%d,%d) bound %.17g\n", ui, uj, ubound);
  if (dosample) printf("soundness violations vs sampling: %d\n", sound_viol);
  printf("elapsed %.1fs\n", now() - t0);
  if (lf) { fprintf(lf, "finished: cells %ld smallest_lb %.17g at (%d,%d) witness_fails %ld unresolved %ld\n", ncell, worst, wi, wj, nfail, nunres); fclose(lf); }
  (void)ubox;
  return (nfail + nunres) ? 1 : 0;
}
