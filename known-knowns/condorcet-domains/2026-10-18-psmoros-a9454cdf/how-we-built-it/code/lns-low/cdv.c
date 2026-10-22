/* cdv.c -- independent Condorcet-domain verifier (lens lns-low, run 2026-10-17-2220).
 * Reads one linear order per line (alternatives 1..n separated by spaces, most preferred first) from a file or
 * stdin ("-"); n is taken from the first line.  Checks: every line is a permutation of 1..n; all lines distinct
 * (orders packed into 2 x 64 bits, sorted); for every triple a<b<c the set of relative orders that occur, and the
 * triple passes iff some member of the triple never occupies some position (top/middle/bottom) within the triple
 * (Sen's never condition).  Prints "n N lines L distinct D triples T violations V bad_lines B" and PASS / FAIL.
 * PASS requires bad_lines = 0, distinct = lines, violations = 0 and lines > 0.
 * Usage: cdv FILE|-
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct { uint64_t hi, lo; } key_t2;
static int cmpk(const void *a, const void *b) {
    const key_t2 *x = a, *y = b;
    if (x->hi != y->hi) return x->hi < y->hi ? -1 : 1;
    if (x->lo != y->lo) return x->lo < y->lo ? -1 : 1;
    return 0;
}

int main(int argc, char **argv) {
    FILE *f = (argc < 2 || !strcmp(argv[1], "-")) ? stdin : fopen(argv[1], "r");
    if (!f) { perror("open"); return 2; }
    char *line = NULL; size_t cap = 0; ssize_t len;
    int n = -1; long lines = 0, bad = 0;
    size_t kcap = 1 << 16; key_t2 *keys = malloc(sizeof(key_t2) * kcap);
    /* seen[t] bitmask of 6 patterns; pattern index = rank pattern of (a,b,c) */
    unsigned char *seen = NULL; int T = 0; int (*tri)[3] = NULL;
    int pos[64], perm[64];
    while ((len = getline(&line, &cap, f)) > 0) {
        int k = 0; char *p = line;
        while (*p) {
            while (*p == ' ' || *p == '\t' || *p == '\n' || *p == '\r') p++;
            if (!*p) break;
            char *e; long v = strtol(p, &e, 10);
            if (e == p) { k = -1; break; }
            if (k < 64) perm[k] = (int)v;
            k++; p = e;
        }
        if (k == 0) continue; /* empty line ignored */
        if (n < 0) {
            n = k;
            if (n < 3 || n > 32) { fprintf(stderr, "bad n %d\n", n); return 2; }
            T = n * (n - 1) * (n - 2) / 6; seen = calloc(T, 1); tri = malloc(sizeof(int[3]) * T);
            int t = 0; for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { tri[t][0] = a; tri[t][1] = b; tri[t][2] = c; t++; }
        }
        lines++;
        int ok = (k == n);
        if (ok) { for (int i = 0; i < n; i++) pos[i] = -1;
            for (int i = 0; i < n; i++) { int v = perm[i]; if (v < 1 || v > n || pos[v - 1] >= 0) { ok = 0; break; } pos[v - 1] = i; } }
        if (!ok) { bad++; continue; }
        key_t2 K = {0, 0};
        for (int i = 0; i < n; i++) { uint64_t v = (uint64_t)(perm[i] - 1); if (i < 12) K.hi |= v << (5 * i); else K.lo |= v << (5 * (i - 12)); }
        if ((size_t)(lines) > kcap) { kcap *= 2; keys = realloc(keys, sizeof(key_t2) * kcap); }
        keys[lines - 1 - bad] = K;
        for (int t = 0; t < T; t++) {
            int pa = pos[tri[t][0]], pb = pos[tri[t][1]], pc = pos[tri[t][2]];
            /* rank of each member within the triple: 0 top .. 2 bottom */
            int ra = (pb < pa) + (pc < pa), rb = (pa < pb) + (pc < pb);
            int pat = ra * 3 + rb; /* ra,rb determine rc; 6 of 9 codes used */
            /* map to 6-bit index */
            static const int idx[9] = {-1, 0, 1, 2, -1, 3, 4, 5, -1};
            seen[t] |= (unsigned char)(1u << idx[pat]);
        }
    }
    long good = lines - bad;
    qsort(keys, good, sizeof(key_t2), cmpk);
    long distinct = good > 0 ? 1 : 0;
    for (long i = 1; i < good; i++) if (cmpk(&keys[i], &keys[i - 1])) distinct++;
    long viol = 0;
    /* pattern code -> (ra, rb, rc) */
    static const int RA[6] = {0, 0, 1, 1, 2, 2}, RB[6] = {1, 2, 0, 2, 0, 1};
    for (int t = 0; t < T; t++) {
        int occ[3][3] = {{0}}; /* occ[member][rank] */
        for (int q = 0; q < 6; q++) if (seen[t] >> q & 1) { int ra = RA[q], rb = RB[q], rc = 3 - ra - rb; occ[0][ra] = occ[1][rb] = occ[2][rc] = 1; }
        int okc = 0; for (int s = 0; s < 3; s++) for (int r = 0; r < 3; r++) if (!occ[s][r]) okc = 1;
        if (!okc) viol++;
    }
    printf("n %d lines %ld distinct %ld triples %d violations %ld bad_lines %ld\n", n, lines, distinct, T, viol, bad);
    int pass = (lines > 0 && bad == 0 && distinct == lines && viol == 0);
    printf("%s\n", pass ? "PASS" : "FAIL");
    return pass ? 0 : 1;
}
