/* m3_mindist: exact minimum distance of a linear code over GF(9) by the column-subset test.

   A nonzero codeword of weight <= W is supported inside some W-subset T of the n coordinates.  With G brought
   to systematic form on an information set I (rest R), a codeword is x G' with x = its values on I, so a
   codeword supported inside T has x supported on I∩T and vanishes on R\T: x restricted to I∩T is a nonzero
   left-kernel vector of A[I∩T, R\T].  The program walks all W-subsets for W = 1, 2, ... and stops at the
   first W where some T gives such a vector; that W is d (all smaller W were checked completely).

   Field: GF(9) = GF(3)[w]/(w^2 - w - 1), element a + b*w stored as a + 3b (0..8), the encoding of the
   claim object.  Arithmetic is done on the (a,b) pairs directly, not with precomputed log tables.

   Input on stdin: "k n" then k rows of n integers 0..8.  Usage: m3_mindist [Wmax]  (default n). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 64
#define MAXK 64

static int ADD[9][9], MUL[9][9], NEG[9], INV[9];

static int enc(int a, int b) { return ((a % 3 + 3) % 3) + 3 * ((b % 3 + 3) % 3); }

static void field_init(void) {
    for (int x = 0; x < 9; x++)
        for (int y = 0; y < 9; y++) {
            int a = x % 3, b = x / 3, c = y % 3, d = y / 3;
            ADD[x][y] = enc(a + c, b + d);
            /* (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2, w^2 = w + 1 */
            MUL[x][y] = enc(a * c + b * d, a * d + b * c + b * d);
        }
    for (int x = 0; x < 9; x++) {
        NEG[x] = enc(-(x % 3), -(x / 3));
        INV[x] = 0;
        for (int y = 1; y < 9; y++)
            if (MUL[x][y] == 1) INV[x] = y;
    }
}

static int k, n;
static int G[MAXK][MAXN];
static int info[MAXK], isinfo[MAXN], red[MAXN], nred;

/* Row-reduce G in place to reduced echelon form; returns the rank and fills info[] with pivot columns. */
static int rref(void) {
    int r = 0;
    for (int c = 0; c < n && r < k; c++) {
        int p = -1;
        for (int i = r; i < k; i++)
            if (G[i][c]) { p = i; break; }
        if (p < 0) continue;
        if (p != r)
            for (int j = 0; j < n; j++) { int t = G[p][j]; G[p][j] = G[r][j]; G[r][j] = t; }
        int iv = INV[G[r][c]];
        for (int j = 0; j < n; j++) G[r][j] = MUL[G[r][j]][iv];
        for (int i = 0; i < k; i++)
            if (i != r && G[i][c]) {
                int f = NEG[G[i][c]];
                for (int j = 0; j < n; j++) G[i][j] = ADD[G[i][j]][MUL[f][G[r][j]]];
            }
        info[r++] = c;
    }
    return r;
}

/* Is there a nonzero x (length t) with sum_i x_i A[S_i][Rc_j] = 0 for all j?  If so, write it to x. */
static int left_kernel(int t, const int *S, int m, const int *Rc, int *x) {
    int B[MAXN][MAXK];   /* m equations in t unknowns: B[j][i] = G[S_i][Rc_j] */
    int pivcol[MAXK], rank = 0;
    for (int j = 0; j < m; j++)
        for (int i = 0; i < t; i++) B[j][i] = G[S[i]][Rc[j]];
    int used[MAXK] = {0};
    for (int c = 0; c < t && rank < m; c++) {
        int p = -1;
        for (int j = rank; j < m; j++)
            if (B[j][c]) { p = j; break; }
        if (p < 0) continue;
        if (p != rank)
            for (int i = 0; i < t; i++) { int tt = B[p][i]; B[p][i] = B[rank][i]; B[rank][i] = tt; }
        int iv = INV[B[rank][c]];
        for (int i = 0; i < t; i++) B[rank][i] = MUL[B[rank][i]][iv];
        for (int j = 0; j < m; j++)
            if (j != rank && B[j][c]) {
                int f = NEG[B[j][c]];
                for (int i = 0; i < t; i++) B[j][i] = ADD[B[j][i]][MUL[f][B[rank][i]]];
            }
        pivcol[rank++] = c;
        used[c] = 1;
    }
    if (rank == t) return 0;
    int free = -1;
    for (int c = 0; c < t; c++)
        if (!used[c]) { free = c; break; }
    for (int i = 0; i < t; i++) x[i] = 0;
    x[free] = 1;
    for (int r = 0; r < rank; r++) x[pivcol[r]] = NEG[B[r][free]];
    return 1;
}

int main(int argc, char **argv) {
    field_init();
    if (scanf("%d %d", &k, &n) != 2 || k < 1 || n < 1 || k > MAXK || n > MAXN) {
        fprintf(stderr, "bad header\n");
        return 2;
    }
    for (int i = 0; i < k; i++)
        for (int j = 0; j < n; j++)
            if (scanf("%d", &G[i][j]) != 1 || G[i][j] < 0 || G[i][j] > 8) {
                fprintf(stderr, "bad entry\n");
                return 2;
            }
    int Wmax = argc > 1 ? atoi(argv[1]) : n;
    int rk = rref();
    printf("k=%d n=%d rank=%d\n", k, n, rk);
    if (rk < k) { printf("RANK_DEFICIENT\n"); return 1; }
    memset(isinfo, 0, sizeof isinfo);
    for (int r = 0; r < k; r++) isinfo[info[r]] = r + 1;
    nred = 0;
    for (int j = 0; j < n; j++)
        if (!isinfo[j]) red[nred++] = j;
    for (int W = 1; W <= Wmax && W <= n; W++) {
        int T[MAXN], inT[MAXN];
        long long subsets = 0;
        for (int i = 0; i < W; i++) T[i] = i;
        for (;;) {
            subsets++;
            memset(inT, 0, sizeof inT);
            for (int i = 0; i < W; i++) inT[T[i]] = 1;
            int S[MAXK], t = 0, Rc[MAXN], m = 0, x[MAXK];
            for (int i = 0; i < W; i++)
                if (isinfo[T[i]]) S[t++] = isinfo[T[i]] - 1;
            for (int j = 0; j < nred; j++)
                if (!inT[red[j]]) Rc[m++] = red[j];
            if (t > 0 && left_kernel(t, S, m, Rc, x)) {
                int c[MAXN], wt = 0;
                for (int j = 0; j < n; j++) {
                    c[j] = 0;
                    for (int i = 0; i < t; i++) c[j] = ADD[c[j]][MUL[x[i]][G[S[i]][j]]];
                    if (c[j]) wt++;
                    if (c[j] && !inT[j]) { printf("INTERNAL_ERROR support outside T\n"); return 3; }
                }
                printf("W=%d complete for all W'<%d; first nonzero codeword supported in a %d-set after %lld subsets\n",
                       W, W, W, subsets);
                printf("d=%d witness_weight=%d witness=", W, wt);
                for (int j = 0; j < n; j++) printf("%d%s", c[j], j + 1 < n ? " " : "\n");
                return 0;
            }
            int i = W - 1;
            while (i >= 0 && T[i] == n - W + i) i--;
            if (i < 0) break;
            T[i]++;
            for (int j = i + 1; j < W; j++) T[j] = T[j - 1] + 1;
        }
        printf("W=%d: no nonzero codeword of weight <= %d (all %lld subsets)\n", W, W, subsets);
        fflush(stdout);
    }
    printf("no codeword found up to W=%d\n", Wmax);
    return 0;
}
