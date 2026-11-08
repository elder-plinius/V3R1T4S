/* check_e.c -- block-sweep exact checker for C1, C2, C3 of PROOF.md section 5.
 * usage: check_e N K m counts states V [perturb|drop]
 * Streams the certificate window by window with pread(); memory is O(largest block).
 * Successors come from the increment rule (PROOF.md s.2), never the max rule.
 * ROW successors: same window block, found by binary search.
 * SHIFT successors: blocks (b>>1) and (~(b>>1))&mask, found by a monotone two-pointer walk
 *   (h>>1 is non-decreasing in h, so no per-state search is needed).
 * Input checks (2026-11-08): N, K and m are parsed strictly as in check_d.c (whole decimal integers,
 * no empty or trailing text, m within +-2^60), and a window count above 2^N is rejected, since h is
 * strictly ascending and below 2^N within a window (this also keeps every block count small).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

typedef long long ll;
typedef __int128 i128;

static int N; static ll K, M;
static int fd_s, fd_v;
static uint32_t *counts; static ll NB;            /* number of blocks = 2^(N-1) */
static ll *off;                                    /* prefix sums, NB+1 entries */
static ll TOTAL;
static unsigned char *rawS, *rawV; static ll maxcnt;

/* modification applied while loading: 0 none, 1 perturb (V+1 at global idx), 2 drop (global idx) */
static int modmode = 0; static ll modidx = -1;

typedef struct { ll id; int n; uint32_t *h; uint8_t *pol; int32_t *V; } Blk;

static void rejectfatal(const char *fmt, ...);
#include <stdarg.h>
static void rejectfatal(const char *fmt, ...) {
    va_list ap; va_start(ap, fmt);
    printf("REJECT "); vprintf(fmt, ap); printf("\n"); va_end(ap); fflush(stdout); exit(1);
}

static ll parse_ll(const char *s, const char *what) {
    char *end; errno = 0;
    long long v = strtoll(s, &end, 10);
    if (errno || *s == 0 || *end != 0) rejectfatal("bad %s: %s", what, s);
    return v;
}

static void rdfull(int fd, unsigned char *buf, ll len, ll pos) {
    ll got = 0;
    while (got < len) {
        ssize_t r = pread(fd, buf + got, (size_t)(len - got), (off_t)(pos + got));
        if (r < 0) { if (errno == EINTR) continue; rejectfatal("read error: %s", strerror(errno)); }
        if (r == 0) rejectfatal("short read at %lld", pos + got);
        got += r;
    }
}

static void load(Blk *B, ll id) {
    int n = (int)counts[id];
    if (n) { rdfull(fd_s, rawS, 3LL * n, 3LL * off[id]); rdfull(fd_v, rawV, 4LL * n, 4LL * off[id]); }
    uint32_t prev = 0;
    for (int i = 0; i < n; i++) {
        uint32_t e = (uint32_t)rawS[3*i] | ((uint32_t)rawS[3*i+1] << 8) | ((uint32_t)rawS[3*i+2] << 16);
        uint32_t h = e & 0x7FFFFFu;
        if (h >> N) rejectfatal("block %lld state %d: h=%u has bits above N=%d", id, i, h, N);
        if (i > 0 && h <= prev) rejectfatal("block %lld: h not strictly ascending at state %d (%u after %u)", id, i, h, prev);
        prev = h;
        B->h[i] = h; B->pol[i] = (uint8_t)(e >> 23);
        uint32_t u = (uint32_t)rawV[4*i] | ((uint32_t)rawV[4*i+1] << 8) | ((uint32_t)rawV[4*i+2] << 16) | ((uint32_t)rawV[4*i+3] << 24);
        B->V[i] = (int32_t)(u >= 0x80000000u ? (ll)u - 4294967296LL : (ll)u);
    }
    B->n = n; B->id = id;
    if (modmode && modidx >= off[id] && modidx < off[id] + n) {
        int j = (int)(modidx - off[id]);
        if (modmode == 1) B->V[j] += 1;       /* int32 wrap impossible in tests; V stays well below 2^31 */
        else {
            for (int i = j; i + 1 < n; i++) { B->h[i] = B->h[i+1]; B->pol[i] = B->pol[i+1]; B->V[i] = B->V[i+1]; }
            B->n = n - 1;
        }
    }
}

/* Row of PROOF.md s.2: h'_p = x_p - v_p, v_{p+1} = x_p - h_p, x_p = h_p|v_p|m_p, v_0 = 0
 * (PROOF_v2.md Lemma A writes x_p as z_p and m_p as mu_p) */
static uint32_t row_inc(uint32_t h, uint32_t b, int a) {
    uint32_t hn = 0; int v = 0;
    for (int p = 0; p < N; p++) {
        int hp = (h >> p) & 1, bp = (b >> p) & 1;
        int mp = (bp == a);
        int xp = hp | v | mp;
        int hq = xp - v, vq = xp - hp;
        if (hq < 0 || hq > 1 || vq < 0 || vq > 1) rejectfatal("increment rule left {0,1} (internal)");
        hn |= (uint32_t)hq << p; v = vq;
    }
    return hn;
}

static int bsearch_h(const Blk *B, uint32_t t) {
    int lo = 0, hi = B->n - 1;
    while (lo <= hi) { int mid = (lo + hi) >> 1;
        if (B->h[mid] == t) return mid;
        if (B->h[mid] < t) lo = mid + 1; else hi = mid - 1; }
    return -1;
}

typedef struct { int ok; ll minE; ll minIdx; i128 sumE; ll cntE; ll c1, c2, c3; char first[300]; } Res;

static void note(Res *R, const char *s) { if (!R->first[0]) { strncpy(R->first, s, sizeof R->first - 1); } }

static Res sweep(void) {
    Res R; memset(&R, 0, sizeof R); R.minE = 0x7fffffffffffffffLL; R.minIdx = -1;
    Blk cur, t0, t1; Blk *all[3] = {&cur, &t0, &t1};
    for (int k = 0; k < 3; k++) { all[k]->h = malloc(sizeof(uint32_t) * (maxcnt + 1)); all[k]->pol = malloc(maxcnt + 1);
        all[k]->V = malloc(sizeof(int32_t) * (maxcnt + 1)); all[k]->id = -1; all[k]->n = 0;
        if (!all[k]->h || !all[k]->pol || !all[k]->V) rejectfatal("out of memory"); }
    ll mask1 = NB - 1;                                   /* low N-1 bits */
    char msg[300];
    for (ll b = 0; b < NB; b++) {
        load(&cur, b);
        if (cur.n == 0 || cur.h[0] != 0) { R.c1++; snprintf(msg, sizeof msg, "C1: no state (h=0,b=%lld)", b); note(&R, msg); }
        ll tb0 = b >> 1, tb1 = (~(b >> 1)) & mask1;      /* c=0 block ; c=1 block after complement */
        load(&t0, tb0); load(&t1, tb1);
        int p0 = 0, p1 = 0;
        for (int i = 0; i < cur.n; i++) {
            uint32_t h = cur.h[i]; ll Vs = cur.V[i]; ll sumV = -1; ll E; int okc = 1;
            ll gidx = off[b] + i;
            if (cur.pol[i]) {                             /* ROW */
                uint32_t n0 = row_inc(h, (uint32_t)b, 0), n1 = row_inc(h, (uint32_t)b, 1);
                int j0 = bsearch_h(&cur, n0), j1 = bsearch_h(&cur, n1);
                if (j0 < 0 || j1 < 0) { okc = 0; R.c2++; snprintf(msg, sizeof msg, "C2: ROW successor missing from b=%lld h=%u (a=%d)", b, h, j0 < 0 ? 0 : 1); note(&R, msg); }
                else sumV = (ll)cur.V[j0] + cur.V[j1];
                E = sumV - 2 * Vs;
            } else {                                      /* SHIFT, reward r = h_0 */
                uint32_t nh = h >> 1; ll r = h & 1;
                while (p0 < t0.n && t0.h[p0] < nh) p0++;
                while (p1 < t1.n && t1.h[p1] < nh) p1++;
                int f0 = (p0 < t0.n && t0.h[p0] == nh), f1 = (p1 < t1.n && t1.h[p1] == nh);
                if (!f0 || !f1) { okc = 0; R.c2++; snprintf(msg, sizeof msg, "C2: SHIFT successor missing from b=%lld h=%u (c=%d)", b, h, f0 ? 1 : 0); note(&R, msg); }
                else sumV = (ll)t0.V[p0] + t1.V[p1];
                E = sumV + 2 * K * r - 2 * Vs;
            }
            if (!okc) continue;
            R.sumE += E; R.cntE++;
            if (E < R.minE) { R.minE = E; R.minIdx = gidx; }
            if (E < M) { R.c3++; snprintf(msg, sizeof msg, "C3: b=%lld h=%u pol=%s E=%lld < m=%lld", b, h, cur.pol[i] ? "ROW" : "SHIFT", E, M); note(&R, msg); }
        }
    }
    for (int k = 0; k < 3; k++) { free(all[k]->h); free(all[k]->pol); free(all[k]->V); }
    R.ok = (R.c1 == 0 && R.c2 == 0 && R.c3 == 0);
    return R;
}

static void print_i128(i128 v) {
    char buf[64]; int n = 0; int neg = v < 0; if (neg) v = -v;
    if (v == 0) buf[n++] = '0';
    while (v > 0) { buf[n++] = '0' + (int)(v % 10); v /= 10; }
    if (neg) putchar('-');
    while (n) putchar(buf[--n]);
}

static void report(const char *tag, Res *R, ll nstates) {
    printf("[%s] N=%d states=%lld statesWithE=%lld minE=%lld sumE=", tag, N, nstates, R->cntE, R->minE);
    print_i128(R->sumE);
    if (R->sumE > (i128)0x7fffffffffffffffLL || R->sumE < -(i128)0x7fffffffffffffffLL) printf(" (EXCEEDS int64)");
    if (R->cntE > 0) {
        i128 q = R->sumE / R->cntE; i128 rem = R->sumE - q * R->cntE;
        printf(" meanE="); print_i128(q); printf(".%06lld", (ll)((rem * 1000000) / R->cntE));
    }
    printf(" violations C1=%lld C2=%lld C3=%lld\n", R->c1, R->c2, R->c3);
    if (R->first[0]) printf("[%s] first problem: %s\n", tag, R->first);
    fflush(stdout);
}

int main(int argc, char **argv) {
    if (argc < 7 || argc > 8) { fprintf(stderr, "usage: check_e N K m counts states V [perturb|drop]\n"); return 2; }
    ll Narg = parse_ll(argv[1], "N");
    if (Narg < 1 || Narg > 18) rejectfatal("N must be an integer in 1..18");
    N = (int)Narg;
    K = parse_ll(argv[2], "K"); if (K <= 0 || K > (1LL << 40)) rejectfatal("bad K");
    M = parse_ll(argv[3], "m"); if (M < -(1LL << 60) || M > (1LL << 60)) rejectfatal("m out of range");
    int mode = 0;
    if (argc == 8) { if (!strcmp(argv[7], "perturb")) mode = 1; else if (!strcmp(argv[7], "drop")) mode = 2; else { fprintf(stderr, "mode must be perturb or drop\n"); return 2; } }
    NB = 1LL << (N - 1);
    FILE *fc = fopen(argv[4], "rb"); if (!fc) rejectfatal("cannot open counts");
    fseek(fc, 0, SEEK_END); ll csz = ftell(fc); fseek(fc, 0, SEEK_SET);
    if (csz != 4 * NB) rejectfatal("counts file size %lld, expected %lld", csz, 4 * NB);
    unsigned char *cb = malloc(csz); if (fread(cb, 1, csz, fc) != (size_t)csz) rejectfatal("counts read"); fclose(fc);
    counts = malloc(sizeof(uint32_t) * NB); off = malloc(sizeof(ll) * (NB + 1));
    off[0] = 0; maxcnt = 0;
    for (ll b = 0; b < NB; b++) {
        counts[b] = (uint32_t)cb[4*b] | ((uint32_t)cb[4*b+1] << 8) | ((uint32_t)cb[4*b+2] << 16) | ((uint32_t)cb[4*b+3] << 24);
        if ((ll)counts[b] > (1LL << N)) rejectfatal("count %u above 2^N at b=%lld", counts[b], b);
        off[b+1] = off[b] + counts[b]; if (counts[b] > maxcnt) maxcnt = counts[b];
    }
    free(cb); TOTAL = off[NB];
    fd_s = open(argv[5], O_RDONLY); fd_v = open(argv[6], O_RDONLY);
    if (fd_s < 0 || fd_v < 0) rejectfatal("cannot open states/V");
    struct stat st1, st2; fstat(fd_s, &st1); fstat(fd_v, &st2);
    if ((ll)st1.st_size != 3 * TOTAL) rejectfatal("states file size %lld != 3*total(%lld)", (ll)st1.st_size, TOTAL);
    if ((ll)st2.st_size != 4 * TOTAL) rejectfatal("V file size %lld != 4*total(%lld)", (ll)st2.st_size, TOTAL);
    rawS = malloc(3 * (maxcnt + 1)); rawV = malloc(4 * (maxcnt + 1));
    if (!rawS || !rawV) rejectfatal("out of memory");
    printf("N=%d K=%lld m=%lld blocks=%lld states=%lld maxblock=%lld (sizes consistent)\n", N, K, M, NB, TOTAL, maxcnt);
    fflush(stdout);

    Res R = sweep();
    report("base", &R, TOTAL);
    if (!R.ok) { printf("REJECT C1=%lld C2=%lld C3=%lld\n", R.c1, R.c2, R.c3); return 1; }
    if (mode == 0) { printf("ACCEPT m=%lld K=%lld\n", M, K); return 0; }

    ll mid = TOTAL / 2;
    if (mode == 1) modidx = R.minIdx; else modidx = mid;
    modmode = mode;
    printf("%s test: global state index %lld%s\n", mode == 1 ? "perturb" : "drop", modidx, mode == 1 ? " (a state attaining min E): V += 1" : " (middle state) removed");
    fflush(stdout);
    Res R2 = sweep();
    report(mode == 1 ? "perturbed" : "dropped", &R2, TOTAL - (mode == 2));
    if (!R2.ok) { printf("REJECT (%s detected) C1=%lld C2=%lld C3=%lld\n", mode == 1 ? "perturb" : "drop", R2.c1, R2.c2, R2.c3); return 1; }
    printf("WARNING: modification NOT detected\n");
    printf("ACCEPT m=%lld K=%lld\n", M, K);
    return 0;
}
