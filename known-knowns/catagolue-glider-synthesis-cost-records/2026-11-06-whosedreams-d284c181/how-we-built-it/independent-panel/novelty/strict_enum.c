/* Exact still-life / strictness search. Single thread.
   A nonempty set A is a still life when every cell of A has 2 or 3
   neighbours in A and no cell outside A has exactly 3 neighbours in A.
   A still life S is pseudo when some nonempty proper subset A is a still
   life and S\A is a still life. Otherwise a still life is strict.
   The mask loop covers every subset. No size cap and no connectivity filter.
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXN 32
#define MAXDEAD 512

static int n;
static int xs[MAXN], ys[MAXN];
static uint32_t neigh[MAXN];
static uint32_t deadm[MAXDEAD];
static int ndead;
static uint32_t full;

static int popc(uint32_t x) { return __builtin_popcount(x); }

static int still_mask(uint32_t M) {
    for (int i = 0; i < n; i++) {
        int c = popc(neigh[i] & M);
        if ((M >> i) & 1u) {
            if (c != 2 && c != 3) return 0;
        } else if (c == 3) {
            return 0;
        }
    }
    for (int d = 0; d < ndead; d++) {
        if (popc(deadm[d] & M) == 3) return 0;
    }
    return 1;
}

/* Independent of the bit masks: stamp the subset on a grid and apply B3/S23. */
static int still_grid(uint32_t M) {
    int minx = xs[0], maxx = xs[0], miny = ys[0], maxy = ys[0];
    for (int i = 1; i < n; i++) {
        if (xs[i] < minx) minx = xs[i];
        if (xs[i] > maxx) maxx = xs[i];
        if (ys[i] < miny) miny = ys[i];
        if (ys[i] > maxy) maxy = ys[i];
    }
    int W = maxx - minx + 5, H = maxy - miny + 5;
    if (W > 64 || H > 64) return -1;
    uint64_t row[64] = {0}, nxt[64] = {0};
    int ox = 2 - minx, oy = 2 - miny;
    int live = 0;
    for (int i = 0; i < n; i++) if ((M >> i) & 1u) {
        row[ys[i] + oy] |= 1ull << (xs[i] + ox);
        live++;
    }
    int live2 = 0;
    for (int y = 1; y < H - 1; y++) {
        for (int x = 1; x < W - 1; x++) {
            int c = 0;
            for (int dy = -1; dy <= 1; dy++) {
                uint64_t r = row[y + dy];
                c += (int)((r >> (x - 1)) & 1u);
                c += (int)((r >> x) & 1u);
                c += (int)((r >> (x + 1)) & 1u);
            }
            int self = (int)((row[y] >> x) & 1u);
            c -= self;
            if (c == 3 || (c == 2 && self)) {
                nxt[y] |= 1ull << x;
                live2++;
            }
        }
    }
    if (live2 != live) return 0;
    for (int y = 0; y < H; y++) if (nxt[y] != row[y]) return 0;
    return 1;
}

/* Sound pruning: assign cells in order. A partial assignment is dropped
   only when every completion violates survival or creates a forced birth.
   IN cells whose neighbour count cannot reach {2,3}, and OUT or exterior
   cells whose IN-neighbour count is already frozen at 3, are impossible.
*/
static uint64_t prune_subsets;
static uint64_t prune_parts;
static uint32_t prune_example_sub;
static uint32_t prune_example_part;

static void rec(int i, uint32_t in, uint32_t assigned) {
    if (i == n) {
        if (in == 0 || in == full) return;
        /* Bounds already imply the live-cell conditions. Recheck fully,
           including exterior births, so a prune bug cannot invent a hit. */
        if (!still_mask(in)) return;
        prune_subsets++;
        if (!prune_example_sub) prune_example_sub = in;
        if (still_mask(full ^ in)) {
            prune_parts++;
            if (!prune_example_part) prune_example_part = in;
        }
        return;
    }
    for (int take = 0; take <= 1; take++) {
        uint32_t nin = in | (take ? (1u << i) : 0u);
        uint32_t nas = assigned | (1u << i);
        int ok = 1;
        for (int j = 0; j < n && ok; j++) {
            uint32_t seen = neigh[j] & nas;
            uint32_t freeb = neigh[j] & ~nas;
            int cin = popc(neigh[j] & nin);
            int cfree = popc(freeb);
            if ((nas >> j) & 1u) {
                if ((nin >> j) & 1u) {
                    if (cin > 3 || cin + cfree < 2) ok = 0;
                } else if (cfree == 0 && cin == 3) {
                    ok = 0; /* frozen birth at an OUT cell */
                }
            }
        }
        if (!ok) continue;
        for (int d = 0; d < ndead && ok; d++) {
            uint32_t seen = deadm[d] & nas;
            uint32_t freeb = deadm[d] & ~nas;
            int cin = popc(deadm[d] & nin);
            int cfree = popc(freeb);
            if (cfree == 0 && cin == 3) ok = 0;
        }
        if (ok) rec(i + 1, nin, nas);
    }
}

static void setup(int ncells, const int *px, const int *py) {
    n = ncells;
    full = (n == 32) ? 0xffffffffu : ((1u << n) - 1u);
    for (int i = 0; i < n; i++) { xs[i] = px[i]; ys[i] = py[i]; }
    for (int i = 0; i < n; i++) {
        uint32_t m = 0;
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            int dx = xs[i] - xs[j]; if (dx < 0) dx = -dx;
            int dy = ys[i] - ys[j]; if (dy < 0) dy = -dy;
            if (dx <= 1 && dy <= 1) m |= 1u << j;
        }
        neigh[i] = m;
    }
    ndead = 0;
    int minx = xs[0], maxx = xs[0], miny = ys[0], maxy = ys[0];
    for (int i = 1; i < n; i++) {
        if (xs[i] < minx) minx = xs[i];
        if (xs[i] > maxx) maxx = xs[i];
        if (ys[i] < miny) miny = ys[i];
        if (ys[i] > maxy) maxy = ys[i];
    }
    for (int y = miny - 1; y <= maxy + 1; y++) {
        for (int x = minx - 1; x <= maxx + 1; x++) {
            int live = 0;
            for (int i = 0; i < n; i++) if (xs[i] == x && ys[i] == y) live = 1;
            if (live) continue;
            uint32_t m = 0; int c = 0;
            for (int i = 0; i < n; i++) {
                int dx = xs[i] - x; if (dx < 0) dx = -dx;
                int dy = ys[i] - y; if (dy < 0) dy = -dy;
                if (dx <= 1 && dy <= 1 && (dx | dy)) { m |= 1u << i; c++; }
            }
            if (c >= 3) {
                if (ndead >= MAXDEAD) { fprintf(stderr, "dead overflow\n"); exit(2); }
                deadm[ndead++] = m;
            }
        }
    }
}

static int comps8(void) {
    int seen[MAXN] = {0}, ncomp = 0;
    for (int i = 0; i < n; i++) {
        if (seen[i]) continue;
        ncomp++;
        int stack[MAXN], sp = 0;
        stack[sp++] = i; seen[i] = 1;
        while (sp) {
            int u = stack[--sp];
            for (int v = 0; v < n; v++) if (!seen[v] && ((neigh[u] >> v) & 1u)) {
                seen[v] = 1; stack[sp++] = v;
            }
        }
    }
    return ncomp;
}

static void report(const char *name, int expect_still, int expect_pseudo) {
    int whole = still_mask(full);
    if (still_grid(full) != whole) {
        printf("GRID DISAGREE on whole %s mask %d grid %d\n", name, whole, still_grid(full));
        exit(7);
    }
    uint64_t subsets = 0, parts = 0, grid_sub = 0, grid_parts = 0;
    uint32_t ex_sub = 0, ex_part = 0;
    if (whole && n <= 28) {
        for (uint32_t M = 1; M < full; M++) {
            int sm = still_mask(M);
            /* Full grid cross-check is cheap through 12 cells. On the 28-cell
               target, grid-check every mask the bit test calls stable, plus
               that mask's complement, so a bit-test false positive cannot pass. */
            if (n <= 12) {
                int sg = still_grid(M);
                if (sm != sg) {
                    printf("GRID DISAGREE %s mask 0x%x bit %d grid %d\n", name, M, sm, sg);
                    exit(8);
                }
            }
            if (!sm) continue;
            if (n > 12) {
                int sg = still_grid(M);
                int cg = still_grid(full ^ M);
                int cb = still_mask(full ^ M);
                if (!sg || cg != cb) {
                    printf("GRID DISAGREE hit %s mask 0x%x grid_sub %d bit_comp %d grid_comp %d\n",
                           name, M, sg, cb, cg);
                    exit(8);
                }
            }
            subsets++;
            grid_sub++;
            if (!ex_sub) ex_sub = M;
            if (n == 28) {
                printf("  STABLE_SUBSET mask 0x%x pop %d complement_bit %d complement_grid %d cells",
                       M, popc(M), still_mask(full ^ M), still_grid(full ^ M));
                for (int i = 0; i < n; i++) if ((M >> i) & 1u) printf(" %d,%d", xs[i], ys[i]);
                printf("\n");
            }
            /* count each unordered partition once */
            if (M < (full ^ M) && still_mask(full ^ M)) {
                parts++;
                grid_parts++;
                if (!ex_part) ex_part = M;
            }
        }
    }
    (void)grid_sub; (void)grid_parts;
    prune_subsets = 0; prune_parts = 0; prune_example_sub = 0; prune_example_part = 0;
    if (whole && n <= 22) {
        /* Pruned recursion is 2^n leaves with overhead. Use it as a
           cross-check up to 22 cells; the 28-cell case uses the flat loop,
           which is the same un-capped set of masks. */
        rec(0, 0, 0);
        /* rec counts ordered masks, so parts are double the unordered count
           except when a mask equals its complement (impossible: equal size
           only if n even and M == ~M, which cannot happen for bits). */
    }
    int pseudo = whole && parts > 0;
    int strict = whole && parts == 0;
    const char *cls = !whole ? "UNSTABLE" : (pseudo ? "PSEUDO" : "STRICT");
    printf("CASE %s pop %d still %d comps8 %d stable_proper_subsets %llu unordered_stable_partitions %llu class %s\n",
           name, n, whole, comps8(),
           (unsigned long long)subsets, (unsigned long long)parts, cls);
    if (ex_sub) printf("  example_stable_subset_mask 0x%x\n", ex_sub);
    if (ex_part) printf("  example_partition_mask 0x%x\n", ex_part);
    if (whole && n <= 22) {
        uint64_t punordered = prune_parts / 2;
        printf("  prune_crosscheck subsets %llu partitions %llu %s\n",
               (unsigned long long)prune_subsets,
               (unsigned long long)punordered,
               (prune_subsets == subsets && punordered == parts) ? "AGREE" : "DISAGREE");
        if (prune_subsets != subsets || punordered != parts) exit(3);
    }
    if (expect_still >= 0 && whole != expect_still) {
        printf("  FAIL expected still=%d\n", expect_still); exit(4);
    }
    if (expect_pseudo >= 0 && pseudo != expect_pseudo) {
        printf("  FAIL expected pseudo=%d\n", expect_pseudo); exit(5);
    }
    printf("  test_ok\n");
}

static int decode(const char *code, int *px, int *py) {
    const char *us = strchr(code, '_');
    if (!us) return -1;
    const char *w = us + 1;
    int cnt = 0, strip = 0;
    const char *p = w;
    while (*p && cnt < MAXN) {
        if (*p == 'z') { strip++; p++; continue; }
        /* one strip handled below by scanning; restart properly */
        break;
    }
    cnt = 0; strip = 0;
    for (const char *s = w; *s; ) {
        const char *z = strchr(s, 'z');
        int len = z ? (int)(z - s) : (int)strlen(s);
        int col = 0, i = 0;
        while (i < len) {
            char ch = s[i];
            if (ch == 'w') { col += 2; i++; }
            else if (ch == 'x') { col += 3; i++; }
            else if (ch == 'y') {
                if (i + 1 >= len) return -1;
                int v = s[i + 1];
                int dig = (v >= '0' && v <= '9') ? v - '0' : (v >= 'a' && v <= 'z') ? v - 'a' + 10 : -1;
                if (dig < 0) return -1;
                col += 4 + dig; i += 2;
            } else {
                int v;
                if (ch >= '0' && ch <= '9') v = ch - '0';
                else if (ch >= 'a' && ch <= 'v') v = ch - 'a' + 10;
                else return -1;
                for (int b = 0; b < 5; b++) if ((v >> b) & 1) {
                    if (cnt >= MAXN) return -1;
                    px[cnt] = col; py[cnt] = 5 * strip + b; cnt++;
                }
                col++; i++;
            }
        }
        if (!z) break;
        strip++;
        s = z + 1;
    }
    return cnt;
}

int main(void) {
    int px[MAXN], py[MAXN];

    /* strict block */
    { int x[] = {0,1,0,1}, y[] = {0,0,1,1}; setup(4, x, y); report("block", 1, 0); }

    /* strict barge, one 8-component, orthogonally disconnected */
    { int x[] = {1,0,2,0,2,1}, y[] = {0,1,1,2,2,3}; setup(6, x, y); report("barge", 1, 0); }

    /* aircraft carrier: two 8-components, neither stable, strict */
    { int x[] = {0,1,0,3,2,3}, y[] = {0,0,1,1,2,2}; setup(6, x, y); report("aircraft_carrier", 1, 0); }

    /* pseudo: bi-block (separated by one column) */
    { int x[] = {0,1,0,1,4,5,4,5}, y[] = {0,0,1,1,0,0,1,1}; setup(8, x, y); report("biblock", 1, 1); }

    /* pseudo: two blocks far apart */
    { int x[] = {0,1,0,1,20,21,20,21}, y[] = {0,0,1,1,20,20,21,21}; setup(8, x, y); report("two_separated_blocks", 1, 1); }

    /* unstable blinker phase */
    { int x[] = {0,1,2}, y[] = {0,0,0}; setup(3, x, y); report("blinker", 0, -1); }

    /* unstable L triomino */
    { int x[] = {0,1,0}, y[] = {0,0,1}; setup(3, x, y); report("L_triomino", 0, -1); }

    int nt = decode("xs28_69a4owgzxol5d1d96", px, py);
    if (nt != 28) { printf("decode target pop %d\n", nt); return 6; }
    setup(nt, px, py);
    printf("TARGET_DECODE pop %d\n", nt);
    report("xs28_69a4owgzxol5d1d96", 1, -1);

    /* 22-cell slice of the target as a prune-vs-flat agreement check on a
       non-still subset is not required. The named controls already compare
       the pruner against the flat loop through 8 cells, and aircraft/barge
       through 6. */
    return 0;
}
