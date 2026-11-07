/* Lens structured-family: find an alpha-labeling (graceful, bijection V->{0..q}, one bipartition class gets {0..k},
   the other {k+1..q}), then map it to a super edge-magic labeling: lower l -> k+1-l, upper u -> u+1
   (edge sum = (u-l)+k+2, so the q sums are k+3..k+q+2, consecutive). Independent of sem_direct.c.
   Search: BFS order from a random root; a child of a lower vertex gets f(p)+d, a child of an upper vertex f(p)-d,
   d an unused difference, label unused and inside the child's class range. Randomised restarts with a node cap.
   Output "n;edges;SEMlabels;nodes;attempts" or "n;edges;;NOALPHA nodes" (no alpha-labeling found within the cap;
   that is not a proof that none exists). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 40
int n, q, K, adj[MAXN][MAXN], deg[MAXN], order[MAXN], par[MAXN], lab[MAXN], side[MAXN], low[MAXN], usedL[MAXN+1], usedD[MAXN+1];
long long nodes, cap;
static unsigned long long rs = 0x9E3779B97F4A7C15ULL;
static inline unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)rs; }
int rec(int i) {
  if (++nodes > cap) return -1;
  if (i == n) return 1;
  int v = order[i], p = par[v], ds[MAXN], k = 0;
  for (int d = 1; d <= q; d++) if (!usedD[d]) { int l = low[p] ? lab[p] + d : lab[p] - d;
      if (l < 0 || l > q || usedL[l]) continue; if (low[v] ? l > K : l <= K) continue; ds[k++] = d; }
  for (int a = k - 1; a > 0; a--) { int b = rnd() % (a + 1); int t = ds[a]; ds[a] = ds[b]; ds[b] = t; }
  /* bias: try the largest differences first half the time */
  if (rnd() & 1) for (int a = 0; a < k; a++) for (int b = a + 1; b < k; b++) if (ds[b] > ds[a]) { int t = ds[a]; ds[a] = ds[b]; ds[b] = t; }
  for (int z = 0; z < k; z++) { int d = ds[z], l = low[p] ? lab[p] + d : lab[p] - d;
    lab[v] = l; usedL[l] = 1; usedD[d] = 1;
    int r = rec(i + 1); usedL[l] = 0; usedD[d] = 0; if (r) return r; }
  return 0;
}
int main(int argc, char **argv) {
  cap = argc > 1 ? atoll(argv[1]) : 300; long long maxatt = argc > 2 ? atoll(argv[2]) : 20000; rs ^= argc > 3 ? atoll(argv[3]) : 1;
  static char line[8192];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0; char orig[8192]; strcpy(orig, line);
    char *s = strchr(line, ';'); *s = 0; n = atoi(line); q = n - 1; memset(deg, 0, sizeof deg);
    for (char *t = strtok(s + 1, ","); t; t = strtok(NULL, ",")) { int a, b; sscanf(t, "%d-%d", &a, &b); adj[a][deg[a]++] = b; adj[b][deg[b]++] = a; }
    /* bipartition from vertex 0 */
    int seen[MAXN] = {0}, h = 0, k = 0, cnt0 = 0; int ord0[MAXN]; ord0[k++] = 0; seen[0] = 1; side[0] = 0;
    while (h < k) { int x = ord0[h++]; for (int j = 0; j < deg[x]; j++) { int y = adj[x][j]; if (!seen[y]) { seen[y] = 1; side[y] = !side[x]; ord0[k++] = y; } } }
    for (int v = 0; v < n; v++) cnt0 += side[v] == 0;
    long long tot = 0, att; int ok = 0;
    for (att = 0; att < maxatt && !ok; att++) {
      int lowside = rnd() & 1; for (int v = 0; v < n; v++) low[v] = side[v] == lowside;
      K = (lowside == 0 ? cnt0 : n - cnt0) - 1;
      int root = rnd() % n; memset(seen, 0, sizeof seen); h = 0; k = 0; order[k++] = root; seen[root] = 1; par[root] = -1;
      while (h < k) { int x = order[h++]; for (int j = 0; j < deg[x]; j++) { int y = adj[x][j]; if (!seen[y]) { seen[y] = 1; par[y] = x; order[k++] = y; } } }
      memset(usedL, 0, sizeof usedL); memset(usedD, 0, sizeof usedD);
      lab[root] = low[root] ? (int)(rnd() % (K + 1)) : K + 1 + (int)(rnd() % (q - K)); usedL[lab[root]] = 1;
      nodes = 0; int r = rec(1); tot += nodes; if (r == 1) ok = 1;
    }
    if (ok) { printf("%s;", orig); for (int v = 0; v < n; v++) { int L = low[v] ? K + 1 - lab[v] : lab[v] + 1; printf(v ? ",%d" : "%d", L); } printf(";%lld;%lld\n", tot, att); }
    else printf("%s;;NOALPHA %lld\n", orig, tot);
  }
  return 0;
}
