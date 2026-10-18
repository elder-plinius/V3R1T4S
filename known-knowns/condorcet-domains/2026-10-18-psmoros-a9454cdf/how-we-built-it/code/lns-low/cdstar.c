/* cdstar.c -- exact "star" optimisation (lens lns-low, run 2026-10-17-2220).
 *
 * Problem: fix the never conditions on every triple that avoids alternative x; choose the conditions on all
 * C(n-1,2) triples {x,a,b} to maximise the size of the full domain.  Every order of the full domain is an order pi
 * of the fixed sub-domain (the full domain F of the restricted assignment on [n]\{x}) with x inserted at one of n
 * slots, and it is valid iff for every pair {a,b} the relative order of {a,b,x} is allowed by the condition chosen
 * for {a,b,x}.  So |domain| = number of items (pi, slot) all of whose unary pair-constraints hold: a max-coverage
 * problem.  Exact DFS branch and bound over the pairs with bitsets of items:
 *   - bound(node) = min over undecided pairs p of max over options o of |alive & allowed[p][o]|  (valid upper bound)
 *   - branch on the undecided pair with the smallest such max (fail first)
 *   - dominance: an option whose surviving set is contained in another option's surviving set is skipped
 *     (equal sets: keep one), which is exact because the final count is monotone in the surviving set.
 * The search is exhaustive unless the time cap is hit; the output says which.
 *
 * Modes:
 *   cdstar star N in.npy X OPTS SECS [INCUMBENT] [out.npy]
 *       sub-assignment = in.npy (an N-assignment) restricted to triples avoiding X (0-based); incumbent default =
 *       count of in.npy (so it searches for a STRICT improvement); writes out.npy if a better assignment is found.
 *   cdstar ext M in.npy OPTS SECS INCUMBENT [out.npy]
 *       one-point extension of the M-assignment in.npy: N = M+1, new alternative x = N-1 (label-free problem),
 *       searches for an extension of size > INCUMBENT.
 * OPTS: pp6 (never top / never bottom for every member) or all9 (never-middle too).
 * Encoding as lsearch.c: colex triple index C(c,3)+C(b,2)+a, code 3*s+p (s subject index in the sorted triple,
 * p forbidden position 0 top 1 middle 2 bottom).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 26
typedef unsigned long long u64;
static long long binom(int n, int k) { if (k < 0 || n < k) return 0; long long r = 1; for (int i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }
static int tidx(int a, int b, int c) { return (int)(binom(c, 3) + binom(b, 2) + a); }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static int N, NT;
static unsigned char *cond;   /* N-assignment; 9 = free */

static unsigned char *loadnpy(const char *path, int nt) {
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    unsigned char hdr[10]; if (fread(hdr, 1, 10, f) != 10) exit(2);
    int hl = hdr[8] | (hdr[9] << 8); fseek(f, 10 + hl, SEEK_SET);
    unsigned char *c = malloc(nt); if ((int)fread(c, 1, nt, f) != nt) { fprintf(stderr, "short file %s\n", path); exit(3); } fclose(f); return c;
}
static void savenpy(const char *path, unsigned char *c, int nt) {
    FILE *f = fopen(path, "wb"); char h[128]; int l = snprintf(h, sizeof h, "{'descr': '|u1', 'fortran_order': False, 'shape': (%d,), }", nt);
    int tot = 10 + l + 1; int pad = (64 - tot % 64) % 64; fwrite("\x93NUMPY\x01\x00", 1, 8, f);
    int hl = l + pad + 1; unsigned char b[2] = {(unsigned char)(hl & 255), (unsigned char)(hl >> 8)}; fwrite(b, 1, 2, f);
    fwrite(h, 1, l, f); for (int i = 0; i < pad; i++) fputc(' ', f); fputc('\n', f); fwrite(c, 1, nt, f); fclose(f);
}

/* rank of member s (0..2 in label order) in order given by positions */
static int allowed_code(int code, const int rk[3]) { int s = code / 3, p = code % 3; return rk[s] != p; }

/* ---- enumerate the sub-domain: orders of the N-1 alternatives != X obeying all triples avoiding X ---- */
static int X; static int ALT[MAXN], NA; /* alternatives other than X */
static int *ORD; static long NORD, CAPORD;
static int cur[MAXN], posof[MAXN];
static int okplace(int depth, int e) {
    /* e placed at position depth; check every triple {u,v,e} with u,v already placed -> e is bottom so far; triples
       with exactly one other placed are checked at the end via full check (simpler: check full triples only) */
    for (int i = 0; i < depth; i++) for (int j = i + 1; j < depth; j++) {
        int u = cur[i], v = cur[j]; int a = u, b = v, c = e, z;
        if (a > b) { z = a; a = b; b = z; } if (b > c) { z = b; b = c; c = z; } if (a > b) { z = a; a = b; b = z; }
        int code = cond[tidx(a, b, c)]; if (code >= 9) continue;
        int tri[3] = {a, b, c}; int rk[3];
        for (int r = 0; r < 3; r++) { int w = tri[r]; rk[r] = (w == u) ? 0 : (w == v ? 1 : 2); }
        if (!allowed_code(code, rk)) return 0;
    }
    return 1;
}
static void edfs(int depth, unsigned used) {
    if (depth == NA) {
        if (NORD >= CAPORD) { CAPORD = CAPORD ? 2 * CAPORD : 4096; ORD = realloc(ORD, sizeof(int) * CAPORD * NA); }
        memcpy(ORD + NORD * NA, cur, sizeof(int) * NA); NORD++; return;
    }
    for (int i = 0; i < NA; i++) { int e = ALT[i]; if (used >> e & 1) continue; if (!okplace(depth, e)) continue; cur[depth] = e; edfs(depth + 1, used | (1u << e)); }
}

/* ---- items and bitsets ---- */
static int NP; static int PA[400], PB[400], PT[400]; /* pair p = {PA,PB} with X; PT = triple index */
static int OPTS[9], NOPT;
static long NITEM; static int W;
static u64 *ALW; /* ALW[(p*NOPT+o)*W + w] */
static double TCAP, T0; static long NODES; static int TIMEOUT;
static long BEST; static unsigned char BESTOPT[400]; static unsigned char CUROPT[400];
static int decided[400];

static inline long pc(const u64 *a, int w) { long s = 0; for (int i = 0; i < w; i++) s += __builtin_popcountll(a[i]); return s; }
static inline long pcand(const u64 *a, const u64 *b, int w) { long s = 0; for (int i = 0; i < w; i++) s += __builtin_popcountll(a[i] & b[i]); return s; }

static u64 *STK; /* alive bitsets per depth */
static void dfs(int depth, const u64 *alive) {
    NODES++;
    if ((NODES & 1023) == 0 && now() - T0 > TCAP) TIMEOUT = 1;
    if (TIMEOUT) return;
    long acnt = pc(alive, W);
    if (acnt <= BEST) return;
    if (depth == NP) { BEST = acnt; memcpy(BESTOPT, CUROPT, NP); printf("  found %ld at node %ld t %.1fs\n", BEST, NODES, now() - T0); fflush(stdout); return; }
    /* bound and variable choice */
    int bp = -1; long bmax = 1L << 60; long cnt[9];
    for (int p = 0; p < NP; p++) if (!decided[p]) {
        long mx = 0;
        for (int o = 0; o < NOPT; o++) { long c = pcand(alive, ALW + ((long)p * NOPT + o) * W, W); if (c > mx) mx = c; }
        if (mx < bmax) { bmax = mx; bp = p; }
        if (mx <= BEST) return; /* bound */
    }
    for (int o = 0; o < NOPT; o++) cnt[o] = pcand(alive, ALW + ((long)bp * NOPT + o) * W, W);
    /* dominance among options of bp */
    int keepo[9], nk = 0;
    for (int o = 0; o < NOPT; o++) {
        if (cnt[o] <= BEST) continue;
        int dom = 0;
        for (int o2 = 0; o2 < NOPT && !dom; o2++) {
            if (o2 == o || cnt[o2] < cnt[o]) continue;
            if (cnt[o2] == cnt[o] && o2 > o) continue; /* equal sets: keep the smaller index */
            const u64 *A = ALW + ((long)bp * NOPT + o) * W, *B = ALW + ((long)bp * NOPT + o2) * W; int sub = 1;
            for (int i = 0; i < W; i++) if ((alive[i] & A[i]) & ~(alive[i] & B[i])) { sub = 0; break; }
            if (sub) dom = 1;
        }
        if (!dom) keepo[nk++] = o;
    }
    for (int a = 0; a < nk; a++) for (int b = a + 1; b < nk; b++) if (cnt[keepo[b]] > cnt[keepo[a]]) { int z = keepo[a]; keepo[a] = keepo[b]; keepo[b] = z; }
    decided[bp] = 1;
    u64 *nxt = STK + (long)(depth + 1) * W;
    for (int a = 0; a < nk; a++) {
        int o = keepo[a]; if (cnt[o] <= BEST) break;
        const u64 *A = ALW + ((long)bp * NOPT + o) * W;
        for (int i = 0; i < W; i++) nxt[i] = alive[i] & A[i];
        CUROPT[bp] = (unsigned char)o;
        dfs(depth + 1, nxt);
        if (TIMEOUT) break;
    }
    decided[bp] = 0;
}

static void set_opts(const char *s) {
    if (!strcmp(s, "pp6")) { int o[] = {0, 2, 3, 5, 6, 8}; NOPT = 6; memcpy(OPTS, o, sizeof o); }
    else { NOPT = 9; for (int i = 0; i < 9; i++) OPTS[i] = i; }
}

static int solve(long incumbent, const char *outp) {
    NA = 0; for (int i = 0; i < N; i++) if (i != X) ALT[NA++] = i;
    NORD = 0; edfs(0, 0);
    NP = 0;
    for (int i = 0; i < NA; i++) for (int j = i + 1; j < NA; j++) { int a = ALT[i], b = ALT[j]; PA[NP] = a; PB[NP] = b;
        int u[3] = {a, b, X}, z; if (u[0] > u[1]) { z = u[0]; u[0] = u[1]; u[1] = z; } if (u[1] > u[2]) { z = u[1]; u[1] = u[2]; u[2] = z; } if (u[0] > u[1]) { z = u[0]; u[0] = u[1]; u[1] = z; }
        PT[NP] = tidx(u[0], u[1], u[2]); NP++; }
    NITEM = NORD * N; W = (int)((NITEM + 63) / 64);
    ALW = calloc((size_t)NP * NOPT * W, sizeof(u64));
    for (long r = 0; r < NORD; r++) {
        int *pi = ORD + r * NA; int pos[MAXN]; for (int i = 0; i < NA; i++) pos[pi[i]] = i;
        for (int k = 0; k < N; k++) { /* x inserted before pi[k] (k = NA: bottom) */
            long it = r * N + k;
            for (int p = 0; p < NP; p++) {
                int a = PA[p], b = PB[p];
                int qa = pos[a] < k ? pos[a] : pos[a] + 1, qb = pos[b] < k ? pos[b] : pos[b] + 1, qx = k;
                int u[3] = {a, b, X}, q[3] = {qa, qb, qx};
                /* sort members by label */
                for (int s = 0; s < 3; s++) for (int t = s + 1; t < 3; t++) if (u[t] < u[s]) { int z = u[s]; u[s] = u[t]; u[t] = z; z = q[s]; q[s] = q[t]; q[t] = z; }
                int rk[3]; for (int s = 0; s < 3; s++) rk[s] = (q[(s + 1) % 3] < q[s]) + (q[(s + 2) % 3] < q[s]);
                for (int o = 0; o < NOPT; o++) if (allowed_code(OPTS[o], rk)) ALW[((long)p * NOPT + o) * W + (it >> 6)] |= 1ULL << (it & 63);
            }
        }
    }
    printf("star n %d x %d subdomain %ld items %ld pairs %d opts %d incumbent %ld\n", N, X, NORD, NITEM, NP, NOPT, incumbent); fflush(stdout);
    STK = malloc(sizeof(u64) * W * (NP + 2));
    for (long i = 0; i < W; i++) STK[i] = 0; for (long it = 0; it < NITEM; it++) STK[it >> 6] |= 1ULL << (it & 63);
    BEST = incumbent; NODES = 0; TIMEOUT = 0; memset(decided, 0, sizeof decided); T0 = now();
    long inc0 = incumbent;
    dfs(0, STK);
    printf("result n %d x %d best %ld (incumbent %ld) improved %s nodes %ld time %.1fs %s\n", N, X, BEST, inc0, BEST > inc0 ? "YES" : "no", NODES, now() - T0,
           TIMEOUT ? "TIMEOUT (not exhaustive)" : "EXHAUSTIVE (proved: no assignment of the star triples gives more than best)");
    if (BEST > inc0 && outp) {
        for (int p = 0; p < NP; p++) cond[PT[p]] = (unsigned char)OPTS[BESTOPT[p]];
        savenpy(outp, cond, NT); printf("wrote %s\n", outp);
    }
    fflush(stdout);
    free(ALW); free(STK);
    return BEST > inc0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "see header\n"); return 1; }
    if (!strcmp(argv[1], "star")) {
        N = atoi(argv[2]); NT = (int)binom(N, 3); cond = loadnpy(argv[3], NT); X = atoi(argv[4]); set_opts(argv[5]); TCAP = atof(argv[6]);
        /* incumbent default: current count = number of items valid under current conditions; computed by solve if <0 */
        long inc = argc > 7 ? atol(argv[7]) : -1;
        unsigned char *keep = malloc(NT); memcpy(keep, cond, NT);
        if (inc < 0) { /* count current full domain by enumerating with all triples */
            /* simple: run the item construction with the current star conditions as the only option */
            inc = 0;
            NA = 0; for (int i = 0; i < N; i++) if (i != X) ALT[NA++] = i;
            NORD = 0; edfs(0, 0);
            for (long r = 0; r < NORD; r++) { int *pi = ORD + r * NA; int pos[MAXN]; for (int i = 0; i < NA; i++) pos[pi[i]] = i;
                for (int k = 0; k < N; k++) { int ok = 1;
                    for (int i = 0; i < NA && ok; i++) for (int j = i + 1; j < NA && ok; j++) { int a = ALT[i], b = ALT[j];
                        int qa = pos[a] < k ? pos[a] : pos[a] + 1, qb = pos[b] < k ? pos[b] : pos[b] + 1, qx = k;
                        int u[3] = {a, b, X}, q[3] = {qa, qb, qx};
                        for (int s = 0; s < 3; s++) for (int t = s + 1; t < 3; t++) if (u[t] < u[s]) { int z = u[s]; u[s] = u[t]; u[t] = z; z = q[s]; q[s] = q[t]; q[t] = z; }
                        int rk[3]; for (int s = 0; s < 3; s++) rk[s] = (q[(s + 1) % 3] < q[s]) + (q[(s + 2) % 3] < q[s]);
                        int code = cond[tidx(u[0], u[1], u[2])]; if (code < 9 && !allowed_code(code, rk)) ok = 0; }
                    inc += ok; } }
            printf("current count %ld\n", inc);
        }
        int r = solve(inc, argc > 8 ? argv[8] : NULL); (void)keep; return r ? 0 : 3;
    }
    if (!strcmp(argv[1], "ext")) {
        int M = atoi(argv[2]); int NTm = (int)binom(M, 3); unsigned char *old = loadnpy(argv[3], NTm); set_opts(argv[4]); TCAP = atof(argv[5]);
        long inc = atol(argv[6]);
        N = M + 1; NT = (int)binom(N, 3); cond = malloc(NT); memset(cond, 9, NT); X = N - 1;
        for (int t = 0; t < NTm; t++) cond[t] = old[t]; /* colex: triples on 0..M-1 come first, same indices */
        int r = solve(inc, argc > 7 ? argv[7] : NULL); return r ? 0 : 3;
    }
    return 1;
}
