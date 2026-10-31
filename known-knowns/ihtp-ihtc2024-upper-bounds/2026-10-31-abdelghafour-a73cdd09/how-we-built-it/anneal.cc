// IHTP simulated annealing, warm-started from a feasible solution. Our own code, written from the
// validator's cost definitions. Usage: anneal in.flat out_best.txt seconds seed
// Keeps the state hard-feasible at all times (moves that create any violation are undone).
// Every unit cost is recomputed from scratch when touched, so deltas cannot drift from a full evaluation;
// the final best is rebuilt and fully re-evaluated as a self-check.
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <fstream>
using namespace std;

int D, SPD, R, T, U, P, O, N, NS, Q; int w[8];
vector<int> cap, mand, gen, age_, los, rel, last_, dur, surg, occroom, lvl;
vector<vector<int>> avail, maxs, wl, sk, maxload, avn;
vector<vector<char>> incompat;
// state
vector<int> adm, room, ot;
vector<vector<vector<int>>> rd, nrooms, uth;
vector<vector<int>> nurse, otload, otcnt, uload;
// unit costs: 0 roomday, 1 nurseshift, 2 continuity, 3 otday, 4 surgday, 5 patient
vector<long long> uh[6], us[6]; vector<int> stamp[6]; int curstamp = 1;
long long H = 0, S = 0;
mt19937_64 rng;
int rnd(int n) { return (int)(rng() % (unsigned long long)n); }
double urand() { return (rng() >> 11) * (1.0 / 9007199254740992.0); }

inline int st(int q) { return q < P ? adm[q] : 0; }
inline int rm(int q) { return q < P ? room[q] : occroom[q - P]; }

void calc(int ty, int id, long long &h, long long &s) {
  h = 0; s = 0;
  if (ty == 0) {
    int r = id / D, d = id % D; auto &L = rd[r][d];
    int a = 0, b = 0, mn = 1 << 30, mx = -1;
    for (int q : L) { if (gen[q]) a++; else b++; mn = min(mn, age_[q]); mx = max(mx, age_[q]); }
    h += min(a, b) + max(0, (int)L.size() - cap[r]);
    if (!L.empty()) s += (long long)w[0] * (mx - mn);
    for (int sh = d * SPD; sh < (d + 1) * SPD; sh++) {
      int n = nurse[r][sh];
      if (n == -1) { if (!L.empty()) h++; continue; }
      for (int q : L) { int req = sk[q][sh - st(q) * SPD]; if (req > lvl[n]) s += (long long)w[1] * (req - lvl[n]); }
    }
  } else if (ty == 1) {
    int n = id / NS, sh = id % NS; if (maxload[n][sh] < 0) return;
    int load = 0, d = sh / SPD;
    for (int r : nrooms[n][sh]) for (int q : rd[r][d]) load += wl[q][sh - st(q) * SPD];
    if (load > maxload[n][sh]) s = (long long)w[3] * (load - maxload[n][sh]);
  } else if (ty == 2) {
    int q = id; if (q < P && adm[q] < 0) return;
    static vector<int> tag; static int tg = 0; if ((int)tag.size() < N) tag.assign(N, 0); tg++;
    int c = 0, s0 = st(q), r = rm(q);
    for (int d = s0; d < min(D, s0 + los[q]); d++) for (int sh = d * SPD; sh < (d + 1) * SPD; sh++) {
      int n = nurse[r][sh]; if (n != -1 && tag[n] != tg) { tag[n] = tg; c++; }
    }
    s = (long long)w[2] * c;
  } else if (ty == 3) {
    int t = id / D, d = id % D;
    h = max(0, otload[t][d] - avail[t][d]); s = otcnt[t][d] > 0 ? w[4] : 0;
  } else if (ty == 4) {
    int u = id / D, d = id % D, c = 0;
    h = max(0, uload[u][d] - maxs[u][d]);
    for (int t = 0; t < T; t++) if (uth[u][d][t] > 0) c++;
    s = (long long)w[5] * max(0, c - 1);
  } else {
    int p = id;
    if (adm[p] < 0) { if (mand[p]) h = 1; else s = w[7]; return; }
    h = (adm[p] < rel[p] || adm[p] > last_[p]) + incompat[p][room[p]];
    s = (long long)w[6] * max(0, adm[p] - rel[p]);
  }
}

struct Saved { int ty, id; long long h, s; };
vector<Saved> touched;
void touch(int ty, int id) {
  if (stamp[ty][id] == curstamp) return;
  stamp[ty][id] = curstamp; touched.push_back({ty, id, uh[ty][id], us[ty][id]});
}
// undo log
struct Op { int kind, a, b, c, d; }; // kind 0: was placed (p,d,r,t) -> re-place; 1: was unplaced (p) -> unplace; 2: nurse (r,s,old)
vector<Op> undo;

void touchRoomShiftNurse(int r, int sh) { if (nurse[r][sh] != -1) touch(1, nurse[r][sh] * NS + sh); }
void touchPatient(int p) {
  touch(2, p); touch(5, p);
  if (adm[p] < 0) return;
  for (int d = adm[p]; d < min(D, adm[p] + los[p]); d++) {
    touch(0, room[p] * D + d);
    for (int sh = d * SPD; sh < (d + 1) * SPD; sh++) touchRoomShiftNurse(room[p], sh);
  }
  touch(3, ot[p] * D + adm[p]); touch(4, surg[p] * D + adm[p]);
}
void rawPlace(int p, int d, int r, int t) {
  adm[p] = d; room[p] = r; ot[p] = t;
  for (int dd = d; dd < min(D, d + los[p]); dd++) rd[r][dd].push_back(p);
  otload[t][d] += dur[p]; otcnt[t][d]++; uload[surg[p]][d] += dur[p]; uth[surg[p]][d][t]++;
}
void rawUnplace(int p) {
  int d = adm[p], r = room[p], t = ot[p];
  for (int dd = d; dd < min(D, d + los[p]); dd++) { auto &L = rd[r][dd]; auto it = find(L.begin(), L.end(), p); *it = L.back(); L.pop_back(); }
  otload[t][d] -= dur[p]; otcnt[t][d]--; uload[surg[p]][d] -= dur[p]; uth[surg[p]][d][t]--;
  adm[p] = room[p] = ot[p] = -1;
}
void rawNurse(int r, int sh, int n) {
  int o = nurse[r][sh];
  if (o != -1) { auto &L = nrooms[o][sh]; L.erase(find(L.begin(), L.end(), r)); }
  nurse[r][sh] = n; if (n != -1) nrooms[n][sh].push_back(r);
}
void opNurse(int r, int sh, int n) {
  int d = sh / SPD;
  touch(0, r * D + d); touchRoomShiftNurse(r, sh); if (n != -1) touch(1, n * NS + sh);
  for (int q : rd[r][d]) touch(2, q);
  undo.push_back({2, r, sh, nurse[r][sh], 0});
  rawNurse(r, sh, n);
}
void opUnplace(int p) {
  touchPatient(p);
  undo.push_back({0, p, adm[p], room[p], ot[p]});
  rawUnplace(p);
}
void opPlace(int p, int d, int r, int t) {
  for (int dd = d; dd < min(D, d + los[p]); dd++)
    for (int sh = dd * SPD; sh < (dd + 1) * SPD; sh++)
      if (nurse[r][sh] == -1 && !avn[sh].empty()) opNurse(r, sh, avn[sh][rnd(avn[sh].size())]);
  undo.push_back({1, p, 0, 0, 0});
  rawPlace(p, d, r, t);
  touchPatient(p);
}
void begin() { curstamp++; touched.clear(); undo.clear(); }
long long evalDelta() {
  long long dH = 0, dS = 0;
  for (auto &x : touched) { long long h, s; calc(x.ty, x.id, h, s); dH += h - uh[x.ty][x.id]; dS += s - us[x.ty][x.id]; uh[x.ty][x.id] = h; us[x.ty][x.id] = s; }
  H += dH; S += dS; return dS;
}
void rollback() {
  for (int i = (int)undo.size() - 1; i >= 0; i--) {
    Op &o = undo[i];
    if (o.kind == 0) rawPlace(o.a, o.b, o.c, o.d);
    else if (o.kind == 1) rawUnplace(o.a);
    else rawNurse(o.a, o.b, o.c);
  }
  for (auto &x : touched) { H += x.h - uh[x.ty][x.id]; S += x.s - us[x.ty][x.id]; uh[x.ty][x.id] = x.h; us[x.ty][x.id] = x.s; }
}

vector<int> bAdm, bRoom, bOt; vector<vector<int>> bNurse;
void build(const vector<int> &A, const vector<int> &Rm, const vector<int> &Ot, const vector<vector<int>> &Nu) {
  adm.assign(P, -1); room.assign(P, -1); ot.assign(P, -1);
  rd.assign(R, vector<vector<int>>(D)); nrooms.assign(N, vector<vector<int>>(NS));
  nurse.assign(R, vector<int>(NS, -1));
  otload.assign(T, vector<int>(D, 0)); otcnt = otload; uload.assign(U, vector<int>(D, 0));
  uth.assign(U, vector<vector<int>>(D, vector<int>(T, 0)));
  for (int o = 0; o < O; o++) for (int d = 0; d < los[P + o] && d < D; d++) rd[occroom[o]][d].push_back(P + o);
  for (int p = 0; p < P; p++) if (A[p] >= 0) rawPlace(p, A[p], Rm[p], Ot[p]);
  for (int r = 0; r < R; r++) for (int sh = 0; sh < NS; sh++) if (Nu[r][sh] != -1) rawNurse(r, sh, Nu[r][sh]);
  int sizes[6] = {R * D, N * NS, Q, T * D, U * D, P};
  H = S = 0;
  for (int ty = 0; ty < 6; ty++) {
    uh[ty].assign(sizes[ty], 0); us[ty].assign(sizes[ty], 0); stamp[ty].assign(sizes[ty], 0);
    for (int i = 0; i < sizes[ty]; i++) { calc(ty, i, uh[ty][i], us[ty][i]); H += uh[ty][i]; S += us[ty][i]; }
  }
}
void saveBest() { bAdm = adm; bRoom = room; bOt = ot; bNurse = nurse; }
void writeBest(const char *fn) {
  FILE *f = fopen((string(fn) + ".tmp").c_str(), "w");
  for (int p = 0; p < P; p++) fprintf(f, "%d %d %d\n", bAdm[p], bRoom[p], bOt[p]);
  for (int r = 0; r < R; r++) { for (int sh = 0; sh < NS; sh++) fprintf(f, "%d ", bNurse[r][sh]); fprintf(f, "\n"); }
  fclose(f); rename((string(fn) + ".tmp").c_str(), fn);
}

int randomOT(int d) { int t = rnd(T); for (int k = 0; k < T; k++, t = (t + 1) % T) if (avail[t][d] > 0) return t; return -1; }

// one move; returns false if nothing was attempted
bool move() {
  int k = rnd(100);
  if (k < 40) { // nurse change on a room-shift, often to a nurse the room's patients already have
    int r = rnd(R), sh = rnd(NS), d = sh / SPD;
    if (rd[r][d].empty() || avn[sh].size() < 2) return false;
    int n = avn[sh][rnd(avn[sh].size())];
    if (rnd(2)) { int q = rd[r][d][rnd(rd[r][d].size())]; int s0 = st(q), l = min(D, s0 + los[q]) - s0;
      int sh2 = (s0 + rnd(l)) * SPD + rnd(SPD); int n2 = nurse[rm(q)][sh2]; if (n2 != -1 && maxload[n2][sh] >= 0) n = n2; }
    if (n == nurse[r][sh]) return false;
    opNurse(r, sh, n);
  } else if (k < 55) { // swap nurses of two rooms in one shift
    int sh = rnd(NS), r1 = rnd(R), r2 = rnd(R), d = sh / SPD;
    if (r1 == r2 || (rd[r1][d].empty() && rd[r2][d].empty())) return false;
    int n1 = nurse[r1][sh], n2 = nurse[r2][sh]; if (n1 == n2) return false;
    opNurse(r1, sh, n2); opNurse(r2, sh, n1);
  } else if (k < 70) { // patient room change
    int p = rnd(P); if (adm[p] < 0) return false;
    int r = rnd(R); if (r == room[p] || incompat[p][r]) return false;
    int d = adm[p], t = ot[p]; opUnplace(p); opPlace(p, d, r, t);
  } else if (k < 80) { // swap rooms of two patients
    int p = rnd(P), q = rnd(P); if (p == q || adm[p] < 0 || adm[q] < 0 || room[p] == room[q]) return false;
    int dp = adm[p], rp = room[p], tp = ot[p], dq = adm[q], rq = room[q], tq = ot[q];
    if (incompat[p][rq] || incompat[q][rp]) return false;
    opUnplace(p); opUnplace(q); opPlace(p, dp, rq, tp); opPlace(q, dq, rp, tq);
  } else if (k < 86) { // operating theatre change
    int p = rnd(P); if (adm[p] < 0) return false;
    int t = randomOT(adm[p]); if (t < 0 || t == ot[p]) return false;
    int d = adm[p], r = room[p]; opUnplace(p); opPlace(p, d, r, t);
  } else if (k < 95) { // admission day change (same room)
    int p = rnd(P); if (adm[p] < 0) return false;
    int d = rel[p] + rnd(last_[p] - rel[p] + 1); if (d == adm[p] || d >= D) return false;
    int t = avail[ot[p]][d] > 0 && rnd(2) ? ot[p] : randomOT(d); if (t < 0) return false;
    int r = room[p]; if (rnd(3) == 0) { r = rnd(R); if (incompat[p][r]) return false; }
    opUnplace(p); opPlace(p, d, r, t);
  } else { // schedule / unschedule an elective patient
    int p = rnd(P); if (mand[p]) return false;
    if (adm[p] >= 0) opUnplace(p);
    else { int d = rel[p] + rnd(D - rel[p]); int r = rnd(R); if (incompat[p][r]) return false;
      int t = randomOT(d); if (t < 0) return false; opPlace(p, d, r, t); }
  }
  return true;
}

int main(int argc, char **argv) {
  if (argc != 5) { fprintf(stderr, "usage: anneal in.flat out_best.txt seconds seed\n"); return 1; }
  ifstream in(argv[1]); double secs = atof(argv[3]); rng.seed(atoll(argv[4]));
  in >> D >> SPD >> R >> T >> U >> P >> O >> N; NS = D * SPD; Q = P + O;
  for (int i = 0; i < 8; i++) in >> w[i];
  cap.resize(R); for (auto &x : cap) in >> x;
  avail.assign(T, vector<int>(D)); for (auto &v : avail) for (auto &x : v) in >> x;
  maxs.assign(U, vector<int>(D)); for (auto &v : maxs) for (auto &x : v) in >> x;
  mand.resize(P); rel.resize(P); last_.resize(P); dur.resize(P); surg.resize(P); incompat.assign(P, vector<char>(R));
  gen.resize(Q); age_.resize(Q); los.resize(Q); wl.resize(Q); sk.resize(Q); occroom.resize(O);
  for (int p = 0; p < P; p++) {
    in >> mand[p] >> gen[p] >> age_[p] >> los[p] >> rel[p] >> last_[p] >> dur[p] >> surg[p];
    for (int r = 0; r < R; r++) { int x; in >> x; incompat[p][r] = x; }
    wl[p].resize(los[p] * SPD); sk[p].resize(los[p] * SPD);
    for (auto &x : wl[p]) in >> x; for (auto &x : sk[p]) in >> x;
  }
  for (int o = 0; o < O; o++) {
    int q = P + o; in >> gen[q] >> age_[q] >> los[q] >> occroom[o];
    wl[q].resize(los[q] * SPD); sk[q].resize(los[q] * SPD);
    for (auto &x : wl[q]) in >> x; for (auto &x : sk[q]) in >> x;
  }
  lvl.resize(N); maxload.assign(N, vector<int>(NS)); avn.assign(NS, {});
  for (int n = 0; n < N; n++) { in >> lvl[n]; for (int sh = 0; sh < NS; sh++) { in >> maxload[n][sh]; if (maxload[n][sh] >= 0) avn[sh].push_back(n); } }
  vector<int> A(P), Rm(P), Ot(P); vector<vector<int>> Nu(R, vector<int>(NS));
  for (int p = 0; p < P; p++) in >> A[p] >> Rm[p] >> Ot[p];
  for (auto &v : Nu) for (auto &x : v) in >> x;
  if (!in) { fprintf(stderr, "bad input\n"); return 1; }

  build(A, Rm, Ot, Nu);
  printf("start H=%lld S=%lld\n", H, S); fflush(stdout);
  if (H != 0) { fprintf(stderr, "start not feasible\n"); return 2; }
  saveBest(); long long best = S; writeBest(argv[2]);
  auto t0 = chrono::steady_clock::now();
  auto el = [&] { return chrono::duration<double>(chrono::steady_clock::now() - t0).count(); };
  const double cycle = 30.0, T0 = 6.0, T1 = 0.2;
  long long it = 0, acc = 0; double lastw = 0;
  while (el() < secs) {
    double c0 = el(); build(bAdm, bRoom, bOt, bNurse);
    while (true) {
      double e = el(); if (e >= secs) break; double f = (e - c0) / cycle; if (f >= 1) break;
      double temp = T0 * pow(T1 / T0, f);
      for (int k = 0; k < 2000; k++) {
        begin(); if (!move()) { rollback(); continue; }
        long long dS = evalDelta(); it++;
        if (H == 0 && (dS <= 0 || urand() < exp(-dS / temp))) {
          acc++;
          if (S < best) { best = S; saveBest(); }
        } else rollback();
      }
      if (el() - lastw > 20) { writeBest(argv[2]); lastw = el(); printf("t=%.0f best=%lld cur=%lld it=%lld acc=%lld\n", el(), best, S, it, acc); fflush(stdout); }
    }
  }
  writeBest(argv[2]);
  build(bAdm, bRoom, bOt, bNurse);
  printf("final best=%lld rebuilt H=%lld S=%lld it=%lld %s\n", best, H, S, it, (S == best && H == 0) ? "SELFCHECK_OK" : "SELFCHECK_FAIL");
  return (S == best && H == 0) ? 0 : 3;
}
