#!/usr/bin/env python3
"""Run the UNMODIFIED Naibbe (PREREG §5: author's default parameters) on the frozen
20-plaintext x 10-seed grid and score each run.

Output: attempts/falsifier/output/naibbe_batch.json with per-run (ptext, seed, T-cell,
mode) stats; and pooled per-mode corpus stats (all 200 runs, A-mode cells vs B-mode
cells as frozen in PREREG §5: L1-L5/I1-I5 -> A; L6-L10/I6-I10 -> B).

Also records the per-plaintext secondary values (mean over the 10 seeds).
"""
from __future__ import annotations
import json, os, sys, time
RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, RUN)
from code.naibbe_run import PTEXTS, SEEDS
OUT = os.path.join(RUN, 'attempts/falsifier/output')
os.makedirs(OUT, exist_ok=True)

def main():
    t0 = time.time()
    runs = []
    from code.naibbe_run import gen_run
    import code.score_gen as sg
    for pname in sorted(PTEXTS):
        p = PTEXTS[pname]
        for seed in SEEDS:
            r = gen_run(pname, seed)
            lines = r['lines']
            s = sg.score_all(lines)
            runs.append({'ptext': pname, 'lang': p['lang'], 'mode': p['dialect'],
                         'seed': seed, 'n_tokens': r['n_tokens'],
                         'n_lines': len(lines), 'stats': s, 'sha': r['sha']})
            print(f"{pname} s{seed}: H1={s['H1']:.3f} S2={s['S2']:.3f} S3={s['S3']:.3f} "
                  f"S1={s['S1_bits']:.4f} S5={s['S5']:.1f} done ({time.time()-t0:.0f}s)",
                  flush=True)
    # pooled per mode (regenerate lines for the mode's runs; deterministic seeds)
    pooled = {}
    for mode in ('A','B'):
        lines = []
        for pname in sorted(PTEXTS):
            if PTEXTS[pname]['dialect']!=mode: continue
            for seed in SEEDS:
                rr = gen_run(pname, seed)
                lines.extend(rr['lines'])
        pooled[mode] = {'n_runs': sum(1 for r in runs if r['mode']==mode),
                        'n_tokens': sum(r['n_tokens'] for r in runs if r['mode']==mode),
                        'stats': sg.score_all(lines)}
    # per-plaintext secondary (mean of 10 seeds, H1 only — the falsifying statistic)
    per_ptext = {}
    for pname in sorted(PTEXTS):
        p = PTEXTS[pname]
        h1s = [r['stats']['H1'] for r in runs if r['ptext']==pname]
        per_ptext[pname] = {'mode': p['dialect'], 'mean_H1': sum(h1s)/len(h1s)}
    json.dump({'runs': runs, 'pooled': pooled, 'per_ptext_H1': per_ptext,
               'seeds': SEEDS, 'seconds': round(time.time()-t0,1)},
              open(os.path.join(OUT, 'naibbe_batch.json'),'w'))
    print(f"\npooled A: H1={pooled['A']['stats']['H1']:.4f} S2={pooled['A']['stats']['S2']:.3f} "
          f"S3={pooled['A']['stats']['S3']:.3f} S1={pooled['A']['stats']['S1_bits']:.4f} "
          f"S5={pooled['A']['stats']['S5']:.1f}%")
    print(f"pooled B: H1={pooled['B']['stats']['H1']:.4f} S2={pooled['B']['stats']['S2']:.3f} "
          f"S3={pooled['B']['stats']['S3']:.3f} S1={pooled['B']['stats']['S1_bits']:.4f} "
          f"S5={pooled['B']['stats']['S5']:.1f}%")
    print("naibbe_batch.json written")

if __name__ == '__main__':
    main()
