"""Verdict helper for the run_checks.sh script of this claim folder. Standard library only.
Usage: python3 verdict.py MODE RESULT_FILE
MODE is one of: linear, qecc, lp, qubit, audit, negative.
RESULT_FILE holds the output of the checker; its last line is a JSON object.
The script reads INDEX.csv (claimed value) and the-record-we-beat/ (live bounds, neighbour cells) relative to the
folder that contains this verify-it-yourself directory. Prints a line starting with PASS or FAIL."""
import sys, json, csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def last_json(path):
    lines = [l for l in open(path).read().strip().splitlines() if l.strip()]
    return json.loads(lines[-1])


def index_row():
    with open(os.path.join(ROOT, 'INDEX.csv')) as f:
        return list(csv.DictReader(f))[0]


def live():
    return json.load(open(os.path.join(ROOT, 'the-record-we-beat', 'live_bounds.json')))


def rows(name):
    with open(os.path.join(ROOT, 'the-record-we-beat', name)) as f:
        return list(csv.DictReader(f))


def main(mode, rf):
    try:
        r = last_json(rf)
    except Exception as e:
        print('FAIL (checker output unreadable: %s)' % e)
        return 1
    if mode == 'negative':
        print('PASS (negative control rejected)' if r.get('VALID') is False or r.get('consistent') is False
              or r.get('rank_k') is False else 'FAIL (negative control NOT rejected)')
        return 0 if (r.get('VALID') is False or r.get('consistent') is False or r.get('rank_k') is False) else 1
    idx = index_row()
    claimed = int(idx['value'])
    lv = live() if mode != 'audit' else None
    ok = True
    msgs = []
    if mode == 'linear':
        ok = r['rank_k'] and r['min_distance'] == claimed == r['claimed_d'] and r['messages_nonzero'] == r['expected']
        gt = claimed > lv['lower']
        le = claimed <= lv['upper']
        ok = ok and gt and le
        msgs.append('rank k: %s; exact d=%d; live lower=%d (d > lower: %s); live upper=%d (d <= upper: %s); A_d=%d' % (
            r['rank_k'], r['min_distance'], lv['lower'], gt, lv['upper'], le, r['A_d']))
    elif mode == 'qecc':
        gt = claimed > lv['lower']
        le = claimed <= lv['upper']
        ok = r['VALID'] and r['d'] == claimed and gt and le
        msgs.append('exact d=%d; live lower=%d (d > lower: %s); live upper=%d (d <= upper: %s)' % (r['d'], lv['lower'], gt, lv['upper'], le))
        # lower bounds implied by neighbouring live cells (add a qubit; drop a logical qubit; pure puncture)
        best = 0
        for nb in rows('neighbours.csv'):
            best = max(best, int(nb['live_lower']) - int(nb['offset']))
        notimp = best < claimed
        ok = ok and notimp
        msgs.append('best lower bound implied by live neighbours = %d (< claimed %d: %s)' % (best, claimed, notimp))
    elif mode == 'lp':
        D = lv['upper']
        ok = r['VALID'] and r['D'] == D and claimed == D - 1
        msgs.append('certificate excludes d >= D = live upper bound %d; new upper bound %d' % (D, claimed))
        imp = min(int(nb['upper']) + int(nb['offset']) for nb in rows('neighbours.csv'))
        notimp = imp >= D
        ok = ok and notimp
        msgs.append('best upper bound implied by the four live neighbours = %d (>= D: %s, so not implied)' % (imp, notimp))
    elif mode == 'qubit':
        D = lv['upper']
        ok = r['VALID'] and r['d'] == D and claimed == D - 1
        msgs.append('certificate excludes d >= %d = live upper bound; new upper bound %d' % (D, claimed))
        pr = {(int(p['n']), int(p['k'])): int(p['value']) for p in rows('pr_claims.csv')}
        best = None
        for nb in rows('neighbours.csv'):
            n, k = int(nb['n']), int(nb['k'])
            u = int(nb['live_upper'])
            if (n, k) in pr:
                u = min(u, pr[(n, k)])
            v = u + int(nb['offset'])
            best = v if best is None else min(best, v)
        notimp = best >= D
        ok = ok and notimp
        msgs.append('one-step bound implied by live neighbours and merged/open PR values = %d (>= %d: %s)' % (best, D, notimp))
        msgs.append('triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = %s' % idx['closure_of_others'])
    elif mode == 'audit':
        ok = r['VALID'] and r['violations'] == claimed
        msgs.append('violations recomputed = %d, claimed %d' % (r['violations'], claimed))
    print(('PASS' if ok else 'FAIL') + ' ' + '; '.join(msgs))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
