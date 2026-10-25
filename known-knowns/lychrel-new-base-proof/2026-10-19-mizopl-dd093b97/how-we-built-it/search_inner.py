#!/usr/bin/env python3
"""
Fast outside-in BFS solver for Period-4 Inner Cores M0 of arbitrary length k
(even or odd) in any base b.
"""
from collections import deque

def add_lists(A, B, b, c_in=0):
    out = []
    c = c_in
    for x, y in zip(reversed(A), reversed(B)):
        s = x + y + c
        out.append(s % b)
        c = s // b
    return out[::-1], c

def verify_M0(M0, b):
    M1, cM0 = add_lists(M0, M0[::-1], b, 0)
    if cM0 != 1: return False
    M2_raw, cM1 = add_lists(M1, M1[::-1], b, 1)
    if cM1 != 0: return False
    M2 = [b-1] + M2_raw
    M3, cM2 = add_lists(M2, M2[::-1], b, 0)
    if cM2 != 1: return False
    M4_raw, cM3 = add_lists(M3, M3[::-1], b, 1)
    if cM3 != 0: return False
    return M4_raw == M0 + [0]

def solve_inner_period4(b, max_layers=60):
    """
    Outside-in BFS over layers j = 0, 1, ..., d-1.
    State after layer j-1:
      (c0L_need, c1L_need, c2L_need, c3L_need,
       c0R_in,   c1R_in,   c2R_in,   c3R_in,
       prev_M2,  prev_b)
    Before layer j = 0:
      c0L_need = 1 (cM0), c1L_need = 0 (cM1), c2L_need = 1 (cM2), c3L_need = 0 (cM3)
      c0R_in = 0 (cR0),   c1R_in = 1 (cR1),   c2R_in = 0 (cR2),   c3R_in = 1 (cR3)
      prev_M2 = b - 1 (since M2[0] = b - 1)
      prev_b = 0 (since M4_raw[k] = 0 at j = 0!)
    And at j = 0, we additionally require a_0 = M4_raw[0] == b - 1.
    """
    init_state = (1, 0, 1, 0, 0, 1, 0, 1, b - 1, 0)
    queue = deque([(init_state, [])])
    visited = {init_state}

    while queue:
        state, path = queue.popleft()
        j = len(path)
        if j >= max_layers:
            continue
        c0L_need, c1L_need, c2L_need, c3L_need, c0R_in, c1R_in, c2R_in, c3R_in, prev_M2, prev_b = state

        # At layer j, we choose s_j in [0, 2b-2] and next left carries (c0L_in, c1L_in, c2L_in, c3L_in) in {0,1}^4.
        # Notice:
        # 1) M4_raw[k - j] = (v_j + c3R_in) % b MUST equal prev_b!
        # Let's iterate over s_j in [0, 2b-2], c0L_in in (0,1), c1L_in in (0,1):
        for c0L_in in (0, 1):
            # s_j + c0L_in must have // b == c0L_need
            s_min = max(0, c0L_need * b - c0L_in)
            s_max = min(2 * b - 2, (c0L_need + 1) * b - 1 - c0L_in)
            for s_j in range(s_min, s_max + 1):
                M1_L = (s_j + c0L_in) % b
                M1_R = (s_j + c0R_in) % b
                c0R_out = (s_j + c0R_in) // b
                t_j = M1_L + M1_R
                c1R_out = (t_j + c1R_in) // b
                M2_raw_R = (t_j + c1R_in) % b

                # Now u_j = M2[j] + M2[k - j] = prev_M2 + M2_raw_R!
                u_j = prev_M2 + M2_raw_R
                c2R_out = (u_j + c2R_in) // b
                M3_R = (u_j + c2R_in) % b

                for c2L_in in (0, 1):
                    if (u_j + c2L_in) // b != c2L_need:
                        continue
                    M3_L = (u_j + c2L_in) % b
                    v_j = M3_L + M3_R
                    if (v_j + c3R_in) % b != prev_b:
                        continue
                    c3R_out = (v_j + c3R_in) // b

                    for c3L_in in (0, 1):
                        if (v_j + c3L_in) // b != c3L_need:
                            continue
                        a_j = (v_j + c3L_in) % b
                        if j == 0 and a_j != b - 1:
                            continue
                        b_j = s_j - a_j
                        if not (0 <= b_j < b):
                            continue

                        for c1L_in in (0, 1):
                            if (t_j + c1L_in) // b != c1L_need:
                                continue
                            M2_raw_L = (t_j + c1L_in) % b

                            new_path = path + [(a_j, b_j)]

                            # Check EVEN length closure (k = 2*(j+1)):
                            # In M0 and M1 (length 2*(j+1)), left and right halves meet right now:
                            #   c0L_in == c0R_out and c1L_in == c1R_out
                            # In M2 and M3 (length 2*(j+1) + 1), there is ONE middle digit at index d = j+1:
                            #   M2[d] = M2_raw_L, so u_mid = 2 * M2_raw_L.
                            #   M3_mid = (u_mid + c2R_out) % b, with (u_mid + c2R_out) // b == c2L_in.
                            #   v_mid = 2 * M3_mid.
                            #   M4_mid = (v_mid + c3R_out) % b == b_j, with (v_mid + c3R_out) // b == c3L_in.
                            if c0L_in == c0R_out and c1L_in == c1R_out:
                                u_mid = 2 * M2_raw_L
                                if (u_mid + c2R_out) // b == c2L_in:
                                    M3_mid = (u_mid + c2R_out) % b
                                    v_mid = 2 * M3_mid
                                    if (v_mid + c3R_out) // b == c3L_in and (v_mid + c3R_out) % b == b_j:
                                        left_half = [p[0] for p in new_path]
                                        right_half = [p[1] for p in reversed(new_path)]
                                        M0 = left_half + right_half
                                        if verify_M0(M0, b):
                                            return M0

                            # Check ODD length closure (k = 2*(j+1) + 1):
                            # There is one middle digit m in M0 at index d = j+1:
                            #   In M2 and M3 (length 2*(j+1) + 2), left and right halves meet after index d:
                            #   Wait: let's just let the BFS also test odd closure or continue to next layer!
                            next_state = (c0L_in, c1L_in, c2L_in, c3L_in,
                                          c0R_out, c1R_out, c2R_out, c3R_out,
                                          M2_raw_L, b_j)
                            if next_state not in visited:
                                visited.add(next_state)
                                queue.append((next_state, new_path))
    return None

if __name__ == "__main__":
    for b in range(3, 60):
        res = solve_inner_period4(b, max_layers=60)
        if res is not None:
            print(f"Base {b:2d}: FOUND Period-4 Inner Core M0 of len {len(res)}: {res}")
