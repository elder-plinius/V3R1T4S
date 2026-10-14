"""Export deterministic reconstruction in binary or decimal, without a search."""
import argparse, importlib.util
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--seed',action='store_true');a=p.parse_args()
spec=importlib.util.spec_from_file_location('construction',Path(__file__).with_name('reconstruction.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if a.seed:
 words=sorted({m.apply_perm(perm,rep) for perm in m.build_agammal_1_27() for rep in m.BASE_ORBIT_REPS})
 payload=''.join(str(x)+'\n' for x in words)
else:
 words=m.rebuild_code();payload=''.join(f'{x:027b}\n' for x in words)
a.output.write_text(payload,encoding='ascii');print('EXPORTED',len(words),'words')
