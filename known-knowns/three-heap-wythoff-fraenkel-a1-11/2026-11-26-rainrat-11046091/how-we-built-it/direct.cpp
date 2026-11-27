// Enumerate complete middle-heap rows. Index earlier P-positions by the
// signed difference of their last two coordinates in each labeled ordering.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <utility>
#include <vector>

struct Layer {
    std::unordered_map<int, std::vector<int>> by_gap;
    std::unordered_map<int, int> least_partner;
    std::set<int> unused_gaps{0};
    int next_gap = 1;
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const int bound = std::atoi(argv[1]);
    if (bound < 11 || bound > 200000) return 2;
    std::array<Layer, 13> layers;

    auto blocks = [&](int m, int y, int z) {
        const int gap = z - y;
        if (auto it = layers[m].least_partner.find(z);
            it != layers[m].least_partner.end() && it->second < y)
            return true;

        for (int x = 0; x < m; ++x) {
            const int d = m - x;
            for (int delta = -d; delta <= d; ++delta) {
                // d2 xor d3 = d implies d3 - d2 = d - 2 * (d2 & d).
                if (((delta + d) % 2) || (((delta + d) / 2) & ~d)) continue;
                auto it = layers[x].by_gap.find(gap + delta);
                if (it == layers[x].by_gap.end()) continue;
                for (int u : it->second) {
                    if (u > y) continue;
                    const int v = u + gap + delta;
                    if (v <= z && ((y - u) ^ (z - v)) == d) return true;
                }
            }
            auto it = layers[x].by_gap.find(gap);
            if (it != layers[x].by_gap.end() &&
                std::find(it->second.begin(), it->second.end(), y) != it->second.end())
                return true;
        }

        // If the first heap stays m, both other reductions must be equal,
        // including orderings of P-positions whose smallest heap was below m.
        auto it = layers[m].by_gap.find(gap);
        if (it != layers[m].by_gap.end()) {
            for (int u : it->second)
                if (u < y) return true;
        }
        return false;
    };

    for (int y = 0; y <= bound; ++y) {
        for (int m = 0; m <= std::min(y, 12); ++m) {
            Layer &layer = layers[m];
            // A position with this middle heap is blocked throughout its row
            // if an earlier P-position has the same two fixed heap sizes.
            if (layer.least_partner.contains(y)) continue;
            int gap = -1;
            for (int candidate : layer.unused_gaps) {
                if (!blocks(m, y, y + candidate)) {
                    gap = candidate;
                    break;
                }
            }
            while (gap < 0) {
                const int candidate = layer.next_gap++;
                layer.unused_gaps.insert(candidate);
                if (!blocks(m, y, y + candidate)) gap = candidate;
            }
            layer.unused_gaps.erase(gap);
            if (layer.unused_gaps.empty())
                layer.unused_gaps.insert(layer.next_gap++);

            const int z = y + gap;
            std::cout << m << ' ' << y << ' ' << z << '\n';
            std::array<int, 3> end{m, y, z};
            do {
                auto [x, u, v] = end;
                if (x > 12) continue;
                layers[x].by_gap[v - u].push_back(u);
                auto [it, inserted] = layers[x].least_partner.emplace(u, v);
                if (!inserted) it->second = std::min(it->second, v);
            } while (std::next_permutation(end.begin(), end.end()));
        }
        if (y % 1000 == 0) std::cout.flush();
    }
}
