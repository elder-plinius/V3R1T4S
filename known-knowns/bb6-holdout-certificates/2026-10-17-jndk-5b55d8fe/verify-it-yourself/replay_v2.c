/* V3R1T4S lens "replay": naive single-step replay of a TM from the blank tape,
 * checking every application of seven hand-transcribed macro rules.
 *
 * Usage:
 *   replay sim  <machine> <maxsteps>          -- plain simulation (validation)
 *   replay rules <horizon> <mut>               -- rule replay on 1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB
 *        mut = 0 none, 1 = every rule steps+1, 2 = flip last output cell of every rule
 *
 * Conventions: time T = number of defined transitions done. A transition on an
 * undefined entry ('---') is a halt and is NOT counted.
 * Rule patterns are transcribed by hand from result/rules.json (see comments per rule).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NT (1 << 22)          /* tape cells */
#define ORG (NT / 2)          /* origin index */
#define MARGIN 65536

static uint8_t *T;            /* tape */
typedef struct { int ns; uint8_t w[8][2]; int8_t mv[8][2]; int8_t nx[8][2]; } TM;

static int parse(const char *s, TM *m) {
    int st = 0, i = 0;
    while (1) {
        for (int b = 0; b < 2; b++) {
            const char *p = s + i;
            if (p[0] == '-' ) { m->nx[st][b] = -1; m->w[st][b] = 0; m->mv[st][b] = 0; }
            else {
                m->w[st][b] = (uint8_t)(p[0] - '0');
                m->mv[st][b] = (p[1] == 'R') ? 1 : -1;
                m->nx[st][b] = (int8_t)(p[2] - 'A');
                if (p[1] != 'R' && p[1] != 'L') { fprintf(stderr, "bad move\n"); exit(2); }
            }
            i += 3;
        }
        st++;
        if (s[i] == '_') i++;
        else if (s[i] == 0) break;
        else { fprintf(stderr, "parse error at %d\n", i); exit(2); }
    }
    m->ns = st;
    return st;
}

static void bounds(int64_t h, int64_t t) {
    if (h < MARGIN || h > NT - MARGIN) {
        fprintf(stderr, "TAPE OVERFLOW: head index %lld at time %lld\n", (long long)h, (long long)t);
        printf("TAPE OVERFLOW: head index %lld at time %lld\n", (long long)h, (long long)t);
        exit(3);
    }
}

/* ------------------------------------------------------------------ sim mode */
static int run_sim(const char *mach, int64_t maxs) {
    TM m; parse(mach, &m);
    memset(T, 0, NT);
    int64_t h = ORG, t = 0, lo = h, hi = h; int s = 0;
    while (t < maxs) {
        uint8_t b = T[h];
        if (m.nx[s][b] < 0) break;
        T[h] = m.w[s][b]; h += m.mv[s][b]; s = m.nx[s][b]; t++;
        if (h < lo) lo = h;
        if (h > hi) hi = h;
        if ((t & 0xFFFFF) == 0) bounds(h, t);
    }
    bounds(h, t);
    int halted = (t < maxs) || (m.nx[s][T[h]] < 0);
    int64_t ones = 0; for (int64_t i = 0; i < NT; i++) ones += T[i];
    printf("machine %s\n", mach);
    printf("halted=%d defined_transitions=%lld ones_on_tape=%lld halting_state=%c read=%d head_range=[%lld,%lld]\n",
           halted, (long long)t, (long long)ones, 'A' + s, T[h], (long long)(lo - ORG), (long long)(hi - ORG));
    return 0;
}

/* ---------------------------------------------------------------- rule mode */
enum { R_EVEN, R_ODD, R_EODD, R_EDRAIN, R_DSTEP, R_DD1, R_DD3, NR };
static const char *RN[NR] = {"even", "odd", "Eodd", "even_drain", "Dstep", "Ddrain1", "Ddrain3"};
static int MUT = 0;

static int64_t rule_steps(int r, int64_t k) {
    int64_t s = 0;
    switch (r) {
    case R_EVEN:   s = 12 * k - 3; break;
    case R_ODD:    s = 12 * k + 5; break;
    case R_EODD:   s = 24 * k + 7; break;
    case R_EDRAIN: s = 6 * k * k + 3 * k; break;
    case R_DSTEP:  s = 12 * k + 13; break;
    case R_DD1:    s = 12 * k * k + 13 * k; break;
    case R_DD3:    s = 12 * k * k + 25 * k; break;
    }
    if (MUT == 1) s += 1;
    return s;
}

/* builder helpers */
static int bp;
static uint8_t *B;
static void put(int bit, int64_t n) { for (int64_t i = 0; i < n; i++) B[bp++] = (uint8_t)bit; }

/* Build expected output window; returns length; *hoff = head offset from L. */
static int build_out(int r, int64_t k, int x, int *hoff) {
    bp = 0;
    switch (r) {
    case R_EVEN:   /* A x 1^(2k-2) 00 111 */
        *hoff = 0; put(x, 1); put(1, 2 * k - 2); put(0, 2); put(1, 3); break;
    case R_ODD:    /* A x10 1^(2k-1) 00 111 */
        *hoff = 0; put(x, 1); put(1, 1); put(0, 1); put(1, 2 * k - 1); put(0, 2); put(1, 3); break;
    case R_EODD:   /* A x10 1^(2k-1) 00 1^6 */
        *hoff = 0; put(x, 1); put(1, 1); put(0, 1); put(1, 2 * k - 1); put(0, 2); put(1, 6); break;
    case R_EDRAIN: /* A000 1^(3k) */
        *hoff = 0; put(0, 3); put(1, 3 * k); break;
    case R_DSTEP:  /* 1 A010 1^(2k-1) 00 111 */
        *hoff = 1; put(1, 1); put(0, 1); put(1, 1); put(0, 1); put(1, 2 * k - 1); put(0, 2); put(1, 3); break;
    case R_DD1:    /* 1^k A0101 00 1^(3k) */
        *hoff = (int)k; put(1, k); put(0, 1); put(1, 1); put(0, 1); put(1, 1); put(0, 2); put(1, 3 * k); break;
    case R_DD3:    /* 1^k A010 1^3 00 1^(3k) */
        *hoff = (int)k; put(1, k); put(0, 1); put(1, 1); put(0, 1); put(1, 3); put(0, 2); put(1, 3 * k); break;
    }
    if (MUT == 2) B[bp - 1] ^= 1;
    return bp;
}

static inline int64_t run1(int64_t p) { /* length of the run of 1s starting at p */
    const uint8_t *q = memchr(T + p, 0, NT - p);
    if (!q) { printf("RUN OVERFLOW at %lld\n", (long long)p); exit(3); }
    return q - (T + p);
}

typedef struct {
    int64_t start, due, k;
    int32_t L, R, h0;
    uint8_t rule, x, status; /* status: 0 free, 1 active, 2 escaped (await heap pop) */
} Chk;

static Chk *C; static int64_t ncap = 0, nused = 0; static int64_t *freel; static int64_t nfree = 0;
typedef struct { int64_t due; int64_t id; } HE;
static HE *H; static int64_t hn = 0, hcap = 0;
static int32_t *bad;

static int64_t st_sched[NR], st_pass[NR], st_fesc[NR], st_fstate[NR], st_fhead[NR], st_fwin[NR], st_pend[NR],
    st_triv[NR], st_maxk[NR], st_maxkpass[NR];
static int printed_fail[NR];
static int64_t maxactive = 0, nactive = 0;

static void hpush(int64_t due, int64_t id) {
    if (hn == hcap) { hcap = hcap ? hcap * 2 : 1 << 16; H = realloc(H, hcap * sizeof(HE)); if (!H) exit(4); }
    int64_t i = hn++;
    while (i > 0) { int64_t p = (i - 1) / 2; if (H[p].due <= due) break; H[i] = H[p]; i = p; }
    H[i].due = due; H[i].id = id;
}
static HE hpop(void) {
    HE top = H[0], last = H[--hn]; int64_t i = 0;
    while (1) {
        int64_t c = 2 * i + 1; if (c >= hn) break;
        if (c + 1 < hn && H[c + 1].due < H[c].due) c++;
        if (H[c].due >= last.due) break;
        H[i] = H[c]; i = c;
    }
    if (hn > 0) H[i] = last;
    return top;
}
static int64_t alloc_chk(void) {
    if (nfree) return freel[--nfree];
    if (nused == ncap) {
        ncap = ncap ? ncap * 2 : 1 << 16;
        C = realloc(C, ncap * sizeof(Chk)); freel = realloc(freel, ncap * sizeof(int64_t));
        if (!C || !freel) exit(4);
    }
    return nused++;
}

static void print_window(const char *lab, const uint8_t *w, int n) {
    printf("    %s ", lab);
    for (int i = 0; i < n; i++) putchar('0' + w[i]);
    putchar('\n');
}

static void report_fail(Chk *c, const char *why, int64_t t, int64_t head, int state) {
    int r = c->rule;
    if (printed_fail[r] >= 3) return;
    printed_fail[r]++;
    int hoff; int n = build_out(r, c->k, c->x, &hoff);
    printf("FAIL rule=%s k=%lld x=%d reason=%s start=%lld due=%lld now=%lld window=[%d,%d] (rel. origin [%d,%d]) "
           "h0=%d expected_head=%d actual_head=%lld actual_state=%c\n",
           RN[r], (long long)c->k, c->x, why, (long long)c->start, (long long)c->due, (long long)t,
           c->L, c->R, c->L - ORG, c->R - ORG, c->h0 - ORG, c->L + hoff - ORG, (long long)(head - ORG), 'A' + state);
    print_window("expected:", B, n);
    print_window("actual:  ", T + c->L, c->R - c->L + 1);
}

static void schedule(int r, int64_t k, int x, int64_t L, int64_t R, int64_t h, int64_t t) {
    int hoff; int n = build_out(r, k, x, &hoff);
    if (n != R - L + 1) { printf("INTERNAL: window length mismatch rule %s k=%lld in=%lld out=%d\n", RN[r], (long long)k, (long long)(R - L + 1), n); exit(5); }
    int64_t id = alloc_chk(); Chk *c = &C[id];
    c->start = t; c->due = t + rule_steps(r, k); c->k = k; c->L = (int32_t)L; c->R = (int32_t)R; c->h0 = (int32_t)h;
    c->rule = (uint8_t)r; c->x = (uint8_t)x; c->status = 1;
    bad[L - 1]++; bad[R + 1]++;
    st_sched[r]++; if (k > st_maxk[r]) st_maxk[r] = k;
    if (c->due == t) st_triv[r]++;
    nactive++; if (nactive > maxactive) maxactive = nactive;
    hpush(c->due, id);
}

static void match_all(int64_t h, int64_t t) {
    if (T[h] != 0) return;              /* every rule's scanned cell is 0 */
    int64_t r;
    /* even: x A0 1^(2k) 00, k>=1.  cells: h-1=x, h=0, h+1..h+2k=1, h+2k+1=0, h+2k+2=0 */
    /* even_drain: 0^k A0 1^(2k) 00, k>=0 */
    r = run1(h + 1);
    if ((r % 2) == 0 && T[h + r + 1] == 0 && T[h + r + 2] == 0) {
        int64_t k = r / 2;
        if (k >= 1) schedule(R_EVEN, k, T[h - 1], h - 1, h + r + 2, h, t);
        int ok = 1;
        for (int64_t i = 1; i <= k; i++) if (T[h - i] != 0) { ok = 0; break; }
        if (ok) schedule(R_EDRAIN, k, 0, h - k, h + r + 2, h, t);
    }
    /* odd: x00 A0 1^(2k+1) 00, k>=1.  h-3=x, h-2=0, h-1=0, h=0, h+1..h+2k+1=1, then 00 */
    if (r >= 3 && (r % 2) == 1 && T[h - 1] == 0 && T[h - 2] == 0 && T[h + r + 1] == 0 && T[h + r + 2] == 0)
        schedule(R_ODD, (r - 1) / 2, T[h - 3], h - 3, h + r + 2, h, t);
    /* Eodd: x00 A0110 1^(2k+1) 00, k>=1.  h-3=x,h-2=0,h-1=0,h=0,h+1=1,h+2=1,h+3=0, h+4..h+4+2k =1, then 00 */
    if (T[h - 1] == 0 && T[h - 2] == 0 && T[h + 1] == 1 && T[h + 2] == 1 && T[h + 3] == 0) {
        int64_t q = run1(h + 4);
        if (q >= 3 && (q % 2) == 1 && T[h + 4 + q] == 0 && T[h + 5 + q] == 0)
            schedule(R_EODD, (q - 1) / 2, T[h - 3], h - 3, h + 5 + q, h, t);
    }
    /* D family: A010 1^m 00.  h=0,h+1=1,h+2=0, h+3..h+2+m=1, h+3+m=0, h+4+m=0 */
    if (T[h + 1] == 1 && T[h + 2] == 0) {
        int64_t m = run1(h + 3);
        if (T[h + 3 + m] == 0 && T[h + 4 + m] == 0) {
            if (m >= 5 && (m % 2) == 1) schedule(R_DSTEP, (m - 3) / 2, 0, h, h + 4 + m, h, t); /* m=2k+3 */
            if (m >= 1 && (m % 4) == 1) schedule(R_DD1, (m - 1) / 4, 0, h, h + 4 + m, h, t);   /* m=4k+1 */
            if (m >= 3 && (m % 4) == 3) schedule(R_DD3, (m - 3) / 4, 0, h, h + 4 + m, h, t);   /* m=4k+3 */
        }
    }
}

static void free_chk(int64_t id, Chk *c) {
    c->status = 0; freel[nfree++] = id;
}
static void deactivate(Chk *c) { bad[c->L - 1]--; bad[c->R + 1]--; nactive--; }

static int64_t SCHED_UNTIL = 100000000LL; /* v2: schedule only starts <= 1e8; run on until all resolve */
static int run_rules(int64_t horizon) {
    TM m; parse("1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB", &m);
    memset(T, 0, NT);
    bad = calloc(NT, sizeof(int32_t)); B = malloc(NT);
    int64_t h = ORG, t = 0, lo = h, hi = h; int s = 0; int halted = 0;
    printf("replay horizon=%lld mut=%d\n", (long long)horizon, MUT); fflush(stdout);
    while (1) {
        /* (1) context check: head must be inside every active window */
        if (bad[h] > 0) {
            for (int64_t i = 0; i < nused; i++) {
                Chk *c = &C[i];
                if (c->status == 1 && (h < c->L || h > c->R)) {
                    report_fail(c, "head_left_window", t, h, s);
                    st_fesc[c->rule]++; deactivate(c); c->status = 2;
                }
            }
        }
        /* (2) resolve due checks */
        while (hn > 0 && H[0].due == t) {
            HE e = hpop(); Chk *c = &C[e.id];
            if (c->status == 2) { free_chk(e.id, c); continue; }
            int hoff; int n = build_out(c->rule, c->k, c->x, &hoff);
            int r = c->rule;
            if (s != 0) { report_fail(c, "state_not_A", t, h, s); st_fstate[r]++; }
            else if (h != c->L + hoff) { report_fail(c, "head_position", t, h, s); st_fhead[r]++; }
            else if (memcmp(T + c->L, B, n) != 0) { report_fail(c, "window_mismatch", t, h, s); st_fwin[r]++; }
            else { st_pass[r]++; if (c->k > st_maxkpass[r]) st_maxkpass[r] = c->k; }
            deactivate(c); free_chk(e.id, c);
        }
        /* (3) new applications */
        if (s == 0 && t <= SCHED_UNTIL) {
            match_all(h, t);
            /* zero-step applications resolve immediately */
            while (hn > 0 && H[0].due == t) {
                HE e = hpop(); Chk *c = &C[e.id];
                int hoff; int n = build_out(c->rule, c->k, c->x, &hoff);
                int r = c->rule;
                if (h != c->L + hoff) { report_fail(c, "head_position", t, h, s); st_fhead[r]++; }
                else if (memcmp(T + c->L, B, n) != 0) { report_fail(c, "window_mismatch", t, h, s); st_fwin[r]++; }
                else { st_pass[r]++; if (c->k > st_maxkpass[r]) st_maxkpass[r] = c->k; }
                deactivate(c); free_chk(e.id, c);
            }
        }
        if (t >= SCHED_UNTIL && hn == 0) break;
        if (t == horizon) break;
        /* (4) one naive step */
        uint8_t b = T[h];
        if (m.nx[s][b] < 0) { halted = 1; break; }
        T[h] = m.w[s][b]; h += m.mv[s][b]; s = m.nx[s][b]; t++;
        if (h < lo) { lo = h; bounds(h, t); }
        if (h > hi) { hi = h; bounds(h, t); }
        if (t % 10000000 == 0) {
            printf("progress t=%lld head=%lld state=%c head_range=[%lld,%lld] active=%lld maxactive=%lld\n",
                   (long long)t, (long long)(h - ORG), 'A' + s, (long long)(lo - ORG), (long long)(hi - ORG),
                   (long long)nactive, (long long)maxactive);
            fflush(stdout);
        }
    }
    for (int64_t i = 0; i < nused; i++) if (C[i].status == 1) st_pend[C[i].rule]++;
    printf("END t=%lld halted=%d state=%c head=%lld head_range=[%lld,%lld] maxactive=%lld\n", (long long)t, halted,
           'A' + s, (long long)(h - ORG), (long long)(lo - ORG), (long long)(hi - ORG), (long long)maxactive);
    printf("%-11s %10s %10s %8s %8s %8s %8s %8s %10s %8s %8s %10s\n", "rule", "scheduled", "passed", "f_escape",
           "f_state", "f_head", "f_window", "f_total", "pending", "trivial0", "max_k", "max_k_pass");
    int64_t tf = 0, tp = 0, ts = 0;
    for (int r = 0; r < NR; r++) {
        int64_t f = st_fesc[r] + st_fstate[r] + st_fhead[r] + st_fwin[r];
        tf += f; tp += st_pass[r]; ts += st_sched[r];
        printf("%-11s %10lld %10lld %8lld %8lld %8lld %8lld %8lld %10lld %8lld %8lld %10lld\n", RN[r],
               (long long)st_sched[r], (long long)st_pass[r], (long long)st_fesc[r], (long long)st_fstate[r],
               (long long)st_fhead[r], (long long)st_fwin[r], (long long)f, (long long)st_pend[r],
               (long long)st_triv[r], (long long)st_maxk[r], (long long)st_maxkpass[r]);
    }
    printf("TOTAL scheduled=%lld passed=%lld failures=%lld\n", (long long)ts, (long long)tp, (long long)tf);
    return 0;
}

int main(int argc, char **argv) {
    T = calloc(NT, 1);
    if (!T) return 4;
    if (argc >= 4 && !strcmp(argv[1], "sim")) return run_sim(argv[2], atoll(argv[3]));
    if (argc >= 4 && !strcmp(argv[1], "rules")) { MUT = atoi(argv[3]); return run_rules(atoll(argv[2])); }
    fprintf(stderr, "usage: replay sim <machine> <maxsteps> | replay rules <horizon> <mut>\n");
    return 1;
}
