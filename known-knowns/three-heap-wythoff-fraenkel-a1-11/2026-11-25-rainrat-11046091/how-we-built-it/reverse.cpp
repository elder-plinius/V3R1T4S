// Mark the ordered predecessors of each P-position in a downward-closed box.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const int cap = std::atoi(argv[1]);
    if (cap < 11 || cap > 12000) return 2;
    const int side = cap + 1;
    std::vector<unsigned char> marked(13ULL * side * side);
    auto at = [&](int a, int b, int c) -> unsigned char & {
        return marked[(static_cast<size_t>(a) * side + b) * side + c];
    };
    for (int a = 0; a <= 12; ++a) {
        for (int b = a; b <= cap; ++b) {
            for (int c = b; c <= cap; ++c) {
                if (at(a, b, c)) continue;
                std::cout << a << ' ' << b << ' ' << c << '\n';
                std::array<int, 3> end{a, b, c};
                do {
                    auto [x, y, z] = end;
                    if (x > 12) continue;
                    if (y <= z) {
                        for (int first = x + 1; first <= std::min(y, 12); ++first)
                            at(first, y, z) = 1;
                    }
                    if (x <= y) {
                        for (int third = std::max(y, z + 1); third <= cap; ++third)
                            at(x, y, third) = 1;
                    }
                    for (int second = std::max(x, y + 1); second <= z; ++second)
                        at(x, second, z) = 1;
                    for (int first = x; first <= 12; ++first) {
                        for (int second = std::max(first, y); second <= cap; ++second) {
                            int third = z + ((first - x) ^ (second - y));
                            if (third >= second && third <= cap && (first != x || second != y))
                                at(first, second, third) = 1;
                        }
                    }
                } while (std::next_permutation(end.begin(), end.end()));
            }
        }
        std::cout.flush();
    }
}
