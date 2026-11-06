"""Full mp50 geometry and source-witness check; source inputs are obtained separately."""
from pathlib import Path
from fractions import Fraction
import hashlib, json, sys
import mpmath as mp

mp.mp.dps = 50
root = Path(__file__).resolve().parents[1]

def measure(points):
    assert len(points) == 119 and all(len(row) == 4 for row in points)
    assert all(mp.isfinite(v) for row in points for v in row)
    distances = sorted(mp.sqrt(sum((a-b)**2 for a,b in zip(points[i],points[j]))) for i in range(len(points)) for j in range(i))
    radius = min(distances[0]/2, 1-max(mp.sqrt(sum(x*x for x in row)) for row in points))
    return radius, distances

def main():
    assert len(sys.argv) == 3, 'Supply posted hsp4-119.txt and prior hsp4_119.txt paths'
    record = json.loads((root/'the-record-we-beat/record.json').read_text(encoding='utf-8'))
    candidate = (root/'object/candidate.txt').read_bytes()
    posted, prior = [Path(arg).read_bytes() for arg in sys.argv[1:]]
    assert hashlib.sha256(candidate).hexdigest() == record['candidate_sha256']
    assert hashlib.sha256(posted).hexdigest() == record['posted_coordinate_sha256']
    assert hashlib.sha256(prior).hexdigest() == record['stronger_prior']['member_sha256']
    own_rows = [line.split() for line in candidate.decode('ascii').splitlines() if line.strip()]
    posted_lines = [line.split() for line in posted.decode('ascii').splitlines() if line.strip()]
    assert all(int(row[0]) == i for i,row in enumerate(posted_lines[1:],1))
    posted_rows = [row[1:] for row in posted_lines[1:]]
    prior_lines = [line.split() for line in prior.decode('ascii').splitlines() if line.strip()]
    assert prior_lines[0][0] == 'r'
    prior_rows = prior_lines[1:]
    own_r, own_d = measure([[mp.mpf(v) for v in row] for row in own_rows])
    posted_r, posted_d = measure([[mp.mpf(v) for v in row] for row in posted_rows])
    prior_r, _ = measure([[mp.mpf(v) for v in row] for row in prior_rows])
    table = mp.mpf(record['table_value'])
    assert own_r-table >= mp.mpf('1e-10')
    assert own_r-prior_r >= mp.mpf('1e-10')
    assert abs(posted_r-table) <= mp.mpf('1e-11')
    assert max(abs(a-b) for a,b in zip(own_d,posted_d)) > mp.mpf('1e-8')
    p = [[Fraction(v) for v in row] for row in posted_rows]
    squared = sorted(sum((a-b)**2 for a,b in zip(p[i],p[j])) for i in range(len(p)) for j in range(i))
    witness=record['nonisometry_witness']
    assert squared[witness['sorted_index_zero_based']] == Fraction(witness['posted_squared_distance'])
    assert max(sum(v*v for v in row) for row in p) == Fraction(witness['posted_max_norm_squared'])
    p = [[Fraction(v) for v in row] for row in prior_rows]
    assert min(sum((a-b)**2 for a,b in zip(p[i],p[j])) for i in range(len(p)) for j in range(i)) == Fraction(record['stronger_prior']['minimum_pair_squared'])
    assert max(sum(v*v for v in row) for row in p) == Fraction(record['stronger_prior']['max_norm_squared'])
    print(json.dumps({'mpmath_digits':50,'r_star':mp.nstr(own_r,50),'posted_r_star':mp.nstr(posted_r,50),'prior_r_star':mp.nstr(prior_r,50),'pair_constraints_per_object':len(own_d),'source_witnesses':'exact fractions reproduced'},indent=2))
    print('PASS')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('Reason: '+str(exc))
        print('FAIL')
        sys.exit(1)
