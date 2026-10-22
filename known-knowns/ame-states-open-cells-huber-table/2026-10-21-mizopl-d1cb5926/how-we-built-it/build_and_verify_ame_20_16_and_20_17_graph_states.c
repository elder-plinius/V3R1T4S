#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/*
 * Corollary D29.1 Verifier & Graph-State Extractor:
 *   1. Maps our Theorem D28 [20, 10, 11]_{17^2} Hermitian self-dual MDS code over F_289
 *      to an explicit 20x20 zero-diagonal symmetric graph state Gamma_20^{(17)} over F_17,
 *      and brute-force verifies all C(20, 10) = 184,756 balanced 10x10 bipartite cuts over F_17.
 *   2. Maps our Theorem D29 [20, 10, 11]_{16^2} Hermitian self-dual MDS code over F_256
 *      to an explicit 20x20 zero-diagonal symmetric graph state Gamma_20^{(16)} over F_16,
 *      and brute-force verifies all C(20, 10) = 184,756 balanced 10x10 bipartite cuts over F_16.
 */

/* ---------------- Part 1: F_289 -> F_17 ---------------- */
static int mod17(int x) { x %= 17; return x < 0 ? x + 17 : x; }
static int inv17[17];

static int det10_f17(const int G[20][20], const int S[10], const int Sc[10]) {
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
            det = mod17(-det);
            for (int c = col; c < 10; c++) {
                int t = M[col][c]; M[col][c] = M[piv][c]; M[piv][c] = t;
            }
        }
        det = mod17(det * M[col][col]);
        int iv = inv17[M[col][col]];
        for (int row = col + 1; row < 10; row++) {
            if (!M[row][col]) continue;
            int f = mod17(M[row][col] * iv);
            for (int c = col; c < 10; c++)
                M[row][c] = mod17(M[row][c] - f * M[col][c]);
        }
    }
    return det;
}

static int verify_ame_20_17_graph_state(int Gamma17[20][20]) {
    for (int a = 1; a < 17; a++)
        for (int b = 1; b < 17; b++)
            if ((a * b) % 17 == 1) inv17[a] = b;

    const int u11[5] = {59, 86, 102, 59, 275};
    const int u12[5] = {204, 224, 197, 194, 235};
    int U[10][10];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            int u_rev = u11[(5 - d) % 5];
            int u22_d = (u_rev % 17) + mod17(-(u_rev / 17)) * 17;
            U[5 + i][5 + j] = u22_d;
            U[i][5 + j] = u12[d];
            U[5 + i][j] = u12[d];
        }
    }
    /* Multiply U by gamma = 3 + 3*alpha (54) so G = [I_10 | gamma*U] satisfies G * G^dagger = 0 */
    int GU[10][20];
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) GU[i][j] = (i == j) ? 1 : 0;
        for (int j = 0; j < 10; j++) {
            int a0 = 3, a1 = 3;
            int b0 = U[i][j] % 17, b1 = U[i][j] / 17;
            int c0 = mod17(a0 * b0 + 3 * a1 * b1);
            int c1 = mod17(a0 * b1 + a1 * b0);
            GU[i][10 + j] = c0 + 17 * c1;
        }
    }
    /*
     * Over F_289 = F_17[alpha]/(alpha^2 - 3), for u = x + alpha*z and v = x' + alpha*z',
     * Im(u * conj(v)) = z*x' - x*z'.
     * Thus with X(u) = Re(u), Z(u) = Im(u) on the 20-dim F_17-span of {e_i * G, alpha * e_i * G},
     * we have:
     *   rows 0..9  (G):       X = Re(G),      Z = Im(G)
     *   rows 10..19 (alpha*G): X = 3*Im(G),    Z = Re(G)
     * Notice on columns 0..9, G = I_10 has Re(G) = I_10, Im(G) = 0, so rows 10..19 have X[:, 0..9] = 0!
     * To make X invertible (which is a local X <-> Z Fourier gate on coordinates 10..19),
     * we apply the symplectic swap (X_j, Z_j) -> (-Z_j, X_j) on coordinates j = 10..19
     * (or multiply columns 10..19 of G by norm-1 scalar or use the invertible X submatrix)!
     * Wait: let's check if X is ALREADY invertible without any swap!
     * On cols 0..9, rows 0..9 have X = I_10, rows 10..19 have X = 0.
     * So det(X) = det(I_10) * det(3 * Im(gamma * U)) = 3^10 * det(Im(gamma * U))!
     */
    int X[20][20], Z[20][20];
    /* Try unit-norm phase omega in U(1, F_289) on cols 10..19 so Im(omega * gamma * U) is invertible */
    int unit_elems[18], nu = 0;
    for (int a = 1; a < 289; a++) {
        int a0 = a % 17, a1 = a / 17;
        if (mod17(a0 * a0 - 3 * a1 * a1) == 1) unit_elems[nu++] = a;
    }
    int found_inv = 0;
    for (int ui = 0; ui < nu; ui++) {
        int w = unit_elems[ui];
        int w0 = w % 17, w1 = w / 17;
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 20; j++) {
                int val = GU[i][j];
                if (j >= 10) {
                    int b0 = val % 17, b1 = val / 17;
                    val = mod17(w0 * b0 + 3 * w1 * b1) + 17 * mod17(w0 * b1 + w1 * b0);
                }
                int re = val % 17, im = val / 17;
                X[i][j]      = re;
                Z[i][j]      = im;
                X[10 + i][j] = mod17(3 * im);
                Z[10 + i][j] = re;
            }
        }
        /* Invert X over F_17 */
        int aug[20][40];
        for (int i = 0; i < 20; i++) {
            for (int j = 0; j < 20; j++) {
                aug[i][j] = X[i][j];
                aug[i][20 + j] = Z[i][j];
            }
        }
        int ok = 1;
        for (int col = 0; col < 20; col++) {
            int piv = -1;
            for (int row = col; row < 20; row++)
                if (aug[row][col] != 0) { piv = row; break; }
            if (piv < 0) { ok = 0; break; }
            if (piv != col) {
                for (int c = col; c < 40; c++) {
                    int t = aug[col][c]; aug[col][c] = aug[piv][c]; aug[piv][c] = t;
                }
            }
            int iv = inv17[aug[col][col]];
            for (int c = col; c < 40; c++) aug[col][c] = mod17(aug[col][c] * iv);
            for (int row = 0; row < 20; row++) {
                if (row == col || !aug[row][col]) continue;
                int f = aug[row][col];
                for (int c = col; c < 40; c++)
                    aug[row][c] = mod17(aug[row][c] - f * aug[col][c]);
            }
        }
        if (ok) {
            for (int i = 0; i < 20; i++)
                for (int j = 0; j < 20; j++)
                    Gamma17[i][j] = (i == j) ? 0 : aug[i][20 + j];
            printf("[F_17 Graph State] Found invertible X at unit phase w=%d (%d + %d*alpha)\n", w, w0, w1);
            found_inv = 1;
            break;
        }
    }
    if (!found_inv) { printf("Failed to invert X for F_17!\n"); return 0; }

    int sym_err = 0;
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20; j++)
            if (Gamma17[i][j] != Gamma17[j][i] || (i == j && Gamma17[i][j] != 0)) sym_err++;
    printf("[F_17 Graph State] Symmetry & zero-diagonal errors: %d / 400\n", sym_err);

    long checked = 0, bad = 0;
    for (uint32_t m = 0; m < (1u << 20); m++) {
        if (__builtin_popcount(m) != 10) continue;
        int S[10], Sc[10], si = 0, sci = 0;
        for (int i = 0; i < 20; i++) {
            if ((m >> i) & 1) S[si++] = i;
            else              Sc[sci++] = i;
        }
        checked++;
        if (det10_f17(Gamma17, S, Sc) == 0) bad++;
    }
    printf("[F_17 Graph State] All 10-party bipartite cuts checked: %ld / %ld non-singular (bad = %ld)\n",
           checked - bad, checked, bad);
    return (sym_err == 0 && bad == 0);
}

/* ---------------- Part 2: F_256 -> F_16 ---------------- */
static uint8_t mul256[256][256], inv256[256], conj256[256];
static uint8_t exp256[512], log256[256];
static uint8_t f16_to_256[16], f256_to_16[256];
static uint8_t mul16[16][16], inv16[16];

static void init_gf256_and_f16(void) {
    int x = 1;
    for (int i = 0; i < 255; i++) {
        exp256[i] = (uint8_t)x;
        exp256[i + 255] = (uint8_t)x;
        log256[x] = (uint8_t)i;
        x <<= 1;
        if (x & 0x100) x ^= 0x11D;
    }
    log256[0] = 0;
    for (int a = 0; a < 256; a++) {
        for (int b = 0; b < 256; b++)
            mul256[a][b] = (a && b) ? exp256[(int)log256[a] + (int)log256[b]] : 0;
        inv256[a] = a ? exp256[255 - log256[a]] : 0;
        conj256[a] = a ? exp256[((int)log256[a] * 16) % 255] : 0;
    }
    /* Map F_16 = {0} U {g^(17*k)} canonically as a polynomial field over F_2 with generator alpha16 = g^17 */
    uint8_t g17 = exp256[17];
    /* Find minimal polynomial of g17 over F_2: (g17)^4 + (g17) + 1 or (g17)^4 + (g17)^3 + 1 */
    for (int m = 0; m < 16; m++) {
        uint8_t val = 0, p = 1;
        for (int b = 0; b < 4; b++) {
            if ((m >> b) & 1) val ^= p;
            p = mul256[p][g17];
        }
        f16_to_256[m] = val;
        f256_to_16[val] = (uint8_t)m;
    }
    for (int a = 0; a < 16; a++) {
        for (int b = 0; b < 16; b++)
            mul16[a][b] = f256_to_16[mul256[f16_to_256[a]][f16_to_256[b]]];
        inv16[a] = a ? f256_to_16[inv256[f16_to_256[a]]] : 0;
    }
    printf("[F_16 Setup] g^17 = %d, g^68 ^ g^17 ^ 1 = %d, g^68 ^ g^51 ^ 1 = %d\n",
           g17, exp256[68] ^ exp256[17] ^ 1, exp256[68] ^ exp256[51] ^ 1);
}

static uint8_t det10_f16(const int G[20][20], const int S[10], const int Sc[10]) {
    uint8_t M[10][10];
    for (int i = 0; i < 10; i++)
        for (int j = 0; j < 10; j++)
            M[i][j] = (uint8_t)G[S[i]][Sc[j]];
    uint8_t det = 1;
    for (int col = 0; col < 10; col++) {
        int piv = -1;
        for (int row = col; row < 10; row++)
            if (M[row][col] != 0) { piv = row; break; }
        if (piv < 0) return 0;
        if (piv != col) {
            for (int c = col; c < 10; c++) {
                uint8_t t = M[col][c]; M[col][c] = M[piv][c]; M[piv][c] = t;
            }
        }
        det = mul16[det][M[col][col]];
        uint8_t iv = inv16[M[col][col]];
        for (int row = col + 1; row < 10; row++) {
            if (!M[row][col]) continue;
            uint8_t f = mul16[M[row][col]][iv];
            for (int c = col; c < 10; c++)
                M[row][c] ^= mul16[f][M[col][c]];
        }
    }
    return det;
}

static int verify_ame_20_16_graph_state(int Gamma16[20][20]) {
    init_gf256_and_f16();
    const uint8_t u11[5] = {150, 84, 21, 129, 138};
    const uint8_t u12[5] = {11, 251, 50, 238, 241};
    uint8_t U[10][10];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            int d = (j - i + 5) % 5;
            U[i][j] = u11[d];
            U[5 + i][5 + j] = conj256[u11[(5 - d) % 5]];
            U[i][5 + j] = u12[d];
            U[5 + i][j] = u12[d];
        }
    }
    /* Find beta in F_256 with beta ^ conj(beta) == 1 */
    uint8_t beta = 0;
    for (int a = 1; a < 256; a++) {
        if ((a ^ conj256[a]) == 1) { beta = (uint8_t)a; break; }
    }
    uint8_t beta_bar = conj256[beta];
    printf("[F_16 Graph State] Using normal-trace basis {1, beta=%d}, beta_bar=%d, beta*beta_bar=%d (F_16 idx=%d)\n",
           beta, beta_bar, mul256[beta][beta_bar], f256_to_16[mul256[beta][beta_bar]]);

    /*
     * For u in F_256, write u = x + beta * z with x, z in F_16:
     *   z = u ^ conj(u) in F_16
     *   x = mul256[beta_bar][u] ^ mul256[beta][conj(u)] in F_16
     * Then for u = x + beta*z, v = x' + beta*z':
     *   Tr_{F_256/F_16}(u * conj(v)) = (u*conj(v)) ^ (conj(u)*v) = (x*z') ^ (z*x')!
     * For G = [I_10 | w*U] with w in U(1, F_256) (w^17 = 1), we form the 20 rows over F_256:
     *   rows 0..9:   G[i]
     *   rows 10..19: beta * G[i]
     */
    for (int ui = 0; ui < 17; ui++) {
        uint8_t w = exp256[15 * ui]; /* w^17 = 1 */
        uint8_t X[20][20], Z[20][20];
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 20; j++) {
                uint8_t u0 = (j < 10) ? ((i == j) ? 1 : 0) : mul256[w][U[i][j - 10]];
                uint8_t u1 = mul256[beta][u0];

                uint8_t z0 = u0 ^ conj256[u0];
                uint8_t x0 = mul256[beta_bar][u0] ^ mul256[beta][conj256[u0]];
                uint8_t z1 = u1 ^ conj256[u1];
                uint8_t x1 = mul256[beta_bar][u1] ^ mul256[beta][conj256[u1]];

                X[i][j]      = f256_to_16[x0];
                Z[i][j]      = f256_to_16[z0];
                X[10 + i][j] = f256_to_16[x1];
                Z[10 + i][j] = f256_to_16[z1];
            }
        }
        uint8_t aug[20][40];
        for (int i = 0; i < 20; i++)
            for (int j = 0; j < 20; j++) {
                aug[i][j] = X[i][j];
                aug[i][20 + j] = Z[i][j];
            }
        int ok = 1;
        for (int col = 0; col < 20; col++) {
            int piv = -1;
            for (int row = col; row < 20; row++)
                if (aug[row][col] != 0) { piv = row; break; }
            if (piv < 0) { ok = 0; break; }
            if (piv != col) {
                for (int c = col; c < 40; c++) {
                    uint8_t t = aug[col][c]; aug[col][c] = aug[piv][c]; aug[piv][c] = t;
                }
            }
            uint8_t iv = inv16[aug[col][col]];
            for (int c = col; c < 40; c++) aug[col][c] = mul16[aug[col][c]][iv];
            for (int row = 0; row < 20; row++) {
                if (row == col || !aug[row][col]) continue;
                uint8_t f = aug[row][col];
                for (int c = col; c < 40; c++)
                    aug[row][c] ^= mul16[f][aug[col][c]];
            }
        }
        if (ok) {
            for (int i = 0; i < 20; i++)
                for (int j = 0; j < 20; j++)
                    Gamma16[i][j] = (i == j) ? 0 : aug[i][20 + j];
            printf("[F_16 Graph State] Found invertible X at unit phase w=%d (ui=%d)\n", w, ui);
            break;
        }
    }

    int sym_err = 0;
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20; j++)
            if (Gamma16[i][j] != Gamma16[j][i] || (i == j && Gamma16[i][j] != 0)) sym_err++;
    printf("[F_16 Graph State] Symmetry & zero-diagonal errors: %d / 400\n", sym_err);

    long checked = 0, bad = 0;
    for (uint32_t m = 0; m < (1u << 20); m++) {
        if (__builtin_popcount(m) != 10) continue;
        int S[10], Sc[10], si = 0, sci = 0;
        for (int i = 0; i < 20; i++) {
            if ((m >> i) & 1) S[si++] = i;
            else              Sc[sci++] = i;
        }
        checked++;
        if (det10_f16(Gamma16, S, Sc) == 0) bad++;
    }
    printf("[F_16 Graph State] All 10-party bipartite cuts checked: %ld / %ld non-singular (bad = %ld)\n",
           checked - bad, checked, bad);
    return (sym_err == 0 && bad == 0);
}

int main(void) {
    int Gamma17[20][20], Gamma16[20][20];
    int ok17 = verify_ame_20_17_graph_state(Gamma17);
    int ok16 = verify_ame_20_16_graph_state(Gamma16);
    if (!ok17 || !ok16) return 1;

    printf("\nGamma17 (20x20 over F_17):\n");
    for (int i = 0; i < 20; i++) {
        printf("  [");
        for (int j = 0; j < 20; j++) printf("%2d%s", Gamma17[i][j], (j < 19) ? ", " : "");
        printf("]%s\n", (i < 19) ? "," : "");
    }
    printf("\nGamma16 (20x20 over F_16 = F_2[a]/(a^4 + a^3 + 1)):\n");
    for (int i = 0; i < 20; i++) {
        printf("  [");
        for (int j = 0; j < 20; j++) printf("%2d%s", Gamma16[i][j], (j < 19) ? ", " : "");
        printf("]%s\n", (i < 19) ? "," : "");
    }
    return 0;
}
