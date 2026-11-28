"""Independent XHSTT evaluator (Andy, 2026-11-27), written from the HSEval specification (version 2.15, Nov 2026:
hseval.cgi?op=spec and op=spec&part=constraints; saved in raw/spec/). Python standard library only.
Cost of a constraint at one point of application = Weight * CostFunction(deviation); hard (Required=true) costs add to the infeasibility value,
soft ones to the objective value.
Usage: python3 xhstt_eval.py <archive.xml> [instance id]  -> prints, for every solution of every solution group, (infeasibility, objective).
As a module: Instance(elem), evaluate(inst, solution_elem) -> (infeasibility, objective, per-constraint costs)."""
import sys, math, collections, xml.etree.ElementTree as ET

def txt(e, tag, default=None):
    c = e.find(tag)
    return c.text.strip() if c is not None and c.text is not None else default

class Instance:
    def __init__(self, el):
        self.id = el.attrib['Id']; T = el.find('Times')
        self.times = [t.attrib['Id'] for t in T.findall('Time')]; self.tix = {t: i for i, t in enumerate(self.times)}
        self.tgroups = collections.defaultdict(set)
        for t in T.findall('Time'):
            i = self.tix[t.attrib['Id']]
            for tag in ('Week', 'Day'):
                w = t.find(tag)
                if w is not None: self.tgroups[w.attrib['Reference']].add(i)
            tg = t.find('TimeGroups')
            if tg is not None:
                for g in tg: self.tgroups[g.attrib['Reference']].add(i)
        tgdecl = T.find('TimeGroups')
        if tgdecl is not None:
            for g in tgdecl: self.tgroups.setdefault(g.attrib['Id'], set())
        R = el.find('Resources'); self.rtype = {}; self.rgroups = collections.defaultdict(list)
        rgd = R.find('ResourceGroups')
        if rgd is not None:
            for g in rgd: self.rgroups.setdefault(g.attrib['Id'], [])
        for r in R.findall('Resource'):
            rid = r.attrib['Id']; self.rtype[rid] = r.find('ResourceType').attrib['Reference']
            gs = r.find('ResourceGroups')
            if gs is not None:
                for g in gs: self.rgroups[g.attrib['Reference']].append(rid)
        E = el.find('Events'); self.events = {}; self.eorder = []; self.egroups = collections.defaultdict(list)
        egd = E.find('EventGroups')
        if egd is not None:
            for g in egd: self.egroups.setdefault(g.attrib['Id'], [])
        for e in E.findall('Event'):
            eid = e.attrib['Id']; dur = int(txt(e, 'Duration')); wl = txt(e, 'Workload'); wl = int(wl) if wl is not None else dur
            tm = e.find('Time'); pre_t = self.tix[tm.attrib['Reference']] if tm is not None else None
            ers = []
            rs = e.find('Resources')
            if rs is not None:
                for r in rs.findall('Resource'):
                    w = txt(r, 'Workload'); rt = r.find('ResourceType')
                    ers.append(dict(role=txt(r, 'Role'), pre=r.attrib.get('Reference'), workload=int(w) if w is not None else wl,
                                    rtype=rt.attrib['Reference'] if rt is not None else None))
            rgs = e.find('ResourceGroups')
            if rgs is not None:
                for g in rgs:
                    for rid in self.rgroups[g.attrib['Reference']]: ers.append(dict(role=None, pre=rid, workload=wl, rtype=self.rtype[rid]))
            self.events[eid] = dict(dur=dur, workload=wl, pre_t=pre_t, ers=ers); self.eorder.append(eid)
            c = e.find('Course')
            if c is not None: self.egroups[c.attrib['Reference']].append(eid)
            gs = e.find('EventGroups')
            if gs is not None:
                for g in gs: self.egroups[g.attrib['Reference']].append(eid)
        self.constraints = list(el.find('Constraints')) if el.find('Constraints') is not None else []

    def events_of(self, applies):
        out = []
        egs = applies.find('EventGroups')
        if egs is not None:
            for g in egs: out += self.egroups[g.attrib['Reference']]
        es = applies.find('Events')
        if es is not None: out += [e.attrib['Reference'] for e in es]
        return out

    def resources_of(self, applies):
        out = []
        rgs = applies.find('ResourceGroups')
        if rgs is not None:
            for g in rgs: out += self.rgroups[g.attrib['Reference']]
        rs = applies.find('Resources')
        if rs is not None: out += [r.attrib['Reference'] for r in rs]
        return out

    def timeset(self, el):
        s = set()
        if el is None: return s
        tgs = el.find('TimeGroups')
        if tgs is not None:
            for g in tgs: s |= self.tgroups[g.attrib['Reference']]
        ts = el.find('Times')
        if ts is not None:
            for t in ts: s.add(self.tix[t.attrib['Reference']])
        return s

def read_solution(inst, sol):
    """-> {event id: [solution events]}, each a dict(dur, t (index or None), res: list aligned with the event's event resources)."""
    se = collections.defaultdict(list)
    evs = sol.find('Events')
    for e in (evs if evs is not None else []):
        eid = e.attrib['Reference']; ie = inst.events[eid]
        d = txt(e, 'Duration'); d = int(d) if d is not None else ie['dur']
        tm = e.find('Time'); t = inst.tix[tm.attrib['Reference']] if tm is not None else None
        byrole = {}
        rs = e.find('Resources')
        if rs is not None:
            for r in rs.findall('Resource'): byrole[txt(r, 'Role')] = r.attrib['Reference']
        res = [byrole.get(er['role']) if er['role'] is not None else None for er in ie['ers']]
        se[eid].append(dict(dur=d, t=t, res=res))
    for eid in inst.eorder:
        ie = inst.events[eid]
        if not se[eid]: se[eid].append(dict(dur=ie['dur'], t=None, res=[None] * len(ie['ers'])))
        if sum(s['dur'] for s in se[eid]) != ie['dur']: raise ValueError('durations of %s do not add up' % eid)
        for s in se[eid]:
            if s['t'] is None and ie['pre_t'] is not None: s['t'] = ie['pre_t']
            if ie['pre_t'] is not None and s['t'] != ie['pre_t']: raise ValueError('preassigned time changed: ' + eid)
            if s['t'] is not None and s['t'] + s['dur'] > len(inst.times): raise ValueError('runs past the last time: ' + eid)
            for k, er in enumerate(ie['ers']):
                if s['res'][k] is None and er['pre'] is not None: s['res'][k] = er['pre']
                if er['pre'] is not None and s['res'][k] != er['pre']: raise ValueError('preassigned resource changed: ' + eid)
                if s['res'][k] is not None and er['rtype'] is not None and inst.rtype[s['res'][k]] != er['rtype']: raise ValueError('wrong resource type: ' + eid)
    return se

def evaluate(inst, sol):
    return evaluate_se(inst, read_solution(inst, sol))

def evaluate_se(inst, se):
    n = len(inst.times)
    busy = collections.defaultdict(lambda: [0] * n)      # resource -> number of solution resources attending at each time
    wload = collections.defaultdict(float)
    for eid, subs in se.items():
        ie = inst.events[eid]
        for s in subs:
            for k, r in enumerate(s['res']):
                if r is None: continue
                wload[r] += s['dur'] * ie['ers'][k]['workload'] / ie['dur']
                if s['t'] is not None:
                    for q in range(s['t'], s['t'] + s['dur']): busy[r][q] += 1
    def role_idx(eid, role):
        for k, er in enumerate(inst.events[eid]['ers']):
            if er['role'] == role: return k
        return None
    hard = soft = 0; per = collections.Counter()
    for c in inst.constraints:
        k = c.tag; req = txt(c, 'Required') == 'true'; w = int(txt(c, 'Weight')); cf = txt(c, 'CostFunction')
        f = (lambda d: d) if cf == 'Linear' else (lambda d: d * d) if cf == 'Quadratic' else (lambda d: 1 if d else 0)
        ap = c.find('AppliesTo'); devs = []
        mn = txt(c, 'Minimum'); mx = txt(c, 'Maximum'); mn = int(mn) if mn is not None else None; mx = int(mx) if mx is not None else None
        out = lambda v: (mn - v if mn is not None and v < mn else 0) + (v - mx if mx is not None and v > mx else 0)
        if k in ('AssignResourceConstraint', 'PreferResourcesConstraint'):
            role = txt(c, 'Role')
            if k == 'PreferResourcesConstraint':
                pref = set()
                rgs = c.find('ResourceGroups')
                if rgs is not None:
                    for g in rgs: pref |= set(inst.rgroups[g.attrib['Reference']])
                rs = c.find('Resources')
                if rs is not None: pref |= {r.attrib['Reference'] for r in rs}
            for eid in inst.events_of(ap):
                ri = role_idx(eid, role)
                if ri is None or inst.events[eid]['ers'][ri]['pre'] is not None: continue
                if k == 'AssignResourceConstraint': devs.append(sum(s['dur'] for s in se[eid] if s['res'][ri] is None))
                else: devs.append(sum(s['dur'] for s in se[eid] if s['res'][ri] is not None and s['res'][ri] not in pref))
        elif k in ('AssignTimeConstraint', 'PreferTimesConstraint'):
            pref = inst.timeset(c); dd = txt(c, 'Duration'); dd = int(dd) if dd is not None else None
            for eid in inst.events_of(ap):
                if inst.events[eid]['pre_t'] is not None: continue
                if k == 'AssignTimeConstraint': devs.append(sum(s['dur'] for s in se[eid] if s['t'] is None))
                else: devs.append(sum(s['dur'] for s in se[eid] if s['t'] is not None and (dd is None or s['dur'] == dd) and s['t'] not in pref))
        elif k == 'SplitEventsConstraint':
            a, b = int(txt(c, 'MinimumDuration')), int(txt(c, 'MaximumDuration')); lo, hi = int(txt(c, 'MinimumAmount')), int(txt(c, 'MaximumAmount'))
            for eid in inst.events_of(ap):
                subs = se[eid]; devs.append(sum(1 for s in subs if s['dur'] < a or s['dur'] > b) + max(0, lo - len(subs)) + max(0, len(subs) - hi))
        elif k == 'DistributeSplitEventsConstraint':
            dd = int(txt(c, 'Duration'))
            for eid in inst.events_of(ap): devs.append(out(sum(1 for s in se[eid] if s['dur'] == dd)))
        elif k == 'AvoidSplitAssignmentsConstraint':
            role = txt(c, 'Role')
            for g in ap.find('EventGroups'):
                rs = set()
                for eid in inst.egroups[g.attrib['Reference']]:
                    ri = role_idx(eid, role)
                    rs |= {s['res'][ri] for s in se[eid] if s['res'][ri] is not None}
                devs.append(max(0, len(rs) - 1))
        elif k == 'SpreadEventsConstraint':
            tgs = [(inst.tgroups[g.attrib['Reference']], int(txt(g, 'Minimum')), int(txt(g, 'Maximum'))) for g in c.find('TimeGroups')]
            for g in ap.find('EventGroups'):
                starts = [s['t'] for eid in inst.egroups[g.attrib['Reference']] for s in se[eid] if s['t'] is not None]
                d = 0
                for ts, lo, hi in tgs:
                    m = sum(1 for t in starts if t in ts); d += max(0, lo - m) + max(0, m - hi)
                devs.append(d)
        elif k == 'LinkEventsConstraint':
            for g in ap.find('EventGroups'):
                sets = [set(q for s in se[eid] if s['t'] is not None for q in range(s['t'], s['t'] + s['dur'])) for eid in inst.egroups[g.attrib['Reference']]]
                if not sets: devs.append(0); continue
                devs.append(len(set.union(*sets) - set.intersection(*sets)))
        elif k == 'OrderEventsConstraint':
            for p in ap.find('EventPairs'):
                e1, e2 = p.find('FirstEvent').attrib['Reference'], p.find('SecondEvent').attrib['Reference']
                lo = int(txt(p, 'MinSeparation', '0')); hi = txt(p, 'MaxSeparation'); hi = int(hi) if hi is not None else None
                s1, s2 = se[e1], se[e2]
                if not s1 or not s2 or any(s['t'] is None for s in s1 + s2): devs.append(0); continue
                gap = min(s['t'] for s in s2) - max(s['t'] + s['dur'] for s in s1)
                devs.append(max(0, lo - gap) + (max(0, gap - hi) if hi is not None else 0))
        elif k == 'AvoidClashesConstraint':
            for r in inst.resources_of(ap): devs.append(sum(x - 1 for x in busy[r] if x > 1))
        elif k == 'AvoidUnavailableTimesConstraint':
            un = inst.timeset(c)
            for r in inst.resources_of(ap): devs.append(sum(1 for q in un if busy[r][q] > 0))
        elif k in ('LimitIdleTimesConstraint', 'ClusterBusyTimesConstraint', 'LimitBusyTimesConstraint'):
            tgs = [sorted(inst.tgroups[g.attrib['Reference']]) for g in c.find('TimeGroups')]
            for r in inst.resources_of(ap):
                b = busy[r]
                if k == 'LimitIdleTimesConstraint':
                    idle = 0
                    for ts in tgs:
                        bt = [i for i, q in enumerate(ts) if b[q] > 0]
                        if bt: idle += sum(1 for i in range(bt[0], bt[-1] + 1) if b[ts[i]] == 0)
                    devs.append(out(idle))
                elif k == 'ClusterBusyTimesConstraint':
                    devs.append(out(sum(1 for ts in tgs if any(b[q] > 0 for q in ts))))
                else:
                    d = 0
                    for ts in tgs:
                        m = sum(1 for q in ts if b[q] > 0)
                        if m: d += out(m)
                    devs.append(d)
        elif k == 'LimitWorkloadConstraint':
            for r in inst.resources_of(ap):
                v = wload[r]; d = (mn - v if mn is not None and v < mn else 0) + (v - mx if mx is not None and v > mx else 0)
                devs.append(int(math.ceil(d - 1e-9)) if d > 0 else 0)
        else:
            raise ValueError('unsupported constraint ' + k)
        cost = sum(w * f(d) for d in devs); per[(k, req)] += cost
        if req: hard += cost
        else: soft += cost
    return hard, soft, per

if __name__ == '__main__':
    root = ET.parse(sys.argv[1]).getroot(); only = sys.argv[2] if len(sys.argv) > 2 else None
    insts = {i.attrib['Id']: Instance(i) for i in root.find('Instances') if only is None or i.attrib['Id'] == only}
    sgs = root.find('SolutionGroups')
    for sg in (sgs if sgs is not None else []):
        for s in sg.findall('Solution'):
            ref = s.attrib['Reference']
            if ref not in insts: continue
            rep = s.find('Report'); rv = (txt(rep, 'InfeasibilityValue'), txt(rep, 'ObjectiveValue')) if rep is not None else None
            try: h, o, per = evaluate(insts[ref], s); res = '%d.%d' % (h, o)
            except Exception as ex: res = 'ERROR %s' % ex
            print('%-22s %-45s %-14s report %s' % (ref, sg.attrib.get('Id', '')[:45], res, rv), flush=True)
