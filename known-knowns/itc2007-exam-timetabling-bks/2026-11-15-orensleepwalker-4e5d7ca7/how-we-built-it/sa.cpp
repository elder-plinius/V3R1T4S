// ITC-2007 exam track: simulated annealing from a given timetable.
// Moves: single exam (period and/or room), Kempe chain between two periods (rooms kept, overloaded exams re-roomed),
// whole-period swap. Every move is applied incrementally with exact soft and hard deltas; a move is kept only if
// the hard-violation count is back to 0 and the SA test passes. Final best is written and must be re-scored by check.py.
// Usage: sa <inst> <start.sol> <seconds> <seed> <T0> <out.sol>
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int E, P, R, D;
vector<int> dur, sz, durId, plen, ppen, cap, rpen, pday;
vector<vector<pair<int,int>>> nb;            // neighbour exam, shared students
struct PC { int other; int type; bool first; }; // type 0 coincidence 1 exclusion 2 after
vector<vector<PC>> pcons;
vector<char> excl, largest;
ll w2r, w2d, gsp, wnmd, fa, fb, fw;
vector<int> per, rm;
vector<int> cellLoad, cellCnt, cellExcl; vector<int> cellDurCnt; vector<int> cellDistinct;
vector<vector<int>> perExams; vector<int> posInPer;
ll soft = 0, hard = 0;
const ll BIG = 1;
static inline int cell(int p, int r) { return p * R + r; }

static string trim(const string& s) { size_t a = s.find_first_not_of(" \t\r\n"); if (a == string::npos) return ""; size_t b = s.find_last_not_of(" \t\r\n"); return s.substr(a, b - a + 1); }
static vector<string> split(const string& s) { vector<string> o; string t; stringstream ss(s); while (getline(ss, t, ',')) { t = trim(t); if (!t.empty()) o.push_back(t); } return o; }

void parse(const char* path) {
    ifstream in(path); string line, sec; vector<vector<int>> studs; vector<string> pdays;
    map<string, vector<ll>> w; vector<array<int,3>> phc; vector<int> rex;
    while (getline(in, line)) {
        line = trim(line); if (line.empty()) continue;
        if (line[0] == '[') { sec = line.substr(1, line.find_first_of(":]") - 1); continue; }
        auto f = split(line);
        if (sec == "Exams") { dur.push_back(stoi(f[0])); vector<int> s; for (size_t i = 1; i < f.size(); i++) s.push_back(stoi(f[i])); sort(s.begin(), s.end()); s.erase(unique(s.begin(), s.end()), s.end()); studs.push_back(s); }
        else if (sec == "Periods") { pdays.push_back(f[0]); plen.push_back(stoi(f[2])); ppen.push_back(stoi(f[3])); }
        else if (sec == "Rooms") { cap.push_back(stoi(f[0])); rpen.push_back(stoi(f[1])); }
        else if (sec == "PeriodHardConstraints") { int t = f[1] == "EXAM_COINCIDENCE" ? 0 : f[1] == "EXCLUSION" ? 1 : f[1] == "AFTER" ? 2 : -1; if (t < 0) { cerr << "unknown " << f[1] << endl; exit(2);} phc.push_back({stoi(f[0]), t, stoi(f[2])}); }
        else if (sec == "RoomHardConstraints") { if (f[1] != "ROOM_EXCLUSIVE") { cerr << "unknown room c\n"; exit(2);} rex.push_back(stoi(f[0])); }
        else if (sec == "InstitutionalWeightings") { vector<ll> v; for (size_t i = 1; i < f.size(); i++) v.push_back(stoll(f[i])); w[f[0]] = v; }
    }
    E = dur.size(); P = plen.size(); R = cap.size();
    pday.resize(P); { map<string,int> m; for (int p = 0; p < P; p++) { if (!m.count(pdays[p])) { int k = m.size(); m[pdays[p]] = k; } pday[p] = m[pdays[p]]; } }
    auto g = [&](const string& k, int i) -> ll { return w.count(k) && (int)w[k].size() > i ? w[k][i] : 0; };
    w2r = g("TWOINAROW", 0); w2d = g("TWOINADAY", 0); gsp = g("PERIODSPREAD", 0); wnmd = g("NONMIXEDDURATIONS", 0);
    fa = g("FRONTLOAD", 0); fb = g("FRONTLOAD", 1); fw = g("FRONTLOAD", 2);
    sz.resize(E); for (int e = 0; e < E; e++) sz[e] = studs[e].size();
    { map<int,int> m; durId.resize(E); for (int e = 0; e < E; e++) { if (!m.count(dur[e])) { int k = m.size(); m[dur[e]] = k; } durId[e] = m[dur[e]]; } D = m.size(); }
    // neighbours
    unordered_map<int, vector<int>> bys; for (int e = 0; e < E; e++) for (int s : studs[e]) bys[s].push_back(e);
    vector<unordered_map<int,int>> cnt(E);
    for (auto& kv : bys) { auto& es = kv.second; for (size_t i = 0; i < es.size(); i++) for (size_t j = i + 1; j < es.size(); j++) { cnt[es[i]][es[j]]++; cnt[es[j]][es[i]]++; } }
    nb.resize(E); for (int e = 0; e < E; e++) { for (auto& kv : cnt[e]) nb[e].push_back({kv.first, kv.second}); sort(nb[e].begin(), nb[e].end()); }
    pcons.resize(E); for (auto& c : phc) { pcons[c[0]].push_back({c[2], c[1], true}); pcons[c[2]].push_back({c[0], c[1], false}); }
    excl.assign(E, 0); for (int e : rex) excl[e] = 1;
    vector<int> ord(E); iota(ord.begin(), ord.end(), 0); stable_sort(ord.begin(), ord.end(), [&](int a, int b) { return sz[a] > sz[b]; });
    largest.assign(E, 0); for (int i = 0; i < min<ll>(fa, E); i++) largest[ord[i]] = 1;
}

// pair cost between periods p and q (shared k students): returns soft, adds hard
static inline ll pairSoft(int p, int q, int k, ll& h) {
    if (p == q) { h += k; return 0; }
    ll c = 0; int d = abs(p - q);
    if (pday[p] == pday[q]) c += (d == 1 ? w2r : w2d) * k;
    if (d <= gsp) c += k;
    return c;
}
static inline ll cellSoft(int c) { return cellDistinct[c] > 0 ? (cellDistinct[c] - 1) * wnmd : 0; }
static inline ll cellHard(int c, int r) { ll h = 0; if (cellLoad[c] > cap[r]) h++; if (cellExcl[c] > 0 && cellCnt[c] > 1) h += cellExcl[c]; return h; }
static inline ll pcHard(int e, int p, int fp, const PC& c) {
    if (c.type == 0) return p != fp; if (c.type == 1) return p == fp;
    return c.first ? !(p > fp) : !(fp > p);
}
static inline ll singleSoft(int e, int p, int r) { return ppen[p] + rpen[r] + ((largest[e] && p >= P - fb) ? fw : 0); }

void cellAdd(int e, int p, int r, int s) {
    int c = cell(p, r); cellLoad[c] += s * sz[e]; cellCnt[c] += s; cellExcl[c] += s * excl[e];
    int& dc = cellDurCnt[c * D + durId[e]];
    if (s > 0) { if (dc == 0) cellDistinct[c]++; dc++; } else { dc--; if (dc == 0) cellDistinct[c]--; }
}
// move exam e to (p,r), update soft/hard exactly
void moveExam(int e, int p, int r) {
    int p0 = per[e], r0 = rm[e]; if (p0 == p && r0 == r) return;
    ll ds = 0, dh = 0;
    if (p0 != p) {
        for (auto& [f, k] : nb[e]) { ll h0 = 0, h1 = 0; ds += pairSoft(p, per[f], k, h1) - pairSoft(p0, per[f], k, h0); dh += h1 - h0; }
        for (auto& c : pcons[e]) dh += pcHard(e, p, per[c.other], c) - pcHard(e, p0, per[c.other], c);
        dh += (dur[e] > plen[p]) - (dur[e] > plen[p0]);
        // period lists
        auto& L = perExams[p0]; int i = posInPer[e]; L[i] = L.back(); posInPer[L[i]] = i; L.pop_back();
        posInPer[e] = perExams[p].size(); perExams[p].push_back(e);
    }
    ds += singleSoft(e, p, r) - singleSoft(e, p0, r0);
    int c0 = cell(p0, r0), c1 = cell(p, r);
    ds -= cellSoft(c0) + cellSoft(c1); dh -= cellHard(c0, r0) + cellHard(c1, r);
    cellAdd(e, p0, r0, -1); per[e] = p; rm[e] = r; cellAdd(e, p, r, +1);
    ds += cellSoft(c0) + cellSoft(c1); dh += cellHard(c0, r0) + cellHard(c1, r);
    soft += ds; hard += dh;
}
ll fullCost(ll& h) {
    // recompute from scratch for verification
    h = 0; ll s = 0;
    for (int e = 0; e < E; e++) { for (auto& [f, k] : nb[e]) if (f > e) s += pairSoft(per[e], per[f], k, h); s += singleSoft(e, per[e], rm[e]); h += dur[e] > plen[per[e]]; for (auto& c : pcons[e]) if (c.first) h += pcHard(e, per[e], per[c.other], c); }
    for (int p = 0; p < P; p++) for (int r = 0; r < R; r++) { int c = cell(p, r); s += cellSoft(c); h += cellHard(c, r); }
    return s;
}
mt19937_64 rng;
static inline int rnd(int n) { return uniform_int_distribution<int>(0, n - 1)(rng); }
static inline double U() { return uniform_real_distribution<double>(0, 1)(rng); }

vector<array<int,3>> undo; // e, oldp, oldr
void doMove(int e, int p, int r) { undo.push_back({e, per[e], rm[e]}); moveExam(e, p, r); }
void rollback(size_t to) { while (undo.size() > to) { auto u = undo.back(); undo.pop_back(); moveExam(u[0], u[1], u[2]); } }

// re-room exams in overloaded/exclusive-violated cells among 'moved', choosing room minimising (hard, soft)
void repairRooms(const vector<int>& moved) {
    for (int e : moved) {
        int p = per[e], c = cell(p, rm[e]);
        if (cellHard(c, rm[e]) == 0) continue;
        int bestR = rm[e]; ll bh = LLONG_MAX, bs = LLONG_MAX;
        for (int r = 0; r < R; r++) {
            ll h0 = hard, s0 = soft; size_t u = undo.size(); doMove(e, p, r);
            if (hard < bh || (hard == bh && soft < bs)) { bh = hard; bs = soft; bestR = r; }
            rollback(u); (void)h0; (void)s0;
        }
        doMove(e, p, bestR);
    }
}
bool kempe(int e, int p2, vector<int>& moved) {
    int p1 = per[e]; if (p1 == p2) return false;
    vector<int> st{e}; unordered_set<int> in{e}; moved.clear();
    while (!st.empty()) {
        int x = st.back(); st.pop_back(); moved.push_back(x);
        int other = per[x] == p1 ? p2 : p1;
        for (auto& [f, k] : nb[x]) if (per[f] == other && !in.count(f)) { in.insert(f); st.push_back(f); }
        if ((int)moved.size() > E) return false;
    }
    vector<pair<int,int>> tgt; for (int x : moved) tgt.push_back({x, per[x] == p1 ? p2 : p1});
    for (auto& [x, q] : tgt) doMove(x, q, rm[x]);
    return true;
}
int main(int argc, char** argv) {
    if (argc < 7) { cerr << "usage\n"; return 1; }
    parse(argv[1]); double secs = atof(argv[3]); rng.seed(atoll(argv[4])); double T0 = atof(argv[5]);
    // start
    per.assign(E, 0); rm.assign(E, 0);
    { ifstream in(argv[2]); string line; int e = 0; while (getline(in, line)) { line = trim(line); if (line.empty() || line[0] == '{' || line[0] == '#') continue; auto f = split(line); per[e] = stoi(f[0]); rm[e] = stoi(f[1]); e++; } if (e != E) { cerr << "bad sol\n"; return 1; } }
    cellLoad.assign(P * R, 0); cellCnt.assign(P * R, 0); cellExcl.assign(P * R, 0); cellDurCnt.assign(P * R * D, 0); cellDistinct.assign(P * R, 0);
    perExams.assign(P, {}); posInPer.assign(E, 0);
    for (int e = 0; e < E; e++) { cellAdd(e, per[e], rm[e], +1); posInPer[e] = perExams[per[e]].size(); perExams[per[e]].push_back(e); }
    soft = fullCost(hard); ll startSoft = soft;
    if (hard != 0) { cerr << "start infeasible hard=" << hard << endl; return 1; }
    vector<int> bestP = per, bestR = rm; ll best = soft;
    auto t0 = chrono::steady_clock::now(); ll it = 0, acc = 0, nk = 0, nka = 0; double T = T0, el = 0;
    vector<int> moved; ll lastImp = 0;
    while (true) {
        if ((it & 1023) == 0) { el = chrono::duration<double>(chrono::steady_clock::now() - t0).count(); if (el > secs) break; double fr = el / secs; T = T0 * pow(0.01, fr); }
        it++;
        ll s0 = soft; size_t u = undo.size(); double mv = U(); bool isK = false;
        if (mv < 0.55) { int e = rnd(E); int p = U() < 0.8 ? rnd(P) : per[e]; int r = rnd(R); doMove(e, p, r); if (hard) { /* try repair other rooms */ } }
        else if (mv < 0.97) { isK = true; nk++; int e = rnd(E); int p2 = rnd(P); if (!kempe(e, p2, moved)) { rollback(u); continue; } if (hard) repairRooms(moved); }
        else { int p1 = rnd(P), p2 = rnd(P); if (p1 == p2) continue; vector<int> a = perExams[p1], b = perExams[p2]; for (int x : a) doMove(x, p2, rm[x]); for (int x : b) doMove(x, p1, rm[x]); }
        ll d = soft - s0;
        if (hard == 0 && (d <= 0 || U() < exp(-d / max(T, 1e-9)))) { acc++; if (isK) nka++; undo.resize(u); if (soft < best) { best = soft; bestP = per; bestR = rm; lastImp = it; } }
        else rollback(u);
        undo.resize(u);
    }
    // verify best by full recompute
    for (int e = 0; e < E; e++) moveExam(e, bestP[e], bestR[e]);
    ll h; ll full = fullCost(h);
    ofstream o(argv[6]); for (int e = 0; e < E; e++) o << bestP[e] << ", " << bestR[e] << "\n";
    printf("{\"start\": %lld, \"best\": %lld, \"full\": %lld, \"hard\": %lld, \"iters\": %lld, \"acc\": %lld, \"kempe\": %lld, \"kempe_acc\": %lld, \"T0\": %g, \"secs\": %.1f, \"seed\": %s}\n",
           startSoft, best, full, h, it, acc, nk, nka, T0, el, argv[4]);
}
