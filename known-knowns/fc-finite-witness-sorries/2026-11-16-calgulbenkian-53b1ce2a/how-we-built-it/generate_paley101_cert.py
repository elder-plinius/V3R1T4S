#!/usr/bin/env python3
"""Generate and verify the Paley P(101) certificate for R(6,6) >= 102."""


def main() -> None:
    p = 101
    qrs = sorted({pow(x, 2, p) for x in range(1, p)})
    assert len(qrs) == 50

    qr_mask = sum(1 << r for r in qrs)
    invs = [0] + [pow(b, p - 2, p) for b in range(1, p)]

    def qr_bit(d: int) -> bool:
        return ((qr_mask >> d) & 1) == 1

    def adj(u: int, v: int) -> bool:
        return qr_bit((u + p - v) % p)

    # Verify symmetry, irreflexivity, nonresidue x -> 2x, and inverse invariance
    assert not qr_bit(0)
    for d in range(p):
        assert qr_bit(d) == qr_bit((p - d) % p)
    for d in range(1, p):
        if not qr_bit(d):
            assert qr_bit((2 * d) % p)
    for b in range(1, p):
        c = invs[b]
        assert 0 < c < p and (c * b) % p == 1
        if qr_bit(b):
            for d in range(p):
                if qr_bit(d):
                    assert qr_bit((c * d) % p)

    common_01 = [z for z in range(p) if adj(z, 0) and adj(z, 1)]
    assert len(common_01) == 24

    filter_ops = 0

    def no_clique(k: int, verts: list[int]) -> bool:
        nonlocal filter_ops
        if k == 0:
            return False
        if not verts:
            return True
        x, xs = verts[0], verts[1:]
        nbrs = []
        for y in xs:
            filter_ops += 1
            if adj(x, y):
                nbrs.append(y)
        return no_clique(k - 1, nbrs) and no_clique(k, xs)

    ok = no_clique(4, common_01)
    assert ok

    print(f"prime = {p}")
    print(f"qr_count = {len(qrs)}")
    print(f"qr_mask = {qr_mask}")
    print(f"common_01_len = {len(common_01)}")
    print(f"common_01 = {common_01}")
    print(f"no_4_clique_in_common_01 = {ok}")
    print(f"total_filter_adj_evaluations = {filter_ops}")


if __name__ == "__main__":
    main()
