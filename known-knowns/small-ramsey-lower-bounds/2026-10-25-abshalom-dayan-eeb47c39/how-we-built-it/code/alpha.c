/* alpha.c: exact decision "does graph G have an independent set of size >= k?" by bitset branch and bound
 * (max-clique search on the complement, greedy-colouring bound in the style of Tomita MCQ / San Segundo BBMC;
 * colour classes of the complement are cliques of G).  Based on the has_clique core of
 * an earlier run's wit.c (not shipped), extended with: adjacency-matrix input, a general mode,
 * a vertex-transitive mode for circulants (verified in-code), a restriction set, vertex ordering, caps and stats.
 * usage: alpha <file.adj> <k> <mode: sym|nosym> [-r allowed.txt] [-t seconds] [-o 0|1]
 *   sym   : requires G circulant on Z_N (checked: A[i][j] == A[0][(j-i) mod N] for all i,j, else abort);
 *           searches only independent sets containing vertex 0 (valid: rotations are automorphisms, so any
 *           independent k-set maps to one containing 0).
 *   nosym : no symmetry assumption (general graphs).
 *   -r    : restrict to the listed vertices (0-based; e.g. G - S). Not allowed with sym.
 *   -o 1  : relabel the candidate set by a degeneracy order of the complement (default 1).
 * Output lines: "RESULT FOUND <verts>" (witness, 0-based, re-verified in-code), "RESULT NONE" (exact: the
 * search finished), or "RESULT UNKNOWN" (time cap hit). Always prints nodes and seconds. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#define MAXN 512
#define MAXW (MAXN/64)
typedef uint64_t u64;
static int n, W;
static unsigned char G0[MAXN][MAXN];
static u64 C[MAXN][MAXW];          /* complement adjacency in relabelled order */
static int perm[MAXN];             /* new index -> original vertex */
static int stk[MAXN];
static long long nodes = 0; static double tcap = 1e18, t0; static int timed_out = 0;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static inline int popc(const u64 *P) { int c = 0; for (int i = 0; i < W; i++) c += __builtin_popcountll(P[i]); return c; }

static int has_clique(const u64 *Pin, int k, int depth) {
    if (k <= 0) return 1;
    if ((++nodes & 0xFFFF) == 0 && now() - t0 > tcap) timed_out = 1;
    if (timed_out) return 0;
    u64 P[MAXW]; memcpy(P, Pin, W * 8);
    int cnt = popc(P);
    if (cnt < k) return 0;
    if (k == 1) { for (int i = 0; i < W; i++) if (P[i]) { stk[depth] = i * 64 + __builtin_ctzll(P[i]); return 1; } }
    short verts[MAXN], cols[MAXN]; int nv = 0;
    u64 U[MAXW], Q[MAXW]; memcpy(U, P, W * 8);
    int col = 0, left = cnt;
    while (left > 0) {
        col++; memcpy(Q, U, W * 8);
        for (int i = 0; i < W; i++) while (Q[i]) {
            int b = __builtin_ctzll(Q[i]); int v = i * 64 + b;
            Q[i] &= Q[i] - 1; U[i] &= ~(1ULL << b);
            for (int j = 0; j < W; j++) Q[j] &= ~C[v][j];
            verts[nv] = v; cols[nv] = col; nv++; left--;
        }
    }
    if (col < k) return 0;
    for (int idx = nv - 1; idx >= 0; idx--) {
        if (cols[idx] < k) return 0;
        int v = verts[idx]; u64 NP[MAXW];
        for (int j = 0; j < W; j++) NP[j] = P[j] & C[v][j];
        stk[depth] = v;
        if (has_clique(NP, k - 1, depth + 1)) return 1;
        if (timed_out) return 0;
        P[v >> 6] &= ~(1ULL << (v & 63));
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 2; }
    const char *fn = argv[1]; int k = atoi(argv[2]); int sym = strcmp(argv[3], "sym") == 0;
    if (!sym && strcmp(argv[3], "nosym") != 0) { fprintf(stderr, "mode?\n"); return 2; }
    const char *rf = NULL; int ord = 1;
    for (int i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "-r")) rf = argv[++i];
        else if (!strcmp(argv[i], "-t")) tcap = atof(argv[++i]);
        else if (!strcmp(argv[i], "-o")) ord = atoi(argv[++i]);
    }
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); return 2; }
    char line[MAXN + 8]; n = 0;
    while (fgets(line, sizeof line, f)) {
        int L = strlen(line); while (L && (line[L-1] == '\n' || line[L-1] == '\r')) line[--L] = 0;
        if (!L) continue;
        if (n >= MAXN) { fprintf(stderr, "too big\n"); return 2; }
        for (int j = 0; j < L; j++) G0[n][j] = line[j] == '1';
        if (n == 0) W = L; else if (L != W) { fprintf(stderr, "ragged\n"); return 2; }
        n++;
    }
    fclose(f);
    if (W != n) { fprintf(stderr, "not square\n"); return 2; }
    for (int i = 0; i < n; i++) { if (G0[i][i]) { fprintf(stderr, "diag\n"); return 2; }
        for (int j = 0; j < n; j++) if (G0[i][j] != G0[j][i]) { fprintf(stderr, "asym\n"); return 2; } }
    W = (n + 63) / 64;
    int allowed[MAXN]; for (int i = 0; i < n; i++) allowed[i] = 1;
    if (rf) {
        if (sym) { fprintf(stderr, "-r not allowed with sym\n"); return 2; }
        for (int i = 0; i < n; i++) allowed[i] = 0;
        FILE *g = fopen(rf, "r"); int v; while (fscanf(g, "%d", &v) == 1) allowed[v] = 1; fclose(g);
    }
    int need = k;
    if (sym) {
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++)
            if (G0[i][j] != G0[0][(j - i + n) % n]) { fprintf(stderr, "sym mode refused: graph is not circulant on Z_N\n"); return 3; }
        for (int i = 0; i < n; i++) allowed[i] = (i != 0 && !G0[0][i]);   /* non-neighbours of 0 */
        need = k - 1;
    }
    /* candidate list, then optional degeneracy relabelling on the complement induced by the candidates */
    int cand[MAXN], nc = 0; for (int i = 0; i < n; i++) if (allowed[i]) cand[nc++] = i;
    if (ord) {
        int deg[MAXN], alive[MAXN], out[MAXN];
        for (int a = 0; a < nc; a++) { alive[a] = 1; deg[a] = 0; for (int b = 0; b < nc; b++) if (a != b && !G0[cand[a]][cand[b]]) deg[a]++; }
        for (int pos = nc - 1; pos >= 0; pos--) {    /* min complement degree goes last */
            int best = -1; for (int a = 0; a < nc; a++) if (alive[a] && (best < 0 || deg[a] < deg[best])) best = a;
            out[pos] = cand[best]; alive[best] = 0;
            for (int b = 0; b < nc; b++) if (alive[b] && !G0[cand[best]][cand[b]]) deg[b]--;
        }
        memcpy(cand, out, nc * sizeof(int));
    }
    for (int a = 0; a < nc; a++) perm[a] = cand[a];
    int m = nc; int Wsave = W; W = (m + 63) / 64; if (W == 0) W = 1;
    for (int a = 0; a < m; a++) { memset(C[a], 0, sizeof C[a]); for (int b = 0; b < m; b++) if (a != b && !G0[perm[a]][perm[b]]) C[a][b >> 6] |= 1ULL << (b & 63); }
    u64 P[MAXW] = {0}; for (int a = 0; a < m; a++) P[a >> 6] |= 1ULL << (a & 63);
    (void)Wsave;
    t0 = now();
    int r = has_clique(P, need, 0);
    double dt = now() - t0;
    printf("graph %s N %d k %d mode %s candidates %d need %d\n", fn, n, k, sym ? "sym(fix 0)" : "nosym", m, need);
    if (r) {
        int wit[MAXN], nw = 0; if (sym) wit[nw++] = 0;
        for (int i = 0; i < need; i++) wit[nw++] = perm[stk[i]];
        int ok = 1; for (int a = 0; a < nw; a++) for (int b = a + 1; b < nw; b++) if (G0[wit[a]][wit[b]] || wit[a] == wit[b]) ok = 0;
        printf("RESULT FOUND size %d independent_check %s :", nw, ok ? "ok" : "FAILED");
        for (int a = 0; a < nw; a++) printf(" %d", wit[a]); printf("\n");
    } else if (timed_out) printf("RESULT UNKNOWN (time cap %.0f s)\n", tcap);
    else printf("RESULT NONE (exact: search completed)\n");
    printf("nodes %lld seconds %.3f\n", nodes, dt);
    return 0;
}
