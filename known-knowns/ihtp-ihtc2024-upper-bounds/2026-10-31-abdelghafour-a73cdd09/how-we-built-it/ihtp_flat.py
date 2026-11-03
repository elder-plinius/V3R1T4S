"""Convert IHTP JSON <-> flat integer text for the annealer.
export: python3 ihtp_flat.py export inst.json sol.json out.flat
import: python3 ihtp_flat.py import inst.json best.txt out_sol.json"""
import json, sys

def export(ip, sp, op):
    I = json.load(open(ip)); S = json.load(open(sp))
    W = I['weights']; D = I['days']; shn = I['shift_types']; spd = len(shn); NS = D * spd
    ag = {a: i for i, a in enumerate(I['age_groups'])}
    rid = {r['id']: i for i, r in enumerate(I['rooms'])}; tid = {t['id']: i for i, t in enumerate(I['operating_theaters'])}
    uid = {u['id']: i for i, u in enumerate(I['surgeons'])}; pid = {p['id']: i for i, p in enumerate(I['patients'])}
    nid = {n['id']: i for i, n in enumerate(I['nurses'])}
    out = [len(x) if isinstance(x, list) else x for x in (D, spd, I['rooms'], I['operating_theaters'], I['surgeons'], I['patients'], I['occupants'], I['nurses'])]
    out += [W[k] for k in ('room_mixed_age', 'room_nurse_skill', 'continuity_of_care', 'nurse_eccessive_workload', 'open_operating_theater', 'surgeon_transfer', 'patient_delay', 'unscheduled_optional')]
    out += [r['capacity'] for r in I['rooms']]
    for t in I['operating_theaters']: out += t['availability']
    for u in I['surgeons']: out += u['max_surgery_time']
    for p in I['patients']:
        inc = set(p['incompatible_room_ids'] or [])
        out += [int(p['mandatory']), int(p['gender'] == 'A'), ag[p['age_group']], p['length_of_stay'], p['surgery_release_day'],
                p['surgery_due_day'] if p['mandatory'] else D - 1, p['surgery_duration'], uid[p['surgeon_id']]]
        out += [int(r['id'] in inc) for r in I['rooms']] + p['workload_produced'] + p['skill_level_required']
    for o in I['occupants']:
        out += [int(o['gender'] == 'A'), ag[o['age_group']], o['length_of_stay'], rid[o['room_id']]] + o['workload_produced'] + o['skill_level_required']
    for n in I['nurses']:
        ml = [-1] * NS
        for ws in n['working_shifts']: ml[ws['day'] * spd + shn.index(ws['shift'])] = ws['max_load']
        out += [n['skill_level']] + ml
    sol = [[-1, -1, -1] for _ in I['patients']]
    for x in S['patients']:
        if x['admission_day'] != 'none': sol[pid[x['id']]] = [x['admission_day'], rid[x['room']], tid[x['operating_theater']]]
    for s in sol: out += s
    rsn = [[-1] * NS for _ in I['rooms']]
    for x in S['nurses']:
        for a in x['assignments']:
            for rr in a['rooms']:
                s = a['day'] * spd + shn.index(a['shift'])
                assert rsn[rid[rr]][s] == -1, 'double nurse on a room-shift'
                rsn[rid[rr]][s] = nid[x['id']]
    for row in rsn: out += row
    open(op, 'w').write(' '.join(map(str, out)) + '\n')

def imp(ip, bp, op):
    I = json.load(open(ip)); shn = I['shift_types']; spd = len(shn); D = I['days']; NS = D * spd
    v = list(map(int, open(bp).read().split()))
    P = len(I['patients']); R = len(I['rooms'])
    pats = []
    for i, p in enumerate(I['patients']):
        d, r, t = v[3 * i:3 * i + 3]
        pats.append({'id': p['id'], 'admission_day': 'none'} if d < 0 else
                    {'id': p['id'], 'admission_day': d, 'room': I['rooms'][r]['id'], 'operating_theater': I['operating_theaters'][t]['id']})
    rsn = v[3 * P:3 * P + R * NS]
    nurses = []
    for n, x in enumerate(I['nurses']):
        asg = []
        for ws in x['working_shifts']:
            s = ws['day'] * spd + shn.index(ws['shift'])
            asg.append({'day': ws['day'], 'shift': ws['shift'], 'rooms': [I['rooms'][r]['id'] for r in range(R) if rsn[r * NS + s] == n]})
        nurses.append({'id': x['id'], 'assignments': asg})
    json.dump({'patients': pats, 'nurses': nurses}, open(op, 'w'), indent=1)

if __name__ == '__main__':
    (export if sys.argv[1] == 'export' else imp)(*sys.argv[2:5])
