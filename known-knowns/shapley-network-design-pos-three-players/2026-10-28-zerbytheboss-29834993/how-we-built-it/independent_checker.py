#!/usr/bin/env python3
"""
independent_checker.py

Independent second checker for the 3-player undirected Shapley network design game.
Written independently with distinct control flow, state representations, and verification routines.
Uses exact rational fractions throughout.
"""

from fractions import Fraction
import sys

# Graph specification
# 5 vertices labeled 0..4
# Edges with costs:
EDGES = [
    (0, 1, 2928),
    (0, 2, 599),
    (1, 3, 1692),
    (1, 4, 3545),
    (2, 3, 2967),
    (2, 4, 1483),
    (3, 4, 2226)
]

COMMODITIES = [
    (0, 1), # Player 1: s1 -> t1
    (2, 3), # Player 2: s2 -> t2
    (4, 1)  # Player 3: s3 -> t3
]

def get_paths(adj, s, t):
    res = []
    def dfs(u, target, visited, current_path):
        if u == target:
            res.append(list(current_path))
            return
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                current_path.append(v)
                dfs(v, target, visited, current_path)
                current_path.pop()
                visited.remove(v)
    visited = {s}
    dfs(s, t, visited, [s])
    return res

def main():
    adj = {i: [] for i in range(5)}
    cost_map = {}
    for u, v, w in EDGES:
        adj[u].append(v)
        adj[v].append(u)
        cost_map[(min(u, v), max(u, v))] = Fraction(w)

    strategy_sets = [get_paths(adj, s, t) for s, t in COMMODITIES]

    # Convert paths to edge sets
    def to_edge_set(path):
        es = set()
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            es.add((min(u, v), max(u, v)))
        return frozenset(es)

    strategies = [[to_edge_set(p) for p in strat] for strat in strategy_sets]

    nash_equilibria = []
    social_optimum = None
    min_social_cost = Fraction(10**15)

    for i1, s1 in enumerate(strategies[0]):
        for i2, s2 in enumerate(strategies[1]):
            for i3, s3 in enumerate(strategies[2]):
                current_profile = (s1, s2, s3)
                union_edges = s1 | s2 | s3
                scost = sum(cost_map[e] for e in union_edges)
                if scost < min_social_cost:
                    min_social_cost = scost
                    social_optimum = (i1, i2, i3)

                # Nash check
                is_nash = True
                profile_list = [s1, s2, s3]
                for p_idx in range(3):
                    # Compute player's current cost
                    p_edges = profile_list[p_idx]
                    others = [profile_list[j] for j in range(3) if j != p_idx]
                    current_cost = Fraction(0)
                    for e in p_edges:
                        share_count = 1 + sum(1 for o in others if e in o)
                        current_cost += cost_map[e] / share_count

                    # Check unilateral deviations
                    for alt_edge_set in strategies[p_idx]:
                        if alt_edge_set == p_edges:
                            continue
                        alt_cost = Fraction(0)
                        for e in alt_edge_set:
                            share_count = 1 + sum(1 for o in others if e in o)
                            alt_cost += cost_map[e] / share_count
                        if alt_cost < current_cost:
                            is_nash = False
                            break
                    if not is_nash:
                        break

                if is_nash:
                    nash_equilibria.append(((i1, i2, i3), scost))

    print(f"[Independent Checker] Total Profiles Evaluated: {len(strategies[0]) * len(strategies[1]) * len(strategies[2])}")
    print(f"[Independent Checker] Nash Equilibria Found: {len(nash_equilibria)}")
    for ne_idx, ne_cost in nash_equilibria:
        print(f"  NE Profile index: {ne_idx}, Social Cost: {ne_cost}")
    print(f"[Independent Checker] Social Optimum: {social_optimum}, Minimum Social Cost: {min_social_cost}")

    assert len(nash_equilibria) == 1, "Expected unique Nash equilibrium!"
    cheapest_ne_cost = nash_equilibria[0][1]
    pos = cheapest_ne_cost / min_social_cost
    disser_pos = Fraction(1769, 1126)

    print(f"[Independent Checker] Exact PoS: {pos} ({float(pos):.8f})")
    print(f"[Independent Checker] Disser PoS: {disser_pos} ({float(disser_pos):.8f})")
    assert pos > disser_pos, f"PoS {pos} must exceed Disser PoS {disser_pos}!"
    print("[Independent Checker] VERIFICATION PASSED: PoS strictly exceeds 1769/1126.")

if __name__ == "__main__":
    main()
