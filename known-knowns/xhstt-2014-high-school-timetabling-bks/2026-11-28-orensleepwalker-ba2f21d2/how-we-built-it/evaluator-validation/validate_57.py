"""Validate xhstt_eval.py against the archive's own values: every solution listed on each open instance's dataset page (Feasibility value,
Objective value) must be reproduced; values compared as multisets per instance (page names and file ids differ in wording)."""
import sys, re, html, collections, xml.etree.ElementTree as ET
sys.path.insert(0, 'code'); import xhstt_eval as X
tot = bad = 0
for k in ('AU-BG-98', 'DK-FG-12', 'DK-HG-12', 'DK-VG-09', 'NL-KP-03', 'NL-KP-05', 'NL-KP-09', 'UK-SP-06'):
    t = html.unescape(re.sub(r'<[^>]+>', ' | ', open('raw/pages/%s.html' % k, errors='replace').read())); t = re.sub(r'(\s*\|\s*)+', ' | ', t)
    head = re.search(r'The following \(?(feasible)?\)? ?solutions[^:]*:', t); seg = t[head.end():].split('XML file')[0]
    tok = [x.strip() for x in seg.split('|') if x.strip()]; i = tok.index('Received') + 1; feas_only = 'Feasibility value' not in tok[:i]
    page = collections.Counter()
    while i < len(tok):
        name = tok[i]; j = i + 1; nums = []
        while j < len(tok) and re.fullmatch(r'\d+|-', tok[j]): nums.append(tok[j]); j += 1
        if feas_only:
            if nums and nums[0] != '-': page[(0, int(nums[0]))] += 1
        elif len(nums) >= 2 and '-' not in nums[:2]: page[(int(nums[0]), int(nums[1]))] += 1
        i = j + 2

    root = ET.parse('raw/inst/%s.xml' % k).getroot(); inst = X.Instance(root.find('Instances')[0]); ours = collections.Counter()
    for sg in root.find('SolutionGroups'):
        for s in sg.findall('Solution'):
            h, o, _ = X.evaluate(inst, s); ours[(h, o)] += 1
    match = sum((page & ours).values()); tot += sum(page.values()); bad += sum(page.values()) - match
    best = min(ours); print('%-9s page lists %d, reproduced %d | page values %s | ours not on page %s | best ours %s' % (k, sum(page.values()), match, sorted(page), sorted((ours - page).elements()), best), flush=True)
print('total listed', tot, 'not reproduced', bad)
