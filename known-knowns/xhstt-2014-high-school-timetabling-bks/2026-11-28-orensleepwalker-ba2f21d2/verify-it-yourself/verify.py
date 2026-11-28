"""Check one XHSTT solution against a record (V3R1T4S, 2026-11-28). Python 3 standard library only; needs xhstt_eval.py (same folder).
Usage: python3 verify.py <instance archive.xml> <solution.xml> <overview best> <dataset-page best>    (bests written infeasibility.objective as on the archive pages, e.g. 12.2330; a feasible best such as 126 may be given as 0.126)
1. The instance archive (as downloaded from the dataset page, with its submitted solutions) must hold exactly one instance; every stored solution is
   evaluated, and the best one must reproduce the dataset-page best exactly (the bank's precondition for the evaluator).
2. The solution file must hold exactly one solution for that instance; structure checks: every solution event names an event of the instance,
   has a positive duration, a known time (if any), known resources of a role the event has; durations add up; preassignments respected
   (xhstt_eval.read_solution).
3. Its (infeasibility, objective) must be hierarchically strictly lower than both bests. Prints PASS or FAIL (exit 1)."""
import sys, os, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import xhstt_eval as X
def best(s): h, o = s.split('.') if '.' in s else ('0', s); return int(h), int(o)
F = lambda v: '(%d, %d)' % v
def main(ipath, spath, ov, pg):
    ov, pg = best(ov), best(pg); bad = []
    iroot = ET.parse(ipath).getroot(); insts = iroot.find('Instances'); assert len(insts) == 1, 'expected one instance'
    inst = X.Instance(insts[0]); stored = []
    for sg in (iroot.find('SolutionGroups') if iroot.find('SolutionGroups') is not None else []):
        for s in sg.findall('Solution'):
            if s.attrib['Reference'] == inst.id: stored.append(X.evaluate(inst, s)[:2])
    sb = min(stored) if stored else None
    print('  instance %s: %d stored solutions, best stored %s, dataset-page best %s   [(infeasibility, objective)]' % (inst.id, len(stored), F(sb) if sb else None, F(pg)))
    if sb != pg: bad.append('best stored solution does not reproduce the dataset-page best')
    sroot = ET.parse(spath).getroot(); sols = [s for s in sroot.iter('Solution')]
    if len(sols) != 1 or sols[0].attrib.get('Reference') != inst.id: bad.append('solution file must hold exactly one solution for ' + inst.id); sols = sols[:1]
    s = sols[0]
    for e in s.find('Events'):
        eid = e.attrib.get('Reference')
        if eid not in inst.events: bad.append('unknown event %s' % eid); continue
        d = X.txt(e, 'Duration')
        if d is not None and int(d) <= 0: bad.append('non-positive duration in %s' % eid)
        t = e.find('Time')
        if t is not None and t.attrib.get('Reference') not in inst.tix: bad.append('unknown time in %s' % eid)
        roles = {er['role'] for er in inst.events[eid]['ers'] if er['role'] is not None}
        rs = e.find('Resources'); seen = []
        for r in (rs.findall('Resource') if rs is not None else []):
            role = X.txt(r, 'Role'); seen.append(role)
            if r.attrib.get('Reference') not in inst.rtype: bad.append('unknown resource in %s' % eid)
            if role not in roles: bad.append('unknown role %s in %s' % (role, eid))
        if len(seen) != len(set(seen)): bad.append('role given twice in %s' % eid)
    if bad: print('  structure:', '; '.join(bad[:5])); print('FAIL'); return 1
    h, o, per = X.evaluate(inst, s)
    print('  solution %s: %s (overview best %s, dataset-page best %s)' % (os.path.basename(spath), F((h, o)), F(ov), F(pg)))
    for (k, req), c in sorted(per.items()):
        if c: print('    %-36s %-4s %d' % (k, 'hard' if req else 'soft', c))
    ok = (h, o) < ov and (h, o) < pg
    print('PASS' if ok else 'FAIL'); return 0 if ok else 1
if __name__ == '__main__':
    if len(sys.argv) != 5: sys.exit(__doc__)
    try: sys.exit(main(*sys.argv[1:]))
    except Exception as ex: print('  error: %s' % ex); print('FAIL'); sys.exit(1)
