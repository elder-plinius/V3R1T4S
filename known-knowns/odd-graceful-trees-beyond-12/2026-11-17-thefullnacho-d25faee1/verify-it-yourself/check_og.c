/* check_og.c — standalone checker for an odd-graceful tree certificate.
 *
 * Written from the definition (Gnanajothi 1991): a graph with q edges is
 * odd-graceful if there is an injection f: V -> {0,1,...,2q-1} such that the
 * edge labels |f(u)-f(v)| are exactly {1,3,...,2q-1}.
 *
 * Line format: n;u-v,u-v,...;l0,l1,...[;ignored]
 * For each line this program checks that the graph is a tree on vertices
 * {0,...,n-1}, that the labels are injective in {0,...,2q-1}, and that the
 * edge differences are exactly the q odd numbers below 2q. Trees are then
 * reduced by the AHU canonical form of an unrooted tree (one centre: the
 * rooted AHU string; two centres: the sorted pair of the two sides) and
 * stored as SHA-256 truncated to 128 bits; a duplicate form is a failure.
 * The number of lines, valid unique labelings and distinct forms must all
 * equal A000055(n) (built-in through n = 24, or --expect).
 *
 * Build:  cc -O2 -std=c11 -Wall -Wextra -o check_og check_og.c
 * Usage:  ./check_og --selftest
 *         ./check_og [--n N] [--expect K] FILE
 *         gzip -dc cert.txt.gz | ./check_og --n 23 --expect 14828074
 * Last line of a successful run: PASS
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

#define MAXN 32
#define MAXLINE 8192

static const long long A000055[25] = {
    1,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320,48629,
    123867,317955,823065,2144505,5623756,14828074,39299897
};

/* ---- SHA-256 (FIPS 180-4), compact ---- */
static const uint32_t K256[64] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
};
static uint32_t rotr(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
static void sha256(const unsigned char *msg, size_t len, unsigned char out[32]) {
    uint32_t h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    unsigned char block[64];
    size_t i, nblocks;
    uint64_t bitlen = (uint64_t)len * 8;
    /* one-shot: pad into a temporary buffer large enough for our AHU strings */
    size_t pad = 1 + ((55 - (len % 64)) + 64) % 64;
    size_t tot = len + pad + 8;
    unsigned char *buf = (unsigned char *)malloc(tot);
    if (!buf) { fprintf(stderr, "out of memory\n"); exit(2); }
    memcpy(buf, msg, len);
    buf[len] = 0x80;
    memset(buf + len + 1, 0, pad - 1);
    for (i = 0; i < 8; i++) buf[tot - 1 - i] = (unsigned char)(bitlen >> (8 * i));
    nblocks = tot / 64;
    for (i = 0; i < nblocks; i++) {
        uint32_t w[64], a, b, c, d, e, f, g, hh, t1, t2;
        int t;
        memcpy(block, buf + i * 64, 64);
        for (t = 0; t < 16; t++)
            w[t] = ((uint32_t)block[4*t]<<24)|((uint32_t)block[4*t+1]<<16)|((uint32_t)block[4*t+2]<<8)|block[4*t+3];
        for (t = 16; t < 64; t++) {
            uint32_t s0 = rotr(w[t-15],7)^rotr(w[t-15],18)^(w[t-15]>>3);
            uint32_t s1 = rotr(w[t-2],17)^rotr(w[t-2],19)^(w[t-2]>>10);
            w[t] = w[t-16] + s0 + w[t-7] + s1;
        }
        a=h[0]; b=h[1]; c=h[2]; d=h[3]; e=h[4]; f=h[5]; g=h[6]; hh=h[7];
        for (t = 0; t < 64; t++) {
            t1 = hh + (rotr(e,6)^rotr(e,11)^rotr(e,25)) + ((e&f)^((~e)&g)) + K256[t] + w[t];
            t2 = (rotr(a,2)^rotr(a,13)^rotr(a,22)) + ((a&b)^(a&c)^(b&c));
            hh=g; g=f; f=e; e=d+t1; d=c; c=b; b=a; a=t1+t2;
        }
        h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d; h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }
    free(buf);
    for (i = 0; i < 8; i++) {
        out[4*i]   = (unsigned char)(h[i] >> 24);
        out[4*i+1] = (unsigned char)(h[i] >> 16);
        out[4*i+2] = (unsigned char)(h[i] >> 8);
        out[4*i+3] = (unsigned char)h[i];
    }
}

/* ---- open-addressing set of 16-byte keys ---- */
typedef struct { unsigned char *slots; uint8_t *used; size_t cap, n; } HashSet;
static HashSet H;

static int set_init(size_t expect) {
    size_t cap = 16;
    while (cap < expect * 2 + 16) cap <<= 1;
    H.slots = (unsigned char *)calloc(cap, 16);
    H.used  = (uint8_t *)calloc(cap, 1);
    H.cap = cap; H.n = 0;
    return H.slots && H.used;
}
static void set_free(void) { free(H.slots); free(H.used); H.slots = 0; H.used = 0; H.cap = H.n = 0; }
static size_t key_index(const unsigned char k[16]) {
    /* first 8 bytes as little-endian-ish hash */
    uint64_t x = 0; int i;
    for (i = 0; i < 8; i++) x |= (uint64_t)k[i] << (8 * i);
    return (size_t)(x & (H.cap - 1));
}
/* returns 1 if newly inserted, 0 if already present */
static int set_insert(const unsigned char k[16]) {
    size_t i = key_index(k), start = i, probed = 0;
    for (;;) {
        if (!H.used[i]) {
            memcpy(H.slots + i * 16, k, 16);
            H.used[i] = 1;
            H.n++;
            return 1;
        }
        if (memcmp(H.slots + i * 16, k, 16) == 0) return 0;
        i = (i + 1) & (H.cap - 1);
        if (++probed >= H.cap || i == start) {
            fprintf(stderr, "hash table full (%zu keys, cap %zu); raise --expect\n", H.n, H.cap);
            exit(2);
        }
    }
}

/* ---- tree + AHU ---- */
static int nglob, qglob, deg[MAXN], adj[MAXN][MAXN];
static char ahu_buf[4096];
static int ahu_len;

static void ahu_rec(int v, int p) {
    char *child[MAXN];
    int clen[MAXN], nc = 0, i, j;
    ahu_buf[ahu_len++] = '(';
    for (i = 0; i < deg[v]; i++) if (adj[v][i] != p) {
        int start = ahu_len;
        ahu_rec(adj[v][i], v);
        clen[nc] = ahu_len - start;
        child[nc] = (char *)malloc((size_t)clen[nc]);
        if (!child[nc]) { fprintf(stderr, "out of memory\n"); exit(2); }
        memcpy(child[nc], ahu_buf + start, (size_t)clen[nc]);
        ahu_len = start;
        nc++;
    }
    /* sort child strings */
    for (i = 0; i < nc; i++)
        for (j = i + 1; j < nc; j++) {
            int c, L = clen[i] < clen[j] ? clen[i] : clen[j];
            c = memcmp(child[i], child[j], (size_t)L);
            if (c > 0 || (c == 0 && clen[i] > clen[j])) {
                char *tmp = child[i]; int tl = clen[i];
                child[i] = child[j]; clen[i] = clen[j];
                child[j] = tmp; clen[j] = tl;
            }
        }
    for (i = 0; i < nc; i++) {
        memcpy(ahu_buf + ahu_len, child[i], (size_t)clen[i]);
        ahu_len += clen[i];
        free(child[i]);
    }
    ahu_buf[ahu_len++] = ')';
}

static int find_centres(int *c1, int *c2) {
    int d[MAXN], leaf[MAXN], nleaf = 0, remain = nglob, i, j, v;
    for (i = 0; i < nglob; i++) {
        d[i] = deg[i];
        if (d[i] <= 1) leaf[nleaf++] = i;
    }
    if (nglob <= 2) { *c1 = 0; *c2 = (nglob == 2 ? 1 : -1); return nglob == 2 ? 2 : 1; }
    while (remain > 2) {
        int newleaf[MAXN], nn = 0;
        remain -= nleaf;
        for (i = 0; i < nleaf; i++) {
            v = leaf[i];
            for (j = 0; j < deg[v]; j++) {
                int u = adj[v][j];
                if (--d[u] == 1) newleaf[nn++] = u;
            }
        }
        nleaf = nn;
        memcpy(leaf, newleaf, (size_t)nn * sizeof(int));
    }
    if (remain == 1) { *c1 = leaf[0]; *c2 = -1; return 1; }
    *c1 = leaf[0]; *c2 = leaf[1]; return 2;
}

static void ahu_hash(unsigned char key[16]) {
    int c1, c2, nc, L1, L2;
    unsigned char dig[32];
    char form[8192];
    int flen;
    nc = find_centres(&c1, &c2);
    if (nc == 1) {
        ahu_len = 0;
        ahu_rec(c1, -1);
        flen = ahu_len;
        memcpy(form, ahu_buf, (size_t)flen);
    } else {
        ahu_len = 0; ahu_rec(c1, c2); L1 = ahu_len;
        memcpy(form, ahu_buf, (size_t)L1);
        ahu_len = 0; ahu_rec(c2, c1); L2 = ahu_len;
        if (L1 < L2 || (L1 == L2 && memcmp(form, ahu_buf, (size_t)L1) <= 0)) {
            form[L1] = '|';
            memcpy(form + L1 + 1, ahu_buf, (size_t)L2);
            flen = L1 + 1 + L2;
        } else {
            memmove(form + L2 + 1, form, (size_t)L1);
            memcpy(form, ahu_buf, (size_t)L2);
            form[L2] = '|';
            flen = L2 + 1 + L1;
        }
    }
    sha256((unsigned char *)form, (size_t)flen, dig);
    memcpy(key, dig, 16);
}

static int connected(void) {
    int seen[MAXN] = {0}, st[MAXN], sp = 0, cnt = 0, i;
    if (nglob <= 0) return 0;
    st[sp++] = 0; seen[0] = 1;
    while (sp) {
        int v = st[--sp];
        cnt++;
        for (i = 0; i < deg[v]; i++) if (!seen[adj[v][i]]) {
            seen[adj[v][i]] = 1;
            st[sp++] = adj[v][i];
        }
    }
    return cnt == nglob;
}

/* returns 0 ok, 1 parse/tree/label fail, 2 duplicate */
static int check_line(const char *line, int expect_n, unsigned char key[16]) {
    char buf[MAXLINE];
    char *fields[4];
    int nf = 0, i, a, b, lab[MAXN], usedL[2*MAXN], usedD[2*MAXN];
    int usedE[MAXN][MAXN];
    const char *p, *q;
    size_t L;
    L = strlen(line);
    while (L && (line[L-1] == '\n' || line[L-1] == '\r')) L--;
    if (L == 0 || line[0] == '#') return -1; /* skip */
    if (L >= MAXLINE) return 1;
    memcpy(buf, line, L); buf[L] = 0;
    p = buf;
    for (nf = 0; nf < 4; nf++) {
        fields[nf] = (char *)p;
        q = strchr(p, ';');
        if (!q) { nf++; break; }
        *(char *)q = 0;
        p = q + 1;
    }
    if (nf < 3) return 1;
    nglob = atoi(fields[0]);
    if (nglob < 1 || nglob > MAXN) return 1;
    if (expect_n > 0 && nglob != expect_n) return 1;
    qglob = nglob - 1;
    memset(deg, 0, sizeof deg);
    memset(usedE, 0, sizeof usedE);
    /* edges */
    if (qglob == 0) {
        if (fields[1][0]) return 1;
    } else {
        p = fields[1];
        int ne = 0;
        while (*p) {
            if (sscanf(p, "%d-%d", &a, &b) != 2) return 1;
            if (a < 0 || b < 0 || a >= nglob || b >= nglob || a == b) return 1;
            if (usedE[a][b] || usedE[b][a]) return 1;
            usedE[a][b] = usedE[b][a] = 1;
            adj[a][deg[a]++] = b;
            adj[b][deg[b]++] = a;
            ne++;
            while (*p && *p != ',') p++;
            if (*p == ',') p++;
        }
        if (ne != qglob) return 1;
    }
    if (!connected()) return 1;
    /* labels */
    memset(usedL, 0, sizeof usedL);
    p = fields[2];
    for (i = 0; i < nglob; i++) {
        if (!*p) return 1;
        lab[i] = atoi(p);
        if (lab[i] < 0 || lab[i] > 2 * qglob - 1) return 1;
        if (usedL[lab[i]]) return 1;
        usedL[lab[i]] = 1;
        while (*p && *p != ',') p++;
        if (*p == ',') p++;
        else if (i != nglob - 1) return 1;
    }
    if (*p) return 1;
    /* differences */
    memset(usedD, 0, sizeof usedD);
    for (a = 0; a < nglob; a++)
        for (i = 0; i < deg[a]; i++) {
            b = adj[a][i];
            if (b < a) continue;
            int d = lab[a] > lab[b] ? lab[a] - lab[b] : lab[b] - lab[a];
            if (d <= 0 || (d & 1) == 0 || d > 2 * qglob - 1 || usedD[d]) return 1;
            usedD[d] = 1;
        }
    for (i = 1; i <= 2 * qglob - 1; i += 2) if (!usedD[i]) return 1;
    ahu_hash(key);
    return 0;
}

static int failf(const char *msg) { printf("%s\nFAIL\n", msg); return 1; }

static int check_stream(FILE *fp, int expect_n, long long expect_count) {
    char line[MAXLINE];
    long long nlines = 0, skipped = 0, bad = 0, dups = 0;
    unsigned char key[16];
    size_t cap_guess;
    if (expect_count > 0) cap_guess = (size_t)expect_count;
    else if (expect_n > 0 && expect_n <= 24) cap_guess = (size_t)A000055[expect_n];
    else cap_guess = 1 << 20; /* plenty for a single-order certificate up to n=23 */
    if (!set_init(cap_guess)) return failf("out of memory allocating the hash table");
    while (fgets(line, sizeof line, fp)) {
        int r = check_line(line, expect_n, key);
        if (r == -1) { skipped++; continue; }
        nlines++;
        if (r == 1) { bad++; continue; }
        if (!set_insert(key)) dups++;
    }
    printf("lines_ok=%lld skipped_comments=%lld bad_tree_or_label=%lld duplicates=%lld unique=%zu\n",
           nlines - bad, skipped, bad, dups, H.n);
    if (expect_count < 0 && expect_n > 0 && expect_n <= 24) expect_count = A000055[expect_n];
    if (expect_n > 0 && expect_n <= 24) printf("A000055(%d)=%lld\n", expect_n, A000055[expect_n]);
    if (expect_count >= 0) printf("expected=%lld\n", expect_count);
    if (bad || dups) { set_free(); return failf("certificate has invalid or repeated trees"); }
    if (expect_count >= 0 && (nlines != expect_count || (long long)H.n != expect_count)) {
        set_free();
        return failf("count does not equal the expected number of unlabeled trees");
    }
    set_free();
    printf("Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.\n");
    printf("PASS\n");
    return 0;
}

/* ---- self-test ---- */
static int sha_ok(void) {
    unsigned char d[32];
    const char *abc = "abc";
    /* FIPS 180-4: SHA256("") and SHA256("abc") */
    const unsigned char e0[32] = {
        0xe3,0xb0,0xc4,0x42,0x98,0xfc,0x1c,0x14,0x9a,0xfb,0xf4,0xc8,0x99,0x6f,0xb9,0x24,
        0x27,0xae,0x41,0xe4,0x64,0x9b,0x93,0x4c,0xa4,0x95,0x99,0x1b,0x78,0x52,0xb8,0x55
    };
    const unsigned char eabc[32] = {
        0xba,0x78,0x16,0xbf,0x8f,0x01,0xcf,0xea,0x41,0x41,0x40,0xde,0x5d,0xae,0x22,0x23,
        0xb0,0x03,0x61,0xa3,0x96,0x17,0x7a,0x9c,0xb4,0x10,0xff,0x61,0xf2,0x00,0x15,0xad
    };
    sha256((const unsigned char *)"", 0, d);
    if (memcmp(d, e0, 32)) return 0;
    sha256((const unsigned char *)abc, 3, d);
    if (memcmp(d, eabc, 32)) return 0;
    return 1;
}

static int accept(const char *line) {
    unsigned char k[16];
    return check_line(line, 0, k) == 0;
}
static int reject(const char *line) {
    unsigned char k[16];
    int r = check_line(line, 0, k);
    return r == 1;
}

static int selftest(void) {
    int fails = 0;
    if (!sha_ok()) { printf("sha256 test vectors failed\n"); fails++; }
    /* P2, P3, P4, star K1,3, fork */
    if (!accept("2;0-1;0,1")) fails++;
    if (!accept("3;0-1,1-2;0,3,2")) fails++;
    if (!accept("4;0-1,1-2,2-3;0,5,2,3")) fails++;
    if (!accept("4;0-1,0-2,0-3;0,1,3,5")) fails++; /* star */
    /* two numberings of P4 should be isomorphic */
    {
        unsigned char k1[16], k2[16];
        if (check_line("4;0-1,1-2,2-3;0,5,2,3", 0, k1) != 0) fails++;
        if (check_line("4;0-1,1-2,2-3;3,2,5,0", 0, k2) != 0) fails++;  /* vertex-reversal of the previous P4 */
        if (memcmp(k1, k2, 16)) { printf("P4 numberings should match\n"); fails++; }
    }
    /* star != path */
    {
        unsigned char k1[16], k2[16];
        check_line("4;0-1,1-2,2-3;0,5,2,3", 0, k1);
        check_line("4;0-1,0-2,0-3;0,1,3,5", 0, k2);
        if (memcmp(k1, k2, 16) == 0) { printf("path and star should differ\n"); fails++; }
    }
    if (!reject("4;0-1,1-2,2-3;0,1,2,3")) fails++;           /* graceful, not odd */
    if (!reject("4;0-1,1-2,2-3;0,5,2,5")) fails++;           /* duplicate labels */
    if (!reject("4;0-1,1-2,2-3;0,5,2,7")) fails++;           /* label 2q = 7 */
    if (!reject("4;0-1,1-2,2-0;0,1,3,5")) fails++;           /* 3-cycle + isolate? wait 3 verts used, n=4 missing vtx - not a tree */
    if (!reject("3;0-1,1-2,2-0;0,3,2")) fails++;             /* triangle */
    if (!reject("4;0-1,1-2,2-3,0-3;0,5,2,3")) fails++;       /* cycle, too many edges */
    if (!reject("4;0-1,1-2;0,5,2,3")) fails++;               /* missing edge */
    if (!reject("4;0-1,1-2,2-2;0,5,2,3")) fails++;           /* loop */
    if (!reject("4;0-1,1-2,2-3,3-1;0,5,2,3")) fails++;
    if (fails) { printf("selftest failures=%d\nFAIL\n", fails); return 1; }
    printf("selftest_failures=0\nPASS\n");
    return 0;
}

int main(int argc, char **argv) {
    int expect_n = 0, i;
    long long expect_count = -1;
    const char *path = 0;
    FILE *fp;
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--selftest") == 0) return selftest();
        else if (strcmp(argv[i], "--n") == 0 && i + 1 < argc) expect_n = atoi(argv[++i]);
        else if (strcmp(argv[i], "--expect") == 0 && i + 1 < argc) expect_count = atoll(argv[++i]);
        else if (argv[i][0] != '-') path = argv[i];
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    if (path) {
        fp = fopen(path, "r");
        if (!fp) { perror(path); return 2; }
    } else fp = stdin;
    if (expect_n == 0 && path) {
        /* peek first data line for n */
        char tmp[MAXLINE];
        long pos = ftell(fp);
        while (fgets(tmp, sizeof tmp, fp)) {
            if (tmp[0] && tmp[0] != '#') { expect_n = atoi(tmp); break; }
        }
        fseek(fp, pos, SEEK_SET);
    }
    i = check_stream(fp, expect_n, expect_count);
    if (fp != stdin) fclose(fp);
    return i;
}
