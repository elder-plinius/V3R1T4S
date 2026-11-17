/* RESTART VARIANT (hypothesis D5): random difference order, small cap per attempt, many restarts.
   Lens small-data-direct: direct odd-graceful backtracking, independent of the alpha lens.
   For each tree (line "n;u-v,..."), fix an edge with difference 2q-1 as labels 0 and 2q-1 (the complement
   f -> 2q-1-f makes one orientation enough), order the other vertices by BFS from that edge, and give each vertex
   the label f(parent) +- d for an unused odd d, largest d first. Node cap per tree. Prints
   "n;edges;labels;nodes" or "n;edges;;UNLABELED nodes". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 32
int n, q, M, ne, eu[MAXN], ev[MAXN], adj[MAXN][MAXN], deg[MAXN];
int order[MAXN], par[MAXN], lab[MAXN], usedL[2*MAXN], usedD[2*MAXN];
long long nodes, cap;
int rec(int i) {
  if (++nodes > cap) return -1;
  if (i == n) return 1;
  int v = order[i], p = par[v];
  int ds[64], nd = 0; for (int d = M - 2; d >= 1; d -= 2) ds[nd++] = d;
  for (int a = nd - 1; a > 0; a--) { int b = rand() % (a + 1); int t = ds[a]; ds[a] = ds[b]; ds[b] = t; }
  for (int z = 0; z < nd; z++) { int d = ds[z];
    if (usedD[d]) continue;
    for (int s = 0; s < 2; s++) {
      int l = s ? lab[p] - d : lab[p] + d;
      if (l < 0 || l > M || usedL[l]) continue;
      lab[v] = l; usedL[l] = 1; usedD[d] = 1;
      int r = rec(i + 1);
      if (r) { if (r < 0) { usedL[l] = 0; usedD[d] = 0; } return r; }
      usedL[l] = 0; usedD[d] = 0;
    }
  }
  return 0;
}
int main(int argc, char **argv) {
  cap = argc > 1 ? atoll(argv[1]) : 100000LL; int restarts = argc > 2 ? atoi(argv[2]) : 200; srand(argc > 3 ? atoi(argv[3]) : 1);
  static char line[4096], orig[4096];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0; strcpy(orig, line);
    char *s = strchr(line, ';'); *s = 0; n = atoi(line); q = n - 1; M = 2 * q - 1; ne = 0;
    memset(deg, 0, sizeof deg);
    for (char *t = strtok(s + 1, ","); t; t = strtok(NULL, ",")) {
      int a, b; sscanf(t, "%d-%d", &a, &b); eu[ne] = a; ev[ne] = b; ne++;
      adj[a][deg[a]++] = b; adj[b][deg[b]++] = a;
    }
    long long tot = 0; int ok = 0;
    for (int rep = 0; rep < restarts && !ok; rep++) for (int e = 0; e < ne && !ok; e++) {
      memset(usedL, 0, sizeof usedL); memset(usedD, 0, sizeof usedD);
      int u = eu[e], w = ev[e], seen[MAXN] = {0}, h = 0, k = 0;
      order[k++] = u; order[k++] = w; seen[u] = seen[w] = 1; par[u] = par[w] = -1;
      while (h < k) { int x = order[h++]; for (int j = 0; j < deg[x]; j++) { int y = adj[x][j]; if (!seen[y]) { seen[y] = 1; par[y] = x; order[k++] = y; } } }
      lab[u] = 0; lab[w] = M; usedL[0] = usedL[M] = 1; usedD[M] = 1;
      nodes = 0; int r = rec(2); tot += nodes;
      if (r == 1) ok = 1;
    }
    if (ok) { printf("%s;", orig); for (int v = 0; v < n; v++) printf(v ? ",%d" : "%d", lab[v]); printf(";%lld\n", tot); }
    else printf("%s;;UNLABELED %lld\n", orig, tot);
    fflush(stdout);
  }
  return 0;
}
