#!/usr/bin/env python3
"""Exact Rational Support Enumeration Solver for 4-Player Binary-Action Games.

Constructs and certifies an explicit generic 4-player binary-action game
with 37 regular Nash equilibria (Partial Win p1).
Uses 100% exact rational arithmetic (fractions.Fraction).
"""

import sys
import json
import itertools
from fractions import Fraction

def get_hertling_vujic_offsets():
    """Associated order maps p_j^* from Theorem 4.2 / Example 4.3 (Hertling-Vujic 2024/2026).
    
    p_1^*: 2->1, 3->2, 4->3
    p_2^*: 1->3, 3->1, 4->2
    p_3^*: 1->2, 2->3, 4->1
    p_4^*: 1->1, 2->2, 3->3
    
    Offsets a_j^i = p_j^*(i) / 4.
    """
    p_star = {
        1: {2: 1, 3: 2, 4: 3},
        2: {1: 3, 3: 1, 4: 2},
        3: {1: 2, 2: 3, 4: 1},
        4: {1: 1, 2: 2, 3: 3}
    }
    a = {}
    for j in range(1, 5):
        for i in range(1, 5):
            if i != j:
                a[(j, i)] = Fraction(p_star[j][i], 4)
    return a

def delta_i(i, x, a):
    """Compute Delta^i(x_{-i}) = prod_{j != i} (x_j - a_j^i)."""
    prod = Fraction(1, 1)
    for j in range(1, 5):
        if j != i:
            prod *= (x[j] - a[(j, i)])
    return prod

def d_delta_i_dx_k(i, k, x, a):
    """Compute partial derivative d Delta^i / d x_k."""
    if i == k:
        return Fraction(0, 1)
    prod = Fraction(1, 1)
    for j in range(1, 5):
        if j != i and j != k:
            prod *= (x[j] - a[(j, i)])
    return prod

def det2(M):
    return M[0][0]*M[1][1] - M[0][1]*M[1][0]

def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))

def det4(M):
    ans = Fraction(0, 1)
    for c in range(4):
        sub = []
        for r in range(1, 4):
            sub.append([M[r][cc] for cc in range(4) if cc != c])
        term = M[0][c] * det3(sub)
        if c % 2 == 1:
            ans -= term
        else:
            ans += term
    return ans

def compute_jacobian_det(mix_players, x, a):
    k = len(mix_players)
    if k == 0:
        return Fraction(1, 1)
    M = [[d_delta_i_dx_k(i, j, x, a) for j in mix_players] for i in mix_players]
    if k == 2:
        return det2(M)
    elif k == 3:
        return det3(M)
    elif k == 4:
        return det4(M)
    else:
        raise ValueError(f"Unsupported dimension k={k}")

def solve_support(support_tuple, a):
    """Solve the polynomial indifference system for a single support pattern out of 3^4 = 81.
    
    support_tuple: tuple of length 4, each element in {'0', '1', 'M'}.
    Returns list of regular Nash equilibria found on this support.
    """
    mix_players = [i + 1 for i in range(4) if support_tuple[i] == 'M']
    pure_0 = [i + 1 for i in range(4) if support_tuple[i] == '0']
    pure_1 = [i + 1 for i in range(4) if support_tuple[i] == '1']
    k = len(mix_players)
    
    # 1. k = 0 (pure profile)
    if k == 0:
        x = {i + 1: (Fraction(0, 1) if support_tuple[i] == '0' else Fraction(1, 1)) for i in range(4)}
        strict = True
        slacks = {}
        for i in pure_0:
            d = delta_i(i, x, a)
            slacks[f"slack_player_{i}"] = str(d)
            if not (d < 0):
                strict = False
        for i in pure_1:
            d = delta_i(i, x, a)
            slacks[f"slack_player_{i}"] = str(d)
            if not (d > 0):
                strict = False
        if strict:
            return [{
                "support": "".join(support_tuple),
                "k": 0,
                "coordinates": {str(i): str(x[i]) for i in range(1, 5)},
                "jacobian_det": "1",
                "regular": True,
                "slacks": slacks
            }]
        return []

    # 2. k = 1: In generic binary action games, D_i(x_{-i}) is independent of x_i.
    # At a pure profile for x_{-i}, D_i is non-zero (since offsets are in (0, 1)).
    # Hence no solutions.
    if k == 1:
        return []

    # 3. k = 2: exactly 2 players mix {p1, p2}.
    if k == 2:
        p1, p2 = mix_players
        q1, q2 = pure_0 + pure_1
        x_base = {}
        for i in pure_0:
            x_base[i] = Fraction(0, 1)
        for i in pure_1:
            x_base[i] = Fraction(1, 1)
        
        # Factors for pure players in Delta^{p1} and Delta^{p2}
        fac1 = (x_base[q1] - a[(q1, p1)]) * (x_base[q2] - a[(q2, p1)])
        fac2 = (x_base[q1] - a[(q1, p2)]) * (x_base[q2] - a[(q2, p2)])
        if fac1 == 0 or fac2 == 0:
            return []
        
        # Unique isolated solution for indifference:
        x_sol = dict(x_base)
        x_sol[p1] = a[(p1, p2)]
        x_sol[p2] = a[(p2, p1)]
        
        # Check interior condition (0, 1)
        if not (0 < x_sol[p1] < 1 and 0 < x_sol[p2] < 1):
            return []
        
        # Check Jacobian determinant != 0
        j_det = compute_jacobian_det(mix_players, x_sol, a)
        if j_det == 0:
            return []
        
        # Check strict best responses for pure players
        strict = True
        slacks = {}
        for i in pure_0:
            d = delta_i(i, x_sol, a)
            slacks[f"slack_player_{i}"] = str(d)
            if not (d < 0):
                strict = False
        for i in pure_1:
            d = delta_i(i, x_sol, a)
            slacks[f"slack_player_{i}"] = str(d)
            if not (d > 0):
                strict = False
        if strict:
            return [{
                "support": "".join(support_tuple),
                "k": 2,
                "coordinates": {str(i): str(x_sol[i]) for i in range(1, 5)},
                "jacobian_det": str(j_det),
                "regular": True,
                "slacks": slacks
            }]
        return []

    # 4. k = 3: 3 players mix {p1, p2, p3}, 1 pure player q
    if k == 3:
        p1, p2, p3 = mix_players
        q = (pure_0 + pure_1)[0]
        q_val = Fraction(0, 1) if q in pure_0 else Fraction(1, 1)
        
        # Non-zero pure factor
        fac1 = (q_val - a[(q, p1)])
        fac2 = (q_val - a[(q, p2)])
        fac3 = (q_val - a[(q, p3)])
        if fac1 == 0 or fac2 == 0 or fac3 == 0:
            return []
        
        # In the Hertling-Vujic product game, 3-player mixing faces have exactly
        # two 3-cycle derangements: (p1 p2 p3) and (p1 p3 p2).
        # Any other branch has contradictory assignments for some coordinate.
        solutions = []
        for perm in [(p1, p2, p3), (p1, p3, p2)]:
            x_sol = {q: q_val}
            x_sol[perm[1]] = a[(perm[1], perm[0])]
            x_sol[perm[2]] = a[(perm[2], perm[1])]
            x_sol[perm[0]] = a[(perm[0], perm[2])]
            
            # Verify indifference
            assert delta_i(p1, x_sol, a) == 0
            assert delta_i(p2, x_sol, a) == 0
            assert delta_i(p3, x_sol, a) == 0
            
            # Check interior
            if not all(0 < x_sol[p] < 1 for p in mix_players):
                continue
            
            # Check Jacobian determinant
            j_det = compute_jacobian_det(mix_players, x_sol, a)
            if j_det == 0:
                continue
            
            # Check pure player strict inequality
            d_q = delta_i(q, x_sol, a)
            slacks = {f"slack_player_{q}": str(d_q)}
            if q in pure_0 and d_q < 0:
                solutions.append({
                    "support": "".join(support_tuple),
                    "k": 3,
                    "coordinates": {str(i): str(x_sol[i]) for i in range(1, 5)},
                    "jacobian_det": str(j_det),
                    "regular": True,
                    "slacks": slacks
                })
            elif q in pure_1 and d_q > 0:
                solutions.append({
                    "support": "".join(support_tuple),
                    "k": 3,
                    "coordinates": {str(i): str(x_sol[i]) for i in range(1, 5)},
                    "jacobian_det": str(j_det),
                    "regular": True,
                    "slacks": slacks
                })
        return solutions

    # 5. k = 4: interior (totally mixed)
    if k == 4:
        # Exactly the 9 derangements in S_4
        solutions = []
        players = [1, 2, 3, 4]
        for p in itertools.permutations(players):
            if any(p[idx] == players[idx] for idx in range(4)):
                continue
            # Permutation has no fixed points
            x_sol = {players[idx]: a[(players[idx], p[idx])] for idx in range(4)}
            
            # Verify indifference
            assert all(delta_i(i, x_sol, a) == 0 for i in players)
            
            # Check interior
            if not all(0 < x_sol[i] < 1 for i in players):
                continue
            
            # Check Jacobian determinant
            j_det = compute_jacobian_det(mix_players, x_sol, a)
            if j_det == 0:
                continue
            
            solutions.append({
                "support": "".join(support_tuple),
                "k": 4,
                "coordinates": {str(i): str(x_sol[i]) for i in range(1, 5)},
                "jacobian_det": str(j_det),
                "regular": True,
                "slacks": {}
            })
        return solutions

    return []

def main():
    print("="*78)
    print("V3R1T4S Lens 1: Exact Rational Support Enumeration for 4-Player Binary-Action Games")
    print("="*78)
    
    a = get_hertling_vujic_offsets()
    print("Hertling-Vujic maximal product game offsets a_j^i:")
    for (j, i), val in sorted(a.items()):
        print(f"  a_{j}^{i} = {val}")
    
    # Export integer payoff table scaled by 64
    payoff_table = []
    for s in itertools.product([0, 1], repeat=4):
        row = {"profile": list(s)}
        for i in range(1, 5):
            if s[i-1] == 0:
                row[f"U{i}"] = 0
            else:
                prod = Fraction(64, 1)
                for j in range(1, 5):
                    if j != i:
                        prod *= (s[j-1] - a[(j, i)])
                assert prod.denominator == 1
                row[f"U{i}"] = int(prod)
        payoff_table.append(row)
    
    payoff_file = "runs/2026-10-28-2210/attempts/support_enumeration_exact/result/payoff_table_64.json"
    with open(payoff_file, "w") as f:
        json.dump(payoff_table, f, indent=2)
    print(f"\n[+] Saved exact integer payoff table to: {payoff_file}")
    
    # Enumerate all 3^4 = 81 support patterns
    support_options = ['0', '1', 'M']
    all_supports = list(itertools.product(support_options, repeat=4))
    assert len(all_supports) == 81, "Must have exactly 81 support patterns"
    
    all_equilibria = []
    counts_by_k = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    print("\nExecuting exact support enumeration across all 81 support patterns...")
    for supp in all_supports:
        eqs = solve_support(supp, a)
        for eq in eqs:
            counts_by_k[eq["k"]] += 1
            all_equilibria.append(eq)
    
    print(f"\nResults by face dimension k (number of mixing players):")
    print(f"  k = 0 (pure equilibria)       : {counts_by_k[0]} (expected 8)")
    print(f"  k = 1 (1 player mixing)       : {counts_by_k[1]} (expected 0)")
    print(f"  k = 2 (2 players mixing)      : {counts_by_k[2]} (expected 12)")
    print(f"  k = 3 (3 players mixing)      : {counts_by_k[3]} (expected 8)")
    print(f"  k = 4 (totally mixed interior): {counts_by_k[4]} (expected 9)")
    print(f"  TOTAL REGULAR NASH EQUILIBRIA : {len(all_equilibria)} (expected 37)")
    
    assert counts_by_k[0] == 8
    assert counts_by_k[1] == 0
    assert counts_by_k[2] == 12
    assert counts_by_k[3] == 8
    assert counts_by_k[4] == 9
    assert len(all_equilibria) == 37, f"Expected 37 equilibria, got {len(all_equilibria)}"
    
    # Check that all equilibria are regular and distinct
    coords_seen = set()
    for idx, eq in enumerate(all_equilibria, 1):
        coord_tuple = tuple(eq["coordinates"][str(i)] for i in range(1, 5))
        assert coord_tuple not in coords_seen, f"Duplicate equilibrium: {coord_tuple}"
        coords_seen.add(coord_tuple)
        assert eq["regular"] is True
        assert Fraction(eq["jacobian_det"]) != 0
    
    cert_file = "runs/2026-10-28-2210/attempts/support_enumeration_exact/result/certified_37_equilibria.json"
    cert_data = {
        "target": "binary-action-games-max-nash-equilibria",
        "claim": "p1",
        "description": "Explicit generic 4-player binary-action game with rational payoffs and exactly 37 regular Nash equilibria",
        "total_regular_nash_equilibria": len(all_equilibria),
        "counts_by_dimension": counts_by_k,
        "payoff_scale_factor": 64,
        "offsets_a": {f"a_{j}_{i}": str(a[(j, i)]) for (j, i) in sorted(a.keys())},
        "equilibria": all_equilibria
    }
    with open(cert_file, "w") as f:
        json.dump(cert_data, f, indent=2)
    print(f"[+] Exported certified certificate to: {cert_file}")
    
    print("\n" + "="*78)
    print("VERIFICATION COMPLETE: 37 REGULAR NASH EQUILIBRIA CERTIFIED")
    print("PASS: Partial Win p1 Certified")
    print("="*78)

if __name__ == "__main__":
    main()
