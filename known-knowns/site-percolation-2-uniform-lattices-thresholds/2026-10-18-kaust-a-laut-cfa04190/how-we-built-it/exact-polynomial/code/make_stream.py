"""Derive tmcrit_stream.c from tmcrit.c by exact text replacements (each must match once), so the diff between the
two programs is only the storage of the transfer structure. Run once: python make_stream.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "tmcrit.c"), encoding="utf-8").read()


def rep(a, b):
    global t
    assert t.count(a) == 1, a[:70]
    t = t.replace(a, b)


rep("""/* tmcrit.c -- critical-polynomial roots on n x infinity bases by the eigenvalue method""",
    """/* tmcrit_stream.c -- tmcrit.c with the transfer structure streamed from disk (run 2026-10-16-1714).
 * Identical states, transitions, power method and root search; each step's transitions are written to three
 * files per sector during the build (per-state counts, targets, classes) and read back in the same order on every
 * sweep, so memory holds one step plus the vectors. The arithmetic order is unchanged, so the printed root must be
 * bit-identical to tmcrit.exe's (test_stream.py). Generated from tmcrit.c by make_stream.py.
 * usage: tmcrit_stream <program file> <site|bond> <p_lo> <p_hi> [tol] [scratch folder]
 *
 * Original header of tmcrit.c:
 * tmcrit.c -- critical-polynomial roots on n x infinity bases by the eigenvalue method""")

rep("""typedef struct {
    int64_t ns;           /* states at the start of this step */
    int64_t *rowptr;      /* ns+1 */
    int32_t *tgt;
    uint8_t *cls;         /* site: 1 occupied, 0 empty. bond: open | closed << 4 */
} trans_t;

static trans_t *T;
static int64_t nboundary;""",
    """typedef struct {
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
static void rd(void *p, size_t sz, size_t n, FILE *f) { if (n && fread(p, sz, n, f) != n) die("scratch read failed"); }""")

rep("""            T[k].rowptr = NULL; T[k].cls = NULL;
            T[k].tgt = malloc(sizeof(int32_t) * 2 * (ns > 0 ? ns : 1));
            if (!T[k].tgt) die("out of memory (transitions)");
            for (int64_t j = 0; j < ns; j++) {
                T[k].tgt[2 * j] = -1; T[k].tgt[2 * j + 1] = -1;
                decode(cur.keys + j * KW, steps[k].Fb, lab, off);
                int m = successors(k, lab, off, skeys, scls);
                for (int q = 0; q < m; q++) {
                    int32_t id = hs_find_or_add(&nxt, skeys + (int64_t)q * KW, !last);
                    if (id < 0) die("boundary set not closed");
                    T[k].tgt[2 * j + (scls[q] ? 0 : 1)] = id; used++;
                }
            }""",
    """            int32_t *tg = malloc(sizeof(int32_t) * 2 * (ns > 0 ? ns : 1));
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
            free(tg);""")

rep("""            T[k].rowptr = malloc(sizeof(int64_t) * (ns + 1));
            int64_t cap = ns * 2 + 16;
            T[k].tgt = malloc(sizeof(int32_t) * cap);
            T[k].cls = malloc(cap);
            for (int64_t j = 0; j < ns; j++) {
                T[k].rowptr[j] = used;
                decode(cur.keys + j * KW, steps[k].Fb, lab, off);
                int m = successors(k, lab, off, skeys, scls);
                for (int q = 0; q < m; q++) {
                    int32_t id = hs_find_or_add(&nxt, skeys + (int64_t)q * KW, !last);
                    if (id < 0) die("boundary set not closed");
                    if (used >= cap) {
                        cap *= 2;
                        T[k].tgt = realloc(T[k].tgt, sizeof(int32_t) * cap);
                        T[k].cls = realloc(T[k].cls, cap);
                        if (!T[k].tgt || !T[k].cls) die("out of memory (transitions)");
                    }
                    T[k].tgt[used] = id; T[k].cls[used] = scls[q]; used++;
                }
            }
            T[k].rowptr[ns] = used;""",
    """            uint16_t *cn = malloc(sizeof(uint16_t) * (ns > 0 ? ns : 1));
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
            free(cn); free(tg); free(cl);""")

rep("""        if (ns > maxs) maxs = ns;
        tot += used;""", """        T[k].used = used;
        if (ns > maxs) maxs = ns;
        tot += used;""")

rep("""static void free_T(void) {
    for (int k = 0; k < P; k++) { free(T[k].rowptr); free(T[k].tgt); free(T[k].cls); }
    free(T);
}""", """static void free_T(void) { free(T); }""")

rep("""    for (it = 1; it <= 20000; it++) {
        double *x = x0;
        int64_t nx = nboundary;
        for (int k = 0; k < P; k++) {
            int64_t ny = (k == P - 1) ? nboundary : T[k + 1].ns;
            double *y = (x == vec_a) ? vec_b : vec_a;
            memset(y, 0, sizeof(double) * ny);
            const int64_t *rp = T[k].rowptr; const int32_t *tg = T[k].tgt; const uint8_t *cl = T[k].cls;
            if (!bond_mode) {
                const double wo = wt[1], we = wt[0];
                for (int64_t j = 0; j < nx; j++) {
                    double v = x[j];
                    int32_t a = tg[2 * j], b = tg[2 * j + 1];
                    if (a >= 0) y[a] += wo * v;
                    if (b >= 0) y[b] += we * v;
                }
            } else {
                for (int64_t j = 0; j < nx; j++) {
                    double v = x[j];
                    if (v == 0) continue;
                    for (int64_t q = rp[j]; q < rp[j + 1]; q++) y[tg[q]] += wt[cl[q]] * v;
                }
            }
            x = y; nx = ny;
        }""",
    """    for (it = 1; it <= 20000; it++) {
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
        }""")

rep("""/* returns log Lambda per period; x0 (size nboundary) is the start vector and receives the eigenvector */""",
    """#define CH ((int64_t)1 << 20)       /* states per read chunk */
#define TCH ((int64_t)1 << 24)      /* transitions per read chunk (>= max successors per state) */
static int32_t *buf_tg; static uint8_t *buf_cl; static uint16_t *buf_cn;
static FILE *fc_cnt, *fc_tgt, *fc_cls, *fo_cnt, *fo_tgt, *fo_cls;
/* returns log Lambda per period; x0 (size nboundary) is the start vector and receives the eigenvector */""")

rep("""    double tol = argc > 5 ? atof(argv[5]) : 1e-15;""",
    """    double tol = argc > 5 ? atof(argv[5]) : 1e-15;
    if (argc > 6) scratch = argv[6];""")

rep("""    build(0, 1); Tc = T; nbc = nboundary;
    build(1, 1); To = T; nbo = nboundary;""",
    """    open_sector_files(0, "w+b"); build(0, 1); Tc = T; nbc = nboundary; fc_cnt = f_cnt; fc_tgt = f_tgt; fc_cls = f_cls;
    open_sector_files(1, "w+b"); build(1, 1); To = T; nbo = nboundary; fo_cnt = f_cnt; fo_tgt = f_tgt; fo_cls = f_cls;
    fflush(fc_cnt); fflush(fc_tgt); fflush(fc_cls); fflush(fo_cnt); fflush(fo_tgt); fflush(fo_cls);
    buf_tg = malloc(sizeof(int32_t) * (2 * CH > TCH ? 2 * CH : TCH)); buf_cl = malloc(TCH); buf_cn = malloc(sizeof(uint16_t) * CH);
    if (!buf_tg || !buf_cl || !buf_cn) die("out of memory (buffers)");""")

rep("""#define EVAL(p, out) do { T = Tc; nboundary = nbc; double lc = leading(p, xc, &itc, &rc); \\
        T = To; nboundary = nbo; double lo = leading(p, xo, &ito, &ro); out = lo - lc; \\""",
    """#define EVAL(p, out) do { T = Tc; nboundary = nbc; f_cnt = fc_cnt; f_tgt = fc_tgt; f_cls = fc_cls; \\
        double lc = leading(p, xc, &itc, &rc); \\
        T = To; nboundary = nbo; f_cnt = fo_cnt; f_tgt = fo_tgt; f_cls = fo_cls; \\
        double lo = leading(p, xo, &ito, &ro); out = lo - lc; \\""")

rep("""    T = Tc; free_T(); T = To; free_T();
    return 0;""",
    """    T = Tc; free_T(); T = To; free_T();
    fclose(fc_cnt); fclose(fc_tgt); fclose(fc_cls); fclose(fo_cnt); fclose(fo_tgt); fclose(fo_cls);
    for (int s2 = 0; s2 < 2; s2++) for (int i = 0; i < 3; i++) remove(fn_store[s2][i]);
    return 0;""")

rep("#include <time.h>\n", "#include <time.h>\n#include <process.h>\n")

open(os.path.join(HERE, "tmcrit_stream.c"), "w", encoding="utf-8", newline="\n").write(t)
print("tmcrit_stream.c written")
