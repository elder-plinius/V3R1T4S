/* Self-break check, written from the bank definition only: enumerate EVERY vector of
 * N = span(S)^perp over GF(3) (all 3^dimN - 1 nonzero GF(3) combinations of the basis written by sb_prep.py, odometer
 * order, no sampling, no cap), histogram the symplectic weights (positions i with x_i != 0 or z_i != 0), and for every
 * vector of weight <= T decide exactly whether it lies in the isotropic part I = span(S) ∩ N, using
 * v in I  <=>  v in N and <v, b> = 0 for every basis vector b of N (as span(S) = N^perp).
 * d_EA = the least weight carried by a vector of N outside I.
 * Vectors are bitsliced: bit j of p1 (p2) is set when trit j is 1 (2); trits 0..n-1 are x, n..2n-1 are z; n <= 32.
 * Usage: sb_enum T < basis.txt */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int n, dimN;
static uint64_t B1[64], B2[64];
static int Bt[64][64];

static inline void add3(uint64_t a1, uint64_t a2, uint64_t c1, uint64_t c2, uint64_t *r1, uint64_t *r2) {
    *r1 = (a1 & ~(c1 | c2)) | (c1 & ~(a1 | a2)) | (a2 & c2);
    *r2 = (a2 & ~(c1 | c2)) | (c2 & ~(a1 | a2)) | (a1 & c1);
}
static int trit(uint64_t p1, uint64_t p2, int j) { return ((p1 >> j) & 1) ? 1 : (((p2 >> j) & 1) ? 2 : 0); }

int main(int argc, char **argv) {
    int T = argc > 1 ? atoi(argv[1]) : 0;
    /* self-test of add3 on all 9 trit pairs */
    for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) {
        uint64_t r1, r2;
        add3(a == 1, a == 2, b == 1, b == 2, &r1, &r2);
        int r = r1 ? 1 : (r2 ? 2 : 0);
        if (r != (a + b) % 3 || (r1 && r2)) { printf("add3 self-test FAILED %d+%d\n", a, b); return 1; }
    }
    if (scanf("%d %d", &n, &dimN) != 2 || n > 32 || dimN > 40) { printf("bad input\n"); return 1; }
    for (int i = 0; i < dimN; i++) {
        B1[i] = B2[i] = 0;
        for (int j = 0; j < 2 * n; j++) {
            int t; if (scanf("%d", &t) != 1) { printf("bad input\n"); return 1; }
            t %= 3; Bt[i][j] = t;
            if (t == 1) B1[i] |= 1ULL << j; else if (t == 2) B2[i] |= 1ULL << j;
        }
    }
    uint64_t maskn = (n == 32) ? 0xFFFFFFFFULL : ((1ULL << n) - 1);
    static uint64_t hist[65], inI[65], outI[65];
    int dig[64] = {0};
    uint64_t v1 = 0, v2 = 0, steps = 0;
    int wit_w = 999; int wit[64];
    for (;;) {
        int i = 0;
        for (;;) {
            if (i == dimN) goto done;
            uint64_t r1, r2; add3(v1, v2, B1[i], B2[i], &r1, &r2); v1 = r1; v2 = r2;
            if (++dig[i] == 3) { dig[i] = 0; i++; continue; }
            break;
        }
        steps++;
        uint64_t nz = v1 | v2;
        int w = __builtin_popcountll((nz & maskn) | (nz >> n));
        hist[w]++;
        if (w <= T) {
            int v[64];
            for (int j = 0; j < 2 * n; j++) v[j] = trit(v1, v2, j);
            int iso = 1;
            for (int b = 0; b < dimN && iso; b++) {
                int sp = 0;
                for (int j = 0; j < n; j++) sp += v[j] * Bt[b][n + j] - v[n + j] * Bt[b][j];
                if (((sp % 3) + 3) % 3) iso = 0;
            }
            if (iso) inI[w]++; else { outI[w]++; if (w < wit_w) { wit_w = w; for (int j = 0; j < 2 * n; j++) wit[j] = v[j]; } }
        }
    }
done:
    printf("n=%d dimN=%d nonzero vectors enumerated=%llu (expected 3^%d - 1)\n", n, dimN, (unsigned long long)steps, dimN);
    printf("weight histogram (symplectic weight: count):");
    for (int w = 0; w <= n; w++) if (hist[w]) printf(" %d:%llu", w, (unsigned long long)hist[w]);
    printf("\n");
    int dEA = -1;
    for (int w = 0; w <= T && w <= n; w++) if (hist[w]) {
        printf("weight %d: in isotropic part %llu, outside %llu\n", w, (unsigned long long)inI[w], (unsigned long long)outI[w]);
        if (outI[w] && dEA < 0) dEA = w;
    }
    if (dEA >= 0) {
        printf("d_EA = %d (least weight of a vector of N outside I)\nwitness x|z:", dEA);
        for (int j = 0; j < 2 * n; j++) printf("%s%d", j == n ? " | " : " ", wit[j]);
        printf("\n");
    } else printf("no vector of N outside I has weight <= %d: d_EA > %d\n", T, T);
    return 0;
}
