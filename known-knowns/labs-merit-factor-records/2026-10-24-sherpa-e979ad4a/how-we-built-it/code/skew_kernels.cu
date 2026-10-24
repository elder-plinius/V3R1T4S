// Skew-symmetric LABS tabu search, one CUDA block per walker.
// L = 2n+1. Free variables v = 0..n (position v). Skew rule: s[n+j] = (-1)^j s[n-j], j = 1..n,
// equivalently s[2n-q] = (-1)^(n-q) s[q] for every q. Odd-lag correlations vanish, so
// E = sum_{j=1..n} C[2j]^2 and only even lags are stored: Cs[j] = C_{2j}.
// Flipping v < n flips positions v and 2n-v; flipping v = n flips the centre only.
// For even k: dC_k = -4u,  u = s_v (s_{v-k}[k<=v] + w_b s_{v+k}[v+k<=2n, k != 2n-2v]),  w_b = [v<n].
// dE = sum_k dC_k (2C_k + dC_k) = 8 sum_j u_j (2u_j - Cs[j]).

#define ULL unsigned long long

__device__ __forceinline__ unsigned int hash32(unsigned int x) {
    x ^= x >> 16; x *= 0x7feb352dU; x ^= x >> 15; x *= 0x846ca68bU; x ^= x >> 16; return x;
}

// sp: padded sequence, sp[OFF + pos], zeros for pos < 0 and pos > 2n; OFF = 2n.
__device__ __forceinline__ int skew_dE(const int* __restrict__ sp, const int* __restrict__ Cs,
                                       const int n, const int OFF, const int v) {
    const int sv = sp[OFF + v];
    const int wb = (v < n) ? 1 : 0;
    int acc = 0;
    #pragma unroll 4
    for (int j = 1; j <= n; j++) {
        const int k = j << 1;
        const int u = sv * (sp[OFF + v - k] + wb * sp[OFF + v + k]);
        acc += u * ((u << 1) - Cs[j]);
    }
    if (v < n) {                       // pair (v, 2n-v) at lag 2n-2v: both ends flip, no change
        const int j = n - v, k = j << 1;
        const int a = sp[OFF + v - k], b = sp[OFF + v + k];
        const int uf = sv * (a + b), uc = sv * a;
        acc += uc * ((uc << 1) - Cs[j]) - uf * ((uf << 1) - Cs[j]);
    }
    return acc << 3;
}

__device__ __forceinline__ int skew_dC_quarter(const int* __restrict__ sp, const int n, const int OFF,
                                               const int vs, const int j) {
    const int k = j << 1;
    const int a = sp[OFF + vs - k];
    int b = (vs < n) ? sp[OFF + vs + k] : 0;
    if (vs < n && j == n - vs) b = 0;
    return sp[OFF + vs] * (a + b);     // dC_{2j} = -4 * this
}

extern "C" __global__ void skew_dE_all(const int L, const signed char* __restrict__ S,
                                       const int* __restrict__ Cg, int* __restrict__ dEout) {
    const int w = blockIdx.x, tid = threadIdx.x, n = (L - 1) >> 1, OFF = 2 * n;
    extern __shared__ int sh[];
    int* sp = sh; int* Cs = sp + 5 * n + 1;
    for (int i = tid; i < 5 * n + 1; i += blockDim.x) sp[i] = 0;
    __syncthreads();
    for (int i = tid; i < L; i += blockDim.x) sp[OFF + i] = S[(size_t)w * L + i];
    for (int j = tid; j <= n; j += blockDim.x) Cs[j] = Cg[(size_t)w * (n + 1) + j];
    __syncthreads();
    for (int v = tid; v <= n; v += blockDim.x) dEout[(size_t)w * (n + 1) + v] = skew_dE(sp, Cs, n, OFF, v);
}

// Compute even-lag correlations and energy from S for walkers with mask[w] != 0; reset walker state.
extern "C" __global__ void skew_init(const int L, const int* __restrict__ mask,
                                     const signed char* __restrict__ S, int* __restrict__ Cg,
                                     int* __restrict__ Eg, int* __restrict__ bestEg,
                                     signed char* __restrict__ bestS, int* __restrict__ tabu,
                                     int* __restrict__ stepg, int* __restrict__ oddcheck) {
    const int w = blockIdx.x, tid = threadIdx.x, n = (L - 1) >> 1;
    if (!mask[w]) return;
    extern __shared__ int sh[];
    int* s = sh; int* acc = s + L;
    for (int i = tid; i < L; i += blockDim.x) s[i] = S[(size_t)w * L + i];
    if (tid == 0) { acc[0] = 0; acc[1] = 0; }
    __syncthreads();
    int Epart = 0, oddpart = 0;
    for (int k = tid + 1; k < L; k += blockDim.x) {
        int c = 0;
        for (int i = 0; i + k < L; i++) c += s[i] * s[i + k];
        if (k & 1) oddpart |= (c != 0);
        else { Cg[(size_t)w * (n + 1) + (k >> 1)] = c; Epart += c * c; }
    }
    atomicAdd(&acc[0], Epart); atomicOr(&acc[1], oddpart);
    __syncthreads();
    if (tid == 0) { Cg[(size_t)w * (n + 1)] = 0; Eg[w] = acc[0]; bestEg[w] = acc[0]; stepg[w] = 0;
                    oddcheck[w] = acc[1]; }
    for (int i = tid; i < L; i += blockDim.x) bestS[(size_t)w * L + i] = (signed char)s[i];
    for (int v = tid; v <= n; v += blockDim.x) tabu[(size_t)w * (n + 1) + v] = 0;
}

extern "C" __global__ void skew_tabu(const int L, const int nsteps, const unsigned int seed,
                                     const int tenure_min, const int tenure_span,
                                     signed char* __restrict__ S, int* __restrict__ Cg,
                                     int* __restrict__ Eg, int* __restrict__ bestEg,
                                     signed char* __restrict__ bestS, int* __restrict__ tabu,
                                     int* __restrict__ stepg, const int* __restrict__ frozen) {
    // frozen[w] = P: free variables v < P (the head and its mirror) are never flipped.
    const int w = blockIdx.x, tid = threadIdx.x, n = (L - 1) >> 1, NV = n + 1, OFF = 2 * n;
    const int Pw = frozen[w];
    extern __shared__ ULL sh64[];
    ULL* red = sh64;                        // 32 slots
    int* sp = (int*)(sh64 + 32);            // 5n+1
    int* Cs = sp + 5 * n + 1;               // n+1
    int* misc = Cs + n + 1;                 // [0]=v*, [1]=dE*, [2]=E, [3]=bestE, [4]=copy flag
    for (int i = tid; i < 5 * n + 1; i += blockDim.x) sp[i] = 0;
    __syncthreads();
    for (int i = tid; i < L; i += blockDim.x) sp[OFF + i] = S[(size_t)w * L + i];
    for (int j = tid; j <= n; j += blockDim.x) Cs[j] = Cg[(size_t)w * (n + 1) + j];
    if (tid == 0) { misc[2] = Eg[w]; misc[3] = bestEg[w]; misc[4] = 0; }
    const int step0 = stepg[w];
    int my_tabu = (tid < NV) ? tabu[(size_t)w * NV + tid] : 0;
    const unsigned int wseed = hash32(seed ^ (0x9E3779B1u * (unsigned)(w + 1)));
    __syncthreads();
    for (int t = 0; t < nsteps; t++) {
        const int step = step0 + t;
        const int E = misc[2], bestE = misc[3];
        ULL key = ~0ULL;
        if (tid < NV && tid >= Pw) {
            const int dE = skew_dE(sp, Cs, n, OFF, tid);
            const bool allowed = (my_tabu <= step) || (E + dE < bestE);
            const unsigned int r = hash32(wseed ^ hash32((unsigned)step * 0x85EBCA77u + (unsigned)tid));
            key = ((ULL)(unsigned int)(dE + 0x40000000)) << 32 | ((ULL)(r & 0xFFFu) << 20) | (ULL)tid;
            if (!allowed) key |= 0x8000000000000000ULL;
        }
        #pragma unroll
        for (int off = 16; off > 0; off >>= 1) { ULL o = __shfl_down_sync(0xffffffffu, key, off); key = (o < key) ? o : key; }
        if ((tid & 31) == 0) red[tid >> 5] = key;
        __syncthreads();
        if (tid < 32) {
            ULL k2 = (tid < (int)(blockDim.x >> 5)) ? red[tid] : ~0ULL;
            #pragma unroll
            for (int off = 16; off > 0; off >>= 1) { ULL o = __shfl_down_sync(0xffffffffu, k2, off); k2 = (o < k2) ? o : k2; }
            if (tid == 0) { misc[0] = (int)(k2 & 0xFFFFFULL);
                            misc[1] = (int)((k2 >> 32) & 0x7FFFFFFFULL) - 0x40000000; }
        }
        __syncthreads();
        const int vs = misc[0];
        if (tid < n) Cs[tid + 1] -= skew_dC_quarter(sp, n, OFF, vs, tid + 1) << 2;
        if (tid == vs) {
            const unsigned int r = hash32(wseed ^ hash32((unsigned)step * 0x27D4EB2Fu + 0x165667B1u));
            my_tabu = step + 1 + tenure_min + (tenure_span > 0 ? (int)(r % (unsigned)tenure_span) : 0);
        }
        __syncthreads();
        if (tid == 0) {
            sp[OFF + vs] = -sp[OFF + vs];
            if (vs < n) sp[OFF + 2 * n - vs] = -sp[OFF + 2 * n - vs];
            const int En = misc[2] + misc[1];
            misc[2] = En;
            if (En < misc[3]) { misc[3] = En; misc[4] = 1; }
        }
        __syncthreads();
        if (misc[4]) {
            for (int i = tid; i < L; i += blockDim.x) bestS[(size_t)w * L + i] = (signed char)sp[OFF + i];
            __syncthreads();
            if (tid == 0) misc[4] = 0;
            __syncthreads();
        }
    }
    for (int i = tid; i < L; i += blockDim.x) S[(size_t)w * L + i] = (signed char)sp[OFF + i];
    for (int j = tid; j <= n; j += blockDim.x) Cg[(size_t)w * (n + 1) + j] = Cs[j];
    if (tid < NV) tabu[(size_t)w * NV + tid] = my_tabu;
    if (tid == 0) { Eg[w] = misc[2]; bestEg[w] = misc[3]; stepg[w] = step0 + nsteps; }
}

// Self-avoiding walk in the skew space (Dimitrov / lssOrel style): each step moves to the lowest-energy neighbour whose
// state has not been visited in this walk. Visited states are kept in an open-addressing table of 32-bit fingerprints
// of a 64-bit Zobrist hash (tbl slots, power of two, in shared memory). A walk = one launch of nsteps steps from S.
extern "C" __global__ void skew_saw(const int L, const int nsteps, const unsigned int seed, const int tbl,
                                    const unsigned long long* __restrict__ Z,
                                    signed char* __restrict__ S, int* __restrict__ Cg,
                                    int* __restrict__ Eg, int* __restrict__ bestEg,
                                    signed char* __restrict__ bestS, int* __restrict__ stepg,
                                    const int* __restrict__ frozen, int* __restrict__ stuck) {
    const int w = blockIdx.x, tid = threadIdx.x, n = (L - 1) >> 1, NV = n + 1, OFF = 2 * n;
    const int Pw = frozen[w];
    extern __shared__ ULL sh64[];
    ULL* red = sh64;                        // 32 slots
    ULL* hcur = sh64 + 32;                  // current state hash
    unsigned int* T = (unsigned int*)(sh64 + 34);         // tbl slots
    int* sp = (int*)(T + tbl);              // 5n+1
    int* Cs = sp + 5 * n + 1;               // n+1
    int* misc = Cs + n + 1;                 // [0]=v*, [1]=dE*, [2]=E, [3]=bestE, [4]=copy flag, [5]=stuck
    const unsigned int mask = (unsigned int)tbl - 1u;
    for (int i = tid; i < 5 * n + 1; i += blockDim.x) sp[i] = 0;
    for (int i = tid; i < tbl; i += blockDim.x) T[i] = 0u;
    __syncthreads();
    for (int i = tid; i < L; i += blockDim.x) sp[OFF + i] = S[(size_t)w * L + i];
    for (int j = tid; j <= n; j += blockDim.x) Cs[j] = Cg[(size_t)w * (n + 1) + j];
    if (tid == 0) { misc[2] = Eg[w]; misc[3] = bestEg[w]; misc[4] = 0; misc[5] = 0; }
    const ULL zv = (tid < NV) ? Z[tid] : 0ULL;
    __syncthreads();
    ULL hpart = (tid < NV && sp[OFF + tid] > 0) ? zv : 0ULL;          // H = XOR of z[v] over v with s_v = +1
    #pragma unroll
    for (int off = 16; off > 0; off >>= 1) hpart ^= __shfl_down_sync(0xffffffffu, hpart, off);
    if ((tid & 31) == 0) red[tid >> 5] = hpart;
    __syncthreads();
    if (tid == 0) {
        ULL h = 0ULL; for (int i = 0; i < (int)(blockDim.x >> 5); i++) h ^= red[i];
        *hcur = h; unsigned int slot = (unsigned int)h & mask, fp = (unsigned int)(h >> 32) | 1u;
        while (T[slot] != 0u && T[slot] != fp) slot = (slot + 1u) & mask;
        T[slot] = fp;
    }
    const int step0 = stepg[w];
    const unsigned int wseed = hash32(seed ^ (0x9E3779B1u * (unsigned)(w + 1)));
    __syncthreads();
    for (int t = 0; t < nsteps; t++) {
        const int step = step0 + t;
        ULL key = ~0ULL;
        if (tid < NV && tid >= Pw) {
            const int dE = skew_dE(sp, Cs, n, OFF, tid);
            const ULL hv = (*hcur) ^ zv;
            unsigned int slot = (unsigned int)hv & mask; const unsigned int fp = (unsigned int)(hv >> 32) | 1u;
            bool visited = false;
            for (int pr = 0; pr < 16; pr++) { const unsigned int x = T[slot]; if (x == 0u) break; if (x == fp) { visited = true; break; } slot = (slot + 1u) & mask; }
            const unsigned int r = hash32(wseed ^ hash32((unsigned)step * 0x85EBCA77u + (unsigned)tid));
            key = ((ULL)(unsigned int)(dE + 0x40000000)) << 32 | ((ULL)(r & 0xFFFu) << 20) | (ULL)tid;
            if (visited) key |= 0x8000000000000000ULL;
        }
        #pragma unroll
        for (int off = 16; off > 0; off >>= 1) { ULL o = __shfl_down_sync(0xffffffffu, key, off); key = (o < key) ? o : key; }
        if ((tid & 31) == 0) red[tid >> 5] = key;
        __syncthreads();
        if (tid < 32) {
            ULL k2 = (tid < (int)(blockDim.x >> 5)) ? red[tid] : ~0ULL;
            #pragma unroll
            for (int off = 16; off > 0; off >>= 1) { ULL o = __shfl_down_sync(0xffffffffu, k2, off); k2 = (o < k2) ? o : k2; }
            if (tid == 0) { misc[0] = (int)(k2 & 0xFFFFFULL);
                            misc[1] = (int)((k2 >> 32) & 0x7FFFFFFFULL) - 0x40000000;
                            if (k2 & 0x8000000000000000ULL) misc[5] += 1; }
        }
        __syncthreads();
        const int vs = misc[0];
        if (tid < n) Cs[tid + 1] -= skew_dC_quarter(sp, n, OFF, vs, tid + 1) << 2;
        __syncthreads();
        if (tid == 0) {
            sp[OFF + vs] = -sp[OFF + vs];
            if (vs < n) sp[OFF + 2 * n - vs] = -sp[OFF + 2 * n - vs];
            const int En = misc[2] + misc[1];
            misc[2] = En;
            if (En < misc[3]) { misc[3] = En; misc[4] = 1; }
            const ULL h = (*hcur) ^ Z[vs]; *hcur = h;
            unsigned int slot = (unsigned int)h & mask; const unsigned int fp = (unsigned int)(h >> 32) | 1u;
            for (int pr = 0; pr < 64; pr++) { const unsigned int x = T[slot]; if (x == 0u) { T[slot] = fp; break; } if (x == fp) break; slot = (slot + 1u) & mask; }
        }
        __syncthreads();
        if (misc[4]) {
            for (int i = tid; i < L; i += blockDim.x) bestS[(size_t)w * L + i] = (signed char)sp[OFF + i];
            __syncthreads();
            if (tid == 0) misc[4] = 0;
            __syncthreads();
        }
    }
    for (int i = tid; i < L; i += blockDim.x) S[(size_t)w * L + i] = (signed char)sp[OFF + i];
    for (int j = tid; j <= n; j += blockDim.x) Cg[(size_t)w * (n + 1) + j] = Cs[j];
    if (tid == 0) { Eg[w] = misc[2]; bestEg[w] = misc[3]; stepg[w] = step0 + nsteps; stuck[w] = misc[5]; }
}
