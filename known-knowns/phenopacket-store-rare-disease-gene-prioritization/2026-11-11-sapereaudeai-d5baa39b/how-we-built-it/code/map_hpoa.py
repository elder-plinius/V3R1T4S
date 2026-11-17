"""Map an HPOA release's HPO term ids onto the HPO v2026-06-06 ontology that LIRICAL loads (PREREG.v2).
alt_id -> primary id; obsolete with replaced_by -> replacement; a term still not a live node of hp.json v2026-06-06 ->
the HPO_ID row is dropped (Onset/Frequency/Modifier cells with such a term are blanked). Comment and header lines kept.
usage: python -I map_hpoa.py <hp.obo v2026-06-06> <hp.json v2026-06-06> <in.hpoa> <out.hpoa>"""
import sys, json, re
obo, hj, inp, out = sys.argv[1:5]
alt, repl, obsolete = {}, {}, set()
cur = None
for line in open(obo, encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('[Term]'):
        cur = {}
        continue
    if line.startswith('['):
        cur = None; continue
    if cur is None:
        continue
    if line.startswith('id: HP:'):
        cur['id'] = line[4:].strip()
    elif line.startswith('alt_id: '):
        alt[line[8:].strip()] = cur['id']
    elif line.startswith('is_obsolete: true'):
        obsolete.add(cur['id'])
    elif line.startswith('replaced_by: '):
        repl[cur['id']] = line[13:].strip()
g = json.load(open(hj, encoding='utf-8'))
live = set()
for n in g['graphs'][0]['nodes']:
    m = re.search(r'HP_(\d{7})$', n['id'])
    if m and not n.get('meta', {}).get('deprecated', False):
        live.add('HP:' + m.group(1))
def mp(t):
    t = alt.get(t, t)
    t = repl.get(t, t)
    t = alt.get(t, t)
    return t if t in live else None
stats = dict(rows=0, kept=0, remapped=0, dropped=0, cell_blank=0)
with open(inp, encoding='utf-8') as fi, open(out, 'w', encoding='utf-8', newline='\n') as fo:
    header = None
    for line in fi:
        if line.startswith('#') or header is None and line.startswith('database_id') or line.startswith('DatabaseID'):
            fo.write(line)
            if not line.startswith('#') or line.startswith('#DatabaseID'):
                header = line
            continue
        f = line.rstrip('\n').split('\t')
        stats['rows'] += 1
        hcol = 3
        t = f[hcol]; m = mp(t)
        if m is None:
            stats['dropped'] += 1; continue
        if m != t:
            stats['remapped'] += 1; f[hcol] = m
        for j in range(4, len(f)):
            if re.fullmatch(r'HP:\d{7}', f[j] or ''):
                mj = mp(f[j])
                if mj is None:
                    f[j] = ''; stats['cell_blank'] += 1
                else:
                    f[j] = mj
        stats['kept'] += 1
        fo.write('\t'.join(f) + '\n')
print(inp.split('/')[-1], stats, 'live_terms', len(live))
