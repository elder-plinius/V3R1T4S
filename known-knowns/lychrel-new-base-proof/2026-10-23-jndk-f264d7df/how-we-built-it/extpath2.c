/* Exterior column automaton for reverse-and-add template cycles.
   Depth j counts digits from the outside: left depth j (j-th most significant digit) always pairs with right depth j.
   A template cycle of period p with overflow signature o (o_t = 1 iff step t creates a new leading digit) is, at every
   fixed depth j and for large parameter, time-periodic with period p. Column at depth j = (l_j(t), r_j(t))_{t<p}.
   Rules (exact): s = l_j(t) + r_j(t);
     right: r_j(t+1) = (s + cR_j(t)) mod b, cR_{j+1}(t) = (s + cR_j(t)) div b, cR_1 = 0;
     left : u_j(t) = (s + cL_{j+1}(t)) mod b, cL_j(t) = (s + cL_{j+1}(t)) div b, cL_1(t) = o_t;
            l_j(t+1) = u_{j-1}(t) if o_t = 1 (u_0 := 1, the new leading digit) else u_j(t);
     periodic: l_j(p) = l_j(0), r_j(p) = r_j(0); l_1(t) >= 1.
   State between depth j-1 and j: (cR_j(.), cL_j(.) required, u_{j-1}(t) for o_t = 1).
   Every affine run-length template cycle has, past its constant outer runs, a stretch of identical columns, i.e. a
   reachable state with a self-loop. This program explores the full reachable graph from the head state and reports
   whether a self-loop (and whether any cycle) is reachable. Exhaustive unless CAPPED is printed.
   usage: ext b p [maxstates]   (loops over all overflow signatures o != 0, one per rotation class) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef struct {int l[16], r[16];} Col;

static int b, p, K, o[16], opos[16], dbits;
static long maxstates = 20000000;

/* hash set of states */
static uint64_t *keys; static long *ids; static long hcap;
static uint64_t *stlist; static long nst;
static long *estart_dummy;
/* edges */
static long *esrc, *edst; static long ne, ecap;
static long loopst[12]; static Col loopcol[12]; static int nloops;

static long hfind(uint64_t k, int insert, int *isnew) {
    uint64_t h = k * 0x9E3779B97F4A7C15ULL; long i = (long)(h >> 20) & (hcap - 1);
    while (keys[i] != 0) { if (keys[i] == k) { *isnew = 0; return ids[i]; } i = (i + 1) & (hcap - 1); }
    if (!insert) { *isnew = 0; return -1; }
    keys[i] = k; ids[i] = nst; stlist[nst] = k; *isnew = 1; return nst++;
}
/* key layout (ext2): bit 63 flag, bit 62 head, bits 0..p-1 cR, p..2p-1 need, then K digits of dbits bits */
static uint64_t mk(int head, int cR, int need, int *up) {
    uint64_t k = (1ULL << 63) | ((uint64_t)head << 62) | (uint64_t)cR | ((uint64_t)need << p);
    for (int i = 0; i < K; i++) k |= (uint64_t)up[i] << (2 * p + dbits * i);
    return k;
}
static void unk(uint64_t k, int *head, int *cR, int *need, int *up) {
    *head = (k >> 62) & 1; *cR = k & ((1 << p) - 1); *need = (k >> p) & ((1 << p) - 1);
    for (int i = 0; i < K; i++) up[i] = (k >> (2 * p + dbits * i)) & ((1 << dbits) - 1);
}

/* successor enumeration */
static int g_head, g_cR, g_need, g_up[16];
static int l0, r0, cRo, cinb, un[16];
static uint64_t *succ; static int nsucc, succcap;
static int curL[16], curR[16];
static Col *succcol; static Col *colof; static long *par;

static void rec(int t, int l, int r) {
    curL[t] = l; curR[t] = r;
    int s = l + r;
    int vR = s + ((g_cR >> t) & 1);
    int rn = vR % b, cro = vR / b;
    int needt = (g_need >> t) & 1;
    for (int cin = 0; cin <= 1; cin++) {
        int vL = s + cin; if (vL / b != needt) continue;
        int u = vL % b;
        int ln = o[t] ? g_up[opos[t]] : u;
        if (g_head && ln == 0) continue;
        int save_cRo = cRo, save_cin = cinb;
        cRo |= cro << t; cinb |= cin << t;
        if (o[t]) un[opos[t]] = u;
        if (t == p - 1) {
            if (rn == r0 && ln == l0) {
                uint64_t k = mk(0, cRo, cinb, un);
                if (nsucc == succcap) { succcap *= 2; succ = realloc(succ, succcap * sizeof(uint64_t)); succcol = realloc(succcol, succcap * sizeof(Col)); }
                for (int q = 0; q < p; q++) { succcol[nsucc].l[q] = curL[q]; succcol[nsucc].r[q] = curR[q]; }
                succ[nsucc++] = k;
            }
        } else rec(t + 1, ln, rn);
        cRo = save_cRo; cinb = save_cin;
    }
}
static void successors(uint64_t k) {
    unk(k, &g_head, &g_cR, &g_need, g_up); nsucc = 0;
    for (l0 = g_head ? 1 : 0; l0 < b; l0++)
        for (r0 = 0; r0 < b; r0++) { cRo = 0; cinb = 0; rec(0, l0, r0); }
}
static int cmpu(const void *a, const void *c) { uint64_t x = *(uint64_t *)a, y = *(uint64_t *)c; return x < y ? -1 : x > y; }

static void run_case(void) {
    K = 0; for (int t = 0; t < p; t++) { opos[t] = o[t] ? K : -1; if (o[t]) K++; }
    memset(keys, 0, hcap * sizeof(uint64_t)); nst = 0; ne = 0;
    int up[16]; for (int i = 0; i < 16; i++) up[i] = 1;
    int need = 0; for (int t = 0; t < p; t++) need |= o[t] << t;
    int isnew; hfind(mk(1, 0, need, up), 1, &isnew);
    nloops = 0; long qi = 0, selfloops = 0; int capped = 0; long firstloop = -1;
    while (qi < nst) {
        if (nst > maxstates) { capped = 1; break; }
        uint64_t k = stlist[qi];
        successors(k);
        for (int i = 0; i < nsucc; i++) {
            long d = hfind(succ[i], 1, &isnew);
            if (isnew) { par[d] = qi; colof[d] = succcol[i]; }
            if (d == qi && nloops < 12) { loopst[nloops] = qi; loopcol[nloops++] = succcol[i]; }
            if (d == qi) { selfloops++; if (firstloop < 0) firstloop = qi; }
            if (ne == ecap) { ecap *= 2; esrc = realloc(esrc, ecap * sizeof(long)); edst = realloc(edst, ecap * sizeof(long)); }
            esrc[ne] = qi; edst[ne] = d; ne++;
        }
        qi++;
    }
    /* cycle detection: Kahn on the explored graph */
    int cyc = -1;
    if (!capped) {
        long *indeg = calloc(nst, sizeof(long)), *start = calloc(nst + 1, sizeof(long)), *adj = malloc((ne + 1) * sizeof(long));
        for (long e = 0; e < ne; e++) { indeg[edst[e]]++; start[esrc[e] + 1]++; }
        for (long i = 0; i < nst; i++) start[i + 1] += start[i];
        long *fill = calloc(nst, sizeof(long));
        for (long e = 0; e < ne; e++) adj[start[esrc[e]] + fill[esrc[e]]++] = edst[e];
        long *q = malloc(nst * sizeof(long)), qh = 0, qt = 0, removed = 0;
        for (long i = 0; i < nst; i++) if (!indeg[i]) q[qt++] = i;
        while (qh < qt) { long v = q[qh++]; removed++; for (long e = start[v]; e < start[v + 1]; e++) if (--indeg[adj[e]] == 0) q[qt++] = adj[e]; }
        cyc = removed < nst;
        free(indeg); free(start); free(adj); free(fill); free(q);
    }
    printf("CASE b=%d p=%d o=", b, p); for (int t = 0; t < p; t++) printf("%d", o[t]);
    printf(" states=%ld edges=%ld selfloop_states=%ld cycle=%s %s", nst, ne, selfloops,
           cyc < 0 ? "?" : (cyc ? "yes" : "no"), capped ? "CAPPED" : "EXHAUSTIVE");
    if (firstloop >= 0) {
        int h, cR, nd, u[16]; unk(stlist[firstloop], &h, &cR, &nd, u);
        printf(" loop_example=cR:%d,cL:%d,up:", cR, nd); for (int i = 0; i < K; i++) printf("%d.", u[i]);
    }
    printf("\n");
    for (int z = 0; z < nloops; z++) {
        static long chain[1 << 16]; int nc = 0; long v = loopst[z];
        while (v != 0 && nc < (1 << 16)) { chain[nc++] = v; v = par[v]; }
        printf("PATH %d depth=%d\n", z, nc);
        for (int i = nc - 1; i >= 0; i--) { printf(" col"); for (int t = 0; t < p; t++) printf(" %d:%d", colof[chain[i]].l[t], colof[chain[i]].r[t]); printf("\n"); }
        printf(" bulk"); for (int t = 0; t < p; t++) printf(" %d:%d", loopcol[z].l[t], loopcol[z].r[t]); printf("\n");
    }
    fflush(stdout);
}

int main(int argc, char **argv) {
    b = atoi(argv[1]); p = atoi(argv[2]); if (argc > 3) maxstates = atol(argv[3]);
    dbits = 1; while ((1 << dbits) < b) dbits++;
    if (b > 63 || p > 12) { fprintf(stderr, "limits\n"); return 2; }
    hcap = 1; while (hcap < 2 * maxstates + 16) hcap <<= 1;
    keys = calloc(hcap, sizeof(uint64_t)); ids = malloc(hcap * sizeof(long)); stlist = malloc((maxstates + 2) * sizeof(uint64_t));
    ecap = 1 << 20; esrc = malloc(ecap * sizeof(long)); edst = malloc(ecap * sizeof(long));
    succcap = 1 << 16; succ = malloc(succcap * sizeof(uint64_t)); succcol = malloc(succcap * sizeof(Col)); colof = malloc((maxstates + 2) * sizeof(Col)); par = malloc((maxstates + 2) * sizeof(long));
    if (argc > 4) { for (int t = 0; t < p; t++) o[t] = argv[4][t] - '0'; K = 0; for (int t = 0; t < p; t++) K += o[t]; run_case(); return 0; }
    for (int mask = 1; mask < (1 << p); mask++) {
        /* canonical under rotation: smallest rotation value */
        int best = mask;
        for (int r = 1; r < p; r++) { int rot = ((mask >> r) | (mask << (p - r))) & ((1 << p) - 1); if (rot < best) best = rot; }
        if (best != mask) continue;
        for (int t = 0; t < p; t++) o[t] = (mask >> t) & 1;
        { int kk = 0; for (int t = 0; t < p; t++) kk += o[t]; if (2 * p + kk * dbits > 62) { printf("CASE b=%d p=%d mask=%d SKIPPED-KEY-WIDTH\n", b, p, mask); continue; } }
        run_case();
    }
    return 0;
}
