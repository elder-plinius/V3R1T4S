/* Standalone C99 verifier for p2 (arXiv:2112.11766 Section 6 order-5 240-plane problem). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint8_t mat_apply(const uint8_t M[7], uint8_t v) {
    uint8_t out = 0;
    for (int r = 0; r < 7; r++) {
        if ((v >> r) & 1) out ^= M[r];
    }
    return out;
}

static void mat_mul(const uint8_t A[7], const uint8_t B[7], uint8_t C[7]) {
    for (int r = 0; r < 7; r++) C[r] = mat_apply(B, A[r]);
}

static int mat_is_id(const uint8_t A[7]) {
    for (int r = 0; r < 7; r++) if (A[r] != (1u << r)) return 0;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "Usage: %s <file>\n", argv[0]); return 2; }
    FILE *fp = fopen(argv[1], "r");
    if (!fp) { fprintf(stderr, "FAIL: cannot open file\n"); return 1; }

    uint8_t pi[7] = {0};
    for (int r = 0; r < 7; r++) {
        for (int c = 0; c < 7; c++) {
            int bit;
            if (fscanf(fp, "%d", &bit) != 1 || (bit != 0 && bit != 1)) {
                printf("FAIL: invalid pi entry\n"); fclose(fp); return 1;
            }
            if (bit) pi[r] |= (uint8_t)(1u << c);
        }
    }
    int n_planes = 0;
    if (fscanf(fp, "%d", &n_planes) != 1 || n_planes != 240) {
        printf("FAIL: expected 240 planes\n"); fclose(fp); return 1;
    }

    /* 1. Verify pi has exact order 5 */
    if (mat_is_id(pi)) { printf("FAIL: pi == I_7\n"); fclose(fp); return 1; }
    uint8_t pcur[7], pnext[7];
    memcpy(pcur, pi, 7);
    for (int k = 2; k <= 5; k++) {
        mat_mul(pcur, pi, pnext);
        memcpy(pcur, pnext, 7);
        if (k < 5 && mat_is_id(pcur)) { printf("FAIL: pi order %d < 5\n", k); fclose(fp); return 1; }
    }
    if (!mat_is_id(pcur)) { printf("FAIL: pi^5 != I_7\n"); fclose(fp); return 1; }

    /* 2. Fixed-point space F */
    uint8_t is_F[128] = {0};
    int f_cnt = 0;
    for (int v = 1; v < 128; v++) {
        if (mat_apply(pi, (uint8_t)v) == (uint8_t)v) { is_F[v] = 1; f_cnt++; }
    }
    if (f_cnt != 7) { printf("FAIL: |F|=%d != 7\n", f_cnt); fclose(fp); return 1; }

    /* 3. Read 240 RREF planes */
    uint64_t plane_lo[240] = {0}, plane_hi[240] = {0};
    uint8_t plane_pts[240][7];
    int pt_cov[128] = {0};

    for (int i = 0; i < 240; i++) {
        uint8_t rows[3] = {0};
        int piv[3] = {-1, -1, -1};
        for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 7; c++) {
                int bit;
                if (fscanf(fp, "%d", &bit) != 1 || (bit != 0 && bit != 1)) {
                    printf("FAIL: invalid plane bit at %d\n", i); fclose(fp); return 1;
                }
                if (bit) {
                    rows[r] |= (uint8_t)(1u << c);
                    if (piv[r] == -1) piv[r] = c;
                }
            }
            if (piv[r] == -1 || (r > 0 && piv[r] <= piv[r - 1])) {
                printf("FAIL: plane %d not RREF (pivots)\n", i); fclose(fp); return 1;
            }
        }
        for (int r = 0; r < 3; r++) {
            for (int r2 = 0; r2 < 3; r2++) {
                if (r2 != r && ((rows[r2] >> piv[r]) & 1)) {
                    printf("FAIL: plane %d not reduced at pivot\n", i); fclose(fp); return 1;
                }
            }
        }
        int pcnt = 0;
        for (int m = 1; m < 8; m++) {
            uint8_t v = 0;
            for (int r = 0; r < 3; r++) if ((m >> r) & 1) v ^= rows[r];
            if (v == 0 || is_F[v]) {
                printf("FAIL: plane %d rank<3 or meets F\n", i); fclose(fp); return 1;
            }
            plane_pts[i][pcnt++] = v;
            if (v < 64) plane_lo[i] |= (1ULL << v);
            else plane_hi[i] |= (1ULL << (v - 64));
            pt_cov[v]++;
        }
        for (int j = 0; j < i; j++) {
            if (plane_lo[i] == plane_lo[j] && plane_hi[i] == plane_hi[j]) {
                printf("FAIL: duplicate plane %d == %d\n", i, j); fclose(fp); return 1;
            }
        }
    }
    int extra;
    if (fscanf(fp, "%d", &extra) == 1) { printf("FAIL: trailing tokens\n"); fclose(fp); return 1; }
    fclose(fp);

    /* 4. Check pi-invariance of C and pairwise intersection <= 1 projective point! */
    for (int i = 0; i < 240; i++) {
        uint64_t ilo = 0, ihi = 0;
        for (int k = 0; k < 7; k++) {
            uint8_t w = mat_apply(pi, plane_pts[i][k]);
            if (w < 64) ilo |= (1ULL << w);
            else ihi |= (1ULL << (w - 64));
        }
        int found = 0;
        for (int j = 0; j < 240; j++) {
            if (ilo == plane_lo[j] && ihi == plane_hi[j]) { found = 1; break; }
        }
        if (!found) { printf("FAIL: plane %d not stabilized by pi\n", i); return 1; }

        for (int j = i + 1; j < 240; j++) {
            int common = __builtin_popcountll(plane_lo[i] & plane_lo[j]) +
                         __builtin_popcountll(plane_hi[i] & plane_hi[j]);
            if (common > 1) {
                printf("FAIL: planes %d and %d share %d projective points (meet in a line)\n", i, j, common);
                return 1;
            }
        }
    }

    /* 5. Brute-force check over all 2,667 lines of PG(6,2) as well */
    int total_lines = 0, cov1_lines = 0;
    for (int a = 1; a < 128; a++) {
        for (int b = a + 1; b < 128; b++) {
            int c = a ^ b;
            if (b >= c) continue;
            total_lines++;
            uint64_t llo = 0, lhi = 0;
            int pts3[3] = {a, b, c};
            for (int k = 0; k < 3; k++) {
                if (pts3[k] < 64) llo |= (1ULL << pts3[k]);
                else lhi |= (1ULL << (pts3[k] - 64));
            }
            int cnt = 0;
            for (int i = 0; i < 240; i++) {
                if (((plane_lo[i] & llo) == llo) && ((plane_hi[i] & lhi) == lhi)) cnt++;
            }
            if (cnt > 1) { printf("FAIL: line (%d,%d,%d) covered %d times\n", a, b, c, cnt); return 1; }
            if (cnt == 1) cov1_lines++;
        }
    }
    if (total_lines != 2667 || cov1_lines != 1680) {
        printf("FAIL: line counts total=%d cov1=%d\n", total_lines, cov1_lines); return 1;
    }

    /* 6. Point coverage: 0 on F (7 pts), 14 on all 120 pts outside F */
    for (int v = 1; v < 128; v++) {
        int exp_cov = is_F[v] ? 0 : 14;
        if (pt_cov[v] != exp_cov) {
            printf("FAIL: point %d cov=%d expected=%d\n", v, pt_cov[v], exp_cov);
            return 1;
        }
    }

    printf("PASS: C99 independent check verified 240 rank-3 RREF planes, ord(pi)=5, |F|=7, 0/28680 line clashes, 1680/2667 lines=1, 120/120 outside pts=14\n");
    return 0;
}
