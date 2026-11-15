/* Exact join for *3-fixed first rows of CW(208,81).
 *
 * A shift that is a multiple of 13 stays inside one residue class mod 13,
 * hence inside one fiber-group. Those autocorrelations have no cross-group
 * term, so the two halves must cancel on those shifts. Survivors are checked
 * at every shift by integer arithmetic.
 *
 *   liftjoin [target|all] [seconds]  (default: all; 0 seconds: uncapped)
 *   liftjoin --selftest
 *   liftjoin --contractions         (25 lines, 13 integers per line)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <limits.h>

#define N 208
#define NG 5
#define MAXSIG 200
#define MAXNZ 80
#define SHIFTS 7
#define MAP 4194304
static const int SHIFT[SHIFTS] = {13, 26, 39, 52, 65, 78, 91};

static int norb, olen[64], omem[64][16];
static int z13_orb[5][3], z13_len[5];
static int gcount[NG], gorb[NG][8], gcontrib[NG][8];
static int gpos[NG][64], gnpos[NG];

typedef struct {
    int nz;
    int pos[MAXNZ];
    int8_t val[MAXNZ];
} Sig;
static Sig sigs[NG][MAXSIG];
static int nsig[NG];
static int icw[80][13], ntargets;
static int order[NG];

static int64_t hits, matches, streamed;
static time_t start_time, last_ckpt;
static int cap_sec, capped;
static void maybe_ckpt(void);

static void die(const char *m) { fprintf(stderr, "%s\n", m); exit(2); }

static int in_group(int g, int f) {
    for (int k = 0; k < z13_len[g]; k++) if (z13_orb[g][k] == f) return 1;
    return 0;
}

static void build(void) {
    uint8_t seen[N] = {0};
    norb = 0;
    for (int x = 0; x < N; x++) {
        if (seen[x]) continue;
        int y = x, k = 0;
        while (!seen[y]) {
            if (norb >= 64 || k >= 16) die("orbit bounds");
            seen[y] = 1;
            omem[norb][k++] = y;
            y = (3 * y) % N;
        }
        olen[norb++] = k;
    }
    if (norb != 35) die("orbits");
    uint8_t s13[13] = {0};
    int n13 = 0;
    for (int x = 0; x < 13; x++) {
        if (s13[x]) continue;
        int y = x, k = 0;
        while (!s13[y]) {
            if (n13 >= NG || k >= 3) die("z13 bounds");
            s13[y] = 1;
            z13_orb[n13][k++] = y;
            y = (3 * y) % 13;
        }
        z13_len[n13++] = k;
    }
    if (n13 != 5 || z13_len[0] != 1) die("z13");
    for (int o = 0; o < norb; o++) {
        int f = omem[o][0] % 13, g = -1;
        for (int i = 0; i < 5 && g < 0; i++) if (in_group(i, f)) g = i;
        if (g < 0) die("group");
        if (gcount[g] >= 8) die("group bounds");
        int slot = gcount[g]++;
        gorb[g][slot] = o;
        int f0 = z13_orb[g][0], cnt = 0;
        for (int i = 0; i < olen[o]; i++) {
            if (!in_group(g, omem[o][i] % 13)) die("cross");
            if ((omem[o][i] % 13) == f0) cnt++;
            if (gnpos[g] >= 64) die("group position bounds");
            gpos[g][gnpos[g]++] = omem[o][i];
        }
        gcontrib[g][slot] = cnt;
    }
    for (int g = 0; g < NG; g++) if (gcount[g] != 7 || gnpos[g] > 64) die("gcount");
}

static void enum_signings(int g, int T) {
    nsig[g] = 0;
    int c[7];
    for (int i = 0; i < 7; i++) c[i] = gcontrib[g][i];
    for (int a = -1; a <= 1; a++)
    for (int b = -1; b <= 1; b++)
    for (int d = -1; d <= 1; d++)
    for (int e = -1; e <= 1; e++)
    for (int f = -1; f <= 1; f++)
    for (int h = -1; h <= 1; h++)
    for (int i = -1; i <= 1; i++) {
        int sm = c[0]*a + c[1]*b + c[2]*d + c[3]*e + c[4]*f + c[5]*h + c[6]*i;
        if (sm != T) continue;
        if (nsig[g] >= MAXSIG) die("signings");
        int signs[7] = {a, b, d, e, f, h, i};
        Sig *s = &sigs[g][nsig[g]++];
        s->nz = 0;
        for (int k = 0; k < 7; k++) if (signs[k]) {
            int o = gorb[g][k];
            for (int p = 0; p < olen[o]; p++) {
                if (s->nz >= MAXNZ) die("nz");
                s->pos[s->nz] = omem[o][p];
                s->val[s->nz] = (int8_t)signs[k];
                s->nz++;
            }
        }
    }
}

static void enum_icw(void) {
    ntargets = 0;
    for (int b = -3; b <= 3; b++) {
        int Q = 27 - 3 * b * b, S = 3 - b, a0 = 3 * b;
        for (int a = -16; a <= 16; a++)
        for (int c = -16; c <= 16; c++)
        for (int d = -16; d <= 16; d++)
        for (int e = -16; e <= 16; e++) {
            if (a + c + d + e != S) continue;
            if (a*a + c*c + d*d + e*e != Q) continue;
            int vals[4] = {a, c, d, e};
            int seq[13] = {0};
            seq[0] = a0;
            for (int oi = 0; oi < 4; oi++)
                for (int k = 0; k < z13_len[oi + 1]; k++)
                    seq[z13_orb[oi + 1][k]] = vals[oi];
            int ok = 1;
            for (int t = 1; t < 13 && ok; t++) {
                int corr = 0;
                for (int j = 0; j < 13; j++) corr += seq[j] * seq[(j + t) % 13];
                if (corr) ok = 0;
            }
            if (!ok) continue;
            int row_sum = 0, energy = 0;
            for (int j = 0; j < 13; j++) {
                row_sum += seq[j];
                energy += seq[j] * seq[j];
            }
            if (row_sum != 9 || energy != 81) die("target sum/energy");
            if (ntargets >= (int)(sizeof icw / sizeof icw[0])) die("target bounds");
            for (int j = 0; j < ntargets; j++)
                if (memcmp(icw[j], seq, sizeof seq) == 0) die("duplicate target");
            memcpy(icw[ntargets], seq, sizeof seq);
            ntargets++;
        }
    }
    if (ntargets != 25) die("target count");
}

static int8_t dense[N];

static void corr_dense(int out[SHIFTS]) {
    for (int s = 0; s < SHIFTS; s++) {
        int t = SHIFT[s], c = 0;
        for (int i = 0; i < N; i++) {
            int j = i + t;
            if (j >= N) j -= N;
            c += (int)dense[i] * (int)dense[j];
        }
        out[s] = c;
    }
}

static int autocorr_ok(const int8_t seq[N], int weight) {
    int energy = 0;
    if (weight < 0 || weight > N) return 0;
    for (int i = 0; i < N; i++) {
        if (seq[i] < -1 || seq[i] > 1) return 0;
        energy += (int)seq[i] * (int)seq[i];
    }
    if (energy != weight) return 0;
    for (int t = 1; t < N; t++) {
        int c = 0;
        for (int i = 0; i < N; i++) {
            int j = i + t;
            if (j >= N) j -= N;
            c += (int)seq[i] * (int)seq[j];
        }
        if (c) return 0;
    }
    return 1;
}

static int full_ok(void) { return autocorr_ok(dense, 81); }

static void require_clean_dense(void) {
    for (int i = 0; i < N; i++) if (dense[i]) die("dirty dense");
}

typedef struct {
    int16_t fp[SHIFTS];
    int id;
    int next;
} Node;

static Node *nodes;
static int *head;
static int nnodes, node_cap;
static int8_t *stored; /* nstored * N */
static int nstored;

static uint32_t fp_hash(const int16_t *fp) {
    uint32_t h = 2166136261u;
    for (int i = 0; i < SHIFTS; i++) {
        h ^= (uint16_t)fp[i];
        h *= 16777619u;
    }
    return h & (MAP - 1);
}

static void map_add(const int16_t *fp, int id) {
    if (nnodes >= node_cap) die("map");
    uint32_t h = fp_hash(fp);
    nodes[nnodes].id = id;
    memcpy(nodes[nnodes].fp, fp, sizeof(int16_t) * SHIFTS);
    nodes[nnodes].next = head[h];
    head[h] = nnodes++;
}

static int fp_eq(const int16_t *a, const int *bneg) {
    for (int i = 0; i < SHIFTS; i++) if ((int)a[i] != bneg[i]) return 0;
    return 1;
}

static void emit(void) {
    hits++;
    printf("HIT");
    for (int i = 0; i < N; i++) printf(" %d", (int)dense[i]);
    printf("\n");
    fflush(stdout);
}

static void load_target(int idx) {
    if (idx < 0 || idx >= ntargets) die("target bounds");
    for (int g = 0; g < NG; g++) {
        int T = icw[idx][z13_orb[g][0]];
        enum_signings(g, T);
        order[g] = g;
    }
    /* stored half: two largest signing lists. streamed: the other three. */
    for (int i = 0; i < NG; i++)
        for (int j = i + 1; j < NG; j++)
            if (nsig[order[j]] > nsig[order[i]]) {
                int t = order[i];
                order[i] = order[j];
                order[j] = t;
            }
}

/* Group supports are disjoint; paint/unpaint only their nonzeros. */
static void paint(int g, int si) {
    const Sig *s = &sigs[g][si];
    for (int i = 0; i < s->nz; i++) dense[s->pos[i]] = s->val[i];
}
static void unpaint(int g, int si) {
    const Sig *s = &sigs[g][si];
    for (int i = 0; i < s->nz; i++) dense[s->pos[i]] = 0;
}

/* Shared by production and the exact-identity join controls. */
static void store_half(int s0, int s1, int l0, int l1) {
    /* Brute enumeration leaves its final vector here: clear BEFORE storage. */
    memset(dense, 0, sizeof dense);
    nstored = l0 * l1;
    stored = calloc((size_t)nstored * N, 1);
    if (!stored) die("calloc stored");
    nodes = calloc(nstored + 8, sizeof(Node));
    head = calloc(MAP, sizeof(int));
    if (!nodes || !head) die("calloc map");
    for (int i = 0; i < MAP; i++) head[i] = -1;
    node_cap = nstored + 4;
    nnodes = 0;

    int id = 0;
    for (int i = 0; i < l0; i++) {
        paint(s0, i);
        for (int j = 0; j < l1; j++) {
            paint(s1, j);
            int fp[SHIFTS];
            corr_dense(fp);
            int16_t key[SHIFTS];
            for (int s = 0; s < SHIFTS; s++) key[s] = (int16_t)fp[s];
            map_add(key, id);
            memcpy(stored + (size_t)id * N, dense, N);
            id++;
            unpaint(s1, j);
        }
        unpaint(s0, i);
    }
    if (id != nstored) die("id");
    memset(dense, 0, N);

    require_clean_dense();
}

static void free_half(void) {
    free(stored); free(nodes); free(head);
    stored = NULL; nodes = NULL; head = NULL;
    nstored = nnodes = node_cap = 0;
}

/* Visit each exact fingerprint match with the reconstructed full vector. */
static void join_half(void (*visit)(int id, void *ctx), void *ctx) {
    int fp[SHIFTS], want[SHIFTS];
    int16_t key[SHIFTS];
    corr_dense(fp);
    for (int s = 0; s < SHIFTS; s++) {
        want[s] = -fp[s];
        key[s] = (int16_t)want[s];
    }
    for (int n = head[fp_hash(key)]; n >= 0; n = nodes[n].next) {
        if (!fp_eq(nodes[n].fp, want)) continue;
        int8_t saved[N];
        memcpy(saved, dense, sizeof saved);
        const int8_t *b = stored + (size_t)nodes[n].id * N;
        for (int p = 0; p < N; p++) {
            if (saved[p] && b[p]) die("join support overlap");
            dense[p] = (int8_t)(saved[p] + b[p]);
        }
        visit(nodes[n].id, ctx);
        memcpy(dense, saved, sizeof dense);
    }
}

static void check_candidate(int id, void *ctx) {
    (void)id;
    (void)ctx;
    matches++;
    if (full_ok()) emit();
}

static int run_target(int idx) {
    int64_t before = streamed;
    load_target(idx);
    int s0 = order[0], s1 = order[1], a0 = order[2], a1 = order[3], a2 = order[4];
    printf("TARGET %d stored %d*%d=%d stream %d*%d*%d=%lld signings",
           idx, nsig[s0], nsig[s1], nsig[s0] * nsig[s1],
           nsig[a0], nsig[a1], nsig[a2],
           (long long)nsig[a0] * nsig[a1] * nsig[a2]);
    for (int g = 0; g < NG; g++) printf(" %d", nsig[g]);
    printf("\n");
    fflush(stdout);

    store_half(s0, s1, nsig[s0], nsig[s1]);

    for (int i = 0; i < nsig[a0] && !capped; i++) {
        paint(a0, i);
        for (int j = 0; j < nsig[a1] && !capped; j++) {
            paint(a1, j);
            for (int k = 0; k < nsig[a2] && !capped; k++) {
                paint(a2, k);
                streamed++;
                join_half(check_candidate, NULL);
                if ((streamed & 0xffff) == 0) maybe_ckpt();
                unpaint(a2, k);
            }
            unpaint(a1, j);
        }
        unpaint(a0, i);
    }
    require_clean_dense();
    free_half();
    printf("TARGET_END %d streamed=%lld matches=%lld hits=%lld\n",
           idx, (long long)streamed, (long long)matches, (long long)hits);
    fflush(stdout);
    return streamed - before == (int64_t)nsig[a0] * nsig[a1] * nsig[a2];
}

static void maybe_ckpt(void) {
    time_t now = time(NULL);
    if (now - last_ckpt >= 15) {
        printf("CKPT streamed=%lld matches=%lld hits=%lld elapsed=%ld\n",
               (long long)streamed, (long long)matches, (long long)hits,
               (long)(now - start_time));
        fflush(stdout);
        last_ckpt = now;
    }
    if (cap_sec && now - start_time >= cap_sec) capped = 1;
}

typedef struct {
    uint32_t joined;
    unsigned stream_mask;
    int count;
} TestJoin;

static int selected_zero(void) {
    int fp[SHIFTS];
    corr_dense(fp);
    for (int s = 0; s < SHIFTS; s++) if (fp[s]) return 0;
    return 1;
}

static void test_join_candidate(int id, void *ctx) {
    TestJoin *test = ctx;
    if (id < 0 || id >= 4) die("selftest stored id");
    unsigned mask = test->stream_mask | (unsigned)(id / 2) | ((unsigned)(id % 2) << 2);
    uint32_t bit = UINT32_C(1) << mask;
    if (test->joined & bit) die("selftest duplicate join");
    int8_t expected[N] = {0};
    for (int g = 0; g < NG; g++) {
        const Sig *s = &sigs[g][(mask >> g) & 1u];
        for (int i = 0; i < s->nz; i++) {
            if (expected[s->pos[i]]) die("selftest overlapping supports");
            expected[s->pos[i]] = s->val[i];
        }
    }
    if (memcmp(dense, expected, sizeof dense) || !selected_zero())
        die("selftest reconstructed candidate");
    test->joined |= bit;
    test->count++;
}

static void test_subset(const char *label, int expected_count) {
    uint32_t brute = 0;
    int brute_count = 0;
    for (int g = 0; g < NG; g++) if (nsig[g] < 2) die("selftest subset size");
    for (unsigned mask = 0; mask < 32; mask++) {
        memset(dense, 0, sizeof dense);
        for (int g = 0; g < NG; g++) paint(g, (int)((mask >> g) & 1u));
        if (selected_zero()) {
            brute |= UINT32_C(1) << mask;
            brute_count++;
        }
    }
    /* Keep the last brute vector dirty to regress clearing before storage.
     * Put the two cancelling pairs on OPPOSITE halves of the actual join. */
    store_half(0, 2, 2, 2);
    TestJoin test = {0, 0, 0};
    for (int i1 = 0; i1 < 2; i1++) {
        paint(1, i1);
        for (int i3 = 0; i3 < 2; i3++) {
            paint(3, i3);
            for (int i4 = 0; i4 < 2; i4++) {
                paint(4, i4);
                test.stream_mask = ((unsigned)i1 << 1) | ((unsigned)i3 << 3) | ((unsigned)i4 << 4);
                join_half(test_join_candidate, &test);
                unpaint(4, i4);
            }
            unpaint(3, i3);
        }
        unpaint(1, i1);
    }
    free_half();
    require_clean_dense();
    if (brute != test.joined || brute_count != test.count || brute_count != expected_count)
        die("selftest join identity/count");
    printf("SELFTEST %s brute=%d join=%d rejected=%d identity=ok\n",
           label, brute_count, test.count, 32 - test.count);
}

static void selftest(void) {
    load_target(0);
    test_subset("target0", 0);

    /* Synthetic disjoint supports test the join, NOT a CW(208,81) positive.
     * At shift 13 the first pair contributes +1 and the second -1. */
    memset(sigs, 0, sizeof sigs);
    for (int g = 0; g < NG; g++) nsig[g] = 2;
    sigs[0][1] = (Sig){.nz = 2, .pos = {0, 13}, .val = {1, 1}};
    sigs[1][1] = (Sig){.nz = 2, .pos = {1, 14}, .val = {1, -1}};
    sigs[2][1] = (Sig){.nz = 1, .pos = {2}, .val = {1}};
    sigs[3][1] = (Sig){.nz = 1, .pos = {4}, .val = {1}};
    sigs[4][1] = (Sig){.nz = 1, .pos = {7}, .val = {1}};
    test_subset("synthetic-cancel-not-CW20881", 16);
    sigs[1][1].val[1] = 1; /* Both pairs now positive: no cancellation. */
    test_subset("synthetic-reject-not-CW20881", 8);

    /* Inflated CW(4,4) is a weight-4 positive, NOT a CW(208,81). */
    memset(dense, 0, sizeof dense);
    dense[0] = dense[52] = dense[104] = 1;
    dense[156] = -1;
    if (!autocorr_ok(dense, 4) || autocorr_ok(dense, 3) || full_ok())
        die("selftest inflated CW4 positive/weight");
    dense[156] = 1; /* Same weight, nonzero autocorrelations. */
    if (autocorr_ok(dense, 4)) die("selftest autocorrelation negative");
    memset(dense, 0, sizeof dense);
    if (full_ok()) die("selftest zero weight");
    memset(dense, 1, 81);
    if (full_ok()) die("selftest weight81 autocorrelation negative");
    memset(dense, 0, sizeof dense);
    printf("SELFTEST autocorrelation positive_weight4=ok negative=ok weight81_gate=ok\n");

    /* Remove all synthetic state and restore production signings. */
    memset(sigs, 0, sizeof sigs);
    load_target(0);
    require_clean_dense();
    printf("SELFTEST dense_nonzero=0 status=ok\n");
}

static int parse_uint(const char *text, int max, const char *error) {
    if (!text[0]) die(error);
    for (const char *p = text; *p; p++) if (*p < '0' || *p > '9') die(error);
    errno = 0;
    char *end;
    long value = strtol(text, &end, 10);
    if (errno || *end || value < 0 || value > max) die(error);
    return (int)value;
}

int main(int argc, char **argv) {
    int which = -1, selftest_only = 0, contractions_only = 0;
    if (argc > 3) die("usage: liftjoin [all|0..24] [seconds] | --selftest | --contractions");
    if (argc >= 2) {
        if (!strcmp(argv[1], "--selftest")) selftest_only = 1;
        else if (!strcmp(argv[1], "--contractions")) contractions_only = 1;
        else if (strcmp(argv[1], "all")) which = parse_uint(argv[1], 24, "invalid target: expected all or 0..24");
    }
    if ((selftest_only || contractions_only) && argc != 2) die("mode accepts no extra arguments");
    if (argc == 3) cap_sec = parse_uint(argv[2], INT_MAX, "invalid seconds: expected 0..INT_MAX");
    build();
    enum_icw();
    if (contractions_only) {
        for (int i = 0; i < ntargets; i++) {
            for (int j = 0; j < 13; j++) printf("%s%d", j ? " " : "", icw[i][j]);
            putchar('\n');
        }
        return 0;
    }
    printf("ORBITS %d TARGETS %d\n", norb, ntargets);
    selftest();
    require_clean_dense();
    if (selftest_only) return 0;
    start_time = last_ckpt = time(NULL);
    int lo = 0, hi = ntargets, completed = 0;
    if (which >= 0) { lo = which; hi = which + 1; }
    streamed = matches = hits = 0;
    for (int t = lo; t < hi && !capped; t++) completed += run_target(t);
    time_t now = time(NULL);
    printf("END nodes=%lld hits=%lld capped=%d elapsed=%ld targets=%d matches=%lld completed=%d\n",
           (long long)streamed, (long long)hits, capped, (long)(now - start_time),
           ntargets, (long long)matches, completed);
    return 0;
}

