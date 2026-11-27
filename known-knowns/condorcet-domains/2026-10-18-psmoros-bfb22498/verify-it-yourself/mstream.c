/* mstream: main-session streaming checker (run 2026-10-18-0558), separate from mdom.
 * usage: mstream N assignment.txt MINSIZE < orders
 * Checks every line: exactly N tokens 1..N, each once, single spaces, LF, no leading zeros; the stream strictly
 * increasing in numeric-lexicographic order (so all lines are distinct); every order obeys every line of the
 * assignment (one never condition per triple, so every triple of the set satisfies a never condition).
 * Independently of the assignment it also records, per triple, which of the 6 patterns occur, and counts the
 * triples whose occurring patterns satisfy no never condition at all.
 * Prints a summary and PASS iff 0 errors and lines >= MINSIZE. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static int T[5000][3];       /* triple a<b<c */
static int F[5000], J[5000]; /* forbidden element and position */
static unsigned char pat[5000];
static int nt = 0;

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: mstream N assignment.txt MINSIZE < orders\n"); return 2; }
    n = atoi(argv[1]);
    unsigned long long minsize = strtoull(argv[3], 0, 10);
    FILE *f = fopen(argv[2], "r");
    if (!f) { perror(argv[2]); return 2; }
    static unsigned char seen[32][32][32];
    char ln[256];
    while (fgets(ln, sizeof ln, f)) {
        int a, b, c, i, j; char N, extra;
        if (sscanf(ln, "%d %d %d %d%c%d %c", &a, &b, &c, &i, &N, &j, &extra) != 6 || N != 'N' ||
            !(1 <= a && a < b && b < c && c <= n) || i < 1 || i > 3 || j < 1 || j > 3 || seen[a][b][c]++ || nt >= 5000) {
            fprintf(stderr, "bad assignment line: %s", ln); return 3;
        }
        T[nt][0] = a; T[nt][1] = b; T[nt][2] = c;
        F[nt] = (i == 1) ? a : (i == 2) ? b : c;
        J[nt] = j;
        nt++;
    }
    fclose(f);
    if (nt != n * (n - 1) * (n - 2) / 6) { fprintf(stderr, "assignment has %d triples, need C(n,3)\n", nt); return 3; }

    unsigned long long lines = 0, malformed = 0, nonincreasing = 0, disobey_lines = 0;
    int prev[32], cur[32], pos[33], have_prev = 0;
    static char buf[4096];
    while (fgets(buf, sizeof buf, stdin)) {
        lines++;
        size_t L = strlen(buf);
        int ok = (L > 0 && buf[L - 1] == '\n');
        int k = 0; char *p = buf; int used[33]; memset(used, 0, sizeof used);
        while (ok && k < n) {
            if (*p < '1' || *p > '9') { ok = 0; break; }
            int v = 0, digits = 0;
            while (*p >= '0' && *p <= '9') { v = v * 10 + (*p - '0'); p++; digits++; }
            if (digits > 2 || v < 1 || v > n || used[v]) { ok = 0; break; }
            used[v] = 1; cur[k++] = v;
            if (k < n) { if (*p != ' ') { ok = 0; break; } p++; }
        }
        if (ok && !(k == n && *p == '\n' && p[1] == 0)) ok = 0;
        if (!ok) { malformed++; continue; }
        if (have_prev) {
            int d = 0;
            while (d < n && prev[d] == cur[d]) d++;
            if (d == n || cur[d] < prev[d]) nonincreasing++;
        }
        memcpy(prev, cur, sizeof(int) * n); have_prev = 1;
        for (int r = 0; r < n; r++) pos[cur[r]] = r;
        int bad = 0;
        for (int t = 0; t < nt; t++) {
            int a = T[t][0], b = T[t][1], c = T[t][2];
            int pa = pos[a], pb = pos[b], pc = pos[c];
            /* pattern = which of a,b,c is top / middle: index 0..5 */
            int ra = (pb < pa) + (pc < pa), rb = (pa < pb) + (pc < pb);
            pat[t] |= (unsigned char)(1u << (ra * 2 + (rb > ra ? rb - 1 : rb)));
            int x = F[t], px = pos[x];
            int rank = 1 + (pa < px) + (pb < px) + (pc < px);
            if (rank == J[t]) bad = 1;
        }
        if (bad) disobey_lines++;
    }
    /* never conditions from the observed patterns: element e (0,1,2 = a,b,c) at rank r (0 top,1 mid,2 bottom) */
    unsigned long long nocond = 0;
    for (int t = 0; t < nt; t++) {
        int sat = 0;
        for (int e = 0; e < 3 && !sat; e++)
            for (int r = 0; r < 3 && !sat; r++) {
                int occurs = 0;
                for (int ra = 0; ra < 3; ra++)
                    for (int rb = 0; rb < 3; rb++) {
                        if (ra == rb) continue;
                        int rc = 3 - ra - rb;
                        int idx = ra * 2 + (rb > ra ? rb - 1 : rb);
                        if (!(pat[t] >> idx & 1)) continue;
                        int re = (e == 0) ? ra : (e == 1) ? rb : rc;
                        if (re == r) occurs = 1;
                    }
                if (!occurs) sat = 1;
            }
        if (!sat) nocond++;
    }
    int pass = (malformed == 0 && nonincreasing == 0 && disobey_lines == 0 && nocond == 0 && lines >= minsize);
    printf("n %d lines %llu malformed %llu nonincreasing %llu disobeying_lines %llu triples %d triples_without_never_condition %llu minsize %llu\n%s\n",
           n, lines, malformed, nonincreasing, disobey_lines, nt, nocond, minsize, pass ? "PASS" : "FAIL");
    return pass ? 0 : 1;
}
