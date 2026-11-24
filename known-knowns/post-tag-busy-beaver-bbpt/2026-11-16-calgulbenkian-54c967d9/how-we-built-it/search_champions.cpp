// Fast C++20 2-Tag Enumerator & Deep Holdout Simulator for S = 7..11
// Single-threaded, < 32 MB peak RAM (reused 16 MB circular buffer).
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

struct RuleSet {
    int n;
    std::vector<std::vector<uint8_t>> w;
    std::vector<bool> defined;
};

static constexpr uint64_t RING_CAP = (1ULL << 24); // 16 MB
static constexpr uint64_t RING_MASK = RING_CAP - 1;
static uint8_t ring_buf[RING_CAP];

std::string format_rules(const RuleSet& sys) {
    std::string out;
    for (int i = 0; i < sys.n; ++i) {
        if (i > 0) out.push_back('_');
        if (sys.defined[i]) {
            for (uint8_t c : sys.w[i]) out.push_back(char('0' + c));
        } else {
            out.push_back('?');
        }
    }
    return out;
}

enum class Outcome {
    HALT,
    UNDEFINED_RULE,
    CYCLE,
    IMMORTAL_SUBSTRING,
    EPOCH_TRANSLATED_CYCLE,
    HOLDOUT_STEPS,
    HOLDOUT_SPACE
};

struct SimResult {
    Outcome outcome;
    uint64_t steps;
    int undef_sym;
};

// Sound check: if every symbol currently present on the active tape generates a closure
// where every rule is defined and has length >= 2, the tape length can never decrease!
bool active_closure_non_decreasing(const RuleSet& sys, uint64_t head, uint64_t tail) {
    uint32_t seen_mask = 0;
    uint32_t queue_mask = 0;
    for (uint64_t p = head; p < tail; ++p) {
        uint8_t c = ring_buf[p & RING_MASK];
        if (!(seen_mask & (1u << c))) {
            seen_mask |= (1u << c);
            queue_mask |= (1u << c);
        }
    }
    while (queue_mask) {
        int c = __builtin_ctz(queue_mask);
        queue_mask &= ~(1u << c);
        if (!sys.defined[c] || sys.w[c].size() < 2) return false;
        for (uint8_t d : sys.w[c]) {
            if (!(seen_mask & (1u << d))) {
                seen_mask |= (1u << d);
                queue_mask |= (1u << d);
            }
        }
    }
    return seen_mask != 0;
}

// Fast initial screening (used during adaptive tree exploration + quick deciders)
SimResult screen_system(const RuleSet& sys, uint64_t max_steps, uint64_t max_space) {
    ring_buf[0] = 0;
    ring_buf[1] = 0;
    uint64_t head = 0;
    uint64_t tail = 2;
    uint64_t steps = 0;

    // Brent exact cycle state (track up to active length 2048)
    uint64_t power = 1;
    uint64_t lam = 0;
    std::vector<uint8_t> tortoise = {0, 0};

    // Epoch translated-cycler state:
    // Record generations: gen_end = tail when head reaches previous gen_end!
    // Actually: suppose at step t_g, head == gen_start (or head == gen_start + 1),
    // so parity_offset = head - gen_start in {0, 1}, and active window is W_g = buf[head .. tail).
    // Wait: ONLY use 100% mathematically sound prefix-depletion translated cycle here:
    // If active tape X has EVEN length 2*p (2 <= 2*p <= 256), and after p steps the new active tape
    // is X followed by Y (where Y is empty -> exact cycle, or Y non-empty AND wait: if active tape becomes
    // X + Y, after p MORE steps X is consumed again leaving Y + out(X) = Y + X + Y, which changes alignment
    // UNLESS |Y| is even AND out(Y) preserves structure!).
    // Even simpler & 100% sound: what if active tape at t1 is U (even len 2*p), and out(U) = U^k for k >= 1?
    // If out(U) == U^k (k >= 2), then U -> U^k -> U^(k^2) -> ... (exponential growth, 100% sound!).
    // What about linear translated cycler: active tape is P * V^m * S, evolving in p steps to P * V^(m+d) * S (d >= 1)?
    // Check at power-of-2 steps if active tape decomposes as P + V + V + S vs earlier P + V + S? No need to risk any subtlety:
    // C++ ring buffer runs at ~400M steps/s so Brent cycle + active_closure_non_decreasing handles tree pruning cleanly!

    while (tail - head >= 2) {
        uint8_t a = ring_buf[head & RING_MASK];
        if (!sys.defined[a]) {
            return {Outcome::UNDEFINED_RULE, steps, int(a)};
        }
        if (steps >= max_steps) {
            return {Outcome::HOLDOUT_STEPS, steps, -1};
        }
        uint64_t cur_len = tail - head;
        if (cur_len > max_space) {
            return {Outcome::HOLDOUT_SPACE, steps, -1};
        }

        head += 2;
        const auto& wa = sys.w[a];
        for (uint8_t c : wa) {
            ring_buf[tail & RING_MASK] = c;
            ++tail;
        }
        ++steps;

        cur_len = tail - head;
        if (cur_len < 2) {
            return {Outcome::HALT, steps, -1};
        }

        if ((steps & 255ULL) == 0 && cur_len <= 1024) {
            if (active_closure_non_decreasing(sys, head, tail)) {
                return {Outcome::IMMORTAL_SUBSTRING, steps, -1};
            }
        }

        if (!tortoise.empty() && cur_len == tortoise.size()) {
            bool eq = true;
            for (size_t i = 0; i < cur_len; ++i) {
                if (ring_buf[(head + i) & RING_MASK] != tortoise[i]) {
                    eq = false;
                    break;
                }
            }
            if (eq) {
                return {Outcome::CYCLE, steps, -1};
            }
        }
        ++lam;
        if (lam == power) {
            power <<= 1;
            lam = 0;
            if (cur_len <= 2048) {
                tortoise.resize(cur_len);
                for (size_t i = 0; i < cur_len; ++i) {
                    tortoise[i] = ring_buf[(head + i) & RING_MASK];
                }
            } else {
                tortoise.clear();
            }
        }
    }
    return {Outcome::HALT, steps, -1};
}

// Ultra-tight deep simulation loop up to 100M steps (within 16 MB ring buffer)
SimResult deep_simulate(const RuleSet& sys, uint64_t max_steps) {
    uint8_t flat_w[16][16];
    uint8_t flat_len[16];
    for (int i = 0; i < sys.n; ++i) {
        flat_len[i] = uint8_t(sys.w[i].size());
        for (size_t j = 0; j < sys.w[i].size(); ++j) flat_w[i][j] = sys.w[i][j];
    }

    ring_buf[0] = 0;
    ring_buf[1] = 0;
    uint64_t head = 0;
    uint64_t tail = 2;
    uint64_t steps = 0;
    const uint64_t max_space = RING_CAP - 32;

    uint64_t power = 1, lam = 0;
    uint64_t tort_len = 2;
    uint8_t tort_buf[512];
    tort_buf[0] = 0; tort_buf[1] = 0;

    while (tail - head >= 2) {
        if (steps >= max_steps) return {Outcome::HOLDOUT_STEPS, steps, -1};
        uint64_t cur_len = tail - head;
        if (cur_len > max_space) return {Outcome::HOLDOUT_SPACE, steps, -1};

        uint8_t a = ring_buf[head & RING_MASK];
        head += 2;
        uint8_t wl = flat_len[a];
        for (uint8_t j = 0; j < wl; ++j) {
            ring_buf[(tail + j) & RING_MASK] = flat_w[a][j];
        }
        tail += wl;
        ++steps;

        cur_len = tail - head;
        if (cur_len < 2) return {Outcome::HALT, steps, -1};

        if (cur_len == tort_len) {
            bool eq = true;
            for (uint64_t i = 0; i < cur_len; ++i) {
                if (ring_buf[(head + i) & RING_MASK] != tort_buf[i]) { eq = false; break; }
            }
            if (eq) return {Outcome::CYCLE, steps, -1};
        }
        if (++lam == power) {
            power <<= 1;
            lam = 0;
            if (cur_len <= 512) {
                tort_len = cur_len;
                for (uint64_t i = 0; i < cur_len; ++i) tort_buf[i] = ring_buf[(head + i) & RING_MASK];
            } else {
                tort_len = 0;
            }
        }
    }
    return {Outcome::HALT, steps, -1};
}

bool valid_reachability(const RuleSet& sys) {
    std::vector<bool> reach(sys.n, false);
    std::vector<int> q = {0};
    reach[0] = true;
    size_t idx = 0;
    while (idx < q.size()) {
        int r = q[idx++];
        if (sys.defined[r]) {
            for (uint8_t c : sys.w[r]) {
                if (!reach[c]) {
                    reach[c] = true;
                    q.push_back(c);
                }
            }
        } else {
            return true; // open closure
        }
    }
    for (int i = 0; i < sys.n; ++i) if (!reach[i]) return false;
    return true;
}

template <typename F>
void enum_strings_adaptive(int n, int len, std::vector<uint8_t>& cur, int idx, uint8_t max_seen, F&& cb) {
    if (idx == len) {
        cb(cur, max_seen);
        return;
    }
    uint8_t lim = std::min<uint8_t>(uint8_t(n - 1), uint8_t(max_seen + 1));
    for (uint8_t c = 0; c <= lim; ++c) {
        cur[idx] = c;
        enum_strings_adaptive(n, len, cur, idx + 1, std::max(max_seen, c), cb);
    }
}

struct Stats {
    uint64_t total_explored = 0;
    uint64_t halted = 0;
    uint64_t max_halt_steps = 0;
    std::string champion;
    uint64_t cyclers = 0;
    uint64_t immortal = 0;
    uint64_t holdouts = 0;
};

void explore_tnf(RuleSet& sys, const std::vector<int>& lens, uint8_t max_seen,
                 uint64_t screen_steps, uint64_t deep_steps, Stats& st) {
    SimResult res = screen_system(sys, screen_steps, 65536);
    if (res.outcome == Outcome::UNDEFINED_RULE) {
        int c = res.undef_sym;
        int l = lens[c];
        std::vector<uint8_t> buf(l);
        enum_strings_adaptive(sys.n, l, buf, 0, max_seen, [&](const std::vector<uint8_t>& chars, uint8_t new_max) {
            if (c == 0 && new_max == 0 && sys.n > 1) return;
            sys.w[c] = chars;
            sys.defined[c] = true;
            if (valid_reachability(sys)) {
                explore_tnf(sys, lens, new_max, screen_steps, deep_steps, st);
            }
            sys.defined[c] = false;
            sys.w[c].clear();
        });
        return;
    }

    st.total_explored++;
    if (res.outcome == Outcome::HALT) {
        st.halted++;
        if (res.steps > st.max_halt_steps) {
            st.max_halt_steps = res.steps;
            st.champion = format_rules(sys);
        }
    } else if (res.outcome == Outcome::CYCLE) {
        st.cyclers++;
    } else if (res.outcome == Outcome::IMMORTAL_SUBSTRING) {
        st.immortal++;
    } else {
        // Deep simulation!
        SimResult dres = deep_simulate(sys, deep_steps);
        if (dres.outcome == Outcome::HALT) {
            st.halted++;
            if (dres.steps > st.max_halt_steps) {
                st.max_halt_steps = dres.steps;
                st.champion = format_rules(sys);
                std::cout << "  [DEEP HALTER NEW MAX] " << st.champion << " -> " << dres.steps << " steps!\n" << std::flush;
            } else if (dres.steps > screen_steps) {
                std::cout << "  [DEEP HALTER] " << format_rules(sys) << " -> " << dres.steps << " steps\n" << std::flush;
            }
        } else if (dres.outcome == Outcome::CYCLE) {
            st.cyclers++;
        } else {
            st.holdouts++;
        }
    }
}

template <typename F>
void enum_lengths(int n, int rem, std::vector<int>& cur, int idx, F&& cb) {
    if (idx == n - 1) {
        cur[idx] = rem;
        bool has_lt2 = false;
        for (int x : cur) if (x < 2) has_lt2 = true;
        if (has_lt2) cb(cur);
        return;
    }
    for (int i = 0; i <= rem; ++i) {
        cur[idx] = i;
        enum_lengths(n, rem - i, cur, idx + 1, cb);
    }
}

RuleSet parse_rule_str(const std::string& s) {
    RuleSet r;
    std::vector<std::vector<uint8_t>> parts = {{}};
    for (char ch : s) {
        if (ch == '_') parts.emplace_back();
        else parts.back().push_back(uint8_t(ch - '0'));
    }
    r.n = int(parts.size());
    r.w = parts;
    r.defined.assign(r.n, true);
    return r;
}

int main() {
    // 1. Calibration check
    std::pair<std::string, uint64_t> calibs[] = {
        {"0111_1", 10},
        {"111_20_", 19},
        {"11_021_2", 49},
        {"112_1_002", 779},
        {"120221_0_2", 196841}
    };
    std::cout << "=== C++20 Calibration Check ===\n";
    for (auto& [str, exp_st] : calibs) {
        RuleSet rs = parse_rule_str(str);
        SimResult sr = deep_simulate(rs, 1000000);
        std::cout << "  " << str << " -> steps=" << sr.steps << " (expected " << exp_st << ")\n";
        if (sr.outcome != Outcome::HALT || sr.steps != exp_st) {
            std::cerr << "CALIBRATION FAILED!\n";
            return 1;
        }
    }

    // 2. Search S = 7, 8, 9, 10, 11 with deep simulation!
    struct Config { int S; uint64_t screen_st; uint64_t deep_st; };
    Config configs[] = {
        {7,  2000,   100000},
        {8,  5000,   1000000},
        {9,  10000,  5000000},
        {10, 20000,  50000000},
        {11, 50000,  25000000}
    };

    for (auto cfg : configs) {
        Stats st;
        for (int n = 1; n <= cfg.S; ++n) {
            std::vector<int> lens(n, 0);
            enum_lengths(n, cfg.S - n, lens, 0, [&](const std::vector<int>& l) {
                RuleSet sys;
                sys.n = n;
                sys.w.resize(n);
                sys.defined.assign(n, false);
                explore_tnf(sys, l, 0, cfg.screen_st, cfg.deep_st, st);
            });
        }
        std::cout << "\n=== TNF Exhaustive Search S = " << cfg.S
                  << " (deep_steps = " << cfg.deep_st << ") ===\n"
                  << "  Total TNF leaves:  " << st.total_explored << "\n"
                  << "  Halted:            " << st.halted << "\n"
                  << "  Max halt steps:    " << st.max_halt_steps << " (champion: " << st.champion << ")\n"
                  << "  Cyclers:           " << st.cyclers << "\n"
                  << "  Non-dec closure:   " << st.immortal << "\n"
                  << "  Remaining holdout: " << st.holdouts << "\n" << std::flush;
    }
    return 0;
}
