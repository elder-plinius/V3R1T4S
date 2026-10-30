#!/usr/bin/env python3
"""
reproduce_disser_and_po_family.py

Exact rational verification of:
1. Disser, Feldmann, Klimm, and Mihalak (TCS 2015, arXiv:1211.2090) 5-vertex instance
   proving Price of Stability = 1769/1126.
2. The 4-vertex potential-optimal family approaching 286/175 as epsilon -> 0 (Bilo and Bove 2011).

All calculations performed using Python fractions.Fraction (arbitrary-precision exact rational arithmetic).
"""

from fractions import Fraction
import itertools
import json
import os
import sys

def run_disser_5vertex():
    # Vertices: 0: s1, 1: (t1, t3), 2: s2, 3: t2, 4: s3
    V = [0, 1, 2, 3, 4]
    edge_list = [
        (0, 1), # 0: P1 direct (cost 549)
        (0, 2), # 1: (cost 113)
        (1, 3), # 2: (cost 318)
        (1, 4), # 3: P3 direct (cost 664)
        (2, 3), # 4: P2 direct (cost 556)
        (2, 4), # 5: (cost 277)
        (3, 4)  # 6: (cost 418)
    ]
    edge_costs = [
        Fraction(549), Fraction(113), Fraction(318),
        Fraction(664), Fraction(556), Fraction(277), Fraction(418)
    ]
    edge_to_idx = {e: i for i, e in enumerate(edge_list)}
    def ekey(u, v):
        return (u, v) if (u, v) in edge_to_idx else (v, u)

    adj = {v: [] for v in V}
    for u, v in edge_list:
        adj[u].append(v)
        adj[v].append(u)

    def find_simple_paths(s, t, visited=None):
        if visited is None: visited = []
        visited = visited + [s]
        if s == t: return [visited]
        paths = []
        for nxt in adj[s]:
            if nxt not in visited:
                paths.extend(find_simple_paths(nxt, t, visited))
        return paths

    pairs = [(0, 1), (2, 3), (4, 1)] # P1, P2, P3 terminal pairs
    paths = [find_simple_paths(s, t) for s, t in pairs]
    p_edges = [[[edge_to_idx[ekey(p[i], p[i+1])] for i in range(len(p)-1)] for p in paths[j]] for j in range(3)]
    all_profiles = list(itertools.product(range(len(paths[0])), range(len(paths[1])), range(len(paths[2]))))

    def profile_cost(prof):
        used = set()
        for player, p_idx in enumerate(prof):
            used.update(p_edges[player][p_idx])
        return sum(edge_costs[e] for e in used)

    def player_share(player, p_edges_player, all_p_edges):
        cost = Fraction(0)
        for e in p_edges_player:
            cnt = 1 + sum(1 for j in range(3) if j != player and e in all_p_edges[j])
            cost += edge_costs[e] / cnt
        return cost

    ne_profiles = []
    slacks = {}
    for prof in all_profiles:
        cur_edges = [p_edges[j][prof[j]] for j in range(3)]
        is_ne = True
        for i in range(3):
            cur_c = sum(edge_costs[e] / sum(1 for j in range(3) if e in cur_edges[j]) for e in cur_edges[i])
            for alt_idx in range(len(paths[i])):
                if alt_idx == prof[i]: continue
                alt_e = p_edges[i][alt_idx]
                alt_c = sum(edge_costs[e] / (1 + sum(1 for j in range(3) if j != i and e in cur_edges[j])) for e in alt_e)
                if alt_c < cur_c:
                    is_ne = False
                    break
            if not is_ne:
                break
        if is_ne:
            ne_profiles.append(prof)

    opt_cost = min(profile_cost(p) for p in all_profiles)
    opt_profiles = [p for p in all_profiles if profile_cost(p) == opt_cost]
    ne_cost = profile_cost(ne_profiles[0]) if ne_profiles else None
    ratio = Fraction(ne_cost, opt_cost) if ne_cost else None

    result = {
        "num_vertices": len(V),
        "num_edges": len(edge_list),
        "player_paths_count": [len(p) for p in paths],
        "total_profiles": len(all_profiles),
        "ne_profiles_count": len(ne_profiles),
        "ne_profiles": [list(p) for p in ne_profiles],
        "ne_paths": [[paths[i][ne_profiles[0][i]] for i in range(3)]] if ne_profiles else [],
        "ne_cost": str(ne_cost),
        "opt_cost": str(opt_cost),
        "opt_profiles": [list(p) for p in opt_profiles],
        "ratio_exact": str(ratio),
        "ratio_float": float(ratio) if ratio else None,
        "disser_expected_ratio": "1769/1126",
        "matches_expected": (ratio == Fraction(1769, 1126))
    }
    return result

def run_potential_optimal_family(eps_list=[Fraction(1, 100), Fraction(1, 10000), Fraction(1, 1000000)]):
    results = []
    for eps in eps_list:
        edges = {
            (0, 1): Fraction(396),
            (0, 2): Fraction(374),
            (1, 3): Fraction(374),
            (0, 3): Fraction(209) + eps,
            (1, 2): Fraction(209) + eps,
            (2, 3): Fraction(282) + eps
        }
        V = [0, 1, 2, 3]
        adj = {v: [] for v in V}
        for u, v in edges:
            adj[u].append(v); adj[v].append(u)
        def ekey(u, v): return (u, v) if (u, v) in edges else (v, u)
        def find_simple_paths(s, t, visited=None):
            if visited is None: visited = []
            visited = visited + [s]
            if s == t: return [visited]
            paths = []
            for nxt in adj[s]:
                if nxt not in visited: paths.extend(find_simple_paths(nxt, t, visited))
            return paths
        pairs = [(0, 1), (0, 2), (3, 1)]
        paths = [find_simple_paths(s, t) for s, t in pairs]
        p_edges = [[[ekey(p[i], p[i+1]) for i in range(len(p)-1)] for p in paths[j]] for j in range(3)]
        all_profiles = list(itertools.product(range(len(paths[0])), range(len(paths[1])), range(len(paths[2]))))

        def potential(prof):
            counts = {}
            for player, path_idx in enumerate(prof):
                for e in p_edges[player][path_idx]:
                    counts[e] = counts.get(e, 0) + 1
            H = [Fraction(0), Fraction(1), Fraction(3, 2), Fraction(11, 6)]
            return sum(edges[e] * H[cnt] for e, cnt in counts.items())

        def profile_cost(prof):
            used = set()
            for player, path_idx in enumerate(prof):
                used.update(p_edges[player][path_idx])
            return sum(edges[e] for e in used)

        min_pot = min(potential(p) for p in all_profiles)
        pot_opt_profiles = [p for p in all_profiles if potential(p) == min_pot]
        opt_cost = min(profile_cost(p) for p in all_profiles)
        pot_opt_cost = profile_cost(pot_opt_profiles[0])
        ratio = Fraction(pot_opt_cost, opt_cost)

        results.append({
            "eps": str(eps),
            "min_potential": str(min_pot),
            "pot_opt_profile": list(pot_opt_profiles[0]),
            "pot_opt_cost": str(pot_opt_cost),
            "opt_cost": str(opt_cost),
            "ratio": str(ratio),
            "ratio_float": float(ratio),
            "target_limit": "286/175",
            "target_limit_float": float(Fraction(286, 175))
        })
    return results

if __name__ == "__main__":
    print("=== Disser et al. (2015) 1769/1126 Reproduction ===")
    disser_res = run_disser_5vertex()
    print(f"Total strategy profiles: {disser_res['total_profiles']}")
    print(f"NE profiles count: {disser_res['ne_profiles_count']} (Profile: {disser_res['ne_profiles'][0]})")
    print(f"NE cost: {disser_res['ne_cost']}, OPT cost: {disser_res['opt_cost']}")
    print(f"Price of Stability ratio: {disser_res['ratio_exact']} = {disser_res['ratio_float']:.8f}")
    print(f"Exact match 1769/1126: {disser_res['matches_expected']}")

    print("\n=== Potential-Optimal 286/175 Family Reproduction ===")
    po_res = run_potential_optimal_family()
    for item in po_res:
        print(f"eps={item['eps']}: pot_opt_cost={item['pot_opt_cost']}, opt_cost={item['opt_cost']}, ratio={item['ratio']} = {item['ratio_float']:.8f}")

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "disser_1769_1126_verification.json"), "w") as f:
        json.dump(disser_res, f, indent=2)
    with open(os.path.join(out_dir, "potential_optimal_286_175_family.json"), "w") as f:
        json.dump(po_res, f, indent=2)
    print("\nResults successfully saved to output directory.")
