/* Lens small-data-direct: direct super edge-magic search (consecutive edge sums), with random restarts.
   For each tree line "n;u-v,...": pick window start W in [3, n+1], a root and its label, order vertices by BFS, and give
   each vertex label s - f(parent) for an unused sum s in [W, W+q-1] with the label unused in 1..n.
   Each attempt has a node cap; attempts are randomised (W, root, root label, sum order). Prints
   "n;edges;labels;nodes;attempts" or "n;edges;;UNLABELED nodes". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 40
int n, q, W, adj[MAXN][MAXN], deg[MAXN], order[MAXN], par[MAXN], lab[MAXN], usedL[2*MAXN+2], usedS[4*MAXN+4];
long long nodes, cap;
static unsigned long long rs = 88172645463325252ULL;
static inline unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)rs; }
int rec(int i) {
  if (++nodes > cap) return -1;
  if (i == n) return 1;
  int v = order[i], p = par[v], ss[2*MAXN], k = 0;
  for (int s = W; s < W + q; s++) if (!usedS[s]) { int l = s - lab[p]; if (l >= 1 && l <= n && !usedL[l]) ss[k++] = s; }
  if (k == 0) return 0;
  for (int a = k - 1; a > 0; a--) { int b = rnd() % (a + 1); int t = ss[a]; ss[a] = ss[b]; ss[b] = t; }
  for (int z = 0; z < k; z++) { int s = ss[z], l = s - lab[p];
    lab[v] = l; usedL[l] = 1; usedS[s] = 1;
    int r = rec(i + 1);
    usedL[l] = 0; usedS[s] = 0;
    if (r) return r;
  }
  return 0;
}
int main(int argc, char **argv) {
  cap = argc > 1 ? atoll(argv[1]) : 2000; long long maxatt = argc > 2 ? atoll(argv[2]) : 200000; rs ^= argc > 3 ? atoll(argv[3]) : 1;
  static char line[8192];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0; char orig[8192]; strcpy(orig, line);
    char *s = strchr(line, ';'); *s = 0; n = atoi(line); q = n - 1; memset(deg, 0, sizeof deg);
    for (char *t = strtok(s + 1, ","); t; t = strtok(NULL, ",")) { int a, b; sscanf(t, "%d-%d", &a, &b); adj[a][deg[a]++] = b; adj[b][deg[b]++] = a; }
    long long tot = 0, att; int ok = 0;
    for (att = 0; att < maxatt && !ok; att++) {
      W = 3 + rnd() % (n - 1); int root = rnd() % n, seen[MAXN] = {0}, h = 0, k = 0;
      order[k++] = root; seen[root] = 1; par[root] = -1;
      while (h < k) { int x = order[h++]; for (int j = 0; j < deg[x]; j++) { int y = adj[x][j]; if (!seen[y]) { seen[y] = 1; par[y] = x; order[k++] = y; } } }
      memset(usedL, 0, sizeof usedL); memset(usedS, 0, sizeof usedS);
      lab[root] = 1 + rnd() % n; usedL[lab[root]] = 1;
      nodes = 0; int r = rec(1); tot += nodes; if (r == 1) ok = 1;
    }
    if (ok) { printf("%s;", orig); for (int v = 0; v < n; v++) printf(v ? ",%d" : "%d", lab[v]); printf(";%lld;%lld\n", tot, att); }
    else printf("%s;;UNLABELED %lld\n", orig, tot);
  }
  return 0;
}
