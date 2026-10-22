/* mycheck.c -- independent Condorcet-domain checker (lens local-search, run 2026-10-17-2220).
 * Same semantics as RUN/code/cdcheck.py (checker of record): reads one linear order per line (alternatives 1..n
 * separated by spaces or commas, most preferred first; blank lines and lines starting with # ignored), from a file
 * path or "-" for stdin (use gzip -dc FILE.gz | mycheck -).  Checks:
 *   1. every line is a permutation of 1..n (n taken from the first line);
 *   2. all orders distinct (packs each order into 128 bits, sorts, compares neighbours);
 *   3. every triple a<b<c satisfies a never condition: for each triple we record which of its 6 relative orders
 *      occur (bitmask), then test whether some member is never top, never middle or never bottom.
 * Usage: mycheck FILE|- [--expect-n N] [--min-size M] [--assign OUT.txt]
 *   (--assign: also write one satisfied never condition per triple, a by-product, not part of the check)
 * Prints: n, lines, distinct, triples, violations, then PASS/FAIL (exit 0 / 1).
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
    if (argc < 2) { fprintf(stderr, "usage: mycheck FILE|- [--expect-n N] [--min-size M]\n"); return 2; }
    int expn = -1; long long mins = -1; const char *apath = NULL;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--expect-n") && i + 1 < argc) expn = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--min-size") && i + 1 < argc) mins = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--assign") && i + 1 < argc) apath = argv[++i];
    }
    FILE *f = strcmp(argv[1], "-") ? fopen(argv[1], "r") : stdin;
    if (!f) { perror(argv[1]); return 2; }
    char line[4096];
    int n = -1, nt = 0;
    int (*T)[3] = NULL; unsigned char *seen = NULL;
    size_t cap = 1 << 20, m = 0; key_t2 *keys = malloc(cap * sizeof(key_t2));
    long long bad_perm = 0, lineno = 0;
    while (fgets(line, sizeof line, f)) {
        lineno++;
        char *p = line; while (*p == ' ' || *p == '\t') p++;
        if (*p == '\n' || *p == '\r' || *p == 0 || *p == '#') continue;
        int ord[64], k = 0, okline = 1;
        while (*p && *p != '\n' && *p != '\r') {
            if (*p == ' ' || *p == ',' || *p == '\t') { p++; continue; }
            if (*p < '0' || *p > '9') { okline = 0; break; }
            int v = 0; while (*p >= '0' && *p <= '9') { v = v * 10 + (*p - '0'); p++; }
            if (k >= 64) { okline = 0; break; }
            ord[k++] = v;
        }
        if (n < 0) {
            n = k;
            if (n < 3 || n > 25) { fprintf(stderr, "unsupported n %d\n", n); return 2; }
            nt = n * (n - 1) * (n - 2) / 6;
            T = malloc(sizeof(int[3]) * nt); seen = calloc(nt, 1);
            int t = 0;
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { T[t][0] = a; T[t][1] = b; T[t][2] = c; t++; }
        }
        int pos[64]; for (int i = 0; i < n; i++) pos[i] = -1;
        if (okline && k == n) {
            for (int i = 0; i < n; i++) { int v = ord[i]; if (v < 1 || v > n || pos[v - 1] >= 0) { okline = 0; break; } pos[v - 1] = i; }
        } else okline = 0;
        if (!okline) { if (bad_perm < 5) fprintf(stdout, "  line %lld is not a permutation of 1..%d\n", lineno, n); bad_perm++; continue; }
        /* pack the first n-1 entries (the last is determined), 5 bits each, value-1; n <= 25 fits 2 x 60 bits */
        key_t2 kk = {0, 0};
        for (int i = 0; i < n - 1; i++) { uint64_t v = (uint64_t)(ord[i] - 1); if (i < 12) kk.hi |= v << (5 * i); else kk.lo |= v << (5 * (i - 12)); }
        if (m == cap) { cap *= 2; keys = realloc(keys, cap * sizeof(key_t2)); if (!keys) { fprintf(stderr, "oom\n"); return 2; } }
        keys[m++] = kk;
        for (int t = 0; t < nt; t++) {
            int pa = pos[T[t][0]], pb = pos[T[t][1]], pc = pos[T[t][2]];
            int code = (pa < pb) | ((pa < pc) << 1) | ((pb < pc) << 2); /* 6 of 8 codes occur */
            seen[t] |= (unsigned char)(1u << code);
        }
    }
    if (n < 0) { printf("empty domain\nFAIL\n"); return 1; }
    qsort(keys, m, sizeof(key_t2), cmpk);
    size_t distinct = m ? 1 : 0; for (size_t i = 1; i < m; i++) if (cmpk(&keys[i], &keys[i - 1])) distinct++;
    /* for each comparison code, rank of a, b, c within the triple (0 top) */
    int rk[8][3];
    for (int code = 0; code < 8; code++) {
        int ab = code & 1, ac = (code >> 1) & 1, bc = (code >> 2) & 1;
        rk[code][0] = (!ab) + (!ac); rk[code][1] = ab + (!bc); rk[code][2] = ac + bc;
    }
    long long viol = 0;
    if (apath) { /* optional: write one satisfied never condition per triple ("a b c iNj"), peak-pit first */
        FILE *af = fopen(apath, "w"); int pref[9] = {2, 6, 3, 5, 0, 8, 1, 4, 7}; long amb = 0;
        for (int t = 0; t < nt; t++) {
            int nsat = 0, first = -1;
            for (int q = 0; q < 9; q++) {
                int s = pref[q] / 3, p = pref[q] % 3, hit = 0;
                for (int code = 0; code < 8; code++) if (((seen[t] >> code) & 1) && rk[code][s] == p) { hit = 1; break; }
                if (!hit) { nsat++; if (first < 0) first = pref[q]; }
            }
            if (nsat > 1) amb++;
            if (first >= 0) fprintf(af, "%d %d %d %dN%d\n", T[t][0] + 1, T[t][1] + 1, T[t][2] + 1, first / 3 + 1, first % 3 + 1);
        }
        fclose(af); printf("assignment written to %s; triples with more than one satisfied condition: %ld\n", apath, amb);
    }
    for (int t = 0; t < nt; t++) {
        int okc = 0;
        for (int s = 0; s < 3 && !okc; s++) for (int p = 0; p < 3 && !okc; p++) {
            int hit = 0;
            for (int code = 0; code < 8; code++) if ((seen[t] >> code) & 1) if (rk[code][s] == p) { hit = 1; break; }
            if (!hit) okc = 1;
        }
        if (!okc) { if (viol < 5) printf("  triple (%d,%d,%d) satisfies no never condition\n", T[t][0] + 1, T[t][1] + 1, T[t][2] + 1); viol++; }
    }
    printf("n %d lines %zu distinct %zu triples %d violations %lld bad_lines %lld\n", n, m, distinct, nt, viol, bad_perm);
    int fail = viol || bad_perm || distinct != m || (expn >= 0 && n != expn) || (mins >= 0 && (long long)distinct < mins);
    if (distinct != m) printf("  %zu duplicate orders\n", m - distinct);
    printf("%s\n", fail ? "FAIL" : "PASS");
    return fail;
}
