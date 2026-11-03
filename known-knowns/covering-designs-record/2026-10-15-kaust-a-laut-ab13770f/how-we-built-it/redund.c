/* redund: for a (v,k,t) covering design, count for every block the t-subsets covered by that block only.
 * usage: redund v k t blocks.txt [outblocks_minus_best.txt]
 * prints: blocks, uncovered, min_unique, argmin (0-based block index), number of blocks with unique==0,
 * and the histogram of unique counts (first values). If outblocks is given, writes the design without the block
 * that has the fewest uniquely covered t-subsets (the warm start for b-1). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXV 100
#define MAXK 26
#define MAXT 9
static uint64_t binom[MAXV + 1][MAXT + 1];
static int V, K, T;

static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: redund v k t blocks.txt [out]\n"); return 2; }
    V = atoi(argv[1]); K = atoi(argv[2]); T = atoi(argv[3]);
    for (int n = 0; n <= MAXV; n++) { binom[n][0] = 1; for (int r = 1; r <= MAXT; r++) binom[n][r] = n ? binom[n - 1][r - 1] + binom[n - 1][r] : 0; }
    uint64_t NT = binom[V][T];
    if (NT > 1000000000ULL) { fprintf(stderr, "too many t-sets\n"); return 2; }
    FILE *f = fopen(argv[4], "rb"); if (!f) { perror(argv[4]); return 2; }
    int cap = 1024, nb = 0; int (*P)[MAXK] = malloc(sizeof(*P) * cap);
    for (;;) {
        int ok = 1;
        if (nb == cap) { cap *= 2; P = realloc(P, sizeof(*P) * cap); }
        for (int i = 0; i < K; i++) { int x; if (fscanf(f, "%d", &x) != 1) { ok = 0; break; } P[nb][i] = x - 1; }
        if (!ok) break;
        qsort(P[nb], K, sizeof(int), cmpint); nb++;
    }
    fclose(f);
    uint8_t *cnt = calloc(NT, 1);
    int idx[MAXT];
    for (int b = 0; b < nb; b++) {
        for (int i = 0; i < T; i++) idx[i] = i;
        for (;;) {
            uint64_t r = 0; for (int i = 0; i < T; i++) r += binom[P[b][idx[i]]][i + 1];
            if (cnt[r] < 255) cnt[r]++;
            int i = T - 1; while (i >= 0 && idx[i] == K - T + i) i--;
            if (i < 0) break;
            idx[i]++; for (int j = i + 1; j < T; j++) idx[j] = idx[j - 1] + 1;
        }
    }
    uint64_t unc = 0; for (uint64_t r = 0; r < NT; r++) unc += (cnt[r] == 0);
    long minu = -1; int argmin = -1, zeros = 0; long hist[8] = {0};
    for (int b = 0; b < nb; b++) {
        long u = 0;
        for (int i = 0; i < T; i++) idx[i] = i;
        for (;;) {
            uint64_t r = 0; for (int i = 0; i < T; i++) r += binom[P[b][idx[i]]][i + 1];
            u += (cnt[r] == 1);
            int i = T - 1; while (i >= 0 && idx[i] == K - T + i) i--;
            if (i < 0) break;
            idx[i]++; for (int j = i + 1; j < T; j++) idx[j] = idx[j - 1] + 1;
        }
        if (minu < 0 || u < minu) { minu = u; argmin = b; }
        if (u == 0) zeros++;
        if (u < 8) hist[u]++;
    }
    printf("blocks=%d uncovered=%llu min_unique=%ld argmin=%d redundant_blocks=%d hist0-7=%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld\n",
           nb, (unsigned long long)unc, minu, argmin, zeros, hist[0], hist[1], hist[2], hist[3], hist[4], hist[5], hist[6], hist[7]);
    if (argc > 5 && argmin >= 0) {
        FILE *g = fopen(argv[5], "wb");
        for (int b = 0; b < nb; b++) { if (b == argmin) continue; for (int i = 0; i < K; i++) fprintf(g, "%d%c", P[b][i] + 1, i == K - 1 ? '\n' : ' '); }
        fclose(g);
    }
    return 0;
}
