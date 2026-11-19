/* prune.c: greedy removal of redundant blocks from a covering design.
   usage: prune V K T IN OUT SEED   (points 1..V in IN; blocks one per line)
   count[r] = number of blocks containing t-set of colex rank r (uint8, saturating at 255; a saturated count is
   never decremented below 255, which can only make the tool keep more blocks; the frozen checker re-verifies).
   Blocks are scanned in a random order (SEED); a block is removed if every t-subset has count >= 2. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint64_t B[128][16];
static int V, K, T;
static uint8_t *cnt;
static int blk[200000][32]; static int nb = 0; static char removed[200000];
static int sub[16];
static uint64_t rankof(int *s) { uint64_t r = 0; for (int i = 0; i < T; i++) r += B[s[i]][i + 1]; return r; }
/* iterate t-subsets of block b; mode 0: inc, 1: check min>=2, 2: dec */
static int walk(int *b, int mode) {
  int idx[16]; for (int i = 0; i < T; i++) idx[i] = i;
  while (1) {
    for (int i = 0; i < T; i++) sub[i] = b[idx[i]];
    uint64_t r = rankof(sub);
    if (mode == 0) { if (cnt[r] < 255) cnt[r]++; }
    else if (mode == 1) { if (cnt[r] < 2) return 0; }
    else { if (cnt[r] < 255) cnt[r]--; }
    int i = T - 1; while (i >= 0 && idx[i] == K - T + i) i--;
    if (i < 0) break;
    idx[i]++; for (int j = i + 1; j < T; j++) idx[j] = idx[j - 1] + 1;
  }
  return 1;
}
static int cmpi(const void *a, const void *b) { return *(int *)a - *(int *)b; }
int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
  V = atoi(argv[1]); K = atoi(argv[2]); T = atoi(argv[3]); unsigned seed = atoi(argv[6]);
  for (int n = 0; n < 128; n++) { B[n][0] = 1; for (int k = 1; k < 16; k++) B[n][k] = n == 0 ? 0 : B[n - 1][k - 1] + B[n - 1][k]; }
  uint64_t N = B[V][T]; cnt = calloc(N, 1); if (!cnt) { fprintf(stderr, "oom\n"); return 1; }
  FILE *f = fopen(argv[4], "r"); char line[1024];
  while (fgets(line, sizeof line, f)) {
    int c = 0; char *p = strtok(line, " \t\n"); while (p) { blk[nb][c++] = atoi(p) - 1; p = strtok(NULL, " \t\n"); }
    if (c == 0) continue; if (c != K) { fprintf(stderr, "bad block size %d\n", c); return 1; }
    qsort(blk[nb], K, sizeof(int), cmpi); nb++;
  }
  fclose(f);
  for (int i = 0; i < nb; i++) walk(blk[i], 0);
  uint64_t unc = 0; for (uint64_t r = 0; r < N; r++) if (!cnt[r]) unc++;
  printf("in blocks=%d uncovered=%llu\n", nb, (unsigned long long)unc);
  int *ord = malloc(sizeof(int) * nb); for (int i = 0; i < nb; i++) ord[i] = i;
  srand(seed); for (int i = nb - 1; i > 0; i--) { int j = rand() % (i + 1); int x = ord[i]; ord[i] = ord[j]; ord[j] = x; }
  int rem = 0;
  for (int q = 0; q < nb; q++) { int i = ord[q]; if (walk(blk[i], 1)) { walk(blk[i], 2); removed[i] = 1; rem++; } }
  FILE *o = fopen(argv[5], "w");
  for (int i = 0; i < nb; i++) if (!removed[i]) { for (int j = 0; j < K; j++) fprintf(o, j ? " %d" : "%d", blk[i][j] + 1); fprintf(o, "\n"); }
  fclose(o);
  printf("removed=%d out blocks=%d\n", rem, nb - rem);
  return 0;
}
