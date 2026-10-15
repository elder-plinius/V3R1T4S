"""Run independent basin-hopping pipelines (surrogate PGD 45 s -> exact local search 55 s) over a seed range.

Same search as this run's jobs/job3.sh. Each seed r uses surrogate seed 100+r and local-search seed r, writes its
checkpoints under OUT/r<r>/, prints one line per seed, and on any exact lead G >= 2 runs validate_hit.py (official
SCORING/counterexamples_v2.py included) and stops.

Usage (from the repository root):  python tools/hunt_seeds.py --start 1000 --end 1049 [--inst model_48_idx_6371_eps_3]
      [--out seeds_out] [--classes top6] [--from-incumbent]
--from-incumbent starts every local search from the G=-2 incumbent instead of a fresh surrogate point (intensification).
"""
import argparse, json, os, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(ROOT, 'runs', '2026-10-14-1953'); A = os.path.join(RUN, 'attempts'); DATA = os.path.join(RUN, 'data')
ap = argparse.ArgumentParser()
ap.add_argument('--start', type=int, required=True); ap.add_argument('--end', type=int, required=True)
ap.add_argument('--inst', default='model_48_idx_6371_eps_3'); ap.add_argument('--out', default=os.path.join(ROOT, 'seeds_out'))
ap.add_argument('--classes', default='top6'); ap.add_argument('--from-incumbent', action='store_true')
a = ap.parse_args()
py = [sys.executable, '-I']
inc = os.path.join(RUN, 'incumbent', 'model_48_idx_6371_eps_3_G-2.json')
for r in range(a.start, a.end + 1):
    t0 = time.time(); O = os.path.join(a.out, a.inst, f'r{r}')
    if a.from_incumbent:
        init = inc
    else:
        subprocess.run(py + [os.path.join(A, 'surrogate-attack', 'code', 'surrogate.py'), '--data', DATA, '--inst', a.inst, '--secs', '45',
                             '--out', os.path.join(O, 'sur'), '--steps', '300', '--seed', str(100 + r), '--classes', a.classes],
                       check=True, stdout=subprocess.DEVNULL)
        init = os.path.join(O, 'sur', f'{a.inst}.json')
    beta = '3,3,3,3' if r % 2 == 0 else '5,4,3,3'
    subprocess.run(py + [os.path.join(A, 'evaluator-first-local-search', 'code', 'localsearch.py'), '--data', DATA, '--inst', a.inst,
                         '--secs', '55', '--out', os.path.join(O, 'ls'), '--init', init, '--seed', str(r), '--beta', beta,
                         '--hard', '0,0,0,0', '--mu', '0.1'], check=True, stdout=subprocess.DEVNULL)
    ck = os.path.join(O, 'ls', f'{a.inst}.json'); j = json.load(open(ck))
    print(f'seed {r}: G={j["G"]} class={j["cls"]} ({time.time()-t0:.0f} s) {ck}', flush=True)
    if j['G'] >= 2:
        print('LEAD FOUND: validating', flush=True)
        subprocess.run(py + [os.path.join(A, 'exact-solver', 'code', 'validate_hit.py'), '--data', DATA, '--inst', a.inst,
                             '--ckpt', ck, '--out', os.path.join(O, 'witness')])
        break
