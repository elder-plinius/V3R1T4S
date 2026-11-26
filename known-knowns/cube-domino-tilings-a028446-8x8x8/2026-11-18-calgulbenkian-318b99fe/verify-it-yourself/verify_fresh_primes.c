/*
 * verify_fresh_primes.c — Standalone Zero-Shared-Code Verifier (Part 2, C99)
 * Uses a third distinct vertex order — Order C: (5x + 4y + 5z, y - x, z, y, x) —
 * and a 6-bit 6-slice combinadic rank table (tbl6[6][35][64]) with fresh primes
 * disjoint from both Engine 1 (Prime Set A) and Engine 2 (Prime Set B).
 *
 * Verifies from scratch:
 *   1. A028446(1) = 9, A028446(2) = 5051532105, and A028446(3) = A049507(6) = 417898687046465734392674187695263185
 *   2. A049507(0..5) = 1, 6728, 53786626921, 57248060375968384, 123115692449982216049513, 216388579168758145017797108072
 *   3. A028454(1..7) (including both 4x4x6 and 6x4x4 orientations)
 *   4. Two fresh prime residues of A049507(7) = M(P_6 x P_6 x P_7) modulo p_fresh = 21713 and 21683
 *      checked against exact_perfect_matchings parsed directly from object/a049507_7_certificate.json!
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <sys/mman.h>

#define V_CAP 512
#define W_CAP 33
#define BUF_CAP 565722720ULL
#define N_FRESH 9
#define N_WORKERS 4

/* Fresh primes in [21611..21713] — zero overlap with Prime Set A or Prime Set B */
static const uint16_t FRESH_P[N_FRESH] = {
    21713, 21683, 21673, 21661, 21649, 21647, 21617, 21613, 21611
};

static uint64_t nCr[W_CAP + 3][W_CAP + 3];
static uint8_t  pop6[64];
static uint32_t tbl6[6][W_CAP + 3][64];
static uint16_t *mem_a = NULL;
static uint16_t *mem_b = NULL;

static void init_verifier(void) {
    memset(nCr, 0, sizeof(nCr));
    for (int n = 0; n <= W_CAP + 2; n++) {
        nCr[n][0] = 1ULL;
        for (int k = 1; k <= n; k++) nCr[n][k] = nCr[n - 1][k - 1] + nCr[n - 1][k];
    }
    for (int v = 0; v < 64; v++) pop6[v] = (uint8_t)__builtin_popcount((unsigned)v);
    for (int s = 0; s < 6; s++) {
        for (int cp = 0; cp <= W_CAP + 1; cp++) {
            for (int v = 0; v < 64; v++) {
                uint32_t r = 0;
                int k = cp + 1;
                int tmp = v;
                while (tmp) {
                    int b = __builtin_ctz((unsigned)tmp);
                    int bitpos = 6 * s + b;
                    if (bitpos <= W_CAP && k <= W_CAP) r += (uint32_t)nCr[bitpos][k];
                    k++;
                    tmp &= tmp - 1;
                }
                tbl6[s][cp][v] = r;
            }
        }
    }
    size_t bytes = (size_t)BUF_CAP * sizeof(uint16_t);
    mem_a = (uint16_t *)mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    mem_b = (uint16_t *)mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    if (mem_a == MAP_FAILED || mem_b == MAP_FAILED) {
        fprintf(stderr, "mmap failed\n");
        exit(1);
    }
}

static inline size_t rank6(uint32_t B) {
    uint8_t s0 = (uint8_t)(B & 63U);
    uint8_t s1 = (uint8_t)((B >> 6) & 63U);
    uint8_t s2 = (uint8_t)((B >> 12) & 63U);
    uint8_t s3 = (uint8_t)((B >> 18) & 63U);
    uint8_t s4 = (uint8_t)((B >> 24) & 63U);
    uint8_t s5 = (uint8_t)((B >> 30) & 63U);
    int c0 = pop6[s0];
    int c1 = c0 + pop6[s1];
    int c2 = c1 + pop6[s2];
    int c3 = c2 + pop6[s3];
    int c4 = c3 + pop6[s4];
    return (size_t)tbl6[0][0][s0]
         + (size_t)tbl6[1][c0][s1]
         + (size_t)tbl6[2][c1][s2]
         + (size_t)tbl6[3][c2][s3]
         + (size_t)tbl6[4][c3][s4]
         + (size_t)tbl6[5][c4][s5];
}

static uint64_t unrank6(int W, int K, size_t idx) {
    if (K == 0) return 0ULL;
    uint64_t m = 0ULL;
    int k = K;
    for (int b = W - 1; b >= 0 && k > 0; b--) {
        uint64_t c = nCr[b][k];
        if (idx >= c) { idx -= c; m |= (1ULL << b); k--; }
    }
    return m;
}

typedef struct { uint16_t *p; size_t a, b; } ClearSlice;
static void *clear_fn(void *arg) {
    ClearSlice *cs = (ClearSlice *)arg;
    if (cs->b > cs->a) memset(cs->p + cs->a, 0, (cs->b - cs->a) * sizeof(uint16_t));
    return NULL;
}
static void clear_buf(uint16_t *p, size_t n) {
    if (n < 262144) { memset(p, 0, n * sizeof(uint16_t)); return; }
    pthread_t th[N_WORKERS];
    ClearSlice cs[N_WORKERS];
    size_t ch = (n + N_WORKERS - 1) / N_WORKERS;
    int act = 0;
    for (int i = 0; i < N_WORKERS; i++) {
        size_t a = (size_t)i * ch, b = a + ch;
        if (b > n) b = n;
        if (a >= b) break;
        cs[i] = (ClearSlice){p, a, b};
        pthread_create(&th[i], NULL, clear_fn, &cs[i]);
        act++;
    }
    for (int i = 0; i < act; i++) pthread_join(th[i], NULL);
}

typedef struct {
    int W0, K0, W1, K1;
    uint64_t ev0, ev1, lmask;
    int ndrop, drops[6];
    int enters, nsnb, snb[6];
} StepC;

typedef struct {
    const uint16_t *src;
    uint16_t *dst;
    const StepC *st;
    uint16_t mod;
    size_t a, b;
} WorkC;

static inline uint64_t drop_bits(uint64_t x, int nd, const int *dr) {
    for (int i = 0; i < nd; i++) {
        int d = dr[i];
        uint64_t lo = (d == 0) ? 0ULL : ((1ULL << d) - 1ULL);
        x = (x & lo) | ((x >> 1) & ~lo);
    }
    return x;
}

static void *step_fn(void *arg) {
    WorkC *w = (WorkC *)arg;
    const uint16_t *src = w->src;
    uint16_t *dst = w->dst;
    const StepC *st = w->st;
    const uint16_t mod = w->mod;
    const uint16_t mod2 = (uint16_t)(2U * mod);
    size_t i = w->a, end = w->b;
    if (i >= end) return NULL;

    uint64_t sbits[6];
    for (int q = 0; q < st->nsnb; q++) sbits[q] = (1ULL << st->snb[q]);
    const uint64_t ebit = st->enters ? (1ULL << (st->W1 - 1)) : 0ULL;

    uint64_t B = unrank6(st->W0, st->K0, i);
    for (; i < end; i++) {
        uint16_t v = src[i];
        if (v != 0) {
            if (v >= mod2) v = (uint16_t)(v - mod2);
            if (v >= mod)  v = (uint16_t)(v - mod);
            if (v != 0) {
                uint64_t U = B ^ st->ev0;
                uint64_t ul = U & st->lmask;
                if (ul == 0ULL) {
                    uint64_t Uc = drop_bits(U, st->ndrop, st->drops);
                    if (st->enters) {
                        __atomic_fetch_add(&dst[rank6((uint32_t)((Uc | ebit) ^ st->ev1))], v, __ATOMIC_RELAXED);
                    }
                    for (int q = 0; q < st->nsnb; q++) {
                        if (Uc & sbits[q]) {
                            __atomic_fetch_add(&dst[rank6((uint32_t)((Uc ^ sbits[q]) ^ st->ev1))], v, __ATOMIC_RELAXED);
                        }
                    }
                } else if ((ul & (ul - 1ULL)) == 0ULL) {
                    uint64_t Uc = drop_bits(U ^ ul, st->ndrop, st->drops);
                    __atomic_fetch_add(&dst[rank6((uint32_t)(Uc ^ st->ev1))], v, __ATOMIC_RELAXED);
                }
            }
        }
        if (st->K0 > 0 && i + 1 < end) {
            int tz = __builtin_ctzll(B);
            uint64_t r = B + (1ULL << tz);
            B = (((r ^ B) >> (tz + 2))) | r;
        }
    }
    return NULL;
}

typedef struct { int x, y, z; } Pt3;
static int cmp_order_c(const void *pa, const void *pb) {
    const Pt3 *a = (const Pt3 *)pa, *b = (const Pt3 *)pb;
    int wa = 5 * a->x + 4 * a->y + 5 * a->z;
    int wb = 5 * b->x + 4 * b->y + 5 * b->z;
    if (wa != wb) return wa - wb;
    int da = a->y - a->x, db = b->y - b->x;
    if (da != db) return da - db;
    if (a->z != b->z) return a->z - b->z;
    if (a->y != b->y) return a->y - b->y;
    return a->x - b->x;
}

static uint16_t count_mod_order_c(int Lx, int Ly, int Lz, uint16_t mod) {
    int N = Lx * Ly * Lz;
    if (N == 0) return (uint16_t)(1U % mod);
    if (N & 1) return 0U;

    Pt3 pts[V_CAP];
    int idx_of[8][8][16];
    memset(idx_of, -1, sizeof(idx_of));
    int n = 0;
    for (int x = 0; x < Lx; x++)
        for (int y = 0; y < Ly; y++)
            for (int z = 0; z < Lz; z++)
                pts[n++] = (Pt3){x, y, z};
    qsort(pts, N, sizeof(Pt3), cmp_order_c);
    for (int i = 0; i < N; i++) idx_of[pts[i].x][pts[i].y][pts[i].z] = i;

    int deg[V_CAP], adj[V_CAP][6], last_nb[V_CAP];
    const int dx[6] = {-1, 1, 0, 0, 0, 0};
    const int dy[6] = {0, 0, -1, 1, 0, 0};
    const int dz[6] = {0, 0, 0, 0, -1, 1};
    for (int i = 0; i < N; i++) {
        int d = 0, mx = -1;
        for (int k = 0; k < 6; k++) {
            int nx = pts[i].x + dx[k], ny = pts[i].y + dy[k], nz = pts[i].z + dz[k];
            if (nx >= 0 && nx < Lx && ny >= 0 && ny < Ly && nz >= 0 && nz < Lz) {
                int j = idx_of[nx][ny][nz];
                adj[i][d++] = j;
                if (j > mx) mx = j;
            }
        }
        deg[i] = d;
        last_nb[i] = mx;
    }

    int F[W_CAP], W = 0, K = 0;
    uint64_t ev = 0ULL;
    int odd_c = 0, even_c = 0;
    uint16_t *src = mem_a, *dst = mem_b;
    src[0] = 1U;

    for (int t = 0; t < N; t++) {
        if ((pts[t].x + pts[t].y + pts[t].z) & 1) odd_c++; else even_c++;
        StepC st;
        memset(&st, 0, sizeof(st));
        st.W0 = W; st.K0 = K; st.ev0 = ev;

        int Fn[W_CAP], Wn = 0, dr_asc[6], nd = 0;
        for (int j = 0; j < W; j++) {
            int u = F[j];
            if (last_nb[u] > t) {
                int np = Wn;
                Fn[Wn++] = u;
                for (int k = 0; k < deg[t]; k++) {
                    if (adj[t][k] == u) { st.snb[st.nsnb++] = np; break; }
                }
            } else {
                st.lmask |= (1ULL << j);
                dr_asc[nd++] = j;
            }
        }
        if (nd + st.nsnb > 3) { fprintf(stderr, ">3 past nbs\n"); exit(1); }
        st.ndrop = nd;
        for (int i = 0; i < nd; i++) st.drops[i] = dr_asc[nd - 1 - i];
        st.enters = (last_nb[t] > t) ? 1 : 0;
        if (st.enters) Fn[Wn++] = t;

        int we = 0;
        uint64_t evn = 0ULL;
        for (int j = 0; j < Wn; j++) {
            int u = Fn[j];
            if (((pts[u].x + pts[u].y + pts[u].z) & 1) == 0) { we++; evn |= (1ULL << j); }
        }
        int Kn = (odd_c - even_c) + we;
        if (Kn < 0 || Kn > Wn) return 0U;
        st.W1 = Wn; st.K1 = Kn; st.ev1 = evn;

        size_t sz0 = (size_t)nCr[W][K];
        size_t sz1 = (size_t)nCr[Wn][Kn];
        clear_buf(dst, sz1);

        if (sz0 < 65536) {
            WorkC wc = {src, dst, &st, mod, 0, sz0};
            step_fn(&wc);
        } else {
            pthread_t th[N_WORKERS];
            WorkC wc[N_WORKERS];
            size_t ch = (sz0 + N_WORKERS - 1) / N_WORKERS;
            int act = 0;
            for (int i = 0; i < N_WORKERS; i++) {
                size_t a = (size_t)i * ch, b = a + ch;
                if (b > sz0) b = sz0;
                if (a >= b) break;
                wc[i] = (WorkC){src, dst, &st, mod, a, b};
                pthread_create(&th[i], NULL, step_fn, &wc[i]);
                act++;
            }
            for (int i = 0; i < act; i++) pthread_join(th[i], NULL);
        }

        uint16_t *tmp = src; src = dst; dst = tmp;
        memcpy(F, Fn, Wn * sizeof(int));
        W = Wn; K = Kn; ev = evn;
    }
    return src[0] % mod;
}

/* Reconstruct decimal string from k fresh primes */
static void crt_fresh_str(int k, const uint16_t *rems, char *out) {
    uint32_t d[32];
    memset(d, 0, sizeof(d));
    int dn = 1;
    d[0] = rems[0];

    uint32_t M[32];
    memset(M, 0, sizeof(M));
    int mn = 1;
    M[0] = FRESH_P[0] % 10000U;
    if (FRESH_P[0] >= 10000U) { M[1] = FRESH_P[0] / 10000U; mn = 2; }

    for (int i = 1; i < k; i++) {
        uint16_t p = FRESH_P[i];
        uint32_t xm = 0, mm = 0;
        for (int j = dn - 1; j >= 0; j--) xm = (xm * 10000U + d[j]) % p;
        for (int j = mn - 1; j >= 0; j--) mm = (mm * 10000U + M[j]) % p;
        uint32_t diff = (rems[i] >= xm) ? (rems[i] - xm) : (rems[i] + p - xm);
        uint32_t inv = 1, b = mm, e = p - 2;
        while (e > 0) { if (e & 1) inv = (inv * b) % p; b = (b * b) % p; e >>= 1; }
        uint32_t t = (diff * inv) % p;

        uint32_t c = 0;
        int lim = (dn > mn + 2) ? dn : (mn + 2);
        for (int j = 0; j < lim; j++) {
            uint32_t v = ((j < dn) ? d[j] : 0) + ((j < mn) ? M[j] : 0) * t + c;
            d[j] = v % 10000U;
            c = v / 10000U;
        }
        dn = lim;
        while (dn > 1 && d[dn - 1] == 0) dn--;

        c = 0;
        for (int j = 0; j < mn; j++) {
            uint32_t v = M[j] * p + c;
            M[j] = v % 10000U;
            c = v / 10000U;
        }
        while (c > 0) { M[mn++] = c % 10000U; c /= 10000U; }
    }
    int pos = sprintf(out, "%u", d[dn - 1]);
    for (int j = dn - 2; j >= 0; j--) pos += sprintf(out + pos, "%04u", d[j]);
}

static uint16_t dec_str_mod(const char *s, uint16_t m) {
    uint32_t r = 0;
    for (size_t i = 0; s[i]; i++) {
        if (s[i] < '0' || s[i] > '9') { fprintf(stderr, "non-digit in claimed value\n"); exit(1); }
        r = (r * 10U + (uint32_t)(s[i] - '0')) % m;
    }
    return (uint16_t)r;
}

/* Extract "exact_perfect_matchings": "<digits>" from object/a049507_7_certificate.json */
static void read_claimed_decimal(char *out, size_t cap) {
    FILE *f = fopen("object/a049507_7_certificate.json", "rb");
    if (!f) { fprintf(stderr, "cannot open certificate json\n"); exit(1); }
    char buf[16384];
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    fclose(f);
    buf[n] = '\0';
    const char *key = "\"exact_perfect_matchings\"";
    char *p = strstr(buf, key);
    if (!p) { fprintf(stderr, "missing exact_perfect_matchings key\n"); exit(1); }
    p = strchr(p + strlen(key), ':');
    if (!p) { fprintf(stderr, "malformed json\n"); exit(1); }
    p = strchr(p, '"');
    if (!p) { fprintf(stderr, "malformed value string\n"); exit(1); }
    p++;
    char *q = strchr(p, '"');
    if (!q || (size_t)(q - p) == 0 || (size_t)(q - p) >= cap) {
        fprintf(stderr, "invalid value string length\n");
        exit(1);
    }
    memcpy(out, p, (size_t)(q - p));
    out[q - p] = '\0';
}

int main(void) {
    init_verifier();
    char claimed[128];
    read_claimed_decimal(claimed, sizeof(claimed));

    struct { int x, y, z, np; const char *name, *exp; } checks[] = {
        {2, 2, 2, 1, "A028446(1) P_2xP_2xP_2", "9"},
        {4, 4, 4, 3, "A028446(2) P_4xP_4xP_4", "5051532105"},
        {4, 4, 1, 1, "A028454(1) P_4xP_4xP_1", "36"},
        {4, 4, 2, 2, "A028454(2) P_4xP_4xP_2", "32000"},
        {4, 4, 3, 2, "A028454(3) P_4xP_4xP_3", "10885344"},
        {4, 4, 5, 3, "A028454(5) P_4xP_4xP_5", "2132137503232"},
        {4, 4, 6, 4, "A028454(6) P_4xP_4xP_6", "932814464901633"},
        {6, 4, 4, 4, "A028454(6) P_6xP_4xP_4", "932814464901633"},
        {4, 4, 7, 5, "A028454(7) P_4xP_4xP_7", "403325499406267520"},
        {6, 6, 0, 1, "A049507(0) P_6xP_6xP_0", "1"},
        {6, 6, 1, 1, "A049507(1) P_6xP_6xP_1", "6728"},
        {6, 6, 2, 3, "A049507(2) P_6xP_6xP_2", "53786626921"},
        {6, 6, 3, 4, "A049507(3) P_6xP_6xP_3", "57248060375968384"},
        {6, 6, 4, 6, "A049507(4) P_6xP_6xP_4", "123115692449982216049513"},
        {6, 6, 5, 7, "A049507(5) P_6xP_6xP_5", "216388579168758145017797108072"},
        {6, 6, 6, 9, "A028446(3) = A049507(6) P_6xP_6xP_6", "417898687046465734392674187695263185"},
    };
    int n_chk = (int)(sizeof(checks) / sizeof(checks[0]));
    uint16_t rems[N_FRESH];
    char dec[128];
    for (int i = 0; i < n_chk; i++) {
        for (int j = 0; j < checks[i].np; j++) {
            rems[j] = count_mod_order_c(checks[i].x, checks[i].y, checks[i].z, FRESH_P[j]);
        }
        crt_fresh_str(checks[i].np, rems, dec);
        if (strcmp(dec, checks[i].exp) != 0) {
            printf("VERIFY ERROR: %s expected %s got %s\n", checks[i].name, checks[i].exp, dec);
            return 1;
        }
        printf("[OK] Order C reproduced %-36s = %s\n", checks[i].name, dec);
        fflush(stdout);
    }

    /* Fresh prime checks on 6x6x7 (p_fresh = 21713 and 21683, disjoint from Engine 1 and Engine 2) */
    for (int j = 0; j < 2; j++) {
        uint16_t p = FRESH_P[j];
        uint16_t actual_r = count_mod_order_c(6, 6, 7, p);
        uint16_t claimed_r = dec_str_mod(claimed, p);
        if (actual_r != claimed_r) {
            printf("VERIFY ERROR: fresh prime %u residue mismatch: recomputed=%u vs claimed=%u\n", p, actual_r, claimed_r);
            return 1;
        }
        printf("[OK] Order C fresh prime check M(P_6xP_6xP_7) mod %u == %u (matches claimed value)\n", p, actual_r);
        fflush(stdout);
    }
    return 0;
}
