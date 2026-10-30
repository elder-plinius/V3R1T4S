/* Exact EAQECC distance test over GF(3) by position subsets (written from the definition).
   Input (stdin): "n dimI dimN", then dimN rows of 2n entries in {0,1,2} (x part then z part); the first dimI rows
   span the isotropic part I = span(S) ∩ span(S)^perp, all dimN rows span N = span(S)^perp.
   A vector of N \ I with symplectic weight <= W exists  iff  for some W-subset T of positions,
   dim N_T > dim I_T (N_T = vectors of N vanishing outside T).  With OUT = complement of T and N's basis ordered
   I first: dim N_T = dimN - rank(N|OUT), dim I_T = dimI - rank(I|OUT), so the test is
   rank(N|OUT) - rank(I|OUT) < dimN - dimI, i.e. some non-I row becomes dependent during elimination.
   Usage: subset_ea W part parts      examines every W-subset T whose lexicographic index = part (mod parts);
          prints the number of subsets examined and the number (and first) with a vector of N \ I inside T. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct { uint64_t lo, hi; } v3;           /* lo bit = entry 1, hi bit = entry 2 */

static inline v3 add3(v3 a, v3 b) {
    uint64_t a0 = ~(a.lo | a.hi), b0 = ~(b.lo | b.hi);
    v3 r;
    r.lo = (a.lo & b0) | (a0 & b.lo) | (a.hi & b.hi);
    r.hi = (a.hi & b0) | (a0 & b.hi) | (a.lo & b.lo);
    return r;
}
static inline v3 neg3(v3 a) { v3 r = { a.hi, a.lo }; return r; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: subset_ea W part parts\n"); return 2; }
    int W = atoi(argv[1]); long part = atol(argv[2]), parts = atol(argv[3]);
    int n, dI, dN;
    if (scanf("%d %d %d", &n, &dI, &dN) != 3 || n > 32 || dN > 64) { fprintf(stderr, "bad input\n"); return 2; }
    v3 R[64];
    for (int i = 0; i < dN; i++) {
        R[i].lo = R[i].hi = 0;
        for (int j = 0; j < 2 * n; j++) {
            int e; if (scanf("%d", &e) != 1) { fprintf(stderr, "bad row\n"); return 2; }
            e %= 3; if (e < 0) e += 3;
            int bit = (j < n) ? j : 32 + (j - n);
            if (e == 1) R[i].lo |= 1ULL << bit;
            if (e == 2) R[i].hi |= 1ULL << bit;
        }
    }
    int idx[33];
    for (int i = 0; i < W; i++) idx[i] = i;
    long long examined = 0, bad = 0, count = 0;
    int firstbad[33]; int havebad = 0;
    for (;;) {
        if (count % parts == part) {
            examined++;
            uint32_t tmask = 0;
            for (int i = 0; i < W; i++) tmask |= 1u << idx[i];
            uint32_t om32 = (~tmask) & ((n == 32) ? 0xffffffffu : ((1u << n) - 1));
            uint64_t om = (uint64_t)om32 | ((uint64_t)om32 << 32);
            v3 piv[64]; int pc[64]; int np = 0, rI = 0, dependent_nonI = 0;
            for (int i = 0; i < dN; i++) {
                v3 r = { R[i].lo & om, R[i].hi & om };
                for (int j = 0; j < np; j++) {
                    uint64_t b = 1ULL << pc[j];
                    if (r.lo & b) {                      /* r_p = 1 */
                        r = add3(r, (piv[j].lo & b) ? neg3(piv[j]) : piv[j]);
                    } else if (r.hi & b) {               /* r_p = 2 */
                        r = add3(r, (piv[j].hi & b) ? neg3(piv[j]) : piv[j]);
                    }
                }
                uint64_t nz = r.lo | r.hi;
                if (nz) { piv[np] = r; pc[np] = __builtin_ctzll(nz); np++; if (i < dI) rI++; }
                else if (i >= dI) { dependent_nonI = 1; break; }
            }
            (void)rI;
            if (dependent_nonI) {
                bad++;
                if (!havebad) { havebad = 1; for (int i = 0; i < W; i++) firstbad[i] = idx[i]; }
            }
        }
        count++;
        int i = W - 1;
        while (i >= 0 && idx[i] == n - W + i) i--;
        if (i < 0) break;
        idx[i]++;
        for (int j = i + 1; j < W; j++) idx[j] = idx[j - 1] + 1;
    }
    printf("W=%d part=%ld/%ld total_subsets=%lld examined=%lld with_vector_outside_isotropic=%lld", W, part, parts, count, examined, bad);
    if (havebad) { printf(" first="); for (int i = 0; i < W; i++) printf("%s%d", i ? "," : "", firstbad[i]); }
    printf("\n");
    return 0;
}
