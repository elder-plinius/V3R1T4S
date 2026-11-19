#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// Format of plain-text exact matrix file (.kmat):
// Line 1: m n D
// Next m lines: n signed 64-bit integers P[i][j]
// Represents exact rational matrix A[i][j] = P[i][j] / D.

static void print_i128(__int128 v) {
    if (v < 0) { putchar(45); v = -v; }
    char buf[64]; int pos = 0;
    if (v == 0) buf[pos++] = 48;
    while (v > 0) { buf[pos++] = (char)(48 + (int)(v % 10)); v /= 10; }
    while (pos > 0) putchar(buf[--pos]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "Usage: %s <file.kmat>\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("fopen"); return 2; }
    int m, n;
    long long D_ll;
    if (fscanf(f, "%d %d %lld", &m, &n, &D_ll) != 3 || m <= 0 || n <= 0 || n > 40 || m > 256 || D_ll <= 0) {
        fprintf(stderr, "Invalid header\n"); return 2;
    }
    __int128 D = (__int128)D_ll;
    __int128 D2 = D * D;
    long long P[256][40];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (fscanf(f, "%lld", &P[i][j]) != 1) { fprintf(stderr, "Invalid entry\n"); return 2; }
        }
    }
    fclose(f);

    // 1. Exact column squared Euclidean norm check
    for (int j = 0; j < n; j++) {
        __int128 sq = 0;
        for (int i = 0; i < m; i++) {
            __int128 v = (__int128)P[i][j];
            sq += v * v;
        }
        if (sq == 0) { fprintf(stderr, "FAIL: column %d is all zero\n", j); return 1; }
        if (sq > D2) {
            fprintf(stderr, "FAIL: column %d norm^2 > 1\n", j);
            return 1;
        }
    }

    // 2. Exhaustive Gray-code enumeration over 2^{n-1} sign vectors with x_0 = +1
    __int128 S[256];
    int sgn[40];
    for (int j = 0; j < n; j++) sgn[j] = 1;
    for (int i = 0; i < m; i++) {
        __int128 s = 0;
        for (int j = 0; j < n; j++) s += (__int128)P[i][j];
        S[i] = s;
    }

    __int128 best_min = 0;
    for (int i = 0; i < m; i++) {
        __int128 a = S[i] < 0 ? -S[i] : S[i];
        if (a > best_min) best_min = a;
    }
    uint64_t best_mask = 0; // bit (j-1) == 1 means x_j = -1

    uint64_t total = 1ULL << (n - 1);
    uint64_t gray_prev = 0;
    for (uint64_t k = 1; k < total; k++) {
        uint64_t gray = k ^ (k >> 1);
        uint64_t diff = gray ^ gray_prev;
        int bit = __builtin_ctzll(diff);
        int col = bit + 1;
        gray_prev = gray;
        if (sgn[col] == 1) {
            sgn[col] = -1;
            for (int i = 0; i < m; i++) S[i] -= (__int128)2 * (__int128)P[i][col];
        } else {
            sgn[col] = 1;
            for (int i = 0; i < m; i++) S[i] += (__int128)2 * (__int128)P[i][col];
        }
        __int128 mx = 0;
        for (int i = 0; i < m; i++) {
            __int128 a = S[i] < 0 ? -S[i] : S[i];
            if (a > mx) mx = a;
        }
        if (mx < best_min) {
            best_min = mx;
            best_mask = gray;
        }
    }

    // 3. Direct re-evaluation of witness sign vector
    __int128 check_mx = 0;
    for (int i = 0; i < m; i++) {
        __int128 s = (__int128)P[i][0];
        for (int j = 1; j < n; j++) {
            int xj = ((best_mask >> (j - 1)) & 1ULL) ? -1 : 1;
            s += (__int128)xj * (__int128)P[i][j];
        }
        __int128 a = s < 0 ? -s : s;
        if (a > check_mx) check_mx = a;
    }
    if (check_mx != best_min) { fprintf(stderr, "INTERNAL MISMATCH\n"); return 2; }

    int pass_p1 = (n <= 15) && (best_min >= 2 * D);
    int pass_p2 = (n <= 15) && (1000 * best_min > 2006 * D);
    int pass_full = (best_min > D) && ((best_min - D) * (best_min - D) > 2 * D2);

    printf("C_VERIFIER: m=%d n=%d exact_disc=", m, n);
    print_i128(best_min); putchar(47); print_i128(D);
    printf(" approx=%.12Lf | p1=%d p2=%d full=%d\n",
           (long double)best_min / (long double)D, pass_p1, pass_p2, pass_full);
    return 0;
}
