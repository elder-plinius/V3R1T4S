/*
 * qecc_toeplitz.c
 *
 * Toeplitz Shortened Double-Circulant & Bordered Hermitian Self-Orthogonal Search
 * for explicit binary quantum stabilizer codes [[n, k, d]]_2 (Partial Win p1).
 *
 * Mathematical mechanism:
 * Let C_{k4}(a) be the k4 x m matrix over GF(4) whose i-th row (0 <= i < k4) is the i-th
 * cyclic shift of a in GF(4)^m. Because cyclic shift is unitary, the k4 x k4 Hermitian
 * Gram matrix C_{k4}(a) * C_{k4}(a)^dagger is Toeplitz, determined solely by its first row
 * delta = 0, 1, ..., k4 - 1, which has 2*k4 - 1 bits: sig(a) in [0, 2^{2*k4 - 1} - 1].
 *
 * - For even n = 2*m: if sig(a) == sig(b), G4 = [C_{k4}(a) | C_{k4}(b)] satisfies
 *   G4 * G4^dagger = 0 identically!
 * - For odd n = 2*m + 1: appending the all-ones column 1_{k4 x 1} adds 1 to every entry of
 *   the Gram matrix (also Toeplitz with signature sig_ones). Thus if sig(a) ^ sig(b) == sig_ones,
 *   G4 = [C_{k4}(a) | C_{k4}(b) | 1] satisfies G4 * G4^dagger = 0 identically!
 *
 * Exact quantum minimum distance d = min { j >= 1 : B_j > A_j } is evaluated via full
 * enumeration of all 4^{k4} codewords of C4 + the exact integer Quantum MacWilliams Identity.
 */

#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "time.h"

#define MAX_N 64
#define MAX_K4 11

static const uint8_t GF4_MUL[4][4] = {
    {0,0,0,0}, {0,1,2,3}, {0,2,3,1}, {0,3,1,2}
};
static const uint8_t GF4_CONJ[4] = {0, 1, 3, 2};
static const uint8_t GF4_INV[4] = {0, 1, 3, 2};

static uint64_t rng_state = 0x9e3779b97f4a7c15ULL;
static inline uint64_t xorshift64(void) {
    uint64_t x = rng_state;
    x ^= x << 13; x ^= x >> 7; x ^= x << 17;
    return (rng_state = x);
}

/* Compute (2*k4 - 1)-bit Toeplitz Hermitian autocorrelation signature of a[0..m-1] */
static uint32_t compute_sig(const uint8_t *a, int m, int k4) {
    uint32_t sig = 0;
    int p0 = 0;
    for (int c = 0; c < m; c++) if (a[c] != 0) p0 ^= 1;
    sig |= (uint32_t)p0;
    for (int d = 1; d < k4; d++) {
        uint8_t acc = 0;
        for (int c = 0; c < m; c++) {
            int c2 = (c + m - d) % m;
            if (a[c] && a[c2]) {
                acc ^= GF4_MUL[a[c]][GF4_CONJ[a[c2]]];
            }
        }
        sig |= ((uint32_t)acc) << (2 * d - 1);
    }
    return sig;
}

static uint32_t compute_sig_ones(int k4) {
    uint32_t sig = 1;
    for (int d = 1; d < k4; d++) {
        sig |= (1U << (2 * d - 1));
    }
    return sig;
}

/* Precompute Krawtchouk polynomials K_j(i; n, 4) for j = 0..10, i = 0..n */
static int64_t KRAW4[12][MAX_N + 1];
static void init_kraw4(int n) {
    for (int i = 0; i <= n; i++) KRAW4[0][i] = 1;
    for (int j = 1; j <= 10; j++) {
        for (int i = 0; i <= n; i++) {
            /* Compute C(i, s) * C(n - i, j - s) * (-1)^s * 3^(j - s) */
            int64_t sum = 0;
            for (int s = 0; s <= j; s++) {
                if (s > i || (j - s) > (n - i)) continue;
                int64_t c1 = 1;
                for (int t = 1; t <= s; t++) c1 = c1 * (i - t + 1) / t;
                int64_t c2 = 1;
                for (int t = 1; t <= j - s; t++) c2 = c2 * (n - i - t + 1) / t;
                int64_t p3 = 1;
                for (int t = 0; t < j - s; t++) p3 *= 3;
                int64_t term = c1 * c2 * p3;
                if (s & 1) sum -= term;
                else       sum += term;
            }
            KRAW4[j][i] = sum;
        }
    }
}

static int check_rank_gf4(int k4, int n, const uint8_t G[MAX_K4][MAX_N]) {
    uint8_t M[MAX_K4][MAX_N];
    memcpy(M, G, sizeof(M));
    int r = 0;
    for (int col = 0; col < n && r < k4; col++) {
        int piv = -1;
        for (int i = r; i < k4; i++) if (M[i][col]) { piv = i; break; }
        if (piv < 0) continue;
        for (int j = 0; j < n; j++) { uint8_t t = M[r][j]; M[r][j] = M[piv][j]; M[piv][j] = t; }
        uint8_t iv = GF4_INV[M[r][col]];
        for (int j = 0; j < n; j++) M[r][j] = GF4_MUL[iv][M[r][j]];
        for (int i = 0; i < k4; i++) {
            if (i != r && M[i][col]) {
                uint8_t fac = M[i][col];
                for (int j = 0; j < n; j++) M[i][j] ^= GF4_MUL[fac][M[r][j]];
            }
        }
        r++;
    }
    return r;
}

static int verify_hermitian_self_orth(int k4, int n, const uint8_t G[MAX_K4][MAX_N]) {
    for (int i = 0; i < k4; i++) {
        for (int j = i; j < k4; j++) {
            uint8_t dot = 0;
            for (int c = 0; c < n; c++) {
                if (G[i][c] && G[j][c]) dot ^= GF4_MUL[G[i][c]][GF4_CONJ[G[j][c]]];
            }
            if (dot != 0) return 0;
        }
    }
    return 1;
}

/*
 * Fast exact evaluation of quantum minimum distance d = min { j >= 1 : B_j > A_j }
 * using bit-sliced 64-bit representation of GF(4)^n vectors (lo, hi bitmasks of length n <= 64):
 * Element x in {0, 1, 2, 3} at column c is stored as:
 *   lo_bit = x & 1,  hi_bit = (x >> 1) & 1.
 * Addition in GF(4) is bitwise XOR of lo and hi!
 * Multiplication by 2 (omega): (lo, hi) -> (hi, lo ^ hi)!
 * Multiplication by 3 (omega^2): (lo, hi) -> (lo ^ hi, lo)!
 * Hamming weight is __builtin_popcountll(lo | hi)!
 */
static int eval_qecc_bitsliced(int k4, int n, const uint8_t G[MAX_K4][MAX_N], int64_t *B_d_out) {
    uint64_t row_lo[MAX_K4][4], row_hi[MAX_K4][4];
    for (int i = 0; i < k4; i++) {
        uint64_t l1 = 0, h1 = 0;
        for (int c = 0; c < n; c++) {
            if (G[i][c] & 1) l1 |= (1ULL << c);
            if (G[i][c] & 2) h1 |= (1ULL << c);
        }
        row_lo[i][0] = 0;       row_hi[i][0] = 0;
        row_lo[i][1] = l1;      row_hi[i][1] = h1;
        row_lo[i][2] = h1;      row_hi[i][2] = l1 ^ h1;
        row_lo[i][3] = l1 ^ h1; row_hi[i][3] = l1;
    }

    int64_t A[MAX_N + 1];
    memset(A, 0, sizeof(A));
    A[0] = 1;

    /* Enumerate all (4^{k4} - 1)/3 monic messages and multiply count by 3 */
    uint64_t cw_lo = 0, cw_hi = 0;
    int coeff[MAX_K4];

    for (int lead = 0; lead < k4; lead++) {
        int rem = k4 - 1 - lead;
        cw_lo = row_lo[lead][1];
        cw_hi = row_hi[lead][1];
        for (int i = 0; i < rem; i++) coeff[i] = 0;

        while (1) {
            int w = __builtin_popcountll(cw_lo | cw_hi);
            A[w] += 3;

            int pos = 0;
            while (pos < rem) {
                int r_idx = lead + 1 + pos;
                int old_c = coeff[pos];
                int new_c = (old_c + 1) & 3;
                cw_lo ^= row_lo[r_idx][old_c] ^ row_lo[r_idx][new_c];
                cw_hi ^= row_hi[r_idx][old_c] ^ row_hi[r_idx][new_c];
                coeff[pos] = new_c;
                if (new_c != 0) break;
                pos++;
            }
            if (pos == rem) break;
        }
    }

    int64_t scale = 1LL << (2 * k4);
    for (int j = 1; j <= 10; j++) {
        int64_t sum = 0;
        for (int i = 0; i <= n; i++) {
            if (A[i]) sum += A[i] * KRAW4[j][i];
        }
        int64_t Bj = sum / scale;
        if (Bj > A[j]) {
            if (B_d_out) *B_d_out = Bj - A[j];
            return j;
        }
    }
    return 11;
}

static void save_qecc_json(int n, int k, int k4, int d, int d_lo, int d_up, const uint8_t G[MAX_K4][MAX_N], const char *desc) {
    char fname[256];
    snprintf(fname, sizeof(fname), "results/qecc_p1_n%d_k%d_d%d.json", n, k, d);
    FILE *fp = fopen(fname, "w");
    if (!fp) return;

    /* Convert each row of G4 over GF(4) into two binary stabilizer rows (r and omega*r):
     * 0 -> (X=0, Z=0), 1 -> (X=1, Z=0), 2 (omega) -> (X=0, Z=1), 3 (omega^2) -> (X=1, Z=1)
     */
    int r_stab = 2 * k4;
    uint8_t X[32][MAX_N], Z[32][MAX_N];
    for (int i = 0; i < k4; i++) {
        for (int c = 0; c < n; c++) {
            uint8_t v1 = G[i][c];
            X[2 * i][c] = v1 & 1;
            Z[2 * i][c] = (v1 >> 1) & 1;
            uint8_t v2 = GF4_MUL[2][v1];
            X[2 * i + 1][c] = v2 & 1;
            Z[2 * i + 1][c] = (v2 >> 1) & 1;
        }
    }

    fprintf(fp, "{\n");
    fprintf(fp, "  \"kind\": \"qecc\",\n");
    fprintf(fp, "  \"n\": %d,\n", n);
    fprintf(fp, "  \"k\": %d,\n", k);
    fprintf(fp, "  \"d\": %d,\n", d);
    fprintf(fp, "  \"d_lo_codetables\": %d,\n", d_lo);
    fprintf(fp, "  \"d_up_codetables\": %d,\n", d_up);
    fprintf(fp, "  \"construction\": \"%s\",\n", desc);
    fprintf(fp, "  \"G4\": [\n");
    for (int i = 0; i < k4; i++) {
        fprintf(fp, "    [");
        for (int c = 0; c < n; c++) fprintf(fp, "%d%s", G[i][c], (c + 1 < n) ? "," : "");
        fprintf(fp, "]%s\n", (i + 1 < k4) ? "," : "");
    }
    fprintf(fp, "  ],\n");
    fprintf(fp, "  \"X\": [\n");
    for (int i = 0; i < r_stab; i++) {
        fprintf(fp, "    [");
        for (int c = 0; c < n; c++) fprintf(fp, "%d%s", X[i][c], (c + 1 < n) ? "," : "");
        fprintf(fp, "]%s\n", (i + 1 < r_stab) ? "," : "");
    }
    fprintf(fp, "  ],\n");
    fprintf(fp, "  \"Z\": [\n");
    for (int i = 0; i < r_stab; i++) {
        fprintf(fp, "    [");
        for (int c = 0; c < n; c++) fprintf(fp, "%d%s", Z[i][c], (c + 1 < n) ? "," : "");
        fprintf(fp, "]%s\n", (i + 1 < r_stab) ? "," : "");
    }
    fprintf(fp, "  ]\n}\n");
    fclose(fp);
}

typedef struct {
    uint8_t a[32];
    uint32_t sig;
} PolyItem;

static int cmp_sig(const void *p1, const void *p2) {
    uint32_t s1 = ((const PolyItem *)p1)->sig;
    uint32_t s2 = ((const PolyItem *)p2)->sig;
    return (s1 > s2) - (s1 < s2);
}

static int search_toeplitz_cell(int n, int k, int d_lo, int d_up, int pool_size, int max_pairs) {
    int r = n - k;
    if (r % 2 != 0) return 0;
    int k4 = r / 2;
    int is_odd = n & 1;
    int m = n / 2;
    int d_target = d_lo + 1;

    init_kraw4(n);
    printf("[QECC-Toeplitz] Searching [[%d, %d, >=%d]]_2 (m=%d, bordered=%d, k4=%d, live=%d-%d)...\n",
           n, k, d_target, m, is_odd, k4, d_lo, d_up);
    fflush(stdout);

    PolyItem *pool = (PolyItem *)malloc(pool_size * sizeof(PolyItem));
    for (int i = 0; i < pool_size; i++) {
        pool[i].a[0] = 1;
        for (int c = 1; c < m; c++) pool[i].a[c] = xorshift64() & 3;
        pool[i].sig = compute_sig(pool[i].a, m, k4);
    }
    qsort(pool, pool_size, sizeof(PolyItem), cmp_sig);

    uint32_t target_xor = is_odd ? compute_sig_ones(k4) : 0;
    int best_d = 0;
    int64_t best_Bd = 0x7fffffffffffffffLL;
    int tested = 0;

    for (int i = 0; i < pool_size && tested < max_pairs; i++) {
        uint32_t want = pool[i].sig ^ target_xor;
        /* Binary search for want in pool */
        int lo = 0, hi = pool_size - 1, start = -1;
        while (lo <= hi) {
            int mid = (lo + hi) >> 1;
            if (pool[mid].sig >= want) {
                if (pool[mid].sig == want) start = mid;
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        if (start < 0) continue;

        for (int j = start; j < pool_size && pool[j].sig == want && tested < max_pairs; j++) {
            if (!is_odd && j <= i) continue;
            uint8_t G[MAX_K4][MAX_N];
            memset(G, 0, sizeof(G));
            for (int r_idx = 0; r_idx < k4; r_idx++) {
                for (int c = 0; c < m; c++) {
                    G[r_idx][(c + r_idx) % m] = pool[i].a[c];
                    G[r_idx][m + ((c + r_idx) % m)] = pool[j].a[c];
                }
                if (is_odd) G[r_idx][2 * m] = 1;
            }
            if (check_rank_gf4(k4, n, G) < k4) continue;
            tested++;
            int64_t Bd = 0;
            int d = eval_qecc_bitsliced(k4, n, G, &Bd);
            if (d > best_d || (d == best_d && Bd < best_Bd)) {
                best_d = d;
                best_Bd = Bd;
            }
            if (d >= d_target) {
                if (!verify_hermitian_self_orth(k4, n, G)) continue;
                printf("\n*** QUANTUM BREAKTHROUGH WIN (p1): [[%d, %d, %d]]_2 (beats codetables.de QECC d_lo=%d, d_up=%d, B_%d-A_%d=%lld) ***\n",
                       n, k, d, d_lo, d_up, d, d, (long long)Bd);
                fflush(stdout);
                char desc[160];
                snprintf(desc, sizeof(desc), "Toeplitz shortened double-circulant Hermitian self-orthogonal code [n=%d, k4=%d]_4 (m=%d, bordered=%d)",
                         n, k4, m, is_odd);
                save_qecc_json(n, k, k4, d, d_lo, d_up, G, desc);
                free(pool);
                return 1;
            }
        }
    }
    printf("  Tested %d valid Hermitian self-orthogonal pairs -> best d = %d (min B_%d-A_%d = %lld)\n",
           tested, best_d, best_d, best_d, (long long)best_Bd);
    free(pool);
    return 0;
}

int main(void) {
    /* Candidate holes in live codetables.de/QECC */
    search_toeplitz_cell(23, 9,  4, 6, 150000, 120000);
    search_toeplitz_cell(32, 18, 4, 5, 150000, 120000);
    search_toeplitz_cell(33, 19, 4, 5, 150000, 120000);
    search_toeplitz_cell(34, 20, 4, 6, 150000, 120000);
    search_toeplitz_cell(39, 23, 4, 6, 200000, 60000);
    search_toeplitz_cell(25, 7,  5, 7, 250000, 25000);
    return 0;
}
