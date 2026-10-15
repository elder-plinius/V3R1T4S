import unittest,json,copy,sys,subprocess
from pathlib import Path
import verify_no_initial_bet as V
F=V.F;ROOT=V.ROOT

def encode(p):return [[list(m),str(c)] for m,c in p.c.items()]
class FullOpeningTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.obj=json.loads((ROOT/'attempts/solver/output/no_initial_bet_certificate.json').read_text())
 def reject(self,obj):
  with self.assertRaises((AssertionError,KeyError,ValueError,TypeError)):V.verify(obj)
 def test_complete(self):self.assertEqual(V.verify(self.obj)['variables'],48)
 def test_missing_contradiction(self):
  o=copy.deepcopy(self.obj);o['positive_bluff'].pop();self.reject(o)
 def test_missing_branch(self):
  o=copy.deepcopy(self.obj);o['zero_bluff']=[];self.reject(o)
 def test_changed_assumption(self):
  o=copy.deepcopy(self.obj);o['positive_bluff'][0]['poly']=encode(F.D['a']);self.reject(o)
 def test_changed_identity(self):
  o=copy.deepcopy(self.obj);ev=next(e for e in o['events'] if e['rule']=='derive');ev['poly']=encode(F.decode(ev['poly'])+1);self.reject(o)
 def test_duplicate_id(self):
  o=copy.deepcopy(self.obj);o['events'][1]['id']=o['events'][0]['id'];self.reject(o)
 def test_coupled_high_forbidden(self):
  inherited={'p':(F.G['z'],'gt')};ev={'rule':'kkt','name':'z','mode':'high','premise':'p','poly':encode(F.D['z']-1),'rel':'eq','id':'z'}
  with self.assertRaises(AssertionError):F.check([ev],inherited)
 def test_pyramid_vertex_rejects_wrong_calls(self):
  ev={'rule':'pyramid_vertex_bet','name':'q','calls':['y','b44'],'poly':encode((F.D['q']-1)*F.G['q']+F.D['y']*F.G['y']+F.D['b44']*F.G['b44']),'rel':'ge','id':'v'}
  with self.assertRaises(AssertionError):F.check([ev])
 def test_p1_call_cap(self):
  ev={'rule':'cap_upperproduct','name':'a42','bet':'C','poly':encode(-(1-F.D['C']-F.D['a42'])*F.G['a42']),'rel':'ge','id':'v'}
  self.assertEqual(F.check([ev])[1],1);ev['bet']='a'
  with self.assertRaises(AssertionError):F.check([ev])
 def test_optimized_python_rejected(self):
  result=subprocess.run([sys.executable,'-O',str(Path(V.__file__))],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  self.assertNotEqual(result.returncode,0);self.assertIn(b'Do not disable proof assertions',result.stderr)
if __name__=='__main__':unittest.main()
