import copy, json, sys

def count_part(fresh, out):
    return len(fresh) + sum(max(0, len(e) - 1) for e in out)

def expand_dag(n_in, fresh, out):
    vs = [tuple(1 if j == i else 0 for j in range(n_in)) for i in range(n_in)]
    for expr in fresh:
        v = [0] * n_in
        for t in expr:
            idx, val = t["index"], t["value"]
            for k in range(n_in):
                v[k] += val * vs[idx][k]
        vs.append(tuple(v))
    outs = []
    for expr in out:
        v = [0] * n_in
        for t in expr:
            idx, val = t["index"], t["value"]
            for k in range(n_in):
                v[k] += val * vs[idx][k]
        outs.append(tuple(v))
    return vs, outs

def to_canonical_binary_dag(n_in, fresh_list, out_list):
    fresh = copy.deepcopy(fresh_list)
    out = copy.deepcopy(out_list)
    new_fresh = []
    idx_map = {i: i for i in range(n_in)}
    for old_m, expr in enumerate(fresh):
        cur_terms = [{"index": idx_map[t["index"]], "value": t["value"]} for t in expr]
        while len(cur_terms) > 2:
            t0, t1 = cur_terms[0], cur_terms[1]
            new_idx = n_in + len(new_fresh)
            new_fresh.append([t0, t1])
            cur_terms = [{"index": new_idx, "value": 1}] + cur_terms[2:]
        new_idx = n_in + len(new_fresh)
        new_fresh.append(cur_terms)
        idx_map[n_in + old_m] = new_idx
    new_out = []
    for expr in out:
        cur_terms = [{"index": idx_map[t["index"]], "value": t["value"]} for t in expr]
        while len(cur_terms) >= 2:
            t0, t1 = cur_terms[0], cur_terms[1]
            new_idx = n_in + len(new_fresh)
            new_fresh.append([t0, t1])
            cur_terms = [{"index": new_idx, "value": 1}] + cur_terms[2:]
        new_out.append(cur_terms)
    return new_fresh, new_out

def prune_and_toposort(n_in, fresh, out):
    n_tot = n_in + len(fresh)
    used = set()
    stack = [t["index"] for expr in out for t in expr if t["index"] >= n_in]
    while stack:
        u = stack.pop()
        if u in used or u < n_in:
            continue
        used.add(u)
        for t in fresh[u - n_in]:
            if t["index"] >= n_in:
                stack.append(t["index"])
    visited = set()
    order = []
    def dfs(u):
        if u < n_in or u in visited:
            return
        visited.add(u)
        for t in fresh[u - n_in]:
            dfs(t["index"])
        order.append(u)
    for u in sorted(used):
        dfs(u)
    remap = {i: i for i in range(n_in)}
    new_fresh = []
    for old_u in order:
        new_u = n_in + len(new_fresh)
        remap[old_u] = new_u
        expr = fresh[old_u - n_in]
        new_fresh.append([{"index": remap[t["index"]], "value": t["value"]} for t in expr])
    new_out = [[{"index": remap[t["index"]], "value": t["value"]} for t in expr] for expr in out]
    return new_fresh, new_out

def compute_ancestors(n_in, fresh):
    anc = [set() for _ in range(n_in + len(fresh))]
    for m_idx, expr in enumerate(fresh):
        u = n_in + m_idx
        for t in expr:
            c = t["index"]
            anc[u].add(c)
            anc[u].update(anc[c])
    return anc

def get_exclusive_cone(n_in, fresh, out, target_u):
    n_tot = n_in + len(fresh)
    ref_cnt = [0] * n_tot
    for expr in fresh:
        for t in expr:
            ref_cnt[t["index"]] += 1
    for expr in out:
        for t in expr:
            ref_cnt[t["index"]] += 1
    cone = set()
    stack = []
    for t in fresh[target_u - n_in]:
        c = t["index"]
        if c >= n_in:
            ref_cnt[c] -= 1
            if ref_cnt[c] == 0:
                stack.append(c)
    while stack:
        u = stack.pop()
        if u in cone:
            continue
        cone.add(u)
        for t in fresh[u - n_in]:
            c = t["index"]
            if c >= n_in:
                ref_cnt[c] -= 1
                if ref_cnt[c] == 0:
                    stack.append(c)
    return cone

def fold_single_use_outputs(n_in, fresh, out):
    fresh, out = prune_and_toposort(n_in, fresh, out)
    changed = True
    while changed:
        changed = False
        n_tot = n_in + len(fresh)
        ref_cnt = [0] * n_tot
        for expr in fresh:
            for t in expr:
                ref_cnt[t["index"]] += 1
        for expr in out:
            for t in expr:
                ref_cnt[t["index"]] += 1
        for r_idx, expr in enumerate(out):
            new_expr = []
            did_inline = False
            for t in expr:
                u, s = t["index"], t["value"]
                if u >= n_in and ref_cnt[u] == 1 and not did_inline:
                    for ct in fresh[u - n_in]:
                        new_expr.append({"index": ct["index"], "value": s * ct["value"]})
                    did_inline = True
                    changed = True
                else:
                    new_expr.append(t)
            if did_inline:
                out[r_idx] = new_expr
                fresh, out = prune_and_toposort(n_in, fresh, out)
                break
    return fresh, out

def optimize_dag_deep(n_in, fresh_list, out_list):
    fresh, out = to_canonical_binary_dag(n_in, fresh_list, out_list)
    fresh, out = prune_and_toposort(n_in, fresh, out)
    improved = True
    while improved:
        improved = False
        vars_vec, _ = expand_dag(n_in, fresh, out)
        anc = compute_ancestors(n_in, fresh)
        n_tot = len(vars_vec)
        vec_to_nodes = {}
        for idx, v in enumerate(vars_vec):
            vec_to_nodes.setdefault(v, []).append((idx, 1))
            vec_to_nodes.setdefault(tuple(-x for x in v), []).append((idx, -1))
        for m_idx in range(len(fresh) - 1, -1, -1):
            u = n_in + m_idx
            cone = get_exclusive_cone(n_in, fresh, out, u)
            if not cone:
                continue
            forbidden = cone | {u}
            vu = vars_vec[u]
            found = None
            for a in range(n_tot):
                if a in forbidden or (anc[a] & forbidden):
                    continue
                va = vars_vec[a]
                for sa in (1, -1):
                    rem = tuple(vu[k] - sa * va[k] for k in range(n_in))
                    if rem in vec_to_nodes:
                        for b, sb in vec_to_nodes[rem]:
                            if b != a and b not in forbidden and not (anc[b] & forbidden):
                                found = (a, sa, b, sb)
                                break
                    if found:
                        break
                if found:
                    break
            if found:
                a, sa, b, sb = found
                fresh[m_idx] = [{"index": a, "value": sa}, {"index": b, "value": sb}]
                fresh, out = prune_and_toposort(n_in, fresh, out)
                improved = True
                break
    return fold_single_use_outputs(n_in, fresh, out)

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    n1, n2, n3 = d["n"]
    m = d["m"]
    for fk, ok, nin in (("u_fresh", "u", n1 * n2), ("v_fresh", "v", n2 * n3), ("w_fresh", "w", m)):
        nf, no = optimize_dag_deep(nin, d[fk], d[ok])
        if count_part(nf, no) < count_part(d[fk], d[ok]):
            d[fk], d[ok] = nf, no
    d["complexity"]["reduced"] = sum(count_part(d[fk], d[ok]) for fk, ok in (("u_fresh", "u"), ("v_fresh", "v"), ("w_fresh", "w")))
    json.dump(d, open(sys.argv[2], "w"), indent=2)
