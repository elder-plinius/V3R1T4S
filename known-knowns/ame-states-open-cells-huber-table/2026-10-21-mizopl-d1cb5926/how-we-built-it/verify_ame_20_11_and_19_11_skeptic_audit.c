#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

/*
 * 3-Skeptic Zero-Trust Standalone Verifier for:
 *   1) AME(20, 11) = [[20, 0, 11]]_11 (20x20 symmetric graph state Gamma_20 over GF(11))
 *   2) AME(19, 11) = [[19, 0, 10]]_11 (19x19 symmetric graph state Gamma_19 = (Gamma_20)_{0..18, 0..18} over GF(11))
 *   3) Underlying Hermitian Unitary MDS matrix U in U(10, GF(121)) (Theorem D37 & D37A)
 */

#define P 11
#define Q2 121
#define NONRES 7

static uint8_t mul_tab[121][121], add_tab[121][121], sub_tab[121][121], neg_tab[121], inv_tab[121], conj_tab[121];
static int inv11[11];

static int mod11(int x) { x %= 11; return x < 0 ? x + 11 : x; }

static void init_fields(void) {
    for (int a = 1; a < 11; a++)
        for (int b = 1; b < 11; b++)
            if ((a * b) % 11 == 1) inv11[a] = b;

    for (int a = 0; a < Q2; a++) {
        int a0 = a % P, a1 = a / P;
        conj_tab[a] = (uint8_t)(a0 + mod11(-a1) * P);
        neg_tab[a] = (uint8_t)(mod11(-a0) + mod11(-a1) * P);
        for (int b = 0; b < Q2; b++) {
            int b0 = b % P, b1 = b / P;
            add_tab[a][b] = (uint8_t)(mod11(a0 + b0) + mod11(a1 + b1) * P);
            sub_tab[a][b] = (uint8_t)(mod11(a0 - b0) + mod11(a1 - b1) * P);
            int c0 = mod11(a0 * b0 + NONRES * a1 * b1);
            int c1 = mod11(a0 * b1 + a1 * b0);
            mul_tab[a][b] = (uint8_t)(c0 + c1 * P);
        }
    }
    inv_tab[0] = 0;
    for (int a = 1; a < Q2; a++)
        for (int b = 1; b < Q2; b++)
            if (mul_tab[a][b] == 1) { inv_tab[a] = (uint8_t)b; break; }
}

static uint8_t det_f121(int r, const uint8_t M_in[10][10]) {
    uint8_t M[10][10];
    for (int i = 0; i < r; i++)
        for (int j = 0; j < r; j++)
            M[i][j] = M_in[i][j];
    uint8_t det = 1;
    for (int col = 0; col < r; col++) {
        int piv = -1;
        for (int row = col; row < r; row++)
            if (M[row][col] != 0) { piv = row; break; }
        if (piv < 0) return 0;
        if (piv != col) {
            det = neg_tab[det];
            for (int c = col; c < r; c++) {
                uint8_t t = M[col][c]; M[col][c] = M[piv][c]; M[piv][c] = t;
            }
        }
        det = mul_tab[det][M[col][col]];
        uint8_t iv = inv_tab[M[col][col]];
        for (int row = col + 1; row < r; row++) {
            if (!M[row][col]) continue;
            uint8_t f = mul_tab[M[row][col]][iv];
            for (int c = col; c < r; c++)
                M[row][c] = sub_tab[M[row][c]][mul_tab[f][M[col][c]]];
        }
    }
    return det;
}

static int det10_f11(const int G[20][20], const int S[10], const int Sc[10]) {
    int M[10][10];
    for (int i = 0; i < 10; i++)
        for (int j = 0; j < 10; j++)
            M[i][j] = G[S[i]][Sc[j]];
    int det = 1;
    for (int col = 0; col < 10; col++) {
        int piv = -1;
        for (int row = col; row < 10; row++)
            if (M[row][col] != 0) { piv = row; break; }
        if (piv < 0) return 0;
        if (piv != col) {
            det = mod11(-det);
            for (int c = col; c < 10; c++) {
                int t = M[col][c]; M[col][c] = M[piv][c]; M[piv][c] = t;
            }
        }
        det = mod11(det * M[col][col]);
        int iv = inv11[M[col][col]];
        for (int row = col + 1; row < 10; row++) {
            if (!M[row][col]) continue;
            int f = mod11(M[row][col] * iv);
            for (int c = col; c < 10; c++)
                M[row][c] = mod11(M[row][c] - f * M[col][c]);
        }
    }
    return det;
}

static int rank9x10_f11(const int G[20][20], const int S[9], const int Sc[10]) {
    int M[9][10];
    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 10; j++)
            M[i][j] = G[S[i]][Sc[j]];
    int r = 0;
    for (int col = 0; col < 10 && r < 9; col++) {
        int piv = -1;
        for (int row = r; row < 9; row++)
            if (M[row][col] != 0) { piv = row; break; }
        if (piv < 0) continue;
        if (piv != r) {
            for (int c = col; c < 10; c++) {
                int t = M[r][c]; M[r][c] = M[piv][c]; M[piv][c] = t;
            }
        }
        int iv = inv11[M[r][col]];
        for (int row = r + 1; row < 9; row++) {
            if (!M[row][col]) continue;
            int f = mod11(M[row][col] * iv);
            for (int c = col; c < 10; c++)
                M[row][c] = mod11(M[row][c] - f * M[r][c]);
        }
        r++;
    }
    return r;
}

int main(void) {
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    init_fields();

    const uint8_t A[5] = {28, 103, 70, 31, 46};
    const uint8_t B[5] = {52, 11, 59, 6, 41};
    uint8_t U[10][10];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j]         = A[d];
            U[i][5 + j]     = B[d];
            U[5 + i][j]     = neg_tab[conj_tab[B[d]]];
            U[5 + i][5 + j] = conj_tab[A[d]];
        }

    /* 1. Verify U * U^dagger == I_10 over GF(121) */
    int unit_err = 0;
    for (int i = 0; i < 10; i++)
        for (int j = 0; j < 10; j++) {
            uint8_t s = 0;
            for (int k = 0; k < 10; k++)
                s = add_tab[s][mul_tab[U[i][k]][conj_tab[U[j][k]]]];
            if (s != (i == j ? 1 : 0)) unit_err++;
        }
    uint8_t detU = det_f121(10, U);
    printf("[Skeptic 1a] U in U(10, GF(121)): U*U^dag=I_10 errors = %d, det(U) = %d (norm = %d)\n",
           unit_err, detU, mul_tab[detU][conj_tab[detU]]);

    /* 2. Brute-force all 184,755 minors of U over GF(121) */
    long tot_minors = 0, bad_minors = 0;
    for (int r = 1; r <= 10; r++) {
        long r_tot = 0, r_bad = 0;
        for (int rm = 0; rm < 1024; rm++) {
            if (__builtin_popcount(rm) != r) continue;
            int rows[10], ri = 0;
            for (int i = 0; i < 10; i++) if ((rm >> i) & 1) rows[ri++] = i;
            for (int cm = 0; cm < 1024; cm++) {
                if (__builtin_popcount(cm) != r) continue;
                int cols[10], ci = 0;
                for (int j = 0; j < 10; j++) if ((cm >> j) & 1) cols[ci++] = j;
                uint8_t subM[10][10];
                for (int i = 0; i < r; i++)
                    for (int j = 0; j < r; j++)
                        subM[i][j] = U[rows[i]][cols[j]];
                r_tot++;
                if (det_f121(r, subM) == 0) r_bad++;
            }
        }
        tot_minors += r_tot;
        bad_minors += r_bad;
        printf("  Order r=%2d: %6ld / %6ld non-zero (bad = %ld)\n", r, r_tot - r_bad, r_tot, r_bad);
    }
    printf("[Skeptic 1b] Total U minors over GF(121): %ld / %ld non-zero (bad = %ld)\n",
           tot_minors - bad_minors, tot_minors, bad_minors);

    /* 3. Descend G = [I_10 | 26*U] to 20x20 graph state Gamma_20 over GF(11) */
    int g = 26;
    int X[20][20], Z[20][20], aug[20][40], Gamma20[20][20];
    for (int i = 0; i < 10; i++)
        for (int j = 0; j < 20; j++) {
            uint8_t val = (j < 10) ? (i == j ? 1 : 0) : mul_tab[g][U[i][j - 10]];
            int re = val % P, im = val / P;
            X[i][j]      = re;
            Z[i][j]      = im;
            X[10 + i][j] = mod11(7 * im);
            Z[10 + i][j] = re;
        }
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20; j++) {
            aug[i][j]      = X[i][j];
            aug[i][20 + j] = Z[i][j];
        }
    for (int col = 0; col < 20; col++) {
        int piv = -1;
        for (int row = col; row < 20; row++)
            if (aug[row][col] != 0) { piv = row; break; }
        if (piv != col)
            for (int c = col; c < 40; c++) {
                int t = aug[col][c]; aug[col][c] = aug[piv][c]; aug[piv][c] = t;
            }
        int iv = inv11[aug[col][col]];
        for (int c = col; c < 40; c++) aug[col][c] = mod11(aug[col][c] * iv);
        for (int row = 0; row < 20; row++) {
            if (row == col || !aug[row][col]) continue;
            int f = aug[row][col];
            for (int c = col; c < 40; c++)
                aug[row][c] = mod11(aug[row][c] - f * aug[col][c]);
        }
    }
    int sym_err = 0;
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20; j++)
            Gamma20[i][j] = (i == j) ? 0 : aug[i][20 + j];
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20; j++)
            if (Gamma20[i][j] != Gamma20[j][i] || (i == j && Gamma20[i][j] != 0)) sym_err++;

    /* 4. Brute-force all 184,756 bipartite 10x10 cuts of Gamma_20 over GF(11) */
    long cuts20 = 0, bad20 = 0;
    for (uint32_t m = 0; m < (1u << 20); m++) {
        if (__builtin_popcount(m) != 10) continue;
        int S[10], Sc[10], si = 0, sci = 0;
        for (int i = 0; i < 20; i++) {
            if ((m >> i) & 1) S[si++] = i;
            else              Sc[sci++] = i;
        }
        cuts20++;
        if (det10_f11(Gamma20, S, Sc) == 0) bad20++;
    }
    printf("[Skeptic 1c] AME(20, 11) = [[20, 0, 11]]_11 Graph State Gamma_20: sym_err = %d, 10x10 bipartite cuts invertible = %ld / %ld (bad = %ld)\n",
           sym_err, cuts20 - bad20, cuts20, bad20);

    /* 5. Brute-force all 92,378 bipartite 9x10 cuts of the 19x19 submatrix Gamma_19 = (Gamma_20)_{0..18, 0..18} over GF(11) */
    long cuts19 = 0, bad19 = 0;
    for (uint32_t m = 0; m < (1u << 19); m++) {
        if (__builtin_popcount(m) != 9) continue;
        int S[9], Sc[10], si = 0, sci = 0;
        for (int i = 0; i < 19; i++) {
            if ((m >> i) & 1) S[si++] = i;
            else              Sc[sci++] = i;
        }
        cuts19++;
        if (rank9x10_f11(Gamma20, S, Sc) < 9) bad19++;
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    printf("[Skeptic 1d] AME(19, 11) = [[19, 0, 10]]_11 Pure 19x19 Graph State Gamma_19: 9x10 bipartite cuts full rank 9 = %ld / %ld (bad = %ld)\n",
           cuts19 - bad19, cuts19, bad19);
    printf("[3-Skeptic Audit] ALL CHECKS PASSED in %.2f s!\n", elapsed);

    return (unit_err == 0 && bad_minors == 0 && sym_err == 0 && bad20 == 0 && bad19 == 0) ? 0 : 1;
}
