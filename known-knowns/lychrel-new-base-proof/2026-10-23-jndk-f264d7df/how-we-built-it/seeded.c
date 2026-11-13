/* Seeded interior hunt. For each spec line (b p a L[a] R[a] lb rb), and every interior I of length m <= mmax (all
   b^m strings, cumulative cap), build x = L . lb^N . I . rb^N . reverse(R) (R[0] is the least significant digit),
   iterate reverse-and-add T steps (stop at palindrome) and test run-length-skeleton periodicity in the last W steps.
   Prints HIT lines (spec index, interior digits, period). Discovery only; proofs come from rle_check.py.
   usage: seeded specs.txt N T cap */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXD 8000
#define W 60
#define PMAX 20
static unsigned char A[MAXD + 2], Bf[MAXD + 2];
static int ra(unsigned char *x, int L, unsigned char *y, int b) {
    int c = 0;
    for (int i = 0; i < L; i++) { int v = x[i] + x[L - 1 - i] + c; y[i] = v % b; c = v / b; }
    if (c) { y[L] = c; return L + 1; }
    return L;
}
static int ispal(unsigned char *x, int L) { for (int i = 0; i < L / 2; i++) if (x[i] != x[L - 1 - i]) return 0; return 1; }
static uint64_t skel(unsigned char *x, int L, int *nlong, long *ls) {
    uint64_t h = 1469598103934665603ULL; int i = 0; *nlong = 0; *ls = 0;
    while (i < L) { int j = i; while (j < L && x[j] == x[i]) j++; int n = j - i, code = n < 3 ? n : 255;
        if (n >= 3) { (*nlong)++; *ls += n; } h ^= (uint64_t)(x[i] * 256 + code); h *= 1099511628211ULL; i = j; }
    return h;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); int N = atoi(argv[2]), T = atoi(argv[3]); long cap = atol(argv[4]);
    char line[4096]; int si = 0;
    while (fgets(line, sizeof line, f)) {
        int b, p, a, L[64], R[64], lb, rb; char *s = line; int nread;
        if (sscanf(s, "%d %d %d%n", &b, &p, &a, &nread) < 3) continue; s += nread;
        for (int i = 0; i < a; i++) { sscanf(s, "%d%n", &L[i], &nread); s += nread; }
        for (int i = 0; i < a; i++) { sscanf(s, "%d%n", &R[i], &nread); s += nread; }
        sscanf(s, "%d %d", &lb, &rb);
        long tried = 0, surv = 0, hits = 0; int mreached = 0;
        for (int m = 0; m <= 12; m++) {
            long cnt = 1; for (int i = 0; i < m; i++) cnt *= b;
            if (tried + cnt > cap) break;
            mreached = m;
            int I[16];
            for (long code = 0; code < cnt; code++) {
                long c = code; for (int i = 0; i < m; i++) { I[i] = c % b; c /= b; }
                /* build MSB-first then store LSB-first */
                unsigned char msb[MAXD]; int Lx = 0;
                for (int i = 0; i < a; i++) msb[Lx++] = L[i];
                for (int i = 0; i < N; i++) msb[Lx++] = lb;
                for (int i = 0; i < m; i++) msb[Lx++] = I[i];
                for (int i = 0; i < N; i++) msb[Lx++] = rb;
                for (int i = a - 1; i >= 0; i--) msb[Lx++] = R[i];
                for (int i = 0; i < Lx; i++) A[i] = msb[Lx - 1 - i];
                unsigned char *x = A, *y = Bf; int Ln = Lx, pal = 0, t;
                uint64_t hs[W]; int nl[W]; long lsum[W]; int filled = 0;
                for (t = 1; t <= T; t++) {
                    if (Ln >= MAXD - 1) break;
                    Ln = ra(x, Ln, y, b); unsigned char *tmp = x; x = y; y = tmp;
                    if (ispal(x, Ln)) { pal = 1; break; }
                    if (t > T - W) { int k = t - (T - W) - 1; hs[k] = skel(x, Ln, &nl[k], &lsum[k]); filled = k + 1; }
                }
                tried++;
                if (pal || t <= T) continue;
                surv++;
                for (int pp = 1; pp <= PMAX; pp++) {
                    int ok = 1; for (int k = 0; k + pp < filled; k++) if (hs[k] != hs[k + pp]) { ok = 0; break; }
                    if (ok && nl[filled - 1] > 0 && lsum[filled - 1] > lsum[filled - 1 - pp]) {
                        if (hits < 5) { printf("HIT spec=%d b=%d m=%d I=", si, b, m); for (int i = 0; i < m; i++) printf("%d.", I[i]);
                        printf(" period=%d len=%d\n", pp, Ln); } hits++; break;
                    }
                }
            }
        }
        printf("SPEC %d b=%d p=%d a=%d mmax=%d tried=%ld survivors=%ld hits=%ld\n", si, b, p, a, mreached, tried, surv, hits);
        fflush(stdout); si++;
    }
    return 0;
}
