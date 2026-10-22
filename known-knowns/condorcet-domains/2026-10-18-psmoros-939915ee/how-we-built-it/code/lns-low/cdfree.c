/* cdfree.c -- exact re-optimisation of all triples meeting a small set S of alternatives (lens lns-low).
 *
 * Generalises cdstar.c (|S| = 1) to |S| = 1, 2, 3.  Fix the conditions on every triple avoiding S; the full domain
 * is the set of orders pi of the sub-domain on [n]\S (all orders obeying the fixed triples) with the members of S
 * inserted at any positions, such that every free triple (meeting S) obeys its chosen condition.  Each such order
 * is an "item"; the free triples are the variables; each (variable, option) allows a subset of items.  Maximise the
 * number of items allowed by all variables: exact DFS branch and bound on bitsets
 *   bound = min over undecided variables of max over options of |alive & allowed|, fail-first branching,
 *   dominance (an option whose surviving set is contained in another's is skipped; equal sets keep one).
 * Modes:
 *   cdfree solve N in.npy S OPTS SECS [INCUMBENT|-1] [out.npy]      S = "x" or "x,y" or "x,y,z" (0-based)
 *   cdfree lns N in.npy K OPTS SECS_PER TOTAL SEED out.npy [NEUTRAL]
 *       iterate over all K-sets in random order, solve each exactly (cap SECS_PER), accept strict improvements;
 *       stops after a full pass without improvement (exact K-set local optimum, if no solve timed out) or TOTAL s.
 *       NEUTRAL = 1: when a solve finds a different assignment of equal size, take it (plateau move).
 * OPTS: pp6 | all9.  Encoding as lsearch.c (colex index, code 3*s+p, 9 = free).
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
static u64 rs = 0x9E3779B97F4A7C15ULL;
static inline u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

static int N, NT; static unsigned char *cond; static int TM[3000][3];

static unsigned char *loadnpy(const char *path, int nt) {
    FILE *f = fopen(path, "rb"); if (!f) { perror(path); exit(1); }
    unsigned char hdr[10]; if (fread(hdr, 1, 10, f) != 10) exit(2);
    int hl = hdr[8] | (hdr[9] << 8); fseek(f, 10 + hl, SEEK_SET);
    unsigned char *c = malloc(nt); if ((int)fread(c, 1, nt, f) != nt) { fprintf(stderr, "short file %s\n", path); exit(3); } fclose(f); return c;
}
static void savenpy(const char *path, unsigned char *c, int nt) {
    char tmp[1024]; snprintf(tmp, sizeof tmp, "%s.tmp", path);
    FILE *f = fopen(tmp, "wb"); char h[128]; int l = snprintf(h, sizeof h, "{'descr': '|u1', 'fortran_order': False, 'shape': (%d,), }", nt);
    int tot = 10 + l + 1; int pad = (64 - tot % 64) % 64; fwrite("\x93NUMPY\x01\x00", 1, 8, f);
    int hl = l + pad + 1; unsigned char b[2] = {(unsigned char)(hl & 255), (unsigned char)(hl >> 8)}; fwrite(b, 1, 2, f);
    fwrite(h, 1, l, f); for (int i = 0; i < pad; i++) fputc(' ', f); fputc('\n', f); fwrite(c, 1, nt, f); fclose(f); rename(tmp, path);
}
static inline int allowed_code(int code, const int rk[3]) { return rk[code / 3] != code % 3; }

/* ---- sub-domain enumeration (orders of [n]\S obeying all triples avoiding S) ---- */
static int INS[MAXN]; static int ALT[MAXN], NA;
static int *ORD; static long NORD, CAPORD; static int curo[MAXN];
static int okplace(int depth, int e) {
    for (int i = 0; i < depth; i++) for (int j = i + 1; j < depth; j++) {
        int u = curo[i], v = curo[j]; int a = u, b = v, c = e, z;
        if (a > b) { z = a; a = b; b = z; } if (b > c) { z = b; b = c; c = z; } if (a > b) { z = a; a = b; b = z; }
        int code = cond[tidx(a, b, c)]; if (code >= 9) continue;
        int tri[3] = {a, b, c}, rk[3];
        for (int r = 0; r < 3; r++) { int w = tri[r]; rk[r] = (w == u) ? 0 : (w == v ? 1 : 2); }
        if (!allowed_code(code, rk)) return 0;
    }
    return 1;
}
static void edfs(int depth, unsigned used) {
    if (depth == NA) {
        if (NORD >= CAPORD) { CAPORD = CAPORD ? 2 * CAPORD : 4096; ORD = realloc(ORD, sizeof(int) * CAPORD * NA); }
        memcpy(ORD + NORD * NA, curo, sizeof(int) * NA); NORD++; return;
    }
    for (int i = 0; i < NA; i++) { int e = ALT[i]; if (used >> e & 1) continue; if (!okplace(depth, e)) continue; curo[depth] = e; edfs(depth + 1, used | (1u << e)); }
}

/* ---- B&B ---- */
static int OPTS[9], NOPT;
static int NV; static int VT[1200];
static long NITEM; static long W;
static u64 *ALW;
static double TCAP, T0; static long NODES; static int TIMEOUT;
static long BEST; static unsigned char BESTOPT[1200], CUROPT[1200]; static int decided[1200]; static int FOUND;
static u64 *STK;
static inline long pc(const u64 *a, long w) { long s = 0; for (long i = 0; i < w; i++) s += __builtin_popcountll(a[i]); return s; }
static inline long pcand(const u64 *a, const u64 *b, long w) { long s = 0; for (long i = 0; i < w; i++) s += __builtin_popcountll(a[i] & b[i]); return s; }
static long *CNT; /* scratch NV*NOPT */
static int RANDTIE = 0;
static void dfs(int depth, const u64 *alive) {
    NODES++;
    if ((NODES & 255) == 0 && now() - T0 > TCAP) TIMEOUT = 1;
    if (TIMEOUT) return;
    long acnt = pc(alive, W);
    if (acnt <= BEST) return;
    if (depth == NV) { BEST = acnt; memcpy(BESTOPT, CUROPT, NV); FOUND = 1; return; }
    int bp = -1; long bmax = 1L << 60;
    for (int p = 0; p < NV; p++) if (!decided[p]) {
        long mx = 0;
        for (int o = 0; o < NOPT; o++) { long c = pcand(alive, ALW + ((long)p * NOPT + o) * W, W); if (c > mx) mx = c; }
        if (mx <= BEST) return;
        if (mx < bmax) { bmax = mx; bp = p; }
    }
    long cnt[9];
    for (int o = 0; o < NOPT; o++) cnt[o] = pcand(alive, ALW + ((long)bp * NOPT + o) * W, W);
    int keepo[9], nk = 0;
    for (int o = 0; o < NOPT; o++) {
        if (cnt[o] <= BEST) continue;
        int dom = 0;
        for (int o2 = 0; o2 < NOPT && !dom; o2++) {
            if (o2 == o || cnt[o2] < cnt[o]) continue;
            if (cnt[o2] == cnt[o] && o2 > o) continue;
            const u64 *A = ALW + ((long)bp * NOPT + o) * W, *B = ALW + ((long)bp * NOPT + o2) * W; int sub = 1;
            for (long i = 0; i < W; i++) if (alive[i] & A[i] & ~B[i]) { sub = 0; break; }
            if (sub) dom = 1;
        }
        if (!dom) keepo[nk++] = o;
    }
    if (RANDTIE) for (int a = nk - 1; a > 0; a--) { int j = (int)(rnd() % (a + 1)); int z = keepo[a]; keepo[a] = keepo[j]; keepo[j] = z; }
    for (int a = 0; a < nk; a++) for (int b = a + 1; b < nk; b++) if (cnt[keepo[b]] > cnt[keepo[a]]) { int z = keepo[a]; keepo[a] = keepo[b]; keepo[b] = z; }
    decided[bp] = 1;
    u64 *nxt = STK + (long)(depth + 1) * W;
    for (int a = 0; a < nk; a++) {
        int o = keepo[a]; if (cnt[o] <= BEST) break;
        const u64 *A = ALW + ((long)bp * NOPT + o) * W;
        for (long i = 0; i < W; i++) nxt[i] = alive[i] & A[i];
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

/* build items for set S (size ks); returns current count (items obeying current conditions on free triples) */
static int PMASK_ON = 0; static int PART[MAXN]; /* if PMASK_ON (|S| = 1 only): free only triples {x,a,b} with a or b in PART */
static u64 *ROOT; static int NVALL;
static long build(const int *S, int ks) {
    memset(INS, 0, sizeof INS); for (int i = 0; i < ks; i++) INS[S[i]] = 1;
    NA = 0; for (int i = 0; i < N; i++) if (!INS[i]) ALT[NA++] = i;
    unsigned char *keep = malloc(NT); memcpy(keep, cond, NT);
    NV = 0; static int FIXT[1200]; int NF = 0;
    for (int t = 0; t < NT; t++) if (INS[TM[t][0]] || INS[TM[t][1]] || INS[TM[t][2]]) {
        int fr = 1; if (PMASK_ON) { fr = 0; for (int r = 0; r < 3; r++) if (!INS[TM[t][r]] && PART[TM[t][r]]) fr = 1; }
        if (fr) VT[NV++] = t; else FIXT[NF++] = t; cond[t] = 9; }
    NORD = 0; edfs(0, 0);
    /* insertion tuples: ordered distinct positions for S members */
    int ntup = 0; static int TUP[20000][3];
    if (ks == 1) for (int a = 0; a < N; a++) { TUP[ntup][0] = a; ntup++; }
    else if (ks == 2) { for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) if (a != b) { TUP[ntup][0] = a; TUP[ntup][1] = b; ntup++; } }
    else for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++) if (a != b && a != c && b != c) { TUP[ntup][0] = a; TUP[ntup][1] = b; TUP[ntup][2] = c; ntup++; }
    NITEM = NORD * ntup; W = (NITEM + 63) / 64;
    free(ALW); ALW = calloc((size_t)NV * NOPT * W, sizeof(u64));
    long curcount = 0;
    int pos[MAXN];
    free(ROOT); ROOT = calloc(W, sizeof(u64));
    for (long r = 0; r < NORD; r++) {
        int *pi = ORD + r * NA;
        for (int tu = 0; tu < ntup; tu++) {
            long it = r * ntup + tu;
            int occ[MAXN]; for (int q = 0; q < N; q++) occ[q] = -1;
            for (int i = 0; i < ks; i++) occ[TUP[tu][i]] = S[i];
            int k = 0; for (int q = 0; q < N; q++) if (occ[q] < 0) occ[q] = pi[k++];
            for (int q = 0; q < N; q++) pos[occ[q]] = q;
            int okc = 1;
            for (int v = 0; v < NV; v++) {
                int t = VT[v]; int q0 = pos[TM[t][0]], q1 = pos[TM[t][1]], q2 = pos[TM[t][2]];
                int rk[3] = {(q1 < q0) + (q2 < q0), (q0 < q1) + (q2 < q1), (q0 < q2) + (q1 < q2)};
                for (int o = 0; o < NOPT; o++) if (allowed_code(OPTS[o], rk)) ALW[((long)v * NOPT + o) * W + (it >> 6)] |= 1ULL << (it & 63);
                if (keep[t] < 9 && !allowed_code(keep[t], rk)) okc = 0;
            }
            int okf = 1;
            for (int f = 0; f < NF && okf; f++) {
                int t = FIXT[f]; int q0 = pos[TM[t][0]], q1 = pos[TM[t][1]], q2 = pos[TM[t][2]];
                int rk[3] = {(q1 < q0) + (q2 < q0), (q0 < q1) + (q2 < q1), (q0 < q2) + (q1 < q2)};
                if (keep[t] < 9 && !allowed_code(keep[t], rk)) okf = 0;
            }
            if (okf) ROOT[it >> 6] |= 1ULL << (it & 63);
            curcount += okc && okf;
        }
    }
    memcpy(cond, keep, NT); free(keep);
    return curcount;
}
static long run_bb(long incumbent, double cap) {
    free(STK); STK = malloc(sizeof(u64) * W * (NV + 2));
    for (long i = 0; i < W; i++) STK[i] = ROOT[i];
    BEST = incumbent; NODES = 0; TIMEOUT = 0; FOUND = 0; memset(decided, 0, sizeof decided); T0 = now(); TCAP = cap;
    dfs(0, STK);
    return BEST;
}
static void apply_best(void) { for (int v = 0; v < NV; v++) cond[VT[v]] = (unsigned char)OPTS[BESTOPT[v]]; }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "see header\n"); return 1; }
    N = atoi(argv[2]); NT = (int)binom(N, 3); cond = loadnpy(argv[3], NT);
    for (int c = 2; c < N; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) { int t = tidx(a, b, c); TM[t][0] = a; TM[t][1] = b; TM[t][2] = c; }
    if (!strcmp(argv[1], "solve")) {
        int S[3], ks = 0; const char *p = argv[4]; while (*p && ks < 3) { S[ks++] = atoi(p); while (*p && *p != ',') p++; if (*p) p++; }
        set_opts(argv[5]); double cap = atof(argv[6]); long inc = argc > 7 ? atol(argv[7]) : -1;
        long cur = build(S, ks); if (inc < 0) inc = cur;
        printf("solve n %d S", N); for (int i = 0; i < ks; i++) printf(" %d", S[i]);
        printf(" subdomain %ld items %ld vars %d opts %d current %ld incumbent %ld\n", NORD, NITEM, NV, NOPT, cur, inc); fflush(stdout);
        long b = run_bb(inc, cap);
        printf("result best %ld improved %s nodes %ld time %.1fs %s\n", b, FOUND ? "YES" : "no", NODES, now() - T0, TIMEOUT ? "TIMEOUT (not exhaustive)" : "EXHAUSTIVE");
        if (FOUND && argc > 8) { apply_best(); savenpy(argv[8], cond, NT); printf("wrote %s\n", argv[8]); }
        return 0;
    }


    if (!strcmp(argv[1], "plns")) {
        /* plns N in.npy P OPTS PER TOTAL SEED out.npy : partner-star LNS. Random x and random partner set Q of size P:
           free = triples {x,a,b} with a or b in Q (P(n-2) - C(P,2) triples), solved exactly (cap PER); strict
           improvements accepted; one log line per solve. */
        int P = atoi(argv[4]); set_opts(argv[5]); double per = atof(argv[6]), total = atof(argv[7]); rs ^= (u64)atoll(argv[8]) * 0x2545F4914F6CDD1DULL; rnd();
        const char *outp = argv[9]; PMASK_ON = 1;
        double tstart = now(); long cur = -1, solves = 0, exh = 0, sinceimp = 0;
        while (now() - tstart < total) {
            int x = (int)(rnd() % N); memset(PART, 0, sizeof PART); int c = 0;
            while (c < P) { int a = (int)(rnd() % N); if (a != x && !PART[a]) { PART[a] = 1; c++; } }
            int S[1] = {x}; long c0 = build(S, 1);
            if (cur < 0) { cur = c0; printf("plns n %d P %d start %ld\n", N, P, cur); fflush(stdout); }
            if (c0 != cur) printf("WARNING count mismatch %ld vs %ld\n", c0, cur);
            long b = run_bb(cur, per); solves++; if (!TIMEOUT) exh++;
            if (FOUND && b > cur) { apply_best(); printf("solve %ld x %d improve %ld -> %ld vars %d nodes %ld %.1fs t %.0fs\n", solves, x, cur, b, NV, NODES, now() - T0, now() - tstart); cur = b; savenpy(outp, cond, NT); sinceimp = 0; fflush(stdout); }
            else sinceimp++;
            if (solves % 25 == 0) { printf("solves %ld exhaustive %ld cur %ld since-improve %ld last-nodes %ld last-time %.1fs t %.0fs\n", solves, exh, cur, sinceimp, NODES, now() - T0, now() - tstart); fflush(stdout); }
        }
        savenpy(outp, cond, NT); printf("final plns %ld solves %ld exhaustive %ld t %.0fs\n", cur, solves, exh, now() - tstart); return 0;
    }
    if (!strcmp(argv[1], "ils")) {
        /* ils N in.npy OPTS PER TOTAL SEED out.npy KICKSET : iterated local search. kick = random options on all
           triples meeting a random KICKSET-set in >= 2 points; descent = exact star solves (K = 1) in random order
           until a full pass gives no strict improvement; accept the result if >= best (plateau drift). */
        set_opts(argv[4]); double per = atof(argv[5]), total = atof(argv[6]); rs ^= (u64)atoll(argv[7]) * 0x2545F4914F6CDD1DULL; rnd();
        const char *outp = argv[8]; int ks = atoi(argv[9]);
        unsigned char *best = malloc(NT); memcpy(best, cond, NT);
        int S1[1]; S1[0] = 0; long bestv = build(S1, 1); double tstart = now(); long it = 0, acc = 0;
        printf("ils n %d start %ld opts %s kickset %d\n", N, bestv, argv[4], ks); fflush(stdout);
        while (now() - tstart < total) {
            memcpy(cond, best, NT);
            int in[MAXN]; memset(in, 0, sizeof in); int c = 0; while (c < ks) { int a = (int)(rnd() % N); if (!in[a]) { in[a] = 1; c++; } }
            for (int t = 0; t < NT; t++) if (in[TM[t][0]] + in[TM[t][1]] + in[TM[t][2]] >= 2) cond[t] = (unsigned char)OPTS[rnd() % NOPT];
            long cur = -1; int imp = 1, passes = 0;
            while (imp && now() - tstart < total) {
                imp = 0; int ord[MAXN]; for (int i = 0; i < N; i++) ord[i] = i;
                for (int i = N - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); int z = ord[i]; ord[i] = ord[j]; ord[j] = z; }
                for (int i = 0; i < N; i++) { int S[1] = {ord[i]}; long c0 = build(S, 1); cur = c0; long b = run_bb(cur, per); if (FOUND && b > cur) { apply_best(); cur = b; imp = 1; } }
                passes++;
            }
            it++;
            if (cur > bestv) { bestv = cur; memcpy(best, cond, NT); savenpy(outp, best, NT); printf("it %ld NEW BEST %ld (passes %d) t %.0fs\n", it, bestv, passes, now() - tstart); fflush(stdout); }
            else if (cur == bestv) { acc++; memcpy(best, cond, NT); }
            if (it % 10 == 0) { printf("it %ld last %ld best %ld plateau-accepts %ld t %.0fs\n", it, cur, bestv, acc, now() - tstart); fflush(stdout); }
        }
        savenpy(outp, best, NT); printf("final ils best %ld iterations %ld t %.0fs\n", bestv, it, now() - tstart); return 0;
    }
    if (!strcmp(argv[1], "lns")) {
        int K = atoi(argv[4]); set_opts(argv[5]); double per = atof(argv[6]), total = atof(argv[7]); rs ^= (u64)atoll(argv[8]) * 0x2545F4914F6CDD1DULL; rnd();
        const char *outp = argv[9]; int neutral = argc > 10 ? atoi(argv[10]) : 0; RANDTIE = neutral;
        static int SETS[3000][3]; int ns = 0;
        if (K == 1) for (int a = 0; a < N; a++) { SETS[ns][0] = a; ns++; }
        else if (K == 2) for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) { SETS[ns][0] = a; SETS[ns][1] = b; ns++; }
        else for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) { SETS[ns][0] = a; SETS[ns][1] = b; SETS[ns][2] = c; ns++; }
        double tstart = now(); long cur = -1; int pass = 0;
        while (now() - tstart < total) {
            for (int i = ns - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); for (int q = 0; q < 3; q++) { int z = SETS[i][q]; SETS[i][q] = SETS[j][q]; SETS[j][q] = z; } }
            int imp = 0, tout = 0;
            for (int si = 0; si < ns && now() - tstart < total; si++) {
                long c0 = build(SETS[si], K); if (cur < 0) { cur = c0; printf("lns n %d K %d start %ld\n", N, K, cur); fflush(stdout); }
                if (c0 != cur) printf("WARNING count mismatch %ld vs %ld\n", c0, cur);
                long b = run_bb(neutral ? cur - 1 : cur, per);
                if (TIMEOUT) tout++;
                if (FOUND && b > cur) {
                    apply_best(); printf("pass %d set %d %d %d improve %ld -> %ld (nodes %ld, %.1fs, items %ld) t %.0fs\n", pass, SETS[si][0], K > 1 ? SETS[si][1] : -1, K > 2 ? SETS[si][2] : -1, cur, b, NODES, now() - T0, NITEM, now() - tstart);
                    cur = b; imp++; savenpy(outp, cond, NT); fflush(stdout);
                } else if (FOUND && neutral && b == cur) { apply_best(); }
                printf("  solve set %d %d nodes %ld %.1fs %s cur %ld\n", SETS[si][0], K > 1 ? SETS[si][1] : -1, NODES, now() - T0, TIMEOUT ? "timeout" : "exhaustive", cur); fflush(stdout);
            }
            printf("pass %d done improvements %d timeouts %d/%d cur %ld t %.0fs\n", pass, imp, tout, ns, cur, now() - tstart); fflush(stdout);
            pass++;
            if (!imp && !neutral) { printf("LOCAL OPTIMUM for all %d-sets%s\n", K, tout ? " (some solves timed out)" : " (every solve exhaustive)"); break; }
        }
        savenpy(outp, cond, NT); printf("final %ld t %.0fs\n", cur, now() - tstart); return 0;
    }
    return 1;
}
