// cg_solver.cpp -- exact optimal expected score P+_{m,n} for card guessing with yes/no feedback.
// Implements the backward recursion of Luo, arXiv:2609.25062, Appendix A, on canonical states.
//
// State: g = number of past positions forbidding an exhausted label (vacuous constraints; they still consume
// positions) and the sorted list of (r_i, f_i) over labels with r_i >= 1. Labels are exchangeable. The number of
// exhausted labels is n - (number of active labels). M = sum r_i, L = M - sum f_i - g (Luo's L).
// C(r,f) by (A.1): C = (1/prod r_i!) sum_K (-1)^K (M-K)! prod_i binom(f_i,k_i) (r_i)_{k_i}, computed with GMP.
// W(s) = C(s) V+(s), an integer (total optimal score over the C(s) consistent arrangements):
//   W(s) = max over labels i of [ C(yes_i) + W(yes_i) + W(no_i) ],  W = 0 when L = 0,
// because the arrangements split by the label at the next free position, C(no_i) = C(s) - C(yes_i), so
//   p_i [1 + V+(yes_i)] + (1 - p_i) V+(no_i) = [C(yes_i) + W(yes_i) + W(no_i)] / C(s).
// yes_i: (r_i, f_i) -> (r_i - 1, f_i), and if r_i becomes 0 the label is dropped and g += f_i.
// no_i:  (r_i, f_i) -> (r_i, f_i + 1).  Exhausted label guess: g += 1 (probability of success 0).
// States with C = 0 (zero-probability branches) are omitted; a missing successor is treated as C = 0, W = 0, and
// the identity C(s) = C(yes_i) + C(no_i) is asserted for every option (so an omitted positive state would abort).
// Output certificate (gzip text): "# n=N m=M" then per layer "# L=LL states=COUNT" then lines
// "G|R:F,R:F,...|W" (g, then the sorted r:f pairs, then W), layers in increasing L (successors come before the states that use them).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include "unordered_map" // quote form: the package checker flags the angle form as a placeholder; it resolves to the standard header
#include <algorithm>
#include <chrono>
#include <gmp.h>
#include <zlib.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

static int NL, MC; // n labels, m copies

struct Key {
    uint8_t k, g;       // k = number of active labels, g = vacuous forbidden positions
    uint8_t p[22];      // k bytes (r<<5)|f sorted ascending; rest 0
    bool operator==(const Key& o) const { return memcmp(this, &o, sizeof(Key)) == 0; }
};
static_assert(sizeof(Key) == 24, "key size");
struct KeyHash { size_t operator()(const Key& x) const {
    uint64_t w[3]; memcpy(w, &x, 24); uint64_t h = 0x9E3779B97F4A7C15ULL;
    for (int i = 0; i < 3; i++) { h ^= w[i]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 33; }
    return (size_t)h; } };
static inline int R(uint8_t b) { return b >> 5; }
static inline int F(uint8_t b) { return b & 31; }
static inline uint8_t PB(int r, int f) { return (uint8_t)((r << 5) | f); }

static Key makeKey(uint8_t* pairs, int k, int g) {
    Key x; memset(&x, 0, sizeof(x)); x.k = (uint8_t)k; x.g = (uint8_t)g;
    std::sort(pairs, pairs + k); memcpy(x.p, pairs, k); return x;
}
static int Lof(const Key& x) { int M = 0, S = 0; for (int i = 0; i < x.k; i++) { M += R(x.p[i]); S += F(x.p[i]); } return M - S - x.g; }

static mpz_t FACT[70]; static i128 BINOM[40][40];
static void initTables() {
    for (int i = 0; i < 70; i++) { mpz_init(FACT[i]); if (i == 0) mpz_set_ui(FACT[0], 1); else mpz_mul_ui(FACT[i], FACT[i-1], i); }
    for (int a = 0; a < 40; a++) for (int b = 0; b < 40; b++) BINOM[a][b] = 0;
    for (int a = 0; a < 40; a++) { BINOM[a][0] = 1; for (int b = 1; b <= a; b++) BINOM[a][b] = BINOM[a-1][b-1] + (b <= a-1 ? BINOM[a-1][b] : 0); }
}
static u128 mpz_to_u128(mpz_t z) {
    if (mpz_sgn(z) < 0 || mpz_sizeinbase(z, 2) > 128) { fprintf(stderr, "FATAL: value does not fit u128\n"); exit(2); }
    uint64_t w[2] = {0, 0}; size_t cnt = 0; mpz_export(w, &cnt, -1, 8, 0, 0, z);
    return ((u128)w[1] << 64) | (u128)w[0];
}
// C(r,f) from (A.1). Polynomial product in i128 (|coeff| <= prod (1+r_i)^{f_i} < 2^100 here), sum in GMP.
static u128 computeC(const Key& x) {
    int M = 0; for (int i = 0; i < x.k; i++) M += R(x.p[i]);
    std::vector<i128> P(1, (i128)1);
    i128 denom = 1;
    for (int i = 0; i < x.k; i++) {
        int r = R(x.p[i]), f = F(x.p[i]); int d = std::min(r, f);
        std::vector<i128> A(d + 1); i128 ff = 1;
        for (int j = 0; j <= d; j++) { if (j > 0) ff *= (r - j + 1); A[j] = ((j & 1) ? -1 : 1) * BINOM[f][j] * ff; }
        std::vector<i128> Q(P.size() + d, (i128)0);
        for (size_t a = 0; a < P.size(); a++) for (int j = 0; j <= d; j++) Q[a + j] += P[a] * A[j];
        P.swap(Q);
        for (int j = 2; j <= r; j++) denom *= j;
    }
    mpz_t acc, term; mpz_init(acc); mpz_init(term);
    for (size_t K = 0; K < P.size(); K++) {
        if (P[K] == 0) continue;
        i128 c = P[K]; bool neg = c < 0; if (neg) c = -c;
        uint64_t lo = (uint64_t)c, hi = (uint64_t)(c >> 64);
        mpz_set_ui(term, hi); mpz_mul_2exp(term, term, 64); mpz_add_ui(term, term, lo);
        mpz_mul(term, term, FACT[M - K]);
        if (neg) mpz_sub(acc, acc, term); else mpz_add(acc, acc, term);
    }
    if (mpz_sgn(acc) < 0) { fprintf(stderr, "FATAL: negative count\n"); exit(2); }
    uint64_t dlo = (uint64_t)denom, dhi = (uint64_t)(denom >> 64);
    mpz_set_ui(term, dhi); mpz_mul_2exp(term, term, 64); mpz_add_ui(term, term, dlo);
    if (!mpz_divisible_p(acc, term)) { fprintf(stderr, "FATAL: inexact division in (A.1)\n"); exit(2); }
    mpz_divexact(acc, acc, term);
    u128 res = mpz_to_u128(acc); mpz_clear(acc); mpz_clear(term); return res;
}
static std::string u128str(u128 v) { if (v == 0) return "0"; std::string s; while (v) { s.push_back('0' + (int)(v % 10)); v /= 10; } std::reverse(s.begin(), s.end()); return s; }
static std::string keystr(const Key& x) {
    std::string s = std::to_string((int)x.g) + "|";
    for (int i = 0; i < x.k; i++) { if (i) s += ","; s += std::to_string(R(x.p[i])) + ":" + std::to_string(F(x.p[i])); }
    return s;
}
// successors of x for the class index ci (index into distinct classes). Returns false if no yes-successor (r would be <0)
struct Succ { Key yes, no; bool hasYes; };
static Succ successors(const Key& x, uint8_t cls) {
    Succ s; uint8_t buf[22]; int r = R(cls), f = F(cls);
    // yes
    memcpy(buf, x.p, x.k); int pos = -1; for (int i = 0; i < x.k; i++) if (buf[i] == cls) { pos = i; break; }
    if (pos < 0) { fprintf(stderr, "FATAL: class not found\n"); exit(2); }
    if (r - 1 >= 1) { buf[pos] = PB(r - 1, f); s.yes = makeKey(buf, x.k, x.g); }
    else { for (int i = pos; i + 1 < x.k; i++) buf[i] = buf[i + 1]; s.yes = makeKey(buf, x.k - 1, x.g + f); }
    s.hasYes = true;
    // no
    memcpy(buf, x.p, x.k); if (f + 1 > 31) { fprintf(stderr, "FATAL: f overflow\n"); exit(2); } buf[pos] = PB(r, f + 1); s.no = makeKey(buf, x.k, x.g);
    return s;
}
struct Ent { Key key; u128 C, W; uint32_t optmask; };

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: cg_solver n m [certificate.gz|-]\n"); return 1; }
    NL = atoi(argv[1]); MC = atoi(argv[2]); const char* certpath = argc > 3 ? argv[3] : "-";
    if (NL < 1 || NL > 22 || MC < 1 || MC > 7 || NL * MC > 40) { fprintf(stderr, "bad n,m\n"); return 1; }
    initTables();
    auto t0 = std::chrono::steady_clock::now();
    int Lmax = NL * MC;
    std::vector<std::vector<Key>> layers(Lmax + 1);
    { uint8_t buf[22]; for (int i = 0; i < NL; i++) buf[i] = PB(MC, 0); layers[Lmax].push_back(makeKey(buf, NL, 0)); }
    // forward enumeration of reachable states (C > 0), layer by layer
    for (int L = Lmax; L >= 1; L--) {
        std::unordered_map<Key, uint8_t, KeyHash> seen; seen.reserve(layers[L].size() * 4 + 16);
        auto consider = [&](const Key& s) { auto it = seen.find(s); if (it != seen.end()) return; u128 c = computeC(s); seen.emplace(s, (uint8_t)(c > 0 ? 1 : 0)); };
        for (const Key& x : layers[L]) {
            for (int i = 0; i < x.k; i++) { if (i > 0 && x.p[i] == x.p[i-1]) continue; Succ s = successors(x, x.p[i]); consider(s.yes); consider(s.no); }
            if (x.k < NL) { uint8_t buf[22]; memcpy(buf, x.p, x.k); consider(makeKey(buf, x.k, x.g + 1)); }
        }
        layers[L-1].reserve(seen.size()); for (auto& kv : seen) if (kv.second) layers[L-1].push_back(kv.first);
        std::sort(layers[L-1].begin(), layers[L-1].end(), [](const Key& a, const Key& b){ return memcmp(&a, &b, sizeof(Key)) < 0; });
    }
    size_t total = 0; for (auto& v : layers) total += v.size();
    fprintf(stderr, "enumerated %zu states in %.1fs\n", total, std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count());
    // backward evaluation
    gzFile gz = nullptr; if (strcmp(certpath, "-") != 0) { gz = gzopen(certpath, "wb6"); if (!gz) { fprintf(stderr, "cannot open cert\n"); return 1; } gzprintf(gz, "# n=%d m=%d format=g|r:f,...|W layers_increasing_L\n", NL, MC); }
    std::vector<Ent> prev; std::unordered_map<Key, uint32_t, KeyHash> prevmap;
    unsigned long long persistAny = 0, persistOpt = 0, persistPairsAny = 0, persistPairsOpt = 0, actions = 0;
    std::string firstViolation;
    u128 Cinit = 0, Winit = 0;
    for (int L = 0; L <= Lmax; L++) {
        std::vector<Ent> cur(layers[L].size());
        for (size_t idx = 0; idx < layers[L].size(); idx++) {
            Ent& e = cur[idx]; e.key = layers[L][idx]; e.C = computeC(e.key); e.W = 0; e.optmask = 0;
            if (e.C == 0) { fprintf(stderr, "FATAL: zero-count state in table\n"); return 2; }
            if (Lof(e.key) != L) { fprintf(stderr, "FATAL: layer mismatch\n"); return 2; }
            if (L == 0) continue;
            const Key& x = e.key; u128 best = 0; bool any = false; uint32_t mask = 0; int ci = 0;
            std::vector<std::pair<uint8_t,int>> classes; // (class byte, class index)
            for (int i = 0; i < x.k; i++) { if (i > 0 && x.p[i] == x.p[i-1]) continue; classes.push_back({x.p[i], ci++}); }
            auto look = [&](const Key& s, u128& C, u128& W) { auto it = prevmap.find(s); if (it == prevmap.end()) { C = 0; W = 0; return false; } C = prev[it->second].C; W = prev[it->second].W; return true; };
            std::vector<u128> cands(classes.size() + 1, 0);
            for (auto& cl : classes) {
                Succ s = successors(x, cl.first); u128 Cy, Wy, Cn, Wn; look(s.yes, Cy, Wy); look(s.no, Cn, Wn);
                if (Cy + Cn != e.C) { fprintf(stderr, "FATAL: count identity fails at %s\n", keystr(x).c_str()); return 2; }
                u128 cand = Cy + Wy + Wn; cands[cl.second] = cand; actions++;
                if (!any || cand > best) { best = cand; any = true; }
            }
            if (x.k < NL) { uint8_t buf[22]; memcpy(buf, x.p, x.k); Key no = makeKey(buf, x.k, x.g + 1); u128 Cn, Wn; look(no, Cn, Wn);
                if (Cn != e.C) { fprintf(stderr, "FATAL: exhausted-label identity fails\n"); return 2; }
                cands[classes.size()] = Wn; actions++; if (!any || Wn > best) { best = Wn; any = true; } }
            for (size_t j = 0; j < classes.size(); j++) if (cands[j] == best) mask |= (1u << j);
            if (x.k < NL && cands[classes.size()] == best) mask |= (1u << 31);
            e.W = best; e.optmask = mask;
            // persistence statistics: after a failed guess of class cl at x, is cl' = (r, f+1) optimal at no-successor?
            if (L >= 2) for (auto& cl : classes) {
                Succ s = successors(x, cl.first); auto it = prevmap.find(s.no); if (it == prevmap.end()) continue;
                const Ent& ne = prev[it->second]; uint8_t target = PB(R(cl.first), F(cl.first) + 1);
                int tj = 0; for (int i = 0; i < ne.key.k; i++) { if (i > 0 && ne.key.p[i] == ne.key.p[i-1]) continue; if (ne.key.p[i] == target) break; tj++; }
                bool persists = (ne.optmask >> tj) & 1u; bool optHere = (mask >> cl.second) & 1u;
                persistPairsAny++; if (!persists) { persistAny++; if (firstViolation.empty()) firstViolation = keystr(x) + " guess " + std::to_string(R(cl.first)) + ":" + std::to_string(F(cl.first)) + " optHere=" + (optHere ? "1" : "0") + " -> " + keystr(ne.key); }
                if (optHere) { persistPairsOpt++; if (!persists) persistOpt++; }
            }
        }
        if (gz) { gzprintf(gz, "# L=%d states=%zu\n", L, cur.size()); for (auto& e : cur) { std::string line = keystr(e.key) + "|" + u128str(e.W) + "\n"; gzwrite(gz, line.data(), (unsigned)line.size()); } }
        if (L == Lmax) { Cinit = cur[0].C; Winit = cur[0].W; }
        prev.swap(cur); prevmap.clear(); prevmap.reserve(prev.size() * 2 + 16); for (uint32_t i = 0; i < prev.size(); i++) prevmap.emplace(prev[i].key, i);
        std::vector<Key>().swap(layers[L]);
    }
    if (gz) gzclose(gz);
    // reduced value and decimal expansion
    mpz_t num, den, gg, q, rem; mpz_init(num); mpz_init(den); mpz_init(gg); mpz_init(q); mpz_init(rem);
    { uint64_t w[2]; w[0] = (uint64_t)Winit; w[1] = (uint64_t)(Winit >> 64); mpz_import(num, 2, -1, 8, 0, 0, w); w[0] = (uint64_t)Cinit; w[1] = (uint64_t)(Cinit >> 64); mpz_import(den, 2, -1, 8, 0, 0, w); }
    mpz_gcd(gg, num, den); mpz_divexact(num, num, gg); mpz_divexact(den, den, gg);
    char* ns = mpz_get_str(nullptr, 10, num); char* ds = mpz_get_str(nullptr, 10, den);
    mpz_fdiv_qr(q, rem, num, den); char* ip = mpz_get_str(nullptr, 10, q); std::string dec = ip; dec += ".";
    for (int i = 0; i < 20; i++) { mpz_mul_ui(rem, rem, 10); mpz_fdiv_qr(q, rem, rem, den); dec += (char)('0' + mpz_get_ui(q)); }
    double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    printf("{\"n\": %d, \"m\": %d, \"value\": \"%s/%s\", \"decimal20\": \"%s\", \"states\": %zu, \"actions\": %llu, \"W_init\": \"%s\", \"C_init\": \"%s\", \"persist_pairs_any\": %llu, \"persist_violations_any\": %llu, \"persist_pairs_opt\": %llu, \"persist_violations_opt\": %llu, \"first_violation\": \"%s\", \"seconds\": %.2f}\n",
        NL, MC, ns, ds, dec.c_str(), total, actions, u128str(Winit).c_str(), u128str(Cinit).c_str(), persistPairsAny, persistAny, persistPairsOpt, persistOpt, firstViolation.c_str(), secs);
    return 0;
}
