"""Verify the pinned packing with exact rational inequalities; no dependencies."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    record=json.loads((ROOT/'the-record-we-beat/record.json').read_text(encoding='utf-8'))
    raw=(ROOT/'object/candidate.txt').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==record['candidate_sha256'], 'object hash differs'
    points=[[Fraction(v) for v in line.split()] for line in raw.decode('ascii').splitlines() if line.strip()]
    assert len(points)==record['n'] and all(len(p)==record['dimension'] for p in points), 'wrong shape'
    radius=Fraction(record['certified_radius'])
    assert 0 < radius < 1, 'radius outside physical range'
    posted=Fraction(record['table_value'])
    assert radius-posted>=Fraction('1e-10'), 'insufficient improvement'
    norms=[sum(x*x for x in p) for p in points]
    assert all(q<=(1-radius)**2 for q in norms), 'container violation'
    squared=sorted(sum((x-y)**2 for x,y in zip(points[i],points[j])) for i in range(len(points)) for j in range(i))
    assert all(q>=4*radius**2 for q in squared), 'overlapping balls'
    witness=record['nonisometry_witness']
    # The source scalar and maximum norm are a dated table-derived receipt.
    # Both distance sets are bounded by 2, so squared gap >4e-8 implies gap >1e-8.
    assert Fraction(witness['posted_max_norm_squared'])<=1
    difference=abs(squared[witness['sorted_index_zero_based']]-Fraction(witness['posted_squared_distance']))
    assert difference>Fraction('4e-8'), 'non-isometry witness does not pass'
    prior=record['stronger_prior']
    upper=Fraction(prior['radius_upper_bound'])
    assert 0 < upper < 1
    assert Fraction(prior['max_norm_squared']) >= (1-upper)**2 or Fraction(prior['minimum_pair_squared']) <= 4*upper**2, 'prior radius upper bound has no witness'
    assert radius-upper>=Fraction('1e-10'), 'insufficient improvement over stronger public prior'
    print(json.dumps({'n':len(points),'pair_constraints':len(squared),'wall_constraints':len(norms),'certified_radius':record['certified_radius'],'table_value':record['table_value'],'candidate_sha256':record['candidate_sha256'],'arithmetic':'exact fractions; no geometric tolerance','scope':'pinned object versus dated source receipt; no live novelty or optimality claim'},indent=2))
    print('PASS')

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('Reason: '+str(exc))
        print('FAIL')
        sys.exit(1)
