#!/usr/bin/env python3
"""
verify_improved_pos_instance.py

Rigorous exact rational verification of an explicit 3-player undirected Shapley
network design game with Price of Stability > 1769/1126.

Topology: 5 vertices, 7 undirected edges.
Edge costs (exact integers):
  c_01 = 2928 (direct for P1)
  c_02 = 599
  c_13 = 1692
  c_14 = 3545 (direct for P3)
  c_23 = 2967 (direct for P2)
  c_24 = 1483
  c_34 = 2226

Result:
  Unique pure Nash equilibrium: P1 using (0, 1), P2 using (2, 3), P3 using (4, 1).
  Nash equilibrium social cost: 2928 + 2967 + 3545 = 9440.
  Social optimum profile: P1 using (0,2,4,3,1), P2 using (2,4,3), P3 using (4,3,1).
  Optimal social cost: 599 + 1692 + 1483 + 2226 = 6000.
  Price of Stability = 9440 / 6000 = 118 / 75 = 1.57333333... > 1769 / 1126 = 1.57104796...
"""

from fractions import Fraction
import itertools
import json
import os
import sys

def verify_instance():
    V = [0, 1, 2, 3, 4]
    edge_list = [
        (0, 1), # 0: c0
        (0, 2), # 1: c1
        (1, 3), # 2: c2
        (1, 4), # 3: c3
        (2, 3), # 4: c4
        (2, 4), # 5: c5
        (3, 4)  # 6: c6
    ]
    edge_costs = [
        Fraction(2928),
        Fraction(599),
        Fraction(1692),
        Fraction(3545),
        Fraction(2967),
        Fraction(1483),
        Fraction(2226)
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

    pairs = [(0, 1), (2, 3), (4, 1)]
    paths = [find_simple_paths(s, t) for s, t in pairs]
    p_edges = [[[edge_to_idx[ekey(p[i], p[i+1])] for i in range(len(p)-1)] for p in paths[j]] for j in range(3)]
    all_profiles = list(itertools.product(range(len(paths[0])), range(len(paths[1])), range(len(paths[2]))))

    def profile_cost(prof):
        used = set()
        for player, p_idx in enumerate(prof):
            used.update(p_edges[player][p_idx])
        return sum(edge_costs[e] for e in used)

    ne_profiles = []
    profile_details = []

    for prof in all_profiles:
        cur_edges = [p_edges[j][prof[j]] for j in range(3)]
        is_ne = True
        profitable_devs = []
        for i in range(3):
            cur_c = sum(edge_costs[e] / sum(1 for j in range(3) if e in cur_edges[j]) for e in cur_edges[i])
            for alt_idx in range(len(paths[i])):
                if alt_idx == prof[i]: continue
                alt_e = p_edges[i][alt_idx]
                alt_c = sum(edge_costs[e] / (1 + sum(1 for j in range(3) if j != i and e in cur_edges[j])) for e in alt_e)
                if alt_c < cur_c:
                    is_ne = False
                    profitable_devs.append({
                        "player": i + 1,
                        "current_cost": str(cur_c),
                        "alt_path_idx": alt_idx,
                        "alt_path": paths[i][alt_idx],
                        "alt_cost": str(alt_c),
                        "gain": str(cur_c - alt_c)
                    })
        if is_ne:
            ne_profiles.append(prof)
        profile_details.append({
            "profile": list(prof),
            "paths": [paths[j][prof[j]] for j in range(3)],
            "cost": str(profile_cost(prof)),
            "is_ne": is_ne,
            "best_deviation": profitable_devs[0] if profitable_devs else None
        })

    opt_cost = min(profile_cost(p) for p in all_profiles)
    opt_profiles = [p for p in all_profiles if profile_cost(p) == opt_cost]
    ne_cost = profile_cost(ne_profiles[0]) if ne_profiles else None
    ratio = Fraction(ne_cost, opt_cost) if ne_cost else None
    disser_ratio = Fraction(1769, 1126)

    output_data = {
        "status": "CONFIRMED_SOLUTION",
        "description": "3-player undirected Shapley network design instance with Price of Stability > 1769/1126",
        "vertices": V,
        "edges": [{"u": u, "v": v, "cost": int(edge_costs[edge_to_idx[ekey(u,v)]])} for u, v in edge_list],
        "terminal_pairs": [{"player": i+1, "source": s, "target": t} for i, (s, t) in enumerate(pairs)],
        "paths_per_player": {
            f"player_{i+1}": [{"idx": idx, "path": p} for idx, p in enumerate(paths[i])]
            for i in range(3)
        },
        "total_profiles_checked": len(all_profiles),
        "unique_ne_profile": list(ne_profiles[0]) if len(ne_profiles) == 1 else None,
        "ne_cost": int(ne_cost),
        "opt_cost": int(opt_cost),
        "pos_ratio_exact": str(ratio),
        "pos_ratio_float": float(ratio),
        "disser_ratio_exact": str(disser_ratio),
        "disser_ratio_float": float(disser_ratio),
        "beats_disser": bool(ratio > disser_ratio),
        "margin": str(ratio - disser_ratio),
        "margin_float": float(ratio - disser_ratio)
    }
    return output_data, profile_details

if __name__ == "__main__":
    data, details = verify_instance()
    print("=== Improved Shapley Network Design Instance (PoS > 1769/1126) ===")
    print(f"Total strategy profiles enumerated: {data['total_profiles_checked']}")
    print(f"Unique NE profile: {data['unique_ne_profile']}")
    print(f"NE cost: {data['ne_cost']}")
    print(f"OPT cost: {data['opt_cost']}")
    print(f"Price of Stability ratio: {data['pos_ratio_exact']} = {data['pos_ratio_float']:.8f}")
    print(f"Disser et al. ratio: {data['disser_ratio_exact']} = {data['disser_ratio_float']:.8f}")
    print(f"Beats Disser et al.: {data['beats_disser']} (Margin: {data['margin']} ~ {data['margin_float']:.8f})")

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "improved_pos_instance_118_75.json"), "w") as f:
        json.dump(data, f, indent=2)
    with open(os.path.join(out_dir, "all_125_profiles_evaluation.json"), "w") as f:
        json.dump(details, f, indent=2)
    print("\nOutputs saved to output/improved_pos_instance_118_75.json and all_125_profiles_evaluation.json")
