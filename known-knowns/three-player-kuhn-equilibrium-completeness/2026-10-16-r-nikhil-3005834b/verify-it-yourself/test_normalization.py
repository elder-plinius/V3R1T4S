import copy,json,unittest
from pathlib import Path
import verify_normalization as v
O=v.ROOT/'attempts/solver/output'
OB=[json.loads((O/p).read_text()) for p in ['normalization_preconditions.json','normalization_dominance.json','restricted_family_certificate.json']]
class Test(unittest.TestCase):
 def test_positive(self):self.assertEqual(v.verify(*OB)['dominance_polynomials'],3)
 def test_missing_c12(self):
  x=copy.deepcopy(OB);x[0]['events'].pop()
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_wrong_dominance_goal(self):
  x=copy.deepcopy(OB);x[1]['goals'][0],x[1]['goals'][1]=x[1]['goals'][1],x[1]['goals'][0]
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_dominance_forbidden_equilibrium_premise(self):
  x=copy.deepcopy(OB);x[1]['events'][0]['rule']='kkt_product';x[1]['events'][0]['name']='r'
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_missing_dominance_goal(self):
  x=copy.deepcopy(OB);x[1]['goals'].pop()
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_wrong_dominance_sign(self):
  x=copy.deepcopy(OB);e=x[1]['events'][-1];e['poly'][0][1]=str(-v.Q(e['poly'][0][1]))
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_bad_restricted_proof(self):
  x=copy.deepcopy(OB);x[2]['events'][0]['poly']=[[[0]*len(x[2]['variables']),'-1']]
  with self.assertRaises(AssertionError):v.verify(*x)
 def test_bad_precondition_domain(self):
  x=copy.deepcopy(OB);x[0]['events'][0]['poly']=[[[0]*len(x[0]['variables']),'-1']]
  with self.assertRaises(AssertionError):v.verify(*x)
if __name__=='__main__':unittest.main()
