/* check_d.c - independent exact checker for the adaptive-strip certificate.
 * Build: cc -O2 -o check_d check_d.c
 * Usage: check_d N K m counts states V [perturb|drop]
 *   (N is given first for the user's convenience but is also derived from the
 *    counts file size and must agree; see below.)
 *
 * Tests (PROOF.md section 5): C1, C2, C3 for every state, exact int64 arithmetic.
 * Successors are computed from the max-rule definition with explicit integer
 * frontier values F_0..F_N (no bit tricks).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

typedef int64_t i64;
typedef uint64_t u64;

static int N;
static u64 NB;            /* number of windows = 2^(N-1) */
static u64 MASKN;         /* (1<<N)-1 */
static const unsigned char *ST, *VV;
static uint32_t *cnt;
static u64 *off;          /* off[b] = first state index of window b; off[NB]=total */
static u64 total;

static i64 Kc, mc;
static u64 STsz, VVsz;   /* mapped sizes */
static const char *STpath, *VVpath;
static const void *map_file(const char *path, u64 *size);
/* macOS ignores madvise(DONTNEED) on file maps, so drop resident pages by remapping */
static void remap_all(void) {
    u64 t;
    munmap((void *)ST, STsz); munmap((void *)VV, VVsz);
    ST = map_file(STpath, &t); VV = map_file(VVpath, &t);
}

static const void *map_file(const char *path, u64 *size) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) { printf("cannot open %s: %s\n", path, strerror(errno)); printf("REJECT\n"); exit(1); }
    struct stat sb;
    if (fstat(fd, &sb) != 0) { printf("cannot stat %s\n", path); printf("REJECT\n"); exit(1); }
    *size = (u64)sb.st_size;
    if (sb.st_size == 0) { close(fd); return NULL; }
    void *p = mmap(NULL, (size_t)sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (p == MAP_FAILED) { printf("mmap failed %s\n", path); printf("REJECT\n"); exit(1); }
    close(fd);
    return p;
}

/* state entry i: h and policy */
static inline u64 ent(u64 i) {
    const unsigned char *q = ST + 3 * i;
    return (u64)q[0] | ((u64)q[1] << 8) | ((u64)q[2] << 16);
}
static inline i64 val(u64 i) {
    const unsigned char *q = VV + 4 * i;
    uint32_t u = (uint32_t)q[0] | ((uint32_t)q[1] << 8) | ((uint32_t)q[2] << 16) | ((uint32_t)q[3] << 24);
    return (i64)(int32_t)u;
}

/* look up canonical state (b,h); return index or -1 */
static inline i64 find(u64 b, u64 h) {
    u64 lo = off[b], hi = off[b + 1];   /* [lo,hi) */
    while (lo < hi) {
        u64 mid = lo + (hi - lo) / 2;
        u64 hm = ent(mid) & 0x7FFFFF;
        if (hm == h) return (i64)mid;
        if (hm < h) lo = mid + 1; else hi = mid;
    }
    return -1;
}

static inline u64 canon_b(u64 b) {
    if ((b >> (N - 1)) & 1) b ^= MASKN;
    return b;
}

/* ROW successor with character a: from (h,b). Returns 0 ok, -1 if increment form broken. */
static int succ_row(u64 h, u64 b, int a, u64 *nh, u64 *nb) {
    int F[20], G[20];
    F[0] = 0;
    for (int p = 0; p < N; p++) F[p + 1] = F[p] + (int)((h >> p) & 1);
    G[0] = F[0];
    for (int p = 0; p < N; p++) {
        int mp = (int)((b >> p) & 1) == a ? 1 : 0;
        int t = F[p + 1];
        if (G[p] > t) t = G[p];
        if (F[p] + mp > t) t = F[p] + mp;
        G[p + 1] = t;
    }
    u64 h2 = 0;
    for (int p = 0; p < N; p++) {
        int d = G[p + 1] - G[p];
        if (d != 0 && d != 1) return -1;
        h2 |= (u64)d << p;
    }
    *nh = h2;
    *nb = canon_b(b);
    return 0;
}

/* SHIFT successor reading character c. reward r = F_1 - F_0. */
static int succ_shift(u64 h, u64 b, int c, u64 *nh, u64 *nb, int *r) {
    int F[20], G[20];
    F[0] = 0;
    for (int p = 0; p < N; p++) F[p + 1] = F[p] + (int)((h >> p) & 1);
    *r = F[1] - F[0];
    for (int p = 0; p < N; p++) G[p] = F[p + 1];
    G[N] = F[N];
    u64 h2 = 0;
    for (int p = 0; p < N; p++) {
        int d = G[p + 1] - G[p];
        if (d != 0 && d != 1) return -1;
        h2 |= (u64)d << p;
    }
    /* new window: positions 0..N-2 = old 1..N-1, position N-1 = c */
    u64 b2 = 0;
    for (int p = 0; p < N - 1; p++) b2 |= ((b >> (p + 1)) & 1) << p;
    b2 |= (u64)c << (N - 1);
    *nh = h2;
    *nb = canon_b(b2);
    return 0;
}

typedef struct {
    int ok;            /* verdict */
    i64 minE;
    i64 minIdx;        /* first index attaining minE */
    u64 nmin;          /* count attaining */
    u64 c3fail, c2fail, c1fail, struct_fail;
    u64 nrow, nshift;
} Res;

/* Full pass. drop: index removed (or -1); pert: index whose V is raised by 1 (or -1). */
static Res sweep(i64 drop, i64 pert, int structure) {
    Res R; memset(&R, 0, sizeof R);
    R.minE = INT64_MAX; R.minIdx = -1;
    u64 idx = 0;
    for (u64 b = 0; b < NB; b++) {
        if ((b & 1023) == 1023) remap_all();
        /* C1: (0,b) in S */
        {
            i64 j = find(b, 0);
            if (j < 0 || j == drop) { if (R.c1fail < 5) printf("C1 fail: b=%llu\n", (unsigned long long)b); R.c1fail++; }
        }
        u64 prevh = 0; int first = 1;
        for (u64 k = 0; k < cnt[b]; k++, idx++) {
            u64 e = ent(idx);
            u64 h = e & 0x7FFFFF;
            int rowp = (int)((e >> 23) & 1);
            if (structure) {
                if (h >> N) { if (R.struct_fail < 5) printf("bad h bits at state %llu\n", (unsigned long long)idx); R.struct_fail++; }
                if (!first && h <= prevh) { if (R.struct_fail < 5) printf("order violation at state %llu\n", (unsigned long long)idx); R.struct_fail++; }
            }
            first = 0; prevh = h;
            if ((i64)idx == drop) continue;
            if (rowp) R.nrow++; else R.nshift++;
            i64 vs = val(idx) + ((i64)idx == pert ? 1 : 0);
            i64 vsum = 0; i64 r = 0;
            int bad = 0;
            for (int ch = 0; ch < 2; ch++) {
                u64 nh, nb; int rr = 0;
                int rc;
                if (rowp) rc = succ_row(h, b, ch, &nh, &nb);
                else rc = succ_shift(h, b, ch, &nh, &nb, &rr);
                if (rc != 0) { if (R.c2fail < 5) printf("increment form broken at state %llu\n", (unsigned long long)idx); R.c2fail++; bad = 1; break; }
                r = rr;
                i64 j = find(nb, nh);
                if (j < 0 || j == drop) {
                    if (R.c2fail < 5) printf("C2 fail: state %llu (b=%llu h=%llu) successor missing (b=%llu h=%llu)\n",
                        (unsigned long long)idx, (unsigned long long)b, (unsigned long long)h,
                        (unsigned long long)nb, (unsigned long long)nh);
                    R.c2fail++; bad = 1; break;
                }
                vsum += val((u64)j) + (j == pert ? 1 : 0);
            }
            if (bad) continue;
            i64 E = vsum - 2 * vs + (rowp ? 0 : 2 * Kc * r);
            if (E < R.minE) { R.minE = E; R.minIdx = (i64)idx; R.nmin = 1; }
            else if (E == R.minE) R.nmin++;
            if (E < mc) {
                if (R.c3fail < 5) printf("C3 fail: state %llu (b=%llu h=%llu %s) E=%lld < m=%lld\n",
                    (unsigned long long)idx, (unsigned long long)b, (unsigned long long)h,
                    rowp ? "ROW" : "SHIFT", (long long)E, (long long)mc);
                R.c3fail++;
            }
        }
    }
    R.ok = (R.c1fail == 0 && R.c2fail == 0 && R.c3fail == 0 && R.struct_fail == 0);
    return R;
}

static i64 parse_ll(const char *s, const char *what) {
    char *end; errno = 0;
    long long v = strtoll(s, &end, 10);
    if (errno || *s == 0 || *end != 0) { printf("bad %s: %s\nREJECT\n", what, s); exit(1); }
    return (i64)v;
}

int main(int argc, char **argv) {
    if (argc < 7 || argc > 8) {
        fprintf(stderr, "usage: %s N K m counts states V [perturb|drop]\n", argv[0]);
        return 2;
    }
    int Narg = (int)parse_ll(argv[1], "N");
    Kc = parse_ll(argv[2], "K");
    mc = parse_ll(argv[3], "m");
    const char *mode = argc == 8 ? argv[7] : NULL;
    if (mode && strcmp(mode, "perturb") && strcmp(mode, "drop")) { printf("bad mode\nREJECT\n"); return 2; }
    if (Kc <= 0 || Kc > ((i64)1 << 40)) { printf("K out of range (0,2^40]\nREJECT\n"); return 1; }
    if (mc < -((i64)1 << 60) || mc > ((i64)1 << 60)) { printf("m out of range\nREJECT\n"); return 1; }
    if (Narg < 1 || Narg > 18) { printf("N=%d out of range 1..18\nREJECT\n", Narg); return 1; }
    N = Narg; NB = (u64)1 << (N - 1); MASKN = ((u64)1 << N) - 1;

    u64 csz, ssz, vsz;
    const unsigned char *cb = map_file(argv[4], &csz);
    ST = map_file(argv[5], &ssz);
    VV = map_file(argv[6], &vsz);
    STsz = ssz; VVsz = vsz; STpath = argv[5]; VVpath = argv[6];
    if (csz != 4 * NB) { printf("counts file size %llu != 4*2^(N-1) = %llu\n", (unsigned long long)csz, (unsigned long long)(4 * NB)); printf("REJECT\n"); return 1; }
    cnt = malloc(NB * sizeof(uint32_t));
    off = malloc((NB + 1) * sizeof(u64));
    if (!cnt || !off) { printf("oom\nREJECT\n"); return 1; }
    u64 tot = 0;
    for (u64 b = 0; b < NB; b++) {
        const unsigned char *q = cb + 4 * b;
        cnt[b] = (uint32_t)q[0] | ((uint32_t)q[1] << 8) | ((uint32_t)q[2] << 16) | ((uint32_t)q[3] << 24);
        off[b] = tot; tot += cnt[b];
    }
    off[NB] = tot; total = tot;
    if (ssz != 3 * tot) { printf("states file size %llu != 3*%llu\nREJECT\n", (unsigned long long)ssz, (unsigned long long)tot); return 1; }
    if (vsz != 4 * tot) { printf("V file size %llu != 4*%llu\nREJECT\n", (unsigned long long)vsz, (unsigned long long)tot); return 1; }
    if (tot == 0) { printf("empty state set\nREJECT\n"); return 1; }

    printf("N=%d\n", N);
    printf("states=%llu\n", (unsigned long long)tot);
    fflush(stdout);

    Res R = sweep(-1, -1, 1);
    printf("rowStates=%llu shiftStates=%llu\n", (unsigned long long)R.nrow, (unsigned long long)R.nshift);
    printf("minE=%lld (attained by %llu states, first index %lld)\n", (long long)R.minE, (unsigned long long)R.nmin, (long long)R.minIdx);
    printf("failures: structure=%llu C1=%llu C2=%llu C3=%llu\n",
        (unsigned long long)R.struct_fail, (unsigned long long)R.c1fail,
        (unsigned long long)R.c2fail, (unsigned long long)R.c3fail);
    fflush(stdout);
    if (!R.ok) { printf("REJECT m=%lld K=%lld\n", (long long)mc, (long long)Kc); return 1; }

    if (mode) {
        Res R2;
        if (!strcmp(mode, "perturb")) {
            printf("perturb: V[%lld] += 1 (state with E = minE)\n", (long long)R.minIdx);
            R2 = sweep(-1, R.minIdx, 0);
        } else {
            i64 d = (i64)(tot / 2);
            printf("drop: removing middle state index %lld\n", (long long)d);
            R2 = sweep(d, -1, 0);
        }
        printf("mutated: minE=%lld failures C1=%llu C2=%llu C3=%llu\n", (long long)R2.minE,
            (unsigned long long)R2.c1fail, (unsigned long long)R2.c2fail, (unsigned long long)R2.c3fail);
        if (!R2.ok) { printf("REJECT m=%lld K=%lld (mutated, %s)\n", (long long)mc, (long long)Kc, mode); return 1; }
        printf("ACCEPT m=%lld K=%lld\n", (long long)mc, (long long)Kc);
        return 0;
    }
    printf("ACCEPT m=%lld K=%lld\n", (long long)mc, (long long)Kc);
    return 0;
}
