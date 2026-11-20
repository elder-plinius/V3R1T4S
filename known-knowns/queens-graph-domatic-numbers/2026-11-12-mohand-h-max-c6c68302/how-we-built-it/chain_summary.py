"""Summary of the chain from the recorded results (l12.json and state.json of every class): a manifest with one line
per drat-trim check (class, step, verdict, sha256 of the formula file, sha256 and size of the proof file, solving and
checking times) and totals per class. It reads records only; audit_chain.py is the program that checks the files.
Usage: python chain_summary.py chain_root enc K manifest_out"""
import json, os, sys

root, enc, K, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
lines, tot = [], {'checks': 0, 'bytes': 0, 'solve': 0.0, 'check': 0.0, 'max': 0, 'bad': 0}
print('%s: class | checks | verified | proof bytes | solve s | check s' % enc)
for c in range(K):
    d12 = os.path.join(root, '%s-c%02d-l12' % (enc, c)); d4 = os.path.join(root, '%s-c%02d-a4' % (enc, c))
    if not (os.path.exists(os.path.join(d12, 'l12.json')) and os.path.exists(os.path.join(d4, 'state.json'))):
        print('%s: class %2d | not finished' % (enc, c)); tot['bad'] += 1; continue
    recs = [(r['lemma'], r) for r in json.load(open(os.path.join(d12, 'l12.json')))]
    st = json.load(open(os.path.join(d4, 'state.json')))
    last = {}
    for r in st['pieces']:
        last[r['piece']] = r
    recs += [('piece-%02d' % i, last[i]) for i in sorted(last)]
    if st.get('glue'):
        g = dict(st['glue']); g.setdefault('proof_bytes', 2); g.setdefault('solve_s', 0.0)
        recs.append(('glue', g))
    cl = {'checks': 0, 'ver': 0, 'bytes': 0, 'solve': 0.0, 'check': 0.0}
    for name, r in recs:
        v = r.get('drat_trim', '?')
        lines.append('%s c%02d %-8s %-10s cnf=%s proof=%s bytes=%d solve_s=%.1f check_s=%.1f' % (
            enc, c, name, v.replace(' ', '_'), r['cnf_sha256'], r['proof_sha256'], r['proof_bytes'], r['solve_s'], r['verify_s']))
        cl['checks'] += 1; cl['ver'] += v == 's VERIFIED'; cl['bytes'] += r['proof_bytes']; cl['solve'] += r['solve_s']; cl['check'] += r['verify_s']
        tot['max'] = max(tot['max'], r['proof_bytes'])
    print('%s: class %2d | %d | %d | %d | %.0f | %.0f' % (enc, c, cl['checks'], cl['ver'], cl['bytes'], cl['solve'], cl['check']))
    tot['checks'] += cl['checks']; tot['bytes'] += cl['bytes']; tot['solve'] += cl['solve']; tot['check'] += cl['check']
    tot['bad'] += cl['checks'] - cl['ver']
open(out, 'w', newline='\n').write('\n'.join(lines) + '\n')
print('%s: %d checks recorded, %d problems; proof bytes %d in total, largest single proof %d; solving %.0fs, checking %.0fs' % (
    enc, tot['checks'], tot['bad'], tot['bytes'], tot['max'], tot['solve'], tot['check']))
print('CHAIN %s: %s' % (enc, 'ALL RECORDED CHECKS VERIFIED' if tot['bad'] == 0 and tot['checks'] > 0 else 'INCOMPLETE'))
