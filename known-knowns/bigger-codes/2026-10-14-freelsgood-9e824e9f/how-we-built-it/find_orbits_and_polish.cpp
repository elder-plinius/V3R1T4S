#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <cstring>
#include <algorithm>
#include <random>
#include <chrono>

using namespace std;

const int N = 27;
const int W = 10;
uint8_t* cnt;
uint64_t* in_code;

inline void set_in_code(uint32_t m) { in_code[m >> 6] |= (1ULL << (m & 63)); }
inline void clr_in_code(uint32_t m) { in_code[m >> 6] &= ~(1ULL << (m & 63)); }
inline bool get_in_code(uint32_t m) { return (in_code[m >> 6] >> (m & 63)) & 1ULL; }
inline void inc_c(uint32_t m) { if (cnt[m] < 255) cnt[m]++; }
inline int overlap(uint32_t a, uint32_t b) { return __builtin_popcount(a & b); }
inline int dist(uint32_t a, uint32_t b) { return __builtin_popcount(a ^ b); }

void add_word(uint32_t x) {
    set_in_code(x);
    inc_c(x);
    int ones[27], zeros[27], no = 0, nz = 0;
    for (int i = 0; i < N; ++i) if ((x >> i) & 1) ones[no++] = i; else zeros[nz++] = i;
    for (int i = 0; i < no; ++i) {
        uint32_t x1 = x ^ (1U << ones[i]);
        for (int k = 0; k < nz; ++k) inc_c(x1 | (1U << zeros[k]));
    }
    for (int i = 0; i < no; ++i)
        for (int j = i + 1; j < no; ++j) {
            uint32_t base = x ^ (1U << ones[i]) ^ (1U << ones[j]);
            for (int k = 0; k < nz; ++k)
                for (int l = k + 1; l < nz; ++l)
                    inc_c(base | (1U << zeros[k]) | (1U << zeros[l]));
        }
}

void remove_word(uint32_t x, vector<uint32_t>& zero_cands, vector<uint32_t>& new_c1, vector<uint32_t>& new_c2) {
    clr_in_code(x);
    if (--cnt[x] == 0) zero_cands.push_back(x);
    int ones[27], zeros[27], no = 0, nz = 0;
    for (int i = 0; i < N; ++i) if ((x >> i) & 1) ones[no++] = i; else zeros[nz++] = i;
    for (int i = 0; i < no; ++i) {
        uint32_t x1 = x ^ (1U << ones[i]);
        for (int k = 0; k < nz; ++k) {
            uint32_t z = x1 | (1U << zeros[k]);
            uint8_t v = --cnt[z];
            if (v == 0) zero_cands.push_back(z);
            else if (v == 1) new_c1.push_back(z);
            else if (v == 2) new_c2.push_back(z);
        }
    }
    for (int i = 0; i < no; ++i)
        for (int j = i + 1; j < no; ++j) {
            uint32_t base = x ^ (1U << ones[i]) ^ (1U << ones[j]);
            for (int k = 0; k < nz; ++k)
                for (int l = k + 1; l < nz; ++l) {
                    uint32_t z = base | (1U << zeros[k]) | (1U << zeros[l]);
                    uint8_t v = --cnt[z];
                    if (v == 0) zero_cands.push_back(z);
                    else if (v == 1) new_c1.push_back(z);
                    else if (v == 2) new_c2.push_back(z);
                }
        }
}

void find_conflicts_in_code(uint32_t y, vector<uint32_t>& out) {
    out.clear();
    if (get_in_code(y)) out.push_back(y);
    int ones[27], zeros[27], no = 0, nz = 0;
    for (int i = 0; i < N; ++i) if ((y >> i) & 1) ones[no++] = i; else zeros[nz++] = i;
    for (int i = 0; i < no; ++i) {
        uint32_t y1 = y ^ (1U << ones[i]);
        for (int k = 0; k < nz; ++k) {
            uint32_t z = y1 | (1U << zeros[k]);
            if (get_in_code(z)) out.push_back(z);
        }
    }
    for (int i = 0; i < no; ++i)
        for (int j = i + 1; j < no; ++j) {
            uint32_t base = y ^ (1U << ones[i]) ^ (1U << ones[j]);
            for (int k = 0; k < nz; ++k)
                for (int l = k + 1; l < nz; ++l) {
                    uint32_t z = base | (1U << zeros[k]) | (1U << zeros[l]);
                    if (get_in_code(z)) out.push_back(z);
                }
        }
}

void collect_low(int idx, int w_left, uint32_t mask, vector<uint32_t>& c0, vector<uint32_t>& c1, vector<uint32_t>& c2) {
    if (w_left == 0) {
        if (get_in_code(mask)) return;
        uint8_t c = cnt[mask];
        if (c == 0) c0.push_back(mask);
        else if (c == 1) c1.push_back(mask);
        else if (c == 2) c2.push_back(mask);
        return;
    }
    if (N - idx < w_left) return;
    collect_low(idx + 1, w_left - 1, mask | (1U << idx), c0, c1, c2);
    collect_low(idx + 1, w_left, mask, c0, c1, c2);
}

int main() {
    cnt = new uint8_t[1ULL << N];
    in_code = new uint64_t[1ULL << (N - 6)];
    memset(cnt, 0, 1ULL << N);
    memset(in_code, 0, (1ULL << (N - 6)) * sizeof(uint64_t));

    ifstream fin("seed_27_6_10.txt");
    uint32_t w;
    int cur_size = 0;
    while (fin >> w) {
        add_word(w);
        cur_size++;
    }
    cout << "Loaded seed_27_6_10.txt: " << cur_size << " words" << endl;

    vector<uint32_t> c0, c1, c2;
    collect_low(0, W, 0, c0, c1, c2);
    cout << "Initial |c0|=" << c0.size() << " |c1|=" << c1.size() << " |c2|=" << c2.size() << endl;

    // Analyze conflict graph of the 702 free words in c0!
    int n0 = c0.size();
    vector<int> deg(n0, 0);
    for (int i = 0; i < n0; ++i)
        for (int j = i + 1; j < n0; ++j)
            if (dist(c0[i], c0[j]) < 6) { deg[i]++; deg[j]++; }
    cout << "c0[0] degree in c0: " << deg[0] << endl;

    // Multi-start randomized greedy + local search on c0 (702 vertices)
    mt19937 rng(42);
    vector<uint32_t> best_c0_ind;
    for (int t = 0; t < 500; ++t) {
        vector<uint32_t> p = c0;
        shuffle(p.begin(), p.end(), rng);
        vector<uint32_t> cur;
        for (uint32_t u : p) {
            bool ok = true;
            for (uint32_t v : cur) if (dist(u, v) < 6) { ok = false; break; }
            if (ok) cur.push_back(u);
        }
        if (cur.size() > best_c0_ind.size()) best_c0_ind = cur;
    }
    cout << "Max independent set found inside 702 free words: " << best_c0_ind.size() << endl;
    for (uint32_t u : best_c0_ind) {
        add_word(u);
        cur_size++;
    }
    cout << ">>> NEW SIZE AFTER ADDING FREE INDEPENDENT SET: " << cur_size << " (beats 12987 by +" << (cur_size - 12987) << ") <<<" << endl;

    // Re-scan c0, c1, c2 after adding best_c0_ind!
    c0.clear(); c1.clear(); c2.clear();
    collect_low(0, W, 0, c0, c1, c2);
    cout << "Post-c0 scan: |c0|=" << c0.size() << " |c1|=" << c1.size() << " |c2|=" << c2.size() << endl;

    // Now run plateau 1-swaps and 2-swaps for 6 seconds!
    auto t0 = chrono::steady_clock::now();
    vector<uint32_t> zero_cands, new_c1, new_c2, confs;
    int best_size = cur_size;
    // Save best code
    auto save_best = [&]() {
        ofstream fout("best_27_6_10.txt");
        for (uint32_t m = 0; m < (1U << N); ++m) {
            if (get_in_code(m)) fout << m << "\n";
        }
    };
    save_best();

    int steps = 0;
    while (true) {
        auto now = chrono::steady_clock::now();
        if (chrono::duration_cast<chrono::milliseconds>(now - t0).count() > 6000) break;
        steps++;

        if (!c1.empty() && (rng() % 2 == 0 || c2.empty())) {
            int idx = rng() % c1.size();
            uint32_t y = c1[idx];
            c1[idx] = c1.back(); c1.pop_back();
            if (cnt[y] != 1 || get_in_code(y)) continue;
            find_conflicts_in_code(y, confs);
            if (confs.size() != 1) continue;
            uint32_t x = confs[0];
            zero_cands.clear(); new_c1.clear(); new_c2.clear();
            remove_word(x, zero_cands, new_c1, new_c2);

            vector<uint32_t> chosen = {y};
            for (uint32_t z : zero_cands) {
                if (z == x || z == y) continue;
                bool ok = true;
                for (uint32_t ch : chosen) if (dist(z, ch) < 6) { ok = false; break; }
                if (ok) chosen.push_back(z);
            }
            for (uint32_t ch : chosen) add_word(ch);
            cur_size += (int)chosen.size() - 1;
            for (uint32_t nc : new_c1) if (cnt[nc] == 1 && !get_in_code(nc)) c1.push_back(nc);
            for (uint32_t nc : new_c2) if (cnt[nc] == 2 && !get_in_code(nc) && c2.size() < 50000) c2.push_back(nc);
            if (cur_size > best_size) {
                best_size = cur_size;
                cout << ">>> IMPROVED TO " << best_size << " (step " << steps << ") <<<" << endl;
                save_best();
            }
        } else if (!c2.empty()) {
            int idx = rng() % c2.size();
            uint32_t y = c2[idx];
            c2[idx] = c2.back(); c2.pop_back();
            if (cnt[y] == 1 && !get_in_code(y)) { c1.push_back(y); continue; }
            if (cnt[y] != 2 || get_in_code(y)) continue;
            find_conflicts_in_code(y, confs);
            if (confs.size() != 2) continue;
            uint32_t x1 = confs[0], x2 = confs[1];
            zero_cands.clear(); new_c1.clear(); new_c2.clear();
            remove_word(x1, zero_cands, new_c1, new_c2);
            remove_word(x2, zero_cands, new_c1, new_c2);
            vector<uint32_t> zc;
            for (uint32_t z : zero_cands) if (cnt[z] == 0 && z != x1 && z != x2) zc.push_back(z);
            sort(zc.begin(), zc.end());
            zc.erase(unique(zc.begin(), zc.end()), zc.end());
            vector<uint32_t> best_is;
            for (size_t i = 0; i < zc.size(); ++i)
                for (size_t j = i + 1; j < zc.size(); ++j)
                    if (dist(zc[i], zc[j]) >= 6) {
                        vector<uint32_t> cur_is = {zc[i], zc[j]};
                        for (size_t k = j + 1; k < zc.size(); ++k) {
                            bool ok = true;
                            for (uint32_t u : cur_is) if (dist(zc[k], u) < 6) { ok = false; break; }
                            if (ok) cur_is.push_back(zc[k]);
                        }
                        if (cur_is.size() > best_is.size()) best_is = cur_is;
                    }
            if (best_is.size() >= 2) {
                for (uint32_t ch : best_is) add_word(ch);
                cur_size += (int)best_is.size() - 2;
                for (uint32_t nc : new_c1) if (cnt[nc] == 1 && !get_in_code(nc)) c1.push_back(nc);
                for (uint32_t nc : new_c2) if (cnt[nc] == 2 && !get_in_code(nc) && c2.size() < 50000) c2.push_back(nc);
                if (cur_size > best_size) {
                    best_size = cur_size;
                    cout << ">>> IMPROVED TO " << best_size << " (step " << steps << ") <<<" << endl;
                    save_best();
                }
            } else {
                add_word(x1); add_word(x2);
            }
        } else break;
    }
    cout << "Final best size for A(27, 6, 10): " << best_size << " (steps=" << steps << ")" << endl;
    return 0;
}
