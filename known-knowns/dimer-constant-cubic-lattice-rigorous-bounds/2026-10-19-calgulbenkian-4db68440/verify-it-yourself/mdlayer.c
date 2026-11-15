/* Monomer-dimer diagonal-layer transfer matrix applied to a vector, built from the definition.
   Usage: mdlayer M N xfile.bin out.bin
   V = Z/M x Z/N, vertex v = a*N + b.  D = {(0,0),(1,0),(0,1)}.  A[u,w] = 1 iff w-u in D.
   T[U,W] = sum over S subset of (V minus U) of per A[S,W].
   (T x)_U = sum_{S subset of comp(U)} g(S),  g(S) = sum_W per A[S,W] x_W
   g is computed by a dynamic program over the vertices of S in index order, keeping the processed
   part of S and the still-usable targets W.  Output: (T x)_U for every U as unsigned 128-bit
   little-endian (two uint64: low, high).  Exact integer arithmetic only. */
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage\n"); return 2; }
    int M = atoi(argv[1]), N = atoi(argv[2]), V = M * N;
    if (V > 24 || M < 2 || N < 2) { fprintf(stderr, "bad size\n"); return 2; }
    uint64_t NS = 1ULL << V;
    uint64_t *x = malloc(NS * 8);
    FILE *f = fopen(argv[3], "rb");
    if (!f || fread(x, 8, NS, f) != NS) { fprintf(stderr, "read x failed\n"); return 2; }
    fclose(f);
    int tg[32][3];
    for (int a = 0; a < M; a++) for (int b = 0; b < N; b++) {
        int u = a * N + b;
        tg[u][0] = u; tg[u][1] = ((a + 1) % M) * N + b; tg[u][2] = a * N + (b + 1) % N;
    }
    /* last consumer of target t = largest u whose targets contain t */
    int last[32];
    for (int t = 0; t < V; t++) last[t] = -1;
    for (int u = 0; u < V; u++) for (int k = 0; k < 3; k++) if (u > last[tg[u][k]]) last[tg[u][k]] = u;
    /* live[i] = list of targets still usable before processing vertex i (those with last >= i) */
    int Lcur[32], nl = 0;
    for (int t = 0; t < V; t++) Lcur[nl++] = t;
    u128 *cur = malloc(NS * sizeof(u128)); /* index = Sprefix(0 bits) , compressed W (V bits) */
    for (uint64_t w = 0; w < NS; w++) cur[w] = x[w];
    free(x);
    u128 *nxt;
    int peak = V;
    for (int i = 0; i < V; i++) {
        int Lnew[32], nn = 0;
        for (int j = 0; j < nl; j++) if (last[Lcur[j]] > i) Lnew[nn++] = Lcur[j];
        /* new array: (i+1) S bits, nn W bits */
        if (i + 1 + nn > peak) peak = i + 1 + nn;
        uint64_t nsz = 1ULL << (i + 1 + nn);
        nxt = calloc(nsz, sizeof(u128));
        if (!nxt) { fprintf(stderr, "alloc fail\n"); return 3; }
        /* position of each target in old / new compressed index */
        int posold[32], posnew[32];
        for (int t = 0; t < V; t++) { posold[t] = -1; posnew[t] = -1; }
        for (int j = 0; j < nl; j++) posold[Lcur[j]] = j;
        for (int j = 0; j < nn; j++) posnew[Lnew[j]] = j;
        uint64_t osz = 1ULL << (i + nl);
        for (uint64_t idx = 0; idx < osz; idx++) {
            u128 val = cur[idx];
            if (val == 0) continue;
            uint64_t S = idx & ((1ULL << i) - 1), wc = idx >> i;
            /* unpack W as a V-bit mask */
            uint32_t W = 0;
            for (int j = 0; j < nl; j++) if (wc >> j & 1) W |= 1u << Lcur[j];
            /* option 1: i not in S */
            for (int opt = -1; opt < 3; opt++) {
                uint32_t W2 = W; uint64_t S2 = S;
                if (opt >= 0) {
                    int t = tg[i][opt];
                    if (!(W >> t & 1)) continue;
                    W2 = W & ~(1u << t); S2 = S | (1ULL << i);
                }
                /* every target whose last consumer is i (or earlier) must now be unused */
                int bad = 0; uint64_t nc = 0;
                for (int j = 0; j < nl; j++) {
                    int t = Lcur[j];
                    if (W2 >> t & 1) { if (posnew[t] < 0) { bad = 1; break; } nc |= 1ULL << posnew[t]; }
                }
                if (bad) continue;
                nxt[S2 | (nc << (i + 1))] += val;
            }
        }
        free(cur); cur = nxt;
        nl = nn; memcpy(Lcur, Lnew, sizeof(int) * nn);
    }
    /* now nl == 0, cur[S] = g(S).  Subset-sum transform: Z[X] = sum_{S subset X} g(S) */
    for (int b = 0; b < V; b++)
        for (uint64_t X = 0; X < NS; X++) if (X >> b & 1) cur[X] += cur[X ^ (1ULL << b)];
    FILE *o = fopen(argv[4], "wb");
    for (uint64_t U = 0; U < NS; U++) {
        u128 v = cur[(NS - 1) ^ U];
        uint64_t w[2] = { (uint64_t)v, (uint64_t)(v >> 64) };
        fwrite(w, 8, 2, o);
    }
    fclose(o);
    fprintf(stderr, "peak state bits %d\n", peak);
    return 0;
}
