"""Standalone p1 checker (Python 3 standard library only). Last line: PASS or FAIL.

1. Object files: sha256 of every object/ file against verify-it-yourself/OBJECT_SHA256.txt.
2. Detection: from object/window_and_template.csv, the normalised cross-correlation of the saved S14 data window with
   the saved A38 template on each channel (NCC = sum t (w - mean w) / sqrt(sum (w - mean w)^2), template zero-mean and
   unit-norm); one channel >= 0.6; the two-channel mean D above every one of the 401 null controls' full-span maxima
   (object/null_full_span_maxima.csv); no PDS catalogue row within 5 min (candidate.json).
3. Glitch-catalogue gate G1 (pre-registered after the claim's original panel; see how-we-built-it/PREREG_glitch_gates.md):
   no interval [start, end] of the Liu, Xiao and Li (2025) S14 MH1/MH2 ACC-Spike catalogue (object/glitch_catalogue_*.csv,
   every catalogued interval that overlaps the onset +/- 24 h) overlaps [window start, window start + 450 s]; the
   nearest catalogued spikes after the onset and before the window are recomputed and compared with candidate.json.
4. Gate G2: the frozen glitch rule (|x - median| > 8 max(MAD, 0.5) on the valid raw samples of the 450 s window,
   object/g2_raw_window.csv) flags samples; every flagged sample and every catalogued spike overlapping the window is
   muted from 5 s before to 5 s after (template and data muted at the same samples) in the prepped series
   (object/g2_prepped_window_pm10s.csv, window +/- 33 samples); NCC over the unmuted samples at every lag within
   +/- 33 samples (+/- 10 s); pass if the best lag has a channel with CC >= 0.6 and D > 0.2868 (the null maximum).
"""
import csv, datetime as dt, hashlib, json, math, os, statistics, sys

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); obj = os.path.join(root, 'object')
ok = True


def fail(m):
    global ok
    ok = False; print('mismatch:', m)


def rows(name):
    with open(os.path.join(obj, name), newline='') as f:
        return list(csv.DictReader(f))


def ncc(t, w):
    mw = sum(w) / len(w); wd = [x - mw for x in w]
    return sum(a * b for a, b in zip(t, wd)) / math.sqrt(sum(x * x for x in wd)) / math.sqrt(sum(x * x for x in t))


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def main():
    # 1. object files
    for line in open(os.path.join(here, 'OBJECT_SHA256.txt')):
        h, name = line.split(); p = os.path.join(obj, name)
        if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
            fail('sha256 of object/' + name)
    try:
        cand = json.load(open(os.path.join(obj, 'candidate.json')))
        gg = cand['glitch_catalogue_gates']
    except (ValueError, KeyError) as e:
        fail('candidate.json unreadable: %s' % e)
        return

    # 2. detection
    wt = rows('window_and_template.csv')
    tm = {ch: [float(r['template_' + ch]) for r in wt] for ch in ('mh1', 'mh2')}
    cc = []
    for ch in ('mh1', 'mh2'):
        t = tm[ch]; w = [float(r['data_' + ch]) for r in wt]
        if abs(sum(t)) > 1e-6 or abs(math.sqrt(sum(x * x for x in t)) - 1) > 1e-6:
            fail('template %s not zero-mean unit-norm' % ch)
        cc.append(ncc(t, w))
    D = sum(cc) / 2
    ctrl = [float(r['full_span_max']) for r in rows('null_full_span_maxima.csv')]
    print('detection: NCC MH1 %.4f, MH2 %.4f, D %.4f; controls %d, best control %.4f' % (cc[0], cc[1], D, len(ctrl), max(ctrl)))
    if abs(cc[0] - cand['ncc_mh1']) > 2e-4 or abs(cc[1] - cand['ncc_mh2']) > 2e-4 or abs(D - cand['detection_statistic_D']) > 2e-4:
        fail('recomputed NCC differs from candidate.json')
    if max(cc) < 0.6:
        fail('no channel reaches CC 0.6')
    if len(ctrl) < 401 or not all(D > c for c in ctrl):
        fail('D does not exceed every control')
    if abs(max(ctrl) - max(cand['null_best_phase_randomised_full_span_max'], cand['null_c0_time_reversed_full_span_max'])) > 1e-6:
        fail('control maxima differ from candidate.json')
    if any(abs(r[0]) <= 5 for r in cand['nearest_catalogue_rows_min']):
        fail('a catalogue row lies within 5 minutes')

    # 3. G1
    epoch = dt.datetime(1970, 1, 1)
    ws = dt.datetime.strptime(cand['window_start_utc'][:23], '%Y-%m-%dT%H:%M:%S.%f')
    we = ws + dt.timedelta(seconds=cand['window_s'])
    on = ws + dt.timedelta(seconds=30)
    lo, hi = on - dt.timedelta(hours=24), on + dt.timedelta(hours=24)
    sec = lambda d: d.total_seconds()
    spikes = []
    for ch in ('MH1', 'MH2'):
        fn = 'glitch_catalogue_s14_acc_spike_%s_onset_pm24h.csv' % ch.lower()
        rec = gg['extracts'][fn]
        if hashlib.sha256(open(os.path.join(obj, fn), 'rb').read()).hexdigest() != rec['sha256']:
            fail('sha256 of %s differs from candidate.json' % fn)
        iv = [(T(r['Start time']), T(r['End time']), ch) for r in rows(fn)]
        if len(iv) != rec['rows'] or not all(b >= lo and a <= hi and b >= a for a, b, _ in iv):
            fail('%s: row count or span differs from the extraction rule' % fn)
        spikes += iv
    longest = max(sec(b - a) for a, b, _ in spikes)
    over = [x for x in spikes if x[1] >= ws and x[0] <= we]
    g1 = {'nearest_spike_start_after_onset_s': {}, 'last_spike_end_before_window_s_from_onset': {}}
    for ch in ('MH1', 'MH2'):
        g1['nearest_spike_start_after_onset_s'][ch] = round(min(sec(a - on) for a, b, c in spikes if c == ch and a > on), 3)
        g1['last_spike_end_before_window_s_from_onset'][ch] = round(max(sec(b - on) for a, b, c in spikes if c == ch and b < ws), 3)
    quiet = sum(1 for a, b, c in spikes if dt.datetime(1971, 5, 13, 10) <= a < dt.datetime(1971, 5, 13, 19))
    print('G1: %d catalogued S14 MH1/MH2 spike intervals within the onset +/- 24 h (longest %.3f s); overlapping the window: %d; '
          'nearest start after the onset MH1 %+.3f s, MH2 %+.3f s; last end before the window MH1 %+.3f s, MH2 %+.3f s; '
          'spikes starting 1971-05-13 10:00-19:00 UTC: %d' % (
              len(spikes), longest, len(over), g1['nearest_spike_start_after_onset_s']['MH1'],
              g1['nearest_spike_start_after_onset_s']['MH2'], g1['last_spike_end_before_window_s_from_onset']['MH1'],
              g1['last_spike_end_before_window_s_from_onset']['MH2'], quiet))
    G1 = gg['G1']
    if (len(over) == 0) != G1['pass'] or len(over) != G1['overlapping_intervals']:
        fail('G1 overlap differs from candidate.json')
    for k in ('nearest_spike_start_after_onset_s', 'last_spike_end_before_window_s_from_onset'):
        for ch in ('MH1', 'MH2'):
            if abs(g1[k][ch] - G1[k][ch]) > 2e-3:
                fail('G1 %s %s differs from candidate.json' % (k, ch))
    if quiet != gg['descriptive']['spike_intervals_starting_1971_05_13_10_to_19_utc']:
        fail('descriptive spike count 10:00-19:00 differs from candidate.json')
    if not G1['pass']:
        fail('G1 does not pass')

    # 4. G2
    rate, fs, ns = 6.625, 3.3125, 10 ** 9
    d0 = ws - epoch
    ws_ns = (d0.days * 86400 + d0.seconds) * ns + d0.microseconds * 1000
    spans = [(int(sec(a - epoch) * 1e9) - 5 * ns, int(sec(b - epoch) * 1e9) + 5 * ns) for a, b, c in over]
    flags = {}
    raw = rows('g2_raw_window.csv')
    for ch in ('mh1', 'mh2'):
        x = [float(r['raw_' + ch]) for r in raw]
        v = [r['valid_' + ch] == '1' for r in raw]
        med = statistics.median([a for a, b in zip(x, v) if b])
        xv = [a - med for a in x]
        xvv = [a for a, b in zip(xv, v) if b]
        m2 = statistics.median(xvv)
        mad = statistics.median([abs(a - m2) for a in xvv])
        fl = [k for k in range(len(x)) if v[k] and abs(xv[k]) > 8 * max(mad, 0.5)]
        flags[ch.upper()] = (len(fl), mad)
        for k in fl:
            t = ws_ns + int(k / rate * 1e9)
            spans.append((t - 5 * ns, t + 5 * ns))
    off = {int(r['offset']): (float(r['data_mh1']), float(r['data_mh2'])) for r in rows('g2_prepped_window_pm10s.csv')}
    M = len(wt); best = None; lag0 = None
    for lag in range(-33, 34):
        tt = [ws_ns + (lag + i) * (ns / fs) for i in range(M)]
        keep = [not any(s0 <= t <= s1 for s0, s1 in spans) for t in tt]
        c2 = []
        for c, ch in enumerate(('mh1', 'mh2')):
            t = [a for a, k in zip(tm[ch], keep) if k]
            w = [off[lag + i][c] for i in range(M) if keep[i]]
            c2.append(ncc(t, w))
        rec = dict(lag_s=round(lag / fs, 3), ncc=[round(q, 4) for q in c2], D=round(sum(c2) / 2, 4), muted_samples=keep.count(False))
        if lag == 0:
            lag0 = rec
        if best is None or rec['D'] > best['D']:
            best = rec
    G2 = gg['G2']
    g2_pass = max(best['ncc']) >= 0.6 and best['D'] > G2['threshold_D']
    print('G2: rule-flagged raw samples MH1 %d (MAD %.1f), MH2 %d (MAD %.1f); muted samples %d; lag 0: NCC %.4f / %.4f, D %.4f; '
          'best lag %+.3f s: NCC %.4f / %.4f, D %.4f; threshold D > %.4f -> %s' % (
              flags['MH1'][0], flags['MH1'][1], flags['MH2'][0], flags['MH2'][1], lag0['muted_samples'], lag0['ncc'][0],
              lag0['ncc'][1], lag0['D'], best['lag_s'], best['ncc'][0], best['ncc'][1], best['D'], G2['threshold_D'],
              'pass' if g2_pass else 'fail'))
    if [flags['MH1'][0], flags['MH2'][0]] != [G2['rule_flagged_raw_samples']['MH1'], G2['rule_flagged_raw_samples']['MH2']]:
        fail('G2 flagged-sample counts differ from candidate.json')
    if lag0['muted_samples'] != G2['muted_samples'] or abs(best['lag_s'] - G2['best_lag_s']) > 1e-3:
        fail('G2 muting or best lag differs from candidate.json')
    if any(abs(a - b) > 1.5e-4 for a, b in zip(best['ncc'] + [best['D']], G2['best_ncc'] + [G2['best_D']])):
        fail('G2 NCC differs from candidate.json')
    if g2_pass != G2['pass'] or not g2_pass:
        fail('G2 does not pass')


try:
    main()
except Exception as e:  # a damaged object must end in FAIL, not in a traceback
    fail('checker error: %r' % (e,))
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
