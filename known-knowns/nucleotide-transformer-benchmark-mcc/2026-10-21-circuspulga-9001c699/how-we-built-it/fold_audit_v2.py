# fold_audit v2 (PREREG v2): identical to nt.fold_audit, except rows whose MCC array does not have exactly 10 folds are
# excluded from paired tests and listed (nt.fold_audit crashed on them: HyenaDNA rows with 9/12/13/14 values).
import sys, json, itertools, os
import numpy as np, pandas as pd, ast
path, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(path); d['m'] = d.MCC.apply(lambda s: np.array(ast.literal_eval(s))); d['n'] = d.m.apply(len)
signs = np.array(list(itertools.product([1, -1], repeat=10))); res = {}
bad = d[d.n != 10][['Dataset', 'Model', 'n']].to_dict('records')
for t, g in d.groupby('Dataset'):
    g = g[g.n == 10]
    g = g.assign(mean=g.m.apply(np.mean)).sort_values('mean', ascending=False); rows = list(g.itertuples()); rank = {r.Model: i for i, r in enumerate(rows)}
    pairs = []
    for a, b in itertools.combinations(rows, 2):
        diff = a.m - b.m; obs = abs(diff.mean()); null = np.abs((signs * diff).mean(1))
        pairs.append(dict(a=a.Model, b=b.Model, diff=float(diff.mean()), p=float((null >= obs - 1e-12).mean())))
    adj = [p for p in pairs if abs(rank[p['a']] - rank[p['b']]) == 1]; best = rows[0]
    res[t] = dict(n_models=len(rows), best=best.Model, best_mean=float(best.mean), fold_sd_best=float(best.m.std(ddof=1)),
                  n_pairs=len(pairs), pairs_p_ge_0p05=int(sum(p['p'] >= 0.05 for p in pairs)), adjacent_pairs=len(adj),
                  adjacent_p_ge_0p05=int(sum(p['p'] >= 0.05 for p in adj)),
                  best_vs_second=dict(second=rows[1].Model, diff=float(best.mean - rows[1].mean), p=next(p['p'] for p in pairs if p['a'] == best.Model and p['b'] == rows[1].Model)),
                  models_not_sig_below_best=[p['b'] for p in pairs if p['a'] == best.Model and p['p'] >= 0.05], pairs=pairs)
    print('FAUDIT', t, json.dumps({k: v for k, v in res[t].items() if k != 'pairs'}), flush=True)
json.dump(dict(rows_not_10_folds=bad, tasks=res), open(out, 'w'), indent=1); print('BAD_ROWS', json.dumps(bad))
