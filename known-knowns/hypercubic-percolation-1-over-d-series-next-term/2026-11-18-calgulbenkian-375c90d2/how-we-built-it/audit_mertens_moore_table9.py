#!/usr/bin/env python3
"""
Cross-checks Theorem 7 against all 8 published perimeter polynomials D_4(q)..D_11(q)
and [binom(d, 9)] D_12(1) in Mertens & Moore (arXiv:1805.02701, Appendix A), and
computes the exact newly unlocked coefficients removing Table 9 tasks (9, 12) and (11, 14).
"""

from fractions import Fraction


PUBLISHED_E_MINUS_3 = {
    4: {(0, 0): 1, (0, 1): 0, (0, 2): 0, (0, 3): 0, (1, 0): 0, (1, 1): 0},
    5: {(0, 0): 172, (0, 1): 160, (0, 2): 30, (0, 3): 0, (1, 0): 8, (1, 1): 0},
    6: {(0, 0): 17041, (0, 1): 15600, (0, 2): 4704, (0, 3): 400, (1, 0): 376, (1, 1): 84},
    7: {(0, 0): 1382400, (0, 1): 1141248, (0, 2): 350400, (0, 3): 40256, (1, 0): 15840, (1, 1): 4416},
    8: {(0, 0): 104454120, (0, 1): 77177280, (0, 2): 22232640, (0, 3): 2609280, (1, 0): 688640, (1, 1): 192000},
    9: {(0, 0): 7801139200, (0, 1): 5187225600, (0, 2): 1371264000, (0, 3): 151859200, (1, 0): 32037120, (1, 1): 8398080},
    10: {(0, 0): 593322510704, (0, 1): 357772800000, (0, 2): 86356596480, (0, 3): 8787116800, (1, 0): 1612800000, (1, 1): 389760000},
    11: {(0, 0): 46672464052224, (0, 1): 25712480747520, (0, 2): 5672976777216, (0, 3): 526170193920, (1, 0): 88050271232, (1, 1): 19520083968},
}
PUBLISHED_D12_AT_1_BINOM_D_9 = 6199599459637248


def eval_th7_row(e: int):
    f2 = Fraction(1 << e)
    ep1 = Fraction(e + 1) ** (e - 8)
    ep0 = Fraction(e) ** (e - 7)
    return {
        (0, 0): int(f2 * ep1 * Fraction(e - 3, 384) * (
            8 * e**8 - 76 * e**7 + 254 * e**6 - 345 * e**5 + 446 * e**4
            - 2240 * e**3 + 16024 * e**2 - 76155 * e + 126212
        )),
        (0, 1): int(f2 * ep1 * Fraction((e - 3) * (e - 4), 96) * (
            12 * e**6 - 56 * e**5 - 49 * e**4 + 771 * e**3 - 245 * e**2 - 7243 * e + 15930
        )),
        (0, 2): int(f2 * ep1 * Fraction((e - 3) * (e - 4), 32) * (
            8 * e**5 - 2 * e**4 - 325 * e**3 + 376 * e**2 + 5541 * e - 16990
        )),
        (0, 3): int(f2 * ep1 * Fraction((e - 3) * (e - 4) * (e - 5), 24) * (
            4 * e**3 + 51 * e**2 + 120 * e - 2195
        )),
        (1, 0): int(f2 * ep0 * Fraction((e - 3) * (e - 4), 32) * (
            2 * e**3 - 9 * e**2 + 5 * e + 50
        )),
        (1, 1): int(f2 * ep0 * Fraction((e - 3) * (e - 4) * (e - 5), 16) * (2 * e + 9)),
    }


def main():
    for e in range(4, 12):
        row = eval_th7_row(e)
        assert row == PUBLISHED_E_MINUS_3[e], f"Mismatch at D_{e}: {row} != {PUBLISHED_E_MINUS_3[e]}"
        print(f"D_{e:2d}(q) [binom(d, {e-3:2d})]: 100% EXACT MATCH across all 6 terms ({sum(row.values())} total animals)")

    r12 = eval_th7_row(12)
    s12 = sum(r12.values())
    assert s12 == PUBLISHED_D12_AT_1_BINOM_D_9, f"D_12(1) mismatch: {s12} != {PUBLISHED_D12_AT_1_BINOM_D_9}"
    print(f"\nUNLOCKED Table 9 Pade task (d=9, e=12) [estimated 4.5 years in Mertens-Moore Table 9]:")
    print(f"  [binom(d, 9)] D_12(q) = q^(26d-24) * ({r12[(0,0)]} + {r12[(0,1)]}*q^-1 + {r12[(0,2)]}*q^-2 + {r12[(0,3)]}*q^-3 + {r12[(1,0)]}*q^(-2d) + {r12[(1,1)]}*q^(-2d-1))")
    print(f"  Sum at q=1: {s12} == [binom(d, 9)] D_12(1) = {PUBLISHED_D12_AT_1_BINOM_D_9} [EXACT 16-DIGIT MATCH]")

    r14 = eval_th7_row(14)
    print(f"\nUNLOCKED Table 9 Classical task (d=11, e=14) [estimated 133,800 years in Mertens-Moore Table 9]:")
    print(f"  [binom(d, 11)] D_14(q) = q^(30d-28) * ({r14[(0,0)]} + {r14[(0,1)]}*q^-1 + {r14[(0,2)]}*q^-2 + {r14[(0,3)]}*q^-3 + {r14[(1,0)]}*q^(-2d) + {r14[(1,1)]}*q^(-2d-1))")


if __name__ == "__main__":
    main()
