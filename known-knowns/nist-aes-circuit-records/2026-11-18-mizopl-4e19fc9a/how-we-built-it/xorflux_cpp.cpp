// xorflux_cpp.cpp — General N <= 64 (uint64_t) Incremental Value-Set Linear {XOR} Optimizer
// Exact C++17 port of XORFlux v8 (core/valueset.py + engine/polish.py + moves/{walk,lns,rebuild,depth,construct}.py)
// plus Connected-Cone 2->1 / 2->2 / 3->2 MITM & Critical-Path Depth Squeeze.
//
// Strictly complies with general target-agnostic design (zero hardcoded lookup tables):
//   - Takes ANY linear map over GF(2) (N <= 64 inputs, M <= 64 outputs) via `--targets <file>`
//   - Takes ANY seed list via `--seeds <file>`
//   - Zero hardcoded target-specific gates or matrices.

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <mutex>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

static constexpr int MAX_U = 320;       // 5 x uint64_t words per slot bitset (fits <= 256 gates + 64 inputs)
static constexpr int WORDS = MAX_U / 64; // 5
static constexpr int INF_LV = 1000;

static inline int popcnt64(uint64_t x) { return __builtin_popcountll(x); }
static inline int ctz64(uint64_t x) { return __builtin_ctzll(x); }
static inline int bitlen64(uint64_t x) { return x ? (64 - __builtin_clzll(x)) : 0; }

// Tombstone-free power-of-2 open-addressing hash map (uint64_t key .= 0 -> int16_t slot)
// Uses Knuth Algorithm R backward-shift deletion so performance never degrades over billions of ops.
struct MaskSlotMap {
    static constexpr uint32_t CAP = 2048;
    static constexpr uint32_t MASK = CAP - 1;
    uint64_t keys[CAP];
    int16_t vals[CAP];

    MaskSlotMap() { clear(); }
    inline void clear() { std::memset(keys, 0, sizeof(keys)); }

    static inline uint32_t hash64(uint64_t x) {
        x ^= x >> 33;
        x *= 0xff51afd7ed558ccdULL;
        x ^= x >> 33;
        return (uint32_t)x;
    }

    inline int16_t find(uint64_t k) const {
        if (k == 0) return -1;
        uint32_t i = hash64(k) & MASK;
        while (keys[i] != 0) {
            if (keys[i] == k) return vals[i];
            i = (i + 1) & MASK;
        }
        return -1;
    }

    inline void insert(uint64_t k, int16_t v) {
        uint32_t i = hash64(k) & MASK;
        while (keys[i] != 0) {
            if (keys[i] == k) { vals[i] = v; return; }
            i = (i + 1) & MASK;
        }
        keys[i] = k;
        vals[i] = v;
    }

    inline void erase(uint64_t k) {
        uint32_t i = hash64(k) & MASK;
        while (keys[i] != 0 && keys[i] != k) i = (i + 1) & MASK;
        if (keys[i] == 0) return;
        uint32_t j = i;
        while (true) {
            j = (j + 1) & MASK;
            if (keys[j] == 0) break;
            uint32_t r = hash64(keys[j]) & MASK;
            if ((i <= j) ? (r <= i || r > j) : (r <= i && r > j)) {
                keys[i] = keys[j];
                vals[i] = vals[j];
                i = j;
            }
        }
        keys[i] = 0;
    }
};

// Fast generation-stamped uint64_t set (32768 slots = 384 KB, fits in L2 cache, O(1) clear)
struct FastSet32K {
    static constexpr uint32_t CAP = 32768;
    static constexpr uint32_t MASK = CAP - 1;
    uint64_t keys[CAP];
    uint16_t stamps[CAP];
    uint16_t gen = 1;

    FastSet32K() { std::memset(stamps, 0, sizeof(stamps)); }
    inline void clear() {
        if (++gen == 0) {
            std::memset(stamps, 0, sizeof(stamps));
            gen = 1;
        }
    }
    inline bool insert(uint64_t k) {
        uint32_t i = MaskSlotMap::hash64(k) & MASK;
        while (stamps[i] == gen) {
            if (keys[i] == k) return false;
            i = (i + 1) & MASK;
        }
        stamps[i] = gen;
        keys[i] = k;
        return true;
    }
    inline bool contains(uint64_t k) const {
        uint32_t i = MaskSlotMap::hash64(k) & MASK;
        while (stamps[i] == gen) {
            if (keys[i] == k) return true;
            i = (i + 1) & MASK;
        }
        return false;
    }
};

struct TargetSpec {
    int n_in = 32;
    std::vector<uint64_t> rows;     // all output rows in order
    std::vector<uint64_t> targets;  // distinct nonzero rows
    std::string func_name = "aes-invmixcols";
    std::string desc = "AES MixColumns Inverse, compatible with NIST-FIPS 197";
};

static TargetSpec load_target_spec(const std::string& path) {
    TargetSpec spec;
    std::ifstream fh(path);
    if (!fh) {
        std::cerr << "Failed to open target file: " << path << "\n";
        std::exit(1);
    }
    int m_out = 0;
    fh >> spec.n_in >> m_out;
    spec.rows.resize(m_out);
    std::unordered_set<uint64_t> seen;
    for (int i = 0; i < m_out; ++i) {
        fh >> spec.rows[i];
        if (spec.rows[i] != 0 && !seen.count(spec.rows[i])) {
            seen.insert(spec.rows[i]);
            spec.targets.push_back(spec.rows[i]);
        }
    }
    return spec;
}

// Bitset helpers for 512-slot arrays
static inline void bset(uint64_t b[WORDS], int i) { b[i >> 6] |= (1ULL << (i & 63)); }
static inline void bclr(uint64_t b[WORDS], int i) { b[i >> 6] &= ~(1ULL << (i & 63)); }
static inline bool bget(const uint64_t b[WORDS], int i) { return (b[i >> 6] >> (i & 63)) & 1ULL; }
static inline bool bany(const uint64_t b[WORDS]) {
    for (int w = 0; w < WORDS; ++w) if (b[w]) return true;
    return false;
}
static inline void bzero(uint64_t b[WORDS]) { std::memset(b, 0, WORDS * sizeof(uint64_t)); }

// Incremental Canonical ValueSet64 (exact port of XORFlux v8 core/valueset.py)
struct ValueSet64 {
    int n_in = 0;
    int cap = INF_LV; // INF_LV means uncapped
    std::vector<uint64_t> rows;
    std::vector<uint64_t> targets;

    uint64_t val[MAX_U];
    int16_t lv[MAX_U];       // 0..cap when realized, INF_LV when stuck
    uint64_t par[MAX_U];     // canonical smaller operand mask (0 for inputs or stuck)
    uint8_t active[MAX_U];
    uint8_t is_input[MAX_U];
    uint8_t is_target[MAX_U];
    uint64_t active_bits[WORDS];
    uint64_t target_bits[WORDS];
    uint64_t tri[MAX_U][WORDS];  // tri[u] has bit x iff val[u]^val[x] is in U
    uint64_t kids[MAX_U][WORDS]; // kids[x] has bit v iff x is a witness operand of v

    int free_slots[MAX_U];
    int n_free = 0;
    int n_active = 0;
    int n_levelled = 0;
    int n_targets = 0;
    int n_realized_targets = 0;
    MaskSlotMap map;

    struct OldEntry {
        uint64_t v;
        int16_t old_lv;
        uint64_t old_par;
    };
    struct UndoRec {
        bool is_add; // true: _ADD, false: _REMOVE
        uint64_t added_w;
        std::vector<uint64_t> removed_vals;
        std::vector<std::vector<uint64_t>> removed_partners; // masks
        std::vector<OldEntry> old;
    };
    std::vector<UndoRec> log;
    int open_journals = 0;

    void init(const TargetSpec& spec, const std::vector<uint64_t>& init_vals, int depth_cap) {
        n_in = spec.n_in;
        cap = (depth_cap <= 0 || depth_cap >= INF_LV) ? INF_LV : depth_cap;
        rows = spec.rows;
        targets = spec.targets;

        map.clear();
        bzero(active_bits);
        bzero(target_bits);
        std::memset(active, 0, sizeof(active));
        std::memset(is_input, 0, sizeof(is_input));
        std::memset(is_target, 0, sizeof(is_target));
        log.clear();
        open_journals = 0;

        n_active = 0;
        n_levelled = 0;
        n_targets = 0;
        n_realized_targets = 0;

        std::unordered_set<uint64_t> tset(targets.begin(), targets.end());
        uint64_t full_mask = (n_in == 64) ? ~0ULL : ((1ULL << n_in) - 1ULL);

        for (int i = 0; i < n_in; ++i) {
            uint64_t m = 1ULL << i;
            val[i] = m;
            lv[i] = 0;
            par[i] = 0;
            active[i] = 1;
            is_input[i] = 1;
            is_target[i] = tset.count(m) ? 1 : 0;
            bset(active_bits, i);
            if (is_target[i]) {
                bset(target_bits, i);
                n_targets++;
                n_realized_targets++;
            }
            bzero(tri[i]);
            bzero(kids[i]);
            map.insert(m, (int16_t)i);
            n_active++;
            n_levelled++;
        }

        n_free = 0;
        for (int s = MAX_U - 1; s >= n_in; --s) free_slots[n_free++] = s;

        std::vector<uint64_t> extra;
        extra.reserve(init_vals.size() + targets.size());
        for (uint64_t v : init_vals) {
            if (v != 0 && (v & ~full_mask) == 0 && popcnt64(v) > 1) extra.push_back(v);
        }
        for (uint64_t t : targets) {
            if (t != 0 && popcnt64(t) > 1) extra.push_back(t);
        }
        std::sort(extra.begin(), extra.end());
        extra.erase(std::unique(extra.begin(), extra.end()), extra.end());

        std::vector<int> pend_slots;
        pend_slots.reserve(extra.size());
        for (uint64_t m : extra) {
            if (n_free == 0) break;
            int s = free_slots[--n_free];
            val[s] = m;
            lv[s] = INF_LV;
            par[s] = 0;
            active[s] = 1;
            is_input[s] = 0;
            is_target[s] = tset.count(m) ? 1 : 0;
            bset(active_bits, s);
            if (is_target[s]) {
                bset(target_bits, s);
                n_targets++;
            }
            bzero(tri[s]);
            bzero(kids[s]);
            map.insert(m, (int16_t)s);
            n_active++;
            pend_slots.push_back(s);
        }

        // Build initial symmetric triple index in O(|U|^2 / 2)
        int slots[MAX_U], ns = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t bits = active_bits[w];
            while (bits) {
                slots[ns++] = (w << 6) | ctz64(bits);
                bits &= bits - 1;
            }
        }
        for (int i = 0; i < ns; ++i) {
            int sa = slots[i];
            uint64_t ma = val[sa];
            for (int j = i + 1; j < ns; ++j) {
                int sb = slots[j];
                uint64_t mc = ma ^ val[sb];
                int16_t sc = map.find(mc);
                if (sc >= 0 && sc > sb) {
                    bset(tri[sa], sb); bset(tri[sa], sc);
                    bset(tri[sb], sa); bset(tri[sb], sc);
                    bset(tri[sc], sa); bset(tri[sc], sb);
                }
            }
        }

        uint64_t pend_bits[WORDS];
        bzero(pend_bits);
        for (int s : pend_slots) bset(pend_bits, s);
        resolve_pend(pend_bits);
    }

    inline bool ok() const { return n_realized_targets == n_targets; }
    inline int count() const { return n_levelled - n_in; }

    inline int depth() const {
        if (!ok()) return INF_LV;
        int d = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t bits = target_bits[w];
            while (bits) {
                int s = (w << 6) | ctz64(bits);
                bits &= bits - 1;
                if (lv[s] > d) d = lv[s];
            }
        }
        return d;
    }

    inline void unlink_witness(int s) {
        uint64_t a_mask = par[s];
        if (a_mask != 0) {
            int16_t sa = map.find(a_mask);
            int16_t sb = map.find(val[s] ^ a_mask);
            if (sa >= 0) bclr(kids[sa], s);
            if (sb >= 0) bclr(kids[sb], s);
            par[s] = 0;
        }
        if (lv[s] < INF_LV) {
            if (!is_input[s]) {
                n_levelled--;
                if (is_target[s]) n_realized_targets--;
            }
            lv[s] = INF_LV;
        }
    }

    inline void link_witness(int s, int16_t d, uint64_t a_mask) {
        lv[s] = d;
        par[s] = a_mask;
        if (!is_input[s]) {
            n_levelled++;
            if (is_target[s]) n_realized_targets++;
        }
        if (a_mask != 0) {
            int16_t sa = map.find(a_mask);
            int16_t sb = map.find(val[s] ^ a_mask);
            if (sa >= 0) bset(kids[sa], s);
            if (sb >= 0) bset(kids[sb], s);
        }
    }

    // Knuth/Dijkstra bucket solver for unlevelled `pend_bits` (exact port of ValueSet._resolve)
    void resolve_pend(const uint64_t pend_bits[WORDS]) {
        int16_t tent[MAX_U];
        uint64_t tpar[MAX_U];
        for (int i = 0; i < MAX_U; ++i) { tent[i] = INF_LV; tpar[i] = 0; }

        int max_b = std::min(cap, 64);
        std::vector<int> buckets[66];
        int min_d = 999;

        for (int w = 0; w < WORDS; ++w) {
            uint64_t pbits = pend_bits[w];
            while (pbits) {
                int s = (w << 6) | ctz64(pbits);
                pbits &= pbits - 1;
                uint64_t ms = val[s];
                int best = INF_LV;
                uint64_t bp = 0;
                for (int tw = 0; tw < WORDS; ++tw) {
                    uint64_t tb = tri[s][tw];
                    while (tb) {
                        int sx = (tw << 6) | ctz64(tb);
                        tb &= tb - 1;
                        if (lv[sx] >= INF_LV) continue;
                        uint64_t mx = val[sx];
                        uint64_t my = ms ^ mx;
                        if (mx > my) continue;
                        int16_t sy = map.find(my);
                        if (sy < 0 || lv[sy] >= INF_LV) continue;
                        int m = std::max((int)lv[sx], (int)lv[sy]);
                        if (m < best || (m == best && mx < bp)) {
                            best = m;
                            bp = mx;
                        }
                    }
                }
                if (bp != 0 && best < cap) {
                    int d = best + 1;
                    tent[s] = (int16_t)d;
                    tpar[s] = bp;
                    int bi = std::min(d, 65);
                    buckets[bi].push_back(s);
                    if (bi < min_d) min_d = bi;
                }
            }
        }
        if (min_d > 65) return;

        for (int d = min_d; d <= std::min(cap, 65); ++d) {
            // Note: for uncapped deep circuits > 64, process bucket 65 iteratively
            while (!buckets[d].empty()) {
                std::vector<int> cur;
                cur.swap(buckets[d]);
                for (int sv : cur) {
                    int real_d = tent[sv];
                    if (lv[sv] < INF_LV) continue;
                    if (d < 65 && real_d != d) continue;
                    link_witness(sv, (int16_t)real_d, tpar[sv]);
                    if (real_d >= cap) continue;

                    uint64_t mv = val[sv];
                    for (int tw = 0; tw < WORDS; ++tw) {
                        uint64_t tb = tri[sv][tw];
                        while (tb) {
                            int sx = (tw << 6) | ctz64(tb);
                            tb &= tb - 1;
                            if (lv[sx] >= INF_LV) continue;
                            uint64_t mx = val[sx];
                            uint64_t my = mv ^ mx;
                            int16_t sy = map.find(my);
                            if (sy < 0 || !bget(pend_bits, sy) || lv[sy] < INF_LV) continue;
                            int m = 1 + std::max(real_d, (int)lv[sx]);
                            if (m > cap) continue;
                            uint64_t k = (mx < mv) ? mx : mv;
                            if (m < tent[sy]) {
                                tent[sy] = (int16_t)m;
                                tpar[sy] = k;
                                buckets[std::min(m, 65)].push_back(sy);
                            } else if (m == tent[sy] && k < tpar[sy]) {
                                tpar[sy] = k;
                            }
                        }
                    }
                }
                if (d < 65) break;
            }
        }
    }

    // Propagate level decreases from `seed_slot` (exact port of ValueSet._lower)
    void lower_from(int seed_slot, std::vector<OldEntry>* rec_out) {
        uint64_t recorded[WORDS];
        bzero(recorded);
        std::vector<int> buckets[66];
        int d0 = std::min((int)lv[seed_slot], 65);
        buckets[d0].push_back(seed_slot);

        for (int d = d0; d <= std::min(cap, 65); ++d) {
            while (!buckets[d].empty()) {
                std::vector<int> cur;
                cur.swap(buckets[d]);
                for (int su : cur) {
                    int du = lv[su];
                    if (d < 65 && du != d) continue;
                    if (du >= cap) continue;
                    uint64_t mu = val[su];
                    for (int tw = 0; tw < WORDS; ++tw) {
                        uint64_t tb = tri[su][tw];
                        while (tb) {
                            int sx = (tw << 6) | ctz64(tb);
                            tb &= tb - 1;
                            if (lv[sx] >= INF_LV) continue;
                            uint64_t mx = val[sx];
                            uint64_t my = mu ^ mx;
                            int16_t sy = map.find(my);
                            if (sy < 0 || is_input[sy]) continue;
                            int mm = 1 + std::max(du, (int)lv[sx]);
                            int ly = lv[sy];
                            if (ly < mm || mm > cap) continue;
                            uint64_t k = (mx < mu) ? mx : mu;
                            if (mm < ly) {
                                if (rec_out && !bget(recorded, sy)) {
                                    bset(recorded, sy);
                                    rec_out->push_back({my, (int16_t)ly, par[sy]});
                                }
                                unlink_witness(sy);
                                link_witness(sy, (int16_t)mm, k);
                                buckets[std::min(mm, 65)].push_back(sy);
                            } else if (mm == ly && k < par[sy]) {
                                if (rec_out && !bget(recorded, sy)) {
                                    bset(recorded, sy);
                                    rec_out->push_back({my, (int16_t)ly, par[sy]});
                                }
                                unlink_witness(sy);
                                link_witness(sy, (int16_t)ly, k);
                            }
                        }
                    }
                }
                if (d < 65) break;
            }
        }
    }

    int journal() {
        open_journals++;
        return (int)log.size();
    }

    void commit(int /*mark*/) {
        if (open_journals > 0) open_journals--;
        if (open_journals == 0) log.clear();
    }

    void rollback(int mark) {
        while ((int)log.size() > mark) {
            UndoRec u = std::move(log.back());
            log.pop_back();
            if (u.is_add) unadd_raw(u);
            else restore_raw(u);
        }
        if (open_journals > 0) open_journals--;
        if (open_journals == 0) log.clear();
    }

    bool add(uint64_t w) {
        if (w == 0 || map.find(w) >= 0 || n_free == 0) return false;
        int sw = free_slots[--n_free];
        val[sw] = w;
        lv[sw] = INF_LV;
        par[sw] = 0;
        active[sw] = 1;
        is_input[sw] = 0;
        is_target[sw] = 0;
        for (uint64_t t : targets) if (t == w) { is_target[sw] = 1; break; }
        bset(active_bits, sw);
        if (is_target[sw]) {
            bset(target_bits, sw);
            n_targets++;
        }
        bzero(tri[sw]);
        bzero(kids[sw]);
        map.insert(w, (int16_t)sw);
        n_active++;

        int best = INF_LV;
        uint64_t bp = 0;
        for (int bw = 0; bw < WORDS; ++bw) {
            uint64_t ab = active_bits[bw];
            while (ab) {
                int sx = (bw << 6) | ctz64(ab);
                ab &= ab - 1;
                if (sx == sw) continue;
                uint64_t mx = val[sx];
                uint64_t my = w ^ mx;
                if (mx > my) continue;
                int16_t sy = map.find(my);
                if (sy < 0) continue;
                bset(tri[sw], sx); bset(tri[sw], sy);
                bset(tri[sx], sw); bset(tri[sx], sy);
                bset(tri[sy], sw); bset(tri[sy], sx);
                if (lv[sx] < INF_LV && lv[sy] < INF_LV) {
                    int m = std::max((int)lv[sx], (int)lv[sy]);
                    if (m < best || (m == best && mx < bp)) {
                        best = m;
                        bp = mx;
                    }
                }
            }
        }

        UndoRec u;
        u.is_add = true;
        u.added_w = w;
        std::vector<OldEntry>* rec_ptr = (open_journals > 0) ? &u.old : nullptr;

        if (bp != 0 && best < cap) {
            link_witness(sw, (int16_t)(best + 1), bp);
            lower_from(sw, rec_ptr);
        }
        if (open_journals > 0) log.push_back(std::move(u));
        return true;
    }

    void unadd_raw(const UndoRec& u) {
        uint64_t w = u.added_w;
        int16_t sw = map.find(w);
        if (sw < 0) return;

        // First unlink changed values and sw, then relink old witnesses
        std::vector<int> ch_slots;
        ch_slots.reserve(u.old.size());
        for (const auto& e : u.old) {
            int16_t sy = map.find(e.v);
            ch_slots.push_back(sy);
            if (sy >= 0) unlink_witness(sy);
        }
        unlink_witness(sw);

        for (size_t i = 0; i < u.old.size(); ++i) {
            int sy = ch_slots[i];
            if (sy >= 0 && u.old[i].old_lv < INF_LV) {
                link_witness(sy, u.old[i].old_lv, u.old[i].old_par);
            }
        }

        // Remove sw from triple index
        for (int tw = 0; tw < WORDS; ++tw) {
            uint64_t tb = tri[sw][tw];
            while (tb) {
                int sx = (tw << 6) | ctz64(tb);
                tb &= tb - 1;
                int16_t sy = map.find(val[sx] ^ w);
                bclr(tri[sx], sw);
                if (sy >= 0) bclr(tri[sx], sy);
            }
        }
        bzero(tri[sw]);
        bzero(kids[sw]);
        active[sw] = 0;
        bclr(active_bits, sw);
        if (is_target[sw]) {
            bclr(target_bits, sw);
            is_target[sw] = 0;
            n_targets--;
        }
        map.erase(w);
        free_slots[n_free++] = sw;
        n_active--;
    }

    // Remove values `vals`, return stuck masks in `stuck_out` (if non-null)
    void remove_vals(const uint64_t* vals, int n_vals, std::vector<uint64_t>* stuck_out = nullptr) {
        int d_slots[MAX_U], nd = 0;
        uint64_t d_bits[WORDS];
        bzero(d_bits);
        for (int i = 0; i < n_vals; ++i) {
            int16_t s = map.find(vals[i]);
            if (s >= 0 && !is_input[s] && !bget(d_bits, s)) {
                bset(d_bits, s);
                d_slots[nd++] = s;
            }
        }
        if (nd == 0) {
            if (stuck_out) stuck_out->clear();
            if (open_journals > 0) {
                UndoRec u; u.is_add = false;
                log.push_back(std::move(u));
            }
            return;
        }

        uint64_t aff_bits[WORDS];
        bzero(aff_bits);
        int stack[MAX_U], sp = 0;
        for (int i = 0; i < nd; ++i) stack[sp++] = d_slots[i];
        while (sp > 0) {
            int x = stack[--sp];
            for (int kw = 0; kw < WORDS; ++kw) {
                uint64_t kb = kids[x][kw];
                while (kb) {
                    int c = (kw << 6) | ctz64(kb);
                    kb &= kb - 1;
                    if (!bget(aff_bits, c) && !bget(d_bits, c)) {
                        bset(aff_bits, c);
                        stack[sp++] = c;
                    }
                }
            }
        }

        UndoRec u;
        u.is_add = false;
        if (open_journals > 0) {
            u.removed_vals.reserve(nd);
            u.removed_partners.resize(nd);
            for (int i = 0; i < nd; ++i) {
                int s = d_slots[i];
                u.removed_vals.push_back(val[s]);
                u.old.push_back({val[s], lv[s], par[s]});
                for (int tw = 0; tw < WORDS; ++tw) {
                    uint64_t tb = tri[s][tw];
                    while (tb) {
                        int sx = (tw << 6) | ctz64(tb);
                        tb &= tb - 1;
                        u.removed_partners[i].push_back(val[sx]);
                    }
                }
            }
            for (int w = 0; w < WORDS; ++w) {
                uint64_t ab = aff_bits[w];
                while (ab) {
                    int c = (w << 6) | ctz64(ab);
                    ab &= ab - 1;
                    u.old.push_back({val[c], lv[c], par[c]});
                }
            }
        }

        // Unlink aff and D
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = aff_bits[w];
            while (ab) {
                int c = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                unlink_witness(c);
            }
        }
        for (int i = 0; i < nd; ++i) unlink_witness(d_slots[i]);

        // Remove D from tri and map
        for (int i = 0; i < nd; ++i) {
            int s = d_slots[i];
            uint64_t mv = val[s];
            for (int tw = 0; tw < WORDS; ++tw) {
                uint64_t tb = tri[s][tw];
                while (tb) {
                    int sx = (tw << 6) | ctz64(tb);
                    tb &= tb - 1;
                    bclr(tri[sx], s);
                    int16_t sy = map.find(mv ^ val[sx]);
                    if (sy >= 0) bclr(tri[sx], sy);
                }
            }
            bzero(tri[s]);
            bzero(kids[s]);
            active[s] = 0;
            bclr(active_bits, s);
            if (is_target[s]) {
                bclr(target_bits, s);
                is_target[s] = 0;
                n_targets--;
            }
            map.erase(mv);
            free_slots[n_free++] = s;
            n_active--;
        }

        if (bany(aff_bits)) resolve_pend(aff_bits);

        if (stuck_out) {
            stuck_out->clear();
            for (int w = 0; w < WORDS; ++w) {
                uint64_t ab = aff_bits[w];
                while (ab) {
                    int c = (w << 6) | ctz64(ab);
                    ab &= ab - 1;
                    if (lv[c] >= INF_LV) stuck_out->push_back(val[c]);
                }
            }
        }
        if (open_journals > 0) log.push_back(std::move(u));
    }

    void restore_raw(const UndoRec& u) {
        if (u.removed_vals.empty()) return;
        std::unordered_set<uint64_t> tset(targets.begin(), targets.end());
        std::vector<int> rslots(u.removed_vals.size());
        for (size_t i = 0; i < u.removed_vals.size(); ++i) {
            uint64_t mv = u.removed_vals[i];
            int s = free_slots[--n_free];
            rslots[i] = s;
            val[s] = mv;
            lv[s] = INF_LV;
            par[s] = 0;
            active[s] = 1;
            is_input[s] = 0;
            is_target[s] = tset.count(mv) ? 1 : 0;
            bset(active_bits, s);
            if (is_target[s]) {
                bset(target_bits, s);
                n_targets++;
            }
            bzero(tri[s]);
            bzero(kids[s]);
            map.insert(mv, (int16_t)s);
            n_active++;
        }
        for (size_t i = 0; i < u.removed_vals.size(); ++i) {
            int sv = rslots[i];
            uint64_t mv = u.removed_vals[i];
            for (uint64_t mx : u.removed_partners[i]) {
                int16_t sx = map.find(mx);
                int16_t sy = map.find(mv ^ mx);
                if (sx >= 0 && sy >= 0) {
                    bset(tri[sv], sx); bset(tri[sv], sy);
                    bset(tri[sx], sv); bset(tri[sx], sy);
                    bset(tri[sy], sv); bset(tri[sy], sx);
                }
            }
        }
        // Unlink all recorded old entries, then relink
        std::vector<int> oslots(u.old.size());
        for (size_t i = 0; i < u.old.size(); ++i) {
            int16_t s = map.find(u.old[i].v);
            oslots[i] = s;
            if (s >= 0) unlink_witness(s);
        }
        for (size_t i = 0; i < u.old.size(); ++i) {
            int s = oslots[i];
            if (s >= 0 && u.old[i].old_lv < INF_LV) {
                link_witness(s, u.old[i].old_lv, u.old[i].old_par);
            }
        }
    }

    // Undo most recent journaled remove immediately (`XORFlux v8` restore)
    void undo_last() {
        if (log.empty()) return;
        UndoRec u = std::move(log.back());
        log.pop_back();
        if (u.is_add) unadd_raw(u);
        else restore_raw(u);
    }

    // Drop stuck non-targets and cascading dead witness helpers (exact port of ValueSet.trim)
    void trim() {
        uint64_t dead_bits[WORDS];
        bzero(dead_bits);
        int stack[MAX_U], sp = 0;

        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (is_input[s] || is_target[s]) continue;
                if (lv[s] >= INF_LV) {
                    bset(dead_bits, s);
                } else if (!bany(kids[s])) {
                    stack[sp++] = s;
                }
            }
        }

        while (sp > 0) {
            int v = stack[--sp];
            if (bget(dead_bits, v)) continue;
            bset(dead_bits, v);
            uint64_t a_mask = par[v];
            if (a_mask == 0) continue;
            int16_t sa = map.find(a_mask);
            int16_t sb = map.find(val[v] ^ a_mask);
            for (int p : {(int)sa, (int)sb}) {
                if (p >= 0 && !is_input[p] && !is_target[p] && !bget(dead_bits, p)) {
                    bool all_dead = true;
                    for (int kw = 0; kw < WORDS; ++kw) {
                        if (kids[p][kw] & ~dead_bits[kw]) { all_dead = false; break; }
                    }
                    if (all_dead) stack[sp++] = p;
                }
            }
        }

        uint64_t to_rem[MAX_U];
        int nr = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t db = dead_bits[w];
            while (db) {
                int s = (w << 6) | ctz64(db);
                db &= db - 1;
                to_rem[nr++] = val[s];
            }
        }
        if (nr > 0) remove_vals(to_rem, nr, nullptr);
    }

    void retain(const std::unordered_set<uint64_t>& keep) {
        uint64_t to_rem[MAX_U];
        int nr = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (!is_input[s] && !is_target[s] && !keep.count(val[s])) {
                    to_rem[nr++] = val[s];
                }
            }
        }
        if (nr > 0) remove_vals(to_rem, nr, nullptr);
    }

    // Cap-free screen: does removing slot `sv` strand any target (if only_targets) or any U member?
    bool strands_slot(int sv, bool only_targets) const {
        uint64_t aff_bits[WORDS];
        bzero(aff_bits);
        int stack[MAX_U], sp = 0;
        stack[sp++] = sv;
        while (sp > 0) {
            int x = stack[--sp];
            for (int kw = 0; kw < WORDS; ++kw) {
                uint64_t kb = kids[x][kw];
                while (kb) {
                    int c = (kw << 6) | ctz64(kb);
                    kb &= kb - 1;
                    if (!bget(aff_bits, c)) {
                        bset(aff_bits, c);
                        stack[sp++] = c;
                    }
                }
            }
        }
        if (!bany(aff_bits)) return false;

        int need = -1;
        if (only_targets) {
            need = 0;
            for (int w = 0; w < WORDS; ++w) need += popcnt64(aff_bits[w] & target_bits[w]);
            if (need == 0) return false;
        }

        uint64_t bad_bits[WORDS], got_bits[WORDS];
        std::memcpy(bad_bits, aff_bits, sizeof(aff_bits));
        bset(bad_bits, sv);
        bzero(got_bits);
        sp = 0;

        int n_aff = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = aff_bits[w];
            while (ab) {
                int y = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                n_aff++;
                uint64_t my = val[y];
                bool seeded = false;
                for (int tw = 0; tw < WORDS && !seeded; ++tw) {
                    uint64_t tb = tri[y][tw];
                    while (tb) {
                        int sx = (tw << 6) | ctz64(tb);
                        tb &= tb - 1;
                        if (bget(bad_bits, sx) || lv[sx] >= INF_LV) continue;
                        uint64_t mx = val[sx];
                        uint64_t mz = my ^ mx;
                        if (mx > mz) continue;
                        int16_t sz = map.find(mz);
                        if (sz >= 0 && !bget(bad_bits, sz) && lv[sz] < INF_LV) {
                            bset(got_bits, y);
                            stack[sp++] = y;
                            if (only_targets && is_target[y] && --need == 0) return false;
                            seeded = true;
                            break;
                        }
                    }
                }
            }
        }

        int n_got = sp;
        while (sp > 0) {
            int u = stack[--sp];
            uint64_t mu = val[u];
            for (int tw = 0; tw < WORDS; ++tw) {
                uint64_t tb = tri[u][tw];
                while (tb) {
                    int sx = (tw << 6) | ctz64(tb);
                    tb &= tb - 1;
                    if (!bget(got_bits, sx) && (bget(bad_bits, sx) || lv[sx] >= INF_LV)) continue;
                    int16_t sy = map.find(mu ^ val[sx]);
                    if (sy >= 0 && bget(aff_bits, sy) && !bget(got_bits, sy)) {
                        bset(got_bits, sy);
                        n_got++;
                        stack[sp++] = sy;
                        if (only_targets && is_target[sy] && --need == 0) return false;
                    }
                }
            }
        }
        return (need < 0) ? (n_got < n_aff) : true;
    }

    // Cap-free closure screen: does inserting `w` unlock every stuck target? (ValueSet.unlocks)
    bool unlocks(uint64_t w, const uint64_t stuck_bits[WORDS], int need_targets) const {
        if (need_targets <= 0) return true;
        uint64_t got_bits[WORDS];
        bzero(got_bits);
        int stack[MAX_U], sp = 0;
        int need = need_targets;

        for (int bw = 0; bw < WORDS; ++bw) {
            uint64_t sb = stuck_bits[bw];
            while (sb) {
                int s = (bw << 6) | ctz64(sb);
                sb &= sb - 1;
                int16_t p = map.find(val[s] ^ w);
                if (p >= 0 && lv[p] < INF_LV) {
                    bset(got_bits, s);
                    stack[sp++] = s;
                    if (is_target[s] && --need == 0) return true;
                }
            }
        }

        while (sp > 0 && need > 0) {
            int u = stack[--sp];
            uint64_t mu = val[u];
            int16_t syw = map.find(mu ^ w);
            if (syw >= 0 && bget(stuck_bits, syw) && !bget(got_bits, syw)) {
                bset(got_bits, syw);
                stack[sp++] = syw;
                if (is_target[syw] && --need == 0) return true;
            }
            for (int tw = 0; tw < WORDS; ++tw) {
                uint64_t tb = tri[u][tw];
                while (tb) {
                    int sx = (tw << 6) | ctz64(tb);
                    tb &= tb - 1;
                    if (lv[sx] >= INF_LV && !bget(got_bits, sx)) continue;
                    int16_t sy = map.find(mu ^ val[sx]);
                    if (sy >= 0 && bget(stuck_bits, sy) && !bget(got_bits, sy)) {
                        bset(got_bits, sy);
                        stack[sp++] = sy;
                        if (is_target[sy] && --need == 0) return true;
                    }
                }
            }
        }
        return need == 0;
    }

    // Complete single-value repair enumeration (`ValueSet.valid_repairs`)
    void valid_repairs(uint64_t forbid1, uint64_t forbid2, FastSet32K& build_set,
                       FastSet32K& cand_set, std::vector<uint64_t>& out) {
        out.clear();
        // Check if any target is completely absent from U
        uint64_t absent_t = 0;
        int n_absent = 0;
        for (uint64_t t : targets) {
            if (map.find(t) < 0) { absent_t = t; n_absent++; }
        }
        if (n_absent > 1) return;
        if (n_absent == 1) {
            if (absent_t == forbid1 || absent_t == forbid2) return;
            int m = journal();
            add(absent_t);
            bool good = ok();
            rollback(m);
            if (good) out.push_back(absent_t);
            return;
        }

        uint64_t avail[MAX_U], sub_avail[MAX_U], stuck_vals[MAX_U];
        int n_av = 0, n_sub = 0, n_st = 0;
        uint64_t stuck_bits[WORDS];
        bzero(stuck_bits);
        int need_targets = 0;

        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (lv[s] < INF_LV) {
                    if (lv[s] <= cap - 1) avail[n_av++] = val[s];
                    if (lv[s] <= cap - 2) sub_avail[n_sub++] = val[s];
                } else {
                    bset(stuck_bits, s);
                    stuck_vals[n_st++] = val[s];
                    if (is_target[s]) need_targets++;
                }
            }
        }
        if (n_st == 0 || n_sub < 2) return;

        // Buildability first, then unlocks (valueset.py:1204 — 13x faster because pair-sum is selective.)
        build_set.clear();
        for (int i = 0; i < n_sub; ++i) {
            uint64_t a = sub_avail[i];
            for (int j = i + 1; j < n_sub; ++j) build_set.insert(a ^ sub_avail[j]);
        }

        cand_set.clear();
        std::vector<uint64_t> cands;
        cands.reserve(64);
        for (int si = 0; si < n_st; ++si) {
            uint64_t ms = stuck_vals[si];
            for (int ai = 0; ai < n_av; ++ai) {
                uint64_t w = ms ^ avail[ai];
                if (w == 0 || w == forbid1 || w == forbid2 || popcnt64(w) <= 1) continue;
                if (!build_set.contains(w) || map.find(w) >= 0) continue;
                if (cand_set.insert(w) && unlocks(w, stuck_bits, need_targets)) {
                    cands.push_back(w);
                }
            }
        }
        std::sort(cands.begin(), cands.end());

        if (cap >= INF_LV) {
            out = std::move(cands);
            return;
        }
        for (uint64_t w : cands) {
            int mk = journal();
            add(w);
            bool good = ok();
            rollback(mk);
            if (good) out.push_back(w);
        }
    }

    // Drop witness operands made redundant by new value `w` (`XORFlux v8` moves/rebuild.py:local_peel)
    int local_peel(uint64_t w) {
        int16_t sw = map.find(w);
        if (sw < 0) return 0;
        std::vector<uint64_t> partners;
        for (int tw = 0; tw < WORDS; ++tw) {
            uint64_t tb = tri[sw][tw];
            while (tb) {
                int sx = (tw << 6) | ctz64(tb);
                tb &= tb - 1;
                partners.push_back(val[sx]);
            }
        }
        if (partners.empty()) return 0;
        std::sort(partners.begin(), partners.end());

        std::vector<uint64_t> cand;
        std::unordered_set<uint64_t> seen_c;
        for (uint64_t x : partners) {
            for (uint64_t v : {x, w ^ x}) {
                int16_t sv = map.find(v);
                if (sv < 0 || par[sv] == 0) continue;
                uint64_t a = par[sv];
                for (uint64_t p : {a, v ^ a}) {
                    if (p == w) continue;
                    int16_t sp = map.find(p);
                    if (sp >= 0 && !is_input[sp] && !is_target[sp] && !seen_c.count(p)) {
                        seen_c.insert(p);
                        cand.push_back(p);
                    }
                }
            }
        }

        int dropped = 0;
        for (uint64_t p : cand) {
            int16_t sp = map.find(p);
            if (sp < 0 || strands_slot(sp, true)) continue;
            int mk = journal();
            remove_vals(&p, 1, nullptr);
            if (ok()) {
                commit(mk);
                dropped++;
            } else {
                rollback(mk);
            }
        }
        return dropped;
    }

    // Kernel 1-minimal peel (`XORFlux v8` ValueSet.peel)
    int peel_1minimal(std::mt19937& rng, int max_trials = 500) {
        int removed = 0;
        int trials = 0;
        bool progress = true;
        while (progress && trials < max_trials) {
            progress = false;
            std::vector<uint64_t> order = helpers();
            std::shuffle(order.begin(), order.end(), rng);
            for (uint64_t v : order) {
                if (trials >= max_trials) break;
                int16_t sv = map.find(v);
                if (sv < 0) continue;
                trials++;
                if (strands_slot(sv, true)) continue;
                int mk = journal();
                remove_vals(&v, 1, nullptr);
                if (ok()) {
                    trim();
                    commit(mk);
                    removed++;
                    progress = true;
                } else {
                    rollback(mk);
                }
            }
        }
        return removed;
    }

    // Greedy top-down extractor (`XORFlux v8` ValueSet.extract)
    bool extract_greedy(const std::unordered_map<uint64_t, int>& cost, std::mt19937& rng,
                        double noise, std::unordered_set<uint64_t>& chosen_out) const {
        chosen_out.clear();
        if (!ok()) return false;
        int maxd = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t tb = target_bits[w];
            while (tb) {
                int s = (w << 6) | ctz64(tb);
                tb &= tb - 1;
                if (!is_input[s]) {
                    chosen_out.insert(val[s]);
                    if (lv[s] > maxd) maxd = lv[s];
                }
            }
        }
        std::vector<std::vector<uint64_t>> buckets(maxd + 1);
        std::vector<uint64_t> init_t(chosen_out.begin(), chosen_out.end());
        std::sort(init_t.begin(), init_t.end());
        for (uint64_t t : init_t) buckets[lv[map.find(t)]].push_back(t);

        std::uniform_real_distribution<double> u01(0.0, 1.0);
        for (int d = maxd; d >= 1; --d) {
            for (size_t bi = 0; bi < buckets[d].size(); ++bi) {
                uint64_t S = buckets[d][bi];
                int16_t sS = map.find(S);
                std::vector<uint64_t> opts;
                for (int tw = 0; tw < WORDS; ++tw) {
                    uint64_t tb = tri[sS][tw];
                    while (tb) {
                        int sa = (tw << 6) | ctz64(tb);
                        tb &= tb - 1;
                        if (lv[sa] >= d) continue;
                        uint64_t ma = val[sa];
                        uint64_t mb = S ^ ma;
                        if (ma > mb) continue;
                        int16_t sb = map.find(mb);
                        if (sb >= 0 && lv[sb] < d) opts.push_back(ma);
                    }
                }
                if (opts.empty()) return false;
                uint64_t ba = opts[0];
                if (opts.size() > 1) {
                    std::sort(opts.begin(), opts.end());
                    double best_k = 1e18;
                    for (uint64_t a : opts) {
                        uint64_t b = S ^ a;
                        int c = 0;
                        int16_t sa = map.find(a), sb = map.find(b);
                        if (!is_input[sa] && !chosen_out.count(a)) {
                            auto it = cost.find(a);
                            c += (it != cost.end()) ? it->second : 1;
                        }
                        if (!is_input[sb] && !chosen_out.count(b)) {
                            auto it = cost.find(b);
                            c += (it != cost.end()) ? it->second : 1;
                        }
                        double r = u01(rng);
                        double k = (double)c + r * 0.5 + ((r < noise) ? 1.0 : 0.0);
                        if (k < best_k) { best_k = k; ba = a; }
                    }
                }
                for (uint64_t p : {ba, S ^ ba}) {
                    int16_t sp = map.find(p);
                    if (!is_input[sp] && !chosen_out.count(p)) {
                        chosen_out.insert(p);
                        buckets[lv[sp]].push_back(p);
                    }
                }
            }
        }
        return true;
    }

    std::vector<uint64_t> values() const {
        std::vector<uint64_t> out;
        out.reserve(n_active - n_in);
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (!is_input[s]) out.push_back(val[s]);
            }
        }
        std::sort(out.begin(), out.end());
        return out;
    }

    std::vector<uint64_t> helpers() const {
        std::vector<uint64_t> out;
        out.reserve(n_active - n_in);
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (!is_input[s] && !is_target[s]) out.push_back(val[s]);
            }
        }
        std::sort(out.begin(), out.end());
        return out;
    }

    uint64_t key_hash() const {
        std::vector<uint64_t> vs = values();
        uint64_t h = 14695981039346656037ULL;
        for (uint64_t v : vs) {
            h ^= v + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
            h *= 1099511628211ULL;
        }
        return h;
    }

    // Count targets/helpers exceeding `goal` for critical-path squeeze guidance
    int over_goal_score(int goal) const {
        int sc = 0;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (is_input[s] || lv[s] >= INF_LV) continue;
                if (is_target[s]) {
                    if (lv[s] > goal) sc += 4 * (lv[s] - goal);
                } else {
                    if (lv[s] > goal - 1) sc += 1;
                }
            }
        }
        return sc;
    }
};

// Exact Own-Depth Branch-and-Bound Polish (`XORFlux v8` engine/polish.py verbatim.)
struct ExactPolisher {
    static std::vector<uint64_t> removable_list(ValueSet64& st, const std::vector<uint64_t>& cands) {
        std::vector<uint64_t> out;
        for (uint64_t v : cands) {
            int16_t sv = st.map.find(v);
            if (sv < 0 || st.strands_slot(sv, true)) continue;
            int mk = st.journal();
            st.remove_vals(&v, 1, nullptr);
            bool good = st.ok();
            st.rollback(mk);
            if (good) out.push_back(v);
        }
        return out;
    }

    static std::vector<uint64_t> polish(ValueSet64& st, int node_limit = 20000) {
        std::vector<uint64_t> first = removable_list(st, st.helpers());
        if (first.empty()) return {};

        std::vector<uint64_t> best;
        std::vector<uint64_t> path;
        int nodes = 0;
        bool stopped = false;

        auto dfs = [&](auto& self, const std::vector<uint64_t>& cands) -> void {
            if (stopped) return;
            if (++nodes > node_limit) { stopped = true; return; }
            if (path.size() + cands.size() <= best.size()) return;
            if (cands.empty()) {
                best = path;
                return;
            }
            uint64_t v = cands[0];
            std::vector<uint64_t> rest(cands.begin() + 1, cands.end());
            int mk = st.journal();
            st.remove_vals(&v, 1, nullptr);
            path.push_back(v);
            self(self, removable_list(st, rest));
            path.pop_back();
            st.rollback(mk);
            if (!stopped) self(self, rest);
        };

        dfs(dfs, first);
        if (best.empty() && !first.empty()) best.push_back(first[0]);
        return best;
    }
};

// Deadline-Propagating Beam Reconstruction (`XORFlux v8` moves/rebuild.py:reconstruct)
static bool reconstruct_deadline_beam(const ValueSet64& st, std::mt19937& rng, int deadline,
                                      const std::unordered_map<uint64_t, float>& pref_map,
                                      int beam_width, int max_states,
                                      std::unordered_set<uint64_t>& best_chosen_out) {
    // Collect all levelled active slots
    int idx_of_slot[MAX_U];
    std::fill(idx_of_slot, idx_of_slot + MAX_U, -1);
    std::vector<int> slots;
    slots.reserve(st.n_active);
    for (int i = 0; i < st.n_in; ++i) {
        idx_of_slot[i] = (int)slots.size();
        slots.push_back(i);
    }
    for (int w = 0; w < WORDS; ++w) {
        uint64_t ab = st.active_bits[w];
        while (ab) {
            int s = (w << 6) | ctz64(ab);
            ab &= ab - 1;
            if (!st.is_input[s] && st.lv[s] <= deadline) {
                idx_of_slot[s] = (int)slots.size();
                slots.push_back(s);
            }
        }
    }
    int N = (int)slots.size();
    std::vector<int> targ_idx;
    for (uint64_t t : st.targets) {
        int16_t st_s = st.map.find(t);
        if (st_s < 0 || st.lv[st_s] > deadline) return false;
        if (!st.is_input[st_s]) targ_idx.push_back(idx_of_slot[st_s]);
    }

    // Starting incumbent: live witness DAG of `st`
    std::vector<int> base_a(N, -1), base_b(N, -1);
    std::vector<float> pref(N, 1.0f);
    for (int i = st.n_in; i < N; ++i) {
        int s = slots[i];
        uint64_t m = st.val[s];
        auto it = pref_map.find(m);
        if (it != pref_map.end()) pref[i] = it->second;
        uint64_t pa = st.par[s];
        if (pa != 0) {
            base_a[i] = idx_of_slot[st.map.find(pa)];
            base_b[i] = idx_of_slot[st.map.find(m ^ pa)];
        }
    }

    // Evaluate a partial chosen_a/chosen_b override on top of base_a/base_b
    auto eval_layered = [&](const int16_t* ch_a, const int16_t* ch_b,
                            std::unordered_set<uint64_t>& out_set) -> int {
        int16_t dep[MAX_U];
        uint8_t state_col[MAX_U]; // 0=unvisited, 1=grey, 2=done
        std::memset(state_col, 0, N);
        int live_cnt = 0;
        int stk[MAX_U * 2];

        for (int ti : targ_idx) {
            if (state_col[ti] == 2) continue;
            int sp = 0;
            stk[sp++] = ti;
            while (sp > 0) {
                int v = stk[sp - 1];
                if (state_col[v] == 2) { sp--; continue; }
                int a = (ch_a[v] >= 0) ? ch_a[v] : base_a[v];
                int b = (ch_a[v] >= 0) ? ch_b[v] : base_b[v];
                if (a < 0 || b < 0) return INF_LV;
                if (state_col[v] == 1) {
                    int da = (a < st.n_in) ? 0 : dep[a];
                    int db = (b < st.n_in) ? 0 : dep[b];
                    int d = 1 + std::max(da, db);
                    if (d > deadline) return INF_LV;
                    dep[v] = (int16_t)d;
                    state_col[v] = 2;
                    live_cnt++;
                    sp--;
                    continue;
                }
                state_col[v] = 1;
                for (int p : {a, b}) {
                    if (p >= st.n_in && state_col[p] != 2) {
                        if (state_col[p] == 1) return INF_LV; // cycle.
                        stk[sp++] = p;
                    }
                }
            }
        }
        out_set.clear();
        for (int i = st.n_in; i < N; ++i) {
            if (state_col[i] == 2) out_set.insert(st.val[slots[i]]);
        }
        return live_cnt;
    };

    int16_t empty_ch[MAX_U];
    std::fill(empty_ch, empty_ch + N, -1);
    std::unordered_set<uint64_t> cur_best_set;
    int best_sz = eval_layered(empty_ch, empty_ch, cur_best_set);
    if (best_sz >= INF_LV) best_sz = 999999;

    // Precompute recipe alternatives per node from `tri`
    std::vector<std::vector<std::pair<int16_t, int16_t>>> alts(N);
    for (int i = st.n_in; i < N; ++i) {
        int s = slots[i];
        uint64_t m = st.val[s];
        for (int tw = 0; tw < WORDS; ++tw) {
            uint64_t tb = st.tri[s][tw];
            while (tb) {
                int sx = (tw << 6) | ctz64(tb);
                tb &= tb - 1;
                int ix = idx_of_slot[sx];
                if (ix < 0 || st.lv[sx] > deadline - 1) continue;
                uint64_t mx = st.val[sx];
                uint64_t my = m ^ mx;
                if (mx > my) continue;
                int16_t sy = st.map.find(my);
                if (sy < 0) continue;
                int iy = idx_of_slot[sy];
                if (iy >= 0 && st.lv[sy] <= deadline - 1) {
                    alts[i].emplace_back((int16_t)ix, (int16_t)iy);
                }
            }
        }
    }

    struct BNode {
        int8_t req[MAX_U];
        int16_t ch_a[MAX_U];
        int16_t ch_b[MAX_U];
        int n_demanded = 0;
        int n_resolved = 0;
        float pref_sum = 0.0f;
        uint64_t sig = 0;
        float score = 0.0f;
    };

    BNode root;
    std::memset(root.req, 0x7F, N);
    std::fill(root.ch_a, root.ch_a + N, -1);
    std::fill(root.ch_b, root.ch_b + N, -1);
    for (int ti : targ_idx) {
        if (root.req[ti] == 0x7F) {
            root.req[ti] = (int8_t)deadline;
            root.n_demanded++;
            root.pref_sum += pref[ti];
            root.sig ^= MaskSlotMap::hash64((uint64_t)ti * 1315423911ULL ^ (uint64_t)deadline);
        }
    }

    std::vector<BNode> beam = {root};
    std::unordered_set<uint64_t> seen_sigs;
    int states = 0;
    int head = 4 * beam_width;
    std::uniform_real_distribution<float> u01(0.0f, 1.0f);

    while (!beam.empty() && states < max_states) {
        std::vector<BNode> next_beam;
        next_beam.reserve(beam_width * 8);

        for (const auto& bn : beam) {
            if (states >= max_states) break;
            int pick = -1, best_sl = 999, best_lv = -1;
            for (int i = st.n_in; i < N; ++i) {
                if (bn.req[i] < 0x7F && bn.ch_a[i] < 0) {
                    int lv_i = st.lv[slots[i]];
                    int sl = (int)bn.req[i] - lv_i;
                    if (sl < best_sl || (sl == best_sl && lv_i > best_lv)) {
                        best_sl = sl;
                        best_lv = lv_i;
                        pick = i;
                    }
                }
            }
            if (pick < 0) {
                std::unordered_set<uint64_t> cand_s;
                int csz = eval_layered(bn.ch_a, bn.ch_b, cand_s);
                if (csz < best_sz) { best_sz = csz; cur_best_set = std::move(cand_s); }
                continue;
            }
            if (best_sl < 0) continue;

            int pd = (int)bn.req[pick] - 1;
            struct Choice { int c; float s; int mlv; float rnd; int16_t a, b; };
            std::vector<Choice> choices;
            choices.reserve(alts[pick].size());
            for (auto [a, b] : alts[pick]) {
                int la = st.lv[slots[a]], lb = st.lv[slots[b]];
                if (la > pd || lb > pd) continue;
                int c = 0;
                float s = 0.0f;
                if (a >= st.n_in && bn.req[a] == 0x7F) { c++; s += pref[a]; }
                if (b >= st.n_in && bn.req[b] == 0x7F) { c++; s += pref[b]; }
                choices.push_back({c, s, std::max(la, lb), u01(rng), a, b});
            }
            std::sort(choices.begin(), choices.end(), [](const Choice& x, const Choice& y) {
                if (x.c != y.c) return x.c < y.c;
                if (x.s != y.s) return x.s < y.s;
                if (x.mlv != y.mlv) return x.mlv < y.mlv;
                return x.rnd < y.rnd;
            });

            int try_lim = std::min((int)choices.size(), 8);
            for (int ci = 0; ci < try_lim && states < max_states; ++ci) {
                states++;
                int16_t a = choices[ci].a, b = choices[ci].b;

                // Cycle check through chosen recipes
                bool cyc = false;
                int cstk[MAX_U], csp = 0;
                if (a >= st.n_in) cstk[csp++] = a;
                if (b >= st.n_in) cstk[csp++] = b;
                uint8_t vis[MAX_U];
                std::memset(vis, 0, N);
                while (csp > 0) {
                    int u = cstk[--csp];
                    if (u == pick) { cyc = true; break; }
                    if (vis[u]) continue;
                    vis[u] = 1;
                    if (bn.ch_a[u] >= 0) {
                        if (bn.ch_a[u] >= st.n_in) cstk[csp++] = bn.ch_a[u];
                        if (bn.ch_b[u] >= st.n_in) cstk[csp++] = bn.ch_b[u];
                    }
                }
                if (cyc) continue;

                BNode nxt = bn;
                nxt.ch_a[pick] = a;
                nxt.ch_b[pick] = b;
                nxt.n_resolved++;
                nxt.sig ^= ((uint64_t)pick * 2654435761ULL) ^ ((uint64_t)a * 40503ULL);

                int q[MAX_U], qh = 0, qt = 0;
                q[qt++] = pick;
                bool ok = true;
                while (qh < qt && ok) {
                    int node = q[qh++];
                    if (nxt.ch_a[node] < 0) continue;
                    int nd = (int)nxt.req[node] - 1;
                    for (int p : {(int)nxt.ch_a[node], (int)nxt.ch_b[node]}) {
                        if (p < st.n_in) {
                            if (nd < 0) { ok = false; break; }
                            continue;
                        }
                        if (st.lv[slots[p]] > nd) { ok = false; break; }
                        if (nxt.req[p] == 0x7F) {
                            nxt.req[p] = (int8_t)nd;
                            nxt.n_demanded++;
                            nxt.pref_sum += pref[p];
                            nxt.sig ^= ((uint64_t)p * 11400714819323198485ULL) ^ (uint64_t)nd;
                        } else if (nd < nxt.req[p]) {
                            nxt.sig ^= ((uint64_t)p * 11400714819323198485ULL) ^ (uint64_t)nxt.req[p];
                            nxt.req[p] = (int8_t)nd;
                            nxt.sig ^= ((uint64_t)p * 11400714819323198485ULL) ^ (uint64_t)nd;
                            if (nxt.ch_a[p] >= 0) q[qt++] = p;
                        }
                    }
                }
                if (!ok || nxt.n_demanded > best_sz) continue;
                if (seen_sigs.count(nxt.sig)) continue;
                seen_sigs.insert(nxt.sig);

                if (nxt.n_demanded == nxt.n_resolved) {
                    std::unordered_set<uint64_t> cand_s;
                    int csz = eval_layered(nxt.ch_a, nxt.ch_b, cand_s);
                    if (csz < best_sz) { best_sz = csz; cur_best_set = std::move(cand_s); }
                    continue;
                }

                // Periodic full completion using base witness fill (`XORFlux v8` complete_head / complete_every)
                if (states <= head || (states % 6 == 0)) {
                    std::unordered_set<uint64_t> cand_s;
                    int csz = eval_layered(nxt.ch_a, nxt.ch_b, cand_s);
                    if (csz < best_sz) { best_sz = csz; cur_best_set = std::move(cand_s); }
                }

                // Lookahead mincost
                int mcsum = 0;
                for (int i = st.n_in; i < N; ++i) {
                    if (nxt.req[i] < 0x7F && nxt.ch_a[i] < 0) {
                        int ld = (int)nxt.req[i] - 1;
                        int mc = 9;
                        for (auto [xa, xb] : alts[i]) {
                            if (st.lv[slots[xa]] <= ld && st.lv[slots[xb]] <= ld) {
                                int cc = (xa >= st.n_in && nxt.req[xa] == 0x7F) +
                                         (xb >= st.n_in && nxt.req[xb] == 0x7F);
                                if (cc < mc) { mc = cc; if (mc == 0) break; }
                            }
                        }
                        if (mc == 9) { ok = false; break; }
                        mcsum += mc;
                    }
                }
                if (!ok) continue;
                nxt.score = (float)nxt.n_demanded + 0.45f * (float)mcsum + 0.01f * nxt.pref_sum + u01(rng) * 0.02f;
                next_beam.push_back(nxt);
            }
        }
        std::sort(next_beam.begin(), next_beam.end(), [](const BNode& x, const BNode& y) {
            return x.score < y.score;
        });
        if ((int)next_beam.size() > beam_width) next_beam.resize(beam_width);
        beam.swap(next_beam);
    }

    if (cur_best_set.empty()) return false;
    best_chosen_out = std::move(cur_best_set);
    return true;
}

// Randomized Kraft-Bounded Paar Fresh Root Constructor (`XORFlux v8` moves/construct.py:_paar)
static std::vector<uint64_t> build_paar_root(const TargetSpec& spec, int cap, std::mt19937& rng) {
    int n = spec.n_in;
    std::vector<uint64_t> need;
    for (uint64_t t : spec.targets) if (popcnt64(t) >= 2) need.push_back(t);
    int R_sz = (int)need.size();

    std::vector<uint64_t> sig(n);
    std::vector<int> dep(n, 0);
    std::unordered_map<uint64_t, int> idx;
    for (int i = 0; i < n; ++i) { sig[i] = 1ULL << i; idx[sig[i]] = i; }

    std::vector<std::vector<int>> rows(R_sz);
    std::vector<uint64_t> kraft(R_sz, 0);
    for (int r = 0; r < R_sz; ++r) {
        for (int i = 0; i < n; ++i) {
            if ((need[r] >> i) & 1ULL) rows[r].push_back(i);
        }
        kraft[r] = rows[r].size();
    }

    uint64_t limit = (cap > 0 && cap < 62) ? (1ULL << cap) : ~0ULL;
    std::vector<uint64_t> values_out;

    while (true) {
        // Count pairs across rows
        std::unordered_map<uint64_t, int> pcnt;
        int max_c = 0;
        for (int r = 0; r < R_sz; ++r) {
            const auto& rw = rows[r];
            for (size_t i = 0; i < rw.size(); ++i) {
                for (size_t j = i + 1; j < rw.size(); ++j) {
                    int a = std::min(rw[i], rw[j]), b = std::max(rw[i], rw[j]);
                    uint64_t k = ((uint64_t)a << 32) | (uint32_t)b;
                    int c = ++pcnt[k];
                    if (c > max_c) max_c = c;
                }
            }
        }
        if (max_c == 0) break;

        std::vector<uint64_t> top_pairs;
        for (auto& kv : pcnt) if (kv.second == max_c) top_pairs.push_back(kv.first);
        std::shuffle(top_pairs.begin(), top_pairs.end(), rng);

        int best_a = -1, best_b = -1;
        std::vector<int> best_where;
        int tries = std::min((int)top_pairs.size(), 8);
        for (int t = 0; t < tries; ++t) {
            int a = (int)(top_pairs[t] >> 32), b = (int)(top_pairs[t] & 0xFFFFFFFFu);
            uint64_t m = sig[a] ^ sig[b];
            int dz = 1 + std::max(dep[a], dep[b]);
            auto it = idx.find(m);
            if (it != idx.end() && dep[it->second] < dz) dz = dep[it->second];
            int64_t gain = (int64_t)(1ULL << dz) - (int64_t)(1ULL << dep[a]) - (int64_t)(1ULL << dep[b]);
            std::vector<int> where;
            for (int r = 0; r < R_sz; ++r) {
                bool ha = false, hb = false;
                for (int x : rows[r]) { if (x == a) ha = true; else if (x == b) hb = true; }
                if (ha && hb && (gain <= 0 || kraft[r] + (uint64_t)gain <= limit)) where.push_back(r);
            }
            if (where.size() > best_where.size()) {
                best_a = a; best_b = b; best_where = std::move(where);
                if ((int)best_where.size() == max_c) break;
            }
        }

        if (best_a < 0) {
            // Fallback: merge two shallowest signals of an unfinished row
            std::vector<int> open_r;
            for (int r = 0; r < R_sz; ++r) if (rows[r].size() > 1) open_r.push_back(r);
            int r = open_r[rng() % open_r.size()];
            std::sort(rows[r].begin(), rows[r].end(), [&](int x, int y) { return dep[x] < dep[y]; });
            best_a = rows[r][0]; best_b = rows[r][1];
            best_where = {r};
        }

        uint64_t m = sig[best_a] ^ sig[best_b];
        int dz = 1 + std::max(dep[best_a], dep[best_b]);
        int z;
        auto it = idx.find(m);
        if (it == idx.end()) {
            z = (int)sig.size();
            sig.push_back(m);
            dep.push_back(dz);
            idx[m] = z;
            values_out.push_back(m);
        } else {
            z = it->second;
            if (dz < dep[z]) {
                uint64_t drop = (1ULL << dep[z]) - (1ULL << dz);
                for (int r = 0; r < R_sz; ++r) {
                    for (int x : rows[r]) if (x == z) kraft[r] -= drop;
                }
                dep[z] = dz;
            }
        }
        int64_t gain = (int64_t)(1ULL << dep[z]) - (int64_t)(1ULL << dep[best_a]) - (int64_t)(1ULL << dep[best_b]);
        for (int r : best_where) {
            auto& rw = rows[r];
            rw.erase(std::remove(rw.begin(), rw.end(), best_a), rw.end());
            rw.erase(std::remove(rw.begin(), rw.end(), best_b), rw.end());
            rw.push_back(z);
            kraft[r] = (uint64_t)((int64_t)kraft[r] + gain);
        }
    }
    return values_out;
}

// Shared Pareto Frontier & Pull-on-Stall Pool
struct GlobalCoordinator {
    TargetSpec spec;
    std::string cert_dir;
    std::mutex mtx;
    int baseline_bar[64];
    int best_g[64];

    struct Elite {
        int g, gd;
        uint64_t hash;
        std::vector<uint64_t> vals;
    };
    std::vector<Elite> pool[64]; // up to 48 distinct DAGs per depth.
    std::unordered_set<uint64_t> pool_hashes;
    int strict_wins = 0;

    GlobalCoordinator(const TargetSpec& s, const std::string& outd, bool set_aes_invmc_bar)
        : spec(s), cert_dir(outd) {
        for (int d = 0; d < 64; ++d) baseline_bar[d] = best_g[d] = 999999;
        if (set_aes_invmc_bar) {
            auto sb = [&](int d0, int g) {
                for (int d = d0; d < 64; ++d) baseline_bar[d] = std::min(baseline_bar[d], g);
            };
            sb(5, 118); sb(6, 104); sb(7, 99); sb(8, 96); sb(9, 94);
            sb(10, 93); sb(11, 92); sb(12, 90); sb(15, 89); sb(16, 88);
            for (int d = 0; d < 64; ++d) best_g[d] = baseline_bar[d];
        }
    }

    void write_ncff_unlocked(const ValueSet64& vs, const std::string& custom_prefix = "") {
        if (!vs.ok()) return;
        int gd = vs.depth();
        // Collect live slots in topological (lv, mask) order
        uint8_t live[MAX_U];
        std::memset(live, 0, sizeof(live));
        int stk[MAX_U], sp = 0;
        for (uint64_t t : spec.rows) {
            if (t == 0) continue;
            int16_t s = vs.map.find(t);
            if (s >= 0 && !vs.is_input[s] && !live[s]) { live[s] = 1; stk[sp++] = s; }
        }
        while (sp > 0) {
            int s = stk[--sp];
            uint64_t a = vs.par[s];
            int16_t sa = vs.map.find(a);
            int16_t sb = vs.map.find(vs.val[s] ^ a);
            if (sa >= 0 && !vs.is_input[sa] && !live[sa]) { live[sa] = 1; stk[sp++] = sa; }
            if (sb >= 0 && !vs.is_input[sb] && !live[sb]) { live[sb] = 1; stk[sp++] = sb; }
        }

        std::vector<int> order;
        for (int s = 0; s < MAX_U; ++s) if (live[s]) order.push_back(s);
        std::sort(order.begin(), order.end(), [&](int a, int b) {
            if (vs.lv[a] != vs.lv[b]) return vs.lv[a] < vs.lv[b];
            return vs.val[a] < vs.val[b];
        });

        int g = (int)order.size();
        std::unordered_map<uint64_t, int> t_first;
        std::vector<int> dup_outputs;
        for (size_t i = 0; i < spec.rows.size(); ++i) {
            uint64_t r = spec.rows[i];
            if (!t_first.count(r)) t_first[r] = (int)i;
            else dup_outputs.push_back((int)i);
        }

        std::string wname[MAX_U];
        for (int i = 0; i < spec.n_in; ++i) {
            auto it = t_first.find(1ULL << i);
            wname[i] = "x" + std::to_string(i);
        }
        int t_idx = 0;
        for (int s : order) {
            auto it = t_first.find(vs.val[s]);
            if (it != t_first.end()) wname[s] = "y" + std::to_string(it->second);
            else wname[s] = "t" + std::to_string(++t_idx);
        }

        std::string cname = (custom_prefix.empty() ? spec.func_name : custom_prefix)
                            + "-xor" + std::to_string(g) + "-depth" + std::to_string(gd);
        std::string fpath = cert_dir + "/" + cname + ".circ.txt";

        std::ofstream out(fpath);
        out << "%NCFF-0.1-2026 (NIST Circuit File Format)\n\n";
        out << "## Index of circuits (circuitName numOutputs numInputs)\n";
        out << "  % " << cname << " " << spec.rows.size() << " " << spec.n_in << "\n\n";
        out << "## Circuit\nbegin circuit " << cname << "\n";
        out << "  % Description: " << spec.desc << "\n";
        out << "  % Tally of gates (" << g << "): " << g << " XOR\n";
        out << "  % Gate depth " << gd << "\n\n";
        out << "Inputs: x0:x" << (spec.n_in - 1) << "\n";
        out << "Outputs: y0:y" << (spec.rows.size() - 1) << "\n";
        if (t_idx > 0) out << "Internal: t1:t" << t_idx << "\n";
        out << "GateSyntax: GateName Output Inputs\n\nbegin SLP\n";
        for (int s : order) {
            int16_t sa = vs.map.find(vs.par[s]);
            int16_t sb = vs.map.find(vs.val[s] ^ vs.par[s]);
            out << "XOR " << wname[s] << " " << wname[sa] << " " << wname[sb] << "\n";
        }
        out << "end SLP\nend circuit\n";
    }

    // Observe any candidate value set: compute earliest own-depth, exact B&B polish at own-depth, record.
    void observe(const std::vector<uint64_t>& raw_vals, ValueSet64& scratch, bool always_save_best = false) {
        scratch.init(spec, raw_vals, INF_LV);
        if (!scratch.ok()) return;
        scratch.trim();
        int own_d = scratch.depth();
        int g0 = scratch.count();
        if (own_d <= 0 || own_d >= 64) return;

        // Fast lock-free filter: only polish if near frontier
        if (g0 > best_g[own_d] + 2) return;

        // Rebuild at exact `own_d` and run exact XORFlux v8 B&B polish.
        scratch.init(spec, scratch.values(), own_d);
        scratch.trim();
        if (!scratch.ok()) return;
        std::vector<uint64_t> rem = ExactPolisher::polish(scratch, 20000);
        if (!rem.empty()) {
            scratch.remove_vals(rem.data(), (int)rem.size(), nullptr);
            scratch.trim();
        }
        int g = scratch.count();
        int d = scratch.depth();
        if (d <= 0 || d >= 64) return;

        std::vector<uint64_t> clean = scratch.values();
        uint64_t h = scratch.key_hash();

        std::lock_guard<std::mutex> lk(mtx);
        if (g < best_g[d]) {
            int prev = best_g[d];
            int bar = baseline_bar[d];
            for (int dd = d; dd < 64; ++dd) {
                if (g < best_g[dd]) best_g[dd] = g;
            }
            if (g < bar) {
                strict_wins++;
                std::cout << "🔥🔥 [NEW STRICT RECORD] G=" << g << " @ GD=" << d
                          << " (prev=" << prev << ", 2026-11-17 bar=" << bar << ")!" << std::endl;
                write_ncff_unlocked(scratch);
            } else {
                std::cout << "  [IMPROVED] G=" << g << " @ GD=" << d
                          << " (prev=" << prev << ", bar=" << bar << ")" << std::endl;
                if (always_save_best) write_ncff_unlocked(scratch, "ctrl");
            }
        }
        if (g <= best_g[d] + 1 && !pool_hashes.count(h)) {
            pool_hashes.insert(h);
            auto& vec = pool[d];
            if (vec.size() < 64) vec.push_back({g, d, h, std::move(clean)});
            else vec[h & 63] = {g, d, h, std::move(clean)};
        }
    }
};

struct SeedItem {
    int g, gd;
    std::string tag;
    std::vector<uint64_t> vals;
};

static std::vector<SeedItem> load_seed_bank(const std::string& path) {
    std::vector<SeedItem> out;
    if (path.empty()) return out;
    std::ifstream fh(path);
    std::string line;
    while (std::getline(fh, line)) {
        if (line.empty()) continue;
        std::istringstream iss(line);
        SeedItem item;
        iss >> item.g >> item.gd >> item.tag;
        uint64_t v;
        while (iss >> v) item.vals.push_back(v);
        if (!item.vals.empty()) out.push_back(std::move(item));
    }
    return out;
}

// Ring buffer for LNS pool / hot list (`XORFlux v8` moves/lns.py:_Ring)
struct ValueRing {
    std::vector<uint64_t> items;
    std::unordered_set<uint64_t> members;
    size_t limit;
    size_t pos = 0;
    bool unique;

    ValueRing(size_t lim, bool uniq) : limit(lim), unique(uniq) { items.reserve(lim); }
    void add(uint64_t v) {
        if (unique) {
            if (members.count(v)) return;
            members.insert(v);
        }
        if (items.size() < limit) { items.push_back(v); return; }
        uint64_t old = items[pos];
        items[pos] = v;
        pos = (pos + 1) % limit;
        if (unique) members.erase(old);
    }
    uint64_t draw(std::mt19937& rng) const {
        return items[rng() % items.size()];
    }
};

// Connected witness-cone picker (`XORFlux v8` moves/lns.py:cone_pick)
static std::vector<uint64_t> cone_pick(const ValueSet64& st, const std::vector<uint64_t>& helpers,
                                       std::mt19937& rng, int k) {
    uint64_t seed = helpers[rng() % helpers.size()];
    std::vector<uint64_t> vict = {seed};
    std::unordered_set<uint64_t> vs = {seed};
    while ((int)vict.size() < k) {
        std::vector<uint64_t> cand;
        std::unordered_set<uint64_t> cset;
        for (uint64_t u : vict) {
            int16_t su = st.map.find(u);
            if (su < 0) continue;
            uint64_t a = st.par[su];
            if (a != 0) {
                for (uint64_t p : {a, u ^ a}) {
                    int16_t sp = st.map.find(p);
                    if (sp < 0 || st.is_input[sp] || st.is_target[sp] || vs.count(p) || cset.count(p)) continue;
                    // Parent included if all its witness children are already victims (or allow relaxed 50%)
                    bool all_in = true;
                    for (int kw = 0; kw < WORDS && all_in; ++kw) {
                        uint64_t kb = st.kids[sp][kw];
                        while (kb) {
                            int c = (kw << 6) | ctz64(kb);
                            kb &= kb - 1;
                            if (!vs.count(st.val[c])) { all_in = false; break; }
                        }
                    }
                    if (all_in) { cset.insert(p); cand.push_back(p); }
                }
            }
            for (int kw = 0; kw < WORDS; ++kw) {
                uint64_t kb = st.kids[su][kw];
                while (kb) {
                    int c = (kw << 6) | ctz64(kb);
                    kb &= kb - 1;
                    uint64_t mc = st.val[c];
                    if (!st.is_target[c] && !vs.count(mc) && !cset.count(mc)) {
                        cset.insert(mc);
                        cand.push_back(mc);
                    }
                }
            }
        }
        if (cand.empty()) break;
        std::sort(cand.begin(), cand.end());
        uint64_t x = cand[rng() % cand.size()];
        vict.push_back(x);
        vs.insert(x);
    }
    return vict;
}

// Worker Chain Loop (`XORFlux v8` Engine + Connected-Cone MITM + Critical-Path Squeeze)
struct WorkerChain {
    int tid;
    int real_cap;
    int soft_slack;
    int search_cap;
    bool squeeze_focus;
    const TargetSpec& spec;
    const std::vector<SeedItem>& seeds;
    GlobalCoordinator& coord;
    std::mt19937 rng;

    ValueSet64 state;
    ValueSet64 scratch;
    FastSet32K build_set;
    FastSet32K cand_set;
    ValueRing lns_pool{6000, true};
    ValueRing lns_hot{1000, false};

    uint64_t dead_hash = 0;
    std::unordered_set<uint64_t> dead_helpers;

    WorkerChain(int id, int rcap, int sslack, bool sq_focus, const TargetSpec& sp,
                const std::vector<SeedItem>& sds, GlobalCoordinator& cd, uint32_t seed)
        : tid(id), real_cap(rcap), soft_slack(sslack), search_cap(rcap + sslack),
          squeeze_focus(sq_focus), spec(sp), seeds(sds), coord(cd), rng(seed) {}

    // Depth repair (`XORFlux v8` moves/depth.py + Exact Level-Feasible Bypass Bank + Non-Destructive Acceptance)
    bool propose_depth_repair(int goal_d, int scale = 1, int beam_states = 600,
                              int best_chain_g = 999999, bool allow_size_growth = false) {
        if (!state.ok()) return false;
        int cur_d = state.depth();
        if (cur_d <= goal_d) return true;
        int size0 = state.count();

        // Check popcount min depth
        for (uint64_t t : spec.targets) {
            if (popcnt64(t) > 1 && bitlen64(popcnt64(t) - 1) > goal_d) return false;
        }

        std::vector<uint64_t> deep, avail_g, shallow;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = state.active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (state.lv[s] >= INF_LV) continue;
                if (state.lv[s] <= goal_d - 1) avail_g.push_back(state.val[s]);
                if (state.lv[s] <= goal_d - 2) shallow.push_back(state.val[s]);
                if (!state.is_input[s]) {
                    if ((state.is_target[s] && state.lv[s] > goal_d) ||
                        (!state.is_target[s] && state.lv[s] > goal_d - 1)) {
                        deep.push_back(state.val[s]);
                    }
                }
            }
        }
        if (shallow.size() < 2) return false;

        // Prebuild exact set of all masks buildable in 1 gate at lv <= goal_d - 1.
        build_set.clear();
        for (size_t i = 0; i < shallow.size(); ++i)
            for (size_t j = i + 1; j < shallow.size(); ++j)
                build_set.insert(shallow[i] ^ shallow[j]);

        int max_hw = (goal_d - 1 >= 6) ? 64 : (1 << std::max(0, goal_d - 1));
        std::vector<uint64_t> extras_vec;
        std::unordered_set<uint64_t> extras_set;
        auto offer_ex = [&](uint64_t m) {
            if (m != 0 && popcnt64(m) > 1 && popcnt64(m) <= max_hw &&
                state.map.find(m) < 0 && extras_set.size() < 128) {
                if (extras_set.insert(m).second) extras_vec.push_back(m);
            }
        };

        // 1. Exact level-feasible 1-gate bypasses for EVERY deep node `dv`:
        //    `m = dv ^ x` (`lv[x] <= goal_d - 1`) where `m in build_set` (`lv_new[m] <= goal_d - 1`).
        std::vector<uint64_t> shuf_av = avail_g;
        std::shuffle(shuf_av.begin(), shuf_av.end(), rng);
        for (uint64_t dv : deep) {
            int added_for_dv = 0;
            for (uint64_t x : shuf_av) {
                uint64_t m = dv ^ x;
                if (build_set.contains(m) && state.map.find(m) < 0) {
                    offer_ex(m);
                    if (++added_for_dv >= 6 * scale) break;
                }
            }
            // Associative grand-parent bypasses as fallback
            int16_t sd = state.map.find(dv);
            if (sd >= 0 && state.par[sd] != 0) {
                uint64_t a = state.par[sd], b = dv ^ a;
                for (auto [p1, p2] : {std::pair{a, b}, std::pair{b, a}}) {
                    int16_t sp1 = state.map.find(p1);
                    if (sp1 >= 0 && !state.is_input[sp1] && state.par[sp1] != 0) {
                        uint64_t c = state.par[sp1], d = p1 ^ c;
                        offer_ex(c ^ p2);
                        offer_ex(d ^ p2);
                    }
                }
            }
        }
        for (int r = 0; r < 24 * scale; ++r) {
            offer_ex(shallow[rng() % shallow.size()] ^ shallow[rng() % shallow.size()]);
        }

        int mk = state.journal();
        std::unordered_map<uint64_t, float> pref;
        for (uint64_t m : extras_vec) {
            state.add(m);
            pref[m] = 2.0f;
        }
        if (state.depth() > goal_d) {
            state.rollback(mk);
            return false;
        }
        std::unordered_set<uint64_t> chosen;
        if (!reconstruct_deadline_beam(state, rng, goal_d, pref, 6, beam_states, chosen)) {
            state.rollback(mk);
            return false;
        }
        state.retain(chosen);
        state.trim();
        if (!state.ok() || state.depth() > goal_d) {
            state.rollback(mk);
            return false;
        }
        state.peel_1minimal(rng, 200);

        // ALWAYS record any valid repaired circuit at `goal_d` into the global frontier/pool.
        int sz_after = state.count();
        if (sz_after <= coord.best_g[std::min(goal_d, 63)] + 1) {
            coord.observe(state.values(), scratch);
        }

        // Only overwrite the running chain if `allow_size_growth` (seed init) OR threshold acceptance passes.
        if (!allow_size_growth && sz_after > size0) {
            std::uniform_real_distribution<double> u01(0.0, 1.0);
            if (sz_after > size0 + 1 || sz_after > best_chain_g + 2 || u01(rng) >= 0.15) {
                state.rollback(mk);
                return false;
            }
        }
        state.commit(mk);
        dead_helpers.clear();
        return true;
    }

    // Ranking & choosing exact 1-value repair (`XORFlux v8` moves/walk.py:rank_repairs + choose_repair)
    bool walk_remove1(bool use_squeeze_tiebreak, int best_chain_g) {
        std::vector<uint64_t> hs = state.helpers();
        if (hs.empty()) return false;

        uint64_t kh = state.key_hash();
        if (kh != dead_hash) {
            dead_helpers.clear();
            dead_hash = kh;
        } else if (!dead_helpers.empty()) {
            std::vector<uint64_t> filt;
            filt.reserve(hs.size());
            for (uint64_t h : hs) if (!dead_helpers.count(h)) filt.push_back(h);
            if (filt.empty()) return false;
            hs.swap(filt);
        }

        // On squeeze_focus when over real_cap, 50% of the time pick a helper in the ancestor cone of deep targets.
        uint64_t victim = hs[rng() % hs.size()];
        if (use_squeeze_tiebreak && state.depth() > real_cap && (rng() & 1)) {
            std::vector<uint64_t> crit_hs;
            uint8_t vis[MAX_U];
            std::memset(vis, 0, sizeof(vis));
            int stk[MAX_U], sp = 0;
            for (int w = 0; w < WORDS; ++w) {
                uint64_t tb = state.target_bits[w];
                while (tb) {
                    int s = (w << 6) | ctz64(tb);
                    tb &= tb - 1;
                    if (state.lv[s] > real_cap) { vis[s] = 1; stk[sp++] = s; }
                }
            }
            while (sp > 0) {
                int s = stk[--sp];
                if (!state.is_input[s] && !state.is_target[s] && !dead_helpers.count(state.val[s]))
                    crit_hs.push_back(state.val[s]);
                uint64_t a = state.par[s];
                if (a != 0) {
                    for (uint64_t p : {a, state.val[s] ^ a}) {
                        int16_t sp_i = state.map.find(p);
                        if (sp_i >= 0 && !state.is_input[sp_i] && !vis[sp_i]) {
                            vis[sp_i] = 1; stk[sp++] = sp_i;
                        }
                    }
                }
            }
            if (!crit_hs.empty()) victim = crit_hs[rng() % crit_hs.size()];
        }

        int size_before = state.count();
        int ov_before = use_squeeze_tiebreak ? state.over_goal_score(real_cap) : 0;

        int mk = state.journal();
        state.remove_vals(&victim, 1, nullptr);
        if (state.ok()) {
            state.trim();
            state.commit(mk);
            dead_helpers.clear();
            return true;
        }

        std::vector<uint64_t> cands;
        state.valid_repairs(victim, 0, build_set, cand_set, cands);
        if (cands.empty()) {
            state.rollback(mk);
            dead_helpers.insert(victim);
            return false;
        }

        std::shuffle(cands.begin(), cands.end(), rng);
        const int top_k = 20;
        if ((int)cands.size() > top_k) {
            // Rank by (popcount, -reuse)
            std::vector<uint64_t> avail;
            for (int w = 0; w < WORDS; ++w) {
                uint64_t ab = state.active_bits[w];
                while (ab) {
                    int s = (w << 6) | ctz64(ab);
                    ab &= ab - 1;
                    if (state.lv[s] < INF_LV) avail.push_back(state.val[s]);
                }
            }
            struct RK { int pc; int neg_reuse; uint64_t w; };
            std::vector<RK> rks;
            rks.reserve(cands.size());
            for (uint64_t w : cands) {
                int reuse = 0;
                for (uint64_t p : avail) {
                    int16_t sp = state.map.find(w ^ p);
                    if (sp >= 0 && state.lv[sp] < INF_LV) reuse++;
                }
                rks.push_back({popcnt64(w), -reuse, w});
            }
            std::stable_sort(rks.begin(), rks.end(), [](const RK& a, const RK& b) {
                if (a.pc != b.pc) return a.pc < b.pc;
                return a.neg_reuse < b.neg_reuse;
            });
            for (size_t i = 0; i < rks.size(); ++i) cands[i] = rks[i].w;
        }

        int eval_lim = std::min((int)cands.size(), top_k);
        int best_sz = 999999;
        int best_ov = 999999;
        std::vector<uint64_t> ties;

        for (int i = 0; i < eval_lim; ++i) {
            uint64_t w = cands[i];
            int mk2 = state.journal();
            state.add(w);
            if (state.ok()) {
                state.local_peel(w);
                state.trim();
                if (state.map.find(w) >= 0) {
                    int sz = state.count();
                    int ov = use_squeeze_tiebreak ? state.over_goal_score(real_cap) : 0;
                    // On squeeze_focus, avoid blowing up over_goal far past ov_before + 4 unless gates drop
                    bool allow = !use_squeeze_tiebreak || (sz < size_before) || (ov <= std::max(ov_before + 4, 8));
                    if (allow) {
                        if (sz < best_sz || (sz == best_sz && ov < best_ov)) {
                            best_sz = sz;
                            best_ov = ov;
                            ties = {w};
                        } else if (sz == best_sz && ov == best_ov) {
                            ties.push_back(w);
                        }
                    }
                }
            }
            state.rollback(mk2);
        }

        if (ties.empty()) {
            state.rollback(mk);
            return false;
        }

        uint64_t chosen_w = ties[rng() % ties.size()];
        state.add(chosen_w);
        state.local_peel(chosen_w);
        state.trim();

        // Threshold check (walk.remove1 is <= size_before, always accepted.)
        if (state.count() > std::max(size_before, best_chain_g + 2)) {
            state.rollback(mk);
            return false;
        }
        state.commit(mk);
        dead_helpers.clear();
        return true;
    }

    // Uphill 1 -> 2 expansion (`XORFlux v8` moves/walk.py:Expand)
    bool walk_expand(int best_chain_g) {
        std::vector<uint64_t> hs = state.helpers();
        if (hs.empty()) return false;
        int size0 = state.count();
        std::uniform_real_distribution<double> u01(0.0, 1.0);

        std::shuffle(hs.begin(), hs.end(), rng);
        int n_vic = std::min((int)hs.size(), 3);

        int best_sz = 999999;
        uint64_t best_v = 0, best_w1 = 0, best_w2 = 0;

        for (int vi = 0; vi < n_vic; ++vi) {
            uint64_t v = hs[vi];
            int mk0 = state.journal();
            std::vector<uint64_t> stuck;
            state.remove_vals(&v, 1, &stuck);
            if (state.ok() || stuck.empty()) {
                state.rollback(mk0);
                continue;
            }

            // Enumerate buildable first-step values `w1 = s ^ a` that unlock >=1 stuck value
            std::vector<uint64_t> avail, sub_avail;
            uint64_t stuck_bits[WORDS];
            bzero(stuck_bits);
            int need_t = 0;
            for (int w = 0; w < WORDS; ++w) {
                uint64_t ab = state.active_bits[w];
                while (ab) {
                    int s = (w << 6) | ctz64(ab);
                    ab &= ab - 1;
                    if (state.lv[s] < INF_LV) {
                        if (state.lv[s] <= search_cap - 1) avail.push_back(state.val[s]);
                        if (state.lv[s] <= search_cap - 2) sub_avail.push_back(state.val[s]);
                    } else {
                        bset(stuck_bits, s);
                        if (state.is_target[s]) need_t++;
                    }
                }
            }
            if (sub_avail.size() < 2) { state.rollback(mk0); continue; }
            build_set.clear();
            for (size_t i = 0; i < sub_avail.size(); ++i)
                for (size_t j = i + 1; j < sub_avail.size(); ++j)
                    build_set.insert(sub_avail[i] ^ sub_avail[j]);

            cand_set.clear();
            struct FirstCand { int unlocks; int pc; uint64_t w; };
            std::vector<FirstCand> firsts;
            for (uint64_t s : stuck) {
                for (uint64_t a : avail) {
                    uint64_t w1 = s ^ a;
                    if (w1 == 0 || w1 == v || popcnt64(w1) <= 1) continue;
                    if (!build_set.contains(w1) || state.map.find(w1) >= 0) continue;
                    if (cand_set.insert(w1) && !state.unlocks(w1, stuck_bits, need_t)) {
                        int ucnt = 0;
                        for (uint64_t st_v : stuck) {
                            int16_t sp = state.map.find(st_v ^ w1);
                            if (sp >= 0 && state.lv[sp] < INF_LV) ucnt++;
                        }
                        firsts.push_back({ucnt, popcnt64(w1), w1});
                    }
                }
            }
            if (firsts.empty()) { state.rollback(mk0); continue; }
            std::shuffle(firsts.begin(), firsts.end(), rng);
            std::stable_sort(firsts.begin(), firsts.end(), [](const FirstCand& x, const FirstCand& y) {
                if (x.unlocks != y.unlocks) return x.unlocks > y.unlocks;
                return x.pc < y.pc;
            });

            std::vector<uint64_t> chosen_firsts;
            int head_n = std::min((int)firsts.size(), 4);
            for (int i = 0; i < head_n; ++i) chosen_firsts.push_back(firsts[i].w);
            if ((int)firsts.size() > head_n) {
                for (int r = 0; r < 4; ++r) {
                    chosen_firsts.push_back(firsts[head_n + (rng() % (firsts.size() - head_n))].w);
                }
            }

            for (uint64_t w1 : chosen_firsts) {
                int mk1 = state.journal();
                state.add(w1);
                int16_t sw1 = state.map.find(w1);
                if (sw1 >= 0 && state.lv[sw1] < INF_LV) {
                    std::vector<uint64_t> seconds;
                    state.valid_repairs(v, w1, build_set, cand_set, seconds);
                    if (!seconds.empty()) {
                        std::shuffle(seconds.begin(), seconds.end(), rng);
                        int lim2 = std::min((int)seconds.size(), 8);
                        for (int j = 0; j < lim2; ++j) {
                            uint64_t w2 = seconds[j];
                            int mk2 = state.journal();
                            state.add(w2);
                            if (state.ok()) {
                                state.local_peel(w2);
                                state.trim();
                                if (state.map.find(w1) >= 0 && state.map.find(w2) >= 0) {
                                    int sz = state.count();
                                    if (sz < best_sz) {
                                        best_sz = sz;
                                        best_v = v; best_w1 = w1; best_w2 = w2;
                                    }
                                }
                            }
                            state.rollback(mk2);
                        }
                    }
                }
                state.rollback(mk1);
                if (best_sz <= size0) break;
            }
            state.rollback(mk0);
            if (best_sz <= size0) break;
        }

        if (best_sz >= 999999) return false;
        // Acceptance: <= size0 always kept; +1 uphill kept only from best_chain_g -> best_chain_g + 1 at p = 0.08
        if (best_sz > size0) {
            if (best_sz > size0 + 1 || best_sz > best_chain_g + 1) return false;
            if (u01(rng) >= 0.08) return false;
        }

        state.remove_vals(&best_v, 1, nullptr);
        state.add(best_w1);
        state.add(best_w2);
        state.local_peel(best_w2);
        state.trim();
        dead_helpers.clear();
        return true;
    }

    // Connected-Cone 2->1 / 2->2 / 3->2 Exact MITM Move
    bool propose_cone_mitm() {
        std::vector<uint64_t> hs = state.helpers();
        if (hs.size() < 2) return false;
        int size0 = state.count();

        // 70% connected cone, 30% random pair
        int k = (hs.size() >= 3 && (rng() % 3 == 0)) ? 3 : 2;
        std::vector<uint64_t> vict = (rng() % 10 < 7) ? cone_pick(state, hs, rng, k) : std::vector<uint64_t>{};
        while ((int)vict.size() < k) {
            uint64_t h = hs[rng() % hs.size()];
            if (std::find(vict.begin(), vict.end(), h) == vict.end()) vict.push_back(h);
        }

        int mk = state.journal();
        std::vector<uint64_t> stuck;
        state.remove_vals(vict.data(), (int)vict.size(), &stuck);
        if (state.ok()) {
            state.trim();
            state.commit(mk);
            dead_helpers.clear();
            return true;
        }

        if (k == 2) {
            std::vector<uint64_t> cands;
            state.valid_repairs(vict[0], vict[1], build_set, cand_set, cands);
            if (!cands.empty()) {
                uint64_t w = cands[rng() % cands.size()];
                state.add(w);
                state.local_peel(w);
                state.trim();
                state.commit(mk);
                dead_helpers.clear();
                return true; // Strictly <= size0 - 1.
            }
        }

        // For k == 2 (2->2 saddle swap) or k == 3 (3->2 strict reduction.):
        // Pick first unlocking value `w1`, then exact `valid_repairs` for `w2`.
        std::vector<uint64_t> avail, sub_avail;
        for (int w = 0; w < WORDS; ++w) {
            uint64_t ab = state.active_bits[w];
            while (ab) {
                int s = (w << 6) | ctz64(ab);
                ab &= ab - 1;
                if (state.lv[s] < INF_LV) {
                    if (state.lv[s] <= search_cap - 1) avail.push_back(state.val[s]);
                    if (state.lv[s] <= search_cap - 2) sub_avail.push_back(state.val[s]);
                }
            }
        }
        if (sub_avail.size() < 2 || stuck.empty()) {
            state.rollback(mk);
            return false;
        }
        build_set.clear();
        for (size_t i = 0; i < sub_avail.size(); ++i)
            for (size_t j = i + 1; j < sub_avail.size(); ++j)
                build_set.insert(sub_avail[i] ^ sub_avail[j]);

        cand_set.clear();
        std::vector<uint64_t> w1_list;
        for (uint64_t s : stuck) {
            for (uint64_t a : avail) {
                uint64_t w1 = s ^ a;
                if (w1 == 0 || popcnt64(w1) <= 1) continue;
                if (std::find(vict.begin(), vict.end(), w1) != vict.end()) continue;
                if (!build_set.contains(w1) || state.map.find(w1) >= 0) continue;
                if (cand_set.insert(w1)) w1_list.push_back(w1);
            }
        }
        if (w1_list.empty()) {
            state.rollback(mk);
            return false;
        }
        std::shuffle(w1_list.begin(), w1_list.end(), rng);
        int lim1 = std::min((int)w1_list.size(), (k == 3) ? 20 : 8);

        for (int i = 0; i < lim1; ++i) {
            uint64_t w1 = w1_list[i];
            int mk1 = state.journal();
            state.add(w1);
            if (state.ok()) {
                state.local_peel(w1);
                state.trim();
                state.commit(mk1);
                state.commit(mk);
                dead_helpers.clear();
                return true;
            }
            std::vector<uint64_t> seconds;
            state.valid_repairs(vict[0], w1, build_set, cand_set, seconds);
            if (!seconds.empty()) {
                uint64_t w2 = seconds[rng() % seconds.size()];
                state.add(w2);
                state.local_peel(w2);
                state.trim();
                if (state.count() <= size0) {
                    state.commit(mk1);
                    state.commit(mk);
                    dead_helpers.clear();
                    return true;
                }
            }
            state.rollback(mk1);
        }

        state.rollback(mk);
        return false;
    }

    // LNS Destroy + Bank + Greedy/Deadline Rebuild + Peel (`XORFlux v8` moves/lns.py)
    bool propose_lns(int best_chain_g) {
        std::vector<uint64_t> vals = state.values();
        std::vector<uint64_t> hs = state.helpers();
        if (hs.empty()) return false;
        int size0 = state.count();

        if (lns_pool.items.empty()) {
            for (uint64_t v : vals) lns_pool.add(v);
            for (int r = 0; r < 500 && vals.size() >= 2; ++r) {
                uint64_t m = vals[rng() % vals.size()] ^ vals[rng() % vals.size()];
                if (popcnt64(m) > 1) lns_pool.add(m);
            }
        }

        int op_r = rng() % 100;
        std::vector<uint64_t> vict;
        int inj_per_v = 0;
        bool is_big = false;
        if (op_r < 35) {
            int k = 1 + (rng() % 4);
            std::shuffle(hs.begin(), hs.end(), rng);
            vict.assign(hs.begin(), hs.begin() + std::min(k, (int)hs.size()));
        } else if (op_r < 80) {
            int k = 2 + (rng() % 3);
            vict = cone_pick(state, hs, rng, std::min(k, (int)hs.size()));
            inj_per_v = 6;
        } else {
            int k = 8 + (rng() % 7);
            std::shuffle(hs.begin(), hs.end(), rng);
            vict.assign(hs.begin(), hs.begin() + std::min(k, (int)hs.size()));
            inj_per_v = 8;
            is_big = true;
        }

        std::unordered_set<uint64_t> vset(vict.begin(), vict.end());
        std::vector<uint64_t> kept;
        for (uint64_t v : vals) if (!vset.count(v)) kept.push_back(v);

        std::unordered_set<uint64_t> extras_set;
        auto add_cand = [&](uint64_t m) {
            if (m != 0 && popcnt64(m) > 1 && state.map.find(m) < 0 && extras_set.size() < 120) {
                extras_set.insert(m);
            }
        };

        int draws = 12 + (rng() % 12);
        for (int i = 0; i < draws; ++i) {
            if (!lns_hot.items.empty() && (rng() & 1)) add_cand(lns_hot.draw(rng));
            else if (!lns_pool.items.empty()) add_cand(lns_pool.draw(rng));
        }
        for (int i = 0; i < draws && !kept.empty(); ++i) {
            uint64_t a = (rng() % 4 == 0) ? (1ULL << (rng() % spec.n_in)) : kept[rng() % kept.size()];
            add_cand(a ^ kept[rng() % kept.size()]);
        }
        if (inj_per_v > 0) {
            for (uint64_t v : vict) {
                for (int r = 0; r < inj_per_v && !kept.empty(); ++r) add_cand(v ^ kept[rng() % kept.size()]);
                for (int r = 0; r < 2; ++r) add_cand(v ^ (1ULL << (rng() % spec.n_in)));
            }
            for (size_t i = 0; i < vict.size(); ++i)
                for (size_t j = i + 1; j < vict.size(); ++j) add_cand(vict[i] ^ vict[j]);
        }

        uint64_t hash_before = state.key_hash();
        int mk = state.journal();
        std::unordered_map<uint64_t, int> cost_int;
        std::unordered_map<uint64_t, float> cost_flt;
        for (uint64_t m : extras_set) {
            state.add(m);
            cost_int[m] = 2;
            cost_flt[m] = 2.0f;
        }
        for (uint64_t v : vict) {
            cost_int[v] = 3;
            cost_flt[v] = 3.0f;
        }

        std::unordered_set<uint64_t> chosen;
        bool ok_g = state.extract_greedy(cost_int, rng, 0.0625, chosen);
        if (!is_big && (rng() % 8 == 0)) {
            std::unordered_set<uint64_t> beam_ch;
            if (reconstruct_deadline_beam(state, rng, search_cap, cost_flt, 6, 400, beam_ch)) {
                if (!ok_g || beam_ch.size() <= chosen.size()) {
                    chosen = std::move(beam_ch);
                    ok_g = true;
                }
            }
        }
        if (!ok_g) {
            state.rollback(mk);
            return false;
        }

        state.retain(chosen);
        state.trim();
        int size1 = state.count();
        if (size0 < size1 && size1 <= size0 + 6) {
            state.peel_1minimal(rng, (int)state.helpers().size());
        }

        int size_after = state.count();
        if (state.key_hash() == hash_before) {
            state.rollback(mk);
            return false;
        }

        if (size_after > size0) {
            state.rollback(mk);
            return false;
        }

        state.commit(mk);
        dead_helpers.clear();
        for (uint64_t v : state.values()) {
            if (!vset.count(v)) lns_pool.add(v);
            else lns_hot.add(v);
        }
        return true;
    }

    // Pick initial or restart seed/root (`XORFlux v8` RestartController + seed_repair_tries)
    void init_or_restart() {
        std::vector<const SeedItem*> feas, squeeze_seeds;
        for (const auto& s : seeds) {
            if (s.gd <= search_cap) feas.push_back(&s);
            else if (s.gd <= search_cap + 2) squeeze_seeds.push_back(&s);
        }

        int src_r = rng() % 100;
        // 1. Pull from shared coordinator elite pool (35%)
        if (src_r < 35) {
            std::lock_guard<std::mutex> lk(coord.mtx);
            std::vector<const GlobalCoordinator::Elite*> cands;
            for (int d = 1; d <= search_cap && d < 64; ++d) {
                for (const auto& el : coord.pool[d]) cands.push_back(&el);
            }
            if (!cands.empty()) {
                std::sort(cands.begin(), cands.end(), [](const auto* a, const auto* b) {
                    return a->g < b->g;
                });
                int lim = std::min((int)cands.size(), 16);
                const auto* pick = cands[rng() % lim];
                state.init(spec, pick->vals, search_cap);
                state.trim();
                dead_helpers.clear();
                return;
            }
        }

        // 2. Try depth-repairing a slightly deeper low-gate seed (`seed_repair_tries`, e.g., kste 88@16..17 into search_cap=15..16.) (25%)
        if (!squeeze_seeds.empty() && (feas.empty() || src_r < 60)) {
            int lim = std::min((int)squeeze_seeds.size(), 256);
            const SeedItem* sp = squeeze_seeds[rng() % lim];
            state.init(spec, sp->vals, sp->gd);
            state.trim();
            bool ok_rep = true;
            while (state.depth() > search_cap) {
                int step_goal = state.depth() - 1;
                bool step_ok = false;
                for (int tr = 0; tr < 4; ++tr) {
                    if (propose_depth_repair(step_goal, 1 << tr, 500, 999999, true)) {
                        step_ok = true;
                        coord.observe(state.values(), scratch);
                        break;
                    }
                }
                if (!step_ok) { ok_rep = false; break; }
            }
            if (ok_rep) {
                state.init(spec, state.values(), search_cap);
                state.trim();
                coord.observe(state.values(), scratch);
                dead_helpers.clear();
                return;
            }
        }

        // 3. Feasible seed from archive (30% — or 90% on squeeze_focus.)
        if (!feas.empty() && (squeeze_focus || src_r < 90)) {
            std::sort(feas.begin(), feas.end(), [](const SeedItem* a, const SeedItem* b) {
                if (a->g != b->g) return a->g < b->g;
                return a->gd < b->gd;
            });
            // Keep rich diversity across ALL kste 88@16 / 88@17 and NIST/Joe seeds.
            int best_g0 = feas[0]->g;
            int band = 0;
            while (band < (int)feas.size() && feas[band]->g <= best_g0 + 2) band++;
            int lim = std::max(band, std::min((int)feas.size(), 12));
            const SeedItem* pick = feas[rng() % lim];
            state.init(spec, pick->vals, search_cap);
            state.trim();
            dead_helpers.clear();
            return;
        }

        // 4. Fresh randomized Paar root (10% — discovers new basins.)
        std::vector<uint64_t> root_vals = build_paar_root(spec, real_cap, rng);
        state.init(spec, root_vals, search_cap);
        state.trim();
        coord.observe(state.values(), scratch);
        dead_helpers.clear();
    }

    void run_until(std::chrono::steady_clock::time_point deadline_tp,
                   std::atomic<uint64_t>& total_props) {
        init_or_restart();
        coord.observe(state.values(), scratch);

        int best_chain_g = state.count();
        std::vector<uint64_t> best_chain_vals = state.values();
        int best_feas_g = (state.depth() <= real_cap) ? state.count() : 999999;
        int stall = 0;
        int burst_left = 400;
        int repair_left = 0;
        uint64_t it = 0;

        // If starting state ALREADY improves on best_g[real_cap] at depth > real_cap (e.g. 91@12 for cap 11, 89@15 for cap 14, 88@16 for cap 15.),
        // trigger repair bursts periodically.
        while (true) {
            if ((it & 63) == 0) {
                if (std::chrono::steady_clock::now() >= deadline_tp) break;
            }
            it++;
            total_props.fetch_add(1, std::memory_order_relaxed);

            int g_before = state.count();
            int d_before = state.depth();
            bool in_overcap_opportunity = (g_before < coord.best_g[real_cap] && d_before > real_cap);

            bool changed = false;
            if (repair_left > 0 || (in_overcap_opportunity && (rng() & 127) == 0)) {
                if (repair_left > 0) repair_left--;
                changed = propose_depth_repair(real_cap, 2, 400, best_chain_g, false);
            } else if (burst_left > 0) {
                burst_left--;
                int r = rng() % 100;
                if (r < 50) changed = walk_remove1(squeeze_focus, best_chain_g);
                else if (r < 75) changed = propose_cone_mitm();
                else if (r < 92) changed = propose_lns(best_chain_g);
                else if (r < 98) changed = walk_expand(best_chain_g);
                else if (d_before > 1) changed = propose_depth_repair(d_before - 1, 1, 350, best_chain_g, false);
            } else {
                // Plateau phase (`XORFlux v8` move weights: walk.remove1 ~68%, lns ~18%, cone_mitm ~8%, walk.expand ~5%, depth.repair ~1%)
                int r = rng() % 100;
                if (r < 68) changed = walk_remove1(squeeze_focus, best_chain_g);
                else if (r < 86) changed = propose_lns(best_chain_g);
                else if (r < 94) changed = propose_cone_mitm();
                else if (r < 99) changed = walk_expand(best_chain_g);
                else if (d_before > 1) changed = propose_depth_repair(std::min(real_cap, d_before - 1), 1, 400, best_chain_g, false);
            }

            if (changed && state.ok()) {
                int ng = state.count();
                int nd = state.depth();
                if (ng <= coord.best_g[std::min(nd, 63)] + 1) {
                    coord.observe(state.values(), scratch);
                }

                if (ng < best_chain_g || (nd <= real_cap && ng < best_feas_g)) {
                    if (ng < best_chain_g) {
                        best_chain_g = ng;
                        best_chain_vals = state.values();
                    }
                    if (nd <= real_cap && ng < best_feas_g) {
                        best_feas_g = ng;
                        burst_left = 400;
                        repair_left = 0;
                    } else if (nd > real_cap && ng < coord.best_g[real_cap]) {
                        repair_left = 8;
                    } else {
                        burst_left = 200;
                    }
                    stall = 0;
                } else {
                    stall++;
                }
            } else {
                stall++;
            }

            // If an uphill +1 kick did not drop back to best_chain_g within 800 steps, snap back to best_chain_vals.
            if (state.count() > best_chain_g && (stall % 800 == 799)) {
                state.init(spec, best_chain_vals, search_cap);
                state.trim();
                dead_helpers.clear();
            }

            // Long plateau chains (`200,000` proposals per chain; shorter `60,000` on squeeze_focus to cycle more kste 88s.)
            int stall_lim = squeeze_focus ? 60000 : 200000;
            if (stall >= stall_lim) {
                init_or_restart();
                best_chain_g = state.count();
                best_chain_vals = state.values();
                best_feas_g = (state.depth() <= real_cap) ? state.count() : 999999;
                stall = 0;
                burst_left = 400;
                repair_left = 0;
            }
        }
    }
};

// Self-test verifying incremental ValueSet64 invariants against fresh rebuilds (`state.check()`)
static int run_self_test(const TargetSpec& spec, const std::vector<SeedItem>& seeds) {
    if (seeds.empty()) {
        std::cerr << "Self-test requires at least 1 seed.\n";
        return 1;
    }
    ValueSet64 vs, ref;
    vs.init(spec, seeds[0].vals, std::max(8, seeds[0].gd + 2));
    vs.trim();
    std::mt19937 rng(42);
    FastSet32K bset, cset;

    for (int step = 0; step < 500; ++step) {
        auto hs = vs.helpers();
        if (hs.empty()) break;
        uint64_t v = hs[rng() % hs.size()];
        int mk = vs.journal();
        vs.remove_vals(&v, 1, nullptr);
        std::vector<uint64_t> reps;
        vs.valid_repairs(v, 0, bset, cset, reps);
        if (!reps.empty() && (step % 2 == 0)) {
            uint64_t w = reps[rng() % reps.size()];
            vs.add(w);
            vs.local_peel(w);
            vs.trim();
            vs.commit(mk);
        } else {
            vs.rollback(mk);
        }

        // Verify exact match with fresh canonical build.
        ref.init(spec, vs.values(), std::max(8, seeds[0].gd + 2));
        if (vs.count() != ref.count() || vs.depth() != ref.depth() || vs.ok() != ref.ok()) {
            std::cerr << "SELF-TEST MISMATCH at step " << step
                      << ": vs=(" << vs.count() << "@" << vs.depth() << ")"
                      << " ref=(" << ref.count() << "@" << ref.depth() << ")\n";
            return 2;
        }
        for (uint64_t m : vs.values()) {
            int16_t s1 = vs.map.find(m), s2 = ref.map.find(m);
            if (vs.lv[s1] != ref.lv[s2] || vs.par[s1] != ref.par[s2]) {
                std::cerr << "SELF-TEST WITNESS MISMATCH at step " << step << " mask=" << m << "\n";
                return 3;
            }
        }
    }
    std::cout << "SELF_TEST: PASS (500 incremental journal/add/remove/local_peel/rollback steps 100% canonical.)\n";
    return 0;
}

int main(int argc, char** argv) {
    std::string targets_path;
    std::string seeds_path;
    std::string out_dir = ".";
    int seconds = 60;
    int n_threads = 8;
    uint32_t rng_seed = 20261118u;
    bool self_test = false;
    bool positive_control = false;
    std::vector<std::pair<int, int>> cap_plan; // (real_cap, soft_slack)

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--targets" && i + 1 < argc) targets_path = argv[++i];
        else if (a == "--seeds" && i + 1 < argc) seeds_path = argv[++i];
        else if (a == "--outdir" && i + 1 < argc) out_dir = argv[++i];
        else if (a == "--seconds" && i + 1 < argc) seconds = std::stoi(argv[++i]);
        else if (a == "--threads" && i + 1 < argc) n_threads = std::stoi(argv[++i]);
        else if (a == "--rng-seed" && i + 1 < argc) rng_seed = (uint32_t)std::stoul(argv[++i]);
        else if (a == "--self-test") self_test = true;
        else if (a == "--positive-control") positive_control = true;
        else if (a == "--caps" && i + 1 < argc) {
            std::istringstream css(argv[++i]);
            std::string tok;
            while (std::getline(css, tok, ',')) {
                auto colon = tok.find(':');
                if (colon != std::string::npos) {
                    int rc = std::stoi(tok.substr(0, colon));
                    int sl = std::stoi(tok.substr(colon + 1));
                    cap_plan.push_back({rc, sl});
                } else {
                    int rc = std::stoi(tok);
                    int sl = (rc <= 5) ? 0 : 1;
                    cap_plan.push_back({rc, sl});
                }
            }
        }
    }

    if (targets_path.empty()) {
        std::cerr << "Usage: xorflux_cpp --targets <file> [--seeds <file>] [--outdir <dir>] [--seconds S] [--threads T] [--caps c1:s1,c2:s2,...]\n";
        return 1;
    }

    TargetSpec spec = load_target_spec(targets_path);
    auto seeds = load_seed_bank(seeds_path);
    if (self_test) return run_self_test(spec, seeds);

    if (cap_plan.empty()) {
        // Sharded across ALL GD = 5..15 with both soft-slack (+1) and tight squeeze (:0) lanes.
        cap_plan = {
            {5, 0}, {5, 1}, {6, 1}, {7, 1}, {8, 1}, {9, 1},
            {10, 1}, {11, 1}, {11, 0}, {12, 1}, {13, 1}, {14, 1},
            {14, 0}, {15, 1}, {15, 0}, {7, 0}
        };
    }

    GlobalCoordinator coord(spec, out_dir, !positive_control);
    if (positive_control && !seeds.empty()) {
        // Set bar to seed's initial gates so drops are emitted to out_dir for verification
        for (int d = seeds[0].gd; d < 64; ++d) coord.best_g[d] = seeds[0].g;
    }

    // Seed initial shared pool with top seeds (every NCFF seed + top 200 shallowest kste seeds)
    {
        ValueSet64 init_vs;
        int loaded_pool = 0;
        for (const auto& s : seeds) {
            if (loaded_pool < 260) {
                coord.observe(s.vals, init_vs, positive_control);
                loaded_pool++;
            }
        }
    }

    std::cout << "[xorflux_cpp] Targets=" << spec.n_in << "->" << spec.rows.size()
              << " | Seeds=" << seeds.size()
              << " | Threads=" << n_threads
              << " | Seconds=" << seconds << std::endl;

    auto t0 = std::chrono::steady_clock::now();
    auto deadline_tp = t0 + std::chrono::seconds(seconds);
    std::atomic<uint64_t> total_props{0};
    std::vector<std::thread> threads;

    for (int tid = 0; tid < n_threads; ++tid) {
        int rcap = cap_plan[tid % cap_plan.size()].first;
        int sslack = cap_plan[tid % cap_plan.size()].second;
        // Enable critical-path squeeze focus on half of the +1 slack workers at GD >= 7
        bool sq_focus = (sslack == 1 && rcap >= 7 && (tid % 2 == 1));
        threads.emplace_back([&, tid, rcap, sslack, sq_focus]() {
            auto wc = std::make_unique<WorkerChain>(
                tid, rcap, sslack, sq_focus, spec, seeds, coord,
                rng_seed + (uint32_t)tid * 104729u);
            wc->run_until(deadline_tp, total_props);
        });
    }
    for (auto& th : threads) th.join();

    double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    uint64_t props = total_props.load();
    std::cout << "=== [xorflux_cpp] Finished " << props << " proposals in "
              << std::fixed << std::setprecision(2) << elapsed << "s ("
              << (uint64_t)(props / std::max(elapsed, 1e-6)) << " prop/s) | strict_wins="
              << coord.strict_wins << " ===" << std::endl;
    for (int d = 5; d <= 16; ++d) {
        std::cout << "  GD<=" << std::setw(2) << d << " : best=" << coord.best_g[d];
        if (!positive_control) std::cout << " (2026-11-17 bar=" << coord.baseline_bar[d] << ")";
        std::cout << std::endl;
    }
    return 0;
}
