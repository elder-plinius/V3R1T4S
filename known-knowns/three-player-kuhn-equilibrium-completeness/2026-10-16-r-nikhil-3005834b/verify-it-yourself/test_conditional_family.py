import copy,json,unittest
from fractions import Fraction as Q
from itertools import permutations
import verify_conditional_family as v
from exact_kuhn import evaluate,walk
from family import family
O=v.norm.ROOT/'attempts/solver/output'
FILES=['normalization_preconditions.json','normalization_dominance.json','restricted_family_certificate.json','terminal_family_certificate.json']
OB=[json.loads((O/p).read_text()) for p in FILES]

class Test(unittest.TestCase):
 def test_positive(self):self.assertEqual(v.verify(*OB)['terminal_records'],312)
 def test_missing_terminal(self):
  x=copy.deepcopy(OB);x[3]['terminals'].pop()
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_duplicate_terminal(self):
  x=copy.deepcopy(OB);x[3]['terminals'][-1]=x[3]['terminals'][0]
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_wrong_terminal_multiplier(self):
  x=copy.deepcopy(OB);e=next(e for e in x[3]['terminals'] if e['equalities']);e['equalities'][0][1][0][1]='99'
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_missing_case(self):
  x=copy.deepcopy(OB);del x[3]['cases']['half']
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_bad_case_assumption(self):
  x=copy.deepcopy(OB);x[3]['cases']['zero'][0]['poly']=[[[0]*32,'1']]
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_missing_table_goal(self):
  x=copy.deepcopy(OB);x[2]['events']=[e for e in x[2]['events'] if e['id']!='f'+str(0)]
  with self.assertRaises((AssertionError,KeyError)):v.verify(*x)
 def test_family_calibration(self):
  cases=[{'b11':Q(1,10),'b21':Q(1,5),'c11':0},{},{'b11':Q(1,5),'b21':Q(1,20),'c11':Q(1,2),'b23':Q(1,20)}]
  for kw in cases:
   p=family(**kw);res=evaluate(p);self.assertTrue(res['is_nash'])
   # All original full-game leaf probabilities match independently built noopening factors.
   indices=[1,2,3,5,6,7,9,10,11,13,14,15,16,18,19,20,22,23,24,26,27,28,30,31,32,33,36,37,40,41,44,45]
   flat=[x for player in p for card in player for x in card]
   for card in range(4):
    for kk in [2,3]:flat[16+4*card+kk]*=1-flat[16+4*card]
   vec=[flat[ix] for ix in indices]
   for deal in permutations(range(4),3):
    ls=v.leaves(deal,v.F.D)
    self.assertEqual(sum(x.value(vec) for x in ls.values()),1)
    # Expected payoff calibration covers every deal, independently of proof coefficients.
    from exact_kuhn import payoff
    expected=[sum(poly.value(vec)*payoff(deal,h)[i] for h,poly in ls.items()) for i in range(3)]
    tree=walk(p,deal)
    self.assertEqual(expected,tree)
if __name__=='__main__':unittest.main()
