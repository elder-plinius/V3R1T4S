/* cwsec.c : exact Collatz-Wielandt checker for the diagonal-layer dimer transfer matrix of
   Q. He (arXiv 2607.28810), three dimensions, cross-section (m,n), written from the definition.
   Matrix-free: the compressed blocks X and Y are never stored. One pass applies
      (Phi_k y)(U) = sum over injections f : U -> V_{m,n} with f(u)-u in D={(0,0),(1,0),(0,1)}
                     of  y( orbit of the complement of f(U) ),     |U| = k,
   which is the compressed block of the matrix T with T[U,V] = per A[U, V_{m,n} minus V].
   All exact arithmetic is unsigned 128-bit with overflow detection (exit 3 on overflow).
   Usage:
     cwsec check m n i certfile          exact CW ratio of sector i for the vector in certfile
     cwsec iter  m n P                   exact (XY)^p 1 iterates, all sectors, p = 0..P (needs no overflow)
     cwsec power m n i K bits outfile    K long-double power steps, write rounded integer vector
   Certificate line format (comment lines start with #):  orbit_id canonical_mask x [listed_value]
*/
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "stdint.h"
#include "math.h"
#include "pthread.h"
#include "unistd.h"
typedef unsigned __int128 u128;
static int m, n, N, NT;
static uint32_t FULL;
static int ng;
static int (*gperm)[32];
static uint32_t *tabs;
static int32_t *orbid;
static int nb[32][3];

static void pr128(u128 x, char *buf) {
  char t[64]; int k = 0;
  if (x == 0) { strcpy(buf, "0"); return; }
  while (x) { t[k++] = '0' + (int)(x % 10); x /= 10; }
  for (int j = 0; j < k; j++) buf[j] = t[k - 1 - j];
  buf[k] = 0;
}
static int add_v(int v, int dx, int dy) { int x = v / n, y = v % n; return ((x + dx) % m) * n + ((y + dy) % n); }
static inline uint32_t img(int g, uint32_t mask) {
  uint32_t r = 0;
  for (int c = 0; c < 4; c++) r |= tabs[((size_t)g * 4 + c) * 256 + ((mask >> (8 * c)) & 255)];
  return r;
}
/* group G = V x| K : all x -> t + phi(x), phi an automorphism of Z/m x Z/n with phi(D) = s + D for some s */
static void build_group(void) {
  gperm = malloc(sizeof(int[32]) * (size_t)N * N * N); ng = 0;
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) {
    int ax = a / n, ay = a % n, bx = b / n, by = b % n;
    if ((m * ax) % m != 0 || (m * ay) % n != 0) continue;
    if ((n * bx) % m != 0 || (n * by) % n != 0) continue;
    int phi[32], seen[32] = {0}, ok = 1;
    for (int x = 0; x < m && ok; x++) for (int y = 0; y < n; y++) {
      int px = (x * ax + y * bx) % m, py = (x * ay + y * by) % n, w = px * n + py;
      phi[x * n + y] = w; if (seen[w]) { ok = 0; break; } seen[w] = 1; }
    if (!ok) continue;
    int Dd[3][2] = {{0,0},{1,0},{0,1}}, tfound = 0;
    for (int t = 0; t < N && !tfound; t++) {
      uint32_t lhs = 0, rhs = 0;
      for (int d = 0; d < 3; d++) { lhs |= 1u << phi[add_v(0, Dd[d][0], Dd[d][1])]; rhs |= 1u << add_v(t, Dd[d][0], Dd[d][1]); }
      if (lhs == rhs) tfound = 1; }
    if (!tfound) continue;
    for (int u = 0; u < N; u++) {
      for (int v = 0; v < N; v++) { int w = phi[v]; gperm[ng][v] = ((w / n + u / n) % m) * n + ((w % n + u % n) % n); }
      ng++; }
  }
  tabs = calloc((size_t)ng * 4 * 256, 4);
  for (int g = 0; g < ng; g++) for (int c = 0; c < 4; c++) for (int bb = 0; bb < 256; bb++) {
    uint32_t r = 0; for (int j = 0; j < 8; j++) if (bb >> j & 1) { int v = 8 * c + j; if (v < N) r |= 1u << gperm[g][v]; }
    tabs[((size_t)g * 4 + c) * 256 + bb] = r; }
}
typedef struct { int k, nor; uint32_t *rep; } Sect;
static uint32_t canon(uint32_t mask) { uint32_t c = mask; for (int g = 0; g < ng; g++) { uint32_t t = img(g, mask); if (t < c) c = t; } return c; }
static int cmpu(const void *a, const void *b) { uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b; return x < y ? -1 : x > y; }
/* enumerate all masks of popcount k, collect canonical reps (sorted), fill orbid for every mask of that popcount */
typedef struct { int k; uint32_t *masks; size_t lo, hi; uint32_t *canonv; } CJ;
static void *canon_worker(void *p) { CJ *j = p; for (size_t i = j->lo; i < j->hi; i++) j->canonv[i] = canon(j->masks[i]); return 0; }
static Sect enum_sector(int k) {
  Sect s; s.k = k;
  size_t cnt = 0, cap = 1 << 20; uint32_t *masks = malloc(4 * cap);
  if (k == 0) { masks[cnt++] = 0; }
  else { uint32_t mk = (1u << k) - 1;
    for (;;) { if (cnt == cap) { cap *= 2; masks = realloc(masks, 4 * cap); } masks[cnt++] = mk;
      if (k == N) break;
      uint32_t cc = mk & -mk, r = mk + cc; if (r > FULL || r == 0) break; mk = (((r ^ mk) >> 2) / cc) | r; if (mk > FULL) break; } }
  uint32_t *cv = malloc(4 * cnt);
  pthread_t th[256]; CJ js[256];
  for (int t = 0; t < NT; t++) { js[t].k = k; js[t].masks = masks; js[t].canonv = cv; js[t].lo = cnt * t / NT; js[t].hi = cnt * (t + 1) / NT; pthread_create(&th[t], 0, canon_worker, &js[t]); }
  for (int t = 0; t < NT; t++) pthread_join(th[t], 0);
  s.rep = malloc(4 * (cnt + 1)); s.nor = 0;
  for (size_t i = 0; i < cnt; i++) if (cv[i] == masks[i]) s.rep[s.nor++] = masks[i];
  qsort(s.rep, s.nor, 4, cmpu);
  for (size_t i = 0; i < cnt; i++) { /* binary search canonical rep */
    int lo = 0, hi = s.nor - 1; while (lo < hi) { int mid = (lo + hi) / 2; if (s.rep[mid] < cv[i]) lo = mid + 1; else hi = mid; }
    orbid[masks[i]] = lo; }
  free(masks); free(cv); return s;
}
typedef struct { int tid; Sect *rows; int exact; u128 *vin128, *out128; long double *vin, *out; int bad; long next_unused; } Job;
static long g_next; static pthread_mutex_t g_mu = PTHREAD_MUTEX_INITIALIZER;
static int g_bad;
typedef struct { int k; const int *vs; const uint32_t *ru; u128 acc; long double facc; int bad; const u128 *v128; const long double *vf; int exact; } Ctx;
static void dfs(Ctx *c, int idx, uint32_t used) {
  if (idx == c->k) {
    int o = orbid[FULL ^ used];
    if (c->exact) { u128 a = c->v128[o], s; if (__builtin_add_overflow(c->acc, a, &s)) c->bad = 1; c->acc = s; }
    else c->facc += c->vf[o];
    return; }
  if (__builtin_popcount(c->ru[idx] & ~used) < c->k - idx) return;
  int u = c->vs[idx];
  for (int d = 0; d < 3; d++) { int t = nb[u][d]; if (used >> t & 1) continue; dfs(c, idx + 1, used | (1u << t)); }
}
static void *worker(void *p) {
  Job *J = p; int nrows = J->rows->nor;
  for (;;) {
    pthread_mutex_lock(&g_mu); long r0 = g_next; g_next += 8; pthread_mutex_unlock(&g_mu);
    if (r0 >= nrows) break;
    for (long r = r0; r < r0 + 8 && r < nrows; r++) {
      uint32_t U = J->rows->rep[r]; int vs[32], k = 0; for (int v = 0; v < N; v++) if (U >> v & 1) vs[k++] = v;
      uint32_t ru[34]; ru[k] = 0; for (int q = k - 1; q >= 0; q--) { ru[q] = ru[q + 1]; for (int d = 0; d < 3; d++) ru[q] |= 1u << nb[vs[q]][d]; }
      Ctx c; c.k = k; c.vs = vs; c.ru = ru; c.acc = 0; c.facc = 0; c.bad = 0; c.v128 = J->vin128; c.vf = J->vin; c.exact = J->exact;
      dfs(&c, 0, 0);
      if (J->exact) { J->out128[r] = c.acc; if (c.bad) { J->bad = 1; } } else J->out[r] = c.facc; }
  }
  return 0;
}
/* out = Phi(in): rows = sector of size k = rows->k ; in is indexed by orbits of (N-k)-sets */
static void apply(Sect *rows, int exact, u128 *vin128, long double *vin, u128 *out128, long double *out) {
  Job js[256]; pthread_t th[256]; g_next = 0;
  for (int t = 0; t < NT; t++) { js[t].tid = t; js[t].rows = rows; js[t].exact = exact; js[t].vin128 = vin128; js[t].vin = vin; js[t].out128 = out128; js[t].out = out; js[t].bad = 0; pthread_create(&th[t], 0, worker, &js[t]); }
  for (int t = 0; t < NT; t++) { pthread_join(th[t], 0); if (js[t].bad) { fprintf(stderr, "OVERFLOW in u128 arithmetic\n"); exit(3); } }
}
static int ge_ratio(u128 a, u128 b, u128 c, u128 d) { /* a/b > c/d  <=> a*d > c*b with 256-bit products */
  uint64_t al[2] = {(uint64_t)a, (uint64_t)(a >> 64)}, dl[2] = {(uint64_t)d, (uint64_t)(d >> 64)}, cl[2] = {(uint64_t)c, (uint64_t)(c >> 64)}, bl[2] = {(uint64_t)b, (uint64_t)(b >> 64)};
  uint64_t L[4] = {0,0,0,0}, R[4] = {0,0,0,0};
  for (int pass = 0; pass < 2; pass++) { uint64_t *x = pass ? cl : al, *y = pass ? bl : dl, *res = pass ? R : L;
    u128 carry; uint64_t w[4] = {0,0,0,0};
    for (int i = 0; i < 2; i++) { carry = 0; for (int j = 0; j < 2; j++) { u128 t = (u128)x[i] * y[j] + w[i + j] + carry; w[i + j] = (uint64_t)t; carry = t >> 64; } w[i + 2] += (uint64_t)carry; }
    for (int i = 0; i < 4; i++) res[i] = w[i]; }
  for (int i = 3; i >= 0; i--) { if (L[i] != R[i]) return L[i] > R[i]; }
  return 0;
}
static void setup(int mm, int nn) {
  m = mm; n = nn; N = m * n; FULL = (N == 32) ? 0xffffffffu : ((1u << N) - 1);
  NT = (int)sysconf(_SC_NPROCESSORS_ONLN); if (getenv("CWSEC_THREADS")) NT = atoi(getenv("CWSEC_THREADS")); if (NT < 1) NT = 1; if (NT > 200) NT = 200;
  for (int v = 0; v < N; v++) { nb[v][0] = v; nb[v][1] = add_v(v, 1, 0); nb[v][2] = add_v(v, 0, 1); }
  build_group();
  orbid = malloc(4 * ((size_t)1 << N)); memset(orbid, 0xff, 4 * ((size_t)1 << N));
}
static void print_ratio(const char *tag, int i, int p, u128 num, u128 den, int u) {
  char a[64], b[64]; pr128(num, a); pr128(den, b);
  long double r = (long double)num / (long double)den;
  printf("%s sector=%d p=%d u=%d ratio=%s/%s approx=%.9Lf l3bound=%.10Lf\n", tag, i, p, u, a, b, r, logl(r) / (2.0L * N));
}
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "see header\n"); return 1; }
  const char *mode = argv[1]; setup(atoi(argv[2]), atoi(argv[3]));
  if (!strcmp(mode, "iter")) {
    int P = atoi(argv[4]);
    for (int i = 0; i <= N / 2; i++) {
      Sect Sm = enum_sector(i); Sect Sp = (N - i == i) ? Sm : enum_sector(N - i);
      int a = Sm.nor, b = Sp.nor; u128 *v = malloc(16 * (size_t)a), *w = malloc(16 * (size_t)b), *z = malloc(16 * (size_t)a);
      for (int r = 0; r < a; r++) v[r] = 1;
      for (int p = 0; p <= P; p++) {
        apply(&Sp, 1, v, 0, w, 0);   /* Y v : rows are (N-i)-sets */
        apply(&Sm, 1, w, 0, z, 0);   /* X w : rows are i-sets */
        int best = 0; for (int r = 1; r < a; r++) if (ge_ratio(z[r], v[r], z[best], v[best])) best = r;
        print_ratio("ITER", i, p, z[best], v[best], best); fflush(stdout);
        memcpy(v, z, 16 * (size_t)a); }
      free(v); free(w); free(z);
    }
    return 0; }
  int i = atoi(argv[4]);
  if (!strcmp(mode, "check")) {
    const char *cf = argv[5];
    Sect Sm = enum_sector(i); Sect Sp = (N - i == i) ? Sm : enum_sector(N - i);
    int a = Sm.nor, b = Sp.nor; fprintf(stderr, "m=%d n=%d |G|=%d sector=%d orbits=%d/%d threads=%d\n", m, n, ng, i, a, b, NT);
    u128 *x = calloc(a, 16), *w = malloc(16 * (size_t)b), *z = malloc(16 * (size_t)a), *listed = calloc(a, 16); char *have = calloc(a, 1);
    FILE *f = fopen(cf, "r"); if (!f) { perror("cert"); return 1; }
    char line[4096]; long nl = 0, nbad = 0, nlisted = 0;
    while (fgets(line, sizeof line, f)) {
      if (line[0] == '#' || line[0] == '\n') continue;
      char s1[40], s2[40], s3[80], s4[200]; s4[0] = 0;
      int got = sscanf(line, "%39s %39s %79s %199s", s1, s2, s3, s4); if (got < 3) { nbad++; continue; }
      unsigned long id = strtoul(s1, 0, 10), mask = strtoul(s2, 0, 10); nl++;
      if (mask > FULL || orbid[mask] < 0 || (int)id != orbid[mask] || Sm.rep[id] != mask) { nbad++; continue; }
      u128 xv = 0; int okd = 1; for (char *q = s3; *q; q++) { if (*q < '0' || *q > '9') { okd = 0; break; } xv = xv * 10 + (*q - '0'); }
      if (!okd || xv == 0) { nbad++; continue; }
      if (have[id]) { nbad++; continue; }
      x[id] = xv; have[id] = 1;
      if (got >= 4) { u128 t = 0; for (char *q = s4; *q >= '0' && *q <= '9'; q++) t = t * 10 + (*q - '0'); listed[id] = t; nlisted++; } }
    long cov = 0; for (int r = 0; r < a; r++) cov += have[r];
    printf("CERT lines=%ld bad_lines=%ld orbits_covered=%ld/%d\n", nl, nbad, cov, a);
    if (nbad || cov != a) { printf("CERT INVALID\n"); return 1; }
    apply(&Sp, 1, x, 0, w, 0); apply(&Sm, 1, w, 0, z, 0);
    int best = 0; for (int r = 1; r < a; r++) if (ge_ratio(z[r], x[r], z[best], x[best])) best = r;
    if (nlisted) { long mism = 0; for (int r = 0; r < a; r++) if (listed[r] != z[r]) mism++; printf("LISTED_VALUE_MISMATCHES %ld of %d\n", mism, a); }
    print_ratio("CHECK", i, 0, z[best], x[best], best); printf("CHECK_DONE\n"); return 0; }
  if (!strcmp(mode, "power")) {
    int K = atoi(argv[5]), bits = atoi(argv[6]); const char *of = argv[7];
    Sect Sm = enum_sector(i); Sect Sp = (N - i == i) ? Sm : enum_sector(N - i);
    int a = Sm.nor, b = Sp.nor; long double *v = malloc(sizeof(long double) * a), *w = malloc(sizeof(long double) * b), *z = malloc(sizeof(long double) * a);
    for (int r = 0; r < a; r++) v[r] = 1;
    for (int it = 0; it < K; it++) {
      apply(&Sp, 0, 0, v, 0, w); apply(&Sm, 0, 0, w, 0, z);
      long double mx = 0; for (int r = 0; r < a; r++) if (z[r] > mx) mx = z[r];
      for (int r = 0; r < a; r++) v[r] = z[r] / mx; }
    FILE *f = fopen(of, "w"); fprintf(f, "# builder-generated test vector, (m,n)=(%d,%d), sector i=%d, %d long-double power steps from the all-ones vector, rounded up to integers with max about 2^%d\n# Format: orbit_id canonical_mask x_u\n", m, n, i, K, bits);
    long double sc = ldexpl(1.0L, bits);
    for (int r = 0; r < a; r++) { unsigned long long xv = (unsigned long long)ceill(v[r] * sc); if (xv < 1) xv = 1; fprintf(f, "%d %u %llu\n", r, Sm.rep[r], xv); }
    fclose(f); printf("wrote %s (%d orbits)\n", of, a); return 0; }
  return 1;
}
