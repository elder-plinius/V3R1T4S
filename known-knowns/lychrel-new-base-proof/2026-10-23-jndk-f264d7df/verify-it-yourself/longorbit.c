/* Independent long-orbit validator (no shared code with rle_check.py).
   Input file: line 1 "b p t0 seedlen", line 2 seed digits MSB first, then p lines "nruns d a k d a k ...".
   For t = 0..STEPS: x_t from exact reverse-and-add; checks x_t is not a palindrome for t >= 1, and for t >= t0 that
   x_t equals template T_{(t-t0) mod p} at parameter m = (t-t0) div p (run lengths a + k m). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); long STEPS = atol(argv[2]);
    int b, p, t0, sl; fscanf(f, "%d %d %d %d", &b, &p, &t0, &sl);
    long cap = sl + STEPS + 16;
    unsigned char *x = malloc(cap), *y = malloc(cap), *e = malloc(cap);
    unsigned char *msb = malloc(sl); for (int i = 0; i < sl; i++) { int d; fscanf(f, "%d", &d); msb[i] = d; }
    long L = sl; for (long i = 0; i < L; i++) x[i] = msb[L - 1 - i];   /* LSB first */
    int nr[64]; int *D[64]; long *A[64], *K[64];
    for (int i = 0; i < p; i++) { fscanf(f, "%d", &nr[i]); D[i] = malloc(nr[i] * sizeof(int)); A[i] = malloc(nr[i] * sizeof(long)); K[i] = malloc(nr[i] * sizeof(long));
        for (int r = 0; r < nr[i]; r++) fscanf(f, "%d %ld %ld", &D[i][r], &A[i][r], &K[i][r]); }
    long mismatches = 0, pals = 0, checked = 0;
    for (long t = 0; t <= STEPS; t++) {
        if (t >= 1) { int pal = 1; for (long i = 0; i < L / 2; i++) if (x[i] != x[L - 1 - i]) { pal = 0; break; } if (pal) { pals++; printf("PALINDROME at t=%ld\n", t); } }
        if (t >= t0) {
            long m = (t - t0) / p; int i = (t - t0) % p; long n = 0;
            for (int r = 0; r < nr[i]; r++) { long len = A[i][r] + K[i][r] * m; for (long q = 0; q < len; q++) e[n++] = D[i][r]; }
            int ok = (n == L); for (long q = 0; ok && q < n; q++) if (e[q] != x[L - 1 - q]) ok = 0;
            if (!ok) { mismatches++; if (mismatches < 5) printf("MISMATCH at t=%ld (m=%ld i=%d) len %ld vs %ld\n", t, m, i, L, n); }
            checked++;
        }
        if (t == STEPS) break;
        int c = 0; for (long i = 0; i < L; i++) { int v = x[i] + x[L - 1 - i] + c; y[i] = v % b; c = v / b; }
        long L2 = L; if (c) y[L2++] = c;
        unsigned char *tmp = x; x = y; y = tmp; L = L2;
    }
    printf("RESULT base=%d steps=%ld final_len=%ld template_checks=%ld mismatches=%ld palindromes=%ld\n", b, STEPS, L, checked, mismatches, pals);
    return (mismatches || pals) ? 1 : 0;
}
