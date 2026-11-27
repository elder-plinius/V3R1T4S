// cwbst: seeded bit-swap tabu search for binary constant-weight codes (n <= 64).
//
// The move scheme (pick a pair of words closer than d, move one 1 of one of them to a position where both have 0,
// tabu tenure drawn from [tabu_min, tabu_max], aspiration on a new best penalty, restart after a run without
// improvement) and the hyper-parameter names follow bit-swap-tabu.c by Christopher D. Rosin
// (https://github.com/Constructive-Codes/CWBC, MIT licence, notice in LICENSE-CWBC); starting from a known code is the
// seeded variant described by W. Echols, arXiv:2608.13906. The bitset incidence and incremental conflict/boundary
// masks are this program's own.
//
// usage: cwbst n w d s seed cpu_seconds outfile seedfile [tabu_min tabu_max max_no_improve_restart]
//   seedfile: one word per line as n characters 0/1 ('#' lines ignored; "-" or a missing file = no seed words).
//   The first s distinct weight-w words of seedfile are kept; the rest of the s words are padded with words of least
//   penalty against them (all C(n,w) words when that is cheap, else a random sample), or random words.
// Time is process CPU time, so a SIGSTOPped run loses nothing. Deterministic for a given seed and input.
// stdout, last line: "RESULT FOUND pen 0 ..." (outfile written) or "RESULT NOT_FOUND pen <best penalty> ...";
// penalty = sum over pairs closer than d of (d - distance), so one pair at distance d-2 is penalty 2.
#include <algorithm>
#include <chrono>
#include <climits>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
using u64 = unsigned long long;
static int n, w, d, s, BW;
static u64 FULL;
static vector<u64> cb, bestcb;
static vector<u64> onebits;  // n*BW: bit v set if word v has a 1 at this coordinate
static vector<u64> conf, boundary;  // s*BW symmetric pair masks: distance < d, distance == d
static vector<int> confdeg, confpos, confverts;
static vector<int> tabu_rem, tabu_add;
static vector<u64> padlib;
static string seedfile;
static int basem = 0;
static int penaltyCur = 0, bestPenalty = 0;
static double timelimit;
static int tabu_min = 5, tabu_max = 15, max_no_improve_restart = 100000;
static const size_t PADLIB_MAX = 1u << 20;

static inline int popc(u64 x) { return __builtin_popcountll(x); }
static double cpu0;
static inline double cpunow() {
    timespec t;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}
static inline double elapsed() { return cpunow() - cpu0; }
static inline bool getb(const vector<u64> &a, int idx, int v) { return (a[(size_t)idx * BW + (v >> 6)] >> (v & 63)) & 1ULL; }
static inline void setb(vector<u64> &a, int idx, int v, bool val) {
    u64 &z = a[(size_t)idx * BW + (v >> 6)];
    u64 bit = 1ULL << (v & 63);
    if (val) z |= bit; else z &= ~bit;
}
static inline void setpair(vector<u64> &a, int i, int j, bool val) { setb(a, i, j, val); setb(a, j, i, val); }
static void addconfvert(int v) { if (confpos[v] >= 0) return; confpos[v] = confverts.size(); confverts.push_back(v); }
static void delconfvert(int v) {
    int p = confpos[v]; if (p < 0) return;
    int last = confverts.back(); confverts[p] = last; confpos[last] = p; confverts.pop_back(); confpos[v] = -1;
}
static void edge_update(int i, int j, bool isconf) {
    if (getb(conf, i, j) == isconf) return;
    setpair(conf, i, j, isconf);
    if (isconf) { confdeg[i]++; confdeg[j]++; if (confdeg[i] == 1) addconfvert(i); if (confdeg[j] == 1) addconfvert(j); }
    else { confdeg[i]--; confdeg[j]--; if (confdeg[i] == 0) delconfvert(i); if (confdeg[j] == 0) delconfvert(j); }
}
static void compute_all() {
    fill(conf.begin(), conf.end(), 0); fill(boundary.begin(), boundary.end(), 0);
    fill(confdeg.begin(), confdeg.end(), 0); fill(confpos.begin(), confpos.end(), -1); confverts.clear();
    penaltyCur = 0;
    for (int i = 0; i < s; i++) for (int j = i + 1; j < s; j++) {
        int dd = popc(cb[i] ^ cb[j]);
        if (dd < d) { penaltyCur += d - dd; edge_update(i, j, true); }
        else if (dd == d) setpair(boundary, i, j, true);
    }
}
static u64 random_word(mt19937 &rng) {
    u64 x = 0; int c = 0;
    while (c < w) { int b = rng() % n; if (!((x >> b) & 1)) { x |= 1ULL << b; c++; } }
    return x;
}
static int penalty_against(u64 x, int upto) {
    int pen = 0;
    for (int i = 0; i < upto; i++) { int dd = popc(x ^ cb[i]); if (dd < d) pen += d - dd; }
    return pen;
}
static double binom(int a, int b) { double r = 1; for (int i = 1; i <= b; i++) r = r * (a - b + i) / i; return r; }
static void offer_pad(u64 x, int pen, int &best) {
    if (pen < best) { best = pen; padlib.clear(); }
    if (pen == best && padlib.size() < PADLIB_MAX) padlib.push_back(x);
}
static void build_padlib(mt19937 &rng) {
    if (!padlib.empty() || basem == 0) return;
    int best = INT_MAX;
    unordered_set<u64> ss(cb.begin(), cb.end());
    double total = binom(n, w);
    if (total <= 5e7 && total * basem <= 4e9) {  // every weight-w word, in increasing order (Gosper)
        u64 x = (1ULL << w) - 1;
        while (true) {
            if (!ss.count(x)) offer_pad(x, penalty_against(x, basem), best);
            u64 c = x & (~x + 1), r = x + c;
            if (r == 0) break;
            u64 nx = (((r ^ x) >> 2) / c) | r;
            if ((n < 64 && nx >> n) || nx <= x) break;
            x = nx;
        }
    } else {  // random sample; its own generator so the search stream does not depend on the sample size
        mt19937 r2(rng());
        long k = (long)min(2e6, 4e9 / basem);
        for (long i = 0; i < k; i++) { u64 x = random_word(r2); if (!ss.count(x)) offer_pad(x, penalty_against(x, basem), best); }
    }
    cerr << "padlib size " << padlib.size() << " minpen " << best << " base " << basem << "\n";
}
static void init_state(mt19937 &rng) {
    cb.clear();
    ifstream in(seedfile);
    string line;
    while ((int)cb.size() < s && getline(in, line)) {
        if (line.empty() || line[0] == '#') continue;
        string z;
        for (char c : line) if (c == '0' || c == '1') z.push_back(c);
        if ((int)z.size() != n) continue;
        u64 x = 0; int cnt = 0;
        for (int i = 0; i < n; i++) if (z[i] == '1') { x |= 1ULL << i; cnt++; }
        if (cnt == w && find(cb.begin(), cb.end(), x) == cb.end()) cb.push_back(x);
    }
    basem = cb.size();
    build_padlib(rng);
    while ((int)cb.size() < s) {
        u64 x; int tries = 0;
        do { x = padlib.empty() ? random_word(rng) : padlib[rng() % padlib.size()]; tries++; }
        while (find(cb.begin(), cb.end(), x) != cb.end() && tries < 1000);
        cb.push_back(x);
    }
    fill(onebits.begin(), onebits.end(), 0);
    for (int v = 0; v < s; v++) for (int b = 0; b < n; b++) if ((cb[v] >> b) & 1) setb(onebits, b, v, true);
    fill(tabu_rem.begin(), tabu_rem.end(), 0); fill(tabu_add.begin(), tabu_add.end(), 0);
    compute_all(); bestPenalty = penaltyCur;
}
static void write_code(const string &outfile, const vector<u64> &c) {
    ofstream o(outfile);
    for (int i = 0; i < s; i++) { for (int b = 0; b < n; b++) o << (((c[i] >> b) & 1) ? '1' : '0'); o << '\n'; }
}
static int check_penalty() {
    int z = 0;
    for (int i = 0; i < s; i++) for (int j = i + 1; j < s; j++) { int dd = popc(cb[i] ^ cb[j]); if (dd < d) z += d - dd; }
    return z;
}
static int search(const string &outfile, unsigned seed) {
    mt19937 rng(seed);
    init_state(rng); bestcb = cb;
    long iter = 0, steps = 0, restarts = 0; int noimp = 0; int globalbest = penaltyCur;
    while (true) {
        if (penaltyCur == 0) {
            if (check_penalty() != 0) { printf("RESULT ERROR penalty mismatch at end\n"); return 2; }
            write_code(outfile, cb);
            printf("RESULT FOUND pen 0 steps %ld restarts %ld cpu %.1f\n", steps, restarts, elapsed());
            return 0;
        }
        if (confverts.empty()) { printf("RESULT ERROR no conflicts but penalty %d\n", penaltyCur); return 2; }
        iter++; steps++;
        if ((steps & 1023) == 0 && elapsed() >= timelimit) break;
        // a random conflicted word, then a random word it conflicts with
        int a = confverts[rng() % confverts.size()];
        const u64 *ca = &conf[(size_t)a * BW];
        int deg = confdeg[a]; int pick = rng() % deg; int b = -1, seen = 0;
        for (int wi = 0; wi < BW; wi++) {
            u64 bits = ca[wi];
            while (bits) { int v = wi * 64 + __builtin_ctzll(bits); if (seen++ == pick) { b = v; break; } bits &= bits - 1; }
            if (b >= 0) break;
        }
        if (b < 0) { printf("RESULT ERROR bad conflict pick\n"); return 2; }
        int best_c = -1, best_p = -1, best_q = -1, best_new_pen = INT_MAX; long ties = 0;
        for (int which = 0; which < 2; which++) {
            int c = which ? b : a, o = which ? a : b;
            u64 ck = cb[c], ok = cb[o];
            u64 P = ck & ok, Q = (~ck) & (~ok) & FULL;
            const u64 *cf = &conf[(size_t)c * BW]; const u64 *bd = &boundary[(size_t)c * BW];
            for (int p = 0; p < n; p++) if ((P >> p) & 1) {
                const u64 *bp = &onebits[(size_t)p * BW];
                for (int q = 0; q < n; q++) if ((Q >> q) & 1) {
                    const u64 *bq = &onebits[(size_t)q * BW];
                    int inc = 0, dec = 0;
                    for (int z = 0; z < BW; z++) {
                        u64 notp = ~bp[z];
                        inc += __builtin_popcountll((cf[z] | bd[z]) & bq[z] & notp);
                        dec += __builtin_popcountll(cf[z] & bp[z] & ~bq[z]);
                    }
                    int pen2 = penaltyCur + 2 * (inc - dec);
                    bool tabu = (tabu_rem[c * n + p] > iter || tabu_add[c * n + q] > iter);
                    if (tabu && pen2 >= bestPenalty) continue;
                    if (pen2 < best_new_pen) { best_new_pen = pen2; best_c = c; best_p = p; best_q = q; ties = 1; }
                    else if (pen2 == best_new_pen) { if (rng() % ++ties == 0) { best_c = c; best_p = p; best_q = q; } }
                }
            }
        }
        if (best_c >= 0) {
            int c = best_c, p = best_p, q = best_q;
            u64 newx = cb[c] ^ (1ULL << p) ^ (1ULL << q);
            setb(onebits, p, c, false); setb(onebits, q, c, true);
            cb[c] = newx; penaltyCur = best_new_pen;
            for (int t = 0; t < s; t++) {
                if (t == c) continue;
                int nd = popc(newx ^ cb[t]);
                edge_update(c, t, nd < d);
                bool isb = (nd == d);
                if (isb != getb(boundary, c, t)) setpair(boundary, c, t, isb);
            }
            int ten = tabu_min + (int)(rng() % (tabu_max - tabu_min + 1));
            tabu_rem[c * n + p] = iter + ten; tabu_add[c * n + q] = iter + ten;
        }
        if (penaltyCur < bestPenalty) { bestPenalty = penaltyCur; noimp = 0; } else noimp++;
        if (penaltyCur < globalbest) { globalbest = penaltyCur; bestcb = cb; }
        if (best_c < 0 || noimp >= max_no_improve_restart) { restarts++; init_state(rng); iter = 0; noimp = 0; }
        if ((steps & 1048575) == 0 && check_penalty() != penaltyCur) { printf("RESULT ERROR penalty mismatch\n"); return 2; }
    }
    printf("RESULT NOT_FOUND pen %d steps %ld restarts %ld cpu %.1f\n", globalbest, steps, restarts, elapsed());
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 9) { cerr << "usage: cwbst n w d s seed cpu_seconds outfile seedfile [tabu_min tabu_max max_no_improve_restart]\n"; return 2; }
    n = atoi(argv[1]); w = atoi(argv[2]); d = atoi(argv[3]); s = atoi(argv[4]);
    if (n < 2 || n > 64 || w < 1 || w >= n || s < 2 || d < 2) { cerr << "bad parameters\n"; return 2; }
    unsigned seed = (unsigned)strtoul(argv[5], 0, 0); timelimit = atof(argv[6]); seedfile = argv[8];
    FULL = n == 64 ? ~0ULL : ((1ULL << n) - 1);
    BW = (s + 63) / 64;
    cb.reserve(s); onebits.assign((size_t)n * BW, 0); conf.assign((size_t)s * BW, 0); boundary.assign((size_t)s * BW, 0);
    confdeg.assign(s, 0); confpos.assign(s, -1); tabu_rem.assign((size_t)s * n, 0); tabu_add.assign((size_t)s * n, 0);
    if (argc >= 12) { tabu_min = atoi(argv[9]); tabu_max = atoi(argv[10]); max_no_improve_restart = atoi(argv[11]); }
    cpu0 = cpunow();
    return search(argv[7], seed);
}
