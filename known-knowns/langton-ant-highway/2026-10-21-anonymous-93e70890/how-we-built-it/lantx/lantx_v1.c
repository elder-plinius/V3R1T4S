/* lantx.c — independent Langton's-ant highway checker (run 2026-10-20-2306).
 * Written from the spec in BRIEF.md/PREREG.md; does not reuse lant.c/lant2/lant4/ref code.
 * Convention: box W x H, bit b -> (b%W-(W-1)/2, b/W-(H-1)/2) black; ant at (0,0) heading 0 (north);
 * step: g=cell; h=(h+1+2g)&3; cell^=1; move by dir(h); dir 0:(0,+1) 1:(+1,0) 2:(0,-1) 3:(-1,0).
 * Certificate X (see PREREG.md): periodic heading stretch (h(u)==h(u-104)) from snapshot s0, B0 = bbox of
 * box + all cells visited up to s0, V0 = predicted period-0 cells, M = floor(min span/2),
 * K = least K>=M with bbox(V0)+K v strictly beyond B0 in a moving-away coordinate; certified once
 * periods 0..K are verified. T_cap = first s with h(u)==h(u-104) for all u >= s+104.
 * Modes:
 *   lantx range W H START END [CAP]          per-mask lines: mask tcap vx vy dir STATUS
 *   lantx list W H FILE [CAP]                masks (decimal, one per line) from FILE
 *   lantx plant W H MASK X Y [CAP]           extra black cell at (X,Y) (negative test)
 *   lantx sample PASS W NW OUTDIR            6x6, 1% hash sample pass PASS, chunks c = W, W+NW, ...
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define LG 13
#define S (1L << LG)
#define MARGIN 160
#define CERT_LIMIT 4000000L
static uint8_t *G;
static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {1, 0, -1, 0};

typedef struct { long tcap; int vx, vy, dir; int status; long steps; } res_t; /* status 0 CAP 1 UNCAP 2 OOB */

static res_t run(int W, int H, uint64_t mask, long cap, int px, int py, int plant) {
    res_t r = {-1, 0, 0, 0, 1, 0};
    const long c = S / 2;
    int ox = (W - 1) / 2, oy = (H - 1) / 2;
    int xmin = c - ox, xmax = c - ox + W - 1, ymin = c - oy, ymax = c - oy + H - 1; /* bbox of box */
    for (int b = 0; b < W * H; b++)
        if ((mask >> b) & 1) G[(long)(c + b / W - oy) * S + (c + b % W - ox)] = 1;
    if (plant) {
        long X = c + px, Y = c + py;
        G[Y * S + X] = 1;
        if (X < xmin) xmin = X; if (X > xmax) xmax = X; if (Y < ymin) ymin = Y; if (Y > ymax) ymax = Y;
    }
    long DP[4] = {S, 1, -S, -1};
    uint8_t R[104];
    R[0] = 0; for (int k = 1; k < 104; k++) R[k] = 4;
    int x = c, y = c, h = 0, ri = 0;
    long p = (long)c * S + c, t = 0, L = 0;
    long need = 208, Lsnap = -1;
    int vx = 0, vy = 0;
    int bad = 0;
    for (;;) {
        for (int k = 0; k < 64; k++) {
            int g = G[p];
            h = (h + 1 + 2 * g) & 3;
            G[p] = g ^ 1;
            p += DP[h]; x += DX[h]; y += DY[h];
            t++;
            if (++ri == 104) ri = 0;
            int old = R[ri]; R[ri] = h;           /* slot t%104 held h(t-104) */
            L = (old != h) ? t : L;
            xmin = x < xmin ? x : xmin; xmax = x > xmax ? x : xmax;
            ymin = y < ymin ? y : ymin; ymax = y > ymax ? y : ymax;
        }
        if (x < MARGIN || x >= S - MARGIN || y < MARGIN || y >= S - MARGIN) { r.status = 2; break; }
        if (t - L >= need) {
            if (Lsnap == L) { /* certified */
                long tc = L - 103; if (tc < 0) tc = 0;
                r.tcap = tc; r.vx = vx; r.vy = vy; r.dir = R[tc % 104];
                r.status = (tc <= cap) ? 0 : 1;
                break;
            }
            /* new snapshot at s0 = t: B0 = current bbox; replay predicted period 0 */
            long s0 = t;
            int bx0 = xmin, bx1 = xmax, by0 = ymin, by1 = ymax;
            int qx = x, qy = y, vx0 = x, vx1 = x, vy0 = y, vy1 = y;
            for (int j = 1; j <= 104; j++) {
                int hh = R[(s0 + j) % 104];
                qx += DX[hh]; qy += DY[hh];
                if (j < 104) {
                    if (qx < vx0) vx0 = qx; if (qx > vx1) vx1 = qx;
                    if (qy < vy0) vy0 = qy; if (qy > vy1) vy1 = qy;
                }
            }
            vx = qx - x; vy = qy - y;
            if (!((vx == 2 || vx == -2) && (vy == 2 || vy == -2))) { bad++; need = (t - L) + 104 * 8; Lsnap = -1; }
            else {
                int sx = vx1 - vx0, sy = vy1 - vy0;
                long M = (sx < sy ? sx : sy) / 2;
                long Kx = vx > 0 ? (bx1 - vx0) / 2 + 1 : (vx1 - bx0) / 2 + 1;
                long Ky = vy > 0 ? (by1 - vy0) / 2 + 1 : (vy1 - by0) / 2 + 1;
                if (Kx < 0) Kx = 0; if (Ky < 0) Ky = 0;
                long K = Kx < Ky ? Kx : Ky; if (K < M) K = M;
                need = (s0 + 104 * (K + 1)) - L;
                Lsnap = L;
            }
        } else if (Lsnap != L && Lsnap != -1) { Lsnap = -1; need = 208; }
        if (t > CERT_LIMIT || (t - 104 > cap && t - L < 208)) { r.status = 1; break; }
    }
    r.steps = t;
    for (long yy = ymin; yy <= ymax; yy++) memset(G + yy * S + xmin, 0, xmax - xmin + 1);
    (void)bad;
    return r;
}

static const char *ST[3] = {"CAP", "UNCAPTURED_WITHIN_CAP", "OUT_OF_BOUNDS"};
static void pr(uint64_t m, res_t r) {
    printf("%llu %ld %d %d %d %s\n", (unsigned long long)m, r.tcap, r.vx, r.vy, r.dir, ST[r.status]);
}
static uint64_t smix(uint64_t z) {
    z += 0x9E3779B97F4A7C15ULL;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
#define SEED 0x5EED20261020ULL

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    G = calloc(S * S, 1);
    if (!G) return 3;
    long cap = 2000000;
    if (!strcmp(argv[1], "range")) {
        int W = atoi(argv[2]), H = atoi(argv[3]);
        uint64_t a = strtoull(argv[4], 0, 10), b = strtoull(argv[5], 0, 10);
        if (argc > 6) cap = atol(argv[6]);
        for (uint64_t m = a; m < b; m++) pr(m, run(W, H, m, cap, 0, 0, 0));
    } else if (!strcmp(argv[1], "list")) {
        int W = atoi(argv[2]), H = atoi(argv[3]);
        if (argc > 5) cap = atol(argv[5]);
        FILE *f = fopen(argv[4], "r"); unsigned long long m;
        while (fscanf(f, "%llu", &m) == 1) pr(m, run(W, H, m, cap, 0, 0, 0));
    } else if (!strcmp(argv[1], "plant")) {
        int W = atoi(argv[2]), H = atoi(argv[3]);
        uint64_t m = strtoull(argv[4], 0, 10);
        int X = atoi(argv[5]), Y = atoi(argv[6]);
        if (argc > 7) cap = atol(argv[7]);
        res_t r = run(W, H, m, cap, X, Y, 1);
        pr(m, r); printf("steps %ld\n", r.steps);
    } else if (!strcmp(argv[1], "sample")) {
        int pass = atoi(argv[2]), w = atoi(argv[3]), nw = atoi(argv[4]);
        const char *od = argv[5];
        char fn[512], tmp[512], stopf[512];
        snprintf(stopf, sizeof stopf, "%s/STOP", od);
        for (int ch = w; ch < 4096; ch += nw) {
            snprintf(fn, sizeof fn, "%s/p%d_c%04d.sum", od, pass, ch);
            struct stat st;
            if (stat(fn, &st) == 0) continue;
            if (stat(stopf, &st) == 0) return 0;
            uint64_t m0 = (uint64_t)ch << 24, m1 = m0 + (1ULL << 24);
            long n = 0, ncap = 0, nunc = 0, noob = 0, maxt = -1, sumt = 0, steps = 0;
            uint64_t maxm = 0, hx = 0;
            snprintf(tmp, sizeof tmp, "%s/p%d_c%04d.noncap.tmp", od, pass, ch);
            FILE *nf = NULL;
            for (uint64_t m = m0; m < m1; m++) {
                uint64_t rr = smix(m + SEED) % 10000;
                if (rr >= 100 || (int)(rr / 25) != pass) continue;
                res_t r = run(6, 6, m, cap, 0, 0, 0);
                n++; steps += r.steps;
                if (r.status == 0) {
                    ncap++; sumt += r.tcap;
                    if (r.tcap > maxt) { maxt = r.tcap; maxm = m; }
                    hx ^= smix(m ^ ((uint64_t)r.tcap << 36) ^ ((uint64_t)(r.vx + 2) << 60) ^ ((uint64_t)(r.vy + 2) << 57) ^ ((uint64_t)r.dir << 54));
                } else {
                    if (r.status == 1) nunc++; else noob++;
                    if (!nf) nf = fopen(tmp, "w");
                    fprintf(nf, "%llu %ld %d %d %d %s %ld\n", (unsigned long long)m, r.tcap, r.vx, r.vy, r.dir, ST[r.status], r.steps);
                }
            }
            if (nf) { fclose(nf); char nn[512]; snprintf(nn, sizeof nn, "%s/p%d_c%04d.noncap", od, pass, ch); rename(tmp, nn); }
            snprintf(tmp, sizeof tmp, "%s/p%d_c%04d.sum.tmp", od, pass, ch);
            FILE *o = fopen(tmp, "w");
            fprintf(o, "pass %d chunk %d n %ld CAP %ld UNCAP %ld OOB %ld maxtcap %ld maxtcap_mask %llu sumtcap %ld steps %ld linehash %016llx\n",
                    pass, ch, n, ncap, nunc, noob, maxt, (unsigned long long)maxm, sumt, steps, (unsigned long long)hx);
            fclose(o);
            rename(tmp, fn);
        }
    } else return 2;
    return 0;
}
