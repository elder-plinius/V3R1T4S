// tm.cpp -- eigenvalue form of the critical-polynomial condition (Jacobsen 2015, arXiv 1507.03027, eq. (13);
// Scullard-Jacobsen 2020, arXiv 1910.12376, eq. (4)) for site or bond percolation on a semi-infinite cylinder.
//
// Sectors (connectivity-state translation of the s = 0 open / closed sectors, see NOTES.md):
//   closed: histories in which no occupied cluster ever closes a cycle winding around the cylinder
//           (lift of every frontier site in the universal cover is tracked; a merge whose lifts disagree = winding).
//   open:   histories in which the cluster connected to the far past (label 1) keeps at least one frontier site.
// p(W) = root of f(p) = log Lambda_open(p) - log Lambda_closed(p).
//
// Lattices: row words over {S,T} (BRIEF.md construction), "kagome" (full rows + every-other connector rows),
// "dsq" (square lattice in diagonal orientation: T-word without horizontal edges).
//
// usage: tm LATTICE site|bond W root LO HI [tol]      -> prints p(W)
//        tm LATTICE site|bond W eval P                 -> prints f(P), Lambdas
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>

typedef unsigned __int128 u128;
enum { NEWV = 0, EDGE = 1, KILL = 2, PERM = 3 };
struct Op { int t, a, b, dk; std::vector<int> perm; };

static int K = 0;                 // number of slots
static bool SITE = true;          // site or bond percolation
static std::vector<Op> OPS;       // one period
static std::vector<int> INITSLOTS;// slots occupied by frontier vertices at period start

// ---------------------------------------------------------------- lattice construction (generic)
struct GV { int col; };                       // vertex of one period, column in units where circumference = C
struct GE { int u, v, delta; };               // u,v: vertex ids; negative id -1-j means vertex j of previous period
struct Graph { int C; std::vector<GV> vs; std::vector<GE> es; };

static void build_ops(const Graph& g) {
    int n = g.vs.size();
    // remaining edge counters
    std::vector<int> remCur(n, 0), remPrev(n, 0);
    for (auto& e : g.es) {
        // edges inside this period count once for each endpoint; edges to previous period count for prev endpoint
        if (e.u >= 0) remCur[e.u]++; else remPrev[-1 - e.u]++;
        if (e.v >= 0) remCur[e.v]++; else remPrev[-1 - e.v]++;
    }
    // edges to the next period: a vertex j of this period has as many next-period edges as remPrev[j]
    // initial frontier = previous-period vertices with remPrev>0, canonical slot order = by index
    std::vector<int> frontier;
    for (int j = 0; j < n; j++) if (remPrev[j] > 0) frontier.push_back(j);
    // slot management
    std::vector<int> slotOfPrev(n, -1), slotOfCur(n, -1);
    std::vector<int> used; // slot -> 1 if used
    int maxslot = 0;
    auto alloc = [&]() { for (size_t s = 0; s < used.size(); s++) if (!used[s]) { used[s] = 1; return (int)s; }
                         used.push_back(1); return (int)used.size() - 1; };
    INITSLOTS.clear();
    for (size_t i = 0; i < frontier.size(); i++) { int s = alloc(); slotOfPrev[frontier[i]] = s; INITSLOTS.push_back(s); }
    // per-vertex edge lists (edges whose later endpoint is this vertex)
    // processing order = vertex index order; an edge is emitted when its later endpoint is created
    std::vector<std::vector<int>> at(n);
    for (size_t k = 0; k < g.es.size(); k++) {
        const GE& e = g.es[k];
        int later = std::max(e.u, e.v);
        if (later < 0) { fprintf(stderr, "edge between two previous-period vertices\n"); exit(1); }
        at[later].push_back(k);
    }
    std::vector<int> rc = remCur, rp = remPrev;
    // next-period edges of current vertex j: rp_next[j] = remPrev[j]
    std::vector<int> rcTot(n); for (int j = 0; j < n; j++) rcTot[j] = remCur[j] + remPrev[j];
    std::vector<int> rpp = remPrev; // remaining for previous-period vertices
    OPS.clear();
    auto colOf = [&](int id) { return id >= 0 ? g.vs[id].col : g.vs[-1 - id].col; };
    auto slotOf = [&](int id) { return id >= 0 ? slotOfCur[id] : slotOfPrev[-1 - id]; };
    for (int v = 0; v < n; v++) {
        int s = alloc(); slotOfCur[v] = s; if (s + 1 > maxslot) maxslot = s + 1;
        OPS.push_back({NEWV, s, -1, 0, {}});
        std::vector<int> toKill;
        for (int k : at[v]) {
            const GE& e = g.es[k];
            int a = e.u, b = e.v, d = e.delta;
            int num = colOf(a) + d - colOf(b);
            if (num % g.C != 0) { fprintf(stderr, "bad delta\n"); exit(1); }
            OPS.push_back({EDGE, slotOf(a), slotOf(b), num / g.C, {}});
            for (int id : {a, b}) {
                if (id >= 0) { if (--rcTot[id] == 0) toKill.push_back(id); }
                else { if (--rpp[-1 - id] == 0) toKill.push_back(id); }
            }
        }
        if (rcTot[v] == 0 && std::find(toKill.begin(), toKill.end(), v) == toKill.end()) toKill.push_back(v);
        for (int id : toKill) { int sl = slotOf(id); OPS.push_back({KILL, sl, -1, 0, {}}); used[sl] = 0;
                                if (id >= 0) slotOfCur[id] = -1; else slotOfPrev[-1 - id] = -1; }
    }
    // final frontier must be the same index set
    std::vector<int> fin;
    for (int j = 0; j < n; j++) if (slotOfCur[j] >= 0) fin.push_back(j);
    if (fin != frontier) { fprintf(stderr, "frontier mismatch %zu vs %zu\n", fin.size(), frontier.size()); exit(1); }
    K = std::max(maxslot, (int)used.size());
    Op P; P.t = PERM; P.a = P.b = P.dk = 0; P.perm.assign(K, -1);
    for (size_t i = 0; i < frontier.size(); i++) P.perm[INITSLOTS[i]] = slotOfCur[frontier[i]];
    OPS.push_back(P);
    if (K * (5 + (SITE ? 2 : 3)) > 128) { fprintf(stderr, "K=%d too large\n", K); exit(1); }
}

static Graph row_word(const std::string& word, int W, bool horiz = true) {
    Graph g; g.C = W; int R = word.size();
    auto id = [&](int x, int y) { // y = 0 means previous period's last row; y = 1..R this period
        x = ((x % W) + W) % W; return y == 0 ? -1 - ((R - 1) * W + x) : (y - 1) * W + x; };
    for (int y = 1; y <= R; y++) for (int x = 0; x < W; x++) g.vs.push_back({x});
    for (int y = 1; y <= R; y++) {
        char gt = word[y - 1];
        for (int x = 0; x < W; x++) {
            if (horiz && x >= 1) g.es.push_back({id(x - 1, y), id(x, y), +1});
            g.es.push_back({id(x, y - 1), id(x, y), 0});
            if (gt == 'T') g.es.push_back({id(x + 1, y - 1), id(x, y), -1});
            if (horiz && x == W - 1) g.es.push_back({id(W - 1, y), id(0, y), +1});
        }
    }
    return g;
}

static Graph kagome(int W) { // W full sites per full row (even); C = 2W in doubled coordinates
    if (W % 2) { fprintf(stderr, "kagome needs even W\n"); exit(1); }
    Graph g; g.C = 2 * W; int h = W / 2;
    // period rows: F0 (W), C1 (h, offset 0), F2 (W), C3 (h, offset 1); previous period's last row = C3
    int base[4] = {0, W, W + h, 2 * W + h};
    int n = 2 * W + 2 * h;
    auto fid = [&](int r, int x) { x = ((x % W) + W) % W; return base[r] + x; };
    auto cid = [&](int r, int j) { j = ((j % h) + h) % h; return base[r] + j; };
    for (int x = 0; x < W; x++) g.vs.push_back({2 * x});
    for (int j = 0; j < h; j++) g.vs.push_back({4 * j + 1});
    for (int x = 0; x < W; x++) g.vs.push_back({2 * x});
    for (int j = 0; j < h; j++) g.vs.push_back({(4 * j + 3) % (2 * W)});
    (void)n;
    auto prev = [&](int id) { return -1 - id; };
    // connector rows: r=1 (offset 0) between F0 and F2; r=3 (offset 1) between F2 and next F0 (= prev F0... )
    // edges F0 <- previous C3 (offset 1): connector j at coord 4j+3 connects to full x=2j+1 (delta from conn: -1)
    // and x=2j+2 (delta +1) of F0 (this period).
    for (int x = 0; x < W; x++) if (x >= 1) g.es.push_back({fid(0, x - 1), fid(0, x), +2});
    g.es.push_back({fid(0, W - 1), fid(0, 0), +2});
    for (int j = 0; j < h; j++) {
        int c = prev(cid(3, j)); // previous-period connector, coord 4j+3
        g.es.push_back({c, fid(0, 2 * j + 1), (2 * (2 * j + 1)) - (4 * j + 3)});
        g.es.push_back({c, fid(0, 2 * j + 2), (2 * (2 * j + 2)) - (4 * j + 3)});
    }
    for (int j = 0; j < h; j++) { // C1 offset 0 connector at 4j+1 over pair (2j, 2j+1) of F0 and F2
        g.es.push_back({fid(0, 2 * j), cid(1, j), (4 * j + 1) - 4 * j});
        g.es.push_back({fid(0, 2 * j + 1), cid(1, j), (4 * j + 1) - (4 * j + 2)});
    }
    for (int x = 0; x < W; x++) if (x >= 1) g.es.push_back({fid(2, x - 1), fid(2, x), +2});
    g.es.push_back({fid(2, W - 1), fid(2, 0), +2});
    for (int j = 0; j < h; j++) {
        g.es.push_back({cid(1, j), fid(2, 2 * j), 4 * j - (4 * j + 1)});
        g.es.push_back({cid(1, j), fid(2, 2 * j + 1), (4 * j + 2) - (4 * j + 1)});
    }
    for (int j = 0; j < h; j++) { // C3 offset 1 connector at 4j+3 over pair (2j+1, 2j+2) of F2
        g.es.push_back({fid(2, 2 * j + 1), cid(3, j), (4 * j + 3) - (4 * j + 2)});
        g.es.push_back({fid(2, 2 * j + 2), cid(3, j), (4 * j + 3) - (4 * j + 4)});
    }
    return g;
}

// ---------------------------------------------------------------- states
typedef u128 Key; // 7 bits per slot: label (5 bits) + lift offset + 1 (2 bits); K <= 18
struct St { uint8_t lab[24]; int8_t kk[24]; };
static bool OPEN = false;

static int KB = 2, KBIAS = 1; // lift-offset bits per slot: site 2 bits [-1,2]; bond 3 bits [-4,3] (set in main)
static inline Key pack(const St& s) {
    Key k = 0; int sh = 5 + KB;
    for (int i = K - 1; i >= 0; i--) k = (k << sh) | ((u128)s.lab[i] << KB) | (u128)(s.kk[i] + KBIAS);
    return k;
}
static inline void unpack(Key k, St& s) {
    int sh = 5 + KB; unsigned m = (1u << sh) - 1, mk = (1u << KB) - 1;
    for (int i = 0; i < K; i++) { unsigned c = (unsigned)(k & m); s.lab[i] = (uint8_t)(c >> KB); s.kk[i] = (int8_t)((int)(c & mk) - KBIAS); k >>= sh; }
}
static bool canon(St& s) {
    uint8_t map[32]; int8_t base[32]; memset(map, 0, sizeof map); memset(base, 0, sizeof base);
    int next = OPEN ? 2 : 1;
    if (OPEN) map[1] = 1;
    for (int i = 0; i < K; i++) {
        int l = s.lab[i];
        if (!l) { s.kk[i] = 0; continue; }
        if (!map[l]) { map[l] = (uint8_t)next++; base[l] = s.kk[i]; }
        else if (OPEN && l == 1) {}
    }
    if (next > 31) { fprintf(stderr, "too many labels\n"); exit(2); }
    bool seen[32]; memset(seen, 0, sizeof seen);
    for (int i = 0; i < K; i++) {
        int l = s.lab[i];
        if (!l) continue;
        if (OPEN) s.kk[i] = 0;
        else {
            if (!seen[l]) { seen[l] = 1; base[l] = s.kk[i]; }
            int v = s.kk[i] - base[l];
            if (v < -KBIAS || v > (1 << KB) - 1 - KBIAS) { fprintf(stderr, "kk out of range: slot %d v=%d state:", i, v); for (int z = 0; z < K; z++) fprintf(stderr, " %d/%d", s.lab[z], s.kk[z]); fprintf(stderr, "\n"); exit(2); }
            s.kk[i] = (int8_t)v;
        }
        s.lab[i] = map[l];
    }
    return true;
}
static inline int freshlab(const St& s) { int m = OPEN ? 1 : 0; for (int i = 0; i < K; i++) if (s.lab[i] > m) m = s.lab[i]; return m + 1; }

// apply one op; outcome used only for branching ops. returns false if the configuration dies (weight 0).
static bool apply(St& s, const Op& op, int outcome) {
    switch (op.t) {
    case NEWV:
        if (SITE && outcome == 0) { s.lab[op.a] = 0; s.kk[op.a] = 0; return true; }
        s.lab[op.a] = (uint8_t)freshlab(s); s.kk[op.a] = 0; return true;
    case EDGE: {
        if (!SITE && outcome == 0) return true;
        int la = s.lab[op.a], lb = s.lab[op.b];
        if (!la || !lb) return true;
        if (OPEN) {
            if (la == lb) return true;
            int m = (la == 1 || lb == 1) ? 1 : la, o = (m == la) ? lb : la;
            for (int i = 0; i < K; i++) if (s.lab[i] == o) s.lab[i] = (uint8_t)m;
            return true;
        } else {
            if (la == lb) return s.kk[op.b] == s.kk[op.a] + op.dk; // else: winding -> dies
            int shift = s.kk[op.a] + op.dk - s.kk[op.b];
            for (int i = 0; i < K; i++) if (s.lab[i] == lb) { s.lab[i] = (uint8_t)la; s.kk[i] = (int8_t)(s.kk[i] + shift); }
            return true;
        }
    }
    case KILL:
        s.lab[op.a] = 0; s.kk[op.a] = 0;
        if (OPEN) { for (int i = 0; i < K; i++) if (s.lab[i] == 1) return true; return false; }
        return true;
    case PERM: {
        St t; for (int i = 0; i < K; i++) { int src = op.perm[i]; if (src < 0) { t.lab[i] = 0; t.kk[i] = 0; }
                                             else { t.lab[i] = s.lab[src]; t.kk[i] = s.kk[src]; } }
        s = t; return true;
    }
    }
    return true;
}

// ---------------------------------------------------------------- hash table
struct Table {
    std::vector<int32_t> idx; size_t mask = 0;
    std::vector<Key> list;
    static inline uint64_t h(Key k) {
        uint64_t a = (uint64_t)k, b = (uint64_t)(k >> 64);
        uint64_t x = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
        x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32; return x;
    }
    void init(size_t cap) { size_t c = 1; while (c < cap) c <<= 1; idx.assign(c, -1); mask = c - 1; }
    void grow() {
        init((mask + 1) * 2);
        for (size_t i = 0; i < list.size(); i++) { size_t p = h(list[i]) & mask; while (idx[p] >= 0) p = (p + 1) & mask; idx[p] = (int32_t)i; }
    }
    int get(Key k) {
        if ((list.size() + 1) * 10 > (mask + 1) * 7) grow();
        size_t p = h(k) & mask;
        while (idx[p] >= 0) { if (list[idx[p]] == k) return idx[p]; p = (p + 1) & mask; }
        idx[p] = (int32_t)list.size(); list.push_back(k); return idx[p];
    }
    void freehash() { std::vector<int32_t>().swap(idx); std::vector<Key>().swap(list); }
};

// ---------------------------------------------------------------- sector transfer matrix
struct Sector {
    bool open;
    int L;                                  // macro steps per period
    std::vector<std::vector<int32_t>> d0, d1;
    std::vector<size_t> sz;
    std::vector<double> v;                  // eigenvector estimate on step-0 space
    size_t total = 0;
};

static std::vector<int> branchIdx; // op indices of branching ops
static size_t MAXSTATES = getenv("TMMAXSTATES") ? (size_t)atof(getenv("TMMAXSTATES")) : (size_t)150000000; // ~4.5 GB build peak

static bool isBranch(const Op& o) { return (SITE && o.t == NEWV) || (!SITE && o.t == EDGE); }

static void build_sector(Sector& S, bool open) {
    OPEN = open; S.open = open;
    branchIdx.clear();
    for (size_t i = 0; i < OPS.size(); i++) if (isBranch(OPS[i])) branchIdx.push_back(i);
    int L = branchIdx.size(); S.L = L;
    std::vector<Table> T(L);
    for (int j = 0; j < L; j++) T[j].init(1024);
    // initial state at period start, then deterministic ops before first branching op
    St s0; memset(&s0, 0, sizeof s0);
    if (open) { for (int sl : INITSLOTS) s0.lab[sl] = 1; }
    else if (!SITE) { int l = 1; for (int sl : INITSLOTS) s0.lab[sl] = l++; }
    for (int i = 0; i < branchIdx[0]; i++) if (!apply(s0, OPS[i], 1)) { fprintf(stderr, "init dies\n"); exit(1); }
    canon(s0);
    T[0].get(pack(s0));
    S.d0.assign(L, {}); S.d1.assign(L, {});
    std::vector<size_t> done(L, 0); size_t built = 0;
    bool changed = true;
    while (changed) {
        changed = false;
        for (int j = 0; j < L; j++) {
            int jn = (j + 1) % L;
            int bi = branchIdx[j], be = (j + 1 < L) ? branchIdx[j + 1] : (int)OPS.size() + branchIdx[0];
            while (done[j] < T[j].list.size()) {
                changed = true;
                St s; unpack(T[j].list[done[j]], s);
                for (int o = 0; o < 2; o++) {
                    St t = s; bool alive = apply(t, OPS[bi], o);
                    for (int i = bi + 1; alive && i < be; i++) alive = apply(t, OPS[i % OPS.size()], 1);
                    int d = -1;
                    if (alive) { canon(t); d = T[jn].get(pack(t)); }
                    (o ? S.d1[j] : S.d0[j]).push_back(d);
                }
                done[j]++;
                if ((++built & 0xFFFFF) == 0) {
                    size_t tot = 0; for (int z = 0; z < L; z++) tot += T[z].list.size();
                    if (tot > MAXSTATES) { fprintf(stderr, "ABORT: more than %zu states in one sector (memory guard)\n", MAXSTATES); exit(5); }
                }
            }
        }
    }
    S.sz.resize(L); S.total = 0;
    for (int j = 0; j < L; j++) { S.sz[j] = T[j].list.size(); S.total += S.sz[j]; T[j].freehash(); S.d0[j].shrink_to_fit(); S.d1[j].shrink_to_fit(); }
    S.v.assign(S.sz[0], 0.0); S.v[0] = 1.0;
}

static double ITER_TOL = 1e-15;
static int MAXIT = getenv("TMMAXIT") ? atoi(getenv("TMMAXIT")) : 100000;
static long long TOTIT = 0;

// power iteration; returns log Lambda per period
static double lam(Sector& S, double p, int* itout, double* rout) {
    double q = 1.0 - p;
    std::vector<double> cur, nxt;
    double prevl = 0, prevd = 0, r = 0; int it;
    double ll = 0;
    int stable = 0; double bestd = 1e300; int lastImp = 0;
    for (it = 1; it <= MAXIT; it++) {
        cur = S.v;
        for (int j = 0; j < S.L; j++) {
            int jn = (j + 1) % S.L;
            nxt.assign(S.sz[jn], 0.0);
            const int32_t* a = S.d0[j].data(); const int32_t* b = S.d1[j].data();
            size_t n = S.sz[j];
            for (size_t i = 0; i < n; i++) { double x = cur[i]; if (x == 0) continue;
                if (a[i] >= 0) nxt[a[i]] += q * x; if (b[i] >= 0) nxt[b[i]] += p * x; }
            cur.swap(nxt);
        }
        double sum = 0; for (double x : cur) sum += x;
        for (auto& x : cur) x /= sum;
        S.v.swap(cur);
        ll = log(sum); if (getenv("TMDBG") && (it < 3 || it % 500 == 0)) fprintf(stderr, "it %d ll %.17g\n", it, ll);
        double d = fabs(ll - prevl);
        if (it > 2 && prevd > 0) r = d / prevd;
        double est = (r > 0 && r < 1) ? d * r / (1 - r) : d;
        if (r > 0.999) est = d * 1000;
        if (d < bestd * 0.5) { bestd = d; lastImp = it; }
        if (it - lastImp > 40 && bestd < 1e-12) break; // floating-point limit cycle at the noise floor
        if (it > 3 && ((est < ITER_TOL && d < 1e-13) || d < 1e-14)) { if (++stable >= 3) break; } else stable = 0;
        prevd = d; prevl = ll;
    }
    TOTIT += it;
    if (itout) *itout = it; if (rout) *rout = r;
    return ll;
}

static Sector SO, SC;
static int NFEV = 0;
static double fval(double p, bool verbose = false) {
    int io, ic; double ro, rc;
    OPEN = true; double lo = lam(SO, p, &io, &ro);
    OPEN = false; double lc = lam(SC, p, &ic, &rc);
    NFEV++;
    if (verbose) printf("# p=%.17g logLo=%.17g logLc=%.17g f=%.6e it=%d,%d ratio=%.4f,%.4f\n", p, lo, lc, lo - lc, io, ic, ro, rc);
    return lo - lc;
}

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage: tm LATTICE site|bond W root LO HI [tol] | eval P\n"); return 1; }
    std::string lat = argv[1]; SITE = std::string(argv[2]) == "site"; int W = atoi(argv[3]); std::string mode = argv[4];
    Graph g;
    if (lat == "kagome") g = kagome(W);
    else if (lat == "dsq") g = row_word("T", W, false);
    else g = row_word(lat, W, true);
    if (!SITE) { KB = 3; KBIAS = 4; }
    if (mode == "describe") { // degree histogram of the periodic graph built by this program (lattice identity check)
        std::vector<int> deg(g.vs.size(), 0);
        for (auto& e : g.es) { deg[e.u >= 0 ? e.u : -1 - e.u]++; deg[e.v >= 0 ? e.v : -1 - e.v]++; }
        std::vector<int> hist(16, 0); long tot = 0;
        for (int d : deg) { hist[std::min(d, 15)]++; tot += d; }
        printf("DESCRIBE %s W=%d vertices_per_period=%zu edges_per_period=%zu", lat.c_str(), W, g.vs.size(), g.es.size());
        for (int d = 0; d < 16; d++) if (hist[d]) printf(" deg%d:%d", d, hist[d]);
        printf(" zbar=%ld/%zu\n", tot, g.vs.size());
        return 0;
    }
    build_ops(g);
    auto t0 = std::chrono::steady_clock::now();
    build_sector(SO, true);
    build_sector(SC, false);
    auto t1 = std::chrono::steady_clock::now();
    double tb = std::chrono::duration<double>(t1 - t0).count();
    size_t mo = 0, mc = 0; for (auto x : SO.sz) mo = std::max(mo, x); for (auto x : SC.sz) mc = std::max(mc, x);
    printf("# lattice=%s %s W=%d K=%d ops=%zu steps=%d states_open(max)=%zu states_closed(max)=%zu build=%.2fs\n",
           lat.c_str(), SITE ? "site" : "bond", W, K, OPS.size(), SO.L, mo, mc, tb);
    fflush(stdout);
    if (mode == "eval") {
        double p = atof(argv[5]);
        ITER_TOL = 1e-16;
        double f = fval(p, true);
        printf("EVAL %s %s W=%d p=%.17g f=%.6e\n", lat.c_str(), SITE ? "site" : "bond", W, p, f);
        return 0;
    }
    double a = atof(argv[5]), b = atof(argv[6]); double tol = argc > 7 ? atof(argv[7]) : 1e-15;
    double fa = fval(a, true), fb = fval(b, true);
    for (int ex = 0; ex < 12 && fa * fb > 0; ex++) { // expand bracket (f increasing in p)
        double w = b - a;
        if (fa > 0) { b = a; fb = fa; a = a - w; fa = fval(a, true); }
        else { a = b; fa = fb; b = b + w; fb = fval(b, true); }
    }
    if (fa * fb > 0) { printf("NO BRACKET fa=%g fb=%g\n", fa, fb); return 3; }
    // Brent
    double c = a, fc = fa, d = b - a, e = d;
    for (int iter = 0; iter < 100; iter++) {
        if (fb * fc > 0) { c = a; fc = fa; d = b - a; e = d; }
        if (fabs(fc) < fabs(fb)) { a = b; b = c; c = a; fa = fb; fb = fc; fc = fa; }
        double tol1 = 2 * 2.2e-16 * fabs(b) + 0.5 * tol, xm = 0.5 * (c - b);
        if (fabs(xm) <= tol1 || fb == 0) break;
        if (fabs(e) >= tol1 && fabs(fa) > fabs(fb)) {
            double s = fb / fa, pp, qq, r;
            if (a == c) { pp = 2 * xm * s; qq = 1 - s; }
            else { qq = fa / fc; r = fb / fc; pp = s * (2 * xm * qq * (qq - r) - (b - a) * (r - 1)); qq = (qq - 1) * (r - 1) * (s - 1); }
            if (pp > 0) qq = -qq; pp = fabs(pp);
            if (2 * pp < std::min(3 * xm * qq - fabs(tol1 * qq), fabs(e * qq))) { e = d; d = pp / qq; }
            else { d = xm; e = d; }
        } else { d = xm; e = d; }
        a = b; fa = fb;
        b += (fabs(d) > tol1) ? d : (xm > 0 ? tol1 : -tol1);
        fb = fval(b, true);
    }
    auto t2 = std::chrono::steady_clock::now();
    printf("ROOT %s %s W=%d p=%.17g fevals=%d iters=%lld time=%.1fs bracket_other=%.17g\n", lat.c_str(), SITE ? "site" : "bond", W, b,
           NFEV, TOTIT, std::chrono::duration<double>(t2 - t0).count(), c);
    return 0;
}
