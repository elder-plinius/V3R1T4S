/* Streaming list checker, same rules as checker/check_list.py:
   each line: 15 (NU=0) or 18 (NU=1) integers; all six ACCs (hypercharge-squared one x6, integer form);
   max |F| <= QMAX; not all zero; canonical form (each species sorted ascending; of F and -F, after sorting each
   species, the lexicographically larger); gcd 1; strictly increasing lexicographic order (no duplicates).
   Usage: zcat list.gz | checklist QMAX NU   -> prints "valid solutions: N" and PASS, or the failing line and FAIL. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static ll gcdl(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }
static int cmp3(const ll *a, const ll *b, int n) { for (int i = 0; i < n; i++) { if (a[i] < b[i]) return -1; if (a[i] > b[i]) return 1; } return 0; }
static void sort3(ll *t) { ll a = t[0], b = t[1], c = t[2], x;
  if (a > b) { x = a; a = b; b = x; } if (b > c) { x = b; b = c; c = x; } if (a > b) { x = a; a = b; b = x; }
  t[0] = a; t[1] = b; t[2] = c; }
int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: checklist QMAX NU < list\n"); return 2; }
  ll Q = atoll(argv[1]); int nu = atoi(argv[2]); int n = nu ? 18 : 15, k = nu ? 6 : 5;
  static char line[4096]; ll F[18], prev[18], A[18], B[18]; int have_prev = 0; ll count = 0, ln = 0;
  while (fgets(line, sizeof line, stdin)) {
    ln++;
    char *p = line; int m = 0; char *end;
    while (*p == ' ' || *p == '\t') p++;
    if (*p == '\n' || *p == 0) continue;
    for (;;) { while (*p == ' ' || *p == '\t') p++; if (*p == '\n' || *p == 0) break;
      ll v = strtoll(p, &end, 10); if (end == p) { m = -1; break; } if (m < 18) F[m] = v; m++; p = end; }
    const char *why = NULL;
    if (m != n) why = "wrong length";
    else {
      ll s[6][3] = {{0}}; /* per species: sum, square sum, cube sum */
      for (int sp = 0; sp < k; sp++) for (int i = 0; i < 3; i++) { ll x = F[3*sp+i]; s[sp][0] += x; s[sp][1] += x*x; s[sp][2] += x*x*x; }
      ll nu1 = nu ? s[5][0] : 0, nu3 = nu ? s[5][2] : 0;
      ll e1 = 2*s[0][0] + s[1][0] + s[2][0];
      ll e2 = 3*s[0][0] + s[3][0];
      ll e3 = s[0][0] + 8*s[1][0] + 2*s[2][0] + 3*s[3][0] + 6*s[4][0];
      ll e4 = 6*s[0][0] + 3*s[1][0] + 3*s[2][0] + 2*s[3][0] + s[4][0] + nu1;
      ll e5 = s[0][1] - 2*s[1][1] + s[2][1] - s[3][1] + s[4][1];
      ll e6 = 6*s[0][2] + 3*s[1][2] + 3*s[2][2] + 2*s[3][2] + s[4][2] + nu3;
      ll mx = 0; int allz = 1; ll g = 0;
      for (int i = 0; i < n; i++) { ll a = F[i] < 0 ? -F[i] : F[i]; if (a > mx) mx = a; if (F[i]) allz = 0; g = gcdl(g, F[i]); }
      for (int i = 0; i < n; i++) { A[i] = F[i]; B[i] = -F[i]; }
      for (int sp = 0; sp < k; sp++) { sort3(A + 3*sp); sort3(B + 3*sp); }
      const ll *C = cmp3(A, B, n) >= 0 ? A : B;
      if (e1 || e2 || e3 || e4 || e5 || e6) why = "ACC violated";
      else if (mx > Q) why = "charge above QMAX";
      else if (allz) why = "zero solution";
      else if (cmp3(F, C, n) != 0) why = "not canonical";
      else if (g != 1) why = "gcd not 1";
      else if (have_prev && cmp3(F, prev, n) <= 0) why = "not strictly increasing (duplicate or unsorted)";
    }
    if (why) { printf("line %lld: %s: %s", ln, why, line); printf("FAIL\n"); return 1; }
    memcpy(prev, F, sizeof F); have_prev = 1; count++;
  }
  printf("valid solutions: %lld\nPASS\n", count);
  return 0;
}
