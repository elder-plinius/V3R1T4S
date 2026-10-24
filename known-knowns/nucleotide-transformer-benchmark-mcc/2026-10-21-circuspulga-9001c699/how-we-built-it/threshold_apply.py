# applies the PREREG significance rule: a benchmark.csv gap is meaningful iff paired sign-flip p<0.05 AND |gap| > 2*SE_test (CNN fold-0 bootstrap).
import json, sys
F = json.load(open(sys.argv[1]))['tasks']; N = json.load(open(sys.argv[2])); out = {}
lit = {'H3K9me3': 0.509, 'H3K27ac': 0.546, 'H2AFZ': 0.529, 'H3K4me1': 0.504, 'H3K36me3': 0.650, 'H4K20me1': 0.670, 'H3K27me3': 0.619, 'H3K4me2': 0.607, 'H3K4me3': 0.653, 'H3K9ac': 0.570}
for t, n in N.items():
    thr = 2 * n['test_boot_se_f0']; f = F[t]; pr = f['pairs']
    sig_p = [p for p in pr if p['p'] < 0.05]; both = [p for p in sig_p if abs(p['diff']) > thr]
    b2 = f['best_vs_second']
    out[t] = dict(n_test=n['n_test'], se_test=round(n['test_boot_se_f0'], 4), threshold=round(thr, 4), fold_sd_best=round(f['fold_sd_best'], 4),
                  n_pairs=len(pr), p_lt_0p05=len(sig_p), meaningful=len(both), best_vs_second_gap=round(b2['diff'], 4), best_vs_second_meaningful=bool(b2['p'] < 0.05 and b2['diff'] > thr),
                  generator_gap_vs_csv_best=round(lit[t] - f['best_mean'], 4), generator_gap_exceeds_threshold=bool(lit[t] - f['best_mean'] > thr))
    print('THR', t, json.dumps(out[t]))
json.dump(out, open(sys.argv[3], 'w'), indent=1)
