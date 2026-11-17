"""Extract rows of the Liu, Xiao and Li (2025) S14 ACC-Spike catalogue for the A38 package (Python standard library only).

Source: doi:10.5281/zenodo.15715187 (archive lunar_ACC-v1.0.1.zip, CC BY 4.0), files catalogs/S14_ACC-Spike_MH1_all.csv
and catalogs/S14_ACC-Spike_MH2_all.csv. SOURCE is either that zip archive (members are found by their catalogs/ path)
or a folder holding the two CSV files. The script refuses a source whose sha256 differs from the recorded values.

Subset rules (the 'Start time' and 'End time' strings are copied verbatim, in source order; the other columns - trace
id, amplitude range, similarity, network, station, mode, component, azimuth, incidence, ellipticity - are dropped):
- window (default; what the package ships): every row whose interval [start, end] overlaps
  [onset - 24 h, onset + 24 h], onset = 1971-05-13 18:40:03.735 UTC. This holds every interval the gate G1 can touch
  (the longest catalogued spike lasts 40.151 s) and the nearest catalogued spikes on both sides of the window.
- year: every row whose start lies in 1971 days 36-365 (1971-02-05 00:00:00 <= start < 1972-01-01 00:00:00), the span
  the A38 scan searched (not shipped: it would copy a year of a third-party catalogue into the package).

usage: python3 extract_spike_subset.py SOURCE OUT_DIR [window|year]
"""
import csv, hashlib, io, os, sys, zipfile, datetime as dt

SRC_SHA = {'MH1': '78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1',
           'MH2': '1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9'}
ONSET = dt.datetime(1971, 5, 13, 18, 40, 3, 735000)
RULES = {'window': ('onset_pm24h', ONSET - dt.timedelta(hours=24), ONSET + dt.timedelta(hours=24)),
         'year': ('1971d036-365', dt.datetime(1971, 2, 5), dt.datetime(1972, 1, 1))}


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def source_bytes(src, ch):
    name = 'S14_ACC-Spike_%s_all.csv' % ch
    if src.lower().endswith('.zip'):
        z = zipfile.ZipFile(src)
        mem = [n for n in z.namelist() if n.endswith('/catalogs/' + name) or n == 'catalogs/' + name]
        if len(mem) != 1:
            sys.exit('archive has no single catalogs/%s' % name)
        return z.read(mem[0])
    return open(os.path.join(src, name), 'rb').read()


def keep_row(mode, a, b, lo, hi):
    if mode == 'window':
        return b >= lo and a <= hi
    return lo <= a < hi


def main():
    src, out = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'window'
    tag, lo, hi = RULES[mode]
    os.makedirs(out, exist_ok=True)
    for ch in ('MH1', 'MH2'):
        b = source_bytes(src, ch)
        h = hashlib.sha256(b).hexdigest()
        if h != SRC_SHA[ch]:
            sys.exit('source S14_ACC-Spike_%s_all.csv has sha256 %s, expected %s' % (ch, h, SRC_SHA[ch]))
        rows = list(csv.DictReader(io.StringIO(b.decode('utf-8'), newline='')))
        keep = [(r['Start time'], r['End time']) for r in rows if keep_row(mode, T(r['Start time']), T(r['End time']), lo, hi)]
        text = 'Start time,End time\n' + ''.join('%s,%s\n' % k for k in keep)
        fn = 'glitch_catalogue_s14_acc_spike_%s_%s.csv' % (ch.lower(), tag)
        with open(os.path.join(out, fn), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print('%s (%s): source rows %d, sha256 %s; kept %d rows -> %s, %d bytes, sha256 %s' % (
            ch, mode, len(rows), h, len(keep), fn, len(text.encode()), hashlib.sha256(text.encode()).hexdigest()))


if __name__ == '__main__':
    main()
