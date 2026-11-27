/* tmcrit_stream.c -- tmcrit.c with the transfer structure streamed from disk (run 2026-10-16-1714).
 * Identical states, transitions, power method and root search; each step's transitions are written to three
 * files per sector during the build (per-state counts, targets, classes) and read back in the same order on every
 * sweep, so memory holds one step plus the vectors. The arithmetic order is unchanged, so the printed root must be
 * bit-identical to tmcrit.exe's (test_stream.py). Generated from tmcrit.c by make_stream.py.
 * usage: tmcrit_stream <program file> <site|bond> <p_lo> <p_hi> [tol] [scratch folder]
 *
 * Original header of tmcrit.c:
 * tmcrit.c -- critical-polynomial roots on n x infinity bases by the eigenvalue method
 * (Jacobsen, arXiv:1507.03027, eq. 13: P_B = 0  <=>  Lambda_open = Lambda_closed),
 * written here in the cluster (connectivity) representation for site or bond percolation.
 *
 * The lattice is swept vertex by vertex along a semi-infinite cylinder (program file from sweep.py).
 * A state is the frontier: for each slot, empty (0), or a component label, or INF; for non-INF components a
 * lift offset (seam crossings) relative to the component's first slot.
 *   closed sector: no cluster may wind around the cylinder (a winding cluster kills the configuration);
 *   open sector:   a cluster INF that winds around and reaches the infinite past must stay on the frontier,
 *                  and no other cluster may wind (two winding clusters would enclose a winding dual cluster,
 *                  weight n_wind = 0).
 * Lambda_closed and Lambda_open are the leading eigenvalues of the period transfer matrix in each sector
 * (power method). The root p_c(n) of log Lambda_open - log Lambda_closed is found by bisection + secant.
 *
 * usage: tmcrit <program file> <site|bond> <p_lo> <p_hi> [tol]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <process.h>

#define MAXS 48
#define LINF 63
#define LNEW 62
#define MAXNB 16

typedef struct {
    int nnb, nb_s[MAXNB], nb_w[MAXNB];
    int nself, self_w[MAXNB];
    int nrem, rem[MAXNB];
    int Fb;   /* frontier size before the step */
} step_t;

static int n_cyl, P, B, KW;  /* KW: uint64 words per key */
static step_t *steps;
static int bond_mode = 0;

static void die(const char *m) { fprintf(stderr, "error: %s\n", m); exit(2); }

/* ---------------- state coding ---------------- */
static void encode(const uint8_t *lab, const int8_t *off, int F, uint64_t *key) {
    memset(key, 0, sizeof(uint64_t) * KW);
    uint8_t *b = (uint8_t *)key;
    for (int i = 0; i < F; i++) {
        if (lab[i] == 0) b[i] = 0;
        else b[i] = (uint8_t)(lab[i] | ((off[i] + 1) << 6));
    }
}
static void decode(const uint64_t *key, int F, uint8_t *lab, int8_t *off) {
    const uint8_t *b = (const uint8_t *)key;
    for (int i = 0; i < F; i++) {
        lab[i] = b[i] & 63;
        off[i] = lab[i] ? (int8_t)((b[i] >> 6) - 1) : 0;
    }
}
/* canonical relabelling: labels by first appearance, offsets relative to the first slot of each component */
static void canon(uint8_t *lab, int8_t *off, int F) {
    int map[64], base[64];
    for (int i = 0; i < 64; i++) map[i] = -1;
    int next = 1;
    for (int i = 0; i < F; i++) {
        int l = lab[i];
        if (l == 0) { off[i] = 0; continue; }
        if (l == LINF) { off[i] = 0; continue; }
        if (map[l] < 0) { map[l] = next++; base[l] = off[i]; }
        int o = off[i] - base[l];
        if (o < -1 || o > 1) die("lift offset outside {-1,0,1}: frontier not planar-ordered");
        lab[i] = (uint8_t)map[l];
        off[i] = (int8_t)o;
    }
    if (next >= LNEW) die("too many components");
}

/* ---------------- hash set of keys ---------------- */
typedef struct {
    uint64_t *keys; int64_t n, cap_keys;
    int32_t *tab; int64_t tcap;
} hset_t;

static uint64_t hkey(const uint64_t *k) {
    uint64_t h = 0x9E3779B97F4A7C15ULL;
    for (int i = 0; i < KW; i++) { h ^= k[i]; h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 31; }
    return h;
}
static void hs_init(hset_t *h) {
    h->n = 0; h->cap_keys = 1024; h->keys = malloc(sizeof(uint64_t) * KW * h->cap_keys);
    h->tcap = 2048; h->tab = malloc(sizeof(int32_t) * h->tcap);
    for (int64_t i = 0; i < h->tcap; i++) h->tab[i] = -1;
}
static void hs_free(hset_t *h) { free(h->keys); free(h->tab); h->keys = NULL; h->tab = NULL; h->n = 0; }
static void hs_rehash(hset_t *h) {
    int64_t nc = h->tcap * 2;
    int32_t *t = malloc(sizeof(int32_t) * nc);
    for (int64_t i = 0; i < nc; i++) t[i] = -1;
    for (int64_t j = 0; j < h->n; j++) {
        uint64_t x = hkey(h->keys + j * KW) & (nc - 1);
        while (t[x] >= 0) x = (x + 1) & (nc - 1);
        t[x] = (int32_t)j;
    }
    free(h->tab); h->tab = t; h->tcap = nc;
}
static int32_t hs_find_or_add(hset_t *h, const uint64_t *k, int add) {
    uint64_t x = hkey(k) & (h->tcap - 1);
    while (h->tab[x] >= 0) {
        if (memcmp(h->keys + (int64_t)h->tab[x] * KW, k, sizeof(uint64_t) * KW) == 0) return h->tab[x];
        x = (x + 1) & (h->tcap - 1);
    }
    if (!add) return -1;
    if (h->n >= h->cap_keys) {
        h->cap_keys *= 2;
        h->keys = realloc(h->keys, sizeof(uint64_t) * KW * h->cap_keys);
        if (!h->keys) die("out of memory (keys)");
    }
    memcpy(h->keys + h->n * KW, k, sizeof(uint64_t) * KW);
    h->tab[x] = (int32_t)h->n;
    h->n++;
    if (h->n * 2 > h->tcap) hs_rehash(h);
    return (int32_t)(h->n - 1);
}

/* ---------------- one step on one state ---------------- */
/* occ: site occupied (site mode); emask: bitmask of open edges among (neighbours, then self loops) (bond mode).
   Returns 1 and the canonical successor, or 0 if the configuration is killed. */
static int apply(const step_t *st, const uint8_t *lab0, const int8_t *off0, int occ, unsigned emask,
                 uint8_t *lab, int8_t *off, int *Fout) {
    int F = st->Fb;
    int had_inf = 0;
    for (int i = 0; i < F; i++) { lab[i] = lab0[i]; off[i] = off0[i]; if (lab[i] == LINF) had_inf = 1; }
    if (!occ) {
        lab[F] = 0; off[F] = 0;
    } else {
        int par[64], sh[64];
        for (int i = 0; i < 64; i++) { par[i] = i; sh[i] = 0; }
        int inf = 0, wind = 0;
        for (int j = 0; j < st->nnb; j++) {
            if (bond_mode && !((emask >> j) & 1)) continue;
            int s = st->nb_s[j], w = st->nb_w[j];
            int l = lab[s];
            if (l == 0) continue;
            if (l == LINF) { inf = 1; continue; }
            int r = l, a = 0;
            while (par[r] != r) { a += sh[r]; r = par[r]; }
            int need = off[s] + a + w;      /* lift of x in r's frame */
            if (r == LNEW) { if (need != 0) wind = 1; }
            else { par[r] = LNEW; sh[r] = 0 - need; }
        }
        for (int j = 0; j < st->nself; j++) {
            if (bond_mode && !((emask >> (st->nnb + j)) & 1)) continue;
            if (st->self_w[j] != 0) wind = 1;
        }
        for (int i = 0; i < F; i++) {
            int l = lab[i];
            if (l == 0 || l == LINF) continue;
            int r = l, a = 0;
            while (par[r] != r) { a += sh[r]; r = par[r]; }
            if (r == LNEW) {
                if (inf) { lab[i] = LINF; off[i] = 0; }
                else { lab[i] = LNEW; off[i] = (int8_t)(off[i] + a); }
            }
        }
        if (inf) { lab[F] = LINF; off[F] = 0; }
        else {
            if (wind) return 0;
            lab[F] = LNEW; off[F] = 0;
        }
    }
    /* removals */
    int k = 0, r = 0, Fn = 0, has_inf = 0;
    for (int i = 0; i <= F; i++) {
        if (r < st->nrem && st->rem[r] == i) { r++; continue; }
        lab[k] = lab[i]; off[k] = off[i]; if (lab[k] == LINF) has_inf = 1; k++;
    }
    Fn = k;
    (void)Fn;
    if (had_inf && !has_inf) return 0;
    canon(lab, off, k);
    *Fout = k;
    return 1;
}

/* ---------------- transfer structure ---------------- */
typedef struct {
    int64_t ns;           /* states at the start of this step */
    int64_t used;         /* transitions of this step */
} trans_t;

static trans_t *T;
static int64_t nboundary;
/* streamed storage, per sector: uint16 successor counts (bond), int32 targets, uint8 classes (bond) */
static FILE *f_cnt, *f_tgt, *f_cls;
static const char *scratch = ".";
static char fn_store[2][3][1024];
static void open_sector_files(int sector, const char *mode) {
    const char *nm[3] = {"cnt", "tgt", "cls"};
    unsigned tag = (unsigned)time(NULL) ^ ((unsigned)_getpid() << 12);
    for (int i = 0; i < 3; i++)
        snprintf(fn_store[sector][i], sizeof fn_store[sector][i], "%s/tmcrit_stream_%08x_%s_%s.bin", scratch, tag,
                 sector ? "open" : "closed", nm[i]);
    f_cnt = fopen(fn_store[sector][0], mode); f_tgt = fopen(fn_store[sector][1], mode); f_cls = fopen(fn_store[sector][2], mode);
    if (!f_cnt || !f_tgt || !f_cls) die("cannot open scratch files");
    setvbuf(f_cnt, NULL, _IOFBF, 1 << 22); setvbuf(f_tgt, NULL, _IOFBF, 1 << 22); setvbuf(f_cls, NULL, _IOFBF, 1 << 22);
}
static void wr(const void *p, size_t sz, size_t n, FILE *f) { if (n && fwrite(p, sz, n, f) != n) die("scratch write failed (disk full?)"); }
static void rd(void *p, size_t sz, size_t n, FILE *f) { if (n && fread(p, sz, n, f) != n) die("scratch read failed"); }

static int nbranch(const step_t *st) { return bond_mode ? (1 << (st->nnb + st->nself)) : 2; }

/* successors of one decoded state at step k: writes keys and classes, returns count */
static int successors(int k, const uint8_t *lab0, const int8_t *off0, uint64_t *keys, uint8_t *cls) {
    const step_t *st = &steps[k];
    uint8_t lab[MAXS]; int8_t off[MAXS]; int F;
    int m = 0;
    if (!bond_mode) {
        for (int occ = 1; occ >= 0; occ--) {
            if (apply(st, lab0, off0, occ, 0, lab, off, &F)) {
                encode(lab, off, F, keys + (int64_t)m * KW); cls[m] = (uint8_t)occ; m++;
            }
        }
    } else {
        int ne = st->nnb + st->nself;
        for (unsigned e = 0; e < (1u << ne); e++) {
            if (apply(st, lab0, off0, 1, e, lab, off, &F)) {
                int o = __builtin_popcount(e);
                encode(lab, off, F, keys + (int64_t)m * KW); cls[m] = (uint8_t)(o | ((ne - o) << 4)); m++;
            }
        }
    }
    return m;
}

static void build(int sector_open, int verbose) {
    /* 1. closure of the boundary set under one period */
    hset_t bset; hs_init(&bset);
    uint8_t lab[MAXS]; int8_t off[MAXS];
    uint64_t key[8];
    for (int i = 0; i < B; i++) {
        if (sector_open) { lab[i] = LINF; off[i] = 0; }
        else if (bond_mode) { lab[i] = (uint8_t)(i + 1); off[i] = 0; }
        else { lab[i] = 0; off[i] = 0; }
    }
    if (!sector_open && bond_mode && B >= LNEW) die("boundary too wide");
    canon(lab, off, B);
    encode(lab, off, B, key);
    hs_find_or_add(&bset, key, 1);
    uint64_t *skeys = malloc(sizeof(uint64_t) * KW * 64);
    uint8_t scls[64];
    for (int pass = 0; pass < 50; pass++) {
        int64_t before = bset.n;
        hset_t cur; hs_init(&cur);
        for (int64_t j = 0; j < bset.n; j++) hs_find_or_add(&cur, bset.keys + j * KW, 1);
        for (int k = 0; k < P; k++) {
            hset_t nxt; hs_init(&nxt);
            for (int64_t j = 0; j < cur.n; j++) {
                decode(cur.keys + j * KW, steps[k].Fb, lab, off);
                int m = successors(k, lab, off, skeys, scls);
                for (int q = 0; q < m; q++) hs_find_or_add(&nxt, skeys + (int64_t)q * KW, 1);
            }
            hs_free(&cur); cur = nxt;
        }
        for (int64_t j = 0; j < cur.n; j++) hs_find_or_add(&bset, cur.keys + j * KW, 1);
        hs_free(&cur);
        if (verbose) fprintf(stderr, "  closure pass %d: boundary states %lld\n", pass, (long long)bset.n);
        if (bset.n == before) break;
    }
    nboundary = bset.n;
    /* 2. final pass storing transitions; state sets per step in order of discovery */
    T = calloc(P, sizeof(trans_t));
    hset_t cur = bset;   /* step 0 states = boundary set, indices as in bset */
    int64_t maxs = 0, tot = 0;
    for (int k = 0; k < P; k++) {
        hset_t nxt;
        int last = (k == P - 1);
        if (last) nxt = bset; else hs_init(&nxt);
        int64_t ns = cur.n;
        T[k].ns = ns;
        int64_t used = 0;
        if (!bond_mode) {
            /* site mode: exactly two slots per state, [2j] = occupied successor, [2j+1] = empty successor */
            int32_t *tg = malloc(sizeof(int32_t) * 2 * (ns > 0 ? ns : 1));
            if (!tg) die("out of memory (transitions)");
            for (int64_t j = 0; j < ns; j++) {
                tg[2 * j] = -1; tg[2 * j + 1] = -1;
                decode(cur.keys + j * KW, steps[k].Fb, lab, off);
                int m = successors(k, lab, off, skeys, scls);
                for (int q = 0; q < m; q++) {
                    int32_t id = hs_find_or_add(&nxt, skeys + (int64_t)q * KW, !last);
                    if (id < 0) die("boundary set not closed");
                    tg[2 * j + (scls[q] ? 0 : 1)] = id; used++;
                }
            }
            wr(tg, sizeof(int32_t), (size_t)(2 * ns), f_tgt);
            free(tg);
        } else {
            uint16_t *cn = malloc(sizeof(uint16_t) * (ns > 0 ? ns : 1));
            int64_t cap = ns * 2 + 16;
            int32_t *tg = malloc(sizeof(int32_t) * cap);
            uint8_t *cl = malloc(cap);
            if (!cn || !tg || !cl) die("out of memory (transitions)");
            for (int64_t j = 0; j < ns; j++) {
                decode(cur.keys + j * KW, steps[k].Fb, lab, off);
                int m = successors(k, lab, off, skeys, scls);
                if (m > 65535) die("too many successors");
                cn[j] = (uint16_t)m;
                for (int q = 0; q < m; q++) {
                    int32_t id = hs_find_or_add(&nxt, skeys + (int64_t)q * KW, !last);
                    if (id < 0) die("boundary set not closed");
                    if (used >= cap) {
                        cap *= 2;
                        tg = realloc(tg, sizeof(int32_t) * cap);
                        cl = realloc(cl, cap);
                        if (!tg || !cl) die("out of memory (transitions)");
                    }
                    tg[used] = id; cl[used] = scls[q]; used++;
                }
            }
            wr(cn, sizeof(uint16_t), (size_t)ns, f_cnt); wr(tg, sizeof(int32_t), (size_t)used, f_tgt); wr(cl, 1, (size_t)used, f_cls);
            free(cn); free(tg); free(cl);
        }
        T[k].used = used;
        if (ns > maxs) maxs = ns;
        tot += used;
        if (k > 0) hs_free(&cur);
        cur = nxt;
    }
    hs_free(&bset);
    free(skeys);
    if (verbose) fprintf(stderr, "  %s sector: boundary %lld states, max per step %lld, transitions %lld\n",
                         sector_open ? "open" : "closed", (long long)nboundary, (long long)maxs, (long long)tot);
}

static void free_T(void) { free(T); }

/* ---------------- power method ---------------- */
static double wt[256];
static void set_weights(double p) {
    for (int c = 0; c < 256; c++) {
        if (!bond_mode) wt[c] = (c & 1) ? p : 1 - p;
        else { int o = c & 15, z = c >> 4; wt[c] = pow(p, o) * pow(1 - p, z); }
    }
}
static double *vec_a, *vec_b;
static int64_t vec_cap;

#define CH ((int64_t)1 << 20)       /* states per read chunk */
#define TCH ((int64_t)1 << 24)      /* transitions per read chunk (>= max successors per state) */
static int32_t *buf_tg; static uint8_t *buf_cl; static uint16_t *buf_cn;
static FILE *fc_cnt, *fc_tgt, *fc_cls, *fo_cnt, *fo_tgt, *fo_cls;
/* returns log Lambda per period; x0 (size nboundary) is the start vector and receives the eigenvector */
static double leading(double p, double *x0, int *iters_out, double *ratio_out) {
    set_weights(p);
    double s = 0; for (int64_t j = 0; j < nboundary; j++) s += x0[j];
    for (int64_t j = 0; j < nboundary; j++) x0[j] /= s;
    double lam = 0, lam_prev = 0, d_prev = 0, ratio = 0;
    int stable = 0, it;
    for (it = 1; it <= 20000; it++) {
        double *x = x0;
        int64_t nx = nboundary;
        rewind(f_cnt); rewind(f_tgt); rewind(f_cls);
        for (int k = 0; k < P; k++) {
            int64_t ny = (k == P - 1) ? nboundary : T[k + 1].ns;
            double *y = (x == vec_a) ? vec_b : vec_a;
            memset(y, 0, sizeof(double) * ny);
            if (!bond_mode) {
                const double wo = wt[1], we = wt[0];
                for (int64_t j0 = 0; j0 < nx; j0 += CH) {
                    int64_t nj = nx - j0 < CH ? nx - j0 : CH;
                    rd(buf_tg, sizeof(int32_t), (size_t)(2 * nj), f_tgt);
                    for (int64_t jj = 0; jj < nj; jj++) {
                        double v = x[j0 + jj];
                        int32_t a = buf_tg[2 * jj], b = buf_tg[2 * jj + 1];
                        if (a >= 0) y[a] += wo * v;
                        if (b >= 0) y[b] += we * v;
                    }
                }
            } else {
                int64_t left = T[k].used, have = 0, pos = 0;
                for (int64_t j0 = 0; j0 < nx; j0 += CH) {
                    int64_t nj = nx - j0 < CH ? nx - j0 : CH;
                    rd(buf_cn, sizeof(uint16_t), (size_t)nj, f_cnt);
                    for (int64_t jj = 0; jj < nj; jj++) {
                        int m = buf_cn[jj];
                        if (have - pos < m) {      /* refill: keep the unread tail, read the next chunk */
                            int64_t tail = have - pos;
                            memmove(buf_tg, buf_tg + pos, sizeof(int32_t) * tail);
                            memmove(buf_cl, buf_cl + pos, tail);
                            int64_t get = left < TCH - tail ? left : TCH - tail;
                            rd(buf_tg + tail, sizeof(int32_t), (size_t)get, f_tgt);
                            rd(buf_cl + tail, 1, (size_t)get, f_cls);
                            left -= get; have = tail + get; pos = 0;
                            if (have < m) die("stream refill too short");
                        }
                        double v = x[j0 + jj];
                        if (v != 0)
                            for (int q = 0; q < m; q++) y[buf_tg[pos + q]] += wt[buf_cl[pos + q]] * v;
                        pos += m;
                    }
                }
                if (left != 0 || pos != have) die("stream out of step");
            }
            x = y; nx = ny;
        }
        double sum = 0; for (int64_t j = 0; j < nboundary; j++) sum += x[j];
        lam = sum;  /* x0 had unit L1 norm */
        for (int64_t j = 0; j < nboundary; j++) x0[j] = x[j] / sum;
        double d = lam - lam_prev;
        if (it > 2 && d_prev != 0) ratio = d / d_prev;
        /* Convergence is geometric; once |d| reaches the summation-noise floor (a few 1e-15 relative, more for
           long periods) it stops shrinking. A hit is either |d| <= 4e-15 lam, or |d| <= 1e-12 lam and no longer
           shrinking (|d| >= 0.9 |d_prev|). Hits are counted, not reset; 3 hits stop the iteration. */
        if (it > 3 && (fabs(d) <= 4e-15 * lam || (fabs(d) <= 1e-12 * lam && fabs(d) >= 0.9 * fabs(d_prev)))) {
            if (++stable >= 3) break;
        }
        d_prev = d; lam_prev = lam;
    }
    if (it > 20000) fprintf(stderr, "warning: power method hit the iteration cap at p=%.17g\n", p);
    *iters_out = it; *ratio_out = ratio;
    return log(lam);
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: tmcrit prog site|bond p_lo p_hi [tol]\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) die("cannot open program");
    bond_mode = strcmp(argv[2], "bond") == 0;
    double plo = atof(argv[3]), phi = atof(argv[4]);
    double tol = argc > 5 ? atof(argv[5]) : 1e-15;
    if (argc > 6) scratch = argv[6];
    if (fscanf(f, " n %d P %d B %d", &n_cyl, &P, &B) != 3) die("bad header");
    steps = calloc(P, sizeof(step_t));
    int F = B, maxF = B + 1;
    char w[16];
    for (int k = 0; k < P; k++) {
        step_t *st = &steps[k];
        st->Fb = F;
        if (fscanf(f, " %15s %d", w, &st->nnb) != 2 || strcmp(w, "nb")) die("bad nb");
        if (st->nnb > MAXNB) die("too many neighbours");
        for (int j = 0; j < st->nnb; j++) if (fscanf(f, " %d %d", &st->nb_s[j], &st->nb_w[j]) != 2) die("bad nb pair");
        if (fscanf(f, " %15s %d", w, &st->nself) != 2 || strcmp(w, "self")) die("bad self");
        for (int j = 0; j < st->nself; j++) if (fscanf(f, " %d", &st->self_w[j]) != 1) die("bad self w");
        if (fscanf(f, " %15s %d", w, &st->nrem) != 2 || strcmp(w, "rem")) die("bad rem");
        for (int j = 0; j < st->nrem; j++) if (fscanf(f, " %d", &st->rem[j]) != 1) die("bad rem i");
        for (int j = 0; j < st->nnb; j++) if (st->nb_s[j] < 0 || st->nb_s[j] >= F) die("nb slot out of range");
        F = F + 1 - st->nrem;
        if (F + 1 > maxF) maxF = F + 1;
        if (bond_mode && st->nnb + st->nself > 12) die("too many edges for bond branching");
    }
    fclose(f);
    if (F != B) die("program does not return to the boundary size");
    if (maxF > MAXS) die("frontier too wide");
    KW = (maxF + 7) / 8;
    clock_t t0 = clock();
    /* build both sectors, keeping each structure; evaluate f(p) = logL_open - logL_closed */
    fprintf(stderr, "n=%d P=%d B=%d maxF=%d mode=%s\n", n_cyl, P, B, maxF, bond_mode ? "bond" : "site");
    trans_t *Tc, *To; int64_t nbc, nbo;
    open_sector_files(0, "w+b"); build(0, 1); Tc = T; nbc = nboundary; fc_cnt = f_cnt; fc_tgt = f_tgt; fc_cls = f_cls;
    open_sector_files(1, "w+b"); build(1, 1); To = T; nbo = nboundary; fo_cnt = f_cnt; fo_tgt = f_tgt; fo_cls = f_cls;
    fflush(fc_cnt); fflush(fc_tgt); fflush(fc_cls); fflush(fo_cnt); fflush(fo_tgt); fflush(fo_cls);
    buf_tg = malloc(sizeof(int32_t) * (2 * CH > TCH ? 2 * CH : TCH)); buf_cl = malloc(TCH); buf_cn = malloc(sizeof(uint16_t) * CH);
    if (!buf_tg || !buf_cl || !buf_cn) die("out of memory (buffers)");
    int64_t mx = 0;
    for (int k = 0; k < P; k++) { if (Tc[k].ns > mx) mx = Tc[k].ns; if (To[k].ns > mx) mx = To[k].ns; }
    vec_cap = mx + 16;
    vec_a = malloc(sizeof(double) * vec_cap); vec_b = malloc(sizeof(double) * vec_cap);
    double *xc = malloc(sizeof(double) * nbc), *xo = malloc(sizeof(double) * nbo);
    for (int64_t j = 0; j < nbc; j++) xc[j] = 1;
    for (int64_t j = 0; j < nbo; j++) xo[j] = 1;
    fprintf(stderr, "build time %.1f s\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    int itc, ito; double rc, ro;
#define EVAL(p, out) do { T = Tc; nboundary = nbc; f_cnt = fc_cnt; f_tgt = fc_tgt; f_cls = fc_cls; \
        double lc = leading(p, xc, &itc, &rc); \
        T = To; nboundary = nbo; f_cnt = fo_cnt; f_tgt = fo_tgt; f_cls = fo_cls; \
        double lo = leading(p, xo, &ito, &ro); out = lo - lc; \
        fprintf(stderr, "  p=%.17g  f=%.6e  (iters %d/%d, ratios %.3f/%.3f)\n", p, out, itc, ito, rc, ro); } while (0)
    double flo, fhi;
    EVAL(plo, flo); EVAL(phi, fhi);
    if (!(flo < 0 && fhi > 0)) { fprintf(stderr, "root not bracketed: f(lo)=%g f(hi)=%g\n", flo, fhi); return 3; }
    /* Illinois-modified regula falsi */
    double a = plo, b = phi, fa = flo, fb = fhi, c = a, fc;
    int side = 0;
    for (int it = 0; it < 200; it++) {
        c = (a * fb - b * fa) / (fb - fa);
        if (!(c > a && c < b)) c = 0.5 * (a + b);
        EVAL(c, fc);
        if (fc == 0) break;
        if ((fc > 0) == (fb > 0)) { b = c; fb = fc; if (side == -1) fa *= 0.5; side = -1; }
        else { a = c; fa = fc; if (side == 1) fb *= 0.5; side = 1; }
        if (b - a < tol) break;
    }
    double root = (fabs(fa) < fabs(fb)) ? a : b;
    if (fabs(fc) < fabs(fa) && fabs(fc) < fabs(fb)) root = c;
    printf("n %d mode %s pc %.17g bracket %.17g %.17g states_closed %lld states_open %lld time %.1f\n",
           n_cyl, bond_mode ? "bond" : "site", root, a, b, (long long)nbc, (long long)nbo,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    T = Tc; free_T(); T = To; free_T();
    fclose(fc_cnt); fclose(fc_tgt); fclose(fc_cls); fclose(fo_cnt); fclose(fo_tgt); fclose(fo_cls);
    for (int s2 = 0; s2 < 2; s2++) for (int i = 0; i < 3; i++) remove(fn_store[s2][i]);
    return 0;
}
