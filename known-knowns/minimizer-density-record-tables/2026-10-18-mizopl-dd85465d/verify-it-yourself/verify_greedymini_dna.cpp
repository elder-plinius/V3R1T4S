// Verbatim exact expected DNA density verifier from OrensteinLab/GreedyMini
// (GreedyMini/code/density_and_gc.cpp lines 253-480 + WindowTypesManager)
#include <iostream>
#include <vector>
#include <cstdint>
#include <tuple>
#include <unordered_map>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <string>

struct WindowTypesManager {
    std::unordered_map<uint64_t, uint64_t> vector_counts;
    void add_vector(uint64_t v) {
        vector_counts[v]++;
    }
};

std::vector<uint64_t> load_vector_from_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Cannot open " + filename);
    }
    size_t size = 0;
    file.read(reinterpret_cast<char*>(&size), sizeof(size));
    std::vector<uint64_t> vec(size);
    file.read(reinterpret_cast<char*>(vec.data()), size * sizeof(uint64_t));
    return vec;
}

// Verbatim from GreedyMini/code/density_and_gc.cpp lines 253-479
std::tuple<std::vector<uint64_t>, std::vector<uint64_t>, std::vector<uint64_t>> get_gc_ruiners(uint32_t w, uint32_t k) {
    int count_checked = 100000000;
    uint64_t total_sequences = 1ULL << (w + k);

    std::vector<uint64_t> prefix_ruiners(total_sequences, 0);
    std::vector<uint64_t> suffix_ruiners(total_sequences, 0);
    std::vector<uint64_t> both_ruiners(total_sequences, 0);

    if (total_sequences <= static_cast<uint64_t>(count_checked)) {
        for (uint64_t sequence = 0; sequence < total_sequences; ++sequence) {
            uint64_t prefix_ruined_indices = 0;
            uint64_t suffix_ruined_indices = 0;

            uint64_t first_kmer = sequence >> w;
            uint64_t last_kmer = sequence & ((1ULL << k) - 1);

            for (uint32_t j = 1; j < w; ++j) {
                uint64_t kmer_at_j = (sequence >> (w - j)) & ((1ULL << k) - 1);
                if (kmer_at_j < first_kmer) {
                    prefix_ruined_indices |= (1ULL << j);
                }
                if (kmer_at_j <= last_kmer) {
                    suffix_ruined_indices |= (1ULL << j);
                }
            }

            prefix_ruiners[sequence] = prefix_ruined_indices;
            suffix_ruiners[sequence] = suffix_ruined_indices;
            both_ruiners[sequence] = prefix_ruined_indices & suffix_ruined_indices;
        }
    }
    return { prefix_ruiners, suffix_ruiners, both_ruiners };
}

double get_proportion_gc_per_window_type(uint64_t w, uint64_t k, std::vector<uint64_t>& prefix_ruiners, std::vector<uint64_t>& suffix_ruiners, std::vector<uint64_t>& both_ruiners, uint64_t window_type) {
    bool has_first_bit = (window_type & 1) == 1;
    bool has_last_bit = (window_type & (1ULL << (w))) == (1ULL << (w));

    if (has_first_bit && has_last_bit) {
        uint64_t not_ruined_count = 0;
        for (uint64_t i = 0; i < both_ruiners.size(); ++i) {
            if ((both_ruiners[i] & window_type) == 0) {
                not_ruined_count += 1;
            }
        }
        return static_cast<double>(not_ruined_count) / static_cast<double>(both_ruiners.size());
    }
    else if (has_first_bit) {
        uint64_t not_ruined_count = 0;
        for (uint64_t i = 0; i < prefix_ruiners.size(); ++i) {
            if ((prefix_ruiners[i] & window_type) == 0) {
                not_ruined_count += 1;
            }
        }
        return static_cast<double>(not_ruined_count) / static_cast<double>(prefix_ruiners.size());
    }
    else {
        uint64_t not_ruined_count = 0;
        for (uint64_t i = 0; i < suffix_ruiners.size(); ++i) {
            if ((suffix_ruiners[i] & window_type) == 0) {
                not_ruined_count += 1;
            }
        }
        return static_cast<double>(not_ruined_count) / static_cast<double>(suffix_ruiners.size());
    }
}

double get_special_case_expected_gc(uint32_t w, uint32_t k, WindowTypesManager window_types_manager) {
    auto [prefix_ruiners, suffix_ruiners, both_ruiners] = get_gc_ruiners(w, k);
    double expected_gc = 0;
    for (auto const& x : window_types_manager.vector_counts) {
        expected_gc += get_proportion_gc_per_window_type(w, k, prefix_ruiners, suffix_ruiners, both_ruiners, x.first) * x.second;
    }
    return expected_gc;
}

uint64_t gc_dfs_dna(uint32_t w, uint32_t k, const std::vector<uint64_t>& order, uint64_t kmer, uint64_t min_order, uint64_t min_indices, uint32_t lev, WindowTypesManager& window_types_manager, bool is_first_min, bool is_middle_min) {
    uint64_t n_kmers = 1ULL << k;
    uint64_t n_kmers_mask = n_kmers - 1;

    if (lev == w) {
        bool is_last_min = false;
        if (order[kmer] < min_order) {
            return 1;
        }
        else if (order[kmer] == min_order) {
            min_indices += (1ULL << lev);
            is_last_min = true;
        }

        if ((is_first_min || is_last_min)) {
            if (is_middle_min) {
                window_types_manager.add_vector(min_indices);
                return 0;
            }
            else {
                return 1;
            }
        }
        else {
            return 0;
        }
    }
    else {
        uint64_t next_kmer = (kmer << 1) & n_kmers_mask;
        if (order[kmer] < min_order) {
            min_indices = (1ULL << lev);
            return gc_dfs_dna(w, k, order, next_kmer, order[kmer], min_indices, lev + 1, window_types_manager, false, true) +
                gc_dfs_dna(w, k, order, next_kmer + 1, order[kmer], min_indices, lev + 1, window_types_manager, false, true);
        }
        else if (order[kmer] == min_order) {
            min_indices += (1ULL << lev);
            return gc_dfs_dna(w, k, order, next_kmer, min_order, min_indices, lev + 1, window_types_manager, is_first_min, true) +
                gc_dfs_dna(w, k, order, next_kmer + 1, min_order, min_indices, lev + 1, window_types_manager, is_first_min, true);
        }
        else {
            return gc_dfs_dna(w, k, order, next_kmer, min_order, min_indices, lev + 1, window_types_manager, is_first_min, is_middle_min) +
                gc_dfs_dna(w, k, order, next_kmer + 1, min_order, min_indices, lev + 1, window_types_manager, is_first_min, is_middle_min);
        }
    }
}

uint64_t prob_gc_dna(uint32_t w, uint32_t k, const std::vector<uint64_t>& order) {
    WindowTypesManager window_types_manager = WindowTypesManager();
    uint64_t total = 0;
    uint64_t n_kmers = 1ULL << k;
    uint64_t n_kmers_mask = n_kmers - 1;

    for (uint64_t pref = 0; pref < n_kmers; ++pref) {
        uint64_t next_kmer = (pref << 1) & n_kmers_mask;
        total += gc_dfs_dna(w, k, order, next_kmer, order[pref], 1, 1, window_types_manager, true, false) +
            gc_dfs_dna(w, k, order, next_kmer + 1, order[pref], 1, 1, window_types_manager, true, false);
    }

    total *= 1ULL << (w + k);

    double special_case_expected_gc = get_special_case_expected_gc(w, k, window_types_manager);
    special_case_expected_gc *= 1ULL << (w + k);

    total += static_cast<uint64_t>(special_case_expected_gc);

    return total;
}

double density_expected_dna(uint32_t w, uint32_t k, const std::vector<uint64_t>& order) {
    uint64_t total = prob_gc_dna(w, k, order);
    return static_cast<double>(total) / std::ldexp(1.0, 2 * (w + k));
}

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " [w] [k] [gm_file1] [gm_file2 ...]\n";
        return 1;
    }
    uint32_t w = std::stoul(argv[1]);
    uint32_t k = std::stoul(argv[2]);
    std::cout << std::fixed << std::setprecision(10);
    for (int i = 3; i < argc; ++i) {
        std::vector<uint64_t> ord = load_vector_from_file(argv[i]);
        uint64_t gc = prob_gc_dna(w, k, ord);
        double den = density_expected_dna(w, k, ord);
        std::cout << argv[i] << " -> prob_gc_dna = " << gc << " / 2^" << (2*(w+k))
                  << " | density_expected_dna = " << den << std::endl;
    }
    return 0;
}
