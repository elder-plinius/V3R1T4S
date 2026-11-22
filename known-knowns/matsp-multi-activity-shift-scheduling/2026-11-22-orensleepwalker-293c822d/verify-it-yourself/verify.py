"""Independent checker for the optimality certificates (Python standard library only). Usage:
python3 check_certificates.py <instances1_225.zip> <certificates.csv>
The certificate for an instance, from ProblemDefinition.pdf of schedulingbenchmarks.org/matsp:
  (1) every employee e must work at least b_e minutes (constraint 4) in shifts whose lengths are multiples of 15 minutes, so e is on
      duty in at least ceil(b_e / 15) intervals;
  (2) in every interval an on-duty employee is assigned exactly one activity (constraint 7), so the cover counts satisfy
      sum over activities a and intervals i of cover_ia = total on-duty intervals >= W = sum_e ceil(b_e / 15);
  (3) by constraint 8, y_ia >= cover_ia - w_ia with y_ia >= 0 an integer, where w_ia is the maximum cover; summing,
      sum y_ia >= W - M with M = sum over a and i of w_ia;
  (4) the objective is sum y_ia^2 >= sum y_ia (each y_ia is a non-negative integer), so every feasible roster has penalty >= W - M.
If W - M equals the instance's best known penalty, that best known penalty is optimal.
For every row of certificates.csv (instance stem, W, M, bound, best_known) the checker recomputes W and M from the instance file in
the archive, checks bound = W - M, and checks bound = best_known > 0. Prints one line per row and PASS if every row holds."""
import sys, csv, zipfile, math

def read(text):
    sec = {}; cur = None
    for raw in text.splitlines():
        l = raw.strip()
        if not l or l.startswith('#'): continue
        if l.startswith('SECTION_'): cur = l; sec[cur] = []; continue
        sec[cur].append(l)
    mins = [int(l.split(',')[1]) for l in sec['SECTION_STAFF']]
    maxcover = sum(int(l.split(',')[4]) for l in sec['SECTION_COVER'])
    return mins, maxcover

def main(zpath, cpath):
    z = zipfile.ZipFile(zpath); bad = 0; n = 0
    for r in csv.DictReader(open(cpath)):
        mins, M = read(z.read('instances1_225/txt/%s.txt' % r['stem']).decode())
        W = sum(math.ceil(b / 15) for b in mins); bound = W - M; best = int(r['best_known'])
        ok = W == int(r['min_work_intervals']) and M == int(r['max_cover_total']) and bound == int(r['bound']) and bound == best > 0
        n += 1; bad += not ok
        print('%-16s W %6d  M %6d  bound %6d  best known %6d  %s' % (r['stem'], W, M, bound, best, 'ok' if ok else 'FAIL'))
    print('%d certificates checked, %d failed' % (n, bad)); print('PASS' if n and not bad else 'FAIL'); return 0 if n and not bad else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
