/* Criterion-skeptic checker, written from the definition.
   Reads certificate lines n;u-v,...;l0,...,l(n-1)[;extra] on stdin, for a fixed expected n (argv[1]).
   Per line: exactly n-1 edges, endpoints in range, no loops, acyclic (union-find) => tree;
   exactly n labels forming a permutation of 1..n; n-1 edge sums pairwise distinct spanning n-2 => consecutive.
   Canonical key: AHU parenthesis code rooted at the centre (min over the two centres if bicentral),
   stored EXACTLY as a 2n-bit integer (n <= 31), no hashing. Keys are sorted; prints lines, distinct, failures.
   Optional argv[2] = file to dump sorted keys (binary uint64). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int N;
static int adj[32][32], deg[32];
static char code[32][80];

static int cmpstr(const void *a, const void *b){ return strcmp(*(char*const*)a, *(char*const*)b); }

static void build(int v, int p){
    char *kids[32]; int k = 0;
    for (int i = 0; i < deg[v]; i++){ int w = adj[v][i]; if (w == p) continue; build(w, v); kids[k++] = code[w]; }
    qsort(kids, k, sizeof(char*), cmpstr);
    char buf[80]; int L = 0; buf[L++] = '1';
    for (int i = 0; i < k; i++){ int l = strlen(kids[i]); memcpy(buf+L, kids[i], l); L += l; }
    buf[L++] = '0'; buf[L] = 0; strcpy(code[v], buf);
}
static uint64_t tokey(const char *s){ uint64_t x = 0; for (; *s; s++) x = (x<<1) | (uint64_t)(*s=='1'); return x; }

static uint64_t canon(void){
    int d[32], rem = N, removed[32] = {0}, leaves[32], nl = 0;
    for (int v = 0; v < N; v++){ d[v] = deg[v]; if (d[v] <= 1) leaves[nl++] = v; }
    while (rem > 2){
        int nx[32], nn = 0;
        for (int i = 0; i < nl; i++){ int v = leaves[i]; removed[v] = 1; rem--;
            for (int j = 0; j < deg[v]; j++){ int w = adj[v][j]; if (!removed[w]){ d[w]--; if (d[w] == 1) nx[nn++] = w; } } }
        memcpy(leaves, nx, sizeof(int)*nn); nl = nn;
    }
    int c[2], nc = 0; for (int v = 0; v < N; v++) if (!removed[v]) c[nc++] = v;
    char best[80];
    build(c[0], -1); strcpy(best, code[c[0]]);
    if (nc == 2){ build(c[1], -1); if (strcmp(code[c[1]], best) < 0) strcpy(best, code[c[1]]); }
    if ((int)strlen(best) != 2*N) { fprintf(stderr, "internal length error\n"); exit(3); }
    return tokey(best);
}
static uint64_t *ek; static size_t ne; static char *hit; static int ext; static long miss;
static int par[32]; static int fnd(int x){ while (par[x] != x){ par[x] = par[par[x]]; x = par[x]; } return x; }
static int cmpu(const void *a, const void *b){ uint64_t x = *(uint64_t*)a, y = *(uint64_t*)b; return x < y ? -1 : x > y; }

int main(int argc, char **argv){
    int want = atoi(argv[1]);
    if (argc > 3){ FILE *f = fopen(argv[3], "rb"); fseek(f, 0, SEEK_END); ne = ftell(f)/8; fseek(f, 0, SEEK_SET);
        ek = malloc(ne*8); hit = calloc(ne, 1); if (fread(ek, 8, ne, f) != ne) return 5; fclose(f); ext = 1;
        for (size_t i = 1; i < ne; i++) if (ek[i] <= ek[i-1]){ fprintf(stderr, "keys not strictly sorted\n"); return 6; } }
    size_t cap = 1<<20, nk = 0; uint64_t *keys = malloc(cap*8);
    static char line[4096];
    long lines = 0, blank = 0, malformed = 0, wrongn = 0, nottree = 0, badlab = 0;
    while (fgets(line, sizeof line, stdin)){
        size_t L = strlen(line); if (L && line[L-1] == '\n') line[--L] = 0;
        if (L == sizeof(line)-2) { malformed++; continue; }
        if (L == 0){ blank++; continue; }
        lines++;
        char *p = line, *e; long n = strtol(p, &e, 10);
        if (e == p || *e != ';'){ malformed++; continue; }
        if (n != want){ wrongn++; continue; }
        N = (int)n; p = e+1;
        int eu[64], ev[64], m = 0, bad = 0;
        for (;;){
            long u = strtol(p, &e, 10); if (e == p || *e != '-'){ bad = 1; break; } p = e+1;
            long v = strtol(p, &e, 10); if (e == p){ bad = 1; break; }
            if (m >= 60){ bad = 1; break; }
            eu[m] = (int)u; ev[m] = (int)v; m++; p = e;
            if (*p == ','){ p++; continue; } if (*p == ';'){ p++; break; } bad = 1; break;
        }
        if (bad){ malformed++; continue; }
        int lab[64], nlab = 0;
        for (;;){
            long x = strtol(p, &e, 10); if (e == p){ bad = 1; break; }
            if (nlab >= 60){ bad = 1; break; }
            lab[nlab++] = (int)x; p = e;
            if (*p == ','){ p++; continue; } if (*p == ';' || *p == 0) break; bad = 1; break;
        }
        if (bad){ malformed++; continue; }
        /* tree */
        int ok = (m == N-1);
        for (int v = 0; v < N; v++){ par[v] = v; deg[v] = 0; }
        for (int i = 0; ok && i < m; i++){
            if (eu[i] < 0 || eu[i] >= N || ev[i] < 0 || ev[i] >= N || eu[i] == ev[i]){ ok = 0; break; }
            int a = fnd(eu[i]), b = fnd(ev[i]); if (a == b){ ok = 0; break; } par[a] = b;
            adj[eu[i]][deg[eu[i]]++] = ev[i]; adj[ev[i]][deg[ev[i]]++] = eu[i];
        }
        if (!ok){ nottree++; continue; }
        /* labels */
        int lok = (nlab == N), seenl[64] = {0};
        for (int i = 0; lok && i < N; i++){ if (lab[i] < 1 || lab[i] > N || seenl[lab[i]]){ lok = 0; break; } seenl[lab[i]] = 1; }
        if (lok){
            int seens[64] = {0}, mn = 999, mx = -1;
            for (int i = 0; i < m; i++){ int s = lab[eu[i]] + lab[ev[i]]; if (seens[s]){ lok = 0; break; } seens[s] = 1; if (s < mn) mn = s; if (s > mx) mx = s; }
            if (lok && mx - mn != N-2) lok = 0;
        }
        if (!lok){ badlab++; continue; }
        if (nk == cap){ cap *= 2; keys = realloc(keys, cap*8); if (!keys){ fprintf(stderr, "oom\n"); return 4; } }
        keys[nk++] = canon();
        if (ext){
            int M = N; N = M+1; deg[M] = 0;
            for (int v = 0; v < M; v++){
                adj[v][deg[v]++] = M; adj[M][0] = v; deg[M] = 1;
                uint64_t k = canon();
                size_t lo = 0, hi = ne;
                while (lo < hi){ size_t mid = (lo+hi)/2; if (ek[mid] < k) lo = mid+1; else hi = mid; }
                if (lo < ne && ek[lo] == k) hit[lo] = 1; else miss++;
                deg[v]--;
            }
            N = M;
        }
    }
    qsort(keys, nk, 8, cmpu);
    size_t distinct = 0; for (size_t i = 0; i < nk; i++) if (i == 0 || keys[i] != keys[i-1]) distinct++;
    if (ext){ size_t unhit = 0; for (size_t i = 0; i < ne; i++) if (!hit[i]) unhit++;
        printf("EXT order %d->%d: children_not_in_cert=%ld cert_keys=%zu cert_keys_never_generated=%zu\n", want, want+1, miss, ne, unhit); }
    if (argc > 2 && argv[2][0] != '-'){ FILE *f = fopen(argv[2], "wb"); fwrite(keys, 8, nk, f); fclose(f); }
    printf("n=%d lines=%ld blank=%ld malformed=%ld wrong_n=%ld not_tree=%ld bad_label=%ld valid=%zu distinct=%zu\n",
           want, lines, blank, malformed, wrongn, nottree, badlab, nk, distinct);
    return 0;
}
