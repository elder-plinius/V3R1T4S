/* mdom: main-session tool (run 2026-10-18-0558), written from the definition.
 * Input: n and a never-condition assignment A, one line per triple "a b c iNj" (1 <= a < b < c <= n):
 *   the i-th smallest alternative of the triple is never at position j within the triple (1 top, 2 middle, 3 bottom).
 * D(A) = all linear orders of 1..n (most preferred first) that obey every line of A.
 *   mdom count N A   prints |D(A)| (memoised DFS over the set S of already placed alternatives, unsigned 128-bit)
 *   mdom enum  N A   prints every order of D(A), numeric-lexicographic, one per line, single spaces, LF
 * When x is placed after the set S, its position inside triple {x,a,b} is 1 + |S intersect {a,b}|.
 * The loader rejects A unless every one of the C(n,3) triples appears exactly once. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
static int n;
static int ncon[32];
static uint32_t cmask[32][512];
static int cpos[32][512];

#define HBITS 22
#define HSIZE (1u << HBITS)
static uint32_t *hkey;
static u128 *hval;

static int allowed(int x, uint32_t S) {
    for (int k = 0; k < ncon[x]; k++)
        if (1 + __builtin_popcount(S & cmask[x][k]) == cpos[x][k]) return 0;
    return 1;
}

static u128 count(uint32_t S) {
    uint32_t full = (n == 32) ? 0xffffffffu : ((1u << n) - 1);
    if (S == full) return 1;
    uint32_t h = (S * 2654435761u) >> (32 - HBITS);
    while (hkey[h] != 0xffffffffu) {
        if (hkey[h] == S) return hval[h];
        h = (h + 1) & (HSIZE - 1);
    }
    u128 tot = 0;
    for (int x = 1; x <= n; x++) {
        uint32_t b = 1u << (x - 1);
        if (!(S & b) && allowed(x, S)) tot += count(S | b);
    }
    h = (S * 2654435761u) >> (32 - HBITS);
    while (hkey[h] != 0xffffffffu) h = (h + 1) & (HSIZE - 1);
    hkey[h] = S;
    hval[h] = tot;
    return tot;
}

static int order[32];
static char obuf[1 << 20];
static size_t olen = 0;
static unsigned long long emitted = 0;

static void flush_out(void) { fwrite(obuf, 1, olen, stdout); olen = 0; }

static void emit(void) {
    if (olen > sizeof(obuf) - 256) flush_out();
    for (int i = 0; i < n; i++) {
        int v = order[i];
        if (v >= 10) obuf[olen++] = (char)('0' + v / 10);
        obuf[olen++] = (char)('0' + v % 10);
        obuf[olen++] = (i == n - 1) ? '\n' : ' ';
    }
    emitted++;
}

static void enumerate(uint32_t S, int d) {
    if (d == n) { emit(); return; }
    for (int x = 1; x <= n; x++) {
        uint32_t b = 1u << (x - 1);
        if ((S & b) || !allowed(x, S)) continue;
        if (count(S | b) == 0) continue;
        order[d] = x;
        enumerate(S | b, d + 1);
    }
}

static void print_u128(u128 v) {
    char s[64]; int i = 63; s[i] = 0;
    if (v == 0) s[--i] = '0';
    while (v) { s[--i] = (char)('0' + (int)(v % 10)); v /= 10; }
    printf("%s", s + i);
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: mdom count|enum N assignment.txt\n"); return 2; }
    n = atoi(argv[2]);
    if (n < 3 || n > 31) { fprintf(stderr, "bad n\n"); return 2; }
    FILE *f = fopen(argv[3], "r");
    if (!f) { perror(argv[3]); return 2; }
    static unsigned char seen[32][32][32];
    memset(seen, 0, sizeof seen);
    char line[256];
    long lines = 0;
    while (fgets(line, sizeof line, f)) {
        int a, b, c, i, j; char N, extra;
        if (sscanf(line, "%d %d %d %d%c%d %c", &a, &b, &c, &i, &N, &j, &extra) != 6 || N != 'N'
            || !(1 <= a && a < b && b < c && c <= n) || i < 1 || i > 3 || j < 1 || j > 3) {
            fprintf(stderr, "malformed assignment line %ld: %s", lines + 1, line); return 3;
        }
        if (seen[a][b][c]++) { fprintf(stderr, "duplicate triple %d %d %d\n", a, b, c); return 3; }
        int t[3] = {a, b, c};
        int x = t[i - 1], o1 = t[(i) % 3], o2 = t[(i + 1) % 3];
        if (ncon[x] >= 512) { fprintf(stderr, "too many constraints\n"); return 3; }
        cmask[x][ncon[x]] = (1u << (o1 - 1)) | (1u << (o2 - 1));
        cpos[x][ncon[x]] = j;
        ncon[x]++;
        lines++;
    }
    fclose(f);
    long want = (long)n * (n - 1) * (n - 2) / 6;
    if (lines != want) { fprintf(stderr, "assignment has %ld lines, C(n,3) = %ld\n", lines, want); return 3; }
    hkey = malloc(sizeof(uint32_t) * HSIZE);
    hval = malloc(sizeof(u128) * HSIZE);
    if (!hkey || !hval) { fprintf(stderr, "no memory\n"); return 4; }
    memset(hkey, 0xff, sizeof(uint32_t) * HSIZE);
    u128 total = count(0);
    if (!strcmp(argv[1], "count")) {
        printf("n %d assignment_lines %ld count ", n, lines);
        print_u128(total);
        printf("\n");
    } else if (!strcmp(argv[1], "enum")) {
        enumerate(0, 0);
        flush_out();
        fprintf(stderr, "mdom enum n %d emitted %llu dp_count ", n, emitted);
        u128 t = total; char s[64]; int k = 63; s[k] = 0; if (!t) s[--k] = '0';
        while (t) { s[--k] = (char)('0' + (int)(t % 10)); t /= 10; }
        fprintf(stderr, "%s\n", s + k);
    } else { fprintf(stderr, "unknown mode\n"); return 2; }
    return 0;
}
