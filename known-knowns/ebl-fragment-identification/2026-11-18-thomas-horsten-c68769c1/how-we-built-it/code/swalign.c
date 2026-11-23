/* Deterministic full-matrix Smith-Waterman sign-level local alignment, line tracking.
 * X_CODE (-1) is the damaged wildcard: matches any real token with score xmatch.
 * Frozen tie-break: diag >= up >= left  (diag on tie, up over left on tie).
 * Backtrack follows the trace and stops when H reaches 0.
 */
#include <stdlib.h>
#define X_CODE (-1)

int sw_align(const int *a, int n, const int *a_line,
             const int *b, int m, const int *b_line,
             int band, int match, int mismatch, int gap, int xmatch,
             int min_block,
             long *o_score, long *o_aligned, long *o_mism, long *o_wild,
             int *o_alo, int *o_ahi, int *o_blo, int *o_bhi)
{
    (void)band; /* full matrix; band kept for API compatibility */
    if (n <= 0 || m <= 0) return 0;
    long *H    = (long*)calloc((size_t)(n+1)*(m+1), sizeof(long));
    unsigned char *TR = (unsigned char*)calloc((size_t)(n+1)*(m+1), sizeof(unsigned char));
    if (!H || !TR) { free(H); free(TR); return -1; }
    long best = 0; int bi = 0, bj = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int ai = a[i-1], bv = b[j-1];
            long s;
            if (ai == bv) s = match;
            else if (ai == X_CODE || bv == X_CODE) s = xmatch;
            else s = mismatch;
            long d = H[(size_t)(i-1)*(m+1)+(j-1)] + s;
            long u = H[(size_t)(i-1)*(m+1)+j]     + gap;
            long l = H[(size_t)i*(m+1)+(j-1)]     + gap;
            long v = d; unsigned char t = 0;      /* diag default */
            if (u >= v) { v = u; t = 1; }          /* up wins tie vs diag */
            if (l >  v) { v = l; t = 2; }          /* left must strictly exceed */
            H[(size_t)i*(m+1)+j] = v;
            TR[(size_t)i*(m+1)+j] = t;
            if (v > best) { best = v; bi = i; bj = j; }
        }
    }
    if (best <= 0) { free(H); free(TR); return 0; }
    int i = bi, j = bj;
    long aligned = 0, mism = 0, wild = 0;
    int alo = 1000000000, ahi = -1, blo = 1000000000, bhi = -1;
    int guard = 0, maxg = n + m + 4;
    while (i > 0 && j > 0 && H[(size_t)i*(m+1)+j] > 0 && guard < maxg) {
        guard++;
        unsigned char t = TR[(size_t)i*(m+1)+j];
        if (t == 0) {
            int ai = a[i-1], bv = b[j-1];
            aligned++;
            if (ai == bv) { }
            else if (ai == X_CODE || bv == X_CODE) wild++;
            else mism++;
            int li = a_line[i-1], lj = b_line[j-1];
            if (li < alo) alo = li; if (li > ahi) ahi = li;
            if (lj < blo) blo = lj; if (lj > bhi) bhi = lj;
            i--; j--;
        } else if (t == 1) { i--; }
        else { j--; }
    }
    if (ahi < 0) ahi = 0; if (alo > ahi) alo = ahi;
    if (bhi < 0) bhi = 0; if (blo > bhi) blo = bhi;
    if (aligned < min_block) { free(H); free(TR); return 0; }
    *o_score = best; *o_aligned = aligned; *o_mism = mism; *o_wild = wild;
    *o_alo = alo; *o_ahi = ahi; *o_blo = blo; *o_bhi = bhi;
    free(H); free(TR);
    return 1;
}
