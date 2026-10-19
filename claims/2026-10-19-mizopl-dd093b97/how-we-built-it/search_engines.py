#!/usr/bin/env python3
"""
Fast finite-state BFS solver for Period-2 and Period-3 Outer Engines (L0, R0)
across bases b.
"""
from collections import deque

def solve_outer_period2(b, max_len=30):
    """
    In period 2:
    Step 0->1:
      L1 = L0 + Rev(R0) with incoming carry cM0=1 at right (i=ell-1), outgoing carry 0 at left (i=0).
      R1 = R0 + Rev(L0) with incoming carry 0 at right (which is i=0 in Rev(R1)), outgoing carry cR0=0 at left (i=ell-1 in Rev(R1)).
    Step 1->2:
      L2_raw = L1 + Rev(R1) with incoming carry cM1=0 at right (i=ell-1), outgoing carry 1 at left (i=0).
      R2 = R1 + Rev(L1) with incoming carry 0 at right (i=0 in Rev(R2)), outgoing carry cR1=1 at left (i=ell-1 in Rev(R2)).
    Closure:
      L0[0] = 1
      For i = 1..ell-1: L0[i] = L2_raw[i-1]
      L2_raw[ell-1] = b - 1
      For i = 0..ell-1: R0[ell-1-i] = R2[ell-1-i], and R0[0] = R2[0] = 0.
      And for all i = 0..ell-1: L0[i] + R0[ell-1-i] = s_i, with 0 <= L0[i], R0[ell-1-i] < b.
    """
    # Let's work from i = 0 to ell - 1 (left to right in L0, right to left in R0).
    # At position i:
    # Let cL0_out, cL1_out be the carries OUT of position i to position i-1 in L1 and L2_raw.
    # Let cR0_in, cR1_in be the carries INTO position i from position i-1 in Rev(R1) and Rev(R2).
    # Given (cL0_in, cL1_in) at position i (which are the carries from i+1 into i):
    #   L1[i] = (s_i + cL0_in) % b, with cL0_out = (s_i + cL0_in) // b
    #   Rev(R1)[i] = (s_i + cR0_in) % b, with cR0_out = (s_i + cR0_in) // b
    #   t_i = L1[i] + Rev(R1)[i]
    #   L2_raw[i] = (t_i + cL1_in) % b, with cL1_out = (t_i + cL1_in) // b
    #   Rev(R2)[i] = (t_i + cR1_in) % b, with cR1_out = (t_i + cR1_in) // b
    # Notice! At position i, L0[i] is known (for i=0, L0[0]=1; for i>=1, L0[i] = L2_raw[i-1]).
    # And R0[ell-1-i] = Rev(R2)[i].
    # So we require:
    #   L0[i] + Rev(R2)[i] == s_i, and 0 <= Rev(R2)[i] < b (automatic).
    # Start state before i=0:
    #   cL0_out = 0, cL1_out = 1, cR0_in = 0, cR1_in = 0, prev_L2 = 1 (which is L0[0]).
    # Target state after i = ell - 1:
    #   cL0_in = 1 (cM0), cL1_in = 0 (cM1), cR0_out = 0 (cR0), cR1_out = 1 (cR1),
    #   prev_L2 = b - 1 (L2_raw[ell-1] = b - 1), and at i = ell - 1 we also had Rev(R2)[ell-1] = R0[0] = 0!

    start = (0, 1, 0, 0, 1) # (cL0_need, cL1_need, cR0_in, cR1_in, L0_i)
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        state, path = queue.popleft()
        if len(path) >= max_len:
            continue
        cL0_need, cL1_need, cR0_in, cR1_in, L0_i = state
        for cL0_in in (0, 1):
            for cL1_in in (0, 1):
                # Since s_i = L0_i + Rev(R2)[i], s_i is in [L0_i, L0_i + b - 1]
                for s_i in range(L0_i, L0_i + b):
                    if (s_i + cL0_in) // b != cL0_need:
                        continue
                    L1_i = (s_i + cL0_in) % b
                    R1_rev_i = (s_i + cR0_in) % b
                    cR0_out = (s_i + cR0_in) // b
                    t_i = L1_i + R1_rev_i
                    if (t_i + cL1_in) // b != cL1_need:
                        continue
                    L2_i = (t_i + cL1_in) % b
                    R2_rev_i = (t_i + cR1_in) % b
                    cR1_out = (t_i + cR1_in) // b
                    if L0_i + R2_rev_i != s_i:
                        continue
                    new_path = path + [(L0_i, R2_rev_i)]
                    # Check if this can be the final position i = ell - 1:
                    if (cL0_in == 1 and cL1_in == 0 and cR0_out == 0 and cR1_out == 1
                        and L2_i == b - 1 and R2_rev_i == 0):
                        L0 = [p[0] for p in new_path]
                        R0 = [p[1] for p in reversed(new_path)]
                        return L0, R0
                    next_state = (cL0_in, cL1_in, cR0_out, cR1_out, L2_i)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, new_path))
    return None

if __name__ == "__main__":
    for b in range(3, 60):
        res = solve_outer_period2(b, max_len=40)
        if res is not None:
            L0, R0 = res
            print(f"Base {b:2d}: FOUND Period-2 Outer Engine of len {len(L0)}: L0={L0}, R0={R0}")
